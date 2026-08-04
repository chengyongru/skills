---
name: verify
description: General-purpose structured black-box functional verification after code changes. Use for cross-project verification, validation, smoke tests, and evidence checks before merge, push, or release, including explicit $verify requests. Collect diff context, classify user-facing surfaces, plan concrete checks, exercise public interfaces such as APIs, CLIs, web UIs, and package consumers, capture command/output evidence, and report PASS/WARN/FAIL with limitations. Project-specific verification skills take precedence when their scope matches.
---

# Verify

Verify completed code changes from the outside, through interfaces a real user or integrator can use. Source reading, builds, linters, and unit tests provide supporting context; public user actions provide the behavioral proof.

Use a matching project-specific verification skill as the primary workflow. Apply this generic skill to any remaining public surfaces that the specialized workflow does not cover.

## Contract

A PASS requires all of:

- A concrete user-facing action or command.
- Captured evidence: exit code, stdout/stderr, HTTP status/body, browser state, screenshot path, or equivalent.
- An explicit pass rule written before or during execution.
- A judgment that maps the evidence to the pass rule.

Use WARN or FAIL whenever one of these elements is missing. Phrase conclusions as evidence-backed judgments.

## Workflow

1. Collect context.
   - Read the requested range, or default to uncommitted changes plus `HEAD~1..HEAD`.
   - When PowerShell is available, run `scripts/collect-context.ps1 -Root <repo> -OutDir <evidence-dir>`.
   - Identify changed user-facing surfaces and connect each one to its changed files.

2. Classify verification targets.
   - Read `references/test-selection.md`.
   - Map each changed surface to required test types.
   - Prefer 1-5 high-signal tests. Include at least one changed happy path and the most important failure/edge path when user-visible.

3. Discover public interfaces.
   - Read `references/interface-discovery.md`.
   - Use documented commands, routes, packages, pages, or app entrypoints.
   - Treat private modules, internal endpoints, database inspection, and debug helpers as diagnostic context; prove behavior through the public interface.

4. Share a concise verification plan in commentary before executing.
   Use this schema as a thinking aid and keep the prose plan in the conversation:

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
       evidence_capture: terminal | log | screenshot | response
       destructive: false
       resources_required:
   limitations:
   ```

5. Load the interface-specific guidance that matches each target.
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
   - Assign WARN or FAIL to claims whose evidence falls short of the PASS contract.

8. Respond.
   - Reply directly in the conversation with the outcome, actions, evidence, warnings, failures, cleanup, and limitations.
   - Keep machine-consumable logs, screenshots, and raw responses only when they help substantiate the result.
   - Provide paths for retained evidence and ask whether the user wants it deleted.

## Direct Response Format

```markdown
**Result**: PASS/WARN/FAIL

**Change**: <one-line summary>

| # | Concern | Interface | Action | Evidence | Result |
|---|---------|-----------|--------|----------|--------|
| 1 | ... | api | `curl ...` | `<file or key output>` | PASS/WARN/FAIL |

**Evidence**
- Test 1: command/action, exit code/status, relevant output, pass rule, judgment.

**Warnings**
- <WARN details, or "None">

**Failures**
- <FAIL details, or "None">

**Limitations**
- <untested surfaces and why, or "None">

**Cleanup**
- <services stopped, temp dirs removed, or remaining artifacts>

**Conclusion**
PASS/WARN/FAIL - <short evidence-backed summary>
```

## Operating Rules

- Use isolated local resources by default. Use real external services only when the user provides them or the project clearly documents a test environment.
- Obtain confirmation before destructive tests or real writes; disposable test data created for the run is the normal target.
- Redact secrets from responses and retained evidence.
- Include at least one public-interface action in every black-box PASS; use static and unit checks as supporting evidence.
- State the missing resource, limitation, and residual risk when a required test cannot run.
