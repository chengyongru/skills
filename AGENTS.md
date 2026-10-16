# Nanobot Workflows repository guidance

## Package boundary

- Keep exactly two discoverable entries: `skills/workflow/SKILL.md` and the explicit-only `skills/nanobot-gate/SKILL.md`.
- Keep the primary entry under 60 lines. Route to one domain, then load the selected workflow; do not copy the entire catalog into an entry or runtime contract.
- Store internal procedures as `workflow.md` or named reference files, not additional `SKILL.md` registrations. Update every caller and example when moving an internal route.
- Keep executable helpers and their resources adjacent to the owning workflow. Resolve paths from that document, and use an explicit target repo/workdir for commands.
- Keep shared readable resources beneath a registered skill root. Keep runtime state, logs, evidence, bytecode, and generated skills outside the installed package.
- Preserve literal user activation of `$nanobot-gate`. No other route may imply it.

## Source and behavior

- Use concrete actions, preconditions, and expected outcomes. Include decisions and contracts the model cannot safely infer; link optional detail instead of repeating it.
- Preserve the concrete PR, worktree, verification, and environment helpers. Adapt orchestration around them rather than replacing proven operations with generic advice.
- Preserve exact snapshot and authorization boundaries, reachable behavioral assertions, owned-resource cleanup, and honest proof limitations.
- Treat nanobot as the runtime target while keeping project-neutral methods reusable. Route project-specific proof to the matching verifier.
- Preserve third-party attribution, upstream license text, and provenance when adapting or merging pstack material.
- Do not run `ruff format` or edit protected profiles/memory as part of skill maintenance.

## Verification and output

- Run `python -B -m unittest discover -s tests -v` and the adjacent tests for helpers changed or relocated.
- Use a compatible nanobot environment for native discovery, activation, summary, invocation, and restricted-resource-read proof. A skipped native check is not a pass.
- Keep human-facing plans, findings, and verification results in the conversation. Persist machine-readable state or raw evidence only when useful; create a prose report only when requested.
- Update both README files when installation, invocation, or routing contracts change.
