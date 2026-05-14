"""
DANAConnect — Selenium Tests — Valid Login
===========================================
This file contains the automated test for **TC-SE-001**: the positive
login flow. It is the Selenium counterpart to Luna's Playwright
``TC-PW-001`` in ``automation/playwright/tests/test_login.py`` and
asserts the same thing: a user with valid credentials is authenticated
and the URL reaches the post-login route.

Why we assert ``#!MainView`` (not "URL changed away from /LoginView")
---------------------------------------------------------------------
DANAConnect is a **Vaadin 7 / GWT single-page app with hash-based
routing**. After a successful login the URL changes from::

    https://portal.danaconnect.com/LoginView

to::

    https://portal.danaconnect.com/LoginView#!MainView

The path portion — ``/LoginView`` — stays forever. Only the hash
fragment changes from empty to ``#!MainView``. That means the old
approach "wait until ``/LoginView`` is NOT in the URL" would time out
even on a successful login, because the path still says ``/LoginView``.

Luna caught this on 2026-04-21 (see ``test-plans/feature-login.md``).
The correct post-login signal is the PRESENCE of ``#!MainView`` in
the URL, which we wait for with ``EC.url_contains``.

Why this test matters
---------------------
Login is the front door. Every other authenticated test depends on
this one working. We mark it ``critical`` so it blocks release on
failure and ``smoke`` so it runs on every commit.

How Selenium differs from Playwright (for learning)
---------------------------------------------------
- Selenium does **not** auto-wait. Every DOM interaction must be
  wrapped in an explicit ``WebDriverWait`` — the POM handles that
  internally, but this test adds a top-level wait for the final
  URL change.
- Selenium has no equivalent of Playwright's
  ``page.wait_for_load_state("networkidle")``. The idiomatic
  substitute is "wait for the first element we plan to interact
  with" — the POM's ``wait_for_form_rendered()`` method.
- Selenium uses a ``driver`` object; Playwright uses a ``page``.
"""

# ── Standard-library and third-party imports ───────────────────────────
import allure                                                        # Allure adapter — emits per-test labels
import pytest                                                        # Test framework + markers


# ── Allure feature label (applies to every test in this module) ────────
# `pytestmark` is a pytest convention: any marker assigned to this name
# at module scope is applied to every test in the file. The Allure
# feature "Login" puts every test here under one "Login" group in the
# Behaviors tab. Story/severity decorators below add the next levels.
pytestmark = [allure.feature("Login")]

# ── Selenium imports ───────────────────────────────────────────────────
# ``WebDriverWait`` polls a condition at a fixed interval until it
# returns truthy or the timeout expires. ``EC.url_contains`` is a
# ready-made condition that returns True when the driver's current
# URL contains a given substring — perfect for our ``#!MainView``
# assertion.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException             # Cleaner failure message

# ── Page Object import ─────────────────────────────────────────────────
from pages.login_page import LoginPage


# ── Test-scoped fixture: login_page ────────────────────────────────────
# Defined inline (not in conftest.py) because it's only useful to
# login tests. If future test files need it too, we can promote it.
@pytest.fixture(scope="function")
def login_page(driver):
    """
    Build a ``LoginPage`` bound to the ``driver`` fixture.

    ``scope="function"`` matches the ``driver`` fixture in
    ``conftest.py`` so every test gets a fresh browser AND a fresh
    page object. No state leaks between tests.
    """
    return LoginPage(driver)


