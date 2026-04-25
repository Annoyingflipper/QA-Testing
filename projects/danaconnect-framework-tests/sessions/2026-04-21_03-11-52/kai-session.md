# Session Backup: kai
# Saved: 2026-04-25
# Project: DANAConnect Framework Tests

## Status

**TC-CY-001 + TC-CY-002 are written and ready to run.** This was the first
session where Cypress code actually shipped. All 7 files (2 page objects,
2 specs, 2 test-case markdowns, 1 updated commands.js) are in place. CEO
has NOT run the tests yet — they're currently learning bash basics in
preparation for the first manual run. No execution feedback exists yet.

## Completed

### Reconnaissance
- Read `agents/kai-cypress.md`, project `CLAUDE.md`, prior `kai-session.md`
- Read `test-plans/feature-login.md` (TP-LOGIN-001) — the authoritative
  Vaadin handoff with the verified locator table
- Read Luna's Playwright reference implementation:
  - `automation/playwright/tests/test_login.py` (TC-PW-001 + TC-PW-002)
  - `automation/playwright/pages/login_page.py`
  - Lean twins of both
- Read `test-cases/TC-SE-001-valid-login.md` for markdown format
- Confirmed the previous `LoginPage.js` and `commands.js` used broken
  `input[placeholder="..."]` selectors (Vaadin/GWT inputs have NO
  placeholder attribute) — exactly the stale-locator mistake the CEO
  warned about

### Code shipped (7 files)
1. **Rewrote** `automation/cypress/cypress/pages/LoginPage.js` —
   Vaadin-correct getter-based POM. Heavy comments.
2. **Created** `automation/cypress/cypress/pages/lean/LoginPage.js` —
   identical code, lean comments.
3. **Created** `automation/cypress/cypress/e2e/login.cy.js` — one
   `describe('Login', ...)` with two `it()` blocks: TC-CY-001 (valid
   login → asserts `cy.url().should('include', '#!MainView')`) and
   TC-CY-002 (all 7 elements visible). Heavy comments.
4. **Created** `automation/cypress/cypress/e2e/lean/login.cy.js` — lean
   twin.
