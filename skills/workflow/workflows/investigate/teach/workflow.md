# Teach

Explain what a thing does, how the complete behavior works, and why the relevant choices matter. This is read-only teaching, not implementation or review. Follow [behavior-first explanation](../../../references/explanation.md).

1. Infer the user's question and existing knowledge from the conversation. Choose the few things needed to understand the behavior; do not quiz them or introduce a mandatory lesson outline.
2. Read the smallest useful source context. Load [how](../how/workflow.md) when mechanism tracing is needed and [why](../why/workflow.md) when the rationale matters. Reuse existing findings; do not run both investigations or load their full sources by default. Keep source confidence and unresolved uncertainty intact.
3. Work directly for a small question. Use bounded native tasks only for genuinely independent questions when permitted; a no-subagent request prevails. Give children the actual selected references and read-only scope.
4. Lead with a plain result tied to the user's situation. Explain roles, causality, correctness conditions, and relevant edge cases rather than listing functions, fields, or constants.
5. Prefer a small Mermaid diagram when relationships or ordering carry the explanation. Add another diagram only when it improves understanding, not to satisfy a component-count rule. For spatial claims, use existing captured evidence or a labeled illustration. Do not launch an app or attach a debugger solely for the explanation.
6. Use short, natural prose in the user's language. Explain the key reason and tradeoff without narrating every diagram node. Give implementation locations only when useful or requested, and expand at the user's pace without imposing an extra writing workflow.

**Reply:** the explanation itself, not a report of the investigation process. Give the smallest complete answer first, then stop or add only the depth the question needs.
