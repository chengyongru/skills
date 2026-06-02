# Safety

Verification should be realistic without being reckless.

## Resource Policy

Prefer resources in this order:

1. Local isolated temp data created for this run.
2. Project-documented test fixtures or test environments.
3. User-provided staging credentials or accounts.
4. Real external services only after the user clearly authorizes their use.

Do not assume production resources are allowed.

## Destructive or Costly Actions

Ask before:

- Deleting, overwriting, or migrating real data.
- Sending emails, messages, payments, webhooks, or notifications.
- Hitting paid APIs at meaningful cost.
- Modifying remote accounts, repositories, cloud resources, or production systems.

If a write is needed, prefer creating a unique test record and reading it back. Clean it up when safe.

## Secrets

- Do not print secrets in the final report.
- Redact tokens, cookies, API keys, passwords, and authorization headers.
- Keep evidence files local unless the user asks to publish them.

## When Blocked

If a required resource is missing, report NOT RUN or WARN with:

- Resource needed.
- Why it is needed.
- What was verified instead, if anything.
- Residual risk.
