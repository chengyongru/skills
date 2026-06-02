# Service Startup

Use this when verification needs a long-running app, API, web UI, worker, or gateway.

## Startup Rules

- Start the service the way documentation says users start it.
- Use a fresh port when possible. `scripts/find-free-port.ps1 -Count 1` can provide candidates.
- Keep logs in the evidence directory.
- Wait for readiness through a public health endpoint, open port, page load, or documented startup message.
- Set `NO_PROXY` / `no_proxy` for `127.0.0.1,localhost` when local browser or HTTP checks are affected by proxies.

Developer flags for ports, test config paths, or temp directories are acceptable when they only isolate the run. Debug bypasses that skip the changed behavior are not valid proof.

## Cleanup

Record process IDs or job handles. Always stop services before finishing unless the user asked to keep them running.

If cleanup fails, report the remaining process, port, or temp directory.

## Evidence

Capture:

- Startup command.
- PID or job id.
- Readiness check and result.
- Relevant service logs around each request or interaction.
- Shutdown action.
