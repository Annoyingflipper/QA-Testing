# Session Backup: max
# Saved: 2026-04-25
# Project: DANAConnect Framework Tests

## Status
TC-SE-001 (valid login) and TC-SE-002 (login page elements present) are now **fully implemented and passing** on the real DANAConnect site. Both heavy-comment and lean versions pass; total run time ~17s for the heavy suite, ~15s for lean. Selenium parity with Luna's Playwright TC-PW-001/TC-PW-002 is complete. CEO ran tests live this session and verified green; no work in flight.

## Completed

### Test artefacts produced
- **`automation/selenium/pages/login_page.py`** — heavy POM, fully rewritten with Vaadin-correct locators (positional XPath for text inputs, class+role for ENTER, `.v-label-Corp` for footer, XPath class+text alternation for Privacy/Terms). Replaces the original placeholder-based locators (which never matched anything because Vaadin has no `placeholder` attribute).
- **`automation/selenium/tests/test_login_valid.py`** — TC-SE-001 rewritten. Now asserts `EC.url_contains("#!MainView")` instead of "URL changed away from /LoginView" (the old check was always false because Vaadin uses hash-based routing — the path stays `/LoginView` forever).
- **`automation/selenium/tests/test_login_elements.py`** — TC-SE-002, new. Mirrors Luna's `test_all_login_page_elements_are_visible`: navigates, waits, asserts visibility of all 7 required elements (Company, Username, Password, ENTER, Privacy, Terms, Footer).
- **Lean mirrors** under `automation/selenium/{pages,tests}/lean/` — same code, comments stripped, `# Traces to:` preserved per the Dual-File Comment Convention. Includes `__init__.py` files.

### Configuration changes
- **`automation/selenium/pytest.ini`** — new. Registers `smoke`/`critical`/`login` markers (was emitting `PytestUnknownMarkWarning`) and sets `norecursedirs = lean .venv` so default `pytest` runs heavy only.
- **`automation/selenium/requirements.txt`** — bumped shared packages to match Luna's Playwright pins (`pytest==9.0.3`, `python-dotenv==1.2.2`, `allure-pytest==2.15.3`). **Removed `webdriver-manager` entirely** (see Findings).
- **`automation/selenium/conftest.py`** — removed `webdriver-manager` import and `Service(ChromeDriverManager().install())`; switched to bare `webdriver.Chrome(options=options)` which uses Selenium 4.6+'s built-in Selenium Manager. Added `pytest_runtest_makereport` hook + screenshot/page-source/URL capture on test failure into `automation/selenium/screenshots/`.
- **`.gitignore`** — added `automation/*/screenshots/` so failure artefacts never get committed.
- **`.env`** — updated `PASSWORD=Jeanpaul21.` → `PASSWORD=Jeanpaul22.` per CEO mid-session (rotated password). File remains gitignored.

### POM robustness fixes added during live debugging
- **TAB-blur after password** — `enter_password()` now sends `Keys.TAB` after the value to trigger Vaadin's `change` event. Without this, the form submits before Vaadin commits the password value, producing a silent "empty password" failure.
- **JS-click fallback on ENTER** — `click_enter()` tries native `.click()` first, falls back to `arguments[0].click()` via `execute_script` if `ElementClickInterceptedException` or `ElementNotInteractableException` fires. The ENTER button is a Vaadin `<div role="button">` and the native click sometimes doesn't trigger the GWT handler cleanly.

### Verification
- Ran the full heavy suite live: `2 passed in 17.36s` against `https://portal.danaconnect.com/`.
- Ran the lean suite: `2 passed in 14.70s`.
- CEO independently ran `pytest -v` and confirmed green.

## In Progress
- (none) — all work this session is committed-ready and verified passing. No mid-flight files.

## Next Steps
- **Recommended next test: TC-SE-004 (invalid company code)** — Critical priority, mirrors a Luna test slot that's still empty. Forces us to discover the **error-banner locator**, which unlocks the entire negative-testing quadrant (TC-SE-005 invalid username, TC-SE-006 invalid password, TC-SE-007 all empty).
- **Alternate: TC-SE-006 (invalid password)** — also Critical, also forces error-banner discovery. Pick whichever the CEO finds more illustrative.
- **Maintenance task to consider**: CEO has not yet committed/pushed this session's work. When unblocked, recommend a single commit with a message like "Selenium TC-SE-001/002 — Vaadin parity with Luna's Playwright suite".
- After the next test ships, update `test-plans/feature-login.md` to flip the SE column from ⬜ to ✅ for TC-SE-001/002 (currently still shows ⬜ for SE despite being complete).

## Findings

