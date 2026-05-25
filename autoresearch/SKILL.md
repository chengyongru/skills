---
name: autoresearch
description: Turn improvement ideas into formal, auditable experiment plans with isolated worktrees. Use when the user wants to improve, optimize, experiment with, compare, or validate a hypothesis about any codebase behavior. Generates a formal experiment spec and creates an isolated worktree. Does NOT execute experiments — user reviews the plan then runs it.
tools: Read, Glob, Grep, Bash
---

# Autoresearch

Turn improvement ideas into formal, auditable experiment plans with isolated worktrees.

## When to Use

- User says "optimize X", "improve Y", "experiment with Z", "compare A vs B", "validate hypothesis about W", or any request involving measurable changes to a codebase
- User wants to prototype or spike a change in isolation before committing to the main branch
- User types `/autoresearch`

## Process

### Setup Gate (Mandatory)

Before any analysis or planning, you MUST have a complete and validated goal. This is a BLOCKING prerequisite — do NOT proceed to code analysis or worktree creation until the gate passes.

Extract from the user's initial prompt:

| Field | Required | Description |
|-------|----------|-------------|
| **Target** | Yes | Which subsystem, module, or behavior to change |
| **Metric** | Yes | How to measure the outcome (must be quantifiable: latency, accuracy, coverage, build time, error rate, token count, etc.) |
| **Baseline** | No | Current metric value (infer from code/tests if not provided; ask only if inference fails) |
| **Target value** | Yes | What value constitutes success |

**If ANY required field is missing or ambiguous, use `AskUserQuestion` to collect it BEFORE proceeding.** You may batch up to 4 questions per call.

**Example batch:**

| # | Header | Question |
|---|--------|----------|
| 1 | Target | What subsystem or behavior do you want to improve? |
| 2 | Metric | What number tells you if it got better? (e.g., test coverage %, response time ms, build time s) |
| 3 | Baseline | Do you know the current value? If not, I'll try to infer it from the codebase. |
| 4 | Target value | What value would you consider success? |

After collecting answers, restate the goal concisely and ask for confirmation: *"Target: improve X. Metric: Y. Goal: reach Z. Is this correct, or would you like to adjust anything?"*

**Re-entry rule:** At ANY later stage (analysis, planning, or after the plan is written), if the user says "change the goal", "adjust the metric", "let's try a different target", or similar — STOP current work and return to this Setup Gate. Re-collect fields that changed, then re-analyze and rewrite the plan.

### 1. Clarify the Goal

With the setup gate passed, finalize:

- **Target**: subsystem, module, or behavior
- **Metric**: quantifiable measure
- **Baseline**: current value (infer from code/config/tests/logs if user did not provide)
- **Target value**: success threshold

If baseline inference fails, ask the user for it. Do not guess.

### 2. Analyze Code

Read the relevant source files to identify actionable intervention points. Use `Glob` and `Grep` to discover the codebase structure — do NOT assume a fixed directory layout.

Discovery commands to run:

```bash
# Detect project type and layout
ls -la *.{json,toml,yaml,yml} 2>/dev/null
# Find source directories
ls -la src/ app/ lib/ internal/ pkg/ 2>/dev/null
# Check for existing experiments or benchmarks
ls -la exp/ benchmark/ benchmarks/ tests/ 2>/dev/null
```

Key things to identify:

- Relevant modules or functions mentioned by the user
- Configuration files that control the target behavior
- Existing benchmarks or tests that could serve as evaluation
- Any prior experiment history in `exp/` or similar

Output a concise list of files and parameters that could be changed to affect the target metric.

### 3. Create Worktree

Create an isolated git worktree based on `origin/main` (or the repo's default branch). Use `--detach` to avoid branch conflicts (the target branch may already be checked out in another worktree):

```bash
git worktree add .worktrees/exp-<name> --detach origin/main
```

Where `<name>` is a short kebab-case identifier derived from the experiment target.

After creation, verify with `git log --oneline -1` that HEAD matches `origin/main`. Do NOT use `git merge` to bring in main content — the worktree must be a clean checkout.

Ensure `exp/` is in `.gitignore` within the worktree (add it if missing).

### 4. Write Experiment Plan

Create `exp/experiment.md` inside the worktree with this structure:

```markdown
# Experiment: {title}

## Goal
{Original user description}

## Metric
- Name: {metric name}
- Baseline: {current value}
- Target: {target value}

## Scope
- Base branch: {branch}
- Worktree: {worktree path}
- Key files:
  - {file paths identified in code analysis}

## Intervention Points
{For each actionable point, describe what could be changed and why it might affect the metric}

## Constraints
- Max rounds: 10
- Convergence: stop after 3 consecutive rounds with no improvement
- Evaluation: determined by execution agent based on experiment content
- Each round must document: hypothesis, change made, verification method, expected result

## Execution

If your agent supports `/goal`, run this in the worktree to execute autonomously:

```
/goal Improve {target} so that {metric} goes from {baseline} to {target value}. Work inside this worktree ({worktree path}). Follow the plan in exp/experiment.md. After each change, run the verification method documented in the plan. Stop when the metric reaches the target or after max rounds.
```

## Results
{Empty — filled during execution}
```

### 5. Report

Tell the user:

1. The experiment plan is ready at `{worktree path}/exp/experiment.md`
2. Key intervention points found
3. Give the exact `/goal` command to run in the worktree (derived from the experiment plan). For example: `/goal Improve {target} so that {metric} reaches {target value}. Follow the plan in exp/experiment.md and verify after each change.` — this hands the plan off to the agent's sustained-goal loop for autonomous execution
4. **Explicitly offer adjustments:** *"If you want to change the goal, metric, or scope, just tell me and I'll rewrite the plan."*

## What This Skill Does NOT Do

- Execute experiments or make API calls
- Pre-judge evaluation methods (script vs LLM judge — execution agent decides)
- Modify any code (only reads for analysis)
- Write evaluation scripts or judge prompts

## Constraints

- Worktree isolation: all experiment artifacts live in the worktree, never in the main workspace
- `exp/` is never committed to git
- The plan must be idempotent — readable and actionable even after context compaction
- Batch questions during Setup Gate (up to 4 per `AskUserQuestion` call) for efficiency, but confirm the full goal before proceeding
- Do NOT assume nanobot-specific paths or structures; always discover the codebase layout
