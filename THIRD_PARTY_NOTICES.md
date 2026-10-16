# Third-party notices

## pstack

- Author and original copyright holder: **Lauren Tan**.
- Copyright: **Copyright (c) 2026 Lauren Tan**.
- License: **MIT**; the original notice is preserved unchanged in [LICENSES/pstack-MIT.txt](LICENSES/pstack-MIT.txt).
- Source: [cursor/plugins, pstack directory](https://github.com/cursor/plugins/tree/99743e9c151c8537cbbf1f98bb38f34ef3368453/pstack).
- Upstream version: **0.15.25**.
- Fixed upstream commit: `99743e9c151c8537cbbf1f98bb38f34ef3368453`.

This package incorporates material from the reviewed `0.15.25-nanobot.1` adaptation: engineering workflows, principles, playbooks, review/writing methods, reference prompts, and the standard-library helper. The original upstream file hashes and port changes are retained in [the pstack provenance record](third_party/pstack-provenance.json).

This integration replaces the flat skill catalog with domain routes, converts leaf skills into linked workflows/methods/principles, integrates existing personal execution helpers, updates resource paths and invocation examples, and keeps workflow state outside the immutable package. The pstack logo, editor-specific agent metadata, Cursor cloud/Benny automation, Origin/Bun helpers, and upstream Bash scripts are not distributed by this package.

The mapping from previous workflow names to their integrated locations is recorded in [provenance.json](provenance.json). Source attribution does not imply that every resulting file is unchanged upstream material. Adaptation and original integration work are **Copyright (c) 2026 chengyongru**, licensed under MIT alongside the retained pstack notices.

This repository is an independent nanobot integration, not an official Cursor or pstack release, and does not claim endorsement by the upstream author.
