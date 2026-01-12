from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import numpy as np
import yfinance as yf
import pickle
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import redis
import json
from pymongo import MongoClient
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Company Stock Prediction API",
    description="API for predicting stock prices using LSTM, GRU, and Transformer models for multiple companies (TSLA, AAPL, GOOGL, MSFT, AMZN)",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
REQUEST_COUNT = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('api_request_latency_seconds', 'Request latency', ['endpoint'])
PREDICTION_COUNT = Counter('predictions_total', 'Total predictions made', ['model'])

# Database connections
def get_db_connection():
    """Get PostgreSQL connection"""
    return psycopg2.connect(
        host="db",
        database="fintech",
        user="fintech",
        password="fintech"
    )

def get_redis_client():
    """Get Redis client"""
    return redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

def get_mongo_client():
    """Get MongoDB client"""
    return MongoClient('mongodb://mongo:27017/')

# Initialize database tables
def init_db():
    """Initialize PostgreSQL tables"""
    conn = get_db_connection()
    cur = conn.cursor()

    # Create predictions table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_predictions (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            model_name VARCHAR(50) NOT NULL,
            prediction_date DATE NOT NULL,
            predicted_price FLOAT NOT NULL,
            actual_price FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create model metrics table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS model_metrics (
            id SERIAL PRIMARY KEY,
            model_name VARCHAR(50) NOT NULL,
            rmse FLOAT NOT NULL,
            mae FLOAT NOT NULL,
            mape FLOAT NOT NULL,
            trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create stock data table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_data (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            date DATE NOT NULL,
            open_price FLOAT NOT NULL,
            high_price FLOAT NOT NULL,
            low_price FLOAT NOT NULL,
            close_price FLOAT NOT NULL,
            volume BIGINT NOT NULL,
            UNIQUE(symbol, date)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Database initialized successfully")

# Pydantic models
class PredictionRequest(BaseModel):
    symbol: str = "TSLA"
    model: Optional[str] = "all"  # lstm, gru, transformer, or all
    days_ahead: int = 1

class PredictionResponse(BaseModel):
    symbol: str
    model: str
    predicted_price: float
    prediction_date: str
    cached: bool = False

class ModelMetrics(BaseModel):
    model: str
    rmse: float
    mae: float
    mape: float

class StockData(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int

# Helper functions
def load_model_and_scaler(model_name: str, ticker: str):
    """Load trained model and scaler from files"""
    models_dir = f"/app/models/{ticker}"
    ticker_lower = ticker.lower()
    model_path = os.path.join(models_dir, f"{model_name}_{ticker_lower}_model.h5")
    scaler_path = os.path.join(models_dir, f"{model_name}_{ticker_lower}_scaler.pkl")

    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        raise HTTPException(status_code=404, detail=f"Model {model_name} for {ticker} not found. Please train the model first.")

    from tensorflow.keras.models import load_model
    model = load_model(model_path)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)

    return model, scaler

def get_latest_stock_data(symbol: str = "TSLA", days: int = 60):
    """Fetch latest stock data from yfinance"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days + 30)
    df = yf.download(symbol, start=start_date, end=end_date, progress=False)
    return df

def make_prediction(model_name: str, symbol: str = "TSLA"):
    """Make prediction using specified model"""
    # Check Redis cache first
    redis_client = get_redis_client()
    cache_key = f"prediction:{symbol}:{model_name}:{datetime.now().strftime('%Y-%m-%d')}"

    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached), True

    # Load model and scaler
    model, scaler = load_model_and_scaler(model_name, symbol)

    # Get latest stock data
    df = get_latest_stock_data(symbol, days=90)
    data = df[['Close']].values

    # Scale data
    scaled_data = scaler.transform(data)

    # Prepare sequence (last 60 days)
    sequence_length = 60
    if len(scaled_data) < sequence_length:
        raise HTTPException(status_code=400, detail="Insufficient data for prediction")

    X = scaled_data[-sequence_length:].reshape(1, sequence_length, 1)

    # Make prediction
    predicted_scaled = model.predict(X, verbose=0)
    predicted_price = scaler.inverse_transform(predicted_scaled)[0][0]

    result = {
        "symbol": symbol,
        "model": model_name,
        "predicted_price": float(predicted_price),
        "prediction_date": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    }

    # Cache for 1 hour
    redis_client.setex(cache_key, 3600, json.dumps(result))

    # Save to database
    save_prediction_to_db(result)

    # Log to MongoDB
    log_prediction_to_mongo(result)

    # Update Prometheus metrics
    PREDICTION_COUNT.labels(model=model_name).inc()

    return result, False

def save_prediction_to_db(prediction: dict):
    """Save prediction to PostgreSQL"""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO stock_predictions (symbol, model_name, prediction_date, predicted_price)
        VALUES (%s, %s, %s, %s)
    """, (prediction['symbol'], prediction['model'], prediction['prediction_date'], prediction['predicted_price']))

    conn.commit()
    cur.close()
    conn.close()

def log_prediction_to_mongo(prediction: dict):
    """Log prediction to MongoDB"""
    mongo_client = get_mongo_client()
    db = mongo_client['fintech']
    collection = db['prediction_logs']

    log_entry = {
        **prediction,
        'timestamp': datetime.now(),
        'cached': False
    }

    collection.insert_one(log_entry)

# API Endpoints
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()

@app.get("/")
def root():
    """Root endpoint"""
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    return {
        "message": "Multi-Company Stock Prediction API",
        "version": "1.0.0",
        "supported_tickers": ["TSLA", "AAPL", "GOOGL", "MSFT", "AMZN"],
        "endpoints": {
            "predictions": "/predict",
            "future_predictions": "/predict/future",
            "train_model": "/train/{ticker}",
            "tickers": "/tickers",
            "models": "/models/{ticker}",
            "metrics": "/metrics/models/{ticker}",
            "stock_data": "/stock/{symbol}",
            "history": "/predictions/history",
            "prometheus": "/metrics"
        }
    }

@app.post("/predict", response_model=List[PredictionResponse])
async def predict_stock(request: PredictionRequest):
    """Predict stock price using ML models"""
    start_time = time.time()
    REQUEST_COUNT.labels(method='POST', endpoint='/predict').inc()

    try:
        results = []
        models = ['lstm', 'gru', 'transformer'] if request.model == 'all' else [request.model]

        for model_name in models:
            try:
                prediction, cached = make_prediction(model_name, request.symbol)
                prediction['cached'] = cached
                results.append(prediction)
            except Exception as e:
                print(f"Error with model {model_name}: {str(e)}")
                continue

        if not results:
            raise HTTPException(status_code=500, detail="All models failed to make predictions")

        REQUEST_LATENCY.labels(endpoint='/predict').observe(time.time() - start_time)
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics/models/{ticker}", response_model=List[ModelMetrics])
async def get_model_metrics(ticker: str):
    """Get metrics for all trained models for a specific ticker"""
    REQUEST_COUNT.labels(method='GET', endpoint='/metrics/models').inc()

    models_dir = f"/app/models/{ticker}"
    ticker_lower = ticker.lower()
    metrics_list = []

    for model_name in ['lstm', 'gru', 'transformer']:
        metrics_path = os.path.join(models_dir, f"{model_name}_{ticker_lower}_metrics.pkl")
        if os.path.exists(metrics_path):
            with open(metrics_path, 'rb') as f:
                metrics = pickle.load(f)
                metrics_list.append(metrics)

    return metrics_list

@app.get("/tickers")
async def get_available_tickers():
    """Get list of tickers with trained models"""
    REQUEST_COUNT.labels(method='GET', endpoint='/tickers').inc()

    models_base_dir = "/app/models"
    available_tickers = []

    # Check which ticker directories exist and have at least one model
    for ticker in ['TSLA', 'AAPL', 'GOOGL', 'MSFT', 'AMZN']:
        ticker_dir = os.path.join(models_base_dir, ticker)
        if os.path.exists(ticker_dir):
            # Check if at least one model file exists
            ticker_lower = ticker.lower()
            has_models = False
            for model in ['lstm', 'gru', 'transformer']:
                model_path = os.path.join(ticker_dir, f"{model}_{ticker_lower}_model.h5")
                if os.path.exists(model_path):
                    has_models = True
                    break

            if has_models:
                available_tickers.append({
                    "ticker": ticker,
                    "directory": ticker_dir
                })

    return {
        "available_tickers": available_tickers,
        "count": len(available_tickers)
    }

@app.get("/models/{ticker}")
async def get_available_models(ticker: str):
    """Get list of available models for a specific ticker"""
    REQUEST_COUNT.labels(method='GET', endpoint='/models').inc()

    models_dir = f"/app/models/{ticker}"
    ticker_lower = ticker.lower()
    available_models = []

    if not os.path.exists(models_dir):
        raise HTTPException(status_code=404, detail=f"No models found for ticker {ticker}")

    for model_name in ['lstm', 'gru', 'transformer']:
        model_path = os.path.join(models_dir, f"{model_name}_{ticker_lower}_model.h5")
        scaler_path = os.path.join(models_dir, f"{model_name}_{ticker_lower}_scaler.pkl")
        metrics_path = os.path.join(models_dir, f"{model_name}_{ticker_lower}_metrics.pkl")

        if os.path.exists(model_path):
            model_info = {
                "model_name": model_name,
                "has_scaler": os.path.exists(scaler_path),
                "has_metrics": os.path.exists(metrics_path),
                "model_path": model_path
            }

            # Load metrics if available
            if os.path.exists(metrics_path):
                try:
                    with open(metrics_path, 'rb') as f:
                        metrics = pickle.load(f)
                        model_info['metrics'] = metrics
                except:
                    pass

            available_models.append(model_info)

    return {
        "ticker": ticker,
        "available_models": available_models,
        "count": len(available_models)
    }

@app.get("/stock/{symbol}", response_model=List[StockData])
async def get_stock_data(symbol: str, days: int = 30):
    """Get historical stock data"""
    REQUEST_COUNT.labels(method='GET', endpoint='/stock').inc()

    try:
        df = get_latest_stock_data(symbol, days)

        data = []
        for idx, row in df.iterrows():
            data.append({
                "date": idx.strftime('%Y-%m-%d'),
                "open": float(row['Open']),
                "high": float(row['High']),
                "low": float(row['Low']),
                "close": float(row['Close']),
                "volume": int(row['Volume'])
            })

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predictions/history")
async def get_predictions_history(limit: int = 100):
    """Get prediction history from database"""
    REQUEST_COUNT.labels(method='GET', endpoint='/predictions/history').inc()

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT * FROM stock_predictions
        ORDER BY created_at DESC
        LIMIT %s
    """, (limit,))

    results = cur.fetchall()
    cur.close()
    conn.close()

    return results

@app.get("/metrics")
async def prometheus_metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/predict/future")
async def predict_future(
    ticker: str,
    model: str = "gru",
    periods: int = 30,
    period_type: str = "day"
):
    """Predict future stock prices

    Args:
        ticker: Stock ticker symbol (e.g., AAPL, TSLA)
        model: Model to use (lstm, gru, transformer)
        periods: Number of periods to predict
        period_type: Type of period (day, week, month, year)
    """
    REQUEST_COUNT.labels(method='POST', endpoint='/predict/future').inc()

    try:
        # Check if model exists
        models_dir = f"/app/models/{ticker}"
        ticker_lower = ticker.lower()
        model_path = os.path.join(models_dir, f"{model}_{ticker_lower}_model.h5")

        if not os.path.exists(model_path):
            raise HTTPException(
                status_code=404,
                detail=f"Model {model} for {ticker} not found. Please train the model first using /train/{ticker}"
            )

        # Load model and scaler
        from tensorflow.keras.models import load_model as tf_load_model
        model_obj = tf_load_model(model_path)

        scaler_path = os.path.join(models_dir, f"{model}_{ticker_lower}_scaler.pkl")
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)

        # Get latest stock data
        df = get_latest_stock_data(ticker, days=90)
        data = df[['Close']].values
        scaled_data = scaler.transform(data)

        # Convert periods based on type
        if period_type == "week":
            total_days = periods * 7
        elif period_type == "month":
            total_days = periods * 30
        elif period_type == "year":
            total_days = periods * 365
        else:  # day
            total_days = periods

        # Make rolling predictions
        sequence_length = 60
        predictions = []
        current_sequence = scaled_data[-sequence_length:].copy()

        for _ in range(total_days):
            X = current_sequence.reshape(1, sequence_length, 1)
            pred_scaled = model_obj.predict(X, verbose=0)
            pred_price = scaler.inverse_transform(pred_scaled)[0][0]
            predictions.append(float(pred_price))

            # Update sequence
            current_sequence = np.append(current_sequence[1:], pred_scaled, axis=0)

        # Generate dates
        last_date = df.index[-1]
        future_dates = [
            (last_date + timedelta(days=i+1)).strftime('%Y-%m-%d')
            for i in range(total_days)
        ]

        # Calculate trend
        first_price = predictions[0]
        last_price = predictions[-1]
        trend = "Bullish" if last_price > first_price else "Bearish"
        change_percent = ((last_price - first_price) / first_price) * 100

        return {
            "ticker": ticker,
            "model": model,
            "period_type": period_type,
            "periods": periods,
            "total_days": total_days,
            "predictions": predictions,
            "dates": future_dates,
            "current_price": float(data[-1][0]),
            "predicted_price_at_end": predictions[-1],
            "trend": trend,
            "change_percent": round(change_percent, 2)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train/{ticker}")
async def train_model(ticker: str, background_tasks=None):
    """Train models for a specific ticker

    Args:
        ticker: Stock ticker symbol to train
    """
    REQUEST_COUNT.labels(method='POST', endpoint='/train').inc()

    try:
        import subprocess

        # Check if training script exists
        script_path = "/app/../jupyter/scripts/stock_prediction/train_multi_company.py"

        # Run training in background
        command = [
            "python3",
            script_path,
            "--ticker", ticker,
            "--start-date", "2018-01-01"
        ]

        # Start training process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        return {
            "status": "training_started",
            "ticker": ticker,
            "message": f"Training started for {ticker}. This will take 30-60 minutes.",
            "process_id": process.pid,
            "note": "Check /models/{ticker} endpoint to see when models are available"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")