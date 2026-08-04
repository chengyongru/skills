Agent skills
============

English | [简体中文](README.zh-CN.md)

Reusable [Agent Skills](https://agentskills.io/) for focused workflows. Each top-level directory is independently installable.

Choose the smallest set that covers the task. Project-specific skills take precedence over generic ones when both match.

Skill index
-----------

| Skill | Purpose |
|---|---|
| [`grill-me`](grill-me/SKILL.md) | Stress-test a plan one decision at a time. |
| [`idea-capture`](idea-capture/SKILL.md) | Save and maintain actionable ideas. |
| [`idea-next`](idea-next/SKILL.md) | Pick one evidence-based next action. |
| [`material`](material/SKILL.md) | Capture verified fragments worth sharing. |
| [`draft`](draft/SKILL.md) | Turn fragments or raw input into publishable copy. |
| [`rewrite`](rewrite/SKILL.md) | Polish Chinese technical writing while preserving facts and voice. |
| [`autoresearch`](autoresearch/SKILL.md) | Prepare one measurable improvement experiment. |
| [`abtest`](abtest/SKILL.md) | Prepare isolated control/treatment experiments. |
| [`simplify`](simplify/SKILL.md) | Apply behavior-preserving cleanup. |
| [`verify`](verify/SKILL.md) | Verify public behavior with black-box evidence. |
| [`nanobot-webui-verify`](nanobot-webui-verify/SKILL.md) | Verify nanobot WebUI through the real gateway and browser. |
| [`nanobot-gate`](nanobot-gate/SKILL.md) | Coordinate nanobot simplify, verification, review, and CI gates. |
| [`triage`](triage/SKILL.md) | Produce a short decision brief for complex artifacts. |
| [`pr-worktree`](pr-worktree/SKILL.md) | Prepare isolated worktrees for PR workflows. |
| [`pr-review`](pr-review/SKILL.md) | Review PR correctness, reachability, and merge value. |
| [`pr-fix`](pr-fix/SKILL.md) | Apply an authorized focused fix to a PR branch. |
| [`pr-rebase`](pr-rebase/SKILL.md) | Rebase and verify a PR branch safely. |
| [`pr-label`](pr-label/SKILL.md) | Classify and update PR labels from repository evidence. |

Routing
-------

- Content: `material -> draft -> rewrite`.
- PR work: start with `pr-worktree`; add `triage`, `pr-review`, `pr-fix`, `pr-rebase`, or `pr-label` for the requested operation.
- Verification: use generic `verify` across projects, `nanobot-webui-verify` for nanobot browser/gateway surfaces, and `nanobot-gate` for full nanobot readiness.
- Experiments: choose `autoresearch` for iterative improvement or `abtest` for control/treatment comparison.
- Human-readable plans and results stay in the conversation; skills persist deterministic state and raw evidence when useful.

External mutations such as pushes, PR comments, labels, merges, and remote writes begin from explicit authorization for that operation.

Installation
------------

Clone the repository, then copy or link selected skill directories into the discovery path used by your agent:

    git clone https://github.com/chengyongru/skills.git ~/src/agent-skills
    mkdir -p ~/.agents/skills
    ln -s ~/src/agent-skills/pr-worktree ~/.agents/skills/pr-worktree
    ln -s ~/src/agent-skills/pr-review ~/.agents/skills/pr-review

Agent runtimes may use different discovery paths. Codex users can refer to [Build skills](https://learn.chatgpt.com/docs/build-skills).

Invocation
----------

Explicit mentions are the clearest option when installed skills have adjacent scopes:

    Use $idea-capture to save this idea.
    Use $nanobot-gate to check this change before PR creation.
    Use $pr-review to perform a read-only review of PR #123.

Contributing
------------

- Give each skill one responsibility and precise trigger boundaries.
- Keep `SKILL.md` limited to non-obvious decisions, contracts, and helper usage.
- Put deterministic mechanics in `scripts/` and genuinely optional domain knowledge in `references/`.
- Follow [`AGENTS.md`](AGENTS.md) for action-oriented language and direct verification output.
- Update both README files when skills or routing change.
