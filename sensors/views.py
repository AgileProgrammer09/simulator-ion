from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.views.decorators.http import require_GET


from .models import SensorData, AlertLog
from .serializers import SensorDataSerializer, AlertLogSerializer
from .tasks import send_temperature_alert_email


#  API to return recent 50 sensor readings (no login required)
@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_sensor_data(request):
    data = SensorData.objects.all().order_by('-timestamp')[:50]  # get latest 50
    serializer = SensorDataSerializer(data, many=True)
    return Response(serializer.data)


#  API to receive new sensor data from simulator or sensor devices
# This view also:
#  stores data to DB
#  sends real-time WebSocket updates
#  sends alert email if temp is abnormal
@csrf_exempt  # use this if sensor is not sending CSRF token 
@api_view(['POST'])
@permission_classes([AllowAny])
def receive_sensor_data(request):
    serializer = SensorDataSerializer(data=request.data)
    
    if serializer.is_valid():
        #  Save valid data to database
        sensor_data: SensorData = serializer.save()
        temp = sensor_data.temperature

        #  Send real-time data to frontend via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "sensor_data",  # WebSocket group name
            {
                "type": "send_sensor_data",  # event name in consumer
                "data": serializer.data,
            }
        )

        #  If temperature is  high or low, trigger alert
        if temp > 25 or temp < 38:
            subject = f"Temperature Alert from {sensor_data.sensor_id}"
            message = (
                f"Sensor ID: {sensor_data.sensor_id}\n"
                f"Temperature: {temp} °C\n"
                f"Timestamp: {sensor_data.timestamp}"
            )

            #  Send immediate alert email to admin
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            #  Also queue background email logging via Celery
            send_temperature_alert_email.delay(
                sensor_data.sensor_id,
                temp,
                str(sensor_data.timestamp)
            )

        return Response({"message": "Data received successfully."})

    #  If data is invalid, return error
    return Response(serializer.errors, status=400)


#  Render the Chart.js dashboard page 
@require_GET
def dashboard_view(request):
    return render(request, 'sensors/dashboard.html')


#  API to fetch the latest 50 alert logs for admin view
@api_view(['GET'])
def alert_logs(request):
    alerts = AlertLog.objects.order_by('-created_at')[:50]
    serializer = AlertLogSerializer(alerts, many=True)
    return Response(serializer.data)