### Critical: webdriver-manager 4.0.1 is broken on Apple Silicon
On macOS arm64, `ChromeDriverManager().install()` returns the path to `THIRD_PARTY_NOTICES.chromedriver` (a TEXT file shipped alongside the binary in Google's ChromeDriver archive) instead of the actual `chromedriver` binary. Python then tries to `exec` a text file → `OSError: [Errno 8] Exec format error`. The bug is in webdriver-manager's alphabetical file-finder logic. **Resolution: do not use webdriver-manager on this stack**. Selenium 4.6+ ships with **Selenium Manager** built-in, which auto-resolves the correct driver. The conftest now uses `webdriver.Chrome(options=options)` with no `service=` arg. Cleanup: `rm -rf ~/.wdm` removes the broken cache.

### Vaadin-specific gotchas (now codified in the POM)
- **No `placeholder` attribute on inputs** — any locator like `input[placeholder="..."]` will never match. Use positional XPath: `(//input[@type='text'])[1]` for Company, `[2]` for Username.
- **ENTER button is `<div class="v-button" role="button">`** — not a native `<button>`. CSS: `.v-button[role='button']`.
- **Hash-based routing** — post-login URL is `https://portal.danaconnect.com/LoginView#!MainView`. Path stays `/LoginView` forever. Asserting "URL changed away from /LoginView" always fails — assert `#!MainView` in URL.
- **Password field needs blur before submit** — Vaadin fires `change` only on blur, not on each keystroke. Send `Keys.TAB` after `send_keys(password)` or the click submits before the value is committed.
- **GWT-generated IDs change between deploys** (`gwt-uid-9`, `gwt-uid-11`, …) — never pin locators to them.
- **Labels vary by locale** — fresh en-US sessions see "USERNAME"/"PASSWORD"/"ENTER"; cached Spanish sessions see "Usuario"/"Contraseña"/"ENTRAR". Privacy/Terms locators use XPath class+text alternation to handle both.

### conftest.py still uses `implicitly_wait(10)` — known tech debt
The /qa-selenium skill warns against mixing implicit + explicit waits (can stack to 2× expected duration on negative assertions). Left in place this session per CEO call — only flagged for future cleanup. Will matter most when we add negative tests that assert "X is NOT present", since each absence check would burn 10s of implicit wait.

### Test data flow
- `.env` lives at project root (`danaconnect-framework-tests/.env`); `conftest.py` walks up two directories from its own location (`automation/selenium/`) to find it. Symbols: `BASE_URL`, `COMPANY`, `USERNAME`, `PASSWORD`. All required for TC-SE-001; TC-SE-002 needs none.
- Defensive guards (`assert credentials['company'], ...`) at top of TC-SE-001 give a clean error if `.env` is missing keys. Saved real time this session when password rotation initially looked like a Vaadin bug.

### Fixture duplication
Both `test_login_valid.py` and `test_login_elements.py` define a module-scoped `login_page` fixture inline. This works (module-scoped fixtures don't collide across files) but is duplicated. **Promote to `conftest.py`** when a third login-test file appears.

### How TC-SE-001 was actually unblocked
Initial failure (URL stuck on `/LoginView` after click) had **two overlapping causes**: (a) Vaadin password-blur bug, (b) stale password in `.env` (`Jeanpaul21.` was already the OLD password). I added the TAB blur + JS click fallback first as defensive measures, then the CEO mid-stream gave the new password (`Jeanpaul22.`). Test passed on the first run after the password update. The defensive fixes are still good — they protect against future Vaadin race conditions even though they weren't the immediate root cause.

### Allure reporting is wired but never invoked
`allure-pytest==2.15.3` is in requirements but no test was run with `--alluredir=...` this session. When we want reports: `pytest --alluredir=../../reports/allure-results` then `allure serve ../../reports/allure-results`.

## Blockers
- (none) — every test passes, every dependency resolves, CEO has the run instructions.

## Notes for next session

- **Run command** (CEO has memorized this now):
  ```
  cd /Users/vmaniglia/Documents/GitHub/QA-Testing/projects/danaconnect-framework-tests/automation/selenium
  source .venv/bin/activate
  pytest -v
  ```
  Variations: `pytest -v tests/lean/` for lean, `pytest -v -m critical` for TC-SE-001 only.

- **Do NOT reintroduce `webdriver-manager`** even if a future doc/article suggests it. The Selenium Manager path is the modern, supported way and dodges the THIRD_PARTY_NOTICES bug entirely.

- **When asked to add a new test**, follow the existing pattern: heavy version at `tests/test_X.py`, lean at `tests/lean/test_X.py`. Keep the `# Traces to: TC-SE-NNN` line in BOTH per the Dual-File Comment Convention.

- **The next negative test will need a new POM method** like `get_error_message()` plus a new locator constant (probably `ERROR_BANNER` against Vaadin's `.v-Notification` or `.v-errormessage`). Check the live DOM with the browser dev tools first — Luna's reconnaissance plan in `test-plans/feature-login.md` doesn't yet cover the error-banner element.

- **Screenshot-on-failure** writes `<test_name>.png`, `.html`, and `.url.txt` into `automation/selenium/screenshots/` (gitignored). If a future test fails, that folder is the first place to look.

- **CEO Protocol followed throughout this session**: ANNOUNCE → EXPLAIN → ASK before each major change, REPORT + FLAG + PUSH at the end of each block. CEO explicitly authorized me to run tests this session ("run the tests until they work") — that's a one-time exception to the standing "NEVER run tests" rule, not a permanent permission grant.
