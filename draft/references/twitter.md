# Twitter / X

Use this reference for single tweets, threads, replies, and quote-post commentary.

## Audience and Goal

A tweet earns attention through one concrete fact, then earns saves through a reusable insight, resource, or method. Do not treat every post as a project announcement.

For this account, prioritize:

1. Verified resources for a specific audience, with personal endorsement and a usable link.
2. Engineering findings in `problem → investigation → data → conclusion` form.
3. Reusable agent workflows, tools, and skill assets.

## Single Tweet

Prefer a single tweet when the finding can stand on its own. Structure:

```text
[Concrete hook: symptom, surprising number, or specific audience]

[What was investigated or tried]

[Actual finding + measured result]

[General takeaway]

[Link]
```

Requirements:

- Put the strongest concrete fact in the first two paragraphs.
- Include the most compelling before/after number when available.
- Keep paragraphs short and readable on mobile.
- Use Chinese naturally with canonical English technical terms.
- No hashtags unless the user explicitly wants them.
- No emoji by default.
- No engagement bait (`你怎么看`, `转发收藏`, polls without a real question).
- Do not end with administrative details after the main takeaway. The reusable conclusion should be the final thought; put the link after it only when needed.

## Thread

Use a thread only when one tweet would remove necessary evidence or make the argument unreadable.

- Tweet 1: complete hook + core finding. It should be useful even if nobody opens the thread.
- Middle tweets: investigation path, evidence, code/config snippets, caveats.
- Final tweet: reusable checklist, resource, or conclusion.
- Do not split one sentence across tweets or create a thread merely to inflate post count.

## Replies and Quote Posts

- Reply to the actual point, not the surrounding discourse.
- Quote-post only when adding a concrete observation, correction, or tested result.
- Keep social replies short. Do not turn a reply into an article.

## Evidence and Caveats

State limits when they materially change how readers should apply the finding: model/version, test setup, dataset, sample size, or environment. Keep caveats concise; do not bury the result under defensive qualifications.

## Output

Return paste-ready copy first. Follow with at most a few concise notes about evidence gaps or alternative hooks when useful.
