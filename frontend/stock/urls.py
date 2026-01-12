from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='stock_dashboard'),
    path('api/predictions/', views.get_predictions, name='get_predictions'),
    path('api/metrics/', views.get_model_metrics, name='get_metrics'),
    path('api/stock-data/', views.get_stock_data, name='get_stock_data'),
    path('api/history/', views.get_prediction_history, name='get_history'),
    path('api/tickers/', views.get_available_tickers, name='get_tickers'),
    path('api/models/<str:ticker>/', views.get_available_models, name='get_models'),
    path('api/predict-future/', views.predict_future, name='predict_future'),
    path('api/train/<str:ticker>/', views.train_ticker, name='train_ticker'),
]
