# Create a verification skill

Every serious project needs a repeatable way to drive the real app and prove behavior: launch it, exercise a feature the way a user would, and capture evidence. Generate an authorized standalone skill at `<agent-workspace>/skills/verify-<app>/SKILL.md`, tailored to the repo. Resolve the active agent workspace, not the project's directory. Use installed `skill-creator` for authoring and [repo-prose](../../writing/prose/workflow.md) for repository-facing prose. Write for the next agent reading cold mid-task; never create a competing verifier or edit the immutable plugin automatically.

## 1. Interview the repo, not the user

First inspect installed verification skills and harnesses. Prefer the matching project-specific verifier or [project adapter](../../../references/project.md), then [public-surface verification](../../verify/public/workflow.md). If one already covers the need, use it or propose focused maintenance instead of generating a duplicate. Creating a new standalone skill requires the user's authorization. Answer the following from the codebase and only ask what cannot be observed:

- **Surface:** what does a user actually touch? A web UI, a CLI/TUI, a desktop app, an API, a mobile app, a library? A repo can have several; pick the primary one and note the rest.
- **Run:** how does the app start locally? Prefer the repo's own documented dev command (package scripts, Makefile, README quickstart). Note ports, env vars, seed data, auth.
- **Drive:** how can the current environment interact with it? Prefer existing Playwright/Cypress specs, supported terminal harnesses, HTTP endpoints, or debug ports. Use exposed Playwright tools for web when available, a Windows-compatible supported terminal path for CLI/TUI, and plain HTTP for services. Do not assume tmux, Bash, browser APIs, or an uninstalled control CLI; document missing capability as a blocker.
- **Observe:** what evidence can be captured? Screenshots, terminal transcripts, response bodies, logs, exit codes, DB state.
- **Isolate:** can two instances run side by side (ports, data dirs, profiles)? If not, say so in the generated skill: refusing to double-drive a shared instance beats corrupting the user's session.

If the checkout does not build or start, report the precise blocker before claiming a proven generator output. Product fixes need their own authorization; do not turn skill generation into unrelated repairs. A missing disposable test asset may be created only within the authorized verification setup, clearly labeled, isolated from user data, and removed during cleanup.

## 2. Generate the skill

Write `<agent-workspace>/skills/verify-<app>/SKILL.md` with `name: verify-<app>` matching the directory and a single-scalar `description` of at most 1024 characters naming the app, surface, and selection boundary. Use actual `$verify-<app>` invocation examples. Include these sections grounded in the repository and actual host capabilities, with no placeholders left:

- **Launch:** the exact PowerShell-compatible command and working directory, readiness signal, and teardown. Reach usable state from a disposable empty data directory, including authorized migrations and test seeds. A database answering health checks may still be initializing. Launch via `exec` and retain its returned session/process handle; use `exec_session` only for that session. For short-lived CLI/TUI drives, build once and run each in its own supported isolated terminal session. Installation, production access, and remote setup are separate permissions.
- **Doctor:** one read-only check that answers "is this instance worth driving?" — process up, right version/build, port owned by us, auth valid. An agent runs this first whenever anything looks off.
- **Drive:** the harness recipe with real selectors/commands from this repo, not examples. Prefer stable handles (ARIA labels, data attributes, prompt strings, route paths) over coordinates and tab order.
- **Evidence:** what to capture and its external run directory, never the plugin or profile/memory journal. Bound file/database mutations to disposable fixtures; separately authorize real outbound messages or remote writes. State the proof standards: exercise the real user path, not internal setters or test-only endpoints; capture the action and the resulting state, not just the final screen; verify side effects (files written, rows inserted, messages sent) alongside what's visible; mocks only where a production boundary already isolates the external system. When the safe path is a dry-run or test mode, verify what it actually skips by observing (files, network, git refs) rather than trusting its name: some dry-runs still touch the network or open a browser.
- **Cleanup:** how to tear down instances the run created. Never kill by process name; kill what you started. Cleanup removes instances and scratch state, never the evidence: proof artifacts survive the teardown, in a location the skill names.
- **Helpers:** document each helper's actual runtime, dependencies, PowerShell invocation, and allowed side effects. Test helpers that this authorized standalone skill creates; do not assume Unix executable bits or old pstack scripts. A helper the reader has to reverse-engineer is not a helper.

## 3. Seed the feature map

Create `<agent-workspace>/skills/verify-<app>/features/README.md` plus one file per user-facing feature you can identify (aim for the top 3-5 to start, from routes, commands, menus, or docs). Follow the shape in [`references/feature-map-example/`](references/feature-map-example), with a README index and one file per feature. Each file answers, from the user's point of view: what the feature is, how to reach it, how to drive it with the harness, and what observable end state proves it works. The four H2s are `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`. If the seed data lacks a precondition that a journey needs, the journey reports a failure and the reason goes in that feature's `Gotchas`. Never weaken the journey to make it pass. The map is the repo's maintained verification source; a proof that drives one convenient entry point is incomplete when the map lists others.

## 4. Prove the generated skill before handing it over

Within the authorized local test scope, run its instructions end to end once: launch, doctor, drive ONE mapped feature (one is enough; the map exists so later runs can cover the rest), capture evidence, clean up. After cleanup, confirm the evidence still exists at the named location — a cleanup that eats the proof fails this step. Fix what fails, and run the generated cleanup after every failed iteration too, so broken attempts don't strand processes and ports. A generated skill that was never executed is a draft, not a deliverable. If you proved it in a stand-in for the real target (a container in place of a fresh VM, a local stack in place of a remote one), list every setup step the stand-in did that the target will not. Those steps stay unverified until a run on the real target covers them.

## 5. Offer the maintenance loop

Point the user at `$workflow maintain-verification-skill` for keeping the map honest. Suggest a cadence only if asked; create a `cron` schedule only for an explicit approved time/interval, never as a generation side effect. No automatic commit, PR, package edit, or `$nanobot-gate` invocation.
