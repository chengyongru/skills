# Verify

Select proof for the changed public contract. Existing project-specific verifiers take precedence; principles are guidance, not a replacement for an executable verification path.

| Surface or question | Workflow |
|---|---|
| A project-specific launcher, verifier, or acceptance rule | [Target project and adapters](../references/project.md) |
| CLI, API, browser UI, package consumer, service, terminal, or process lifecycle | [Public-surface verification](../workflows/verify/public/workflow.md) |
| Whether a measured speedup or regression is credible | [Benchmark checklist](../workflows/verify/benchmark/workflow.md) |
| What this diff can break outside its immediate files | [Blast radius](../workflows/code/blast-radius/workflow.md) |
| A missing reusable verifier, with authoring authorization | [Create a verifier](../workflows/authoring/create-verifier/workflow.md) |
| Audit or maintain an existing verifier | [Maintain a verifier](../workflows/authoring/maintain-verifier/workflow.md) |

Use the target project's supported environment and documented commands. Scope live checks and task-owned resources before starting; keep evidence outside the installed plugin and clean up owned resources. The public-surface workflow includes terminal and process-lifecycle checks.

Read [prove it works](../principles/prove-it-works.md) when the observation itself is disputed.
