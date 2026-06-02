# Test Selection

Use this file to turn a diff into a small, concrete verification plan. Select tests by changed user-facing behavior, not by file count.

## Surface Mapping

| Changed area | Required verification |
|--------------|-----------------------|
| HTTP route, controller, middleware, OpenAPI, request/response schema | API test for the changed endpoint plus one relevant error path |
| Authentication, authorization, session, token, cookies | Authorized and unauthorized public-interface checks |
| CLI parser, command handler, flags, packaged binary | `--help` or equivalent plus at least one realistic command |
| Config loading, env vars, startup defaults | Start the app using user-level config/env and complete one public action |
| Web UI route, state, form, layout, navigation | Build/start UI, open in browser, inspect visible state, exercise changed interaction |
| Websocket, SSE, streaming, realtime behavior | Connect through documented public endpoint and observe one real event/message |
| Library public API, exports, package metadata | Create a minimal consumer script/project using documented imports |
| Persistence, migrations, filesystem writes | Use isolated test data, run a user-facing write/read path, verify persisted result |
| Error handling, validation, edge cases | Trigger the public error path and verify status/message/user-visible handling |
| Refactor with claimed no behavior change | Smoke-test the main public flow most likely to regress |

## Minimum Plan

For each verification target, write:

- Concern: what could break.
- Interface: API, CLI, web UI, library, service, or other.
- Action: exact command or browser action.
- Pass rule: observable condition that must be true.
- Evidence target: where output, screenshot, or logs will be captured.
- Resource risk: credentials, external service, writes, deletes, or none.

## Prioritization

When the diff is large, choose at most five tests:

1. Changed happy path users are most likely to hit.
2. Highest-risk failure path.
3. Startup/config path if changed.
4. Integration boundary: auth, network, filesystem, database, external service.
5. Regression smoke test for the most important unchanged public flow.

Do not add low-signal tests just to increase count. One deep browser/API/CLI check with strong evidence beats several shallow checks.
