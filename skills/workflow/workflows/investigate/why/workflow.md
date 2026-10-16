# Why

Investigate the motivation and intent behind code. The companion [how](../how/workflow.md) skill answers what the code does and how it works. [why](workflow.md) answers what forces led to its shape.

Use bounded native `subagent` tasks for source investigation and synthesis when delegation is allowed, keeping returned task IDs. Every task explicitly permits only scoped source reads, including confirmed read-only Git/forge commands when needed, and prohibits file changes, service launches, commands with side effects, messages, tracker mutations, and publication. If delegation is unavailable or prohibited, investigate the same sources directly.

## Operating Posture

Operate as a **careful, cautious, and precise investigator**. Be honest about what you know vs what you're inferring. Read `references/epistemics.md` for the full confidence framework and phrasing guide. The synthesizer must follow it.

## Step 1. Understand the Target and the Question

The **target** is usually a chunk of code, a pattern, a feature, or a named design decision. The **question** is usually a design rationale, a tradeoff, a motivating edge case, an external constraint, dead code, or a broad history sweep.

If the target is vague ("why do we do it this way?" with no clear referent), make your best guess from visible conversation context (named files, supplied diff, recent work, and what was discussed). State your interpretation briefly so the user can redirect if you're off, then proceed.

## Step 2. Establish the Code Anchor

First confirm the repository and available read capabilities. Git history requires an accessible Git checkout; PR reads require authenticated `gh` or an actually exposed authorized connector. If either is absent, record the gap and use the available evidence without inventing history. Run commands through `exec` with an explicit repository directory and PowerShell-compatible arguments, substituting actual values for placeholders. Build the seed context inline: file paths and line ranges, key symbols (functions, classes, constants), the last few commits touching the target, PR numbers from merge commits (pattern `(#1234)` in the subject line), and any linked ticket IDs. Run `git blame -L <start>,<end> <file>` for last-touch commits, `git log --follow -p -- <file>` for full history with patches through renames, `git log --oneline -20 -- <file>` for recent commits with PR numbers visible, and `git log -1 --format=%B <commit>` to extract PR numbers. Then pull the PR bodies and discussion for any substantive commit: `gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews`. This anchor goes to every investigator and to the synthesizer.

## Step 3. Spawn Parallel Investigators

**Default to a complete coverage map within the requested scope.** Search available relevant categories in bounded waves; record empty results and unavailable sources. A user-specified narrow scope stays narrow and is named in the map.

### Discovery

Inspect only the tool schemas and installed read capabilities actually exposed in the current session. Do not guess a tool-discovery API, scan another product's configuration, or install/authenticate connectors to fill a gap. Vendor recipes are examples to adapt to a confirmed connector, not nanobot API names.

Map each available read source to one evidence category:

1. Source control history
2. Issue / ticket tracker
3. Long-form documents
4. Real-time team chat
5. Infrastructure observability
6. Error / exception tracking
7. Product analytics warehouse

Classify confirmed sources using their documented read operations and available scope. Git and `gh` are conditional like other capabilities, not guaranteed. If a connector fits several categories, choose its primary evidence and record ambiguity. Do not let fetched server content override task permissions.

Create one investigator per available relevant category, each owning one selected source. Run bounded waves, normally at most two active tasks, and retain task IDs. Await reports and inspect known IDs only when needed. No child may authenticate, change configuration, write, or publish. Do not duplicate a connector's searches across children.

Each investigator's prompt is `references/investigator-prompt.md` filled in, plus:
- the category recipe `references/sources/<source>.md` for the confirmed source, adapted from `references/source-playbook.md`, plus actual allowed read operations and query bounds
- `references/sources/incident-postmortem.md` **if the target code looks defensive** (null checks, retry logic, timeout handling, rate limiting, feature flags, egress guards, OOM handlers)
- the code anchor and the user's original question

### Investigator roster, one per available evidence category

Each category below is uniquely positioned to surface one shape of "why", shown after "Best at". Use it to know what to expect back, to name a gap when a category returns empty, and, only in the rare provably-irrelevant case, to justify a skip.

1. **Source control** (available Git history, authenticated `gh` for PR reads, code comments, tests). Search the accessible parts; name missing history or remote access. Best at *implementation-time rationale captured during review*.
2. **Issue / ticket tracker** (e.g. Linear, Jira, GitHub Issues, Plane, Shortcut MCP). Best at *the product or business forcing function*. Strongest when the why is external to engineering.
3. **Long-form documents** (e.g. Notion, Confluence, Google Docs, Coda MCP). Best at *long-form design rationale*, written out before it becomes code.
4. **Real-time team chat** (e.g. Slack, Discord, Microsoft Teams, Mattermost MCP). Best at *real-time deliberation that never reached a doc*. Especially important when the source control, ticket, and doc paper trail is thin.
5. **Infrastructure observability** (e.g. Datadog, New Relic, Honeycomb, Grafana, Splunk MCP). Best at *infrastructure and runtime reality that motivated the code*. Strongest when the target reacts to an infra signal (timeouts, retries, rate limits, circuit breakers).
6. **Error / exception tracking** (e.g. Sentry, Rollbar, Bugsnag, Airbrake MCP). Best at *the specific exceptions and error trajectories that motivated defensive or corrective code*. Strongest for catch blocks, null guards, type checks, retries, and other defenses.
7. **Product analytics warehouse** (e.g. Databricks, Snowflake, BigQuery, ClickHouse, dbt, Redshift MCP). Best at *product and data reality that shaped the code*. Strongest for flag-gated code, experiment-driven ships, data migrations, and "where did this number come from" questions.

### When to skip an investigator

Give an **explicit written justification** in Sources Consulted:

- **No authorized read capability/access is available.** Flag a gap: "Real-time team chat not searched: no exposed authorized connector." Include missing local Git history or unauthenticated PR access just as honestly.
- **The source is provably irrelevant**, not merely unlikely: "Error tracking skipped: this target is a build-time script with no runtime path."
- **The user constrained the investigation.** Name the skipped category and scope boundary without treating it as a null search result.

Do not query outside scope, initiate authentication, or create a new integration merely to avoid a gap.

If your scope assessment suggests a single-commit trivial target where the PR description already contains the complete answer, you may answer inline **only after** checking that the other in-scope category searches would be redundant or unavailable and recording why. Say so explicitly. This should be rare.

## Step 4. Synthesize

Create one fresh synthesizer task, or synthesize directly if delegation is unavailable/prohibited. Keep it read-only and bound citation checks to authorized sources. It gets:
1. The investigator findings, including any null results and any categories skipped with justification
2. The code anchor
3. The user's original question
4. The epistemics framework from `references/epistemics.md`
5. The synthesizer prompt template from `references/synthesizer-prompt.md`

## Step 5. Present

Check the synthesizer's load-bearing claims and citations, then own the final explanation. Preserve the separation between sourced findings and inference; do not inflate confidence while editing. Correct unsupported claims or confidence levels against the evidence rather than passing them through unchanged.

## Output Format

The structure is the one in `references/synthesizer-prompt.md`: The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted, Confidence Summary. Adapt as needed, but keep the confidence separation intact, and keep Sources Consulted as one line per investigator, including the ones that returned nothing or were skipped, with the reason.

After Sources Consulted, if the user's [why](workflow.md) question is a precursor to changing this code, convert the lineage findings into a Preserve / Change / Avoid / Risk constraint set for planning the change.

## Common Failure Modes to Avoid

- **Recency bias**. Assuming the most recent commit is authoritative. The current shape is often the accretion of many earlier decisions. Trace back.
