---
name: verify
description: Structured black-box functional verification after code changes. Use when asked to verify, validate, smoke-test, or evidence-check completed changes before merge/push/release, including explicit $verify requests. Collect diff context, classify user-facing surfaces, write a concrete verification plan, run tests through public interfaces such as APIs, CLIs, web UIs, and package consumers, capture command/output evidence, and report PASS/WARN/FAIL with limitations.
---

# Verify

Verify completed code changes from the outside, through interfaces a real user or integrator can use. Treat source reading, builds, linters, and unit tests as supporting context only; they do not prove user-visible behavior by themselves.

## Contract

A PASS is invalid unless it has all of:

- A concrete user-facing action or command.
- Captured evidence: exit code, stdout/stderr, HTTP status/body, browser state, screenshot path, or equivalent.
- An explicit pass rule written before or during execution.
- A judgment that maps the evidence to the pass rule.

If any part is missing, report WARN or FAIL. Do not write "should work", "probably", "looks fine", or equivalent language as a conclusion.

## Workflow

1. Collect context.
   - Read the requested range, or default to uncommitted changes plus `HEAD~1..HEAD`.
   - When PowerShell is available, run `scripts/collect-context.ps1 -Root <repo> -OutDir <evidence-dir>`.
   - Identify changed user-facing surfaces, not just changed files.

2. Classify verification targets.
   - Read `references/test-selection.md`.
   - Map each changed surface to required test types.
   - Prefer 1-5 high-signal tests. Include at least one changed happy path and the most important failure/edge path when user-visible.

3. Discover public interfaces.
   - Read `references/interface-discovery.md`.
   - Use documented commands, routes, packages, pages, or app entrypoints.
   - Do not use private modules, internal-only endpoints, direct database edits, or debug bypasses as proof.

4. Write a verification plan before executing.
   Use this schema in the working notes or final report:

   ```yaml
   change_summary:
   changed_user_surfaces:
   risks:
   interfaces_found:
   tests:
     - id:
       concern:
       interface: api | cli | web-ui | library | service | other
       setup:
       action:
       expected_evidence:
       pass_rule:
       evidence_target:
       destructive: false
       resources_required:
   limitations:
   ```

5. Load interface-specific guidance only as needed.
   - API or HTTP service: `references/api.md`
   - CLI: `references/cli.md`
   - Web UI: `references/web-ui.md`
   - Library/package public API: `references/library.md`
   - Long-running app startup, ports, readiness, cleanup: `references/service-startup.md`
   - Credentials, external services, writes, deletes: `references/safety.md`

6. Execute through public interfaces.
   - Capture every command with `scripts/run-with-log.ps1` when practical.
   - Example: `powershell -ExecutionPolicy Bypass -File scripts/run-with-log.ps1 -OutDir .verify -Name api-smoke -CommandLine "curl.exe -i http://127.0.0.1:3000/health"`.
   - For browser checks, capture visible state with Playwright, browser snapshots, screenshots, console errors, or page evaluation.
   - Stop background services and clean temporary files that were created only for verification.

7. Judge evidence.
   - Read `references/evidence-rules.md`.
   - Mark each test PASS, WARN, FAIL, or NOT RUN.
   - Reclassify unsupported PASS claims as WARN or FAIL.

8. Report.
   Include the plan, commands/actions, evidence, warnings, failures, cleanup, and limitations. If you write the report to a file, run `scripts/check-report.ps1 -ReportPath <file>` as a guardrail.

## Report Format

```markdown
## Verification Report

**Change**: <one-line summary>

| # | Concern | Interface | Action | Evidence | Result |
|---|---------|-----------|--------|----------|--------|
| 1 | ... | api | `curl ...` | `<file or key output>` | PASS/WARN/FAIL |

### Evidence
- Test 1: command/action, exit code/status, relevant output, pass rule, judgment.

### Warnings
- <WARN details, or "None">

### Failures
- <FAIL details, or "None">

### Limitations
- <untested surfaces and why, or "None">

### Cleanup
- <services stopped, temp dirs removed, or remaining artifacts>

### Conclusion
PASS/WARN/FAIL - <short evidence-backed summary>
```

## Hard Rules

- Use isolated local resources by default. Use real external services only when the user provides them or the project clearly documents a test environment.
- Ask before destructive tests or real writes unless the target is disposable test data created for this run.
- Redact secrets from reports and evidence summaries.
- Do not silently replace black-box verification with unit tests, static review, or internal imports.
- If the correct test cannot be run, state the limitation and why.
