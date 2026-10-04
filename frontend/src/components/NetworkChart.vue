<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import * as echarts from 'echarts';
import type { MetricData } from '../types';

const props = defineProps<{
  data: MetricData[];
}>();

const chartRef = ref<HTMLDivElement | null>(null);
let chartInstance: echarts.ECharts | null = null;

const initChart = () => {
  if (!chartRef.value) return;
  
  chartInstance = echarts.init(chartRef.value);
  updateChart();
};

const updateChart = () => {
  if (!chartInstance) return;

  const times = props.data.map((item) => {
    const date = new Date(item.timestamp);
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  });

  const upData = props.data.map((item) => item.network_up);
  const downData = props.data.map((item) => item.network_down);

  const option: echarts.EChartsOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 35, 60, 0.9)',
      borderColor: 'rgba(0, 200, 255, 0.3)',
      textStyle: {
        color: '#e0e6ed',
      },
    },
    legend: {
      data: ['上行', '下行'],
      textStyle: {
        color: '#8fa4bf',
      },
      top: 0,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '18%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: times,
      axisLine: {
        lineStyle: {
          color: 'rgba(0, 200, 255, 0.3)',
        },
      },
      axisLabel: {
        color: '#8fa4bf',
        fontSize: 10,
      },
      splitLine: {
        show: false,
      },
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: 'rgba(0, 200, 255, 0.3)',
        },
      },
      axisLabel: {
        color: '#8fa4bf',
        formatter: '{value} Mbps',
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(0, 200, 255, 0.1)',
        },
      },
    },
    series: [
      {
        name: '上行',
        type: 'line',
        smooth: true,
        data: upData,
        lineStyle: {
          color: '#00ff88',
          width: 2,
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(0, 255, 136, 0.3)' },
            { offset: 1, color: 'rgba(0, 255, 136, 0.05)' },
          ]),
        },
        itemStyle: {
          color: '#00ff88',
        },
      },
      {
        name: '下行',
        type: 'line',
        smooth: true,
        data: downData,
        lineStyle: {
          color: '#ffaa00',
          width: 2,
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(255, 170, 0, 0.3)' },
            { offset: 1, color: 'rgba(255, 170, 0, 0.05)' },
          ]),
        },
        itemStyle: {
          color: '#ffaa00',
        },
      },
    ],
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100,
      },
    ],
  };

  chartInstance.setOption(option);
};

const handleResize = () => {
  chartInstance?.resize();
};

watch(() => props.data, () => {
  updateChart();
}, { deep: true });

onMounted(() => {
  initChart();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  chartInstance?.dispose();
});
</script>

<template>
  <div ref="chartRef" class="chart-container"></div>
</template>
