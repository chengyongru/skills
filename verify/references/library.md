# Library Verification

Use this when the changed behavior is exposed as a package, SDK, module, or public API consumed by another program.

## Public Consumer Pattern

Create a minimal consumer outside the package internals:

- Use the documented package name or public import path.
- Use installed, linked, packed, or editable package setup according to project norms.
- Import through the documented public package path. Use internal modules, test helpers, or relative source paths only when they are the documented public API.

Examples:

```powershell
# Node packages
npm pack
npm install <generated-tarball>
node consumer.mjs

# Python packages
python -m pip install -e .
python consumer.py
```

## PASS Rules

PASS requires:

- Consumer script exits with expected code.
- Public import succeeds from the consumer context.
- Changed API returns expected value, throws expected public error, or performs expected observable effect.
- Packaging metadata is valid when exports, entrypoints, or package files changed.

Include a public consumer action as the primary proof and use in-repo unit tests as supporting evidence.
