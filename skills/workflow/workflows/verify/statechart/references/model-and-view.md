# Model and chart semantics

## Write the spec

Write each agreed state rule as an `INVARIANT`, adding the variables needed to express it. Put the actions in a disjunction in `Next`, such as `YouPressPlay \/ YouPressStop`; otherwise TLC may name every step `Next`. Temporal requirements use `PROPERTY`, with justified fairness and a finite state space.

A state without an outgoing action violates `NoDeadlock`, even if it represents a legitimate end. When a configured rule already uses that name, the deadlock rule is named `CHECK_DEADLOCK`. Model an explicit terminal stutter, such as `Done == phase \in {"paid", "failed"} /\ UNCHANGED vars`, only where the intended system may correctly stop. Do not hide a real deadlock with an unconditional stutter. State explicitly if deadlock checking is excluded.

Keep constants small enough to exhaust the reachable state space. A constraint defines the scope of the check, not a repair for a failure. An unbounded model can run until the launcher's timeout without establishing a result.

## Choose the view

A trusted view module may export `state(vars)`, `step(action, from, to)`, `group(vars)`, `colors`, and `title`. It executes code with the caller's permissions. Use only inspected or task-generated views; it is not a sandboxed expression language.

- `state()` returning a string gives a flat chart; an array gives parent states; an object gives parallel regions, one per key. Use reader-facing labels rather than implementation variable names.
- In `vars`, a TLA+ sequence is an object with keys starting at 1; sets are arrays.
- `step()` returns the arrow label. Give actions with the same reader-visible result the same label so they can share an arrow. Use a condition in brackets when needed. In a regions chart, conditions on other regions are generated automatically; custom brackets replace them, so do not accidentally erase a cross-region condition.
- `group()` names a phase. `colors` maps phases to `blue`, `orange`, `purple`, `yellow`, `teal`, `tan`, or `pink`. A chart state combining different groups gets no group color. `title` is a string.
- `state()` and `group()` run at most once per model state, and `step()` once per model step. Make each depend only on its arguments; chart and report share those results.

A step remaining inside one label is not drawn. Split the label when the reader must see that step. Aim for a readable chart, roughly 20 arrows or fewer, by merging only states whose omitted details do not change the explanation. Keep every bug-path state and mark. Do not merge states that break different rules or turn a precise `breaks` state into a vague `mayBreak` mark just to shorten the graph.

Returning `null` from `step()` hides steps. Keep every chart state reachable from a start, retain an outgoing arrow wherever the model has one, and hide all model steps represented by an arrow or none of them. Hiding only some narrows its displayed condition. State what was hidden when handing back the chart.

## Read the report

`breaks` marks states violating a rule; `mayBreak` means only some model states represented by that label violate it. The legend identifies rules; when one mark covers multiple rules, explain which state breaks which rule. Parallel-region marks describe combinations, not proof that each region alone causes the failure.

The chart exploration continues past violations, so states after a bug can appear. `VIEW` and `SYMMETRY` can merge concrete states into one representative; an arrow can reach the representative rather than the concrete successor. Preserve the report's warning when that occurs.

TLC checks rules in a successor beyond `CONSTRAINT` or `ACTION_CONSTRAINT`, but does not explore that successor or check its deadlock. The chart includes such a state/step when it ends a reported shortest counterexample, not all states outside the bound. A constrained-out deadlock therefore remains unchecked. These constraints are part of the proof scope.

The checker first runs the config as written with one worker. After a failing rule it reruns without that rule to identify other failures. Reruns after an incomplete first exploration are limited to 100,000 distinct states. A bound or error leaves affected rules under **Rules not checked**; the chart does not mark those rules, and absence of a mark is not a pass. Checking them may require a separately explained smaller model or a config isolating the remaining properties. The wrapper module used for the bound can change variable ordering and which temporal counterexample TLC finds.

`tlc.out` retains the first run's output. Additional `tlc-RULE.out` files preserve property traces and violations not represented in the chart. A repeated first TLC warning may appear only once in this captured output. Syntax and semantic errors are reported with SANY's source locations rather than a Java stack trace.

The chart budget is 500 states. Above that, only paths to violated rules are drawn; if no rule breaks there is no `chart.mmd`. The report still contains the state count and results. Temporal counterexamples can repeat a cycle forever (`repeats`), while `bugPath` highlights the finite path leading to a violation. Do not describe a liveness cycle as a finite safety failure.
