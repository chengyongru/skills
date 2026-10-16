# Arena

Keep a short checklist for Frame, Fan out, Cross-judge, Pick, Graft, and Verify before launching anything.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric, 3-6 concrete gradeable criteria for what success looks like on *this* task. It is the picker's tool in Phase D. Candidates only see the task.
3. Choose a bounded candidate count, normally two. Give candidates the same brief and separate contexts.
4. Give each candidate its own output location outside the plugin, such as `<agent-workspace>/.nanobot-workflows/runs/<task>/candidate-<n>/`, per the **separate-before-serializing-shared-state** principle skill. Use installed [pr-worktree](../../pr/worktree/workflow.md) for registered worktrees when actual candidate code needs isolation; do not assume child tasks get separate machines.

## Phase B: Fan out

Create candidate tasks with `subagent(action="create", task=..., label=..., wait=false)`, respecting the concurrency limit. Include the shared grounding path, allowed reads, the candidate's only writable output path, and the required artifact plus a short rationale naming rejected alternatives. Prohibit unrelated edits and external actions. Record each returned `task_id`; use `check` on that ID when needed and await completion notifications rather than repeatedly polling.

If a candidate fails without output, inspect its terminal result before a bounded retry or proceeding with N-1. Note the dropout and never treat it as a passing candidate.

## Phase C: Cross-judge

After all candidates finish writing, create one fresh judge task with the rubric and candidates labeled by path. Its contract is read-only: read the completed candidates, score each criterion, and recommend a base with rationale; no edits, commands with side effects, or publication. It may run alongside your reading in Phase D.

## Phase D: Pick a base

Read every candidate end to end before picking. Score each against the rubric criterion by criterion, not on holistic feel, and compare with the judge. Compare the evidence behind both agreement and disagreement to expose bias, missing evidence, or an ambiguous rubric. Read both rationales and check the underlying evidence before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API, per the Laziness Protocol.

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base, usually one or two things per candidate, not most of it. Fold each graft in by hand, per the **redesign-from-first-principles** principle skill, so the result stays coherent under one mental model. Don't paste mechanically.

If the candidates converge on one shape, record the convergence, skip the graft, and verify the result. If they wildly diverge, check whether Phase A was under-specified. Reframe and re-run when necessary rather than averaging the divergence. Deliver the artifact locally; committing or publishing is a separate authorized action.

## Phase F: Verify

Verify the synthesized artifact like any other output, per the **prove-it-works** principle skill. If verification finds a problem the arena missed, either Phase A was wrong (re-frame and re-run) or a candidate caught it and you missed the graft (go back to Phase E). Don't paper over it.

## Outputs

One synthesized artifact, with a short synthesis note alongside naming the base and why, the cross-judge's verdict, each graft with its source candidate, what was rejected and why, any convergence or dropouts, and the verification result.
