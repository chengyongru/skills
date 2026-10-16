# Slack Conversations

## How to search it

Use only an actually exposed authorized Slack read connector and inspect its schema. If absent or unauthenticated, report the gap; do not invent an authentication tool or initiate login. Bound queries to permitted channels/workspace and the relevant time range. Read matching messages and threads, but never send messages, react, join channels, or change state during investigation.

1. **Author-bounded search.** Messages from the PR author around the PR merge date. Limits scope dramatically and often hits gold.
2. **PR URL search.** Slack often links PRs when reviewed or discussed. Search for the PR URL (or its `/pull/<number>` path) within the permitted channels and date range.
3. **Error string search.** Search relevant exact errors within the same bounds; incident threads often surface. Fetch a matching thread through the actual supported read operation rather than interpreting an isolated message.

## Common pitfalls

- **Channel archaeology limits.** Very old messages may be gone due to retention policies. If you can't find anything before a certain date, note the retention cliff.
- **Unsearched DMs.** Many decisions happen in DMs that aren't searchable. You'll miss them. That's a known limitation.
- **Speculative jokes as "decisions."** Slack is casual. "Lol just do the thing" isn't a decision, even if it preceded the commit. Look for considered discussion.
- **Context collapse in single messages.** Without the thread, a single message often reads differently than in context. Always fetch threads.
- **Auth failures.** If the MCP isn't authenticated, stop. Don't make up findings. Report that Slack wasn't searchable.
