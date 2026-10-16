# Swarm

## Start

Keep a short checklist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Choose a bounded worker count and concurrency, normally at most two active tasks. Children inherit the runtime-configured model. Races compare attempts or methods, not model families. If explicit cross-model acceptance is required, report it blocked instead of relabeling same-model views.
4. Give each writing worker its own output paths outside the plugin, or a registered worktree via installed [pr-worktree](../../pr/worktree/workflow.md). Children share the local filesystem unless you arrange isolation. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Create native `subagent` tasks with the standalone brief, label, and `wait=false`, launching bounded waves. Keep each returned `task_id`. The brief names allowed reads and writes, a concrete working directory, exact revision, and prohibited side effects. Read-only verification workers must not change files or external state. A child does not get a cloud machine or a branch automatically; prepare authorized local isolation, never an unsolicited push.

Await completion notifications and use `check` only on known IDs when needed. For `first pass`, cancel unnecessary workers after inspecting the winning evidence, then reconcile their final state and task-owned resources before reporting the race complete.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read completed task results and inspect the cited artifacts. If a result omits the SHAs or method its brief requires, name that failure and retry the slice once; silence alone is not a reason to replace a task. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
