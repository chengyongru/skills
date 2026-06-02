# Interface Discovery

Find how a real user or integrator enters the system before designing tests.

## Inspect

Use fast search first:

```powershell
rg --files -g "README*" -g "CLAUDE.md" -g "package.json" -g "Makefile" -g "docker-compose*.yml" -g "docker-compose*.yaml" -g "pyproject.toml" -g "Cargo.toml" -g "go.mod" -g "*openapi*" -g "*swagger*"
```

Then inspect the relevant files for:

- Start commands and required services.
- Public HTTP routes, CLI commands, web pages, package exports, or desktop/app entrypoints.
- Required configuration, credentials, ports, database, or fixtures.
- Existing E2E, smoke, or integration test commands that use public interfaces.

## Interface Inventory

Record the discovered interfaces:

```yaml
interfaces_found:
  api:
    start:
    base_url:
    endpoints:
  cli:
    command:
    docs:
  web_ui:
    start:
    url:
    routes:
  library:
    package_name:
    public_imports:
  resources:
    required:
    optional:
```

## Valid Proof

Valid proof uses the same boundary a user can use:

- HTTP client against public routes.
- Browser against served UI.
- CLI command as installed or documented.
- Minimal consumer project/script using documented package imports.
- Public websocket/SSE/client protocol.

Invalid proof:

- Calling private functions or internal modules.
- Editing database rows directly to prove application behavior.
- Using debug-only bypasses as the main test.
- Reading source and claiming behavior.
- Treating "server started" as proof of changed behavior.
