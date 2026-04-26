import { AnomalyDetector } from "./anomaly_detector";

const detector = new AnomalyDetector();

export function trackActivity(userId: string, action: string) {
  detector.record({
    userId,
    action,
    timestamp: Date.now(),
  });
}

export function checkUser(userId: string) {
  return detector.analyze(userId);
}