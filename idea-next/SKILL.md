---
name: idea-next
description: Choose one concrete next action from the user's Markdown idea directory. Use when the user invokes $idea-next or asks what to do next, what to work on now, which idea/PR/project to advance, or how to break choice paralysis using previously captured ideas.
---

# Idea Next

## Idea Store

Resolve the idea directory in this order:

1. Use an explicit directory from the request.
2. If the request names an existing idea `.md` file, use that file as a candidate and its parent as the idea directory.
3. Read `$CODEX_HOME/idea-store.json`, or `~/.codex/idea-store.json` if `CODEX_HOME` is unset.
4. If no durable location is known, ask one setup question for the idea directory. If the current workspace looks like a notes repo (`.obsidian`, `content/idea`, `content/notebook`, or `notebook`), mention that as a suggested location but do not write there without user confirmation.

Config shape:

```json
{ "ideas_dir": "/absolute/path/to/idea" }
```

## Selection Workflow

Read or search the idea directory. Consider only files with `status: open` or `status: doing` unless the user asks otherwise.

Each idea is one Markdown file with a short semantic filename such as `slash-command-streaming.md`. Machine-facing metadata lives in YAML frontmatter; the visible note body is for human-readable meaning. Use the available text-search tool to narrow by exact frontmatter patterns such as `^status: open$`, `^project: nanobot$`, `^impact: high$`, or `^source_id: github-pr-4635$`, then read the likely candidate files.

Match the user's language in the final recommendation. If the user writes in Chinese, answer in Chinese and avoid long English prose except for code names, commands, file paths, API names, and canonical source titles.

Before choosing, check whether candidate entries have enough context to compare. A useful entry has frontmatter `id`, `source_id`, `cost`, `impact`, and `confidence`, plus body sections for current state, evidence, blocker, and next action. If the likely top candidates are missing this, do at most three small source lookups total, then decide.

Treat the idea directory as a durable evidence pool, not a task manager. `status`, `cost`, and `impact` are only selection hints. `related:` frontmatter links are useful when they reveal a cluster or dependency, but they are not a ranking by themselves.

Cost scale:

- `low`: a useful probe fits in one small step
- `medium`: needs one focused work block
- `high`: likely needs half a day or cross-module work

Impact scale:

- `low`: local cleanup or optional polish
- `medium`: meaningful workflow, review, or maintainability improvement
- `high`: user-visible capability, core reliability, data-loss/security risk, or unblocker for other work

Choose one action by loose judgment:

- Impact on the user's current important project or life area
- Whether it unlocks other people, review, mergeability, or later work
- Evidence strength from the source
- Current blocker severity: none, draft/review, failing check, conflict, unknown
- Time to feedback
- Cost and current energy fit
- Cost of delaying one day
- Whether one action advances a concrete cluster of related ideas

Prefer the first action that clearly holds. Do not produce a ranking unless asked.

Output exactly this shape:

```markdown
做：<one action>

理由：<two or three concrete sentences grounded in the selected entry's evidence/context/blocker>

下一步：<first concrete probe, with no duration estimate>
```

Reasoning rules:

- Cite concrete evidence from the selected entry, such as check status, linked issue, benchmark result, affected surface, conflict state, or blocker.
- Explain why this is actionable now, not just that it is `low cost` or `high impact`.
- Mention related ideas only when they materially strengthen or weaken the choice.
- Mention rejected alternatives only if the user explicitly asks for comparison.
- Do not include a "reselect condition" section by default.
- Do not mention time boxes or durations unless the user asks.

If the idea directory is empty or stale, choose a concrete capture/discovery action instead of inventing a full plan. Do not update statuses unless the user also asks.

If the user asks to start the chosen action, reread the candidate file, locate exactly one file by `id` or `source_id`, update only that file's `status:` to `doing`, and append one `YYYY-MM-DD started` entry under `events:`.
