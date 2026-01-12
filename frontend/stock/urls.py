from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='stock_dashboard'),
    path('api/predictions/', views.get_predictions, name='get_predictions'),
    path('api/metrics/', views.get_model_metrics, name='get_metrics'),
    path('api/stock-data/', views.get_stock_data, name='get_stock_data'),
    path('api/history/', views.get_prediction_history, name='get_history'),
]
