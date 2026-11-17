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

- Work in the main agent by default. Delegate only when independent work can run in parallel and the benefit justifies extra token and coordination costs; do not repeat a child's assignment. Each worker reads the same bounded worker contract.
- `how` explains the code in one pass, `why` follows recorded decision history, and `reflect` proposes durable skill improvements without reviewer agents. `architect` compares two sketches directly and uses `arena` for large or contested designs. Large, cross-cutting, or unattended tasks use `figure-it-out` to design a scoped workflow first.
- For formal development or repair, available Linear tools are used to associate an existing Issue or create one when no matching task exists. Updates focus on confirmed scope, key decisions, blockers, and delivery. Without a Linear integration, these steps are skipped; no setup is required. Discussion and read-only requests do not start tracking.
- For a known Linear task, use `Resolves` for the PR intended to complete the Issue, even while review or CI is pending; use `Contributes to` for partial delivery and `Related to` for context only. Include clickable Issue links in the PR body and verify the effective relationship. Automatic merge transitions depend on the repository integration and team workflow.
- Technical explanations focus on behavior and end-to-end correctness, using Mermaid when relationships are clearer as a diagram. A PR introduction starts with the scenario, failure, and consequence without the change; implementation review is a separate request.
- `$workflow sharpen <task>` returns a rewritten prompt that asks for experiments to settle empirical choices, without executing the task or granting extra authority. Product and preference choices stay with you. `$workflow ketchup` gives a concise update while listing every item awaiting your decision, with the context needed to decide.

For example:

```text
$workflow Explain what user problem this PR solves and what happens without it. Read-only; do not review or post comments.
$workflow Explain the cause of this bug and propose a fix; do not edit files yet.
$workflow sharpen Compare the startup time of these two implementations; do not change product code.
```

## Formal verification

- `$workflow statechart <question>` checks a bounded TLA+ model with TLC and explains failures as action paths and Mermaid charts.
- `$workflow create-formal-verification-skill <area>` creates an authorized reusable project check, with properties, source mappings, assumptions, bounds, and a demonstrated failing variant.
- `$workflow maintain-formal-verification-skill <check>` reconciles that verification with changed code and distinguishes stale models from product bugs.

These routes load on demand; ordinary changes do not require model checking. A model result covers its stated assumptions and bounds, not arbitrary implementation behavior. Counterexamples must be reconciled with the real code, and required project tests remain in force.

Statechart uses Node, Python, Java, and a pinned TLC JAR. Its portable launcher supports Windows and POSIX process ownership, timeouts, and cancellation. Dependencies and run artifacts stay outside the plugin; nothing is installed automatically. See [Statechart](skills/workflow/workflows/verify/statechart/workflow.md) and [tool setup](skills/workflow/workflows/verify/statechart/references/tools.md). Image rendering is optional.
