from django.contrib import admin
from django.urls import path, include
from viewer.views import log_table

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stock/', include('stock.urls')),
    path('', log_table, name='log_table')
]