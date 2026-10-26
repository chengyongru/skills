# Example task prompts

Substitute the actual target, scope, and completion check.

```text
$workflow triage this PR. Explain the problem, main risk, and next action; no local checkout or publication.
$workflow how does this subsystem work? Show state ownership and the actual callers, without editing.
$workflow why did this behavior change? Limit the search to this repository and the linked issue.
$workflow fix this reproducible defect in an isolated branch worktree; verify the public behavior. No commit or push.
$workflow architect this change with a checkpoint. Stop at the design before implementation.
$workflow simplify the current diff while preserving behavior, then run the focused checks.
$workflow review PR 123 at SHA <sha>. Do not normalize my dirty worktree or publish a review.
$workflow verify this project's settings flow in an isolated test instance; preserve the running application.
$workflow revise this README, preserving its exact commands and compatibility conditions. Do not publish.
$workflow compare two bounded candidate approaches; same-model views are acceptable. Do not deploy.
$workflow recall our work on this branch, reconcile actual state, and report only the next unfinished step.
$workflow reflect on this conversation and propose workflow improvements; do not edit the plugin, profiles, or tracker.
```

Name external operations and targets explicitly when requesting them.
