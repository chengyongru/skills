# Workflow help and authoring

A help or audit question remains read-only. Configure or change an artifact only when that operation was requested; use the host's installed skill-authoring guidance where available.

| Request | Workflow or playbook |
|---|---|
| Explain this plugin or suggest a task prompt (`help`) | [Help](../workflows/authoring/help/workflow.md) |
| Inspect capabilities or change workflow preferences (`settings`, `setup-pstack`) | [Settings](../workflows/authoring/settings/workflow.md) |
| Create or update a skill | [Skill authoring](../playbooks/authoring/authoring-a-skill.md) |
| Create a missing verification skill | [Create a verifier](../workflows/authoring/create-verifier/workflow.md) |
| Audit an existing verifier and its feature map | [Maintain a verifier](../workflows/authoring/maintain-verifier/workflow.md) |
| Draft an authorized personal workflow (`automate-me`) | [Personalize](../workflows/authoring/personalize/workflow.md) |
| Propose improvements from this conversation (`reflect`) | [Reflect](../workflows/authoring/reflect/workflow.md) |
| Enforce a recurring correction in types, checks, or tests (`correct`) | [Correct](../workflows/authoring/correct/workflow.md) |
| Compare skill or prompt behavior in a scoped evaluation | [Eval](../playbooks/authoring/eval.md) |

Do not infer reflection, preference mining, scheduling, or plugin edits from completing an unrelated task. The installed package is immutable: prepare an expressly requested package change in its source checkout or task-owned staging, review the final artifact, and re-enable after installation. Do not write runtime state, bytecode, generated skills, or logs into the installed package. Protected profiles and memory remain outside these workflows.
