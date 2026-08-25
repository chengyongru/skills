---
name: repo-prose
description: Write, review, or clean repository-facing technical prose in documentation, code comments, docstrings, tests, and contributor instructions. Express current repository behavior, preserve contracts, and remove authoring or review-session residue. Do not use for personal publishing or interface copy.
---

# Repository Prose

Write for a reader who has the resulting repository state, not the authoring transcript or PR conversation.

## Preserve the contract

- Make every reference and claim resolvable from the repository or a durable linked source.
- Preserve the complete proposition: actor, action, condition, ordering, modality, exception, ownership, failure mode, and consequence where relevant.
- Keep code, commands, identifiers, paths, values, and quoted output exact unless the task authorizes changing them.
- Retain non-obvious rationale when removing it could cause misuse or an incorrect simplification.

## Edit

1. Confirm the requested scope, applicable repository instructions, and the code or document that owns the behavior.
2. Identify the factual propositions before trimming or restructuring prose.
3. Remove authoring-session references, review choreography, change narration, planning residue, reviewer-directed defenses, code restatement, control-flow walkthroughs, and generic polish that add no durable fact.
4. Keep durable issue or standard references, measured bounds, regression rationale, negative guarantees, and historical narration whose explicit purpose is history.
5. Update the owning source before generated catalogs, snapshots, or derived documentation.
6. Re-read the result without the surrounding conversation and verify that every preserved claim remains concrete and checkable.

## Output

- For an authorized edit, change only the requested prose and run the narrow documentation or behavior checks that cover it.
- For a review, report only the location, missing or distorted proposition, consequence, and recommended correction.
- Follow the user's language. In Chinese, use natural Simplified Chinese and concrete nouns; keep technical identifiers unchanged and avoid translated review jargon or English sentence structure.
- Stop when the prose states the current behavior completely without session residue or unnecessary explanation.
