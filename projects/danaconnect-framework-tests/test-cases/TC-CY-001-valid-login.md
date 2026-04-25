# TC-CY-001 — Valid Login with Correct Credentials (Cypress)

## Info

| Field | Value |
|-------|-------|
| ID | TC-CY-001 |
| Framework | Cypress |
| Priority | Critical |
| Type | Positive / Functional |
| Feature | Login Page |
| Automated | Yes — `automation/cypress/cypress/e2e/login.cy.js` → `Login > logs in with valid credentials and routes to #!MainView` |
| Author | Kai (Cypress Test Writer) |
| Mirrors | TC-PW-001 (Playwright, Luna) |

## Preconditions
- Node.js ≥ 18 and Cypress installed (`npm install` in `automation/cypress/`)
- `.env` file at project root contains non-empty `BASE_URL`, `COMPANY`, `USERNAME`, and `PASSWORD`
- User has no cached authenticated session (Cypress clears cookies/localStorage between tests by default)
- `portal.danaconnect.com` is reachable from the test runner

## Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Launch Cypress and navigate to `baseUrl + /LoginView` | Login page loads; Company, Username, Password fields and ENTER button are visible within 10 s |
| 2 | Enter the valid `COMPANY` value into the Company input (1st text input) | Text appears in the field |
| 3 | Enter the valid `USERNAME` value into the Username input (2nd text input) | Text appears in the field |
| 4 | Enter the valid `PASSWORD` value into the Password input (`input[type="password"]`) | Password is masked (dots/asterisks) |
| 5 | Click the ENTER button (`.v-button[role="button"]`) | Form submits; Vaadin routes client-side to the dashboard |

## Expected Result
The browser's current URL **contains the hash fragment `#!MainView`** within 10 seconds of clicking ENTER. This is the only reliable logged-in signal for this app — see "Hash-based routing" note below.

## Assertion Strategy (Cypress-specific)
- Use `cy.url().should('include', '#!MainView')` — `.should()` auto-retries up to `defaultCommandTimeout` (10 s), so no explicit wait is needed for the client-side route change.
- Do **NOT** assert `cy.url().should('not.include', '/LoginView')` — Vaadin uses hash routing, so the path stays `/LoginView` forever.
- Use `loginPage.<element>.should('be.visible')` before typing to give the Vaadin SPA time to render. This is Cypress's equivalent of Playwright's `page.wait_for_load_state("networkidle")`.

## Hash-based routing (important context)

DANAConnect is a Vaadin/GWT single-page app that uses hash-based routing:

```
Before login:  https://portal.danaconnect.com/LoginView
After login:   https://portal.danaconnect.com/LoginView#!MainView
```

The `/LoginView` path never changes. Any assertion that the URL moves away from `/LoginView` will always fail.

## Notes
- **Never** hardcode credentials. Values come from `Cypress.env('COMPANY')`, etc., which are wired in `cypress.config.js` from the `.env` file.
- The page object (`cypress/pages/LoginPage.js`) uses positional selectors for the text inputs because Vaadin renders no `placeholder`, `name`, or `aria-label` attributes on its inputs. Pinning to element IDs would also fail — GWT auto-generates them (`gwt-uid-N`) and they change between deploys.
- After the first successful login from a given browser, the company is cached and the form shows only 2 inputs. Cypress's default between-test isolation prevents this from affecting subsequent tests in the same `cypress run`, but be aware if you ever run the spec interactively in `cypress open` without closing the browser between runs.
- This test is the "gate" — if it fails, most other login tests are invalid (they assume we CAN reach the login page).
