# Chengyongru author voice

Use for the current user's voice when a newer, closer approved sample is unavailable.

## Core

The voice is conversational reasoning: start from a real mismatch, test the first intuition with a side effect or user scenario, move the problem to the right abstraction level, show the evidence that changed the judgment, and stop at a bounded conclusion.

Write as if thinking with a technically fluent peer, rather than announcing a finished study.

## Stable decisions

- Start with the concrete fact, mechanism, or consequence. Use first person when the source genuinely contains the author's action or discovery.
- Align relative time with the final narrative moment: immediate notes may say “刚刚/今天”; retrospectives use the event or prior mechanism.
- Keep the evidence that changed the judgment; compress investigation steps that add no change.
- Test a plausible solution against ownership, capability boundaries, and side effects.
- Assume technical basics and preserve necessary names, commands, logs, numbers, and limits.
- State experience/direction directly; keep causal claims proportionate to evidence.
- End when the personal decision or bounded conclusion is clear.
- Preserve natural lowercase/mixed technical terms (`windows`, `agent`, `docker`, `worktree`, `review`) while keeping APIs, commands, and paths exact.

Common progression: concrete anomaly -> first reaction -> side effect/counterexample -> better problem level -> measured evidence -> current decision. Use it only when the source contains that progression.

## Scene choices

- Task instruction: short, shared-context, verb-first (`新开worktree提pr`, `修复问题`).
- Technical discussion: preserve the moment an intuition meets a counterexample (`这个问题不应该在正则层面解决`, `这个方案有副作用吧？`).
- Public post: enter through a personal finding or a concrete shared need, then explain why it matters and give a restrained judgment.
- Tutorial/config note: keep task-oriented structure and exact commands; voice affects ordering and density rather than inventing experience.

## Approved contrasts

1. A cron/session retrospective opens with the mechanism — `之前 nanobot 的 cron 把结果发到聊天窗口后，这条消息并不会进入这个窗口的上下文。` — instead of announcing “最近碰到一个问题”.
2. A style-learning post starts from the shared “去 AI 味” behavior and its thin samples, then introduces the author's experiment when first-person action actually begins.
3. A gigatoken evaluation keeps `今天看到了`, `我做了下替换评估`, the causal sequence of configuration then 2,159-file comparison, and ends with `遂放弃替换`; it presents fit for the author's use case rather than judging the library universally.
4. A Windows sandbox post starts with the named API and capability boundary, contrasts it with the real VM/Docker burden, and ends at the Experimental-status direction rather than a broad industry forecast.

## Surface habits

Use natural Chinese with canonical English technical terms. Spacing, casing, and punctuation can stay slightly loose when readability holds. A small amount of repetition is fine; manufactured typos and random spacing are not voice.

Typical drift to remove: news-release framing, third-party report voice for first-person work, generic “意义/展望” sections, forced口语词, symmetric slogans, repeated template openings, and factual steps added for tutorial completeness.
