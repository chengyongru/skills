---
name: pr-label
description: Inspect, classify, add, remove, replace, synchronize, or verify GitHub PR labels through the remote GitHub API. Use repository evidence for inferred impact classifications, preserve unrelated labels, and use the bundled REST helper for authorized mutations.
---

# PR Label

Manage existing PR labels only through the remote API; do not prepare a `pr-worktree`. Exact requested PR label changes are authorized by the request. Do not create/delete repository labels or change code, branches, PR text, review, merge, or closure state.

1. For an exact request naming an existing label, validate the target label and current labels with the helper. Apply directly when the request authorizes the mutation; use a dry run only when the user asks for a plan or the update is ambiguous.
2. For inferred, impact-sensitive, multi-label, or exclusive-family updates, establish policy from the user's instruction, repository docs/automation/descriptions, and consistent maintainer use. Read `references/label-policy.md` for classification or exclusive families.
3. Inspect deterministically when current or repository labels are needed:

```bash
python <skill>/scripts/pr_label.py inspect <PR> --repo <OWNER/REPO> --format markdown
```

4. For inferred labels, state the repository rule and current PR evidence. Classify the result as confirmed, provisional, contradicted, or mechanical cleanup. For an exact user directive, record any conflict without blocking the requested label change.
5. For bug, security, severity, or priority classification, require a supported entrypoint/actor, repository-owned path, concrete present consequence, and policy mapping. Reuse an evidence-backed triage/review when available.

```bash
python <skill>/scripts/pr_label.py update <PR> --repo <OWNER/REPO> --add <label> --apply --format markdown
```

Use `--exclusive-prefix` for a documented exclusive family and explicit `--remove` for known conflicts. Omit `--apply` when the user requested a plan or the classification is unresolved; otherwise review the verified after-state.

6. With mutation authority, use `--apply`. The helper writes through the REST API, rereads labels, and verifies targets, removals, exclusivity, and preservation of unrelated labels.
7. Reply with labels before/after, plan/no-op/applied state, and classification evidence only when classification was part of the request.

Treat explicit but weakly evidenced label requests as directives rather than confirmed classifications.
