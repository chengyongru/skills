# Selection Guidance

Use this reference when choosing the next action from idea notes.

The job is not to rank ideas. The job is to choose the one action most worth doing now.

## What Makes A Good Next Action

A good next action changes state quickly. It should move at least one important thing from:

- unknown to known
- blocked to unblocked
- draft to reviewable
- failing to diagnosed
- unreviewed to reviewed
- vague idea to concrete artifact
- private uncertainty to external feedback

Prefer actions that create new information, unblock other work, or make a decision easier. Avoid actions that merely feel important but leave the situation mostly unchanged.

## Decision Core

For each serious candidate, form a short internal thesis with three parts:

- the action
- the specific evidence that makes it worth doing now
- the state change it should create

Choose the candidate whose thesis is most concrete and useful. A strong thesis has:

- a clear current state from the note
- concrete evidence, not just labels
- an immediate state change
- a realistic first probe
- a reason it matters today, not someday

If no candidate has a strong thesis, choose the action that best improves the evidence base: inspect the source, reproduce the failure, read the diff, ask for review, or clarify the user goal.

## Compare Candidates

Compare candidates in this order:

1. **Readiness**: Can the next action actually be taken now, or is the blocker too vague?
2. **State change**: What will be different after doing it?
3. **Leverage**: Does it unblock people, reviews, merges, future ideas, or user-visible progress?
4. **Evidence**: Is there concrete support in the note or source?
5. **Delay cost**: What gets worse if this waits another day?
6. **Effort fit**: Is the first probe small enough for the user's current context?
7. **Confidence**: Is the action likely to produce signal rather than churn?

Use `cost`, `impact`, and `confidence` as hints only. Do not calculate a score. The best next action is often not the highest-impact idea; it is the highest-leverage state change available now.

## Tie Breakers

When multiple candidates look good:

- Prefer an item waiting only on review/ready state over one needing redesign.
- Prefer a failing check with a clear first log to inspect over a broad conflict.
- Prefer an action that closes or externalizes an open loop.
- Prefer a small action that unlocks a high-impact cluster over a large action inside the same cluster.
- Prefer current user/project context over stale backlog value.

When the user is choosing under low energy or limited time, bias toward a concrete probe that produces information. When the user is choosing a main work block, allow medium-cost actions if they unlock larger value.

## Use Related Links

`related` links matter only when they change the choice:

- A candidate may be better because it unlocks several related notes.
- A candidate may be worse because a related note should be resolved first.
- A cluster may reveal the real next action is not in the most attractive note, but in the bottleneck note.

Do not mention the graph unless it affects the recommendation.

## Candidate Set

Consider `open` and `doing` notes unless the user asks otherwise. Prefer current project context if the user mentions one.

If the top candidates lack evidence, blocker, next action, cost, impact, or confidence, do at most three small source lookups total. Then decide with the available evidence.

## Response

Answer naturally in the user's language and tone. Do not hard-code section labels, headings, or a fixed sentence order.

The response should still make three things clear:

- the chosen action
- the concrete reason, grounded in the selected note's evidence/current state/blocker
- the first next step

The reason must explain the state change. Bad: "high impact and low cost." Good: "checks are already green and the only blocker is review, so marking it ready converts a finished fix into external feedback."

Do not mention rejected alternatives unless asked. Do not include time boxes, reselect conditions, or rankings unless asked.
