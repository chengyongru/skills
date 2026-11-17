# Create formal verification

Use for `$workflow create-formal-verification-skill`, a request to model-check a race or prove an invariant, or an authorized reusable formal check. Find a valuable property, verify it, and leave a check another agent can rerun. A request to explain or plan remains read-only; a one-off investigation need not create a new skill.

## Choose from the code

Start with the user's named area. Read its existing verifier, repository instructions, and relevant source before adding another. Choose a promise whose violation harms users and whose cases ordinary tests cover poorly: event ordering, retry safety, ownership, lifecycle, parsing, arithmetic, or memory safety. Do not select a trivial property merely because it is easy to prove.

Let the question select the least costly adequate tool. TLA+/TLC is the executable default here for concurrent state transitions in any implementation language. A code-level verifier may be more appropriate for bounded input, overflow, or memory-safety claims; an unbounded property may need a theorem prover. Use tools the target repository supports. If no suitable code verifier is available, report that limit; generated-input testing is useful but is not a formal proof. No additional verifier is installed by selecting this workflow.

## Build the check

1. State the property and the harm in one plain sentence each. Identify the exact code snapshot, covered files/functions, other writers of the guarded state, and the real atomic boundaries. Do not combine two separately interleavable code operations into one model step.
2. Record the bounds, environment assumptions, fairness, constraints, and excluded behavior. Map every model action or proof obligation to code a reviewer can open. Keep model checking, code-level verification, and unbounded proof as distinct claims.
3. Put models, harnesses, and coverage metadata in an explicitly chosen target-repository directory or task-owned external location, never the installed plugin. For a requested standalone skill, use installed `skill-creator` and an authorized `<agent-workspace>/skills/verify-<project>-<area>/` destination. Do not add another registration to this package or assume project-local skill discovery exists in the host.
4. Provide one rerun command with reproducible dependency versions, the explicit workdir, timeout, evidence location, and cleanup. For TLA+, route to [Statechart](../../verify/statechart/workflow.md) for the actual commands and interpretation instead of copying its tool paths into a generated skill.
5. Record which files and symbols each check covers, the source commit and dirty-file hashes if applicable, and when their semantic correspondence was inspected. The generated instructions must recheck covered-code changes before trusting a model result. A static model does not automatically detect implementation edits.

## Demonstrate that it can fail

Use an isolated copy or disposable fixture within the authorized scope, preserving existing work. Introduce a meaningful broken variant, such as a removed ownership check or an interleaving that the real code permits. A code-level verifier must reject the changed code. For a separate model, demonstrate the changed source-to-model correspondence and the resulting failed property; do not claim an unchanged model detected a code mutation. Return to the original variant and confirm the original result. A baseline product violation stays a finding, not an invitation to weaken the property.

Run the generated instructions as a cold reader would. Replay discovered counterexamples against the actual code where safely possible. A model-only result without established correspondence is a modeling result, not a confirmed product defect. If execution or replay is blocked, name it; an unexecuted verifier is a draft. Product fixes, publication, installation, and scheduling require their own scope.

**Reply:** the property, chosen tool and reason, bounds and assumptions, actual result, demonstrated failure, source correspondence, rerun command, and uncovered behavior. Point to [Maintain formal verification](../maintain-formal-verifier/workflow.md) for later changes. Keep the human-facing explanation in the conversation unless a report was requested.
