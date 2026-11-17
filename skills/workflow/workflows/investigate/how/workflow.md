# How

Explore the codebase and explain it to a senior engineer unfamiliar with this area. Give them a mental model they can use to work in it: the architecture, state ownership, runtime flow, and correctness conditions. Follow [behavior-first explanation](../../../references/explanation.md). If the question is ambiguous, state your interpretation and explore.

Work directly in one read-only pass. When an independent trace is worth delegating under the [runtime contract](../../../references/runtime.md), give a bounded worker the user's question and the same explanation brief. Do not split exploration and explanation into separate agent stages. Check important claims and incorporate the result without repeating the worker's whole investigation.

Present the explanation, not an investigation report. Use a small diagram when it clarifies the behavior, and cite source locations where useful. Do not edit files, launch the application, or publish anything for an explanation-only request.
