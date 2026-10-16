### Orchestrate

**Own the program's scope, dependency graph, evidence, and handoff.** Use this for a project with several independently verifiable units that will need multiple sessions. For one task, use Autonomous run. A program checkpoint is durable; its agents are not. This playbook does not create a standing coordinator, cloud fleet, or unattended service.

#### Frame the program

1. State the requested outcome as a checkable predicate. Separate implementation, local verification, publication, and landing authority.
2. Inventory the current repository, registered worktrees, branches, PRs, exact heads, and existing work. Use installed [pr-worktree](../../workflows/pr/worktree/workflow.md) for branch ownership. Preserve unrelated and dirty worktrees.
3. Split the work into units with explicit dependencies and acceptance evidence. Start with one representative unit to test the brief and verification recipe. If direct execution is simpler, do it; a coordinator-only role is not required.
4. Choose a bounded session budget and a small concurrency cap, normally at most two children. Respect a session-scoped no-subagent request. Do not create nested coordination layers merely to cover a matrix.

#### External run record

Run the shared [workflow helper](../../scripts/workflow.py) with `paths` to locate the agent workspace's `.nanobot-workflows/runs/`. Keep program state in `.nanobot-workflows/runs/<program>/`, outside the installed plugin. These are ordinary files maintained with file tools, not an orchestration service:

- `checkpoint.md`: current user scope, constraints, repository/worktree paths, exact heads, current phase, known child/process handles, blockers, and next action.
- `units.tsv`: unit, dependencies, owner, allowed paths, branch/worktree, state, artifact or PR, and head SHA.
- `verification.tsv`: unit, head/base, check, observed result, evidence path, and limitation. A changed head requires reconciliation, not silent reuse.
- `decisions.tsv`: run the same helper with `log <file> <phase> <decision> <why> <evidence> <result>` when a decision trail is useful.

Give each checkpoint/table one writer. Workers return reports in disjoint owned files; the coordinator incorporates inspected facts. Keep secrets and unrelated conversation data out of the record. A table entry is evidence to verify, not a permission grant.

#### Brief and coordinate

Each unit brief contains the following, compacted to fit the task:

```text
GOAL        observable result
SCOPE       allowed reads/writes; exclusive registered worktree or disjoint paths
CONTEXT     repository instructions, relevant skill/reference paths, dependency evidence
ACCEPTANCE  concrete checks and pass predicates
VERIFY      supported public entrypoint, commands, evidence location, known limitations
BUDGET      finite effort and a partial-report stop condition
FORBIDDEN   out-of-scope fixes and all unauthorized external/destructive actions
REPORT      status, head/base, changed paths, actual checks, evidence, blockers, next step
```

Use native `subagent(action="create", task=..., label=..., wait=false)` for an independent bounded unit, or `wait=true` when its result is needed immediately.

Await normal completion notifications while doing independent work. Use `check` on a known task ID at a decision boundary, not as a polling loop. Use `send` for a clarified scope or dependency update. Its delivery is advisory. Before replacing a writer, request `cancel` when necessary and confirm the old task and its owned processes have stopped. Silence alone is not a failure.

#### Advance the frontier

1. Inspect each returned artifact and its exact head before marking a unit complete. Relay the relevant upstream facts to dependent tasks; siblings do not inherit one another's context.
2. Scale proof to the changed behavior. Use the target project's verifier or [verify](../../workflows/verify/public/workflow.md). Documentation work needs structural/link and instruction checks, not mandatory live/performance fleets. Use installed [pr-review](../../workflows/pr/review/workflow.md) for PR review; publication remains separately authorized.
3. Keep a dependency frontier: the lowest incomplete prerequisite and the units that can proceed without it. For a stack, record the ordered PRs, bases, and head SHAs from `gh`, not from an old report. One owner may change stack topology only within explicit rebase/remote-update authority.
4. Publish or land only when the user's scope covers that action. Use Opening a PR and Shipping for those authorized stages. Otherwise deliver verified local work or a merge-ready recommendation. A worker's completion never implies permission to push or merge.
5. Reconcile after each meaningful change and before reporting. Track done, pending, blocked, failed, and abandoned units separately. A green check list is not proof of resolved reviews or mergeability.

#### Failure, stop, and pickup

A failure gets a bounded diagnosis before a retry: smaller scope for an exhausted task, a corrected prerequisite for a tool failure, or a reported block when the capability is absent. Do not retry indefinitely, change models through an external agent CLI, or widen the program to repair unrelated infrastructure. Record unrelated discoveries as follow-ups.

On a hold, stop new dispatches, send the hold to known children, cancel where needed, and verify final writer/process state before claiming quiescence. At the session budget, save a handoff even if the predicate is unmet. After restart, reconcile Git, PRs, artifacts, and known processes; private child IDs are stale context, not resumable conversations. Start fresh bounded tasks for remaining work.

For a user-requested time or interval, use `cron` with the requested cadence, bounded instructions, and a stop condition. Do not create a schedule as program ceremony or promise work after this turn. Sustained goals require applicable Goal Runtime Guidance.

**Reply:** outcome predicate and evidenced counts, each unit's current state/head, verified versus unverified work, any authorized publications or merges with links, blockers requiring a user decision, and the checkpoint/evidence paths. State what remains, rather than calling a saved checkpoint a running program.
