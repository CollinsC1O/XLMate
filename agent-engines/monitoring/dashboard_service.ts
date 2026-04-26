import { MetricsCollector } from "./metrics_collector";
import { AIHealthAnalyzer } from "./ai_health";

export class DashboardService {
  private collector = new MetricsCollector();
  private analyzer = new AIHealthAnalyzer(this.collector);

  recordLatency(ms: number) {
    this.collector.record("latency", ms);
  }

  recordError() {
    this.collector.record("errors", 1);
  }

  recordThroughput(count: number) {
    this.collector.record("throughput", count);
  }

  getDashboard() {
    return {
      health: this.analyzer.getHealthStatus(),
      metrics: this.collector.getMetrics(),
    };
  }
}