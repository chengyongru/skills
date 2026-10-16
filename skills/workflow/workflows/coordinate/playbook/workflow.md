# Figure it out

When the task matches no playbook, design one. The deliverable before any code is the workflow itself: a sequence of phases that scales rigor to the task, runs the scientific method, and leaves a decision trail a human can audit after stepping away.

## Start

Keep a short checklist for the phases below. Select only decision-relevant guidance from the [principles reference](../../../references/principles.md), rather than loading the entire catalog. Present the designed workflow in the conversation; save a prose plan only when the user requests a persisted artifact. Keep any authorized run artifacts outside the installed plugin.

## Phase A: Frame

Ground first, then commit. Don't start the run until you can state:

- The definition of done as a falsifiable predicate (the **prove-it-works** principle skill).
- Scope, quantified: rough units and effort, plus the blockers grounding surfaced.
- The rigor level, biased high. One-way doors and high blast radius get more. Reversible low-stakes steps get less. Rigor is gates and artifacts, not "try harder".

Present the framing and tradeoffs before committing to a long run. Reversible work proceeds (the **never-block-on-the-human** principle skill), but a multi-hour run earns one checkpoint.

## Phase B: Design the workflow

Decompose into atomic, independently-landable units. Sequence riskiest-unknown-first. Scaffold and verification come before features (the **foundational-thinking** principle skill).

- Build the verification harness before the work, with the baseline captured from the pre-change state, so the check reads as "old value vs new value".
- For one-way-door design decisions, run the [architect](../../code/architect/workflow.md) skill (it runs [arena](../arena/workflow.md)). Skip it for mechanical work whose shape is already concrete. A second arena over a settled design is over-engineering (the **laziness-protocol** principle skill).
- Decide what fans out. Parallelize only across seams, with bounded native child tasks and distinct allowed output paths or registered worktrees through installed [pr-worktree](../../pr/worktree/workflow.md) (the **separate-before-serializing-shared-state** principle skill). A branch name alone does not isolate a shared checkout.
- Write the designed phase list down. That list is what the human reviews.

Execute only the authorized scope; a plan-only request stops at the workflow. Add concrete steps to the checklist between the Phase C and Phase D entries. Run each under the Phase C loop discipline, and weave the Phase D log through them, a row as each step lands, rather than saving the whole trail for the end.

## Phase C: Run the loop

Each unit is an experiment. State the hypothesis, make the smallest change, measure against the predicate on the real artifact, keep it if it advanced, revert it if it didn't. Apply the **sequence-verifiable-units** principle skill, verifying each unit before starting the next instead of batching checks at the end.

- Verify by inspecting the artifact, never a self-report. When something passes too easily, suspect the observation method before the system.
- Pair delegated work with a judge. If a worker games the gate, reset and harden the contract. If the gate itself is wrong, fix the gate in its own change rather than routing around it.
- A verdict is VERIFIED, NOT VERIFIED, or INCONCLUSIVE. Inconclusive is not a pass. Don't hide a negative.

## Phase D: Keep the audit trail

Log the run via `$workflow show-me-your-work` in the external run directory. The trail plus the diff lets the human audit the work after stepping away. Propose including the trail in a review when useful, but commit or publish it only when authorized. A long run remains bounded by the current session; no schedule or persistent automation is implied.

## Phase E: Verify and hand back

Check the whole against the Phase A predicate on the real product, not just the harness. Encode any recurring correction as a gate, a lint rule, a check, or a script (the **encode-lessons-in-structure** principle skill).

**Reply:** the playbook you designed, the rigor level and why, what's verified against the predicate, and what's still open. Include a decision-trail or plan path only when that artifact was authorized and actually created.
