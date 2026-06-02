# Evidence Rules

Judge only from captured evidence.

## Results

| Result | Use when |
|--------|----------|
| PASS | The action ran through a public interface and all pass-rule conditions are proven by captured output. |
| WARN | The main behavior works, but there are relevant warnings, partial coverage, environmental caveats, or weak evidence. |
| FAIL | The action errors, crashes, returns wrong status/content, misses expected UI, or violates the pass rule. |
| NOT RUN | The test could not be executed. Include the blocker and what resource or state is needed. |

## Invalid PASS

Reclassify as WARN or FAIL if the only evidence is:

- Source code inspection.
- Build, lint, typecheck, or unit test success.
- Server startup without a user action.
- Import success without a public consumer.
- A screenshot or snapshot that does not include the changed area.
- A command with unread output.
- A browser page that loaded but did not exercise the changed interaction.

## Evidence Checklist

Each test should include:

- Exact action or command.
- Exit code, HTTP status, browser state, screenshot path, response body, stdout/stderr, or equivalent.
- Pass rule.
- Judgment explaining why the evidence passes, warns, or fails.

## Conclusion

Overall conclusion:

- PASS only when every required test is PASS and limitations do not affect the changed behavior.
- WARN when core behavior passed but coverage has meaningful caveats.
- FAIL when any required changed behavior fails.

Mention limitations explicitly. Do not bury failed or unrun checks behind a positive summary.
