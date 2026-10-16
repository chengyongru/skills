### Feature

**Own the design, observable contract, and verification.** Implement directly or use bounded children where the work genuinely separates. A session-scoped no-subagent request prevails.

1. Ground the affected subsystem with [how](../../workflows/investigate/how/workflow.md). State the user-visible result, exclusions, compatibility constraints, and acceptance criteria. Product direction is not inferred from a convenient implementation.
2. Explore consequential alternatives with [architect](../../workflows/code/architect/workflow.md), [arena](../../workflows/coordinate/arena/workflow.md), or a small isolated Prototype when warranted and within scope. A straightforward change does not need competing agents.
3. Keep a brief throughput checkpoint, with justified `n/a` entries when appropriate:
   - **Blocking prerequisites:** contracts, shared primitives, fixtures, or user decisions needed first.
   - **Independent workstreams:** truly disjoint outputs that can proceed safely in parallel.
   - **Shared mutable state:** split the target before serializing a genuine shared invariant.
   - **Smallest safe decomposition:** direct execution or a bounded fan-out, normally at most two children.
4. Choose the data shape before adding logic: a state machine for lifecycle, a registry for repeated policy, or a typed model for repeated assumptions. Prefer boring local code when a new abstraction would add more reader load than it removes. Keep public APIs, persistence, migrations, and live/shared state inside the agreed change boundary.
5. Implement in verifiable slices. For delegated work, use native `create` with scope, actual reference paths, exclusive registered worktree/disjoint paths, forbidden external actions, acceptance checks, and a finite report boundary. Use `send` for clarification, `check` on known tasks when needed, and `cancel` with final-state reconciliation before replacing a writer. Do not specify a model, agent type, or environment. Use installed [pr-worktree](../../workflows/pr/worktree/workflow.md) for branch ownership.
6. Inspect the diff and use installed [simplify](../../workflows/code/simplify/workflow.md) for behavior-preserving cleanup when appropriate. Update affected in-scope consumers of a shared change and verify their contracts; do not silently port unrelated improvements across the repository. Respect the no `ruff format` constraint.
7. Prove the changed behavior through the supported interface with the matching installed verifier: [nanobot-webui-verify](../../workflows/verify/webui/workflow.md) for nanobot browser flows, another project verifier, or [verify](../../workflows/verify/public/workflow.md). Cover the changed happy path and highest-risk reachable edge. Terminal behavior needs real supported-terminal evidence. Scale checks to risk; inconclusive, unavailable, or wrong-surface proof is not PASS.
8. Record exact artifact/head, checks, evidence, and remaining decisions in `.nanobot-workflows/runs/<run>/` when a checkpoint is useful. Commit, rebase, push, or open a PR only if covered by the user's scope. Opening a PR is a conditional delivery stage, not the automatic end of feature work.

For one code-coupled feature or migration, prefer one owner and a clear dependency sequence. Parent-level fan-out is for independent artifacts, not two writers on the same model or branch. Reassess the checkpoint at phase boundaries without expanding scope.

**Reply:** built behavior, key choices and tradeoffs, throughput checkpoint, real verification and limitations, delivery state, and open user decisions.
