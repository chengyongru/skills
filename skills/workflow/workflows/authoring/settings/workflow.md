# Workflow settings

Inspect actual capabilities and change workflow preferences only when requested. This does not configure nanobot providers, select per-child models, or edit root nanobot configuration.

1. Use available runtime inspection and the actual `subagent` schema. The current child interface inherits the configured model and does not offer per-child model, reasoning, cloud, readonly-sandbox, or resume selectors. Report blocked cross-model requirements honestly.
2. Run `python -B <plugin-root>/skills/workflow/scripts/workflow.py paths` with the actual installed path. Read its external settings location, not a path relative to the current project.
3. If no settings file exists, use these defaults without creating one merely to answer a question:

```json
{
  "schema_version": 1,
  "model_policy": "inherit-parent",
  "max_parallel_workers": 2
}
```

4. For an authorized settings change, preserve only those documented fields. `schema_version` is `1`; `model_policy` is `inherit-parent`; `max_parallel_workers` is a positive integer, not a Boolean. Report malformed or unsupported values without silent replacement or clamping.
5. Write the requested values to `<agent-workspace>/.nanobot-workflows/settings.json`, then read them back. Never store credentials, a full nanobot config, transcripts, private task IDs, or a fixed project path. The planning ceiling does not alter gateway admission, token limits, or provider reasoning.
6. Explain the saved choices and any capability limitation. Future workflow use reads these preferences; they require neither a package change nor gateway restart and do not activate an always-on mode.

Use fewer or no workers when the task, runtime, or user's no-subagent restriction requires it. For proof use a matching project verifier, including [nanobot WebUI](../../verify/webui/workflow.md) or [public verification](../../verify/public/workflow.md), rather than automatically creating a new verifier.
