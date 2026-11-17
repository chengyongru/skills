# Test Behavior, Not Implementation

A test claims something users of the code can observe: return values, errors, readable state, or effects on external systems. Private helpers, internal call order, and intermediate values are implementation details.

Judge the test against two edits:

- Break the behavior with a wrong value, skipped effect, or duplicate effect. If it still passes, inspect loose assertions, expectations derived from the code under test, and assertions on data the test created itself.
- Change the internals while preserving every observable result. If it fails, check whether it is pinned to implementation rather than a real invariant.

Keep the useful regression assertion when rewriting a test; do not delete coverage to make a refactor green. Drive the public interface with concrete inputs and derive expectations from the requirement. An external service's received payload is behavior; an internal helper call usually is not. Pair a forbidden-effect case with one that demonstrates the effect can be observed. Assert the error contract callers use, including text only when it is part of that contract.

Structural tests may protect skill routing or authorization boundaries, but should not gratuitously pin prose. Pair them with representative runtime behavior when available and disclose unexercised paths. Keep destructive/external effects in isolated fixtures unless separately authorized.
