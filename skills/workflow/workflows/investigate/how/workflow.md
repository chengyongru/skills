# How

Explore the codebase to answer "how does X work?" questions. Use [behavior-first explanation](../../../references/explanation.md): build a mental model of the complete behavior, responsibilities, and correctness conditions, not an annotated tour of variables and calls.

Work directly by default, including for complex questions. Delegate independent tracing only when it meets the runtime contract's parallel-work and benefit criteria. For any bounded native `subagent` task, keep its returned task ID and name the question, angle, actual prompt/reference paths, allowed source reads, and a read-only contract: no file changes, process launches, or external mutations. Children inherit the configured model. This workflow explains the system; it does not change it.

## 1. Assess complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (one behavior or a narrow mechanism): inspect the relevant source and explain directly. Do not load explorer or explainer templates unless delegation is useful. Go to step 4.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): go to step 2.

When in doubt, take the simple path.

## 2. Explore (complex only)

Decompose the question into 2 to 4 distinct angles. Trace them directly unless parallel delegation is justified; in that case, assign non-overlapping angles using `references/explorer-prompt.md` before starting the traces, while the parent works on a different angle or necessary integration. Run bounded waves within the actual concurrency limit, normally at most two children at once. Await their reports and check only known task IDs when status is needed.

## 3. Synthesize (complex only)

Synthesize the evidence and any explorer reports in the main agent; use `references/explainer-prompt.md` as optional guidance, not a reason to spawn a separate explainer.

## 4. Present

Check load-bearing claims and cited paths against the source, resolve disagreements, and own the final explanation. Keep useful structure and evidence, but correct unsupported claims and trim it to the user's question. A returned report is not proof by itself.

## Output format

Use the shared explanation guidance directly; delegated explainers use `references/explainer-prompt.md`. Do not force a sectioned report. Lead with the observable behavior and use a small diagram when it clarifies causality. Include code locations only when necessary or requested.
