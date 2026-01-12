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
    try:
        response = requests.post(f"{FASTAPI_URL}/predict", json={"symbol": "TSLA", "model": "all"})
        response.raise_for_status()
        predictions = response.json()
        return JsonResponse({"status": "success", "data": predictions})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def get_model_metrics(request):
    """Get model performance metrics"""
    try:
        response = requests.get(f"{FASTAPI_URL}/metrics/models")
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
