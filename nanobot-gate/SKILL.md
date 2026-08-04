---
name: nanobot-gate
description: Coordinate snapshot-bound simplify, public-interface verification, candidate review, formal GitHub PR review, and CI readiness for nanobot changes. Use when the user invokes $nanobot-gate, asks to run all gates, wants pre-push or merge readiness, needs a change verified before PR creation/release, or wants a resumable evidence-backed remediation loop.
---

# Nanobot Gate

Run nanobot readiness as a candidate state machine, not a fixed script. Bind every conclusion to
one content snapshot, invalidate stale results after edits, publish once, and report only evidence
from the final candidate.

Read [references/state-model.md](references/state-model.md) before starting. Read
[references/report-template.md](references/report-template.md) before writing the plan or final
report. Use the bundled `scripts/gate_state.py` for candidate fingerprints and gate records.

Reuse the detailed procedures in these skills instead of restating them:

- `pr-worktree` for isolated start, fix, and detached review worktrees;
- `simplify` for behavior-preserving cleanup;
- `verify` for public-interface plans, evidence, and cleanup;
- `nanobot-webui-verify` whenever WebUI/browser/gateway behavior is affected;
- `pr-review` only for a real GitHub PR at a fetched remote head;
- `pr-fix` for confirmed gate remediation.

Load each skill before its phase first needs it.

## Invariants

- Work in the intended independent worktree and read applicable `AGENTS.md`,
  `CONTRIBUTING.md`, and relevant design/security/gotcha guidance.
- Preserve unrelated tracked and untracked changes. Never reset, discard, force-push, or use broad
  cleanup to make a gate green.
- Treat the diff as user-owned until edits are authorized. `simplify` may make only safe,
  behavior-preserving cleanup. `pr-fix` may repair only confirmed findings.
- Never mutate the candidate while tests, browser checks, or review of that candidate are running.
- Bind gate evidence to the candidate ID in `gate-state.json`. A result from another candidate is
  `STALE`, not supporting evidence.
- Default to invalidating all recorded gates after a content change. Carry a result only when its
  protected contract is demonstrably unaffected, and record the reason.
- Verify through a public interface with a written observable pass rule. Source inspection, lint,
  build, type checks, and unit tests are supporting evidence, not a substitute.
- Keep remediation local. Commit, push, create/update a PR, or perform any other GitHub mutation
  only when explicitly authorized and only after the unpublished candidate is ready.
- Publish once per completed local-ready candidate cycle. Do not push intermediate repairs. A
  post-publication blocker starts a new local cycle and requires publication authority again.
- A formal `pr-review` requires a real GitHub PR and a clean detached worktree matching its fetched
  head. A local candidate review is a prerequisite, not a substitute for formal PR review.
- Never approve, merge, close, label, comment on, or otherwise mutate a PR without exact
  authorization. PR creation is opt-in.
- Preserve redacted evidence and ask before deleting it.

## 1. Prepare and declare the terminal state

Determine what the user is asking the gate to prove:

- **local readiness**: simplify and verify are required; formal PR review is optional;
- **pre-PR readiness**: simplify, verify, and a read-only candidate review are required;
- **merge readiness**: simplify, verify, candidate review, formal PR review, and required remote CI
  are required;
- **release readiness**: merge-readiness gates plus repository release checks are required.

Record required versus optional gates before execution. `NOT_RUN` for an optional gate does not
degrade the overall result; `NOT_RUN` for a required gate does.

Inspect the current worktree before creating another:

- Reuse a task-owned topic/fix worktree, including authorized dirty candidate changes.
- Reuse a review worktree only when it is clean, detached, and matches the fetched PR head.
- Otherwise use `pr-worktree start` for a new candidate or `prepare --mode fix|review` for a PR.
- Never switch or stash the user's unrelated workspace.

Create a unique evidence directory:

~~~text
<worktree>\webui\.verify-evidence-gates-<run-id>\
~~~

Record status, branches, remotes, recent commits, repository instructions, PR metadata, and CI.
Use `verify`'s context collector when available.

## 2. Establish contract and plan

Before tests or code edits, write:

- purpose and evidence-backed present-day value;
- changed user/public surfaces and the supported path to the changed boundary;
- expected and actual change cone;
- protected behavior, compatibility, persistence, security, and lifecycle contracts;
- proof obligations, pass rules, required gates, and limitations;
- the cheapest high-signal checks and the escalation conditions for broader checks.

Discover interfaces from repository evidence. Do not assume every change needs WebUI, gateway, or
the full test suite. Prefer this cost order:

~~~text
static/contract checks -> focused tests -> public black-box check -> broader suite -> remote CI
~~~

Write the verification plan using the report template before executing it.

## 3. Normalize, then freeze the candidate

Run `simplify` before final verification:

1. Audit reuse, avoidable complexity, repeated work, and abstraction ownership.
2. Apply only behavior-preserving cleanup inside the change cone.
3. Run the narrowest focused proof for any cleanup.
4. Record either the exact edit or “no safe cleanup found.”

Do not run broad `ruff format`; nanobot repository guidance prohibits it.

After all mutating cleanup stops, create or refresh the candidate snapshot:

~~~powershell
python <skill>\scripts\gate_state.py snapshot --repo <candidate-worktree> --base <base-ref> --state <evidence>\gate-state.json
python <skill>\scripts\gate_state.py record --state <evidence>\gate-state.json --gate simplify --status PASS --required --evidence <path> --judgment "<result>"
~~~

The candidate ID fingerprints the base and materialized diff, including non-ignored untracked files.
A content-preserving commit does not invalidate local evidence; a changed base or diff does.

## 4. Run read-only gates against the frozen candidate

When tools and resources allow, run independent read-only verification and review work in parallel.
Every action must use the frozen candidate and state its candidate ID.

