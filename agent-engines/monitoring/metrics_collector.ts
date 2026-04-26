export type Metric = {
  name: string;
  value: number;
  timestamp: number;
};

export class MetricsCollector {
  private metrics: Metric[] = [];

  record(name: string, value: number) {
    this.metrics.push({
      name,
      value,
      timestamp: Date.now(),
    });
  }

  getMetrics(name?: string): Metric[] {
    if (!name) return this.metrics;
    return this.metrics.filter((m) => m.name === name);
  }

  clear() {
    this.metrics = [];
  }
}