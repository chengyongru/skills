# Explain the Number

- **Write the decision before running.** Name the smallest result that would change it, the noise floor, and a bounded trial plan. If spread exceeds the effect, report inconclusive instead of adding runs until a preferred result appears. A requested ballpark can state its purpose without inventing a decision threshold.
- **Ask why not double.** Identify the limiting resource or code path with authorized profiles or counters from the run. A code-based guess is not a measured limiter; report that uncertainty with the observation.
- **Rule out other explanations.** Check errors, skipped or cached work, code that never ran, an untuned side, noise, and work too small to explain the end-to-end result.
- **Keep the evidence with the number.** Record equivalent workloads, exact artifacts/heads, the procedure, run count, spread, completed/error counts, and limiter or uncertainty. Same-model trials are not cross-model proof.

For performance, use the [benchmark checklist](../workflows/verify/benchmark/workflow.md). For evals, check that every run did the task, the gap holds across the tested trials and models, and the scenario matters. Distinguish an observation from a supported causal improvement claim.
