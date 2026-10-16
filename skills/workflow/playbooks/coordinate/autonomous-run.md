### Autonomous run

**Own a checkable exit condition within a bounded session.** A request to keep going authorizes continued work in scope, not unlimited runtime, unrelated fixes, or new external actions.

1. State the exit predicate, allowed paths/actions, verification method, and session budget before iterating. Separate a local result from any conditional commit, push, PR, or merge. Sustained-goal execution requires applicable Goal Runtime Guidance; this playbook alone is not that guidance.
2. Work directly, or use bounded native children when helpful and permitted. Give each child a concrete scope, acceptance evidence, prohibited external actions, and a finite partial-report boundary. Respect a no-subagent request. Await normal completion; use `check` on known IDs only at decision boundaries, `send` for clarification, and `cancel` plus final-state reconciliation before replacing a writer.
3. Make the smallest change the evidence justifies. Verify one unit before the next. Keep only justified changes; remove a disproven experiment only from your own known edits, without resetting or cleaning a shared tree. Commit or publish only within the user's authorization.
4. Fix blockers inside the requested task. Record unrelated bugs, broken skills, flaky infrastructure, review noise, and possible follow-ups instead of repairing them automatically. Do not edit live plugins, protected profiles/memory, tickets, or separate messages as side work.
5. After each meaningful iteration, update a single-writer checkpoint in the agent workspace's `.nanobot-workflows/runs/<run>/`: hypothesis, exact head/state, observed result, evidence, known handles, and next action. Use the shared [workflow helper](../../scripts/workflow.py) `paths` command to locate it and the supported `log` command when a decision trail helps.
6. Stop when the predicate is met, the user stops the work, a required capability/decision blocks progress, or the runtime budget is reached. A plateau calls for a bounded evidence-based pivot, not infinite retries or a relaxed predicate. Report partial progress honestly and leave a pickup note.

For a user-requested time or interval, use `cron` with the requested cadence, a bounded task, and a stop condition.

**Reply:** predicate, iterations and evidence, kept versus rejected changes, any authorized publications, final predicate state, remaining blockers, and checkpoint path.
