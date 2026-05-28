---
name: verify
description: Black-box functional verification after code changes — analyzes diff, designs user-perspective test cases, runs them through real user-facing interfaces, reports evidence-based results
---

# Black-Box Verification

After code changes, verify things actually work by testing through the same interfaces a real user would use. No internal tools, no shortcuts — if a user can't do it, it's not a valid test.

## When to Use

- After a fix, refactor, or feature is implemented
- When the user types `/verify`
- Before merging or pushing non-trivial changes

## The Gate

Before claiming anything passes, you must:

```
1. DEFINE: What user-facing action proves this works?
2. RUN: Execute the test through a real user interface
3. READ: Full output — exit code, response body, error messages
4. JUDGE: Does the evidence confirm it works?
5. ONLY THEN: Say it passes
```

No "should work", no "probably fine", no partial checks. Evidence first, claim second.

## Process

### 1. Analyze the Diff

Read the git diff. Default range: `HEAD~1..HEAD`, or what the user specifies. Include uncommitted changes if the working tree is dirty.

Understand the **semantics**: not just which files changed, but what user-visible behavior is affected and what could break. Identify the risk areas.

### 2. Discover User-Facing Interfaces

Before designing tests, figure out how users interact with this project. Check:

- **CLAUDE.md / README** — how to start the service, what endpoints exist
- **package.json / Makefile / docker-compose.yml** — build and run commands
- **Config files** — what settings users can change
- **API definitions** — OpenAPI specs, route files, endpoint documentation

Identify the real interfaces: HTTP APIs, CLIs, web UIs, desktop apps, etc. These are your test surface.

### 3. Gather Test Resources

Some tests need real resources: a running database, API credentials, a service endpoint, a test account, etc. **Ask the user** — don't assume these are unavailable or off-limits.

Present what you need clearly:
- Which resources the test cases require
- What each resource is used for
- Any defaults you've detected (e.g., found a config file with an API key)

If the user provides resources, use them. If they decline, say so in the report — don't silently downgrade to a hack.

### 4. Design Test Cases

For each risk area, design a test case that a normal user could perform. Think from the outside:

- What would a user **do** to encounter this change?
- What would they **see** if it's working correctly?
- What would they **see** if it's broken?

For each case, specify:
- **Action**: What the user does (call an endpoint, run a command, open a page)
- **Expected**: What correct behavior looks like (response structure, not exact content)
- **Interface**: Which user-facing interface to use

### 5. Execute

Run tests through user-facing interfaces only.

**If the project is a service (API, web app, etc.):**
1. Start the service the way a user would (the dev server, `docker compose up`, etc.)
2. Send requests through its public interface (curl the API, load the page, etc.)
3. Read the response — status code, body, timing
4. Kill the service when done

**If the project is a CLI tool:**
1. Run the command as a user would, with realistic arguments
2. Check exit code, stdout, stderr

**If the project is a library/package:**
1. Write a minimal script that uses the library's public API the way a user would
2. Run it, check output and exit code

**For UI changes:**
1. Build the frontend the way the project documents it
2. Optionally open in browser and verify the changed element renders

Do NOT:
- Import internal modules or call private functions
- Use developer-only flags or debug endpoints
- Read source code to "check if it looks right"
- Substitute unit tests or linter runs for functional tests

### 5. Judge

For each test, read the actual output and judge:

| Result | Meaning |
|--------|---------|
| **PASS** | Response is correct: expected status, content present, no errors |
| **WARN** | Works but with unexpected warnings related to the change |
| **FAIL** | Error, crash, empty response, wrong status, or garbled output |

Keep yourself honest with the evidence rule:

| If you claim... | You need... | This doesn't count |
|-----------------|-------------|-------------------|
| It works | Real output from a real user action | Import doesn't error |
| API responds | HTTP response with expected structure | Server starts without error |
| CLI works | Correct stdout/exit code from the command | Source code looks right |
| Config loads | Service starts and handles a request | Parser doesn't throw |
| UI renders | Built successfully + page loads | Build passes alone |

### 6. Report

```
## Verification Report

**Change**: [one-line summary of the diff]

| # | Concern | Action | Result |
|---|---------|--------|--------|
| 1 | ... | [what the user would do] | PASS / WARN / FAIL |

### Warnings
[details for any WARN]

### Failures
[full output for any FAIL — response body, exit code, error messages]

### Conclusion
PASS / FAIL — [one-line summary]
```

## Principles

- **Real resources, real calls**: Use real credentials, real services, real data. That's the whole point — verify the actual system works end-to-end. Do not hesitate because it "costs tokens" or "hits a real server".
- **Backup before destruction**: If any test case might modify or delete real data (database writes, file operations, account changes, destructive API calls), back up first. Ask the user which data is at risk and how to protect it. Isolated test data is preferred over production data.
- **User-facing only**: If a normal user can't do it, it's not a valid test. No internal imports, no private APIs, no developer flags.
- **Full stack by default**: Start the real service and test through it. Isolating components is for unit tests, not black-box verification.
- **Be practical**: If the diff is very large, focus on the highest-risk areas. Better to deeply verify 3 critical paths than shallowly touch 20.
- **State limitations honestly**: If something can't be tested from the outside (e.g., external platform integrations, hardware dependencies), say so explicitly in the report rather than substituting a hack.
