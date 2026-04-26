import { SecurityGuard } from "./security_guard";
import { JobQueue } from "./job_queue";
import { trackActivity, checkUser } from "./anomaly_service";

const guard = new SecurityGuard();

export function processPrompt(input: string) {
  if (!guard.validatePrompt(input)) {
    throw new Error("Unsafe prompt detected");
  }

  const sanitized = guard.sanitize(input);

  return {
    processed: sanitized,
  };
}


const queue = new JobQueue();

export function runAIAnalysis(payload: any) {
  queue.enqueue({
    id: Date.now().toString(),
    payload,
  });

  return {
    status: "queued",
  };
}


export function handleUserAction(userId: string, action: string) {
  trackActivity(userId, action);

  const analysis = checkUser(userId);

  if (analysis.isBot) {
    return {
      blocked: true,
      reasons: analysis.reasons,
    };
  }

  return {
    blocked: false,
  };
}