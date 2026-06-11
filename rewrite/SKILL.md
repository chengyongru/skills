---
name: rewrite
description: Rewrite and polish the user's existing Chinese technical notes to reduce AI-ish prose while preserving the original facts, structure, intent, and level of abstraction. Use when the user asks to rewrite, polish, 润色, 去 AI 味, 降低 AI 味, make a note feel more natural, or clean up an AI-assisted draft without changing its substance.
---

# Rewrite

## Goal

Polish an existing note so it feels less like an AI-generated draft and more like a clear technical note. Operate on the supplied draft instead of building a personal voice profile.

The user may have used AI to produce the first version. The point is not to make the text more decorative, but to remove the parts that create discomfort: generic structure, inflated wording, mechanical contrasts, and conclusions that sound stronger than the evidence.

## Narrative

Aim for `娓娓道来`: let the note unfold in the order a reader would naturally follow. Do not frontload the structure or announce the analysis plan; let each paragraph answer the question created by the previous one.

Do not confuse this with spoon-feeding. Assume the reader is technically competent. Explain only the missing step needed for the current argument, not general background the reader can infer.

## Scope

Rewrite conservatively.

- Preserve facts, code, links, examples, and technical claims unless the user explicitly asks for substantive improvement.
- Preserve the note's genre and narrative position. Do not turn a debugging record into an architecture review, or a rough practical note into a polished essay.
- Preserve the original level of abstraction. If the source is about a concrete debugging process, improve the process narration instead of replacing it with generic engineering vocabulary.
- Prefer local sentence and paragraph edits over full restructuring unless the current structure is the source of the AI smell.

## What To Remove

Remove or reduce common AI-ish patterns:

- Meta-analysis scaffolding in the prose. Do the analysis internally, then write the concrete factors directly.
- Repetitive contrast frames, especially when many paragraphs use the same `不是 A，而是 B` shape.
- Generic engineering nouns that make the text sound more systematic than the source.
- Empty polish: broad claims, corporate politeness, and decorative transitions.
- Dramatic verbs where a factual statement is enough.
- Quotation marks used only for emphasis.
- Teaching tone: over-defining concepts, overusing `也就是说` / `换句话说`, or summarizing what the reader can already infer.

## What To Keep

Keep the useful parts of the draft:

- Concrete observations, traces, code snippets, commands, links, and failure modes.
- Necessary English technical terms such as `PR`, `CI`, `LLM`, `parser`, `worker`, `exit`, and `exception`.
- The main engineering judgment, as long as the evidence in the draft supports it.
- Mild directness when it helps the point, but not as a catchphrase.

## Method

1. Identify the note's actual job: record, explain, review, request, or summarize.
2. Mark facts that must not change: names, numbers, commands, code, links, and causal claims.
3. Find the AI smell: over-structured framing, generic abstraction, unnatural emphasis, inflated conclusion, or repeated sentence pattern.
4. Check the flow: each paragraph should follow naturally from the previous one without announcing the outline.
5. Rewrite only as much as needed to make the note natural and technically clear.
6. Recheck that no new technical design or stronger conclusion was introduced.

## Final Check

Before returning the rewrite, verify:

- Did the text preserve the original facts and scope?
- Did it remove AI-ish scaffolding instead of adding new style rules?
- Did the explanation unfold naturally without treating the reader as a beginner?
- Did it keep concrete debugging or engineering details concrete?
- Did it avoid making the article more systematic than the source?
- Did it avoid changing the user's intended conclusion?
