# Third-party notices

## pstack

- Author and original copyright holder: **Lauren Tan**.
- Copyright: **Copyright (c) 2026 Lauren Tan**.
- License: **MIT**; the original notice is preserved unchanged in [LICENSES/pstack-MIT.txt](LICENSES/pstack-MIT.txt).
- Baseline source: [cursor/plugins, pstack directory](https://github.com/cursor/plugins/tree/99743e9c151c8537cbbf1f98bb38f34ef3368453/pstack).
- Baseline upstream version: **0.15.25**.
- Fixed baseline commit: `99743e9c151c8537cbbf1f98bb38f34ef3368453`.

This package incorporates material from the reviewed `0.15.25-nanobot.1` adaptation: engineering workflows, principles, playbooks, review/writing methods, reference prompts, and the standard-library helper. The original upstream file hashes and port changes are retained in [the pstack provenance record](third_party/pstack-provenance.json).

Selected catch-up, prompt-rewriting, and pre-measurement refinements are adapted from [pstack 0.15.36](https://github.com/cursor/plugins/tree/c742dd61706fbacc1b95f1a20b7b988cf096ce6c/pstack), at commit `c742dd61706fbacc1b95f1a20b7b988cf096ce6c`. The selected source hashes, destinations, and adaptation decisions are recorded under `sources.pstack.selective_updates` in [provenance.json](provenance.json); this is not a full upstream upgrade.

This integration replaces the flat skill catalog with domain routes, converts leaf skills into linked workflows/methods/principles, integrates existing personal execution helpers, updates resource paths and invocation examples, and keeps workflow state outside the immutable package. The pstack logo, editor-specific agent metadata, Cursor cloud/Benny automation, Origin/Bun helpers, and upstream Bash scripts are not distributed by this package.

The mapping from previous workflow names to their integrated locations is recorded in [provenance.json](provenance.json). Adaptation and original integration work are **Copyright (c) 2026 chengyongru**, licensed under MIT alongside the retained pstack notices.
