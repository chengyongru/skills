# Sharpen

Rewrite the user's task to make it deeper, not bigger. Return only the rewritten prompt. Do not execute the task it describes; this turn stays read-only.

Before writing, identify what a top professional would do that the task omits, the primary sources they would start from, the methods and available tools they would use, and an independent check that could show the result is right.

Have the rewritten prompt ask the agent to prototype choices an experiment can settle and recommend an option from what it observes. Keep experiments within the user's authorized scope; for a read-only task, propose the experiment rather than granting execution. Leave product and preference choices that no experiment can settle to the user.

Preserve the user's goal, explicit constraints, repository rules, and runtime boundaries. Question self-imposed assumptions, not the user's authority. Add only what improves the requested result.
