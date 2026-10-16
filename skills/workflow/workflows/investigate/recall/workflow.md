# Recall

Rebuild the user's relevant working context and hand back a tight capsule of where things stand now and what to do next. Recall itself is read-only; finding an open thread does not authorize continuing it.

Two records matter. Prior conversations hold what the user and agents did and decided. The shared record holds related reports, reverted fixes, incidents, and design rationale. The [why](../why/workflow.md) skill searches those evidence categories when authorized read capabilities exist. Do not reconstruct a long-running bug from conversation summaries alone.

## Pass

1. **Classify, then route.** A specific branch/chat pickup may use the Session pickup playbook under `$workflow`; turning habits into a skill belongs to `$workflow automate-me`. Recall loads context, not a private child's execution state. If the user supplied a complete state capsule, use it and skip unnecessary mining.
2. **Lock the scope.** State the topic, workspace, and time window. Default "recent" to the last seven days, not an unbounded search. Never quietly reinterpret "all" as a recent sample. Ask for a workable bound if needed, and do not read another workspace without permission.
3. **Search prior sessions.** Use bounded `search_sessions` queries, then `read_session` on exact returned references. Order by returned timestamps, not opaque IDs. Read only matching sessions and relevant regions. The current conversation is the visible conversation, not a transcript file to discover. Do not read raw session stores or profile/memory journals.
4. **Partition only when useful.** For more than a few matching sessions, assign non-overlapping references or excerpts to read-only native child tasks, normally at most two at once. Retain their task IDs and await reports. Each returns topic, user goal, decisions, open threads, struggles/corrections, and artifacts (PRs, tickets, branches), with exact `session_ref` citations. Do not confuse private task IDs with historical session references. For a few sessions, read directly. Separate tasks use the configured model; they are not cross-model checks.
5. **Sweep the relevant shared record.** When the topic names a feature, subsystem, file, or bug, use `$workflow why`'s source recipes to ask: what is current, what was tried and failed, and what do users still report? Query only available authorized read sources; record missing categories. This can run alongside session reading within the same concurrency bound. For pure activity recall with no named target, history and live state may suffice.
6. **Check live state.** Inspect surfaced branches/PRs/tickets with available read-only Git, authenticated `gh`, or exposed connectors. Use installed [pr-review](../../pr/review/workflow.md) for an actual PR review, not an unsolicited fix or published review. For claims about tools an agent ran, use the session detail actually returned. If tool details or older messages are unavailable, report that gap rather than inventing a transcript location or claiming full verification.
7. **Write the brief.** Group by thread and stay on topic. Do not edit files, tickets, messages, profile, or memory to preserve the result.

## Output contract

Lead with the capsule, then thread status, then recurring problems, then the next move. Deeper detail goes below or gets cut.

- **Capsule.** At most five bullets: what the work is and where it stands overall.
- **Threads.** One line each with a supported status: `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[verified, uncommitted]`, `[reverted #N]`, `[planned, not started]`, or `[unknown: <gap>]`. Do not label historical assertions as verified current state.
- **Problems.** At most five recurring symptoms, including failed or reverted fixes so the next attempt starts where the last one failed.
- **Next move.** The single most useful concrete action; recommend it without taking an unrequested action.

Keep adjacent work out unless it blocks this topic. Cut detail before threads. Apply `$workflow unslop`, cite prior discussion by exact `session_ref` and shared evidence by its real source, and sanitize private material before any separately authorized public output.

**Reply:** the brief, with unavailable history or live-state checks clearly marked.
