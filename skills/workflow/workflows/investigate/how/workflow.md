# How

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

Delegate with native `subagent` tasks and keep their returned task IDs. Each task names the question, angle, actual prompt/reference paths, allowed source reads, and a read-only contract: no file changes, process launches, or external mutations. Children inherit the configured model. This workflow explains the system; it does not change it. If delegation is unavailable or prohibited, perform the same scoped exploration and synthesis directly and disclose that limitation.

## 1. Assess complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. Spawn one explainer that explores and explains in one pass, built from `references/explainer-prompt.md` without the explorer-findings section. Go to step 4.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): go to step 2.

When in doubt, take the simple path.

## 2. Explore (complex only)

Decompose the question into 2 to 4 angles, each a distinct slice of the subsystem. Create an explorer task per angle using `references/explorer-prompt.md`; run bounded waves within the actual concurrency limit, normally at most two tasks at once. Await their reports and check only known task IDs when status is needed.

## 3. Synthesize (complex only)

Once all explorers have returned, spawn one explainer with `references/explainer-prompt.md` and every explorer's findings filled in.

## 4. Present

Check the explainer's load-bearing claims and cited paths against the source, resolve disagreements, and own the final explanation. Keep useful structure and evidence, but correct unsupported claims and trim it to the user's question. A returned report is not proof by itself.

## Output format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.
