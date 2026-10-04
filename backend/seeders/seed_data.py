#!/usr/bin/env python
import os
import sys
import random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from django.utils import timezone
from monitoring.models import MetricData, ProcessData, ThresholdConfig


def seed_metrics():
    print("开始生成监控指标数据...")
    
    MetricData.objects.all().delete()
    
    now = timezone.now()
    metrics_to_create = []
    
    for i in range(720):
        timestamp = now - timedelta(seconds=(720 - i) * 5)
        
        cpu_base = random.uniform(30, 70)
        if i % 240 == 0:
            cpu_usage = random.uniform(85, 95)
        else:
            cpu_usage = cpu_base
        
        memory_usage = random.uniform(55, 65)
        memory_total = 16.0
        memory_used = memory_total * memory_usage / 100
        
        disk_usage_c = 60.0 + random.uniform(-2, 2)
        disk_usage_d = 45.0 + random.uniform(-2, 2)
        
        network_up = random.uniform(10, 50)
        network_down = random.uniform(20, 100)
        
        metrics_to_create.append(MetricData(
            timestamp=timestamp,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            memory_total=memory_total,
            memory_used=memory_used,
            disk_usage_c=disk_usage_c,
            disk_usage_d=disk_usage_d,
            network_up=network_up,
            network_down=network_down
        ))
    
    MetricData.objects.bulk_create(metrics_to_create)
    print(f"已生成 {len(metrics_to_create)} 条监控指标数据")


def seed_processes():
    print("开始生成进程数据...")
    
    ProcessData.objects.all().delete()
    
    processes = [
        {'pid': 1001, 'name': 'node', 'cpu': 25.0, 'memory': 12.0},
        {'pid': 1002, 'name': 'python', 'cpu': 15.0, 'memory': 8.0},
        {'pid': 1003, 'name': 'chrome', 'cpu': 12.0, 'memory': 15.0},
        {'pid': 1004, 'name': 'postgres', 'cpu': 8.0, 'memory': 6.0},
        {'pid': 1005, 'name': 'redis', 'cpu': 3.0, 'memory': 2.0},
    ]
    
    for proc in processes:
        ProcessData.objects.create(
            pid=proc['pid'],
            name=proc['name'],
            cpu_percent=proc['cpu'],
            memory_percent=proc['memory']
        )
    
    print(f"已生成 {len(processes)} 条进程数据")


def seed_threshold():
    print("初始化阈值配置...")
    
    ThresholdConfig.get_config()
    print("阈值配置已初始化")


if __name__ == '__main__':
    print("=" * 50)
    print("系统监控数据种子脚本")
    print("=" * 50)
    
    seed_threshold()
    seed_metrics()
    seed_processes()
    
    print("=" * 50)
    print("种子数据生成完成！")
    print("=" * 50)
