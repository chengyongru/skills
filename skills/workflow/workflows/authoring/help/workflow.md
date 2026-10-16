# Workflow help

Answer the user's question without starting setup or implementation. Read only the installed document that owns the answer; provide one relevant example prompt rather than loading every domain.

- For installation, updates, compatibility, and licensing, use the repository [README](../../../../../README.md).
- For supported tools, authorization, models, and lifecycle limits, use the [runtime contract](../../../references/runtime.md).
- For preferences use [settings](../settings/workflow.md); absent settings mean defaults, not a broken configuration.
- For choosing work, use the short [primary router](../../../SKILL.md), then only the selected domain.

The package has two native entries: `$workflow <task or method>` and the separate literal-only `$nanobot-gate`. Old `$how`, `$pr-review`, `$poteto-mode`, and other flat skill names are no longer host registrations; express the intent after `$workflow` instead.

Examples:

```text
$workflow how does request cancellation propagate? Read-only; cite the current callers.
$workflow review PR 123. Do not edit files or publish a review.
$workflow simplify the current diff without changing behavior. Do not commit or push.
```

For a recovery question, reconcile the known checkpoint with actual Git/process state. Private child IDs are not durable sessions, fresh views are not different models, and a green build is not full behavioral acceptance. Explain a real limitation instead of inventing a command or starting an unrelated repair.

Use the [prompt examples](references/recipes.md) or [prompting guidance](references/prompting.md) only if the user needs wording. Installation and help do not activate an always-on mode or autonomous work.
