# Behavior-first explanation

Load when explaining a technical mechanism, design choice, or PR. Explain the complete behavior and its correctness conditions, rather than translating source code into prose or assuming the implementation is correct.

## Explain the behavior

1. Lead with the result or problem in the user's terms. Identify who acts, the triggering situation, the expected outcome, and what actually happens.
2. Follow the causal path across the relevant boundaries. Explain who owns the facts, which steps depend on others, and what makes the final result trustworthy. Include reachable failure, concurrency, cancellation, retry, or persistence consequences when they affect the claim, not as a mandatory checklist.
3. Use roles, actions, and resources as names. Variable, field, class, and function names belong only where necessary to locate code, define an interface, explain diagnostic evidence, or answer an explicit implementation question. Do not begin with a file map or narrated call graph.
4. Distinguish observed behavior, source-based inference, hypotheses, and proposed changes. Do not invent a user bug to justify a refactor or treat a passing unit test as end-to-end acceptance. Assess the complete behavior while keeping edits within the task's scope.

## Use diagrams to carry the explanation

- Prefer Mermaid when relationships make the explanation clearer: flowcharts for causality/data flow, sequence diagrams for ordering and waits, state diagrams for transitions, and before/after diagrams for responsibility changes.
- Label nodes with understandable roles or behavior and arrows with the actual relationship. Draw only edges supported by the evidence; mark an uncertain relationship as a hypothesis. A collection of code identifiers in boxes is not a useful explanation by itself.
- Use the smallest complete diagram. Split or build it up when that helps understanding; do not require repeated diagrams merely because there are several components. A simple conclusion needs no figure.
- For spatial or rendered-UI claims, prefer existing captured evidence or a clearly labeled illustration. A schematic is not a product screenshot or runtime proof. Do not launch an application or debugger solely to decorate an explanation.
- Follow the figure with the key reason, tradeoff, and meaningful uncertainty. Do not repeat every node in prose. Offer implementation detail only when needed or requested.

Keep the initial answer short and in the user's language. Include technical identifiers, exact snapshots, and process metadata only when they help the current decision; retain necessary proof separately rather than weakening or hiding it.
