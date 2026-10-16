# Verify

Select proof for the changed public contract. Existing project-specific verifiers take precedence; principles are guidance, not a replacement for an executable verification path.

| Surface or question | Workflow |
|---|---|
| Nanobot browser-visible WebUI, gateway, routing, settings, or persistence | [Nanobot WebUI verification](../workflows/verify/webui/workflow.md) |
| Another CLI, API, package consumer, service, terminal, or process lifecycle | [Public-surface verification](../workflows/verify/public/workflow.md) |
| Whether a measured speedup or regression is credible | [Benchmark checklist](../workflows/verify/benchmark/workflow.md) |
| What this diff can break outside its immediate files | [Blast radius](../workflows/code/blast-radius/workflow.md) |
| A missing reusable verifier, with authoring authorization | [Create a verifier](../workflows/authoring/create-verifier/workflow.md) |
| Audit or maintain an existing verifier | [Maintain a verifier](../workflows/authoring/maintain-verifier/workflow.md) |

The public-surface workflow retains real WezTerm and real-process-lifecycle recipes. A build or unit pass does not prove an unexercised browser, terminal, or subprocess claim. Scope the live checks and task-owned resources before starting; keep evidence outside the installed plugin, clean up only owned resources, and disclose missing proof.

Read [prove it works](../principles/prove-it-works.md) when the observation itself is disputed. Do not infer an explicit gate request from ordinary verification.
