# TC-CY-002 — All Login Page Elements Are Visible (Cypress)

## Info

| Field | Value |
|-------|-------|
| ID | TC-CY-002 |
| Framework | Cypress |
| Priority | High |
| Type | UI Verification / Smoke |
| Feature | Login Page |
| Automated | Yes — `automation/cypress/cypress/e2e/login.cy.js` → `Login > shows all 7 login page elements on a fresh visit` |
| Author | Kai (Cypress Test Writer) |
| Mirrors | TC-PW-002 (Playwright, Luna) |

## Preconditions
- Node.js ≥ 18 and Cypress installed (`npm install` in `automation/cypress/`)
- User has no cached authenticated session (Cypress clears cookies/localStorage between tests by default)
- `portal.danaconnect.com` is reachable from the test runner
- **No credentials required** — this test does not submit the form

## Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Launch Cypress and navigate to `baseUrl + /LoginView` | Login page loads |
| 2 | Wait for the Vaadin form to render | All elements appear within 10 s (Cypress `.should('be.visible')` auto-retry) |
| 3 | Verify each required element is visible | All 7 elements below pass `.should('be.visible')` |

## Elements to verify (all 7)

| # | Element | Selector (via page object) | Underlying CSS |
|---|---------|---------------------------|----------------|
| 1 | Company input | `loginPage.companyInput` | `input[type="text"]:eq(0)` |
| 2 | Username input | `loginPage.usernameInput` | `input[type="text"]:eq(1)` |
| 3 | Password input | `loginPage.passwordInput` | `input[type="password"]` |
| 4 | ENTER button | `loginPage.enterButton` | `.v-button[role="button"]` |
| 5 | Privacy Policy link | `loginPage.privacyPolicyLink` | `.v-caption-label-signIn-company` containing `/Privacy\|Pol[íi]tica/` |
| 6 | Terms of Use link | `loginPage.termsOfUseLink` | `.v-caption-label-signIn-company` containing `/Terms\|T[ée]rminos/` |
| 7 | Copyright footer | `loginPage.footer` | `.v-label-Corp` |

## Expected Result
Every one of the 7 elements listed above passes `.should('be.visible')` within 10 seconds of page load.

## Assertion Strategy (Cypress-specific)
- One `.should('be.visible')` per element — each is auto-retrying, so Cypress collectively polls the DOM until everything renders or the timeout fires.
- No `cy.wait(ms)` hardcoded delays. We rely on Cypress's built-in retry for the Vaadin SPA's async render.
- Privacy Policy and Terms of Use links share the same class (`.v-caption-label-signIn-company`). The page-object getters disambiguate them with a locale-agnostic regex that matches both English and Spanish labels.

## Why this test exists
- Pure UI regression — catches the scenario where a developer accidentally hides or removes a required element (e.g., the footer, privacy link, or terms link).
- No credentials needed, no form submission — safe and fast to run constantly, on every PR.
- Complementary to TC-CY-001: that test validates the functional login path; this one validates that the form is drawn correctly before the user even tries.

## Notes
- Labels change by locale ("USERNAME" in en-US vs "Usuario" in es). Selectors deliberately avoid pinning to label text.
- The copyright footer is selected via `.v-label-Corp` rather than text-match so it doesn't collide with the "Welcome to DANAConnect" greeting caption that also contains the brand name.
