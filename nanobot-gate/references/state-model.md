# Gate state model

Use this model to keep results current, resumable, and auditable.

## Candidate identity

`gate_state.py` computes a candidate ID from:

- the resolved base commit;
- `git diff --binary <base>` against the materialized candidate worktree;
- every non-ignored untracked file path and content.

Ignored evidence/runtime files do not affect the ID. A commit that preserves the same base-relative
content keeps the ID, even though HEAD changes. A base advance, source edit, test edit, dependency
change, or newly added non-ignored file changes the ID.

The remote PR head SHA is a separate identity. Local simplify/verify evidence binds to candidate
content; formal PR review and CI bind to both candidate content and the remote SHA.

## State transitions

~~~text
PREPARED
  -> NORMALIZING       simplify may edit
  -> FROZEN            candidate ID recorded
  -> CHECKING          read-only verify and review
  -> READY_LOCAL       required unpublished gates pass
  -> REMEDIATING       confirmed finding; edits allowed
       -> FROZEN       new ID; old results stale or explicitly carried
  -> PUBLISHED         one authorized commit/push/PR handoff
  -> CHECKING_REMOTE   formal PR review and CI at exact SHA
       -> REMEDIATING  post-publication blocker starts a new local-ready cycle
  -> READY             requested terminal state proven
~~~

At any point, a content change moves the run back to `FROZEN` with a new ID. Never report `READY`
from evidence attached to a previous ID.

## Gate statuses

| Status | Meaning | Final use |
|---|---|---|
| `PASS` | Contract proven for current candidate | Supports readiness |
| `WARN` | Main contract passes with a material non-blocking limitation | Degrades overall result |
| `FAIL` | Current candidate violates a required contract | Blocks readiness |
| `BLOCKED` | Authority, environment, or infrastructure prevents required proof | Blocks completion without asserting a code defect |
| `NOT_RUN` | Optional/not applicable, or not yet executed | Harmless only when optional |
| `STALE` | Result belongs to another candidate | Never supports readiness |

## Invalidation policy

Safety default: when candidate content changes, mark every recorded gate `STALE`.

Carry a result only when all are true:

1. its protected contract cannot be affected by the changed files or behavior;
2. its evidence remains meaningful for the new candidate;
3. the carry reason names the unaffected contract, not merely the small size of the edit;
4. no repository rule requires rerunning it.

Examples:

| Change | Default action |
|---|---|
| Source, runtime config, dependency, schema, or migration | Invalidate simplify, verify, and review |
| Test-only change | Invalidate simplify/candidate review/formal review/CI and any verification that relied on those tests |
| Public copy, locale, accessibility, route, or UI state | Invalidate verify, review, and CI; rerun simplify unless explicitly carried |
| Ignored evidence/report file | Candidate ID unchanged; no invalidation |
| Content-preserving commit | Candidate ID unchanged; keep local gates, refresh remote SHA-bound gates |
| Base commit advances | Invalidate all gates |
| CI status changes without candidate change | Refresh CI/review remote state only |

Do not carry a `FAIL` or `BLOCKED` result. A repair must make the old conclusion stale and rerun the
relevant proof.

Never carry `candidate-review`, formal `pr-review`, or `remote-ci`, and never carry any gate across
a base commit change. These alter or bind to the complete candidate/review object, so their results
must be regenerated.

## Parallel execution

After `FROZEN`, read-only tasks may overlap when they use independent resources:

- focused tests, static checks, PR metadata, and detached review;
- WebUI build and non-WebUI static checks;
- CI polling and local evidence/report preparation.

Serialize:

- every candidate mutation;
- browser/gateway runs that share ports, config, workspace, or output;
- publication and any post-publication remote reconciliation;
- reruns after a candidate ID change.

If a mutation begins while a read-only action is still running, discard that action's conclusion
even if it later exits successfully.

## Candidate review versus formal PR review

Candidate review is a local, read-only pre-publication check. It proves value, reachability, scope,
contracts, and absence of confirmed blockers. Record it as `candidate-review`, never as formal
`pr-review`.

Formal PR review requires:

- a real GitHub PR;
- fetched metadata and base;
- a clean detached worktree;
- detached HEAD matching the PR head SHA;
- candidate content matching the final candidate ID.

This distinction removes the publication cycle:

~~~text
candidate review + local gates -> publish once -> formal PR review + CI
~~~

“Publish once” means once per locally ready candidate cycle. If formal review or CI finds a
post-publication blocker, the remote candidate is no longer ready: remediate locally, create a new
candidate ID, rerun required local gates, and obtain or confirm authority before another push.

## Differential baseline triage

Run a baseline comparison only after a candidate check fails or produces ambiguous evidence.
Use the exact command, environment, inputs, and public action where practical.

| Candidate | Baseline | Classification |
|---|---|---|
| pass | any | Candidate proof passes; no baseline run needed |
| fail | pass | Regression; `FAIL` |
| fail | same failure | Baseline limitation; `WARN` only if changed contract is still independently proven |
| fail | unavailable | `BLOCKED` when proof is required, otherwise explicit `WARN` |
| different failures | fail | Investigate; do not classify as baseline-equivalent |

Record both candidate IDs/SHAs and evidence paths.

## State helper commands

Create or refresh:

~~~powershell
python scripts/gate_state.py snapshot --repo <worktree> --base <base-ref> --state <evidence>\gate-state.json
~~~

Refresh after a change while explicitly carrying an unaffected result:

~~~powershell
python scripts/gate_state.py snapshot --repo <worktree> --base <base-ref> --state <evidence>\gate-state.json --carry simplify --reason "Only ignored runtime evidence changed; source and simplify contract are unchanged"
~~~

Record:

~~~powershell
python scripts/gate_state.py record --state <state> --gate verify --status PASS --required --evidence <report> --judgment "Public pass rule proven"
~~~

Check readiness:

~~~powershell
python scripts/gate_state.py check --state <state> --required simplify verify pr-review
~~~

Inspect:

~~~powershell
python scripts/gate_state.py show --state <state>
~~~

The helper enforces candidate freshness but does not decide whether a carry is semantically valid;
the gate operator remains responsible for that judgment.
