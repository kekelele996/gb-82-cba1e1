import random
import os
import logging
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .models import MetricData, ProcessData, AlertData, ThresholdConfig

logger = logging.getLogger(__name__)

scheduler = None


def collect_metrics():
    try:
        config = ThresholdConfig.get_config()
        
        cpu_base = random.uniform(30, 70)
        cpu_spike_chance = random.random()
        if cpu_spike_chance < 0.05:
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
        
        metric = MetricData.objects.create(
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            memory_total=memory_total,
            memory_used=memory_used,
            disk_usage_c=disk_usage_c,
            disk_usage_d=disk_usage_d,
            network_up=network_up,
            network_down=network_down
        )
        
        if cpu_usage > config.cpu:
            AlertData.objects.create(
                metric_type='CPU',
                threshold=config.cpu,
                current_value=cpu_usage
            )
        
        if memory_usage > config.memory:
            AlertData.objects.create(
                metric_type='MEMORY',
                threshold=config.memory,
                current_value=memory_usage
            )
        
        logger.info(f"Collected metrics: CPU={cpu_usage:.1f}%, Memory={memory_usage:.1f}%")
    except Exception as e:
        logger.error(f"Error collecting metrics: {e}")


def collect_processes():
    try:
        ProcessData.objects.all().delete()
        
        processes = [
            {'pid': 1001, 'name': 'node', 'cpu': 25 + random.uniform(-5, 5), 'memory': 12 + random.uniform(-2, 2)},
            {'pid': 1002, 'name': 'python', 'cpu': 15 + random.uniform(-3, 3), 'memory': 8 + random.uniform(-1, 1)},
            {'pid': 1003, 'name': 'chrome', 'cpu': 12 + random.uniform(-4, 4), 'memory': 15 + random.uniform(-3, 3)},
            {'pid': 1004, 'name': 'postgres', 'cpu': 8 + random.uniform(-2, 2), 'memory': 6 + random.uniform(-1, 1)},
            {'pid': 1005, 'name': 'redis', 'cpu': 3 + random.uniform(-1, 1), 'memory': 2 + random.uniform(-0.5, 0.5)},
        ]
        
        for proc in processes:
            ProcessData.objects.create(
                pid=proc['pid'],
                name=proc['name'],
                cpu_percent=proc['cpu'],
                memory_percent=proc['memory']
            )
        
        logger.info("Collected process data")
    except Exception as e:
        logger.error(f"Error collecting processes: {e}")


def start_scheduler():
    global scheduler
    
    if scheduler is not None and scheduler.running:
        return
    
    scheduler = BackgroundScheduler(timezone=timezone.get_current_timezone())
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    scheduler.add_job(
        collect_metrics,
        'interval',
        seconds=5,
        id='collect_metrics',
        replace_existing=True
    )
    
    scheduler.add_job(
        collect_processes,
        'interval',
        seconds=5,
        id='collect_processes',
        replace_existing=True
    )
    
    try:
        scheduler.start()
        logger.info("Scheduler started successfully")
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")
