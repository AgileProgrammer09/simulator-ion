from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AlertLog

@admin.register(AlertLog)
class AlertLogAdmin(admin.ModelAdmin):
    list_display = ('sensor_id', 'temperature', 'timestamp', 'alert_message', 'created_at')
    search_fields = ('sensor_id', 'alert_message')
    list_filter = ('created_at',)
