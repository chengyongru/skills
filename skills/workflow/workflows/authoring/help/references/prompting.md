# Word the prompt

State intent and a falsifiable check for done. A playbook supplies the ordinary steps; a few concrete sentences are usually better than a speculative implementation spec.

## Put in

- The goal: what is wrong or what the user wants.
- The done check: something that can pass or fail, not just "make it better" or a duration.
- The proof: real command output, a captured user flow, stored value, or a measured before/after.
- Known evidence: symptom, reproduction, log, source path, or relevant link.
- Real constraints: "repro only", "do not edit code", "zero behavior change", a named base, and "stop before implementation" each change the permitted work.
- Side-effect boundaries: whether commits, remote updates, publication, messages, deployment, and ticket changes are authorized. A generic "finish it" is not a substitute for these boundaries.

## Leave room for investigation

- Prefer the outcome over an untested theory of the implementation. Keep explicit safety, scope, and acceptance constraints intact.
- Avoid listing every skill or forcing a guessed sequence. Name a skill when deliberately choosing its output.
- Separate an assumed cause from the observed problem so the agent can test alternatives.

## Load context first

- Ask for the underlying issue in plain words before work if the report is noisy.
- In a fresh chat, `$workflow recall` can recover relevant prior work using bounded session search. Give a topic, workspace, and time range; do not ask for raw transcript mining.
- Before unfamiliar code changes, `$workflow how` traces mechanics and `$workflow why` investigates reasons.
- Ask `$workflow teach` to explain why a choice addresses the cause rather than the symptom. Preserve uncertainty when evidence is incomplete.

## Design before a long plan

- Compare a few concrete options instead of accepting the first plausible shape. UI prototypes need actual captures, not generated fake screenshots.
- Let prototypes answer open questions; an abstract adversarial review can invent unreachable risks.
- For a shared API, ask for a README-style usage sketch first, then derive the types and implementation.
- Plan after the shape is settled. Each unit ends with a real check; a plan-only request stops at the plan.

## Follow up briefly

- "Do it" or "continue" can continue an already authorized scope; it does not expand permissions or resume a private child by conversation ID.
- Say "new task" when the subject changes, and invoke `$workflow` for the new turn if wanted.

## Before stepping away

- State the bounded task and done predicate, the allowed local workspace/worktree, and where a decision trail should live.
- State which user-owned decisions are pre-approved and which actions must wait. Do not grant commit/push/merge permission accidentally through a copied example.
- Give a budget/exit condition: on a real blocker or the session's limit, stop and leave evidence, known resource handles, and a next action outside the plugin.
- For a timed or recurring job, request `cron` with an explicit interval, task scope, and stop condition.

## Steer in one line

- "The goal is to reproduce. I did not ask for a fix yet."
- "Apply prove it works. Show the real output, not only the build log."
- "Keep the uncertainty. Which claims have direct evidence?"
- "Stop at a local patch. Do not commit, publish, or send anything."

A named principle steers a decision; it does not override scope or native skill policies. `$nanobot-gate` requires its literal invocation, not a generic request for rigor or verification.
