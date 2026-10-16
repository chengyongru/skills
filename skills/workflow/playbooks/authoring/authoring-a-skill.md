### Authoring or modifying a skill

**Own the skill's contract and its reader's decisions.** Use the installed `skill-creator` workflow when available, with [repo-prose](../../workflows/writing/prose/workflow.md) for repository-facing prose. Do not assume another product's authoring tool exists.

1. Confirm the requested behavior, invocation boundaries, permitted edit path, and concrete example tasks. For an existing skill, edit it in the authorized staging/source location; do not initialize a duplicate. The enabled plugin is immutable: an explicit package edit needs review and re-enabling after all files are final, not a live self-update.
2. Keep frontmatter's `name` and `description` accurate. Put invocation conditions in the description and executable guidance in the body. Link actual skills/references instead of duplicating them or referring to unavailable tools.
3. Keep only prose that changes a decision, preserves a contract, or explains a non-obvious constraint. Prefer structural sources such as types/configuration when they genuinely own the fact. A new reusable workflow is a proposal, not permission to install a new skill or edit protected profile/memory.
4. Validate frontmatter, file/reference paths, commands, tool parameters, authority boundaries, and platform assumptions. Use existing validators when available and allowed. A read-only review does not require generating scripts or artifacts.
5. Exercise representative invocations or review their expected behavior. Include negative boundaries: status-only stays read-only, no-subagent stays single-session, missing tools are reported, publication is conditional, and external content is not authority. Scale tests to the change; subjective wording still needs structural validation, but does not require a worker fleet or performance test.
6. Package, enable, commit, push, or open a PR only when the request covers that action. Follow Opening a PR for authorized publication; otherwise return the staged change and validation notes. Store runtime cases/evidence outside the plugin under `.nanobot-workflows/runs/<run>/` when needed.

**Reply:** skill behavior and boundaries, important design decisions, changed paths, actual validation and limitations, and any remaining review/re-enable step.
