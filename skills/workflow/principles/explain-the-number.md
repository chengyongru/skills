# Explain the Number

- **Ask "why not double?"** Investigate the resource or code path that bounds the result, such as a core, lock, disk, network, or the load generator itself. Use an authorized profile or counters from the run and map them to source. A guess from code is not a measured limiter. If the limiter is unknown, report the number as an observation with that limitation, not a proven causal explanation; do not mutate live state merely to obtain a profile.
- **List what else the number could be measuring, and rule out each one with evidence.** The usual suspects are errors, skipped or cached work, code that never ran, an untuned side (one left on default settings), noise, and a piece too small to matter end to end.
- **Keep the evidence with the number.** Record workload, exact artifact/head, actual command or procedure, run count, spread, error/completed-work counts, and measured limiter or uncertainty. Use an external task-owned evidence path when a file is useful; read-only analysis need not create one. Never imply that a same-model trial is a cross-model result or compare unlike scenarios as a speedup ratio.

For a performance number, run the full procedure with the [benchmark-checklist](../workflows/verify/benchmark/workflow.md) skill. For an eval result, ask the same of the trials: did every run do the task, does the gap hold across trials and models, and does the scenario matter.

An explained-improvement claim is unsupported when it omits run count/spread, leaves a proposed limiter unmeasured, or claims more time saved than the changed work consumed. Raw observations can still be reported with those limits; do not promote them into a causal conclusion.

Distinct from [Prove It Works](prove-it-works.md), which checks that an output is real.
