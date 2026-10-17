# Nanobot Workflows: maintainer guide

[English](MAINTAINING.md) | [简体中文](MAINTAINING.zh-CN.md)

For maintainers. For installation and first use, see the [README](README.md).

## Migrate older installs

Users without an older install can skip this section.

- Replace legacy calls such as `$pr-review`, `$verify`, `$how`, and `$poteto-mode` with `$workflow <task or method>`. Keep `$nanobot-gate` as an explicit-only entry point.
- Confirm the path and ownership of old standalone skills before moving them out of discovery paths; preserve local changes. Workspace skills take precedence over plugins, and leftover copies add entries to the skill summary.
- Disable the old `pstack` plugin before replacing it. Enabling both leaves the old plugin's 54 descriptions in place.
- Do not delete a source directory just because a skill was linked from it. Confirm the link, installed copy, and ownership first.
- Workflow preferences live in `<agent-workspace>/.nanobot-workflows/`. `.pstack/` state is neither migrated nor removed automatically; migrate only explicitly selected, supported preference fields.

## Project adaptation and on-demand loading

Read the target repository's `AGENTS.md`, contribution guide, project configuration, scripts, and CI first. Use its commands and acceptance criteria. Prefer existing project verifiers; design a verification approach with public interfaces only when needed.

Project-specific procedures live in the [project adapter layer](skills/workflow/references/project.md). The included [HKUDS/nanobot adapter](skills/workflow/projects/nanobot/workflow.md) applies to that repository and its forks; use each other project's own engineering configuration.

Only `skills/workflow/SKILL.md` and the explicit `skills/nanobot-gate/SKILL.md` are discoverable entries. The main entry routes on demand to `routes/`, `workflows/`, `projects/`, `playbooks/`, `principles/`, `references/`, and helper scripts; these internal documents are not standalone skills.

Run the shared helper from its installed path with `-B` to avoid writing bytecode:

```text
python -B "<plugin-root>/skills/workflow/scripts/workflow.py" paths
```

`paths` prints external settings and task directories without writing state. `log` appends sanitized TSV rows to an external log. `worktrees --repo <repo>` reads registered worktrees without fetching or deleting them. GitHub, browser, PowerShell, and Herdr workflows have prerequisites; see the relevant workflow and [runtime contract](skills/workflow/references/runtime.md).

## Verify changes

Use Python 3.11+ and Git in a separate source workspace:

```text
python -B -m unittest discover -s tests -v
python -B -m unittest discover -s skills/workflow/workflows/pr/worktree/tests -v
python -B -m unittest discover -s skills/workflow/workflows/environment/worktree-right/scripts -p "test_*.py" -v
```

When a compatible nanobot installation is available, package tests run the native loader test; otherwise they explicitly skip it. Native integration checks should use the target nanobot's environment.

## License and provenance

- Original skills and integration: Copyright (c) 2026 chengyongru, MIT.
- pstack-derived content: Copyright (c) 2026 Lauren Tan, MIT; upstream `cursor/plugins/pstack` v0.15.25, pinned to commit `99743e9c151c8537cbbf1f98bb38f34ef3368453`.
- Full details: [LICENSE](LICENSE), [upstream MIT notice](LICENSES/pstack-MIT.txt), [third-party notices](THIRD_PARTY_NOTICES.md), and [provenance](provenance.json).
