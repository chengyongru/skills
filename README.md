# Nanobot Workflows

English | [简体中文](README.zh-CN.md)

An engineering workflow plugin for nanobot. Use [`$workflow`](skills/workflow/SKILL.md) for common software-project tasks.

## Install and enable

Your nanobot must support **Agent Plugins v1** and `$skill-name` invocation. Open a conversation with the nanobot instance where you want the plugin and send it the full prompt below:

```text
Install the nanobot-workflows Agent Plugin from https://github.com/chengyongru/skills into this nanobot instance.

1. First confirm the target instance, config path, agent workspace, and support for Agent Plugins v1 and $skill-name invocation. If the target is ambiguous or there are multiple instances, ask me to choose. If unsupported, stop without changing files.
2. Clone the repository into a temporary directory outside the plugin discovery directory and record the exact commit SHA. Review README.md, plugin.json, LICENSE, THIRD_PARTY_NOTICES.md, provenance.json, and helpers that may be invoked. Do not run repository installation scripts.
3. Check for an existing nanobot-workflows install, an older pstack plugin, or standalone skills from this repository. Do not overwrite existing installs, source workspaces, or local changes. If anything must be moved, disabled, or backed up, report its path and impact and ask me first. If the current account cannot write to the target directory, stop and explain what an administrator needs to do.
4. After review, copy only plugin.json, skills/, LICENSE, LICENSES/, THIRD_PARTY_NOTICES.md, provenance.json, third_party/, README.md, README.zh-CN.md, MAINTAINING.md, and MAINTAINING.zh-CN.md to <agent-workspace>/plugins/nanobot-workflows/. Preserve the instance config, credentials, models, profile, and memory.
5. Verify that the plugin provides workflow, then report the install path, commit SHA, detected conflicts, and enabled state. Do not enable the plugin for me; keep the current gateway running.
```

After installation, open **Apps** in the WebUI, change the filter from **Ready** to **Apps**, find **Nanobot Workflows**, review it, and enable it. If the list is stale, refresh the Apps page. If the plugin is still missing, do not reinstall; ask an administrator whether this instance supports Agent Plugins. Start a new conversation and try:

```text
$workflow Briefly explain what you can help me with. Do not modify any files.
```

## Use

Describe the task in the nanobot conversation. When scopes overlap, use `$workflow` to select the entry point explicitly.

- For formal development or repair, available Linear tools are used to associate an existing Issue or create one when no matching task exists. Updates focus on confirmed scope, key decisions, blockers, and delivery. Without a Linear integration, these steps are skipped; no setup is required. Discussion and read-only requests do not start tracking.
- When delivering a PR for a known Linear task, distinguish `Resolves` (complete delivery), `Contributes to` (partial progress), and `Related to` (context only). Verify the effective link; automatic merge transitions depend on the repository integration and team workflow.
- Technical explanations focus on behavior and end-to-end correctness, using Mermaid when relationships are clearer as a diagram. A PR introduction starts with the scenario, failure, and consequence without the change; implementation review is a separate request.

For example:

```text
$workflow Explain what user problem this PR solves and what happens without it. Read-only; do not review or post comments.
$workflow Explain the cause of this bug and propose a fix; do not edit files yet.
```
