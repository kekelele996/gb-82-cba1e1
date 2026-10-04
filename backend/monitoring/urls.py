from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'metrics', views.MetricDataViewSet, basename='metrics')
router.register(r'processes', views.ProcessDataViewSet, basename='processes')
router.register(r'alerts', views.AlertDataViewSet, basename='alerts')
router.register(r'alerts/threshold', views.ThresholdConfigViewSet, basename='threshold')

urlpatterns = [
    path('alerts/threshold/', views.threshold_config, name='threshold_config'),
    path('', include(router.urls)),
    path('health/', views.health_check, name='health_check'),
]
