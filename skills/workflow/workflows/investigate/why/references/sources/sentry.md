# Sentry error history

## How to search it

Use an actually exposed authorized Sentry read connector. Inspect its schema and map the steps below to supported operations; do not invent tool names, initiate authentication, or modify issues/releases. If access is absent, report the category unavailable. Bound reads to the parent's organization/project, target, and time window.

1. **Orient.** Use known organization/project references first. If they are missing, list only accessible organizations/projects through supported reads, then choose the one tied to the target. Do not enumerate unrelated customer data.
2. **Search issues related to the target.** Build bounded searches from the exception classes the code handles, function/class names, exact error strings, and relevant file paths. Use the actual connector's search syntax, not a guessed natural-language API. Record queries, filters, and truncation.
3. **Narrow by release and time.** Read matching issue events and tag distributions when available. Check first seen, last seen, affected releases, frequency trajectory, environment, version, and sampling. Does the decline line up with the target's ship date? A missing retained event is not proof that the error did not occur.
4. **Read a representative full event.** Use an exact returned issue/event reference. Does its stack pass through the target code? Do tags and breadcrumbs match the conditions the code defends against? Quote a small relevant redacted excerpt, not raw user payloads. If only a summary is available, name that evidence limit.
5. **Check nearby releases.** Read available release metadata around the commit date and correlate versions with the PR merge/deploy date. Distinguish merge from actual rollout and account for neighboring changes.
6. **Treat existing AI analyses as hypotheses.** An already available Seer or similar root-cause report can suggest leads, but events and stack traces remain primary evidence. Do not launch a new analysis job automatically; it can be stateful or billable and requires separate explicit authorization through a supported interface.

Do not resolve, assign, comment on, or edit an issue merely because the evidence suggests a fix. Return findings for the coordinator to synthesize.

## What to return

For each relevant issue:

- Issue ID and title.
- Project and organization.
- First-seen and last-seen timestamps.
- Event count and sampling rate if known.
- Affected releases and the observed rollout window.
- A representative relevant stack-trace excerpt, verbatim and redacted.
- First/last-seen correlation with the target's ship date, without claiming causation from timing alone.
- Exact issue/event link.
- Existing author comments or resolution notes, if accessible.
- Queries performed and gaps caused by access, retention, pagination, or missing capabilities.
