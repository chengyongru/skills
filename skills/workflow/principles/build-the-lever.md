# Build the Lever

For non-trivial mechanical work, prefer a repeatable tool that does or proves the job: a repository check, codemod, script, or generator. Reuse an existing tool before creating one; writing a tool is not itself proof.

- Do one representative unit first, then prove the tool reproduces that result. Bound its paths, make reruns safe, inspect its output, and run the behavioral checks.
- Prefer a deterministic operation to many workers applying the same recipe. For useful delegation, put the recipe, verification, and do-not-touch boundaries in a brief the worker cannot change.
- Build the smallest tool, not a framework. Add a file only when its value justifies maintenance and the task permits it. A read-only question may need only targeted reads or an existing command.
- Keep task-local tooling outside the installed plugin. Commit or publish only when authorized; do not install a skill or edit protected memory merely to preserve a recipe.

[Encode Lessons in Structure](encode-lessons-in-structure.md) covers recurring guardrails; [Prove It Works](prove-it-works.md) covers the quality of the result.
