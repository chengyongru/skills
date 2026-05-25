---
name: abtest
description: Design controlled experiments to compare two implementations or validate a hypothesis. Use when the user wants to A/B test, compare alternatives, run a benchmark shootout, or verify that a change causes a specific effect. Generates a formal experiment spec across two isolated worktrees. Does NOT execute experiments — user reviews the plan then runs it.
tools: Read, Glob, Grep, Bash
---

# A/B Test / Controlled Experiment

Design controlled experiments with isolated worktrees for proper causal inference.

## When to Use

- User says "compare A vs B", "A/B test", "which is better", "benchmark X against Y"
- User wants to validate a hypothesis: "does changing Z cause W?"
- User mentions "controlled experiment", "对照实验", "假设验证"
- User types `/abtest`

## Process

### Setup Gate (Mandatory)

Before any analysis or planning, you MUST have a complete and validated experimental design. This is a BLOCKING prerequisite.

Extract from the user's description:

| Field | Required | Description |
|-------|----------|-------------|
| **Hypothesis** | Yes | What effect are we testing? (e.g., "Replacing algo A with algo B improves readability") |
| **Control** | Yes | Baseline implementation — usually the current code |
| **Treatment** | Yes | Changed implementation — what to compare against the control |
| **Judging dimensions** | No | Which dimensions to evaluate (default: Correctness, Readability, Performance, Maintainability) |

**If ANY required field is missing or ambiguous, use `AskUserQuestion` to collect it BEFORE proceeding.** You may batch up to 4 questions per call.

**Example batch:**

| # | Header | Question |
|---|--------|----------|
| 1 | Hypothesis | What effect are you testing? (e.g., "Does X improve Y?") |
| 2 | Control | What is the baseline? (current implementation / branch / config) |
| 3 | Treatment | What is the changed implementation you want to test? |
| 4 | Judging dimensions | Which aspects matter most? (e.g., readability, performance, correctness) |

After collecting answers, restate the hypothesis concisely and ask for confirmation.

**Re-entry rule:** At ANY later stage, if the user says "change the hypothesis", "adjust the treatment", or similar — STOP current work and return to this Setup Gate.

### 1. Clarify the Design

With the setup gate passed, finalize:

- **Hypothesis**: precise causal claim
- **Control**: baseline code/config
- **Treatment**: changed code/config
- **Judging dimensions**: evaluation criteria (default: Correctness, Readability, Performance, Maintainability)

### 2. Analyze Code

Read the relevant source files for **both** control and treatment conditions. Identify:

- Files that differ between control and treatment (the single variable being tested)
- Files that MUST stay identical (control variables)
- Any confounding variables that could invalidate the experiment

**Critical check:** Verify that only ONE variable changes between control and treatment. If multiple things differ, warn the user and ask which to isolate.

Discovery commands:

```bash
# Detect project type and layout
ls -la *.{json,toml,yaml,yml} 2>/dev/null
# Find source directories
ls -la src/ app/ lib/ internal/ pkg/ 2>/dev/null
# Check for existing benchmarks or tests
ls -la exp/ benchmark/ benchmarks/ tests/ 2>/dev/null
```

### 3. Create Worktrees

Create **two** isolated git worktrees, both based on `origin/main` (or the repo's default branch):

```bash
git worktree add .worktrees/ab-control --detach origin/main
git worktree add .worktrees/ab-treatment --detach origin/main
```

After creation, verify both HEADs match `origin/main` with `git log --oneline -1`.

In the **treatment worktree**, create a `TREATMENT.md` describing the exact changes to apply. Do NOT apply the changes yourself — this skill is read-only for analysis.

Ensure `exp/` is in `.gitignore` in both worktrees.

### 4. Write Experiment Plan

Create `exp/experiment.md` inside **both** worktrees with this structure:

```markdown
# Controlled Experiment: {title}

## Hypothesis
{Hypothesis statement}

## Evaluation Method
- Type: LLM Judge
- Dimensions: {judging dimensions}
- Scale: 1–10 per dimension with weighted total

## Conditions
- Control worktree: {control path}
- Treatment worktree: {treatment path}
- Controlled variables: {what must stay identical between conditions}
- Treatment changes: {summary of changes to apply in treatment worktree}

## Procedure
1. Apply treatment changes to the treatment worktree (see TREATMENT.md)
2. LLM Judge: evaluate both conditions using the rubric below
3. Conclusion: compare scores and decide whether the hypothesis is supported

## LLM Judge

### Judging Criteria (Rubric)

Evaluate both implementations on a 1–10 scale for each dimension:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Correctness | 30% | Does the code behave correctly and handle edge cases? |
| Readability | 25% | Is the code easy to understand and follow? |
| Performance | 25% | Is the implementation efficient in time and space? |
| Maintainability | 20% | Is the code easy to extend, test, and debug? |

### Judging Instructions

1. Read the key files listed in the Scope section from **both** worktrees
2. For each dimension, compare the control vs treatment implementation
3. Assign a score (1–10) to each condition for each dimension
4. Compute the weighted total score for each condition
5. State which condition wins, by how much, and provide specific evidence (file paths, line numbers, code snippets)
6. If a dimension is irrelevant to this experiment, mark it N/A and redistribute weights evenly among the remaining dimensions

### Results

| Dimension | Control | Treatment | Winner | Evidence |
|-----------|---------|-----------|--------|----------|
| Correctness | | | | |
| Readability | | | | |
| Performance | | | | |
| Maintainability | | | | |
| **Weighted Total** | | | | |

## Conclusion
{Empty — filled after LLM judge completes}
```

### 5. Report

Tell the user:

1. The experiment plan is ready in both worktrees (`ab-control/exp/experiment.md` and `ab-treatment/exp/experiment.md`)
2. Key controlled variables and any confounding risks found
3. Give the `/goal` command to run the LLM judge:
   - `/goal In {control path} and {treatment path}, apply the treatment changes from TREATMENT.md. Then evaluate both implementations using the LLM Judge rubric in exp/experiment.md. Score each dimension 1–10, compute weighted totals, fill the Results table with evidence, and state whether the hypothesis is supported.`
4. **Explicitly offer adjustments:** *"If you want to change the hypothesis, treatment, or judging dimensions, just tell me and I'll rewrite the plan."*

## What This Skill Does NOT Do

- Execute experiments or make API calls
- Apply treatment changes to code (only documents them in TREATMENT.md)
- Execute the LLM judge (only writes the rubric and instructions)
- Modify any code (only reads for analysis)

## Constraints

- Worktree isolation: all experiment artifacts live in the worktrees, never in the main workspace
- `exp/` is never committed to git
- The plan must be idempotent — readable and actionable even after context compaction
- Batch questions during Setup Gate (up to 4 per `AskUserQuestion` call) for efficiency, but confirm the full design before proceeding
- Always create exactly two worktrees for proper isolation
- Do NOT assume a fixed directory layout; always discover the codebase structure
