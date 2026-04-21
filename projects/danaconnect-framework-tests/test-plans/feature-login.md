# Test Plan: Login Page — DANAConnect Framework Tests

## Document Info

| Field | Value |
|-------|-------|
| Document ID | TP-LOGIN-001 |
| Feature | Login Page (`/LoginView`) |
| Target URL | https://portal.danaconnect.com/LoginView |
| Created | 2026-04-17 |
| Last Updated | 2026-04-21 (Vaadin reconnaissance correction) |
| Status | Active |

## Feature Description

The DANAConnect login page is the entry point to the platform. A fresh browser session must provide three credentials to authenticate:
1. **Company code** — identifies the organization (multi-tenant app)
2. **Username** — identifies the user within the company
3. **Password** — authenticates the user

After the first successful login from a given browser, the company code is remembered (cookie/localStorage) and subsequent visits show a simplified 2-field form (Username + Password only).

## Technical Notes (CRITICAL for writing automation)

### Framework: Vaadin / GWT
DANAConnect is a **Vaadin 7-style, GWT-compiled single-page app**. This has major implications for locators:

- Inputs have **no** `placeholder`, `name`, or `aria-label` attributes.
- Element IDs look like `gwt-uid-9`, `gwt-uid-11` — **auto-generated at compile time and change between deploys**. Do not pin locators to these IDs.
- The ENTER "button" is a `<div class="v-button" role="button">`, NOT a native `<button>` element.
- Field labels are rendered as sibling `<span class="v-caption">` elements inside a Vaadin FormLayout `<tr>` row structure.

### Hash-based routing
Post-login the URL changes from `/LoginView` to `/LoginView#!MainView`. The path stays `/LoginView` forever — only the hash fragment changes. Any test asserting "URL no longer contains `/LoginView`" will always fail. **Assert the presence of `#!MainView` instead.**

### Locale switching
The site serves different labels based on session locale (browser `Accept-Language`, geolocation, and/or user preference):
- Fresh Playwright/Selenium/Cypress contexts (default en-US) see mostly English labels: `COMPANY`, `USERNAME`, `PASSWORD`, button `ENTER`.
- Cached Spanish-preference sessions see: `Usuario`, `Contraseña`, button `ENTRAR`.

Locators should NOT pin to label text unless the test is explicitly locale-scoped. Prefer positional or class-based selectors.

### Fresh-context vs cached-context forms
- **Fresh browser context** (every `@pytest.fixture` with `scope="function"`): 3-field form (Company, Username, Password)
- **Cached browser context**: 2-field form (Username, Password — Company is pre-filled and hidden behind a "different company" link)

## Page Elements (verified 2026-04-21 via live reconnaissance)

| Element | HTML | Verified label (fresh en-US) | Stable locator strategy |
|---------|------|------------------------------|-------------------------|
| Company input | `<input type="text">` (1st of 2) | "COMPANY*" | `:nth-match(input[type="text"], 1)` |
| Username input | `<input type="text">` (2nd of 2) | "USERNAME*" (varies by locale) | `:nth-match(input[type="text"], 2)` |
| Password input | `<input type="password">` | "PASSWORD*" (varies) | `input[type="password"]` |
| ENTER button | `<div class="v-button" role="button">` | "ENTER" / "ENTRAR" | `.v-button[role="button"]` |
| Privacy Policy link | `<span class="v-caption v-caption-label-signIn-company">` | "Privacy Policy" / "Política de Privacidad" | `.v-caption-label-signIn-company:has-text("Privacy")` |
| Terms of Use link | Same class as above | "Terms of Use of the Service" / "Términos y condiciones" | `.v-caption-label-signIn-company:has-text("Terms")` |
| Copyright footer | `<div class="v-label v-label-Corp">` | "DANAConnect Corp. All Rights Reserved" | `.v-label-Corp` |

## Test Case Index

Automation status legend: ✅ automated | 🟡 in progress | ⬜ not started | ❌ obsolete

### Positive Tests

| ID | Title | Priority | PW | SE | CY |
|----|-------|----------|----|----|----|
| TC-XX-001 | Valid login with correct credentials | Critical | ✅ | ⬜ | ⬜ |
| TC-XX-002 | Verify all login page elements are present | High | 🟡 | ⬜ | ⬜ |
| TC-XX-003 | Verify field labels display correctly (was: placeholder text — reinterpreted 2026-04-21, Vaadin has no placeholders) | Medium | ⬜ | ⬜ | ⬜ |

### Negative Tests

| ID | Title | Priority | PW | SE | CY |
|----|-------|----------|----|----|----|
| TC-XX-004 | Login with invalid company code | Critical | ⬜ | ⬜ | ⬜ |
| TC-XX-005 | Login with invalid username | Critical | ⬜ | ⬜ | ⬜ |
| TC-XX-006 | Login with invalid password | Critical | ⬜ | ⬜ | ⬜ |
| TC-XX-007 | Login with all fields empty | High | ⬜ | ⬜ | ⬜ |
| TC-XX-008 | Login with only company field filled | Medium | ⬜ | ⬜ | ⬜ |
| TC-XX-009 | Login with company and username only (no password) | Medium | ⬜ | ⬜ | ⬜ |

### UI / UX Tests

| ID | Title | Priority | PW | SE | CY |
|----|-------|----------|----|----|----|
| TC-XX-010 | Password field masks input (type="password") | High | ⬜ | ⬜ | ⬜ |
| TC-XX-011 | Privacy Policy link is clickable and opens the policy | Low | ⬜ | ⬜ | ⬜ |
| TC-XX-012 | Terms of Use link is clickable and opens the terms | Low | ⬜ | ⬜ | ⬜ |
| TC-XX-013 | Footer text is displayed | Low | ⬜ | ⬜ | ⬜ |

**Total planned: 13 test cases × 3 frameworks = 39 automated tests**

`XX` is the framework prefix (PW, SE, CY). Each test case file covers all three frameworks.

## Preconditions

- Browser is open to `https://portal.danaconnect.com/LoginView`
- **Fresh browser context (no cached company)** — required to see the 3-field form. Each pytest `page` fixture with `scope="function"` already does this automatically.
- `.env` credentials are configured (see `.env.example`)

## Test Data

| Scenario | Company | Username | Password |
|----------|---------|----------|----------|
| Valid login | (from .env) | (from .env) | (from .env) |
| Invalid company | `invalidcompany` | (from .env) | (from .env) |
| Invalid username | (from .env) | `invaliduser` | (from .env) |
| Invalid password | (from .env) | (from .env) | `wrongpassword` |
| All empty | `""` | `""` | `""` |

## Known Site Behaviors

- **Post-login URL:** `https://portal.danaconnect.com/LoginView#!MainView` (Vaadin hash routing)
- **Company caching:** After first successful login, the company name is persisted in browser storage and the login form auto-populates / hides the Company field on return visits
- **Language persistence:** User's last session language is remembered across visits from the same browser

## Candidate Future Test Cases (not in current scope)

Surfaced during 2026-04-21 reconnaissance. Consider adding when current backlog is cleared:

- TC-XX-014 — Verify company name is cached after successful login (2-field form appears on next visit)
- TC-XX-015 — Verify "Entrar utilizando una compañía diferente" link switches back to the 3-field form
- TC-XX-016 — Verify "Recuperar tu Contraseña" (forgot password) link navigates correctly