### Verify

Invoke `verify`. Load `nanobot-webui-verify` only for browser-visible, route, settings, chat,
sidebar, or gateway-facing changes.

- Run the smallest set that proves the contract.
- Exercise the changed workflow through CLI, API, package consumer, service, or built WebUI.
- Capture command metadata, output, runtime logs, visible state, and screenshots/snapshots where
  relevant.
- Use isolated disposable config/workspaces and fresh ports. Never expose credentials.
- For WebUI, build first, use the real gateway/WebSocket path, wait on the documented HTTP
  readiness endpoint, exercise visible controls, inspect console/runtime errors, and verify
  persistence when relevant.
- Escalate to broader local tests only when risk, repository policy, or earlier results justify it.

If an unrelated check fails, perform differential baseline triage only then: run the exact failing
check against the fetched base or original PR head in an isolated worktree. Classify:

- candidate fails, baseline passes: regression (`FAIL`);
- both fail identically: baseline limitation (`WARN`) only if changed-path proof remains complete;
- baseline cannot run: `BLOCKED` or `WARN` according to whether required proof remains possible.

### Candidate review

Perform a read-only review of the frozen local candidate before publication:

- prove supported-path reachability and net value before deep findings;
- review contract boundaries, compatibility, failure handling, and change-cone discipline;
- classify observations as Confirmed, Risk, Question, or Not a finding;
- put only confirmed actionable problems in the findings list.

Call this **candidate review**, never formal PR review. Record it as `candidate-review` in the state
manifest. If a real PR already points to exactly the same candidate content, formal `pr-review` may
run now in its detached review worktree.

Record gate results with `gate_state.py record`. Include `--remote-head <sha>` for formal review.

## 5. Remediate with incremental invalidation

For a confirmed blocking finding, invoke `pr-fix` in gate-remediation mode:

1. Establish trigger, consequence, violated contract, change cone, and focused proof.
2. Make the smallest local fix in the reusable candidate worktree.
3. Refresh the candidate snapshot before trusting any result:

   ~~~powershell
   python <skill>\scripts\gate_state.py snapshot --repo <candidate-worktree> --base <base-ref> --state <evidence>\gate-state.json
   ~~~

4. By default every prior result becomes `STALE`. Carry an unaffected result only with
   `--carry <gate> --reason "<contract-based reason>"`; convenience is not a reason.
   Never carry candidate/formal review, remote CI, or any result across a base commit change.
5. Rerun stale required gates and the focused regression proof.

Repeat until the unpublished candidate is ready or an external blocker requires user direction.
Do not commit or push inside this loop.

Before publication, run:

~~~powershell
python <skill>\scripts\gate_state.py check --state <evidence>\gate-state.json --required simplify verify candidate-review
~~~

Candidate review must have no confirmed blocker. It is intentionally distinct from formal
`pr-review` unless a matching PR exists.

## 6. Publish once, then reconcile remote state

Only with authorization:

1. Confirm only intended files changed; exclude evidence and disposable runtime files.
2. Commit without rewriting existing history.
3. Push normally; never force-push without explicit approval.
4. Create a PR only when explicitly requested.
5. Re-run `snapshot`. If the content-derived candidate ID is unchanged, local simplify/verify
   evidence remains current even though HEAD changed.
6. Fetch PR metadata and confirm the remote head SHA contains the same candidate.
7. Run formal `pr-review` in a clean detached worktree at that exact SHA.
8. Wait for required CI and record `remote-ci` against the same remote SHA.
9. Update title/body only when the final scope made existing metadata materially inaccurate and the
   applicable authorized workflow permits it. Preserve valid issue links and context.

If push, PR creation, fork write access, or required checks are blocked, stop at that boundary and
report the exact state. Do not claim merge readiness.

If formal review or CI finds a blocker after publication, mark the remote gates failed, return to a
new local remediation cycle, and require local readiness plus publication authority before another
push. Do not repeatedly push work-in-progress repairs.

## 7. Status and completion rules

Use:

- `PASS`: required contract is proven for the current candidate;
- `WARN`: primary behavior passes but a material non-blocking limitation remains;
- `FAIL`: current candidate violates a required contract;
- `BLOCKED`: required proof cannot proceed because of environment, authority, or infrastructure;
- `NOT_RUN`: gate was optional or not applicable; state which;
- `STALE`: result belongs to another candidate and cannot support the conclusion.

Run `gate_state.py check` before the final report. Overall status is computed only from gates
declared required for the requested terminal state:

- `PASS`: every required gate passes;
- `WARN`: no required gate fails, but a required gate warns or a material limitation remains;
- `FAIL`: any required gate fails;
- `BLOCKED`: no failure is established, but required work cannot proceed;
- never finish from a `STALE` required result.

## Evidence and cleanup

At minimum retain:

- `gate-state.json`, contract, verification plan, and candidate IDs;
- context/status, diff, command metadata, stdout, and stderr;
- public-interface evidence and runtime/browser logs where relevant;
- baseline comparison evidence for any failure reclassification;
- PR metadata, reviewed remote SHA, and CI state.

Redact tokens, cookies, API keys, authorization headers, and user configuration. Record PIDs and
ports before startup. Stop exact processes, close browser sessions, remove only pre-validated
disposable runtime/config/test data, and prove ports are released. Keep the evidence directory.

## Final report

Use `references/report-template.md`. Lead with outcome and PR link. Include:

- terminal state requested, required gates, final candidate ID, base, and remote head;
- per-gate status, evidence, pass-rule judgment, and whether anything was carried;
- candidate-review result and formal PR-review result without conflating them;
- baseline comparisons, CI coverage, findings, risks, limitations, and cleanup;
- every publication handoff and GitHub mutation performed.

Ask whether to delete the retained evidence directory.
