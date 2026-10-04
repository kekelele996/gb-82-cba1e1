import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { MetricData, ProcessData, AlertData, ThresholdConfig, TimeRange } from '../types';
import { metricsApi, processApi, alertApi } from '../api';

export const useMonitoringStore = defineStore('monitoring', () => {
  const latestMetric = ref<MetricData | null>(null);
  const metricHistory = ref<MetricData[]>([]);
  const topProcesses = ref<ProcessData[]>([]);
  const alerts = ref<AlertData[]>([]);
  const threshold = ref<ThresholdConfig>({ cpu: 80, memory: 80, disk: 80 });
  const timeRange = ref<TimeRange>('1h');
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchLatestMetric = async () => {
    try {
      const response = await metricsApi.getLatest();
      if (response.success) {
        latestMetric.value = response.data;
      }
    } catch (err) {
      error.value = '获取最新指标失败';
      console.error(err);
    }
  };

  const fetchMetricHistory = async () => {
    try {
      const response = await metricsApi.getHistory(timeRange.value);
      if (response.success) {
        metricHistory.value = response.data;
      }
    } catch (err) {
      error.value = '获取历史数据失败';
      console.error(err);
    }
  };

  const fetchTopProcesses = async () => {
    try {
      const response = await processApi.getTopProcesses();
      if (response.success) {
        topProcesses.value = response.data;
      }
    } catch (err) {
      error.value = '获取进程数据失败';
      console.error(err);
    }
  };

  const fetchAlerts = async () => {
    try {
      const response = await alertApi.getAlerts();
      if (response.success) {
        alerts.value = response.data;
      }
    } catch (err) {
      error.value = '获取告警数据失败';
      console.error(err);
    }
  };

  const fetchThreshold = async () => {
    try {
      const response = await alertApi.getThreshold();
      if (response.success) {
        threshold.value = response.data;
      }
    } catch (err) {
      error.value = '获取阈值配置失败';
      console.error(err);
    }
  };

  const updateThreshold = async (config: ThresholdConfig) => {
    try {
      loading.value = true;
      const response = await alertApi.updateThreshold(config);
      if (response.success) {
        threshold.value = response.data;
      }
    } catch (err) {
      error.value = '更新阈值配置失败';
      console.error(err);
    } finally {
      loading.value = false;
    }
  };

  const setTimeRange = (range: TimeRange) => {
    timeRange.value = range;
    fetchMetricHistory();
  };

  const fetchAll = async () => {
    loading.value = true;
    await Promise.all([
      fetchLatestMetric(),
      fetchMetricHistory(),
      fetchTopProcesses(),
      fetchAlerts(),
      fetchThreshold(),
    ]);
    loading.value = false;
  };

  return {
    latestMetric,
    metricHistory,
    topProcesses,
    alerts,
    threshold,
    timeRange,
    loading,
    error,
    fetchLatestMetric,
    fetchMetricHistory,
    fetchTopProcesses,
    fetchAlerts,
    fetchThreshold,
    updateThreshold,
    setTimeRange,
    fetchAll,
  };
});