5. **Created** `test-cases/TC-CY-001-valid-login.md` — mirrors TC-SE-001
   format but with the **correct hash-routing assertion** (deliberately
   does NOT repeat Max's "URL no longer contains /LoginView" mistake).
6. **Created** `test-cases/TC-CY-002-login-page-elements.md` — new,
   covers the 7-element UI verification.
7. **Updated** `automation/cypress/cypress/support/commands.js` —
   `cy.login()` now delegates to the singleton page object instead of
   hardcoding selectors. Single source of truth for selectors.

### CEO support
- Walked CEO through how to run tests: `cd automation/cypress`,
  `npm install`, `npx cypress open` or `npx cypress run --spec ...`
- Coached CEO on basic bash navigation: `cd ..`, `cd ../..`, `cd -`,
  `cd ~`, `pwd`

## In Progress
- CEO running TC-CY-001 + TC-CY-002 for the first time. They were last
  seen learning `cd ..` to navigate back from the cypress folder. No
  test results returned yet.

## Next Steps

### Immediate (CEO-blocked)
1. CEO runs `npm install` inside `automation/cypress/` (one-time)
2. CEO runs `npx cypress open` → click `login.cy.js` → both tests run
3. Kai triages whatever comes back. Likely failure modes:
   - **Selector miss** — the regex on Privacy/Terms or the `.v-label-Corp`
     class might shift with the live DOM. Have CEO send a screenshot of
     the failing step.
   - **`COMPANY env var is not set`** — `.env` is missing one of the
     three vars. File exists; check values aren't blank.
   - **`#!MainView` timeout** — Vaadin took >10s. Bump
     `defaultCommandTimeout` or check creds.

### Open question for CEO (raised, not yet answered)
- **Apply `excludeSpecPattern: 'cypress/e2e/lean/**/*'` to
  `cypress.config.js`?** Without it, plain `npx cypress run` executes
  BOTH heavy and lean specs, hitting login twice per run. Recommended
  yes — matches the `pytest norecursedirs` convention CLAUDE.md
  specifies for the other two frameworks.

### After TC-CY-001/002 go green
- Write the negative-case batch (mirrors Luna's gaps too — Luna also
  hasn't written these yet):
  - TC-CY-004 — Invalid company code
  - TC-CY-005 — Invalid username
  - TC-CY-006 — Invalid password
  - TC-CY-007 — All fields empty
- Then UI/UX cluster: TC-CY-010 (password masking), TC-CY-013 (footer
  shown), and TC-CY-003 (field labels — note: per TP-LOGIN-001 this
  was reinterpreted from "placeholder text" because Vaadin has no
  placeholders).

## Findings

### Cypress translation table for Luna's Playwright locators
Memorize this — it's the core of the framework-port work.

| Playwright | Cypress | Note |
|---|---|---|
| `:nth-match(input[type="text"], 1)` | `cy.get('input[type="text"]').eq(0)` | **0-indexed**, not 1-indexed |
| `input[type="password"]` | unchanged | only one on the page |
| `.v-button[role="button"]` | unchanged | ENTER is a `<div>`, NOT `<button>` |
| `.v-caption-label-signIn-company:has-text("Privacy")` | `cy.contains('.v-caption-label-signIn-company', /Privacy\|Pol[íi]tica/)` | `:has-text()` is Playwright-only |
| `.v-label-Corp` | unchanged | stable Vaadin class |
| `expect(page).to_have_url(re.compile(r"#!MainView"))` | `cy.url().should('include', '#!MainView')` | both auto-retry |
| `page.wait_for_load_state("networkidle")` | (no equivalent) | rely on `.should('be.visible')` auto-retry on first element |
| `os.environ["COMPANY"]` | `Cypress.env('COMPANY')` | wired in `cypress.config.js` from `.env` |

### Convention notes
- **Project uses ES modules** in pages/specs (`export default`, `import`).
  `cypress.config.js` uses CommonJS (`require`). Both work — stay
  consistent with each file's existing style; do NOT unify unless asked.
- **`/qa-cypress` skill defaults don't apply.** The skill recommends
  `[data-testid]`/`[data-cy]` selectors and CommonJS exports. Vaadin
  has no test attributes, and the project chose ES modules. Defer to
  TP-LOGIN-001 locator strategy and existing project style every time.
- **`defaultCommandTimeout: 10000`** in `cypress.config.js` — 10s
  retry for `.should()` and `cy.url()`. Plenty for Vaadin SPA render
  + post-login client-side route change.
- **Single-file vs. multi-file specs.** Chose ONE `login.cy.js` with a
  single `describe('Login', ...)` containing two `it()` blocks. Mirrors
  Luna's `test_login.py` and matches Cypress idiom of grouping by
  page/feature.
- **commands.js delegation.** Custom commands import the page-object
  singleton and delegate. One source of truth for selectors. When
  Vaadin renames a class, only `LoginPage.js` changes.

### Watch out for
- **Max's TC-SE-001 markdown still has the "URL no longer contains
  /LoginView" mistake** — that's the wrong assertion for Vaadin hash
  routing. Did NOT copy it into TC-CY-001. If CEO ever asks why TC
  formats diverge, this is why. Worth flagging to Max next session.
- **CLAUDE.md got a new "CEO Session Persistence" section** mid-session
  (CEO now has `sessions/latest/ceo-session.md`). Not Kai's
  responsibility, but the file structure changed.

## Blockers
- None on Kai's side. Ball is in CEO's court — install deps and run.

## Notes for next session

- **Resume point:** ask CEO immediately for test results. If anything
  failed, pull the screenshot from `automation/cypress/cypress/screenshots/`
  before guessing at causes.
- **Don't re-litigate the page object selectors** unless tests fail.
  They mirror Luna's verified Playwright selectors 1:1; if Luna's
  passed, ours should too.
- **The `excludeSpecPattern` config tweak is still pending** CEO
  approval. Don't auto-apply it; raise it again if CEO complains
  about double-runs.
- **Negative cases are the next batch** — start ANNOUNCE/ASK for
  TC-CY-004 through TC-CY-007 only after TC-CY-001/002 go green.
- **Spanish-locale handling** — Privacy/Terms regex covers both en and
  es. If CEO ever has a cached Spanish session, those locators should
  still find the links. The text inputs are positional so they're
  locale-immune already.
