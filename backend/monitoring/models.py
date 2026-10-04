from django.db import models


class MetricData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    cpu_usage = models.FloatField(help_text="CPU使用率百分比")
    memory_usage = models.FloatField(help_text="内存使用率百分比")
    memory_total = models.FloatField(default=16.0, help_text="总内存(GB)")
    memory_used = models.FloatField(default=0.0, help_text="已使用内存(GB)")
    disk_usage_c = models.FloatField(default=60.0, help_text="C盘使用率百分比")
    disk_usage_d = models.FloatField(default=45.0, help_text="D盘使用率百分比")
    network_up = models.FloatField(help_text="上行流量(Mbps)")
    network_down = models.FloatField(help_text="下行流量(Mbps)")

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "监控指标"
        verbose_name_plural = "监控指标"

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - CPU: {self.cpu_usage}%"


class ProcessData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    pid = models.IntegerField(help_text="进程ID")
    name = models.CharField(max_length=100, help_text="进程名称")
    cpu_percent = models.FloatField(help_text="CPU使用率")
    memory_percent = models.FloatField(help_text="内存使用率")

    class Meta:
        ordering = ['-cpu_percent']
        verbose_name = "进程数据"
        verbose_name_plural = "进程数据"

    def __str__(self):
        return f"{self.name} (PID: {self.pid})"


class AlertData(models.Model):
    METRIC_TYPES = [
        ('CPU', 'CPU'),
        ('MEMORY', '内存'),
        ('DISK', '磁盘'),
    ]
    
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    threshold = models.FloatField(help_text="阈值")
    current_value = models.FloatField(help_text="当前值")
    triggered_at = models.DateTimeField(auto_now_add=True, help_text="触发时间")
    acknowledged = models.BooleanField(default=False, help_text="是否已确认")

    class Meta:
        ordering = ['-triggered_at']
        verbose_name = "告警记录"
        verbose_name_plural = "告警记录"

    def __str__(self):
        return f"{self.metric_type} 告警 - {self.triggered_at.strftime('%Y-%m-%d %H:%M:%S')}"


class ThresholdConfig(models.Model):
    cpu = models.FloatField(default=80.0, help_text="CPU告警阈值")
    memory = models.FloatField(default=80.0, help_text="内存告警阈值")
    disk = models.FloatField(default=80.0, help_text="磁盘告警阈值")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "阈值配置"
        verbose_name_plural = "阈值配置"

    def __str__(self):
        return f"阈值配置 - CPU: {self.cpu}%, 内存: {self.memory}%, 磁盘: {self.disk}%"

    @classmethod
    def get_config(cls):
        config, created = cls.objects.get_or_create(pk=1)
        return config
