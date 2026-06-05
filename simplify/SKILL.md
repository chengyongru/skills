---
name: simplify
description: Cleanup-only code review and refactor workflow for recent or targeted changes. Use when the user asks to simplify, reduce duplication, remove unnecessary complexity, improve reuse, tighten abstractions, or run a Claude Code style /simplify pass after implementation. Applies safe behavior-preserving fixes and does not hunt for correctness bugs.
---

# Simplify

Run a cleanup pass over changed or targeted code, then apply only safe, behavior-preserving fixes.

## Target Selection

1. If the user gives a path, file list, symbol, branch, PR reference, or focus text, use that as the target.
2. If no target is given inside a git repository, inspect the current working tree diff and recently changed untracked files.
3. If no target is given outside git, ask for the files or scope before editing.
4. Treat focus text such as "memory efficiency" or "reuse helpers" as a constraint, not permission to broaden scope.

## Preflight

1. Check repository state with read-only commands first: current branch, changed files, and untracked files.
2. Read the smallest relevant code paths plus nearby helpers, tests, and call sites needed to judge safe cleanup.
3. Identify the verification command from project metadata or existing instructions before editing.
4. If the target includes generated/vendor/lock files, do not edit them unless the user explicitly requested that target.

## Review Passes

Evaluate the target through four cleanup lenses. If subagents are available, these can be delegated independently; otherwise run the passes sequentially.

1. Reuse: prefer existing helpers, components, types, constants, config, validators, and test utilities over new duplicates.
2. Simplicity: remove avoidable branching, indirection, state, layers, wrappers, comments, dead code, and speculative options.
3. Efficiency: improve obvious waste in hot or repeated paths without trading clarity for cleverness.
4. Abstraction level: move logic to the layer that already owns the concept; keep UI, transport, persistence, and domain boundaries clean.

## Fix Policy

Apply a fix only when all of these are true:

1. The current behavior is preserved.
2. The affected surface is within the chosen target.
3. The simpler version is easier to read or maintain in this codebase's existing style.
4. Verification is available or the risk is low enough to state clearly.

Do not:

1. Search for unrelated bugs.
2. Change public APIs, schemas, migrations, persistence formats, dependency versions, or UX behavior unless the user explicitly asks.
3. Perform broad rewrites, formatting churn, or rename-only changes that make the diff noisy.
4. Collapse abstractions that are intentionally protecting ownership boundaries.

## Implementation Workflow

1. Summarize the cleanup opportunities worth applying, grouped by the four review passes.
2. Edit only the files needed for accepted cleanups.
3. Keep patches small and reversible.
4. Update tests only when the simplification requires test maintenance; do not invent large new suites for a cleanup pass.
5. Run the most focused relevant verification. If verification cannot run, explain exactly why.

## Output

Lead with what changed and verification status:

```text
Simplified:
- <behavior-preserving cleanup>
- <behavior-preserving cleanup>

Verification:
- <command>: pass | fail | not run

Skipped:
- <cleanup idea skipped because it was behavior-changing, out of scope, or too risky>
```

If no safe cleanup is found, say that directly and list the evidence checked.
