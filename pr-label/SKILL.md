---
name: pr-label
description: Inspect, classify, add, remove, replace, synchronize, or verify GitHub PR labels. Use repository evidence for impact classifications, preserve unrelated labels, plan before applying, and use the bundled REST helper for authorized mutations.
---

# PR Label

Separate classification evidence from mutation authority. Exact requested PR label changes are authorized by the request; repository-level label creation/deletion and other PR state changes require separate authorization.

1. Establish policy from the user's instruction, repository docs/automation/descriptions, and consistent maintainer use. Read `references/label-policy.md` for classification or exclusive families.
2. Inspect deterministically:

```bash
python <skill>/scripts/pr_label.py inspect <PR> --repo <OWNER/REPO> --format markdown
```

3. For each proposed label, state the repository rule and current PR evidence. Classify it as confirmed, provisional, contradicted, or mechanical cleanup.
4. For bug, security, severity, or priority labels, require a supported entrypoint/actor, repository-owned path, concrete present consequence, and policy mapping. Reuse an evidence-backed triage/review when available.
5. Plan the minimal update; dry run is the default:

```bash
python <skill>/scripts/pr_label.py update <PR> --repo <OWNER/REPO> --add <label> --format markdown
```

Use `--exclusive-prefix` for a documented exclusive family and explicit `--remove` for known conflicts. Review before/planned-after state.

6. With mutation authority, repeat with `--apply`. The helper writes through the REST API, rereads labels, and verifies targets, removals, exclusivity, and preservation of unrelated labels.
7. Reply with classification evidence, labels before/after, plan/no-op/applied state, and any ambiguity or verification failure.

Treat explicit but weakly evidenced label requests as directives rather than confirmed classifications.
