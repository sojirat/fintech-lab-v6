from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from viewer.views import log_table

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stock/', include('stock.urls')),
    path('logs/', log_table, name='log_table'),
    path('', RedirectView.as_view(url='/stock/', permanent=False)),
]