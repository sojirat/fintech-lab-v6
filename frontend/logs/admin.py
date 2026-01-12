from django.contrib import admin
from .models import PredictionLog

@admin.register(PredictionLog)
class PredictionLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'endpoint', 'client', 'prediction')
    search_fields = ('endpoint', 'client')
    list_filter = ('endpoint',)
    ordering = ('-timestamp',)