---
name: pr-label
description: Use when the user wants to inspect, classify, add, remove, replace, synchronize, or verify labels on a GitHub pull request; require evidence-backed current impact for bug, security, severity, and priority classifications, preserve unrelated labels, plan changes before applying them, and use the bundled REST-based helper for authorized mutations
---

# PR Label

Separate classification from mutation: infer what a label means from repository evidence, then let the bundled helper perform the mechanical update and verification.

## Authorization boundary

- Reading label policy, inspecting labels, or producing a plan is read-only.
- A review, triage, or fix request alone does not authorize label changes.
- A request to label the named PR authorizes only the requested PR label mutation.
- Creating, renaming, recoloring, or deleting repository-level labels requires separate explicit authorization and is outside the bundled helper.
- Never change review state, merge state, milestones, assignees, projects, or branches through this skill.
- An explicit request to add or remove an exact label authorizes that mutation, but does not make the label an evidence-backed classification. Report the distinction instead of inventing support.

## Workflow

### 1. Establish repository policy

Separate mutation instructions from classification evidence. Use:

1. the user's exact instruction for mutation scope and authorization;
2. explicit user-provided or repository-documented label policy;
3. label automation/configuration and label descriptions;
4. consistent recent maintainer usage;
5. clarification when the choice remains material and ambiguous.

Do not infer severity, priority, or exclusivity from a familiar-looking label name alone. Read [references/label-policy.md](references/label-policy.md) when choosing among labels or identifying an exclusive family.

### 2. Inspect deterministically

```bash
python3 <this-skill>/scripts/pr_label.py inspect <PR-number-or-URL> --repo <OWNER/REPO> --format markdown
```

Omit `--repo` when a PR URL supplies it or the current repository is unambiguous. The helper returns PR metadata, current labels, and available repository labels with descriptions.

### 3. Explain the classification

For every proposed label, state the evidence from the PR and the repository rule it satisfies. Distinguish:

- **confirmed classification**: repository policy and PR evidence clearly select it;
- **provisional classification**: plausible, but policy or PR intent is incomplete;
- **contradicted classification**: current repository evidence shows that the label's required impact or scope is absent;
- **mechanical cleanup**: removing a stale/conflicting label without changing the substantive classification.

Before recommending a bug/fix, security, severity, or priority label, require:

1. a current supported entrypoint, affected actor, or operational workflow;
2. a repository-owned path from that entrypoint to the behavior;
3. a concrete present-day consequence;
4. the repository rule mapping that consequence to the label.

A direct internal-helper test, synthetic state, author claim, existing label, sensitive-looking filename, or hypothetical future extension is insufficient. If repository design makes the scenario impossible or no supported consumer reaches it, classify impact labels as unsupported. When synchronization or reclassification is authorized, plan their exact removal; otherwise report the mismatch without mutating it.

Reuse an evidence-backed review or triage conclusion when available. Otherwise inspect only the shortest current caller/contract path needed for classification. If reachability remains unresolved, do not conduct a full code review inside this skill and do not recommend an impact label.

Do not add provisional security, severity, or priority labels unless repository policy explicitly defines them as investigation/workflow labels. Do not use a label to make an unproven review finding appear authoritative.

### 4. Plan the minimal update

Adding an independent label:

```bash
python3 <this-skill>/scripts/pr_label.py update <PR> --repo <OWNER/REPO> --add "<label>" --format markdown
```

Replacing one member of a repository-defined exclusive family:

```bash
python3 <this-skill>/scripts/pr_label.py update <PR> --repo <OWNER/REPO> --add "<target>" --exclusive-prefix "<family-prefix>" --format markdown
```

The default is a dry run. The helper validates added labels against the repository taxonomy, computes removals, and preserves unrelated labels. Use explicit `--remove "<label>"` for conflicts that cannot be represented safely by a prefix.

For an authorized synchronization or reclassification, treat contradicted impact labels as substantive corrections and remove them explicitly. For a narrower add-only request, preserve them and report the evidence mismatch rather than broadening the mutation.

Review the before/planned-after state. If there is no change, stop and report the no-op.

### 5. Apply only when authorized

Repeat the reviewed command with `--apply`:

```bash
python3 <this-skill>/scripts/pr_label.py update <PR> --repo <OWNER/REPO> --add "<label>" --apply --format markdown
```

The helper adds before removing, uses the REST issue-label API, rereads the PR, and verifies that targets are present, removals are absent, exclusive families have one target, and unrelated pre-existing labels remain.

### 6. Report

Report:

- classification and supporting repository/PR evidence;
- any existing impact label whose reachability or consequence is unsupported;
- labels before and after;
- whether the operation was a plan, no-op, or applied update;
- any ambiguity, missing label, partial failure, or verification failure.

Do not claim success from the write response alone; require the verified after-state.

## Failure handling

- **Unknown target label**: stop; do not create it or substitute a similar name.
- **Ambiguous taxonomy**: return a plan or ask for the missing policy decision.
- **Unproven impact classification**: do not recommend it; if the user explicitly ordered that exact mutation, perform only the authorized change and report it as directive rather than confirmed classification.
- **Multiple targets in one exclusive family**: stop and choose one.
- **API or verification failure**: report the observed after-state; do not retry removals blindly.
- **Concurrent unrelated additions**: preserve them.
- **Concurrent removal of an unrelated pre-existing label**: report verification failure rather than silently restoring or overwriting it.
