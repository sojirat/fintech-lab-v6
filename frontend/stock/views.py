from django.shortcuts import render
from django.http import JsonResponse
import requests
from datetime import datetime
import json

FASTAPI_URL = "http://fastapi:8000"

def index(request):
    """Main dashboard page"""
    return render(request, 'stock/dashboard.html')

def get_predictions(request):
    """Get stock predictions from FastAPI"""
    symbol = request.GET.get('symbol', 'AAPL')  # Default to AAPL
    model = request.GET.get('model', 'all')     # Default to all models

    try:
        response = requests.post(f"{FASTAPI_URL}/predict", json={"symbol": symbol, "model": model})
        response.raise_for_status()
        predictions = response.json()
        return JsonResponse({"status": "success", "data": predictions})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def get_model_metrics(request):
    """Get model performance metrics for a specific ticker"""
    ticker = request.GET.get('ticker', 'AAPL')  # Default to AAPL

    try:
        response = requests.get(f"{FASTAPI_URL}/metrics/models/{ticker}")
        response.raise_for_status()
        metrics = response.json()
        return JsonResponse({"status": "success", "data": metrics})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def get_stock_data(request):
    """Get historical stock data"""
    symbol = request.GET.get('symbol', 'TSLA')
    days = request.GET.get('days', 30)

    try:
        response = requests.get(f"{FASTAPI_URL}/stock/{symbol}?days={days}")
        response.raise_for_status()
        data = response.json()
        return JsonResponse({"status": "success", "data": data})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def get_prediction_history(request):
    """Get prediction history"""
    limit = request.GET.get('limit', 100)

    try:
        response = requests.get(f"{FASTAPI_URL}/predictions/history?limit={limit}")
        response.raise_for_status()
        history = response.json()
        return JsonResponse({"status": "success", "data": history})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def get_available_tickers(request):
    """Get list of available tickers with trained models"""
    try:
        response = requests.get(f"{FASTAPI_URL}/tickers")
        response.raise_for_status()
        tickers = response.json()
        return JsonResponse({"status": "success", "data": tickers})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def get_available_models(request, ticker):
    """Get list of available models for a specific ticker"""
    try:
        response = requests.get(f"{FASTAPI_URL}/models/{ticker}")
        response.raise_for_status()
        models = response.json()
        return JsonResponse({"status": "success", "data": models})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def predict_future(request):
    """Get future predictions for a ticker"""
    ticker = request.GET.get('ticker', 'AAPL')
    model = request.GET.get('model', 'gru')
    periods = int(request.GET.get('periods', 30))
    period_type = request.GET.get('period_type', 'day')

    try:
        response = requests.post(
            f"{FASTAPI_URL}/predict/future",
            params={
                "ticker": ticker,
                "model": model,
                "periods": periods,
                "period_type": period_type
            }
        )
        response.raise_for_status()
        predictions = response.json()
        return JsonResponse({"status": "success", "data": predictions})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def train_ticker(request, ticker):
    """Start training models for a specific ticker"""
    try:
        response = requests.post(f"{FASTAPI_URL}/train/{ticker}")
        response.raise_for_status()
        result = response.json()
        return JsonResponse({"status": "success", "data": result})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
