---
name: verify
description: General-purpose black-box verification after code changes. Use for cross-project validation, smoke tests, and evidence checks before merge, push, or release. Exercise public APIs, CLIs, Web UIs, services, or package consumers and return PASS/WARN/FAIL with evidence. A matching project-specific verifier takes precedence.
---

# Verify

Prove changed behavior through an interface a user or integrator can access. Static checks and unit tests support that proof.

1. Inspect the requested diff, or default to uncommitted changes plus `HEAD~1..HEAD`.
2. Map changed user-facing surfaces to 1-5 high-signal checks. Include the changed happy path and the most important reachable edge path.
3. Discover documented public entrypoints. Treat private helpers and internal state as diagnostic context.
4. Share a concise plan in commentary: concern, interface, action, expected evidence, pass rule, resource risk, and limitation.
5. Execute the public action and capture its command, exit/status, observable output, and relevant logs or browser state. Use isolated data and explicit authorization for external or destructive effects.
6. Clean up services and temporary data. Retain raw logs/screenshots only when useful and report their paths.
7. Judge each check:
   - `PASS`: public action and pass rule are fully proven;
   - `WARN`: behavior works with a material limitation or incomplete proof;
   - `FAIL`: observed behavior violates the pass rule;
   - `NOT RUN`: name the missing resource and residual risk.
8. Reply directly with the overall result, evidence per check, warnings/failures, limitations, and cleanup.

Use `scripts/collect-context.ps1`, `run-with-log.ps1`, and `find-free-port.ps1` when they reduce repeated shell work.
