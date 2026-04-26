import { DashboardService } from "./dashboard_service";

describe("DashboardService", () => {
  const dashboard = new DashboardService();

  it("returns healthy status initially", () => {
    const data = dashboard.getDashboard();
    expect(data.health.status).toBe("healthy");
  });

  it("detects degraded state", () => {
    for (let i = 0; i < 20; i++) {
      dashboard.recordError();
    }

    const data = dashboard.getDashboard();
    expect(data.health.status).toBe("degraded");
  });

  it("detects critical state", () => {
    for (let i = 0; i < 100; i++) {
      dashboard.recordError();
    }

    const data = dashboard.getDashboard();
    expect(data.health.status).toBe("critical");
  });
});