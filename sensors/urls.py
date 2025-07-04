from django.urls import path
from .views import receive_sensor_data, get_sensor_data,dashboard_view
from .views import alert_logs
urlpatterns = [
    path('sensor-data/', receive_sensor_data),
    path('sensor-data/recent/', get_sensor_data),
    path('dashboard/', dashboard_view),
    path('sensor-alerts/', alert_logs, name='sensor_alerts'),
]
