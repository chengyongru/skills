# Code

For an existing GitHub PR fix use the [PR route](pr.md); preserve its head branch and publication boundary. Otherwise choose the requested change below. Read repository instructions and existing dirty state before writing.

| Work | Workflow or playbook |
|---|---|
| Settle types, state ownership, or module shape (`architect`) | [Architecture](../workflows/code/architect/workflow.md) |
| Reproduce and fix a defect | [Bug fix](../playbooks/code/bug-fix.md) |
| Add or change a feature | [Feature](../playbooks/code/feature.md) |
| Simplify code or audit comments/workarounds | [Simplify](../workflows/code/simplify/workflow.md) |
| Apply the focused `no-comments` lens | [Comment method](../workflows/code/simplify/methods/comments.md) |
| Larger behavior-preserving structural change | [Refactoring](../playbooks/code/refactoring.md) |
| A requested or cheap, concrete regression-first path (`tdd`) | [Test first](../workflows/code/test-first/workflow.md) |
| TypeScript data modeling and API boundaries | [TypeScript](../workflows/code/typescript/workflow.md) |
| Trace consequences outside the diff (`blast-radius`) | [Blast radius](../workflows/code/blast-radius/workflow.md) |
| Refine product UI, settings, sidebars, or dashboards | [UI design](../workflows/code/ui/workflow.md) |
| Match an existing visual implementation | [Visual parity](../playbooks/code/visual-parity.md) |
| Compare authorized disposable designs | [Prototype](../playbooks/code/prototype.md) |
| Fix measured slowness | [Performance](../playbooks/code/perf-issue.md) |
| Run a bounded optimization hypothesis loop | [Hillclimb](../playbooks/code/hillclimb.md) |
| Build a UI for an existing, documented, authorized webhook | [Webhook UI](../workflows/code/webhook-ui/workflow.md) |

For simplification, the focused simplify workflow owns edits; the comment method supplies a lens, not a second competing cleanup process. A plan-only request stops at the plan. Use the [verification route](verify.md) for changed public behavior, and read a relevant [principle](../references/principles.md) only when it resolves a concrete design decision.
