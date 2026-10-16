# Automate me

Turn the user's working conventions into one short `-mode` skill, such as `jay-mode` or `priya-mode`. Use installed `skill-creator` for authoring and `$workflow unslop` for prose. For repository-facing prose, also follow installed [repo-prose](../../writing/prose/workflow.md). Do not assume an authoring tool beyond the capabilities actually available.

## 0. Check for an existing skill

Resolve the active agent workspace, not the current project directory. Look under `<agent-workspace>/skills/` for a standalone `<handle>-mode/SKILL.md`. If one exists and the user has not already requested an update, ask in ordinary chat whether to update it or start fresh. Preserve sections the user has not contradicted.

A packaged skill is a read-only input. Propose a patch outside the package unless the user expressly requested a plugin change; such a change requires review and re-enabling after the package is final. Do not modify `SOUL.md`, `USER.md`, `memory/MEMORY.md`, or the history journal. Those belong to Dream consolidation, not this workflow.

For an update, use available edit/version metadata to bound new evidence. Do not assume the skill is Git-tracked. If the cutoff is unknown, state a bounded time range rather than inventing one.

## 1. Mine scoped history

Use the visible conversation for the current task. For prior conversations, state a topic, workspace, and time window, normally the last two weeks unless the user chose another range. Use bounded `search_sessions` queries, then `read_session` on exact returned references. Do not scan raw transcript files, session databases, unrelated workspaces, or memory journals.

For enough matching sessions to justify delegation, split the bounded result set into non-overlapping slices. Create native child tasks within the concurrency limit, normally two at once. Each child receives the authorized session references or relevant excerpts, the scope, and a read-only contract. It returns a short list of patterns with exact `session_ref` evidence. For a few sessions, read directly instead.

Look for:

- Response preferences: length, tone, format, and corrections.
- Delegation habits: when to delegate, how much parallelism, and required checks.
- Verification posture: what done means and which installed verifiers the user relies on.
- Code and prose discipline: local conventions, real lint commands, and principles.
- Process boundaries: worktrees, commits, reviews, remote updates, and approvals.
- Skill-authoring habits: which recurring workflows merit a skill.

Cross-check across sessions before elevating a signal. Repeated evidence is stronger than a lone remark, but explicit current preferences override old patterns. If history tools are unavailable or incomplete, use visible evidence and ask targeted questions; label the draft's evidence limits.

## 2. Ask the user directly

Mining misses intent. Ask one or two concise questions in ordinary chat, with four to six choices when useful. Allow multiple selections by saying so, not by inventing a question-tool flag. Start with the areas that matter most, then ask what changed or is missing. End with one free-form opportunity to add a convention. Do not dump twenty questions.

## 3. Cluster findings

Use only sections supported by specific preferences:

- Response style.
- Autonomy and permission boundaries.
- Grounding and investigation.
- Delegation and artifact checking.
- Code and prose discipline.
- Review and verification.
- Process and skill authoring.

The [poteto-mode](../../../SKILL.md) skill illustrates operational granularity, not the user's rules. Do not copy its content or add model-selection settings that the runtime cannot honor. A personal skill cannot override native routing, repository restrictions, or the user's actual authorization.

## 4. Draft the skill

Use installed `skill-creator` when available. Show a draft before applying it unless the user already authorized writing this standalone skill.

- New path: `<agent-workspace>/skills/<handle>-mode/SKILL.md`.
- Name: exactly the directory's kebab-case name.
- Description: one YAML scalar, at most 1024 characters, triggering on the chosen name, `$<handle>-mode`, or an explicit request to work in that style. Do not trigger on every generic code/review request.
- Instructions: short, specific, decision-changing rules. Reference installed skills by name instead of copying them. Preserve the actual configured model and native permission boundaries.

Use an existing authorized standalone skill's path for an update. Package-edit proposals remain external artifacts until the user expressly requests that plugin change. Do not add always-on behavior, root configuration, or profile persistence as a side effect.

## 5. Iterate and deliver

Apply `$workflow unslop`, the installed authoring guidance, and [repo-prose](../../writing/prose/workflow.md) where relevant. Take user feedback and cut anything that would not change a future decision. Validate name, frontmatter, references, and trigger examples using an available validator or transparent static checks.

This is subjective output. Ask whether it reflects the user's conventions rather than inventing a benchmark or description-optimization API. If triggering later proves inaccurate, propose a focused revision.

Deliver the draft, an authorized standalone edit, or a package patch proposal with its path and evidence limits. Do not commit, push, open a PR, publish a message, or schedule follow-up work automatically.

## Guardrails

- Require repeated evidence for inferred habits; do not overfit one conversation.
- Keep only non-default, actionable preferences. "Communicate clearly" does not merit a section.
- Refer to other skills and principles rather than restating them.
- Use "the user" in imperatives, not the author's first name.
- Skip sections without real content; a personal skill is not a manual.
- For a narrow task workflow rather than working conventions, use installed `skill-creator` directly with the user's authorization.
