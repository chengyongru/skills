# Library Verification

Use this when the changed behavior is exposed as a package, SDK, module, or public API consumed by another program.

## Public Consumer Pattern

Create a minimal consumer outside the package internals:

- Use the documented package name or public import path.
- Use installed, linked, packed, or editable package setup according to project norms.
- Avoid importing `src/internal`, private modules, test helpers, or files by relative path unless that is the documented public API.

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

Do not use in-repo unit tests as the only proof. They can support the result, but the evidence must include a public consumer action.
