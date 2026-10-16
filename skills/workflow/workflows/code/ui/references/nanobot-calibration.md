# Nanobot calibration

Derived from the accepted scope of [HKUDS/nanobot PR #5704](https://github.com/HKUDS/nanobot/pull/5704), checked at `afe490a1` on 2026-09-10, and the user's corrections during its development. Read current code before reusing exact values. These are project preferences and examples, not universal web standards.

## Accepted decisions

| Area | Preferred result | Reason / boundary |
|---|---|---|
| Settings navigation | Independent Overview, Appearance, Models, Capabilities, System, Advanced, and About sections | Continuous scrolling and snap navigation were tried and reverted. Full-viewport minimum section heights created large blank gaps. Preserve independent sections unless the user changes direction. |
| Product destinations | Channels in the main sidebar | Chat platforms are a product destination, not buried configuration. Keep the existing route and keyboard access. |
| Repeated settings rows | Compact controls first; inputs together; multiline configuration behind edit icons | A switch in the middle of a numeric list and tall textareas made the group feel inconsistent. Parent/child configuration remains adjacent. |
| Form values | Left-aligned text and numeric input | The mixed left/right alignment in the gateway and API groups was rejected. Keep tabular numerals. |
| Multiline configuration | A right-aligned edit icon opening a blurred dialog | A full-width outlined control saying Edit was also rejected. Keep the icon's accessible name and delayed tooltip. List dialogs save explicitly; provider/MCP editors may update a draft saved by the enclosing form. |
| Hover hints | Shared 500 ms pointer delay, with no instant handoff to the next hint | `TooltipProvider` uses `delayDuration={500}` and `skipDelayDuration={0}`. Focus and click interactions remain immediate. Hint labels have no dotted underline. |
| Typography | Consistent navigation size/weight and a small set of neutral text roles | Favor the coherent icon/text relationship of the supplied Linear reference. Do not infer an exact font from a screenshot. Topic handles use monospace. |
| Modal surface | Unified inner/outer fill, rounded shared surface, 8 px backdrop blur | A white wrapper around a differently colored interior looked accidental. Blur is a repeated user preference, not an optional decoration for each modal. |
| Control shape | Shared radii and steady row height | Icon editor triggers were measured at 36 px; ordinary desktop runtime rows at 60 px. Treat these as calibration values, not constraints on mobile touch targets or error content. |
| Navigation actions | Compact search/new-topic/settings actions where recognizable; text for destination rows | Early icon-only navigation experiments were followed by labeled destination rows. Use the final screen rather than freezing an earlier experiment into a rule. |
| Usage overview | Daily token magnitude and cache composition | The heatmap stayed low-information after trying several week counts. A different chart answered the question better than adjusting density. |
| Usage drill-down | Daily stacked model usage with informative legend tooltips | Show totals, shares, and cache hit rates on demand. Omit zero-usage models and redundant summary lists. Preserve detail without forcing a tall scrolling dialog at normal desktop sizes. |
| Cache semantics | Cached input, uncached input, and unknown cache status remain distinct | “Other input” was ambiguous. Unknown status does not mean a cache miss; exclude it from the hit-rate denominator and explain that scope where needed. |
| Brand | Nanobot orange as the chart anchor, supporting neutral/secondary tones | Borrow OpenRouter's composition and Zed's label-plus-shortcut tooltip structure without importing their palettes wholesale. |
| Exposed preferences | Every option has an observable effect | The appearance density setting only stored an unused browser preference and was removed. A separate sidebar density implementation existed; its presence did not make the settings control functional. |

## Locate the owning code

Paths are relative to a nanobot checkout:

- `webui/src/globals.css`: text roles, settings spacing, alignment, hover fills, and shape tokens.
- `webui/src/components/settings/shared/SettingsControls.tsx`: rows, groups, titles, and save/restart surfaces.
- `webui/src/components/settings/shared/SettingsTextEditor.tsx`: compact edit action, draft, dialog, and save failure handling.
- `webui/src/components/ui/tooltip.tsx`: shared delay; `floating-surface.ts` and `dialog.tsx`: backdrop and modal surface.
- `webui/src/components/settings/system/runtime-config-fields.ts`: control types, order, and conditional dependencies.
- `webui/src/components/settings/system/RuntimeConfigSettings.tsx`: rendering, autosave, explicit list saves, and restart notices.
- `nanobot/webui/settings_runtime.py`: field allowlist and validation. Saving runtime configuration does not hot-reload the agent.
- `webui/src/components/settings/TokenUsageCard.tsx`, `TokenUsageDetails.tsx`, `TokenUsageModelTrend.tsx`, and `nanobot/llm_usage/store.py`: visible chart and underlying aggregation.

## Apply the taste to common requests

- “This settings group feels uneven”: compare control types, row heights, label insets, and value alignment; make multiline configuration an edit action before padding every other row taller.
- “Make this dashboard prettier”: identify the user's question, check available data granularity, and consolidate repeated summaries. Request or implement missing aggregation only if the intended chart requires it.
- “Make everything fit without scrolling”: simplify and widen a desktop dialog first; keep long text editable and all actions reachable on mobile rather than clipping or shrinking indefinitely.
- “Use Linear/Zed/OpenRouter as inspiration”: transfer the demonstrated interaction or hierarchy, then render it with nanobot's typography, accent, and shared components.
- “Use continuous scrolling”: treat it as a new explicit direction, explain the navigation tradeoff briefly, and validate actual content-driven spacing. The earlier rollback remains the default until that direction changes.
