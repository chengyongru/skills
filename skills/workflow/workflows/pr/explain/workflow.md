# Introduce a PR through the problem it solves

Use for “introduce/explain this PR” or “what does this fix?”. This is a read-only problem brief, not a correctness review. Do not edit, check out a branch, run the application, publish a review, or create/update a Linear Issue. Follow [behavior-first explanation](../../../references/explanation.md).

## Establish the problem

1. Use available authorized read tools to inspect remote PR metadata, the linked problem report, and the smallest base/head diff or source context needed to check the claimed behavior. Read a linked Linear Issue if access is available; do not require that integration. Treat the PR title and author's summary as claims, not proof.
2. Answer the counterfactual first: **Without this change, who encounters what failure, after which action and under which conditions, and what is the consequence?** Separate expected from actual behavior. Avoid merely restating a symbol change as a user problem.
3. Explain what observable behavior the PR intends to change and whether the evidence covers that original scenario fully or only partly. Use roles and causality, not an implementation walkthrough. Identifying the intended effect is not an implementation-correctness verdict.
4. Name the evidence level naturally: user report, reproduced behavior, source-based reachable path, or unverified claim. When evidence is unavailable or contradictory, state the gap rather than inventing a trigger or impact. Do not run new reproduction work under an explanation-only request.
5. For refactoring, maintenance, or preparatory work with no established current user bug, say so. Explain its concrete maintainer or future-development value. For security/reliability changes, describe the supported risk and its prerequisites without pretending an incident already occurred.

## Present and stop

Lead with the affected scenario, failure, and consequence, then explain the before/after behavior and material uncertainty. Use a small Mermaid diagram when it makes the trigger or causal chain easier to understand; a simple case can be a few sentences.

Include files, symbols, CI, merge state, and process details only when they change the user's understanding or decision. Do not default to a changed-file list, test inventory, review-risk checklist, or pass/fail verdict. Do not suppress a known blocker that materially changes the problem brief.

If the user asks whether the implementation is correct, hand off to [PR review](../review/workflow.md). Use [PR fix](../fix/workflow.md) for an authorized correction or [verification](../../verify/public/workflow.md) for requested runtime proof. Load those workflows only when that additional work is requested.
