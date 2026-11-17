# Foundational Thinking

Get the data shape right before writing logic. Define core types early, trace access patterns, and choose structures for the dominant paths. Share the domain structure, not every similar line; prefer explicit code to premature abstraction.

Before sharing mutable state between actors, ask what happens if another actor changes it concurrently. If the answer is not nothing, isolate the state first.

Put real prerequisites first: shared types, fixtures, or checks that later units need. Remove proven dead code before building on it when removal is in scope. Do not expand a small task into unrelated CI or framework work. Keep authorized commits coherent and single-purpose; a better data model does not authorize a repository-wide rewrite or publication.
