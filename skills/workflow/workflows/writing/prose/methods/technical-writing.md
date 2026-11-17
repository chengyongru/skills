# Technical writing

Write so a tired engineer understands on the first read. Follow [repository prose](../workflow.md); these layers do not override facts, repository conventions, or the user's language.

- Cut words that do no work and choose everyday words.
- If a style rule makes the sentence worse, fix it another way or leave it alone.
- Use the real symbol, file, flag, or command when naming an implementation detail. Do not invent jargon; explain a named pattern on first use.
- Vary sentence length. Split two thoughts, but keep a longer sentence that carries one fact and its conditions. Be specific rather than sterile.

## Pick the mode first (Diátaxis)

Give each document one purpose; split and link different modes when useful.

- **Tutorial:** learning by doing. State what the learner builds and the visible result of each step. Keep explanation brief and linked.
- **How-to:** steps to a goal. Assume competence, solve the reader's problem, allow necessary forks, and name the guide by the task.
- **Reference:** facts for lookup. Describe completely and precisely, following the structure of the thing described.
- **Explanation:** understanding and reasons. Keep one bounded topic with decisions, constraints, history, and alternatives. Make judgments explicit.

## Write to the reader (Google developer style)

- Use present tense and name who does what. Use passive voice only when the actor is unknown or irrelevant.
- Write instructions as commands, with the condition first and the common case before exceptions.
- Avoid buzzwords, figurative language, and "simply", "easy", or "quickly" in procedures.
- Use descriptive links and sentence case headings without skipped levels.
- Number sequences; use bullets otherwise. Keep list items parallel.
- Put code in code font and UI elements in bold. Do not hide an incomplete list behind "etc.".

## Give one instruction at a time (STE)

- Give each instruction its own sentence and put warnings before the guarded step.
- Split dense instructions rather than impose a word-count limit at the expense of meaning.
- Keep articles and verbs. Give each action one consistent name.
- Prefer direct commands to passive narration.

## Remove ambiguous readings (Global English)

- Put "only" and "not" beside what they modify.
- Break long noun strings and make pronoun references obvious.
- Keep small structural words such as "that" when they prevent a misread.
- Clarify which items "and" or "or" joins; repeat articles when needed.
- Prefer periods to long connector punctuation and avoid ambiguous slashes or "(s)" plurals in prose.
- Use consistent names and literal phrasing rather than idioms or metaphors.

## Apply repository conventions

Use the [style method](style.md) for filler and AI patterns. Keep necessary source uncertainty intact. For PRs and commits, use the sentence layers without imposing a Diátaxis document mode. A PR body is a short briefing; link detailed logs and tables.

Product UI strings follow the product's copy guidelines. Code examples follow the repository's indentation and syntax. Use real paths, and verify counts and tree claims against the delivered snapshot; include a regeneration command when useful.
