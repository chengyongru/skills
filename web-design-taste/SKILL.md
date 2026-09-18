---
name: web-design-taste
description: Refine web application interfaces with a restrained, coherent visual language and useful interactions. Use for taste reviews, settings pages, sidebars, dialogs, and usage dashboards when the user wants less visual clutter, consistent controls, or higher information value. Focus on product UI rather than promotional art direction.
---

# Web design taste

Make the interface feel like one product: calm typography, purposeful controls, predictable interaction, and enough information to justify every element. Treat this as a preference profile; follow the user's current direction and the host product's visual language.

## Establish the target

- Inspect the actual components, shared styles, data contracts, and one representative screen before editing. Distinguish a rendering defect from a missing behavior or missing data.
- Extract the useful property of a reference: baseline alignment, information hierarchy, tooltip composition, or chart encoding. Verify font identity before naming it; optical quality also depends on weight, color, line height, and rendering.
- When applying this profile to nanobot, read [the calibration](references/nanobot-calibration.md). For other products, use it only when a concrete example would resolve an ambiguous choice; preserve their own tokens and brand.

## Arrange controls by purpose and size

- Keep navigation categories separate when each is a destination. Let content determine height. Introduce continuous sections or snapping only when requested and useful; assess the resulting gaps before keeping it.
- Within a semantic group, keep similar controls adjacent and place compact controls before larger editors. Preserve a master control next to its dependent fields, even when that interrupts size order.
- Use one alignment edge for editable values, including numbers. Keep numeric columns right-aligned where comparison requires it; form fields are a different context.
- Keep short option groups on one line without horizontal scrolling. Allocate width, reduce optional padding, or use a select control on narrow screens while keeping every option reachable.
- Give multiline configuration a compact edit action and a focused dialog when inline height disrupts a repeated row layout. Preserve full editors for primary authoring tasks.

## Remove visual disagreement

- Reuse a small set of text colors for primary, secondary, and auxiliary roles. Align main navigation and settings navigation typography; use monospace for compact identifiers and tabular digits for comparable metrics.
- Align icons optically with text using a shared icon box, baseline, and gap. Distribute spacing inside a label when needed, rather than stretching the icon away from it.
- Use a common hover fill and radius scale across related controls. Inspect search fields, inputs, selects, and textareas as a family. Match a dialog's inner and outer surfaces so a contrasting wrapper does not look like an accidental rim.
- Make a small secondary action a small action: use a recognizable icon with an accessible name and tooltip. Keep labels where they explain a destination or disambiguate an unfamiliar operation.
- Place supplemental help in consistently delayed hover/focus hints. Keep critical state and errors visible. Prefer a shared delay over per-component timing; keyboard focus and explicit clicks should remain responsive.

## Make interactions honest

- Trace exposed settings from edit through save to actual use. Describe restart requirements accurately. Remove an inert option when removal is authorized; otherwise identify its missing connection before polishing it.
- Give dialog-opening rows an explicit affordance such as Configure or an edit icon. Keep switches distinguishable from configuration actions. A disabled feature should lead to a useful setup state or a disabled entry, never an empty dialog.
- Use the shared blurred modal backdrop. Stage edits locally, cancel without saving, preserve failed drafts, and return focus on close. When a dialog edits a larger form's draft, make the final apply step clear.

## Give charts a job

- Start with the question the chart answers. Prefer a trend or composition chart over a sparse heatmap when magnitude and breakdown matter more than activity presence.
- Put the overview, the drill-down, and the tooltip at different information levels. Remove repeated lists or metrics once the chart already communicates them clearly.
- Distinguish zero, missing data, and unknown classification. Show honest rate denominators, reconcile stacked parts with totals, and omit zero-usage categories when they add no information. Use user-facing model names rather than internal preset identifiers unless the distinction matters.
- Reuse the product accent, with distinguishable secondary colors or patterns for series and cache status. Keep exact values and rates accessible on hover and keyboard focus. Widen and simplify a statistics dialog before adding internal scrolling; retain access to overflow on small screens.

## Verify the result

- Fix recurring mismatches at the shared component or token that owns them. Keep the patch proportional to the request.
- Inspect the rendered result at desktop and narrow widths, in relevant themes and locales, after entrance animations settle. Check alignment, gaps, row heights, truncation, and horizontal overflow.
- Exercise the changed behavior through its public UI: disabled and empty states, hover delay, keyboard focus, cancel/save, errors, refresh persistence, and dirty-state navigation as relevant. Use the project verifier when available; report any unverified behavior directly.
- Report the concrete change and supporting evidence. Treat building, pushing, reviewing, and changing PR state as separate actions with their existing authorization boundaries.
