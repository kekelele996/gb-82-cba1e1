<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';
import * as echarts from 'echarts';
import type { MetricData } from '../types';

const props = defineProps<{
  data: MetricData[];
  threshold: number;
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

  const cpuData = props.data.map((item) => item.cpu_usage);
  const thresholdLine = props.data.map(() => props.threshold);

  const option: echarts.EChartsOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 35, 60, 0.9)',
      borderColor: 'rgba(0, 200, 255, 0.3)',
      textStyle: {
        color: '#e0e6ed',
      },
      formatter: (params: any) => {
        const data = params[0];
        return `<div>时间: ${data.axisValue}</div><div>CPU: ${data.value}%</div>`;
      },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
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
      max: 100,
      min: 0,
      axisLine: {
        lineStyle: {
          color: 'rgba(0, 200, 255, 0.3)',
        },
      },
      axisLabel: {
        color: '#8fa4bf',
        formatter: '{value}%',
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(0, 200, 255, 0.1)',
        },
      },
    },
    series: [
      {
        name: 'CPU',
        type: 'line',
        smooth: true,
        data: cpuData,
        lineStyle: {
          color: '#00d4ff',
          width: 2,
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(0, 212, 255, 0.4)' },
            { offset: 1, color: 'rgba(0, 212, 255, 0.05)' },
          ]),
        },
        itemStyle: {
          color: '#00d4ff',
        },
        markLine: {
          silent: true,
          data: [
            {
              yAxis: props.threshold,
              lineStyle: {
                color: '#ff4444',
                type: 'dashed',
              },
              label: {
                show: true,
                color: '#ff4444',
                formatter: `阈值: ${props.threshold}%`,
              },
            },
          ],
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

watch(() => [props.data, props.threshold], () => {
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
