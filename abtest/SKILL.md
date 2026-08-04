---
name: abtest
description: Design a controlled experiment across isolated control and treatment worktrees. Use for A/B tests, implementation comparisons, benchmark shootouts, causal hypotheses, 对照实验, or 假设验证. The skill prepares the experiment for later execution.
---

# A/B Test

## Design gate

Establish and confirm:

- precise hypothesis;
- control implementation or configuration;
- treatment change;
- judging dimensions and measurement method.

Ask one compact batch when required fields are ambiguous. Return to this gate when the hypothesis or treatment changes.

## Prepare the experiment

1. Inspect both conditions and identify the single treatment variable, controlled variables, evaluation inputs, and confounders.
2. Resolve multi-variable treatments with the user before creating the plan.
3. Create clean detached `.worktrees/ab-control` and `.worktrees/ab-treatment` worktrees from the same fetched base; verify both HEADs.
4. Keep `exp/` ignored in both worktrees.
5. Write `TREATMENT.md` in the treatment worktree with the exact change to apply.
6. Write the same `exp/experiment.md` in both worktrees with hypothesis, paths, controlled variables, procedure, judging dimensions/weights, evidence requirements, result table, and conclusion placeholder.
7. Give the user both paths, confounding risks, and an exact `/goal` command that applies the treatment, evaluates both conditions from identical inputs, records evidence, and decides whether the hypothesis is supported.

This skill prepares the isolated design and handoff. The execution phase applies code changes and runs the comparison.
