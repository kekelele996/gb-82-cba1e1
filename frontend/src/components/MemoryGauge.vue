<script setup lang="ts">
import { computed } from 'vue';
import type { MetricData } from '../types';

const props = defineProps<{
  data: MetricData | null;
}>();

const memoryPercent = computed(() => {
  if (!props.data) return 0;
  return props.data.memory_usage;
});

const gaugeColor = computed(() => {
  const percent = memoryPercent.value;
  if (percent >= 80) return '#ff4444';
  if (percent >= 60) return '#ffaa00';
  return '#00d4ff';
});

const formatBytes = (gb: number) => {
  return `${gb.toFixed(1)} GB`;
};
</script>

<template>
  <div class="gauge-container">
    <svg viewBox="0 0 200 120" class="gauge-svg">
      <circle
        cx="100"
        cy="100"
        r="80"
        fill="none"
        stroke="rgba(0, 0, 0, 0.3)"
        stroke-width="12"
        stroke-dasharray="251.2"
        stroke-dashoffset="125.6"
        stroke-linecap="round"
      />
      <circle
        cx="100"
        cy="100"
        r="80"
        fill="none"
        :stroke="gaugeColor"
        stroke-width="12"
        :stroke-dasharray="`${memoryPercent * 2.512} 251.2`"
        stroke-dashoffset="125.6"
        stroke-linecap="round"
        class="gauge-arc"
      />
    </svg>
    <div class="gauge-value" :style="{ color: gaugeColor }">
      {{ memoryPercent.toFixed(1) }}%
    </div>
    <div class="gauge-label">
      {{ data ? formatBytes(data.memory_used) : '--' }} / 
      {{ data ? formatBytes(data.memory_total) : '--' }}
    </div>
  </div>
</template>

<style scoped>
.gauge-svg {
  width: 200px;
  height: 120px;
  position: absolute;
  top: 0;
}

.gauge-container {
  position: relative;
  padding-top: 30px;
}

.gauge-arc {
  transition: stroke-dasharray 0.5s ease, stroke 0.5s ease;
  filter: drop-shadow(0 0 10px currentColor);
}

.gauge-value {
  font-size: 36px;
  font-weight: bold;
  text-shadow: 0 0 20px currentColor;
  margin-top: 20px;
}

.gauge-label {
  margin-top: 8px;
  color: #8fa4bf;
  font-size: 14px;
}
</style>
