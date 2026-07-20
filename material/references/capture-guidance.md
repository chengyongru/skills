# Capture Guidance

Use this reference for model judgment while capturing a material fragment.

## What The Model Should Do

Use the model to understand and compress the source:

- Decide what the verifiable fact really is, not just what happened.
- Extract the strongest data point: a number, a measured result, a specific code path.
- Judge verification level honestly. Do not mark `verified` unless the user actually tested it.
- Judge maturity from the evidence already available. A fragmentary observation is `raw`; an existing well-supported experience may start further along.
- Choose a concise human title and filename.
- Match the user's language for the visible note.
- Decide whether existing materials are genuinely related.

Use `scripts/material_store.py` for mechanical actions:

- Resolve the store.
- Search fragments with `find "<query>"`.
- Read, mark, or delete only by exact `id`, `source_url`, or file path.
- List fragments for maturity/topic/kind scans.
- Write or update fragments.
- Mark maturity.
- Delete exactly matched fragments.

## The Minimum Viable Fragment

Every fragment must contain at least one **checkable anchor**:

- A measured number (latency, token count, cache hit rate, error rate)
- A specific code path (file:line, function name, config key)
- A tool name with version and a reproducible observation
- A before/after comparison with data
- A named resource with a source link and a specific reason for endorsement
- A concrete first-hand example supporting an opinion

A vague observation ("Ollama is slow", "the API is unstable") is not ready material. Capture it as `raw` only when preserving it is useful, and record what evidence is still missing.

## Kind Judgment

- `finding`: You discovered something through investigation. The discovery itself is the value. Example: "Ollama chat template moves tool definitions after tool round-trips, breaking KV-cache prefix."
- `experiment`: You ran a controlled comparison. The method and results are the value. Example: "Tested 3 prompt caching strategies, measured token re-evaluation per turn."
- `pitfall`: Others would hit this trap. The warning is the value. Example: "nanobot runtime context was injected via user-message metadata, not system prompt."
- `tool-comparison`: You evaluated alternatives head-to-head. The tradeoffs are the value.
- `opinion`: Your viewpoint backed by experience. Higher bar: must cite specific evidence in the body.
- `resource`: A verified link/tool/reference worth endorsing. Must state why it's worth endorsing.

## Maturity Promotion

- `raw` → `incubating`: You can articulate a content angle. The fragment has a clear point, but may need one more data point or validation.
- `incubating` → `ready`: The fragment stands on its own. A reader would find it useful as-is. All claims are `verified`.
- `ready` → `published`: The fragment has been used in published content. Mark after publishing, not before.

These are evidence states, not mandatory gates. Existing material may start at the level its current evidence supports.

## Verification Honesty

- `verified`: The user measured, tested, or directly observed this. There are logs, numbers, or reproducible steps.
- `unverified`: Plausible from documentation, blog posts, or others' reports. The user has not tested it personally.
- `hypothesis`: The user's inference or speculation. Needs evidence before any maturity promotion.

Never mark `hypothesis` as `verified` to make a fragment look ready. Unverified claims are fine to capture — just label them honestly.

## Relation Rules

Add `related` links only when there is a concrete relationship:

- Same investigation, incident, or debugging session.
- One fragment provides evidence for another's hypothesis.
- Same tool/project with overlapping findings.
- A follow-up that extends or contradicts an earlier fragment.

Do not link only because two fragments share a broad topic.

## Source-Specific Evidence

For GitHub issues/PRs: capture the issue number, the actual root cause (not just the symptom), the fix approach, and any measured before/after data. Keep tracker URLs in metadata.

For experiments: capture the setup, variables, measured results, and what surprised you.

For daily debugging: capture the problem symptom, the investigation path, the actual cause, and the concrete fix or workaround. The most valuable part is usually the gap between the expected cause and the actual cause.
