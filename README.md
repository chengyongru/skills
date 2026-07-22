Agent skills
============

English | [简体中文](README.zh-CN.md)

This repository contains reusable workflows for AI agents.  Each top-level
directory is an independently installable skill with a `SKILL.md` file and,
where needed, scripts or reference material.

The skills follow the open [Agent Skills](https://agentskills.io/) convention.
Most of them are not tied to a particular agent runtime.  Files below an
`agents/` directory provide optional runtime-specific presentation metadata;
they do not define the workflow itself.

Selecting skills
----------------

Do not install every skill in this repository.

Install the smallest set needed for the work at hand.  Add another skill only
when the current workflow has a real hand-off to it.  This keeps trigger scopes
clear, avoids unnecessary tool dependencies, and makes it less likely that a
special-purpose workflow is selected in the wrong context.

Useful starting sets are:

* Idea management: `idea-capture` and `idea-next`.
* Publishing: `material` and `draft`; add `rewrite` for Chinese editing.
* PR review: `pr-worktree` and `pr-review`; add `triage` when the purpose is
  unclear.
* PR repair: `pr-worktree` and `pr-fix`; add `verify` when a separate black-box
  evidence report is needed.
* Code cleanup: `simplify`, followed by `verify` when user-facing proof matters.
* Experiment planning: choose `autoresearch` or `abtest`; usually not both.

Workflows and relationships
---------------------------

Planning and experiments:

* [`grill-me`](grill-me/SKILL.md) examines a plan one question at a time.  It
  may be used before either experiment-planning skill when the goal or
  hypothesis is still unclear.
* [`autoresearch`](autoresearch/SKILL.md) prepares one isolated worktree and an
  auditable plan for improving a measurable target.
* [`abtest`](abtest/SKILL.md) prepares separate control and treatment worktrees
  for a controlled comparison.

`autoresearch` and `abtest` stop after planning.  They do not run the
experiment.

Ideas and publishing:

* [`idea-capture`](idea-capture/SKILL.md) stores actionable work and maintains
  its status.
* [`idea-next`](idea-next/SKILL.md) reads that store and selects one concrete
  next action.
* [`material`](material/SKILL.md) stores verified facts, observations, and
  experience fragments that may be worth sharing.
* [`draft`](draft/SKILL.md) turns a material frame or raw input into publishable
  copy for a specific platform.
* [`rewrite`](rewrite/SKILL.md) selectively edits existing Chinese technical
  writing while preserving facts, authorship, and voice.

The idea and material stores are deliberately separate.  `idea-capture` records
what to do; `material` records what may be worth publishing.  A normal content
hand-off is `material` to `draft`, with `rewrite` as an optional final pass.

Pull request maintenance:

* [`pr-worktree`](pr-worktree/SKILL.md) creates and checks an isolated PR
  worktree.  It is the local foundation for PR-mode `triage`, `pr-review`, and
  `pr-fix`.
* [`triage`](triage/SKILL.md) produces a short decision brief for a PR, issue,
  article, document, or unfamiliar topic.
* [`pr-review`](pr-review/SKILL.md) performs a maintainer-oriented correctness
  and merge-value review.
* [`pr-fix`](pr-fix/SKILL.md) makes a focused change on an existing PR branch
  and pushes it when the user has explicitly authorized that operation.
* [`pr-label`](pr-label/SKILL.md) inspects or changes PR labels according to the
  repository's policy.  Label changes require separate authorization.

For a PR, the longest hand-off is normally:

    pr-worktree -> triage -> pr-review -> pr-fix -> verify

Not every step is required.  A clear fix request may go directly through
`pr-worktree` and `pr-fix`.  A review does not authorize a fix, a push, a label
change, or a GitHub comment.

Cleanup and verification:

* [`simplify`](simplify/SKILL.md) performs behavior-preserving cleanup of recent
  or explicitly selected code.  It does not search for correctness bugs.
* [`verify`](verify/SKILL.md) checks completed changes through public
  interfaces such as an API, CLI, Web UI, or package consumer and reports
  concrete evidence.
* [`nanobot-webui-verify`](nanobot-webui-verify/SKILL.md) is the specialist
  verifier for nanobot WebUI changes through the real gateway and Playwright.

Use `nanobot-webui-verify` for that specific WebUI.  Use `verify` elsewhere.

Hand-off rules
--------------

* Keep one owner for each stage of a workflow.
* Pass a concrete artifact: a material frame, a worktree manifest, a confirmed
  review finding, or an experiment plan.
* Treat a hand-off as context, not permission for an external mutation.
* Keep optional specialists optional.  Install or invoke them only inside their
  stated scope.
* Do not convert a planning workflow into execution without a separate request.

Installation
------------

Clone the repository somewhere convenient:

    git clone https://github.com/chengyongru/skills.git ~/src/agent-skills

Then copy or link only the selected top-level directories into the skill
discovery directory used by your agent.

For example, Codex discovers user-level skills in `$HOME/.agents/skills` and
repository-level skills in `<repo>/.agents/skills`.  The following installs only
the PR review set:

    mkdir -p ~/.agents/skills
    ln -s ~/src/agent-skills/pr-worktree ~/.agents/skills/pr-worktree
    ln -s ~/src/agent-skills/pr-review ~/.agents/skills/pr-review

Other agents may use different discovery paths.  Follow the documentation for
that runtime.  Codex users can refer to
[Build skills](https://learn.chatgpt.com/docs/build-skills).

Invocation
----------

Invocation syntax is runtime-specific.  Agents that support explicit skill
mentions commonly accept requests such as:

    Use $idea-capture to save this as an actionable idea.
    Use $draft to turn the ready material frame into an HN post.
    Use $pr-review to review PR #123; do not post anything to GitHub.

Natural-language requests may also select a skill by its description.  Prefer
an explicit skill name when installed skills have adjacent scopes.

Repository layout
-----------------

    <skill-name>/
        SKILL.md       Required workflow and trigger description
        agents/        Optional runtime-specific presentation metadata
        references/    Optional guidance loaded when relevant
        scripts/       Optional deterministic helpers

Some skills require Git, Python, PowerShell, GitHub CLI, Playwright, or another
local tool.  Read the selected `SKILL.md` before installing its dependencies.

Contributing
------------

* Give each skill one clear responsibility and explicit trigger boundaries.
* State what the skill accepts and what artifact it hands off.
* Separate read-only analysis from edits, pushes, labels, comments, and other
  external mutations.
* Put deterministic mechanics in `scripts/` and optional background material in
  `references/`.
* Update both README files when adding a skill or changing a collaboration
  boundary.
