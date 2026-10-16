# Build the Lever

Prefer a repeatable lever when it reduces error or verification cost: an existing query, repository test, codemod, generator, or concise task recipe. A deterministic tool can turn "trust me" into a check a reviewer can repeat, but writing a new tool is not itself proof.

- Reuse installed skills and repository tools before adding a helper. Direct targeted reads or a documented command can be the right lever for a one-off analysis.
- For repetitive edits, learn the recipe on one unit, then prove the automation against that result before applying it more broadly. Limit paths, expose a dry run when useful, and make reruns safe.
- Prefer one bounded deterministic operation to a fleet hand-applying the same transformation. Inspect its outputs and run the behavioral checks; automation can repeat a mistake perfectly.
- For permitted delegation, put the recipe, acceptance checks, actual reference paths, and do-not-touch fences in the brief or a task-owned external artifact outside the delegate's write scope. A new installed skill is not required.
- A read-only investigation/review does not require a script, generated database, test, or file in the diff. Honor no-write/no-execution limits and report the evidence those limits allow.
- Create a new script only when its value justifies the maintenance and the request permits that output. Store task-local tooling/evidence outside the live plugin, and commit or publish it only if authorized. Never edit protected profile/memory to preserve the recipe.

Use the smallest lever that does or proves the job, not a framework. Do not invent unavailable bundled helpers or expand the task merely to satisfy this principle.

Distinct from [Encode Lessons in Structure](encode-lessons-in-structure.md), which makes a recurring correction durable. This is repeatability and reviewability for the task at hand. See [Prove It Works](prove-it-works.md) for evidence quality.
