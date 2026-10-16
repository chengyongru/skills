# Nanobot TUI: real WezTerm verification

For changes to terminal rendering, selection, appearance, or input, exercise the real WezTerm path. Mocks and ConPTY provide supporting evidence.

1. Pin the requested source snapshot and honor source/index/remote no-edit limits. Put fixtures, logs, and screenshots under an owned `<workspace>\artifacts\<run-id>\wezterm` directory rather than modifying the checkout.
2. Launch a dedicated, uniquely classed WezTerm window and owned runtime. Record the window class, PIDs, and ports for cleanup. Exercise the actual `tui/src/index.ts` CLI with its current flags. Use an isolated, protocol-compatible fake WebSocket server when deterministic `file_edit` activity is needed; inspect the current protocol instead of guessing messages.
3. Trigger the changed interaction with real keyboard/mouse input. Capture visible state and runtime errors, then verify continued navigation and composer input. When practical, compare base and fixed behavior using the same fixture.
4. For auto-theme tests, keep watched config inputs separate from frequently written evidence/log files to avoid reload feedback. Record support for native theme notifications (mode 2031). If unsupported and notification injection is explicitly permitted, change the real terminal colors, then send `\x1b[?997;2n` (light) or `\x1b[?997;1n` (dark) through the owned pane's input using `send-text --no-paste`. Require the TUI's OSC 10/11 queries and genuine WezTerm color replies; never synthesize replies or directly set application theme state. Report injected-notification coverage separately from native notification support.
5. Close only the recorded owned window/processes/server and confirm port release. Preserve unrelated WezTerm panes, gateways, and browser sessions.

Example: for an auto-theme selection fix, seed a deterministic file edit, open `/diff`, select patch text with the mouse, then change terminal appearance in both directions so the diff is rebuilt. Check for `TextBufferView is destroyed` errors or debug-console takeover, continued diff navigation, and working input.

Report the exact snapshot, actions, screenshots/logs, and cleanup. Mark unavailable real-terminal checks as blocked.
