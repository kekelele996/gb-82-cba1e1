export interface MetricData {
  id: number;
  timestamp: string;
  cpu_usage: number;
  memory_usage: number;
  memory_total: number;
  memory_used: number;
  disk_usage_c: number;
  disk_usage_d: number;
  network_up: number;
  network_down: number;
}

export interface ProcessData {
  id: number;
  pid: number;
  name: string;
  cpu_percent: number;
  memory_percent: number;
  timestamp: string;
}

export interface AlertData {
  id: number;
  metric_type: string;
  threshold: number;
  current_value: number;
  triggered_at: string;
  acknowledged: boolean;
}

export interface ThresholdConfig {
  cpu: number;
  memory: number;
  disk: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export type TimeRange = '1h' | '6h' | '24h';
