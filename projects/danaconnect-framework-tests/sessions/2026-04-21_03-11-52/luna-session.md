# Session Backup: luna
# Saved: 2026-04-25
# Project: DANAConnect Framework Tests

## Status
Paused cleanly between test cases. Two Playwright login tests are green and committed.
Environment is fully set up (venv + Playwright browsers + Allure). Dual-file convention
implemented for everything written so far. Login feature plan is aligned with real
Vaadin reconnaissance. Awaiting CEO approval to start TC-PW-004 (invalid company code,
negative login). No blockers.

## Completed

### Environment & infrastructure
- Bumped `automation/playwright/requirements.txt` to Python 3.13-compatible versions:
  pytest 9.0.3, playwright 1.58.0, pytest-playwright 0.7.2, python-dotenv 1.2.2,
  allure-pytest 2.15.3
- Created and activated Python venv, installed deps, installed Playwright browsers
- Added `pytest.ini` with:
  - Registered markers: `smoke`, `critical`, `login`
  - `norecursedirs = lean .venv` (so default `pytest` skips lean mirrors)
- Added `Credentials` dataclass-style class in `conftest.py` with masked `__repr__` —
  password never appears in pytest failure output

### Test cases automated (heavy + lean versions)
- **TC-PW-001 — Valid login redirects away from login page**
  - File: `tests/test_login.py::test_valid_login_redirects_away_from_login_page`
  - Lean mirror: `tests/lean/test_login.py`
  - Asserts post-login URL contains `#!MainView`
  - GREEN
- **TC-PW-002 — All login page elements visible**
  - File: `tests/test_login.py::test_all_login_page_elements_are_visible`
  - Lean mirror: `tests/lean/test_login.py`
  - Asserts company-code field, user field, password field, ENTER button, footer all visible
  - GREEN

### Page objects
- `automation/playwright/pages/login_page.py` (heavy)
- `automation/playwright/pages/lean/login_page.py` (lean mirror — identical code, minimal comments)
- Tightened `LoginPage.FOOTER_TEXT` from ambiguous `text=/DANAConnect/i` to specific `.v-label-Corp`
  (the brand name "DANAConnect" also appears in the "Welcome" caption, causing strict-mode
  violations before the fix)

### Reconnaissance (via Chrome MCP on portal.danaconnect.com)
- Confirmed DANAConnect is a Vaadin 7 / GWT-compiled SPA
- Hash-based routing: path `/LoginView` never changes; only the hash fragment does
- Confirmed post-login URL: `https://portal.danaconnect.com/LoginView#!MainView`
- ENTER button is a `<div class="v-button" role="button">`, NOT a native `<button>`
- No placeholders, no stable IDs (`gwt-uid-*` rotates between deploys)
- Company code is remembered in cookies/localStorage after first successful login —
  fresh contexts see a 3-field form, cached contexts see a 2-field form
- Language varies by session (English/Spanish auto-detected) — locators must not pin to label text
  unless the test is explicitly locale-scoped

### Documentation
- Implemented and propagated the **Dual-File Comment Convention**:
  - Updated `CLAUDE.md` with Dual-File section + Discovery rules
  - Updated `agents/luna-playwright.md`, `agents/max-selenium.md`, `agents/kai-cypress.md`
  - Saved cross-session memory entry so the convention persists
- Rewrote `test-plans/feature-login.md` with:
  - Accurate Vaadin recon data
  - Technical Notes section
  - Verified Page Elements table
  - Known Site Behaviors section
  - Per-framework automation status tracking (✅/🟡/⬜/❌)
- Updated `test-cases/TC-001-valid-login.md` with confirmed post-login URL `#!MainView`

### Session check-in (this turn)
- Resumed from previous session, read `agents/luna-playwright.md`, `CLAUDE.md`, and
  prior `luna-session.md`
- Reported status to CEO, recommended **TC-PW-004 (invalid company code)** as next test
- Noted (this conversation) the new "CEO Session Persistence" section in `CLAUDE.md` —
  this affects the **CEO assistant**, not Luna; my own session file remains `luna-session.md`

