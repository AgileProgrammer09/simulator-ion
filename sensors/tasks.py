from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import SensorData, AlertLog
from datetime import timedelta
from django.utils import timezone

@shared_task
def send_temperature_alert_email(sensor_id, temperature, timestamp):
    subject = f"🔥 Temperature Alert from {sensor_id}"
    message = f"Sensor ID: {sensor_id}\nTemperature: {temperature}°C\nTimestamp: {timestamp}"

    #  Save alert in DB
    AlertLog.objects.create(
        sensor_id=sensor_id,
        temperature=temperature,
        timestamp=timestamp,
        alert_message=message
    )

    


@shared_task
def delete_old_sensor_data():
    threshold_date = timezone.now() - timedelta(days=30)# threshold timestamp (30 days ago from now)
    deleted_count, _ = SensorData.objects.filter(timestamp__lt=threshold_date).delete()#  Delete all records older than threshold
    return f"Deleted {deleted_count} old records." # Return a message for logs/debugging




