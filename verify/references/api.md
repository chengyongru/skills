# API Verification

Use this when the changed behavior is reachable through HTTP, websocket, SSE, or another public network protocol.

## Plan

For each API test, specify:

- Method, URL, headers, and body.
- Auth state: anonymous, valid user, invalid token, expired token, or test credential.
- Expected status code range.
- Expected response shape or key fields.
- Expected error shape for negative tests.

## Execute

Start the service as documented. Use `references/service-startup.md` for ports, readiness, logs, and cleanup.

Prefer `curl` when available because it exposes status and body clearly:

```powershell
curl.exe -i -sS -X GET "http://127.0.0.1:<port>/<path>"
```

For JSON responses, parse enough to prove the shape:

```powershell
$body = curl.exe -sS "http://127.0.0.1:<port>/<path>"
$json = $body | ConvertFrom-Json
$json | ConvertTo-Json -Depth 8
```

## PASS Rules

PASS requires all applicable evidence:

- HTTP status matches the expected class or exact code.
- Body parses when JSON is expected.
- Required fields, headers, or content are present.
- Error responses expose the expected user-facing error, not a stack trace.
- Server logs do not show errors related to the request.

## Common Cases

- Schema change: verify new/changed fields and absence of malformed output.
- Validation change: send valid and invalid payloads.
- Auth change: verify allowed and denied states.
- Pagination/filtering/sorting: verify the response contract, not exact fixture-dependent totals unless controlled.
- Streaming/realtime: connect through the documented endpoint and capture at least one expected message or event.

Do not query databases, import route handlers, or call internal test helpers as the proof.
