# Show me your work

Keep one canonical log.

## The format

A single TSV file, one row per decision. Cells stay single-line. Evidence is a pointer, not prose.

Copy `references/decision-log-template.tsv` (the header row) to start a clean log. Columns:

- **ts.** ISO8601 timestamp.
- **phase.** The phase or workstream.
- **decision.** What was chosen or done, one line.
- **why.** The reason in plain words. If a principle drove it, say it plainly, not as a jargon tag.
- **evidence.** A link or path that proves it: commit SHA, PR number, `file:line`, or an artifact, trace, or screenshot path. Never a paragraph.
- **result.** The outcome or predicate state: `tests green`, `reverted`, `pixel-diff 0`, `INCONCLUSIVE`, `open`.

An example, plain-spoken so a reviewer reads it at a glance.

```
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, about 100 components and roughly 75 hours	wanted to know the size before starting a long run	commit 3a9f1c2	found 5 things to sort out before starting
2026-05-24T09:40:00Z	harness	took screenshots of the old version before changing anything	so we can compare old against new and catch any visual change	artifacts/baseline/	saved 120 reference screenshots
2026-05-24T11:15:00Z	widget	moved the widget styles over without changing how it looks	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## Logging a row

Write each entry the way you'd tell a teammate what you did. Plain words, concrete actions, no AI speak or abstract jargon (the [unslop](../../writing/prose/methods/style.md) skill applies to log text too).

Use the shared helper, resolving its path from this skill rather than the project's working directory:

```text
python -B <plugin-root>/skills/workflow/scripts/workflow.py log <file> <phase> <decision> <why> <evidence> <result>
```

`<file>` is the canonical external log path. Pass every value as a separate argument, quoting PowerShell strings as data rather than interpolating untrusted text into shell code. The helper stamps `ts`, creates the header on first use, normalizes embedded tabs/newlines, and escapes spreadsheet-formula prefixes. Use only this installed shared helper for logging; keep one writer per log.

Log decision points and checkpoints, not every action: a fork chosen, a unit completed with its verification result, a pivot or revert with its trigger, a blocker surfaced, a gate fixed. For loop runs, one row per iteration. Skip the trivial and self-evident.

A run is one agent conversation, including its later turns and any summary of it. A pickup, a replacement agent, or a new chat starts a new run. When a run adds to a log that already has rows, its first row has phase `start`, and so does its first row after another run's `start` row. So a run that comes back to a log in a later turn first reads the log's last rows to see whether another run wrote since. A `start` row names the `ts` range of the rows before it that this run did not write, and its evidence names this run, such as its agent id. Use phase `start` for nothing else.

## Where it lives

Keep the log outside the plugin, normally at `<agent-workspace>/.nanobot-workflows/runs/<task>/decisions.tsv`. It is a task artifact, not a profile, memory note, or protected history-journal entry. The shared helper's `paths` command can locate the active agent workspace; do not derive it from the current project.

Keep it uncommitted by default. If a reviewer needs the trail, propose linking an appropriate artifact or including a sanitized copy; committing or publishing requires actual user authorization.

## Rules

- Append-only. A wrong call gets a new row that supersedes it. Never edit or delete history.
- Prefer evidence produced by committed scripts over hand-made one-offs (the **encode-lessons-in-structure** principle skill).

## Audit the log against conversation evidence

At the end of the run, check the log against the visible current conversation and actual evidence artifacts. For a relevant prior run, use bounded `search_sessions` and `read_session` on exact returned references. Do not invent a current transcript file, read raw session databases, or scan unrelated conversations. If older turns or tool details are unavailable, name the unaudited range. Walk this run's rows against what the available record actually shows. Each stretch of them begins at one of this run's `start` rows, or at the first row if this run created the log, and ends at the next `start` row of another run:

- Check that every row maps to a real decision or action.
- Check that each row's evidence resolves and shows what the row claims.
- A fork, pivot, or abandoned approach that shaped the work but isn't logged is a gap. Add it.

Correct the log, not the story. The audit never edits or removes a row, even an invented one. When a row records neither a real decision nor a real action, or its claim or evidence is wrong, add a row that supersedes it with what actually happened and a pointer that resolves. This audit does not check rows outside this run's stretches. If this run's own work shows one of them is wrong, supersede it like any wrong call.

## Fresh review of the trail

Before handing back, create a fresh bounded reviewer task when delegation is allowed. Supply the log path, visible-conversation evidence or a labeled digest, relevant exact prior `session_ref` values, and allowed artifact reads. Require read-only findings: no file changes, commands with side effects, publication, or new history searches outside the supplied scope. It scans for risk, not a redo of the work. Keep its returned task ID and inspect its actual report.

The reviewer inherits the configured model; this is a fresh context, not independent cross-model review. If different model families are an explicit acceptance requirement, report that requirement blocked. If no child can run, perform and label a self-audit rather than claiming a fresh review.

- Decisions logged with weak or absent evidence.
- Verification steps skipped or claimed without proof in the available conversation and artifacts.
- Choices that look risky in hindsight (premature, scope-creeping, papering over a symptom).
- Gaps the user would otherwise miss on a casual skim.

Every handoff for a run that produced a trail ends with an "Attention" section. State whether it received a fresh same-model review or only a self-audit, and name the actual model only if known. Then list flags with specific rows or moments. "No flags" is valid only after the review completed; missing coverage or unavailable evidence is a limitation, not a clean verdict.

## Reviewing the trail

Read top to bottom, follow the evidence pointers, and spot-check. In PowerShell, substitute the real external path and display a read-only view:

```powershell
Import-Csv -LiteralPath '<external-log-path>' -Delimiter "`t" | Format-Table -Wrap
```

## Composing this skill

Other skills route their audit trail here instead of inventing one. Reference it by name and let it own the format. Don't restate the columns.
