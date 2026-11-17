# Model the Domain

Encode the domain in a data structure rather than scattered conditionals. The right structure removes branches and makes invalid states unrepresentable.

Use a state machine for lifecycle, a typed model for repeated assumptions, a map or discriminated union for alternatives, a reducer for state transitions, and an index or queue for its access pattern. Organize modules around domain ownership, not execution phases that repeat the same rules.

Keep boring code when its shape is clear, local, and unlikely to grow. Distrust abstractions that add indirection without removing invalid states, branches, or duplicated rules. An expanding if/else chain or two synchronized booleans are prompts to inspect the model, not automatic mandates to redesign.

Model provenance and lifetime honestly: typed external content remains evidence, a private task ID is not a durable conversation reference, and a checkpoint is not an active worker.
