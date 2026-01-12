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
    title="TSLA Stock Prediction API",
    description="API for predicting TSLA stock prices using LSTM, GRU, and Transformer models",
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
def load_model_and_scaler(model_name: str):
    """Load trained model and scaler from files"""
    models_dir = "/app/models"
    model_path = os.path.join(models_dir, f"{model_name}_tsla_model.h5")
    scaler_path = os.path.join(models_dir, f"{model_name}_scaler.pkl")

    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found. Please train the model first.")

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
    model, scaler = load_model_and_scaler(model_name)

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
        "message": "TSLA Stock Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "predictions": "/predict",
            "metrics": "/metrics/models",
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

@app.get("/metrics/models", response_model=List[ModelMetrics])
async def get_model_metrics():
    """Get metrics for all trained models"""
    REQUEST_COUNT.labels(method='GET', endpoint='/metrics/models').inc()

    models_dir = "/app/models"
    metrics_list = []

    for model_name in ['lstm', 'gru', 'transformer']:
        metrics_path = os.path.join(models_dir, f"{model_name}_metrics.pkl")
        if os.path.exists(metrics_path):
            with open(metrics_path, 'rb') as f:
                metrics = pickle.load(f)
                metrics_list.append(metrics)

    return metrics_list

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