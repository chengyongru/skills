# Nanobot Workflows

English | [简体中文](README.zh-CN.md)

A nanobot Agent Plugin combining chengyongru's engineering skills with adapted [pstack](https://github.com/cursor/plugins/tree/99743e9c151c8537cbbf1f98bb38f34ef3368453/pstack) workflows. The methods apply across projects; the runtime integration targets nanobot.

Only two skills are discoverable:

| Entry | Purpose |
|---|---|
| [`$workflow`](skills/workflow/SKILL.md) | Route the current task to one domain and load the matching workflow on demand. |
| [`$nanobot-gate`](skills/nanobot-gate/SKILL.md) | Snapshot-bound nanobot readiness workflow, **only when the user literally invokes it**. |

Investigation, code, PR, verification, writing, coordination, authoring, and environment operations live behind the primary router. Their workflows, review methods, principles, and playbooks are files, not separately registered skills. This keeps their descriptions out of nanobot's routine skill summary instead of moving a full catalog into the entry document.

## Install by prompt

Use a nanobot build that supports **Agent Plugins v1** and `$skill-name` invocation. Paste this prompt into that instance:

```text
Install the nanobot-workflows Agent Plugin from https://github.com/chengyongru/skills into my current nanobot instance.

1. Confirm the target instance's configuration path, agent workspace, and Agent Plugins v1 support. Ask me to select the target if it is unclear or several instances are available.
2. Clone the repository into task-owned staging outside the plugin discovery directory, record the exact commit SHA, and review README.md, plugin.json, LICENSE, THIRD_PARTY_NOTICES.md, provenance.json, and the executable helpers. Review without executing the repository's installation scripts.
3. Check for an existing nanobot-workflows package, the older pstack plugin, and standalone skills from this repository. Report conflicts and preserve any local edits. Do not overwrite an existing installation or change my source checkout. If conflicting installations need to be disabled or backed up, show me the specific paths and obtain approval before changing them.
4. After review passes, copy only plugin.json, skills/, LICENSE, LICENSES/, THIRD_PARTY_NOTICES.md, provenance.json, third_party/, README.md, and README.zh-CN.md into <agent-workspace>/plugins/nanobot-workflows/. Preserve my instance configuration, credentials, model, profiles, and memory.
5. Verify that the package exposes workflow and nanobot-gate. Enable the reviewed final snapshot through the supported activation interface. If that interface is unavailable, leave the package disabled and direct me to enable Nanobot Workflows in Apps.
6. Keep the current gateway running and finish with an installation summary: installed path, source SHA, activation state, unresolved conflicts, and one $workflow example.
```

After copying the package, review and enable **Nanobot Workflows** in **Apps**. Refresh the list if needed.

Enabled packages are immutable: changing any packaged file invalidates activation. Develop in a separate source checkout, stage updates outside discovery, review the final content, and re-enable after replacement. Do not `git pull` or run tests inside the enabled package.

## Use it

```text
$workflow triage this PR. Explain the main change, risk, and next action; no local checkout or publication.
$workflow how does request cancellation work? Read-only; show current callers and state ownership.
$workflow fix this reproducible defect locally, then verify the public behavior. Do not commit or push.
$workflow review PR 123 at SHA <sha>. Preserve my dirty worktree and do not publish a review.
$workflow simplify the current diff without changing behavior, then run focused checks.
$workflow revise this README while preserving its commands and compatibility conditions.
$workflow open the current worktree in the right-hand Herdr pane.
```

The short entry description also permits selection for a matching natural-language request. Explicit `$workflow` is the clearest choice when several installed capabilities overlap. Use `$workflow pr-review`, `$workflow how`, or `$workflow architect` to select a specific method.

## Migrate older installations

This repository ships a complete nanobot plugin.

- Replace old invocations such as `$pr-review`, `$verify`, `$how`, and `$poteto-mode` with `$workflow <task or method>`. `$nanobot-gate` remains a separate literal-only entry.
- Review and remove confirmed old standalone installations from the discovery path, preserving backups and local edits. Workspace skills take precedence over plugin skills, and old flat installations continue to add their own summary entries.
- Disable the older `pstack` plugin before using this consolidated package as its replacement. Installing both does not remove the old plugin's 54 descriptions.
- Do not delete a source checkout merely because it was previously linked into a skill directory. Identify each installed link/copy and its ownership first.
- Workflow preferences now use `<agent-workspace>/.nanobot-workflows/`. Existing `.pstack/` state is not migrated or deleted automatically; copy only explicitly chosen, documented preferences if needed.

## Loading and layout

```text
plugin.json
skills/
  workflow/
    SKILL.md                 # small discoverable router
    routes/                  # one index per domain
    workflows/               # concrete workflows and adjacent helpers
    playbooks/               # task sequences, grouped by domain
    principles/              # on-demand decision guidance
    references/              # runtime and worker contracts
    scripts/workflow.py      # paths, decision log, read-only worktree inventory
  nanobot-gate/
    SKILL.md                 # separate explicit-only entry
    scripts/gate_state.py
```

Load the entry, one domain route, and the matching workflow. Read additional methods or domains only when needed. Shared resources stay under a registered skill root so nanobot's approved plugin read paths can reach them.

The shared helper uses Python's standard library. Run it with the actual installed path:

```text
python -B "<plugin-root>/skills/workflow/scripts/workflow.py" paths
```

It locates external settings and task state without creating them. `log` appends a sanitized TSV row outside the package; `worktrees --repo <repo>` inventories local registered worktrees without fetching or deleting. Concrete GitHub, browser, PowerShell, or Herdr workflows have their own prerequisites; see the selected workflow and [runtime contract](skills/workflow/references/runtime.md).

## Verify changes

From a separate source checkout, with Python 3.11+ and Git:

```text
python -B -m unittest discover -s tests -v
python -B -m unittest discover -s skills/workflow/workflows/pr/worktree/tests -v
python -B -m unittest discover -s skills/workflow/workflows/environment/worktree-right/scripts -p "test_*.py" -v
```

Package tests cover route/resource links, the public entry boundary, preserved source contracts, and real shared-helper commands. Native-loader tests run when the Python environment contains a compatible nanobot installation; otherwise they are explicitly skipped. Use the same environment as the target nanobot build for that integration check.

## License and attribution

- Original skills and integration: **Copyright (c) 2026 chengyongru**, MIT.
- pstack-derived content: **Copyright (c) 2026 Lauren Tan**, MIT. Upstream pstack **v0.15.25**, commit `99743e9c151c8537cbbf1f98bb38f34ef3368453`, from `cursor/plugins/pstack`.

See [LICENSE](LICENSE), the unchanged [upstream MIT notice](LICENSES/pstack-MIT.txt), [third-party notices](THIRD_PARTY_NOTICES.md), and [provenance](provenance.json) for source and integration details.
