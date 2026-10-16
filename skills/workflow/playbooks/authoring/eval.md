### Eval

**Own the experiment design, blinding, and evidence limits.** Evaluate an authorized variant; do not claim an unavailable model comparison or inspect private traces to manufacture compliance evidence.

#### Blinding

- Give candidates the same organic task, fixtures, permissions, and effort boundary. Hold the scoring rubric back from them.
- Keep experiment labels and variant/model names out of candidate-visible project names and prompt text when that would bias results. Use neutral project-shaped labels. Do not remove safety constraints or conceal the user's authority boundary for the sake of realism.
- Ask for normal deliverables and concise design notes, not hidden reasoning or a list of which instructions the candidate followed.
- A judge sees outputs under neutral labels and one fixed rubric, not model/variant identities. When comparing two sets, score both on that rubric in a single bounded pass.

#### Steps

1. State the question, variants, success criteria, permitted effects, trial count, and session budget. Write three to six observable scoring criteria before seeing results. An explicitly cross-model experiment is blocked if no supported model-selection interface exists. Nanobot children use the runtime-configured model; separate children are same-model trials, not different model families.
2. Prepare isolated candidate worktrees or disjoint task-owned fixture directories. Use installed [pr-worktree](../../workflows/pr/worktree/workflow.md) for branches. Keep the rubric and identity mapping outside candidate write scope under `.nanobot-workflows/runs/<run>/`. Candidates cannot change the fixture or rubric to pass. A read-only evaluation uses existing outputs and does not require file generation.
3. Run bounded native children only when permitted, normally at most two concurrently; otherwise conduct a single-session/serial evaluation and disclose the reduced independence. Give the organic task plus explicit allowed paths, prohibited publication/external actions, actual reference paths, and the expected artifact/report. Do not pass model, reasoning, agent-type, or environment fields.
4. Await completion notifications. Inspect known task state with `check` when needed; clarify with `send`. Diagnose a failure before a bounded retry. To replace a writer, cancel where necessary and reconcile final task/process state before starting another. A silent candidate is not automatically stuck.
5. Judge the neutral outputs against the fixed rubric, with a separate bounded child only if useful and allowed. That judge is still same-model unless an actual supported interface proves otherwise. Keep the judge's verdict separate from direct behavioral verification.
6. Inspect every output and run the relevant reachable acceptance checks. Use authorized tool receipts, artifact content, and reported commands as leads to verify. Do not glob transcript directories or infer hidden instruction-following. If relevant prior-session evidence is needed and available, use exact `search_sessions`/`read_session` references within scope; missing traces mean that aspect was not measured.
7. Synthesize the observed quality, variance, errors, coverage, and budget. Investigate disagreement rather than assuming the judge is right. Use [benchmark-checklist](../../workflows/verify/benchmark/workflow.md) when reporting quantitative results. A few successful same-model trials do not establish broad model-family superiority.

Promotion, installation, plugin edits, publication, or scheduling requires separate user scope. Preserve useful evidence outside the plugin; do not update private memory or live skills as an automatic result of the experiment.

**Reply:** question/variants, actual runtime/model if known, rubric, trials and evidence, per-output results, judge verdict if used, synthesis, limitations, and recommendation. State blocked cross-model or unmeasured compliance requirements explicitly.
