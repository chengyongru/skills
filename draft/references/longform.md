# Long-form Articles

Use this reference for blog posts, technical notes intended for publication, and article-length project retrospectives.

## Narrative Shape

Let the article unfold in the order a reader would naturally follow. Do not announce the outline or frontload a taxonomy.

A strong technical narrative usually follows:

1. The concrete problem and why it mattered.
2. The initial model or hypothesis.
3. Evidence that contradicted or refined it.
4. The actual mechanism, with enough implementation detail to verify it.
5. The fix or experiment and measured result.
6. The boundary of the conclusion: what was and was not tested.
7. The reusable lesson.

Do not force this structure when the source is a resource guide or tool comparison, but always preserve causal order.

## Evidence

- Preserve exact numbers, commands, links, code snippets, traces, versions, and failure modes.
- Distinguish direct measurements from interpretation.
- Cite source URLs close to the claims they support.
- State test conditions when they affect reproducibility.
- Never turn one environment's result into a universal claim.

## Style

- Assume the reader is technically competent. Explain only the missing step needed for the current argument.
- Prefer concrete nouns and verbs to abstract engineering language.
- Use headings only when they help navigation; do not create a heading for every paragraph.
- Avoid executive-summary repetition at both the beginning and end.
- Do not manufacture a grand conclusion. End at the level supported by the evidence.
- In Chinese, avoid em-dashes and mechanical `不是 A，而是 B` contrasts.

## Length

Let evidence determine length. Remove background that the target reader already knows and details that do not change the conclusion. A debugging record may be 800 words; an architecture essay may need 2,000. Do not pad to a target length.

## Output

Return:

1. A working title.
2. The article draft ready for review.
3. A short list of factual gaps or claims that need verification, only when such gaps exist.

Do not append generic publishing advice unless requested.
