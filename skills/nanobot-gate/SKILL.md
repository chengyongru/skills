---
name: nanobot-gate
description: Explicit-invocation-only workflow for snapshot-bound simplify, verification, candidate review, formal PR review, and CI readiness for HKUDS/nanobot and its forks. Use only when the user explicitly writes `$nanobot-gate`. Never infer or auto-trigger this skill from push, PR, merge, release, readiness, review, verification, or CI requests.
---

# Nanobot Gate

Run this workflow only after the user explicitly invokes `$nanobot-gate`. Do not activate it automatically for adjacent publication or readiness work.

Confirm the target is HKUDS/nanobot or a fork and read its [project adapter](../workflow/projects/nanobot/workflow.md) and the [runtime contract](../workflow/references/runtime.md). Bind every conclusion to one candidate snapshot with `scripts/gate_state.py`; `<skill>` below is this gate's directory. Keep prose in the conversation and raw evidence in an ignored evidence directory.

## Required gates

- local readiness: [simplify](../workflow/workflows/code/simplify/workflow.md), [verify](../workflow/workflows/verify/public/workflow.md);
- pre-PR readiness: local gates plus `candidate-review`;
- merge readiness: pre-PR gates plus formal [pr-review](../workflow/workflows/pr/review/workflow.md) and required CI;
- release readiness: merge gates plus repository release checks.

Use [pr-worktree](../workflow/workflows/pr/worktree/workflow.md) for isolation, [simplify](../workflow/workflows/code/simplify/workflow.md) before freezing, [nanobot-webui-verify](../workflow/projects/nanobot/webui/workflow.md) for WebUI/gateway surfaces, generic [verify](../workflow/workflows/verify/public/workflow.md) for other public surfaces, [pr-fix](../workflow/workflows/pr/fix/workflow.md) for confirmed remediation, and formal [pr-review](../workflow/workflows/pr/review/workflow.md) only at the fetched PR head.

## Candidate cycle

1. Reuse the task-owned worktree when it matches; otherwise prepare one with [pr-worktree](../workflow/workflows/pr/worktree/workflow.md). Read repository instructions and declare required gates.
2. Share the change contract, supported path, protected behavior, proof obligations, pass rules, and limitations.
3. Run [simplify](../workflow/workflows/code/simplify/workflow.md), finish all edits, then snapshot:

```powershell
python <skill>\scripts\gate_state.py snapshot --repo <worktree> --base <base-ref> --state <evidence>\gate-state.json
```

4. Run read-only gates against that candidate. Record each result with `record --gate ... --status ... --evidence <raw-artifact> --judgment <result>`.
5. Candidate review proves current reachability, material value, contract safety, and change-cone discipline. Formal PR review remains a separate remote-head gate.
6. A content change creates a new candidate and makes prior results `STALE`. Carry an unaffected local result only with a contract-based `--reason`; rerun review, CI, and every gate after a base change.
7. For a confirmed blocker, run [pr-fix](../workflow/workflows/pr/fix/workflow.md) locally, resnapshot, and rerun stale required gates.
8. Check readiness:

```powershell
python <skill>\scripts\gate_state.py check --state <evidence>\gate-state.json --required <gates...>
```

## Publication

With explicit authority, stage intended source paths, commit, push once, and create/update the PR as requested. Resnapshot to confirm content identity, then bind formal review and CI to the exact remote SHA. A remote blocker starts a new local candidate cycle.

## Result

Use `PASS`, `WARN`, `FAIL`, `BLOCKED`, `NOT_RUN`, or `STALE` from the current candidate only. Reply with the requested terminal state, candidate/base/remote identities, per-gate judgments and evidence, findings, CI, publication actions, limitations, and cleanup. Preserve redacted raw evidence and ask before deleting it.
