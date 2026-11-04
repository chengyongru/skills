# Code Quality Review

Apply this lens within the requested scope and the [PR review criteria](../../references/review-criteria.md). Structural concerns need a concrete correctness or maintenance consequence; code size and preferred designs are prompts to investigate, not findings by themselves.

Look for simplifications that remove a demonstrated burden while preserving behavior. Count replacement code and new indirection when judging a proposed reduction; moving the same complexity into more files does not remove it.

## Core Prompt

Start from this baseline:

> Audit the supplied diff and exact snapshot. Do not replace a focused scope with the whole current branch.
> Rethink how to structure / implement the changes to meaningfully improve code quality without impacting behavior.
> Work to improve abstractions, modularity, reduce Spaghetti code, improve succinctness and legibility.
> Be ambitious about proposing a restructuring when it clearly improves the implementation, but do not apply changes during this review.
> Be extremely thorough and rigorous. Measure twice, cut once.

## Dimensions

Each dimension is stated once. Apply the ones that are relevant.

0. **Look for structural simplification.** Consider reframings that remove branches, helpers, modes, conditionals, or layers. Explain the actual burden removed and the cost of the replacement. Simple code with no demonstrated problem does not need a redesign.

1. **Inspect file growth for mixed responsibilities.** Propose decomposition when it separates real ownership or removes a concrete maintenance burden. Crossing a line-count threshold alone does not justify a finding or a mechanical split.

2. **Do not allow spaghetti growth in existing code.** Be suspicious of new ad-hoc conditionals, scattered special cases, or one-off branches inserted into unrelated flows. Treat "weird if statements in random places" as a design problem, not a style nit. Prefer pushing the logic into a dedicated helper, state machine, or module instead of tangling an existing path.

3. **Bias toward cleaning the design, not just accepting working code.** If behavior can stay the same while the structure becomes meaningfully cleaner, push for the cleaner version. Prefer simplifications that remove moving pieces over refactors that spread the same complexity around.

4. **Prefer direct, boring, maintainable code over hacky or magical code.** Treat brittle, ad-hoc, or "magic" behavior as a problem. Be skeptical of generic mechanisms that hide simple data-shape assumptions. Flag thin abstractions, identity wrappers, or pass-through helpers that add indirection without buying clarity.

5. **Push on type and boundary cleanliness when it affects maintainability.** Question unnecessary optionality, `unknown`, `any`, or cast-heavy code when a clearer type boundary could exist. Prefer explicit typed models over loosely-shaped ad-hoc objects. If a branch leans on a silent fallback to paper over an unclear invariant, ask whether the boundary should be made explicit.

6. **Keep logic in the canonical layer and reuse existing helpers.** Call out feature logic leaking into shared paths or implementation details leaking through APIs. Prefer existing canonical utilities over bespoke one-offs. Push code toward the right package, service, or module instead of normalizing drift.

7. **Treat unnecessary sequential orchestration and non-atomic updates as design smells when the cleaner structure is obvious.** If independent work is serialized for no reason, ask whether it should run in parallel. If related updates can leave state half-applied, push for a more atomic structure. Do not over-index on micro-optimizations, but do flag avoidable orchestration complexity that makes the code more brittle.

## Output Expectations

Use the parent review's priority order: security, data, and correctness issues come before structural suggestions. Keep confirmed findings separate from risks, questions, and optional improvements.

## Blocking Bar

Block only for a demonstrated contract violation or concrete maintenance consequence within the change's scope. Name the affected caller or maintainer task, the burden introduced, and why the proposed fix is necessary. A preferred abstraction, a shorter file, or an opportunity for unrelated cleanup is not a blocker.

## Review Tone

Be direct, serious, and demanding about quality. Do not be rude, but do not soften major maintainability issues into mild suggestions. If the code is making the codebase messier, say so. If the implementation missed an obvious dramatic simplification, say that too. Do not be satisfied with "maybe rename this" when the real issue is structural.
