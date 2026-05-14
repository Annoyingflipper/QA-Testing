"""
DANAConnect — Login Tests (Playwright)
=======================================
This file contains end-to-end tests for the DANAConnect login page.

How pytest discovers tests:
- Files must start with `test_` (this file: test_login.py ✓)
- Functions must start with `test_` (e.g., test_valid_login ✓)
- pytest automatically injects fixtures by parameter name
  (e.g., `page` and `credentials` come from conftest.py)

Why Page Object Model in tests:
- The test describes WHAT the user does, not HOW to click each element.
- If the UI changes, we update pages/login_page.py — not every test here.

Assertions philosophy (Playwright):
- Prefer `expect(locator).to_...()` over raw Python `assert` for UI checks.
- `expect` auto-waits up to a timeout for the condition to become true,
  which eliminates flaky tests caused by timing/animation issues.
- Use plain `assert` only for non-UI checks (e.g., environment sanity).
"""

import re                                       # Regex for URL pattern matching

import allure                                   # Allure adapter — emits per-test labels
import pytest                                   # Test framework + markers
from playwright.sync_api import expect          # Auto-waiting assertions

from pages.login_page import LoginPage          # Our POM class


# ── Allure feature label (applies to every test in this module) ───────
# `pytestmark` is a pytest convention: any marker assigned to this name
# at module scope is applied to every test in the file. Putting the
# `@allure.feature(...)` decorator here means we don't have to repeat
# it on every test below. In the Allure report's Behaviors tab, every
# test here will appear under the "Login" feature group.
pytestmark = [allure.feature("Login")]


# ── Test Markers ──────────────────────────────────────────────────────
# pytest markers let us group tests and run subsets from the CLI:
#   pytest -m smoke        → run only smoke tests
#   pytest -m "login"      → run only login tests
# These markers are registered in pytest.ini (or can be added there later).


@allure.story("Valid login routes user to MainView")
# `@allure.story(...)` describes the user-facing scenario. Stories
# sit one level below `feature` in the Behaviors tab — so this test
# will show up under: Login > Valid login routes user to MainView.
@allure.severity(allure.severity_level.BLOCKER)
# Severity drives the colour-coded breakdowns in the Allure Graphs
# and Categories tabs. BLOCKER is the most severe: a failure here
# means the system is fundamentally unusable. Login is the front
# door — if it's broken, no other test even has a chance.
@allure.title("Valid credentials authenticate and route to #!MainView")
# `@allure.title(...)` overrides the long pytest function name in
# the report's test list. The function name remains verbose for
# code-search/grep, but the human reading the report sees a
# sentence-case description.
@pytest.mark.smoke          # Part of the fast smoke suite
@pytest.mark.critical       # Blocking priority — must pass
@pytest.mark.login          # Feature group
def test_valid_login_redirects_away_from_login_page(page, base_url, credentials):
    """
    Traces to: TC-PW-001 — Valid Login with Correct Credentials

    Scenario:
        Given the user is on the login page
        When they enter a valid company, username, and password
        And click the ENTER button
        Then they are authenticated and redirected away from /LoginView

    Why this test matters:
        This is the most critical test in the suite. If login is broken,
        no other authenticated feature can be tested. It's the first
        tripwire we want to trigger in CI when something regresses.

    Test data:
        Credentials come from the `credentials` fixture, which reads
        them from the .env file. NEVER hardcode credentials in tests.

    Fixtures used:
        page          — fresh Playwright page navigated to base_url
        base_url      — app root URL (e.g., https://portal.danaconnect.com/)
        credentials   — Credentials object with attributes:
                        company, username, password (password is masked
                        in repr, see conftest.py for why)
    """
    # ── Arrange ────────────────────────────────────────────────────
    # Build the page object. It wraps the raw Playwright `page`
    # with domain-specific methods like enter_company() and login().
    login_page = LoginPage(page)

    # Sanity check: the .env must actually contain credentials.
    # Without this, a missing .env would look like a login failure
    # instead of a configuration problem — confusing to debug.
    # We use plain `assert` here because this is an environment
    # check, not a UI wait.
    assert credentials.company, "COMPANY is not set in .env"
    assert credentials.username, "USERNAME is not set in .env"
    assert credentials.password, "PASSWORD is not set in .env"

    # Navigate explicitly to the login page (/LoginView).
    # The `page` fixture lands on base_url, but the DANAConnect
    # root URL does NOT auto-redirect to /LoginView — we discovered
    # this empirically on the first test run.
    login_page.navigate(base_url)

    # DANAConnect is a Vaadin/GWT single-page app — the login form
    # is rendered by JavaScript after the page loads. We wait for
    # the network to go idle so every Vaadin resource is fetched
    # before we try to interact with the form.
    page.wait_for_load_state("networkidle")

    # Confirm the login form is actually rendered before we interact.
    # `expect(...).to_be_visible()` auto-waits for the element to
    # appear, which handles slow network / page load gracefully.
    expect(page.locator(LoginPage.COMPANY_INPUT)).to_be_visible()
    expect(page.locator(LoginPage.USERNAME_INPUT)).to_be_visible()
    expect(page.locator(LoginPage.PASSWORD_INPUT)).to_be_visible()
    expect(page.locator(LoginPage.ENTER_BUTTON)).to_be_visible()

    # ── Act ────────────────────────────────────────────────────────
    # Perform the full login flow in one call. The page object's
    # login() method fills all three fields and clicks ENTER.
    login_page.login(
        company=credentials.company,
        username=credentials.username,
        password=credentials.password,
    )

    # ── Assert ─────────────────────────────────────────────────────
    # Successful login routes the user to the MainView.
    #
    # Why the "#!MainView" check (and not "URL changed away from /LoginView")?
    # DANAConnect is a Vaadin/GWT single-page app that uses HASH-BASED
    # ROUTING. The URL path stays as /LoginView forever — only the hash
    # fragment changes:
    #     Before login:  https://portal.danaconnect.com/LoginView
    #     After login:   https://portal.danaconnect.com/LoginView#!MainView
    # So the only reliable sign of a successful login is the presence
    # of "#!MainView" in the URL.
    #
    # `expect(page).to_have_url(regex)` is an auto-waiting assertion:
    # Playwright polls the URL for up to the default 5s timeout until
    # the regex matches. This naturally handles the small delay between
    # the click and the Vaadin client-side route change.
    expect(page).to_have_url(re.compile(r"#!MainView"))


