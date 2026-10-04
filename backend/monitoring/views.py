from django.utils import timezone
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .models import MetricData, ProcessData, AlertData, ThresholdConfig
from .serializers import (
    MetricDataSerializer, 
    ProcessDataSerializer, 
    AlertDataSerializer, 
    ThresholdConfigSerializer
)
from datetime import timedelta
import csv
import io


@api_view(['GET'])
def health_check(request):
    return Response({
        'success': True,
        'data': {
            'status': 'healthy',
            'timestamp': timezone.now()
        }
    })


class MetricDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MetricData.objects.all()
    serializer_class = MetricDataSerializer

    @action(detail=False, methods=['get'])
    def latest(self, request):
        latest = MetricData.objects.first()
        if latest:
            serializer = self.get_serializer(latest)
            return Response({
                'success': True,
                'data': serializer.data
            })
        return Response({
            'success': False,
            'message': 'No data available'
        }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def history(self, request):
        range_param = request.query_params.get('range', '1h')
        
        hours_map = {
            '1h': 1,
            '6h': 6,
            '24h': 24,
        }
        hours = hours_map.get(range_param, 1)
        
        time_threshold = timezone.now() - timedelta(hours=hours)
        metrics = MetricData.objects.filter(timestamp__gte=time_threshold).order_by('timestamp')
        
        serializer = self.get_serializer(metrics, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })

    @action(detail=False, methods=['get'])
    def export(self, request):
        range_param = request.query_params.get('range', '1h')
        
        hours_map = {
            '1h': 1,
            '6h': 6,
            '24h': 24,
        }
        hours = hours_map.get(range_param, 1)
        
        time_threshold = timezone.now() - timedelta(hours=hours)
        metrics = MetricData.objects.filter(timestamp__gte=time_threshold).order_by('timestamp')
        
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(['时间', 'CPU使用率(%)', '内存使用率(%)', '总内存(GB)', '已用内存(GB)', 
                         'C盘使用率(%)', 'D盘使用率(%)', '上行(Mbps)', '下行(Mbps)'])
        
        for metric in metrics:
            writer.writerow([
                metric.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                metric.cpu_usage,
                metric.memory_usage,
                metric.memory_total,
                metric.memory_used,
                metric.disk_usage_c,
                metric.disk_usage_d,
                metric.network_up,
                metric.network_down
            ])
        
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="metrics_{range_param}_{timezone.now().strftime("%Y%m%d%H%M%S")}.csv"'
        return response


class ProcessDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProcessData.objects.all()
    serializer_class = ProcessDataSerializer

    @action(detail=False, methods=['get'])
    def top(self, request):
        processes = ProcessData.objects.all()[:10]
        serializer = self.get_serializer(processes, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })


class AlertDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AlertData.objects.all()
    serializer_class = AlertDataSerializer

    def list(self, request, *args, **kwargs):
        alerts = AlertData.objects.all()[:50]
        serializer = self.get_serializer(alerts, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })


@api_view(['GET', 'PUT'])
def threshold_config(request):
    config = ThresholdConfig.get_config()

    if request.method == 'GET':
        serializer = ThresholdConfigSerializer(config)
        return Response({
            'success': True,
            'data': serializer.data
        })

    serializer = ThresholdConfigSerializer(config, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'data': serializer.data
        })

    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


class ThresholdConfigViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        config = ThresholdConfig.get_config()
        serializer = ThresholdConfigSerializer(config)
        return Response({
            'success': True,
            'data': serializer.data
        })

    def update(self, request, pk=None):
        config = ThresholdConfig.get_config()
        serializer = ThresholdConfigSerializer(config, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data
            })
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
