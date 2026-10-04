import axios from 'axios';
import type { MetricData, ProcessData, AlertData, ThresholdConfig, ApiResponse, TimeRange } from '../types';

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    throw error;
  }
);

export const metricsApi = {
  getLatest: async (): Promise<ApiResponse<MetricData>> => {
    const response = await api.get('/metrics/latest/');
    return response.data;
  },

  getHistory: async (range: TimeRange): Promise<ApiResponse<MetricData[]>> => {
    const response = await api.get(`/metrics/history/?range=${range}`);
    return response.data;
  },
};

export const processApi = {
  getTopProcesses: async (): Promise<ApiResponse<ProcessData[]>> => {
    const response = await api.get('/processes/top/');
    return response.data;
  },
};

export const alertApi = {
  getAlerts: async (): Promise<ApiResponse<AlertData[]>> => {
    const response = await api.get('/alerts/');
    return response.data;
  },

  getThreshold: async (): Promise<ApiResponse<ThresholdConfig>> => {
    const response = await api.get('/alerts/threshold/');
    return response.data;
  },

  updateThreshold: async (config: ThresholdConfig): Promise<ApiResponse<ThresholdConfig>> => {
    const response = await api.put('/alerts/threshold/', config);
    return response.data;
  },
};

export const healthApi = {
  check: async (): Promise<ApiResponse<{ status: string }>> => {
    const response = await api.get('/health/');
    return response.data;
  },
};

export const exportApi = {
  exportCSV: async (range: TimeRange): Promise<void> => {
    const response = await api.get(`/metrics/export/?range=${range}`, {
      responseType: 'blob',
    });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `metrics_${range}_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  },
};
