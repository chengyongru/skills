# Label Policy

Read this reference when the requested label is not already explicit or when labels may be mutually exclusive.

## Evidence hierarchy

A label name is not a policy, and a mutation instruction is not factual evidence. Establish meaning and eligibility from:

1. an explicit user-provided or repository-local policy definition;
2. contribution documentation;
3. labeler workflows/configuration and repository label descriptions;
4. recent, consistent maintainer usage on comparable PRs;
5. current PR evidence that satisfies the discovered rule.

Treat conventions inferred only from historical usage as provisional. A few examples can reflect mistakes or a policy transition.

An exact user request controls authorization and requested outcome. If it conflicts with the evidence, follow the authorized instruction but describe it as a directive, not a confirmed classification.

## Reachability and impact evidence

Impact-bearing labels must describe current repository behavior, not the theme of a diff.

- **Bug/fix**: require a supported path whose current behavior violates an existing contract. Odd behavior in an unreachable helper is not a product bug.
- **Security**: require a current trust boundary, reachable actor or capability, and concrete consequence. Permission-related code or generic hardening is insufficient unless repository policy explicitly includes hardening.
- **Severity/priority**: require present-day user, operator, data, security, or maintenance impact at the level defined by the repository. A theoretically serious consequence on an impossible path has no current severity.
- **Area/component/test**: may follow changed ownership or file content when repository policy defines them that way; they do not prove impact.

Trace `supported entrypoint/actor → repository-owned caller → affected boundary → consequence`. A direct internal-helper call, synthetic state, speculative future consumer, arbitrary in-process plugin, PR-body assertion, or existing label does not complete that trace.

A documented public API, package, or supported extension contract can establish reachability when consumers live elsewhere. Mere importability cannot.

If repository design explicitly forbids the claimed state or no supported consumer can reach it, treat corresponding bug, security, severity, and priority labels as contradicted. Remove them only when the requested mutation scope authorizes synchronization or reclassification.

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
- the supported path and concrete consequence for impact-bearing labels;
- why nearby alternatives do not apply;
- any remaining uncertainty.

Do not translate review uncertainty into a bug, security, severity, or priority label. If a finding is not yet confirmed, label it only when the repository explicitly has a workflow label for that uncertainty.

## Missing labels

The helper deliberately refuses to add a label absent from the repository taxonomy. Creating a repository label changes shared project policy and requires an explicit name, meaning, color, description, and authorization. Handle that as a separate task before labeling the PR.
