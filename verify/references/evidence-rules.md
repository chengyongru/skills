# Evidence Rules

Judge only from captured evidence.

## Results

| Result | Use when |
|--------|----------|
| PASS | The action ran through a public interface and all pass-rule conditions are proven by captured output. |
| WARN | The main behavior works, but there are relevant warnings, partial coverage, environmental caveats, or weak evidence. |
| FAIL | The action errors, crashes, returns wrong status/content, misses expected UI, or violates the pass rule. |
| NOT RUN | The test could not be executed. Include the blocker and what resource or state is needed. |

## Supporting Evidence

Pair these forms of supporting evidence with a public user action before assigning PASS:

- Source code inspection.
- Build, lint, typecheck, or unit test success.
- Server startup by itself.
- Import success by itself.
- A screenshot or snapshot outside the changed area.
- A command with unread output.
- A browser page load before exercising the changed interaction.

## Evidence Checklist

Each test should include:

- Exact action or command.
- Exit code, HTTP status, browser state, screenshot path, response body, stdout/stderr, or equivalent.
- Pass rule.
- Judgment explaining why the evidence passes, warns, or fails.

## Conclusion

Overall conclusion:

- PASS when every required test is PASS and the changed behavior remains fully proven after considering limitations.
- WARN when core behavior passed but coverage has meaningful caveats.
- FAIL when any required changed behavior fails.

Lead with failed or unrun checks and state every limitation explicitly.
