from rest_framework import serializers
from .models import SensorData
from .models import AlertLog
from rest_framework import serializers


class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields='__all__'



class AlertLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertLog
        fields = '__all__'




