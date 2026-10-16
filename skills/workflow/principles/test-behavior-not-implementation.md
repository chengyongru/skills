# Test Behavior, Not Implementation

A test is a claim about what the code does for its users: a caller, an end user, or another service. Behavior is what those users can observe through the interface they use. That includes return values, errors, state they can read back, and effects on systems outside the code, such as a request sent, a row written, or a message emitted. Implementation is what they cannot observe: private helpers, internal call order, intermediate data, and which internal collaborator did the work.

Judge each test against two imagined edits:

- **Break the behavior.** Make the code return a wrong value, skip an effect, or do the effect twice. If the test still passes, it proves nothing. The usual causes are an assertion looser than the contract, an expected value computed by the code under test, a restated constant or prompt string that never runs the code that reads it, and an assertion on data that the test built itself.
- **Change the internals.** Keep every observable result the same and restructure the code underneath. If the test now fails, it is pinned to the implementation. It will need a rewrite on every refactor and still catches no bug.

Prefer a test that catches the first edit and survives the second. Inspect a failing or implementation-pinned test before changing it; preserve any useful regression coverage rather than deleting it to make a refactor green. Drive the users' interface with concrete input, derive the expected result from the requirement, and assert what the contract promises, no less and no more. Simulated destructive/external effects belong in isolated fixtures; real publication or user-data mutation needs the appropriate authorization.

The contract decides, not the shape of the assertion. When "an empty cart never charges" is the promise, an assertion that the payment client got no call is behavior. Pair it with a case where the charge happens, so that the test shows it can see a call. The payload that a mocked external service receives is behavior, because that service observes it. A call to an internal helper is implementation, because no user can see it. An empty list is the exact answer when no record matches, and a hollow check when the test only needs some result. An exact error message pins wording that no caller reads. The error type that callers branch on is the contract.

A test can pin an invariant instead of a call, such as a key that must exist in two tables or a compile-time type check. The invariant is the behavior. A structural skill/doc test can legitimately protect a required tool contract or safety boundary; distinguish that from gratuitously pinning wording. Pair structural checks with representative behavior where available, and report when the runtime path was not exercised.

Scale proof to the reachable change. Existing checks may suffice for a read-only analysis, and documentation does not need unrelated live/performance fleets. Do not invent runs, require new test files for every answer, or call same-model review cross-model verification.
