from django.contrib import admin
from .models import MetricData, ProcessData, AlertData, ThresholdConfig


@admin.register(MetricData)
class MetricDataAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'cpu_usage', 'memory_usage', 'network_up', 'network_down')
    list_filter = ('timestamp',)
    search_fields = ('timestamp',)
    date_hierarchy = 'timestamp'


@admin.register(ProcessData)
class ProcessDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'pid', 'cpu_percent', 'memory_percent', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('name', 'pid')


@admin.register(AlertData)
class AlertDataAdmin(admin.ModelAdmin):
    list_display = ('metric_type', 'threshold', 'current_value', 'triggered_at', 'acknowledged')
    list_filter = ('metric_type', 'triggered_at', 'acknowledged')
    actions = ['mark_acknowledged']

    def mark_acknowledged(self, request, queryset):
        queryset.update(acknowledged=True)
        self.message_user(request, f"已确认 {queryset.count()} 条告警")
    mark_acknowledged.short_description = "标记为已确认"


@admin.register(ThresholdConfig)
class ThresholdConfigAdmin(admin.ModelAdmin):
    list_display = ('cpu', 'memory', 'disk', 'updated_at')
    fields = ('cpu', 'memory', 'disk')

    def has_add_permission(self, request):
        return not ThresholdConfig.objects.exists()
