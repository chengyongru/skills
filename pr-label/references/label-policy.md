# PR label policy

Establish label meaning from user/repository policy, contribution docs, automation/config, label descriptions, consistent maintainer use, and current PR evidence—in that order.

An exact user request controls the authorized mutation. Describe evidence conflicts as a directive rather than a confirmed classification.

For an exact request naming an existing label, validate taxonomy and final state without requiring a supported-path value analysis. Use the supported entrypoint/actor trace when inferring an impact label or when the user asks whether a label is justified.

## Impact labels

Trace `supported entrypoint/actor -> repository caller -> boundary -> consequence`.

- bug/fix: current supported behavior violates a contract;
- security: current trust boundary, reachable actor/capability, and concrete consequence;
- severity/priority: present user, operator, data, security, or maintenance impact matching repository definitions;
- area/component/test: ownership or file scope when repository policy defines it.

A documented public API or extension contract can establish external reachability. Internal-helper tests, synthetic states, author claims, existing labels, and hypothetical consumers remain supporting context.

## Dimensions and exclusivity

Keep change type, area, priority/severity, workflow, release/backport, and governance dimensions separate.

Use `--exclusive-prefix` when the repository defines one exclusive family, one target matches, every current match conflicts, and the prefix contains no unrelated labels. Otherwise use exact `--remove` values.

For each inferred substantive label, record the PR fact, repository rule/precedent, supported path/consequence for impact labels, nearby alternatives, and uncertainty. Exact directives need only the target, authorization, and final-state evidence.

The helper accepts labels already present in the repository taxonomy. Treat new repository labels as a separate policy task specifying name, meaning, color, description, and authorization.
