<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useMonitoringStore } from './store/monitoring';
import { exportApi } from './api';
import CpuChart from './components/CpuChart.vue';
import NetworkChart from './components/NetworkChart.vue';
import MemoryGauge from './components/MemoryGauge.vue';
import type { TimeRange, ThresholdConfig } from './types';

const store = useMonitoringStore();
const currentTime = ref(new Date().toLocaleString('zh-CN'));
const showThresholdModal = ref(false);
const tempThreshold = ref<ThresholdConfig>({ cpu: 80, memory: 80, disk: 80 });

const getProgressClass = (percent: number) => {
  if (percent >= 80) return 'danger';
  if (percent >= 60) return 'warning';
  return '';
};

const setTimeRange = (range: TimeRange) => {
  store.setTimeRange(range);
};

const openThresholdModal = () => {
  tempThreshold.value = { ...store.threshold };
  showThresholdModal.value = true;
};

const saveThreshold = async () => {
  await store.updateThreshold(tempThreshold.value);
  showThresholdModal.value = false;
};

const exportData = async () => {
  await exportApi.exportCSV(store.timeRange);
};

let refreshInterval: number | null = null;

onMounted(async () => {
  await store.fetchAll();
  
  setInterval(() => {
    currentTime.value = new Date().toLocaleString('zh-CN');
  }, 1000);
  
  refreshInterval = window.setInterval(async () => {
    await store.fetchLatestMetric();
    await store.fetchTopProcesses();
    await store.fetchAlerts();
  }, 5000);
});

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval);
  }
});
</script>

<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>系统监控大屏</h1>
      <div class="time">{{ currentTime }}</div>
    </div>

    <div class="controls">
      <div class="status-indicator online">
        <span class="status-dot"></span>
        <span>系统运行中</span>
      </div>
      <button 
        class="btn" 
        :class="{ active: store.timeRange === '1h' }"
        @click="setTimeRange('1h')"
      >
        最近1小时
      </button>
      <button 
        class="btn" 
        :class="{ active: store.timeRange === '6h' }"
        @click="setTimeRange('6h')"
      >
        最近6小时
      </button>
      <button 
        class="btn" 
        :class="{ active: store.timeRange === '24h' }"
        @click="setTimeRange('24h')"
      >
        最近24小时
      </button>
      <button class="btn" @click="openThresholdModal">
        配置阈值
      </button>
      <button class="btn btn-primary" @click="exportData">
        导出数据
      </button>
    </div>

    <div class="grid-container">
      <div class="card col-span-2">
        <h3 class="card-title">CPU 使用率</h3>
        <CpuChart :data="store.metricHistory" :threshold="store.threshold.cpu" />
      </div>

      <div class="card">
        <h3 class="card-title">内存使用率</h3>
        <MemoryGauge :data="store.latestMetric" />
      </div>

      <div class="card">
        <h3 class="card-title">磁盘使用率</h3>
        <div class="progress-container">
          <div class="progress-label">
            <span>C 盘</span>
            <span>{{ store.latestMetric?.disk_usage_c || 0 }}%</span>
          </div>
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :class="getProgressClass(store.latestMetric?.disk_usage_c || 0)"
              :style="{ width: `${store.latestMetric?.disk_usage_c || 0}%` }"
            ></div>
          </div>
        </div>
        <div class="progress-container">
          <div class="progress-label">
            <span>D 盘</span>
            <span>{{ store.latestMetric?.disk_usage_d || 0 }}%</span>
          </div>
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :class="getProgressClass(store.latestMetric?.disk_usage_d || 0)"
              :style="{ width: `${store.latestMetric?.disk_usage_d || 0}%` }"
            ></div>
          </div>
        </div>
      </div>

      <div class="card col-span-2">
        <h3 class="card-title">网络流量</h3>
        <NetworkChart :data="store.metricHistory" />
      </div>

      <div class="card col-span-2">
        <h3 class="card-title">TOP 10 进程</h3>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>PID</th>
                <th>进程名</th>
                <th>CPU%</th>
                <th>内存%</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="process in store.topProcesses" :key="process.id">
                <td>{{ process.pid }}</td>
                <td>{{ process.name }}</td>
                <td>{{ process.cpu_percent.toFixed(1) }}%</td>
                <td>{{ process.memory_percent.toFixed(1) }}%</td>
              </tr>
              <tr v-if="store.topProcesses.length === 0">
                <td colspan="4" style="text-align: center; color: #8fa4bf;">暂无数据</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="card col-span-2">
        <h3 class="card-title">告警记录</h3>
        <div class="alert-list">
          <div 
            v-for="alert in store.alerts" 
            :key="alert.id" 
            class="alert-item"
            :class="{ warning: alert.metric_type !== 'CPU' }"
          >
            <div class="alert-message">
              {{ alert.metric_type }} 超过阈值 ({{ alert.threshold }}%)，当前值: {{ alert.current_value.toFixed(1) }}%
            </div>
            <div class="alert-time">{{ new Date(alert.triggered_at).toLocaleString('zh-CN') }}</div>
          </div>
          <div v-if="store.alerts.length === 0" style="text-align: center; color: #8fa4bf; padding: 20px;">
            暂无告警
          </div>
        </div>
      </div>
    </div>

    <div v-if="showThresholdModal" class="modal-overlay" @click="showThresholdModal = false">
      <div class="modal" @click.stop>
        <h3 class="card-title">配置告警阈值</h3>
        <div class="input-group" style="margin-bottom: 16px;">
          <label>CPU 阈值 (%)</label>
          <input v-model.number="tempThreshold.cpu" type="number" min="0" max="100" />
        </div>
        <div class="input-group" style="margin-bottom: 16px;">
          <label>内存阈值 (%)</label>
          <input v-model.number="tempThreshold.memory" type="number" min="0" max="100" />
        </div>
        <div class="input-group" style="margin-bottom: 24px;">
          <label>磁盘阈值 (%)</label>
          <input v-model.number="tempThreshold.disk" type="number" min="0" max="100" />
        </div>
        <div class="controls" style="justify-content: flex-end; margin: 0;">
          <button class="btn" @click="showThresholdModal = false">取消</button>
          <button class="btn btn-primary" @click="saveThreshold">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: linear-gradient(180deg, rgba(15, 35, 60, 0.98), rgba(10, 25, 45, 0.99));
  border: 1px solid rgba(0, 200, 255, 0.3);
  border-radius: 12px;
  padding: 24px;
  min-width: 400px;
}
</style>
