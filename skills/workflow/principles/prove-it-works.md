# Prove It Works

Verify every task output by checking the real thing directly. Do not infer from proxies, self-reports, or "it compiles."

**Why:** Unverified work has unknown correctness. Indirect verification (file mtimes, output freshness, agent self-reports, cached screenshots) feels cheaper than direct observation. Acting on a wrong inference costs far more than checking the source.

Check the real thing, not a proxy:
- Check known task/process state directly before claiming a worker stopped; a cancellation request or old log timestamp is not final-state proof.
- Read the actual artifact/value and record its exact head or dirty-snapshot state. Do not attribute a test of dirty sources to a committed SHA.
- If verification fails, examine both the observation method and the system. Do not dismiss a real failure merely because the harness could be wrong.

## Choose decisive, proportionate proof

Use the target project's verifier or [verify](../workflows/verify/public/workflow.md). Exercise the changed happy path and highest-risk reachable edge through the supported public interface. Terminal rendering/input checks use the project's supported terminal and documented launch path. Static and unit checks support that evidence but do not prove an unexercised live claim.

For documentation, inspect the actual instructions, paths, schema/links, and representative decision boundaries. Do not require UI, performance, ten-worker, or cross-model lanes unrelated to the change.

Reuse a deterministic repository check when it captures the claim. Write a new script only if it adds justified value and the request permits it; read-only work does not require new files. Keep useful receipts under `.nanobot-workflows/runs/<run>/`, outside the live plugin, and commit/publish them only if authorized. Never mutate shared/live state, disable checks, or bypass approvals just to obtain evidence.

Report actual commands/actions, outcomes, artifact/head, and evidence locations. Distinguish PASS, FAIL, WARN/blocked, not run, and inference. A planned command, child self-report, green CI, or missing tool must not be rewritten as a successful user-facing verification.
