# Selection Guidance

Use this reference when choosing the next action from idea notes.

## Role Of The Model

Use the model for judgment:

- Interpret evidence and blockers.
- Compare expected impact against effort and confidence.
- Notice clusters or dependencies from `related`.
- Adapt the final recommendation to the user's language and current intent.
- Explain the choice with concrete facts, not labels.

Use `scripts/idea_store.py` for mechanical work:

- Resolve the store.
- List candidate notes.
- Read selected candidates.
- Mark a chosen note as `doing` only when the user asks to start.

## Candidate Set

Consider `open` and `doing` notes unless the user asks otherwise. Prefer current project context if the user mentions one.

If the top candidates lack evidence, blocker, next action, cost, impact, or confidence, do at most three small source lookups total. Then decide with the available evidence.

## Judgment Heuristics

Choose one action by loose judgment:

- Impact on the user's current important project or life area.
- Whether it unlocks other people, review, mergeability, or later work.
- Evidence strength from the source.
- Blocker severity: none, draft/review, failing check, conflict, unknown.
- Time to feedback.
- Cost and current energy fit.
- Cost of delaying one day.
- Whether one action advances a concrete cluster of related ideas.

Cost, impact, and confidence are hints, not a formula.

## Output

Return exactly:

```markdown
做：<one action>

理由：<two or three concrete sentences grounded in the selected entry's evidence/current state/blocker>

下一步：<first concrete probe, with no duration estimate>
```

Match the user's language. Do not mention rejected alternatives unless asked. Do not include time boxes, reselect conditions, or rankings unless asked.
