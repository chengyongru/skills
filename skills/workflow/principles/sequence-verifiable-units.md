# Sequence work into verifiable units

Order work as small, coherent units: known baseline, one scoped change, a meaningful check, then advance. Run the check even when a tool made the edit. Preserve existing dirty work and do not reset or rebase to manufacture a clean baseline.

Deliver in the order that explains the result: failing check before the fix, subtraction before reshaping, baseline before treatment. Demonstrate red-then-green locally without requiring a published broken commit. Each independently delivered unit meets its contract; coupled migration steps stay isolated until their agreed boundary is verified.

Refresh affected proof when the head, base, or a dependency changes. Unchanged patch text is not enough. Report a blocked unit rather than checking it off on inference. Commits, pushes, PRs, and landing remain conditional on authorization.
