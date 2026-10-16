### Perf issue

**Own the workload, measurement, and causal explanation.** A performance investigation stays read-only; implementation, disruptive profiling, and live-state changes require the appropriate scope.

1. Reproduce the user's complaint on the real supported surface with a representative workload. Capture a baseline at the exact source/runtime version. Use the target project's driver or verifier, or [verify](../../workflows/verify/public/workflow.md) for the measured public surface. Vet measurements with [benchmark-checklist](../../workflows/verify/benchmark/workflow.md): work/error counts, warmup/cache conditions, repetitions/spread, comparable inputs, and the bottleneck. If no safe capture is available, report the gap instead of claiming a ceiling from source inspection.
2. Ground hypotheses with [how](../../workflows/investigate/how/workflow.md) and the trace. Try the performance mantras in order, cheapest first:
   1. Do not do work whose result nobody uses.
   2. Do it, but do not do it again.
   3. Do it less.
   4. Do it later.
   5. Move it off the user's critical path.
   6. Do it concurrently when ownership permits.
   7. Do it cheaper.
   Stop when an evidenced in-scope change meets the target.
3. Plan the fix from the observed mechanism, using [architect](../../workflows/code/architect/workflow.md) for a consequential design boundary. Implement directly or delegate a bounded attempt when permitted, with explicit worktree/paths, prohibited external actions, and proof. Do not specify a model or require a cloud worker. Keep one hypothesis per verified unit and one writer per branch.
4. Rerun the same workload and regression gate after the change. Interleave base/head measurements when noise matters. If base lacks the new behavior, report that and use an absolute budget for the added work/end-to-end result rather than a ratio between unlike scenarios. Preserve rejected evidence; do not retain a tweak that merely "might help" or weakens correctness.
5. Reduce large captures with existing readers or bounded read-only analysis. Derived output belongs in an owned `.nanobot-workflows/runs/<run>/` evidence directory when needed. Do not require dumping every artifact into a database or writing a parser for a small diagnosis. Explain what limits the result and distinguish measured numbers from causal hypotheses.
6. Commit and follow Opening a PR only when authorized. If publication is in scope, cite the meaningful baseline → result, units, workload, and linked evidence. No unsolicited push, merge, schedule, or infrastructure repair follows a performance win.

For a series of authorized attempts against a metric, use Hillclimb with an explicit budget. A long task does not create persistence after this turn; user-timed follow-ups use `cron` at the requested cadence.

**Reply:** workload and target, baseline/result with units and spread, delta, correctness check, measured mechanism, exact artifact/head and evidence paths, and any blocked proof.
