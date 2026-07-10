# Verification Reference

Use this file when CI is non-green/ambiguous or when the review's proof obligations extend beyond the configured CI matrix.

## Interpret CI narrowly

Remote CI is authoritative for the checks it actually runs on the reviewed head SHA. It does not prove untested platforms, persisted migrations, live services, real browsers, clean package consumption, security bypass resistance, or restart behavior.

Trust green CI without duplicating it only when:

- checks are current for the PR head;
- the changed contract is represented by the matrix;
- no concrete failure hypothesis needs reproduction;
- no high-risk public or lifecycle surface remains untested.

## Derive checks from proof obligations

Run focused local checks when at least one condition holds:

- CI is missing, stale, pending, failed, or ambiguous.
- The affected contract is outside CI or hidden by mocks/aggregate coverage.
- A blocker hypothesis needs a minimal reproduction.
- The PR changes security, migration, persistence, concurrency, retry, cancellation, packaging, or public-surface behavior.
- Static inspection cannot establish the claimed before/after.
- The user explicitly requests verification.

Prefer the smallest check that can decide the claim:

1. reproduce the old failure or unsafe behavior on the base when practical;
2. run the closest focused regression test on the PR;
3. use a negative/adversarial probe for trust boundaries;
4. exercise the public interface users actually touch;
5. test old persisted/config/wire input for compatibility changes;
6. run a clean build/install/consumer smoke for packaging changes;
7. run a full suite only when broad shared contracts changed and remote CI cannot answer them.

Use the `verify` skill for structured black-box validation when the changed surface warrants it.

Do not install dependencies or run long suites merely to manufacture confidence. If a required environment or credential is unavailable, report the exact evidence gap instead of simulating success.

## Security and lifecycle checks

For authority changes, test denial as well as success: unauthenticated, malformed, expired, out-of-scope, child/delegated capability, redirect/alias, and alternate entrypoint paths as applicable.

For concurrent or side-effecting changes, test partial completion: timeout after work starts, cancellation, retry, duplicate delivery, process restart, and cleanup failure as applicable.

## Reporting

Report:

- remote CI state and which obligations it covers;
- focused checks run, including command/surface and result;
- base reproduction when performed;
- untested obligations and why they remain;
- whether the conclusion is PASS, WARN, or FAIL for the claimed contract.
