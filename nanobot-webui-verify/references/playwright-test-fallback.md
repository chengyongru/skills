# Playwright Test Fallback

Use a temporary Playwright test spec when the flow needs stronger assertions, polling, or multi-step logic that is awkward through `playwright-cli` commands. Create a uniquely named temporary spec under `webui`, run it with `NANOBOT_WEBUI_URL`, then delete it. Prefer role selectors and assert both visible UI state and `window.location.hash` when verifying route persistence.

Example spec:

```js
import { test, expect } from '@playwright/test';

test('restores settings section hash across reload', async ({ page }) => {
  test.setTimeout(90000);

  await page.goto(`${process.env.NANOBOT_WEBUI_URL}/#/settings?section=models`, {
    waitUntil: 'domcontentloaded',
  });
  await expect(page.getByRole('heading', { name: 'Models' })).toBeVisible({ timeout: 20000 });
  await expect.poll(() => page.evaluate(() => window.location.hash)).toBe('#/settings?section=models');

  await page.reload({ waitUntil: 'domcontentloaded' });
  await expect(page.getByRole('heading', { name: 'Models' })).toBeVisible({ timeout: 20000 });
  await expect.poll(() => page.evaluate(() => window.location.hash)).toBe('#/settings?section=models');
});
```

Run from `webui`:

```powershell
$specPath = ".verify-webui-$runId.spec.mjs"
$env:NANOBOT_WEBUI_URL = "http://127.0.0.1:$websocketPort"
npx playwright test $specPath --browser=chromium --reporter=line
```

If Playwright is missing, install only what is needed and avoid committing generated dependency lockfile churn unless the project intentionally changes dependencies.
