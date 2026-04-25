# Session Backup: luna
# Saved: 2026-04-21_03-11-52
# Project: DANAConnect Framework Tests

## Status
Paused by CEO after two green Playwright login tests. Environment fully set up and working. Ready to resume with TC-PW-004 (invalid company) or stale-doc cleanup.

## Completed
- Bumped `automation/playwright/requirements.txt` to Python 3.13-compatible versions: pytest 9.0.3, playwright 1.58.0, pytest-playwright 0.7.2, python-dotenv 1.2.2, allure-pytest 2.15.3
- Set up Python venv + installed deps + Playwright browsers
- Wrote + debugged + passed **TC-PW-001** (valid login) → `tests/test_login.py::test_valid_login_redirects_away_from_login_page`
- Wrote + passed **TC-PW-002** (all login page elements visible) → `tests/test_login.py::test_all_login_page_elements_are_visible`
- Reconnaissance via Chrome MCP confirming DANAConnect is Vaadin 7 / GWT with hash routing and locale switching
- Added `Credentials` class in `conftest.py` with masked `__repr__` (password never appears in pytest failure output)
- Added `pytest.ini` with registered markers (smoke, critical, login) and `norecursedirs = lean .venv`
- Implemented Dual-File Comment Convention: `pages/lean/login_page.py` and `tests/lean/test_login.py` mirrors with identical code, minimal comments
- Propagated dual-file convention to `CLAUDE.md`, all three agent role files (luna, max, kai), and cross-session memory
- Updated `test-cases/TC-001-valid-login.md` with confirmed post-login URL `#!MainView`
- Rewrote `test-plans/feature-login.md` with accurate Vaadin recon data, Technical Notes section, verified Page Elements table, Known Site Behaviors, and per-framework automation status tracking (✅/🟡/⬜/❌)
- Tightened `LoginPage.FOOTER_TEXT` selector from ambiguous `text=/DANAConnect/i` to specific `.v-label-Corp`

## In Progress
(none — paused cleanly between test cases)

## Next Steps
1. Align `TC-002-page-elements-present.md` with Vaadin reality (stale label/placeholder language)
2. Draft `TC-003-field-labels.md` fresh (reinterpreted from placeholder-verification to label-verification)
3. Audit + patch `TC-004-invalid-company.md` and `TC-007-all-fields-empty.md` for stale assumptions
4. Automate **TC-PW-004** (invalid company code — negative login test) in `tests/test_login.py`
5. Share Vaadin reconnaissance with Max (Selenium) and Kai (Cypress) via `feature-login.md`

## Findings
DANAConnect technical notes for handoff to Max and Kai:
- Vaadin 7 / GWT-compiled SPA — shapes every locator strategy
- No placeholders, no stable IDs (`gwt-uid-*` changes between deploys) — use positional + class-based selectors
- Hash-based routing: path `/LoginView` never changes; only hash fragment does (`#!MainView` after login)
- Language varies by session (English/Spanish); don't pin locators to label text unless test is locale-scoped
- Company code remembered in cookies/localStorage after first login — fresh contexts see 3-field form, cached see 2-field
- ENTER button is `<div class="v-button" role="button">`, NOT a native `<button>`
- Copyright footer is `.v-label-Corp` (brand name "DANAConnect" also appears in "Welcome" caption)
- Confirmed post-login URL: `https://portal.danaconnect.com/LoginView#!MainView`

## Blockers
(none)
