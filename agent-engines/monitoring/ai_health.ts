import { MetricsCollector } from "./metrics_collector";

export class AIHealthAnalyzer {
  constructor(private collector: MetricsCollector) {}

  getHealthStatus() {
    const latency = this.avg("latency");
    const errors = this.sum("errors");
    const throughput = this.sum("throughput");

    let status: "healthy" | "degraded" | "critical" = "healthy";

    if (errors > 50 || latency > 2000) {
      status = "critical";
    } else if (errors > 10 || latency > 1000) {
      status = "degraded";
    }

    return {
      status,
      metrics: {
        latency,
        errors,
        throughput,
      },
    };
  }

  private avg(name: string) {
    const data = this.collector.getMetrics(name);
    if (data.length === 0) return 0;

    return (
      data.reduce((sum, m) => sum + m.value, 0) / data.length
    );
  }

  private sum(name: string) {
    return this.collector
      .getMetrics(name)
      .reduce((sum, m) => sum + m.value, 0);
  }
}