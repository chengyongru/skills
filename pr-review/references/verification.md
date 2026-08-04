# PR verification

Treat current green CI as evidence for its configured matrix. Add focused local proof when CI is missing/stale/failed/ambiguous, the changed contract lies outside that matrix, a concrete hypothesis needs reproduction, or the change affects security, migration, persistence, concurrency, packaging, restart, or a public surface.

Choose the smallest decisive check:

1. reproduce the base behavior when practical;
2. run the closest PR regression;
3. probe denial/bypass for authority changes;
4. exercise the user-facing interface;
5. feed old persisted/config/wire input into compatibility changes;
6. run a clean build/install/consumer smoke for packaging;
7. run broader suites for broad shared contracts when remote CI lacks coverage.

For side effects, cover timeout, cancellation, retry, duplicate delivery, restart, and cleanup according to the contract. For authority, cover applicable anonymous, malformed, expired, out-of-scope, delegated, redirect/alias, and alternate entrypoints.

Report CI coverage, focused actions/results, base comparison, remaining proof gaps, and PASS/WARN/FAIL for the claimed contract. Use `verify` for structured black-box checks.