## In Progress
(none — paused cleanly between test cases, awaiting CEO go/no-go on TC-PW-004)

## Next Steps

### Recommended next action
1. **Automate TC-PW-004 — Invalid company code rejects login** (negative login test)
   - Reconnoiter the Vaadin error-state element via Chrome MCP first (do NOT guess)
   - Add `login_with_invalid_company()` method to `LoginPage` (heavy + lean)
   - Add error-state locator to `LoginPage`
   - Write `test_invalid_company_code_shows_error` in `tests/test_login.py` (heavy + lean)
   - Traceability: `# Traces to: TC-PW-004 — Invalid company code rejects login`
   - Assertions: URL stays on `/LoginView` (no `#!MainView`) AND error element is visible
   - This unlocks the first error-state assertion pattern Max and Kai can mirror

### Test-case doc cleanup (lower priority but should happen soon)
2. Align `TC-002-page-elements-present.md` with Vaadin reality (current copy still references
   placeholder/label language that doesn't exist on the real page)
3. Draft `TC-003-field-labels.md` fresh — reinterpret from "placeholder verification" to
   "label verification" (Vaadin uses external labels, not placeholders)
4. Audit + patch `TC-004-invalid-company.md` for stale assumptions — needs to reflect the
   3-field-form-on-fresh-context behavior
5. Audit + patch `TC-007-all-fields-empty.md` — confirm the empty-submit error path

### Cross-team handoff
6. Share Vaadin reconnaissance with Max (Selenium) and Kai (Cypress) — most of it is already
   in `feature-login.md`, but a direct ping in their session files would help when they spin up

## Findings

### DANAConnect technical profile (handoff-ready for Max and Kai)
- **Stack:** Vaadin 7 / GWT-compiled SPA — shapes every locator strategy
- **IDs:** No stable IDs. `gwt-uid-*` changes between deploys. Use positional + class-based selectors.
- **Routing:** Hash-based. Path `/LoginView` is constant; only the hash fragment changes.
  Use the hash, not the path, to detect navigation.
- **Post-login URL:** `https://portal.danaconnect.com/LoginView#!MainView`
- **Language:** Session-scoped (English / Spanish). Don't pin locators to label text unless
  the test is locale-scoped.
- **Form variants:**
  - Fresh context (no cookies/localStorage) → **3-field** form: company + user + password
  - Cached context (prior successful login on same browser) → **2-field** form: user + password
  - Tests must control which variant they target by managing browser context
- **ENTER button:** `<div class="v-button" role="button">` — NOT a native `<button>`.
  Locator: `div.v-button[role="button"]` or via accessible name.
- **Footer copyright:** `.v-label-Corp`. The brand name "DANAConnect" also appears in the
  "Welcome" caption, so plain text matches collide with strict mode — use the class.

### Dual-File Comment Convention — operational notes
- `pytest` (default) → heavy versions only (lean folders in `norecursedirs`)
- `pytest tests/lean/` → runs lean versions explicitly
- Heavy and lean **must contain identical code** — only comments and docstrings differ
- Traceability comment (`# Traces to: TC-PW-NNN`) is required in BOTH versions

### Credentials handling
- All creds read from `.env` via `python-dotenv` in `conftest.py`
- `Credentials.__repr__` masks the password — safe to log/print in failure output
- `.env` is gitignored; `.env.example` is the template

## Blockers
(none)

## Notes for next session
- When starting TC-PW-004, **first** reconnoiter the error element with Chrome MCP — the Vaadin
  error rendering is non-obvious and likely involves a notification overlay or inline label
  that may or may not have a stable class. Do NOT guess the locator.
- When automating any test that requires the **3-field** form variant, ensure the test uses a
  fresh browser context (no cookies/localStorage) so company code isn't auto-filled.
- The CEO runs all tests manually — never run them, only write them.
- The `CLAUDE.md` "CEO Session Persistence" section applies to the CEO's assistant, not to
  Luna/Max/Kai. My own session file lives at `sessions/latest/luna-session.md`.
- Heavy + lean dual-file output is non-negotiable for every new test and page object.
