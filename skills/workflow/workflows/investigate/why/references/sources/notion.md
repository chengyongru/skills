# Notion Docs

## What this source contains

- PRDs (product requirement documents)
- Technical specs and RFCs
- Architectural decision records (ADRs)
- Meeting notes from design reviews
- Team pages with domain context
- Postmortems from incidents
- Runbooks that may explain defensive code
- Strategy documents that set priorities

Notion is where "why" often lives in long-form before it becomes code. A significant feature usually has a doc.

## How to search it

Use an actually exposed authorized Notion read connector and its schema. If unavailable, report a gap rather than inventing API names or initiating authentication. Bound searches to the permitted workspace/topic/time range; do not create, edit, share, or comment on pages.

1. **Search through the connector's actual page-search operation.** Use its supported scope/date filters and try:
   - The feature name
   - Key symbols / class names from the target code
   - Author handles (design docs are often authored before the code lands)
   - Error strings or user-visible terms
   - Time-bounded queries if you know when the code shipped
2. **Read candidate pages by exact returned reference.** Use supported page/block reads and pagination. Rationale can be buried mid-document; label unavailable sections rather than pretending a preview is complete.
3. **Follow relevant in-source backlinks and child pages.** Stay within authorized scope. Alternatives, appendices, and implementation notes can contain the actual decision.
4. **Check related databases and meeting notes only if supported.** Use actual read/query operations and bounded filters; missing database access is a gap, not an empty result.
5. **Search authorized author-specific workspaces only when in scope.** Do not expand into personal/private spaces because a PR author's name is known.

## What good evidence looks like here

- A PRD with a "Problem statement" or "Motivation" section that matches the target code's purpose
- An "Alternatives considered" or "Rejected approaches" section
- A postmortem that names the target code as the fix for a specific incident
- Meeting notes that record "we decided X because Y" and tie to the same author/date range as the PR
- An ADR template filled out non-trivially (status, context, decision, consequences)

## Common pitfalls

- **Outdated docs.** Specs are often written before implementation and not updated. The doc may describe a plan that changed. Cross-check against the actual PR.
- **Doc vs. reality drift.** A spec may say "we'll do X" but the code actually does Y. Flag the divergence. The synthesizer will surface the contradiction.
- **Boilerplate templates.** Some orgs require a "Why" section that gets filled with fluff. Look for specificity.
- **Unlinked docs.** The most relevant doc may not be linked from anywhere. Broad keyword searches help.
- **Multiple drafts.** If a topic has multiple docs, find the one that was finalized or most recently updated. Check dates.
- **Access-restricted pages.** If you can't access a page, note it as a gap.

## What to return

For each relevant doc:
- Title and URL
- Authors and last-updated date
- The motivation text (verbatim quote), with page/section location
- Relevant linked pages (so the synthesizer can cite them)
- Whether the doc was finalized or draft
