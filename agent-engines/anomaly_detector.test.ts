import { AnomalyDetector } from "./anomaly_detector";

describe("AnomalyDetector", () => {
  let detector: AnomalyDetector;

  beforeEach(() => {
    detector = new AnomalyDetector();
  });

  it("detects high frequency activity", () => {
    const user = "bot1";

    for (let i = 0; i < 30; i++) {
      detector.record({
        userId: user,
        action: "click",
        timestamp: Date.now(),
      });
    }

    const result = detector.analyze(user);

    expect(result.isBot).toBe(true);
    expect(result.reasons).toContain("High activity rate");
  });

  it("detects repeated actions", () => {
    const user = "bot2";

    for (let i = 0; i < 15; i++) {
      detector.record({
        userId: user,
        action: "login",
        timestamp: Date.now(),
      });
    }

    const result = detector.analyze(user);

    expect(result.reasons.some(r => r.includes("Repeated action"))).toBe(true);
  });

  it("does not flag normal user", () => {
    const user = "user1";

    detector.record({
      userId: user,
      action: "login",
      timestamp: Date.now(),
    });

    const result = detector.analyze(user);

    expect(result.isBot).toBe(false);
  });
});