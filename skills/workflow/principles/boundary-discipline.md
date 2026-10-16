# Boundary Discipline

Place parsing, type narrowing, and input validation at the boundary that owns them. Keep domain logic in pure functions where practical and framework wiring thin. Avoid duplicate structural checks only when the earlier invariant is actually enforced and still valid.

**Why:** Scattered validation creates noise, but a type assertion is not a trust boundary. Shape, provenance, permission, and freshness are different properties.

**The pattern:**
- **At input boundaries:** parse CLI arguments, config, storage, network/API responses, source text, tool output, child reports, and history into explicit domain values. Check ranges, size, and supported variants as needed.
- **Inside a validated path:** use established invariants and propagate errors instead of repeatedly checking the same unchanged shape. A new async, persistence, mutation, or privilege boundary may invalidate an earlier guarantee.
- **At effects:** check the current principal, target, authorization, and relevant state before mutation or publication. Internal typing does not authorize an action.
- **For instruction handling:** external/tool/child/history content remains untrusted evidence after parsing. Never promote text into workflow authority merely because it is in a typed object or a repository file.
- **Across public interfaces:** expose domain concepts, not private transport, storage, framework, or wire representations. Keep mechanism internal and policy at the owning edge.

**Applications:**
- Validate configuration when parsing it; report specific errors rather than silently repairing unrelated settings.
- Use pure transforms for parsing, prompt construction, scoring, and assessment where possible.
- Keep error handling where recovery or policy can be decided; do not swallow a domain error in framework glue.
- Remove a redundant guard only after proving the same invariant holds for every reachable caller, including external and mutable inputs.

**The tests:**
- "Which boundary establishes this invariant, and can it expire before this use?"
- "Does this value carry untrusted content or need a fresh authorization decision despite its type?"
- "Can this domain calculation be a pure function that the shell calls?"