# ── THE TEST ───────────────────────────────────────────────────────────
# Markers make it easy to run subsets from the command line:
#   pytest -m smoke       → run only smoke tests
#   pytest -m critical    → run only release-blocking tests
#   pytest -m login       → run only login-feature tests
# The markers are registered in ``automation/selenium/pytest.ini`` so
# pytest does not emit a ``PytestUnknownMarkWarning``.
@allure.story("Valid login routes user to MainView")
# `@allure.story(...)` describes the user-facing scenario. Stories
# sit one level below `feature` in the Behaviors tab — this test
# appears under: Login > Valid login routes user to MainView. Same
# story name as the Playwright equivalent so the report can pivot
# on "same scenario, different framework".
@allure.severity(allure.severity_level.BLOCKER)
# BLOCKER is the highest severity — login is the front door, and
# every other authenticated test depends on it. Mirrors the
# `@pytest.mark.critical` marker below.
@allure.title("Valid credentials authenticate and reach #!MainView")
# `@allure.title(...)` overrides the verbose function name with
# a human-readable sentence in the Allure report's test list.
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.login
def test_valid_login_reaches_main_view(driver, login_page, base_url, credentials):
    """
    Traces to: TC-SE-001 — Valid Login with Correct Credentials

    Scenario:
        Given the user is on the /LoginView page
        When they enter a valid company, username, and password
        And click the ENTER button
        Then they are authenticated and the URL includes "#!MainView"

    Fixtures used:
        driver       — fresh Chrome WebDriver (from conftest.py)
        login_page   — LoginPage POM bound to the driver (above)
        base_url     — e.g. "https://portal.danaconnect.com/" (conftest)
        credentials  — dict with 'company', 'username', 'password'
                       (read from .env — NEVER hardcoded)
    """

    # ── STEP 0: Defensive guard — fail fast if .env is missing ──────────
    # Without this, an empty-string COMPANY would LOOK like a login
    # failure (bad credentials) rather than what it actually is
    # (misconfigured environment). Plain ``assert`` is appropriate
    # here because we are checking test-infrastructure state, not
    # the DOM.
    assert credentials['company'], (
        "COMPANY is missing from .env — cannot run TC-SE-001"
    )
    assert credentials['username'], (
        "USERNAME is missing from .env — cannot run TC-SE-001"
    )
    assert credentials['password'], (
        "PASSWORD is missing from .env — cannot run TC-SE-001"
    )

    # ── STEP 1: Navigate explicitly to /LoginView ──────────────────────
    # The ``driver`` fixture already opens ``base_url``, but Luna's
    # reconnaissance confirmed the DANAConnect root does NOT
    # auto-redirect to /LoginView. We call ``navigate`` to land on
    # the login page deterministically.
    login_page.navigate(base_url)

    # ── STEP 2: Wait for the Vaadin form to render ──────────────────────
    # DANAConnect is a JS-rendered SPA. ``driver.get()`` returns as
    # soon as the initial HTML is loaded, but the login inputs may
    # still be drawing. This call blocks until the Company input is
    # present in the DOM — our proxy for "form ready".
    login_page.wait_for_form_rendered()

    # ── STEP 3: Fill and submit the form ────────────────────────────────
    # The POM's ``login()`` method wraps send_keys + click with
    # explicit waits per field. If any field is slow to render, the
    # POM waits for it.
    login_page.login(
        company=credentials['company'],
        username=credentials['username'],
        password=credentials['password'],
    )

    # ── ASSERTION: URL reaches #!MainView ───────────────────────────────
    # Post-login Vaadin pushes the client-side route to ``#!MainView``.
    # We use ``EC.url_contains("#!MainView")`` — it polls
    # ``driver.current_url`` until the substring appears or the
    # timeout expires.
    #
    # Why 15s? A real authentication round-trip + client-side route
    # change can take a few seconds on a slow network. 15s gives us
    # generous headroom over the 10s default. If login is genuinely
    # broken, we still fail within a user-tolerable window.
    wait = WebDriverWait(driver, timeout=15)

    try:
        wait.until(EC.url_contains("#!MainView"))
    except TimeoutException:
        # Capture the current URL for a debuggable failure message.
        # pytest.fail() marks the test failed with a custom string —
        # the default TimeoutException repr would not show the URL.
        current_url = driver.current_url
        pytest.fail(
            "TC-SE-001 FAILED: URL did not reach '#!MainView' within 15s. "
            f"Current URL: {current_url}. "
            "Likely causes: invalid credentials in .env, server error, "
            "network slowness, or Vaadin rendered an inline error banner "
            "instead of routing forward."
        )

    # ── FINAL ASSERTION (belt-and-suspenders) ──────────────────────────
    # Even though WebDriverWait succeeded, we re-check the URL for a
    # crisp, readable failure message if something somehow regressed
    # between the wait and this line.
    final_url = driver.current_url
    assert "#!MainView" in final_url, (
        "Expected URL to contain '#!MainView' after successful login, "
        f"but final URL was: {final_url}"
    )
