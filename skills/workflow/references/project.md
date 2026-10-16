# Target project

The current repository supplies the engineering contract. Nanobot supplies the tools used to carry it out.

1. Confirm the project root, repository identity, working branch, and existing changes.
2. Read the project's `AGENTS.md`, contribution guidance, relevant issue or task criteria, and affected subsystem documentation.
3. Obtain tool versions and build, lint, format, test, and launch commands from the project's manifests, scripts, and CI. Follow its supported platforms and compatibility requirements.
4. Select the matching installed verifier or project adapter for the changed surface. Otherwise use [public-surface verification](../workflows/verify/public/workflow.md) to design checks through the project's CLI, API, UI, or package interface.
5. For terminal or browser work, use the application's documented launch path and supported environment. Record owned processes, ports, test data, and evidence for cleanup.

## Project adapters

Load an adapter after confirming the target repository or an explicit request to use it.

| Target | Adapter |
|---|---|
| HKUDS/nanobot and its forks | [Nanobot development](../projects/nanobot/workflow.md) |

Keep repository-specific commands, fixtures, visual calibration, and acceptance rules in the owning adapter. Other projects use their own instructions and verification setup.
