---
name: draft
description: "Draft publishable content from material fragments or raw input into platform-appropriate copy — tweets, HN posts, long-form articles, or blog posts. Use when the user wants to write/draft/compose a tweet, HN post, blog post, or any social content; or when material review produces a draft frame ready for final copy. Triggers: draft, write a tweet, 写推文, draft a post, compose content, 成稿."
---

# Draft

Turn material fragments or raw input into platform-appropriate, publishable copy.

## Pipeline Position

```
material (capture) → draft (this skill) → rewrite (去AI味, optional) → publish
```

draft receives either a draft frame from `material` (selected fragments + suggested angle + platform) or direct user input. It produces final copy ready for the user to review and publish.

## Core Principles (All Platforms)

### Tone: Honest Engineer

- Write like an engineer sharing findings with peers, not a founder pitching.
- Concrete numbers over vague claims. "4752 tokens → 15" beats "dramatically improved."
- If something is rough, incomplete, or has caveats, say so directly.
- Readers trust candor. Acknowledge what you don't know.

### Anti-Patterns (Do NOT Do These)

- Marketing language: "revolutionary", "game-changing", "seamless", superlatives.
- Changelog dumps: listing features bullet by bullet without narrative.
- Overly polished copy that feels generated rather than lived.
- Broad claims without supporting data.
- Em-dashes in Chinese text; the user finds them unnatural.

### Anti-AI-Smell Constraints

Apply these during drafting, not after. Do not produce an AI-smelling draft and expect `rewrite` to fix it.

- No meta-analysis scaffolding in the prose. Do the analysis internally, write the concrete result.
- No repetitive contrast frames (`不是 A，而是 B` used more than once).
- No generic engineering nouns that make the text sound more systematic than the source.
- No empty polish: broad claims, corporate politeness, decorative transitions.
- No dramatic verbs where a factual statement is enough.
- No teaching tone: over-defining concepts, overusing `也就是说` / `换句话说`.
- No quotation marks used only for emphasis.

### Structure: Problem → Investigation → Finding → Takeaway

The strongest structure for technical content:

1. **Hook**: a concrete problem or surprising observation (one sentence).
2. **Investigation**: what you checked and ruled out. Show the dead ends.
3. **Finding**: the actual cause, with data. The gap between expected and actual is the most interesting part.
4. **Takeaway**: a generalizable lesson others can apply.

If the content doesn't fit this structure (opinion, resource recommendation, tool comparison), adapt — but always lead with something concrete.

## Workflow

### Step 1: Identify Source and Platform

- What's the source? (material draft frame, raw user input, a specific experience)
- What's the target platform? Ask if unclear. Default to the platform the content fits best.
- Read the platform reference for format constraints and audience expectations.

### Step 2: Extract the Core Fact

- What is the single most interesting, verifiable fact?
- What number or observation would make a reader want to save this?

### Step 3: Draft

Apply core principles + platform-specific constraints from references:

- `references/hn.md` — Hacker News (Show HN, comments, audience)
- `references/twitter.md` — Twitter/X (length, pacing, threads, bilingual)
- `references/longform.md` — Blog posts and articles

### Step 4: Self-Review

Before showing the draft:

- Does every claim have supporting evidence (number, code path, test result)?
- Is the tone honest, not promotional?
- Does it avoid the anti-AI-smell patterns listed above?
- Would the user's voice say this? (direct, concise, slightly opinionated, no filler)

### Step 5: Output

Present the draft ready to paste. For bilingual content (English + Chinese), put the primary-language version first. Flag any claims that are `unverified` or `hypothesis` — the user should decide whether to include them.

Suggest `rewrite` as an optional next step only if the draft still feels rough.

## Language

Match the target platform's primary language:

- HN: English main + Chinese summary for user review.
- Twitter: match user's account language (Chinese-dominant with English terms is fine).
- Longform: match user's preference.

Preserve canonical code names, commands, file paths, API names, and technical terms in their original form.
