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

## Real-terminal verification

For terminal rendering, selection, appearance, or input changes, use the target project's supported terminal and documented launch command. Read its [project adapter](../../../references/project.md) for platform-specific fixtures and acceptance rules.

1. Pin the requested snapshot and keep fixtures, logs, and screenshots in a task-owned evidence directory.
2. Launch an isolated instance in the supported terminal. Record the owned window or pane, PIDs, ports, launch command, and relevant terminal capabilities.
3. Trigger the changed interaction with real keyboard or mouse input. Observe visible state, runtime errors, continued navigation, and input. Compare base and head under the same fixture when practical.
4. For protocol-dependent behavior, capture the application's requests and the terminal's actual responses. Identify any permitted injected events separately from native behavior.
5. Close the owned instance and verify resource release. Report the snapshot, terminal/version, actions, evidence, and unchecked scenarios.

## Process-lifecycle verification

For changes to subprocess budgets, stream collection, cancellation, or process-tree ownership:

1. Exercise the public execution tool or CLI with a real unbuffered child, using argv such as `[sys.executable, "-u", "-c", code]`. Use real timing for budget checks and stdin or owned-file gates to synchronize milestones instead of inferring lifecycle from arbitrary sleeps.
2. Derive expected wait, idle, and runtime outcomes from the changed contract. Isolate each budget; include both stdout and stderr, partial undecoded bytes, and completion without observer polling when relevant.
3. Include a parent that exits while a descendant retains captured pipes when collection or tree ownership changes. Cover the already-exited-root path, not only roots still running when spawn returns. Observe the public result and actual descendant lifetime.
4. Keep process doubles as supporting evidence only. Give each launch fresh `asyncio.StreamReader` instances and an event-backed async `wait()` with a real return code; do not substitute communicate-only mocks for a stream collector.
5. Record owned PIDs, tool output, finish reason, timing, and cleanup. Verify child termination and reap owned tasks/processes even when a probe fails. Report limitations separately from passing checks.

Example: launch a Python parent that starts a child inheriting stdout/stderr and then exits. Hold the child on an owned file gate. Check the execution through public tools before and after releasing the gate; in a separate run, exercise the configured runtime stop while the child remains blocked. Capture descendant exit evidence, not just the root return code.
