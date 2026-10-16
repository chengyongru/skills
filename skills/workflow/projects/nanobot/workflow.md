# HKUDS/nanobot development

Use this adapter for HKUDS/nanobot and its forks, confirmed through repository metadata or the user's target selection.

## Project instructions

Read the checkout's `AGENTS.md`, relevant `.agent/` guidance, contribution instructions, and the exact issue acceptance criteria. Honor the repository's formatting restrictions, including its prohibition on `ruff format`, and its release-record conventions.

## Verification and design resources

| Changed surface | Resource |
|---|---|
| WebUI, gateway, WebSocket routing, settings, chat, or persistence | [WebUI verification](webui/workflow.md) |
| TUI rendering, selection, appearance, or input | [Real WezTerm verification](terminal.md) |
| WebUI visual language and shared components | [UI calibration](ui-calibration.md) |
| CLI, API, package, or subprocess lifecycle | [Public-surface verification](../../workflows/verify/public/workflow.md), using this checkout's entrypoints and contracts |

The separate [`$nanobot-gate`](../../../nanobot-gate/SKILL.md) provides snapshot-bound readiness checks when the user literally invokes it.
