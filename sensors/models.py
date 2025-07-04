from django.db import models


#  This model stores temperature data sent by sensors
class SensorData(models.Model):
    sensor_id = models.CharField(max_length=100)  # ID of the sensor 
    temperature = models.FloatField()             # Temperature value sent by sensor
    timestamp = models.DateTimeField()            # Exact time when data was recorded
    created_at = models.DateTimeField(auto_now_add=True)  # Time when saved to DB

    def __str__(self):
        return f"{self.sensor_id} - {self.temperature}°C"


#  This model logs abnormal temperature alerts (above =>50 or below =>-10)
class AlertLog(models.Model):
    sensor_id = models.CharField(max_length=100)   # ID of the sensor
    temperature = models.FloatField()              # Abnormal temperature value
    timestamp = models.DateTimeField()             # When the data was recorded
    alert_message = models.TextField()             # Alert message shown or emailed
    created_at = models.DateTimeField(auto_now_add=True)  # When alert was logged

    def __str__(self):
        return f"{self.sensor_id} - {self.temperature}°C @ {self.timestamp}"
