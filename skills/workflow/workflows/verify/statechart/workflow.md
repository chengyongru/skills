# Statechart

Use for `$workflow statechart`, a stateful protocol, a concurrency question, or a bug best explained as a path through states. Check a TLA+ model with TLC, then show its behavior and counterexamples as Mermaid. This is optional proof for the named question, not a gate for every change. Keep the user's scope and [runtime contract](../../../references/runtime.md).

## Frame the property

State the user-visible promise and the harm if it breaks. Name the source snapshot, covered code, model bounds, assumptions, and omitted behavior. Each modeled atomic action must match a genuinely indivisible operation; split at yields, awaits, transactions, or concurrent access where another actor can intervene. A hand-written model does not read or prove the implementation automatically.

Prefer a small finite model that exposes the relevant interleavings. Use `INVARIANT` for safety and `PROPERTY` for temporal behavior. State fairness assumptions for liveness; do not add fairness or tighten a constraint just to remove a counterexample. Preserve the original property when it fails.

## Run

1. Read [tool setup](references/tools.md). Use the existing supported Node, Python, and Java. TLC is pinned; dependency downloads require the task's authorization and stay in an explicit external cache. Missing tools are blocked, not a pass. Do not install or alter persistent environment settings automatically.
2. Work in an authorized target-repository verification directory or a task-owned scratch directory. Keep specs, views, output, and generated verifier skills out of the installed plugin. For investigation, use disposable artifacts rather than changing product code.
3. Write the spec and config; read [model and chart semantics](references/model-and-view.md) before choosing constraints, deadlock behavior, or labels. A view is executable JavaScript/TypeScript, not inert data: inspect it before running and use only authorized code.
4. Resolve this leaf's absolute path and run with an explicit target workdir:

```text
node --disable-warning=ExperimentalWarning <skill>/scripts/statechart.ts SPEC.tla --config SPEC.cfg --out <external-new-output-dir> --timeout 120
```

`TLA2TOOLS` names the reviewed JAR. `JAVA` and `STATECHART_PYTHON` optionally name executables. `JAVA_ARGS` is an optional JSON array of JVM or wrapper arguments, not shell text. Add `--view FILE` for reader-facing labels. `--cancel-file FILE` cancels when a task-owned file appears; console SIGINT/SIGTERM also stop the run. Use a new output folder for each run. The launcher owns its child processes and removes only its scratch directories, including after timeout or parent exit.

## Interpret and hand back

- Exit `0`: the configured checks hold in the explored model. Exit `1`: at least one rule breaks. Exit `2`: setup/checker failure; `124`: timeout; `130`: cancellation; `143`: SIGTERM. Only `0` and `1` publish `report.md`, raw TLC output, and a chart when available. This requested verification output is a tool artifact, not permission to create a separate prose report.
- Read every rule's outcome, including **Rules not checked**. Partial exploration, a bound reached, unavailable tooling, or an error never establishes that unchecked properties hold. Record tool version, command, spec/config/view hashes, bounds, and exact source snapshot with the result.
- Show `chart.mmd` as Mermaid. For each failure, give the property in plain words and the reported action sequence. Temporal failures may include an infinite loop, not just a finite bad state. Explain any coarsened labels or hidden steps. The chart is a projection of the model, not extra proof.
- When the model describes code, replay each counterexample against that code through a test or supported interface. A step that cannot occur is evidence of a modeling mismatch. Do not call a model counterexample a confirmed product bug until the correspondence is established. Never modify product code merely to make the check pass.
- State what remains outside the model or bound. A pass is not an unbounded theorem or proof of the entire application; keep the repository's required tests and live acceptance.

For an image, use the optional local [rendering reference](references/render.md). For a reusable project check, use [Create formal verification](../../authoring/create-formal-verifier/workflow.md); keep it current with [Maintain formal verification](../../authoring/maintain-formal-verifier/workflow.md).
