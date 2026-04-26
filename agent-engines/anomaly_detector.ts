type Activity = {
  userId: string;
  timestamp: number;
  action: string;
};

type AnomalyResult = {
  userId: string;
  score: number;
  isBot: boolean;
  reasons: string[];
};

export class AnomalyDetector {
  private activityLog: Map<string, Activity[]> = new Map();

  // Thresholds (tunable)
  private MAX_ACTIONS_PER_MIN = 20;
  private DUPLICATE_ACTION_THRESHOLD = 10;

  record(activity: Activity) {
    if (!this.activityLog.has(activity.userId)) {
      this.activityLog.set(activity.userId, []);
    }

    this.activityLog.get(activity.userId)!.push(activity);
  }

  analyze(userId: string): AnomalyResult {
    const logs = this.activityLog.get(userId) || [];

    const now = Date.now();
    const lastMinute = logs.filter(
      (a) => now - a.timestamp < 60_000
    );

    const reasons: string[] = [];
    let score = 0;

    // 🚨 High frequency detection
    if (lastMinute.length > this.MAX_ACTIONS_PER_MIN) {
      score += 50;
      reasons.push("High activity rate");
    }

    // 🚨 Duplicate pattern detection
    const actionCounts: Record<string, number> = {};
    for (const act of logs) {
      actionCounts[act.action] =
        (actionCounts[act.action] || 0) + 1;
    }

    for (const action in actionCounts) {
      if (actionCounts[action] > this.DUPLICATE_ACTION_THRESHOLD) {
        score += 30;
        reasons.push(`Repeated action: ${action}`);
      }
    }

    // 🚨 Burst behavior detection
    const burst = this.detectBurst(lastMinute);
    if (burst) {
      score += 20;
      reasons.push("Burst activity pattern");
    }

    return {
      userId,
      score,
      isBot: score >= 50,
      reasons,
    };
  }

  private detectBurst(logs: Activity[]): boolean {
    if (logs.length < 5) return false;

    const intervals = [];
    for (let i = 1; i < logs.length; i++) {
      intervals.push(logs[i].timestamp - logs[i - 1].timestamp);
    }

    const avg =
      intervals.reduce((a, b) => a + b, 0) / intervals.length;

    return avg < 1000; // rapid-fire actions
  }
}