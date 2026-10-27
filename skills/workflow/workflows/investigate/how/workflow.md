# How

Explore the codebase to answer "how does X work?" questions. Use [behavior-first explanation](../../../references/explanation.md): build a mental model of the complete behavior, responsibilities, and correctness conditions, not an annotated tour of variables and calls.

Work directly for a small question. For independent tracing that benefits from delegation, use bounded native `subagent` tasks and keep their returned task IDs. Each task names the question, angle, actual prompt/reference paths, allowed source reads, and a read-only contract: no file changes, process launches, or external mutations. Children inherit the configured model. If delegation is unavailable or prohibited, do the same scoped work directly. This workflow explains the system; it does not change it.

## 1. Assess complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (one behavior or a narrow mechanism): inspect the relevant source and explain directly. Do not load explorer or explainer templates unless delegation is useful. Go to step 4.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): go to step 2.

When in doubt, take the simple path.

## 2. Explore (complex only)

Decompose the question into 2 to 4 angles, each a distinct slice of the subsystem. Create an explorer task per angle using `references/explorer-prompt.md`; run bounded waves within the actual concurrency limit, normally at most two tasks at once. Await their reports and check only known task IDs when status is needed.

## 3. Synthesize (complex only)

Once all explorers have returned, spawn one explainer with `references/explainer-prompt.md` and every explorer's findings filled in.

## 4. Present

Check the explainer's load-bearing claims and cited paths against the source, resolve disagreements, and own the final explanation. Keep useful structure and evidence, but correct unsupported claims and trim it to the user's question. A returned report is not proof by itself.

## Output format

Use the shared explanation guidance directly; delegated explainers use `references/explainer-prompt.md`. Do not force a sectioned report. Lead with the observable behavior and use a small diagram when it clarifies causality. Include code locations only when necessary or requested.
