# Attack the Premise

When two or more fixes that share one premise have failed the same gate, suspect the premise, not the fixes.

**Why:** Each failed fix is evidence against the belief it assumed. A third fix on the same premise spends effort where the evidence already says the cause is not.

**Pattern:**
- **Write the premise down.** The premise is the one sentence that every failed fix assumed.
- **Test the premise before the next fix.** Find an observation that would come out differently if the premise were false. Use a safe check within the authorized scope; if it needs disruptive instrumentation or shared/live-state changes, name the proposed probe and missing authority first. Look at how the failures are distributed, not only at how large they are. Reuse a rerunnable check where useful per [Build the Lever](build-the-lever.md); a read-only diagnosis need not create a script.
- **Follow the evidence.** If it contradicts the premise, the cause is elsewhere. Look for what the failures have in common that the premise did not predict. If it confirms the premise, ask the next "why" per [Fix Root Causes](fix-root-causes.md). The earlier fixes may have treated a consequence instead of the cause.
- **Remove the condition instead of compensating for it**, per the [Laziness Protocol](laziness-protocol.md). If the evidence shows that one part always lands on the losing side, change what puts it there. A mechanism that cleans up after it leaves the cause in place and adds work on every run.

**Stop:** Do not start the next fix before the premise is stated and tested, or the missing decisive evidence is explicitly reported. A refuted premise may reveal a wider problem; that is a finding to scope, not permission to repair unrelated systems.

This principle is distinct from [Redesign from First Principles](redesign-from-first-principles.md), which rebuilds a design around a new requirement. It questions a fact the current design assumes.
