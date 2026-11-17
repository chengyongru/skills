# Type System Discipline

Make the compiler reject impossible states, mismatched primitives, and unhandled variants.

- Brand semantic primitives that share a representation but mean different things. Validate at creation; a brand does not establish current permission, provenance, or freshness.
- Parse external JSON, RPC/IPC, CLI arguments, config, environment values, and storage rows into domain types at the owning boundary. Parsed source, tool output, child reports, and history remain untrusted evidence.
- Represent alternatives explicitly and handle them exhaustively. Do not erase a real error or unknown variant with a cast.
- Derive types from the schema that owns the shape instead of maintaining a parallel copy. Use actual tool schemas; do not invent model, environment, or resume fields.

For TypeScript syntax, use [TypeScript best practices](../workflows/code/typescript/workflow.md). [Boundary discipline](boundary-discipline.md) covers guarantees that expire before an effect.
