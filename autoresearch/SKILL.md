---
name: autoresearch
description: Turn a measurable codebase improvement idea into an auditable experiment plan in an isolated worktree. Use for optimization, improvement, experimentation, comparison, or hypothesis-validation planning. The skill prepares the experiment for later execution.
---

# Autoresearch

## Goal gate

Establish and confirm:

- target subsystem or behavior;
- quantifiable metric;
- target value;
- baseline, inferred from repository evidence when available.

Ask one compact batch when required fields are ambiguous. Return to this gate whenever the goal or metric changes.

## Prepare the experiment

1. Discover the repository layout, relevant source/config, benchmarks, tests, and prior experiment artifacts.
2. Identify the smallest intervention points that can affect the metric.
3. Create a clean detached worktree from the fetched default branch under `.worktrees/exp-<name>` and verify its HEAD.
4. Keep `exp/` ignored in the experiment worktree.
5. Write `exp/experiment.md` containing:
   - goal, metric, baseline, target, base, worktree, and key files;
   - intervention points and protected constraints;
   - evaluation method and per-round evidence;
   - maximum 10 rounds and convergence after 3 rounds with no improvement;
   - an empty results section.
6. Give the user the worktree path, key intervention points, and an exact `/goal` command that executes the plan and verifies each round.

This skill reads code, creates the isolated planning worktree, and writes the plan. The execution handoff owns code changes, evaluation, and results.
