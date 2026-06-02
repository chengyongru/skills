# Web UI Verification

Use this when the changed behavior affects routes, navigation, forms, state, rendering, layout, websocket-driven UI, settings, or browser-visible errors.

## Setup

Build or compile the frontend as documented unless the project explicitly supports unbuilt static files. Start the app through the documented dev server or real gateway/server.

For browser checks, use Playwright, `playwright-cli`, or the project's existing E2E runner. Capture at least one of:

- Accessibility/snapshot text.
- Page evaluation result.
- Screenshot path.
- Console errors.
- Network status for changed requests.

## Required Checks

Pick checks that match the diff:

- Route change: open the route directly, verify visible UI, reload, verify the route persists when that is expected.
- Form/state change: perform the interaction and verify visible state or submitted request.
- Layout/rendering change: inspect desktop and mobile viewport when layout risk is meaningful.
- Error/loading change: trigger loading or error state through the public UI.
- Realtime change: connect through the app and observe a user-visible update.

## PASS Rules

PASS requires:

- Page loads without a relevant console/runtime error.
- The changed element, text, route, or interaction is visible to the user.
- The expected state change occurs after interaction.
- Reload, navigation, or persistence behavior is checked when the change touches routing or stored state.
- Screenshots or snapshots do not show obvious overlap, blank content, or missing assets for the changed area.

Build success alone is never enough for a UI PASS.
