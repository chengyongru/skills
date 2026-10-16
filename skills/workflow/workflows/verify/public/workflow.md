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

For changes to terminal rendering, selection, appearance, or input, use real WezTerm; mocks and ConPTY are supporting evidence only.

1. Pin the requested source snapshot and honor source/index/remote no-edit limits. Put fixtures, logs, and screenshots under an owned `<workspace>\artifacts\<run-id>\wezterm` directory rather than modifying the checkout.
2. Launch a dedicated, uniquely classed WezTerm window and owned runtime. Record the window class, PIDs, and ports for cleanup. For nanobot, exercise the actual `tui/src/index.ts` CLI with its current flags. Use an isolated, protocol-compatible fake WebSocket server when deterministic `file_edit` activity is needed; inspect the current protocol instead of guessing messages.
3. Trigger the changed interaction with real keyboard/mouse input. Capture visible state and runtime errors, then verify continued navigation and composer input. When practical, compare base and fixed behavior using the same fixture.
4. For auto-theme tests, keep watched config inputs separate from frequently written evidence/log files to avoid reload feedback. Record support for native theme notifications (mode 2031). If unsupported and notification injection is explicitly permitted, change the real terminal colors, then send `\x1b[?997;2n` (light) or `\x1b[?997;1n` (dark) through the owned pane's input using `send-text --no-paste`. Require the TUI's OSC 10/11 queries and genuine WezTerm color replies; never synthesize replies or directly set application theme state. Report injected-notification coverage separately; it does not prove native notification support.
5. Close only the recorded owned window/processes/server and confirm port release. Never close unrelated WezTerm panes, gateways, or browser sessions.

Example: for an auto-theme selection fix, seed a deterministic file edit, open `/diff`, select patch text with the mouse, then change terminal appearance in both directions so the diff is rebuilt. Prove that no `TextBufferView is destroyed` error or debug-console takeover occurs, and that the diff remains navigable and input still works.

Report the exact snapshot, actions, screenshots/logs, limitations, and cleanup. Do not mark PASS if the real-terminal path was not exercised.

## Process-lifecycle verification

For changes to subprocess budgets, stream collection, cancellation, or process-tree ownership:

1. Exercise the public execution tool or CLI with a real unbuffered child, using argv such as `[sys.executable, "-u", "-c", code]`. Use real timing for budget checks and stdin or owned-file gates to synchronize milestones instead of inferring lifecycle from arbitrary sleeps.
2. Derive expected wait, idle, and runtime outcomes from the changed contract. Isolate each budget; include both stdout and stderr, partial undecoded bytes, and completion without observer polling when relevant.
3. Include a parent that exits while a descendant retains captured pipes when collection or tree ownership changes. Cover the already-exited-root path, not only roots still running when spawn returns. Observe the public result and actual descendant lifetime.
4. Keep process doubles as supporting evidence only. Give each launch fresh `asyncio.StreamReader` instances and an event-backed async `wait()` with a real return code; do not substitute communicate-only mocks for a stream collector.
5. Record owned PIDs, tool output, finish reason, timing, and cleanup. Verify child termination and reap owned tasks/processes even when a probe fails. Report limitations separately from passing checks.

Example: launch a Python parent that starts a child inheriting stdout/stderr and then exits. Hold the child on an owned file gate. Check the execution through public tools before and after releasing the gate; in a separate run, exercise the configured runtime stop while the child remains blocked. Capture descendant exit evidence, not just the root return code.
