# Attack the Premise

When two or more fixes share a premise and fail the same check, test the premise before another fix.

- Write the one sentence every failed fix assumed.
- Find an observation that would differ if it were false. Check how the failures are distributed, not only their size. Use a safe scoped check; disruptive or live instrumentation needs authorization.
- If the evidence contradicts the premise, find what the failures share that it did not predict. Remove the condition causing the failure rather than add a mechanism to compensate for it. If the premise holds, trace the next cause with [Fix Root Causes](fix-root-causes.md).

Do not start another fix until the premise is tested or the missing decisive evidence is reported. A wider cause is a finding to scope, not authority to repair unrelated systems.
