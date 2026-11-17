# Figure it out

For large, cross-cutting, unattended, or otherwise unmatched work, design the workflow before coding. Scale the phases and verification to the task and keep a decision trail the user can inspect after stepping away. The request still determines whether to execute or stop at a plan.

## Start

Keep a short checklist for the phases below. Select only decision-relevant guidance from the [principles reference](../../../references/principles.md), rather than loading the entire catalog. Present the designed workflow in the conversation; save a prose plan only when the user requests a persisted artifact. Keep any authorized run artifacts outside the installed plugin.

## Phase A: Frame

Ground first, then commit. Don't start the run until you can state:

- The definition of done as a falsifiable predicate (the **prove-it-works** principle skill).
- Scope, quantified: rough units and effort, plus the blockers grounding surfaced.
- Verification proportional to the risk. One-way doors and high blast radius need more evidence; reversible low-stakes steps need less. Keep the repository's required gates without inventing extra approval or artifact requirements.

Present the framing and tradeoffs before a long run. Reversible authorized work proceeds (the **never-block-on-the-human** principle skill). Honor agreed checkpoints and report meaningful progress during multi-hour work; ask for a decision only when the user needs to make one.

## Phase B: Design the workflow

Decompose into atomic, independently-landable units. Sequence riskiest-unknown-first. Scaffold and verification come before features (the **foundational-thinking** principle skill).

- Choose verification before the work. Reuse existing checks, capture a pre-change baseline when the comparison matters, and build a new harness only when the question needs one.
- Use [architect](../../code/architect/workflow.md) for consequential design decisions. It routes large or contested designs to [arena](../arena/workflow.md); skip competing candidates for a settled mechanical change.
- Decide what fans out. Parallelize only across seams, with bounded native child tasks and distinct allowed output paths or registered worktrees through installed [pr-worktree](../../pr/worktree/workflow.md) (the **separate-before-serializing-shared-state** principle skill). A branch name alone does not isolate a shared checkout.
- Write the designed phase list down. That list is what the human reviews.

Execute only the authorized scope; a plan-only request stops at the workflow. Add concrete steps to the checklist between the Phase C and Phase D entries. Run each under the Phase C loop discipline, and weave the Phase D log through them, a row as each step lands, rather than saving the whole trail for the end.

## Phase C: Run the loop

Each unit is an experiment. State the hypothesis, make the smallest change, measure against the predicate on the real artifact, keep it if it advanced, revert it if it didn't. Apply the **sequence-verifiable-units** principle skill, verifying each unit before starting the next instead of batching checks at the end.

- Verify by inspecting the artifact, never a self-report. When something passes too easily, suspect the observation method before the system.
- Inspect delegated artifacts and cited evidence yourself. Use a separate judge only when requested or justified under the runtime contract. If a check measures the wrong behavior, correct it explicitly rather than weakening it to obtain a pass.
- A verdict is VERIFIED, NOT VERIFIED, or INCONCLUSIVE. Inconclusive is not a pass. Don't hide a negative.

## Phase D: Keep the audit trail

Use the [decision log](../decision-log/workflow.md) for consequential choices in an external run directory. Keep one writer for any checkpoint: scope, unit dependencies/owners, exact artifact/head, actual checks, known child/process handles, blockers, and next action. Reconcile those facts at a phase boundary or restart; saved task IDs do not resume private agents. A useful log may accompany a review, but committing or publishing it requires authorization. Use [Pause safely](../../../playbooks/coordinate/pause-safely.md) when work must stop. No schedule or persistent execution is implied.

## Phase E: Verify and hand back

Check the whole against the Phase A predicate on the real product, not just the harness. Encode any recurring correction as a gate, a lint rule, a check, or a script (the **encode-lessons-in-structure** principle skill).

**Reply:** the playbook you designed, the rigor level and why, what's verified against the predicate, and what's still open. Include a decision-trail or plan path only when that artifact was authorized and actually created.
