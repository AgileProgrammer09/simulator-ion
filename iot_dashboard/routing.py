from django.urls import re_path
from sensors.consumers import SensorDataConsumer

websocket_urlpatterns = [
    re_path(r'ws/sensor-data/$', SensorDataConsumer.as_asgi()),
]