@allure.story("Login page renders all 7 required elements")
@allure.severity(allure.severity_level.CRITICAL)
# CRITICAL (not BLOCKER) because a missing privacy link or footer
# is a serious regression but doesn't render the system unusable
# the way a broken login would. The choice mirrors the existing
# pytest markers below — this test does NOT have
# `@pytest.mark.critical`, while the valid-login test does.
@allure.title("All 7 login page elements are visible on a fresh visit")
@pytest.mark.smoke          # Part of the fast smoke suite
@pytest.mark.login          # Feature group
def test_all_login_page_elements_are_visible(page, base_url):
    """
    Traces to: TC-PW-002 — Verify All Login Page Elements Are Present

    Scenario:
        Given a fresh browser session (no cached company)
        When the user navigates to the /LoginView page
        Then all 7 login-page elements are visible:
            1. Company input field
            2. Username input field
            3. Password input field
            4. ENTER button
            5. Privacy Policy link
            6. Terms of Use link
            7. Copyright footer

    Why this test matters:
        This is a **pure UI verification** test — no login is performed.
        It catches regressions where a developer accidentally removes or
        hides a required element (e.g., the footer, the privacy link).
        Fast, credential-free, safe to run constantly.

    Why we don't need `credentials`:
        Unlike TC-PW-001, this test doesn't submit the form. It only
        asserts that the form is *drawn correctly*. So the `credentials`
        fixture is deliberately omitted from the parameter list.

    Fixtures used:
        page       — fresh Playwright page navigated to base_url
        base_url   — app root URL (for navigating to /LoginView)
    """
    # ── Arrange ────────────────────────────────────────────────────
    # Build the page object so we can use its selector constants.
    login_page = LoginPage(page)

    # Navigate to the login view. Same pattern as TC-PW-001 — the
    # base URL doesn't auto-redirect to /LoginView, so we go directly.
    login_page.navigate(base_url)

    # Wait for the Vaadin SPA to finish rendering its DOM before
    # asserting visibility. Without this, assertions might run while
    # the form is still being drawn.
    page.wait_for_load_state("networkidle")

    # ── Assert ─────────────────────────────────────────────────────
    # Assert each of the 7 required elements is visible.
    # We use `expect(...).to_be_visible()` which auto-waits up to 5s
    # for each element — essential for SPAs where DOM renders async.

    # 1. Company input (text input, first on page)
    expect(page.locator(LoginPage.COMPANY_INPUT)).to_be_visible()

    # 2. Username input (text input, second on page)
    expect(page.locator(LoginPage.USERNAME_INPUT)).to_be_visible()

    # 3. Password input (input[type="password"])
    expect(page.locator(LoginPage.PASSWORD_INPUT)).to_be_visible()

    # 4. ENTER button (Vaadin div.v-button with role="button")
    expect(page.locator(LoginPage.ENTER_BUTTON)).to_be_visible()

    # 5. Privacy Policy link. The selector uses a comma-separated list
    # covering both English ("Privacy Policy") and Spanish
    # ("Política de Privacidad") variants. `.first` picks the first
    # match so the assertion doesn't error on a multi-match locator.
    expect(page.locator(LoginPage.PRIVACY_POLICY_LINK).first).to_be_visible()

    # 6. Terms of Use link — same multi-language strategy as Privacy.
    expect(page.locator(LoginPage.TERMS_OF_USE_LINK).first).to_be_visible()

    # 7. Copyright footer. The Vaadin class `.v-label-Corp` uniquely
    # identifies the "DANAConnect Corp. All Rights Reserved" element,
    # avoiding collisions with the "Welcome to DANAConnect" caption
    # that also contains the brand name.
    expect(page.locator(LoginPage.FOOTER_TEXT)).to_be_visible()
