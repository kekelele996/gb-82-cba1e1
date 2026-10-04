from rest_framework import serializers
from .models import MetricData, ProcessData, AlertData, ThresholdConfig


class MetricDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricData
        fields = '__all__'


class ProcessDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessData
        fields = '__all__'


class AlertDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertData
        fields = '__all__'


class ThresholdConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThresholdConfig
        fields = ['cpu', 'memory', 'disk']
