# Label Policy

Read this reference when the requested label is not already explicit or when labels may be mutually exclusive.

## Evidence hierarchy

A label name is not a policy. Establish meaning and eligibility from:

1. the user's explicit requested classification;
2. repository-local instructions or contribution documentation;
3. labeler workflows/configuration and repository label descriptions;
4. recent, consistent maintainer usage on comparable PRs.

Treat conventions inferred only from historical usage as provisional. A few examples can reflect mistakes or a policy transition.

## Separate dimensions

Repositories often encode different dimensions:

- change type;
- affected area/component;
- priority or severity;
- workflow/status;
- release or backport intent;
- contributor or governance state.

Do not replace labels across different dimensions. Area labels are often additive; priority or workflow labels are often exclusive, but only repository evidence can establish that.

## Exclusive families

Use `--exclusive-prefix` only when all of these are true:

- the repository defines the matching labels as one family;
- exactly one proposed target matches the prefix;
- every current matching label conflicts with that target;
- no unrelated label shares the prefix.

Otherwise pass exact `--remove` values. Never use a broad prefix such as `status` when it may match unrelated labels.

Examples are mechanical, not universal policy:

```bash
# Repository documents priority:* as exclusive.
python3 scripts/pr_label.py update 42 --repo owner/repo \
  --add "priority: high" --exclusive-prefix "priority:"

# Repository allows multiple component labels.
python3 scripts/pr_label.py update 42 --repo owner/repo \
  --add "area: api" --add "area: cli"

# Family has no safe shared prefix; remove the exact conflict.
python3 scripts/pr_label.py update 42 --repo owner/repo \
  --add "P1" --remove "P2"
```

## Classification standard

For each substantive label, record:

- the relevant PR fact;
- the repository rule or precedent;
- why nearby alternatives do not apply;
- any remaining uncertainty.

Do not translate review uncertainty into a high-severity label. If a finding is not yet confirmed, label it only when the repository explicitly has a workflow label for that uncertainty.

## Missing labels

The helper deliberately refuses to add a label absent from the repository taxonomy. Creating a repository label changes shared project policy and requires an explicit name, meaning, color, description, and authorization. Handle that as a separate task before labeling the PR.
