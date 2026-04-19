"""
DANAConnect — Selenium Tests — Valid Login
===========================================
This file contains the automated test for TC-SE-001: a positive login flow
that verifies a user with correct credentials is redirected away from the
login page (i.e., authentication succeeded).

Why this test exists
--------------------
Login is the front door. If this breaks, everything behind it is unreachable —
so it is marked Critical priority. We run it first as a smoke check.

How Selenium differs from Playwright (for learning)
---------------------------------------------------
- Selenium does NOT auto-wait. Every interaction that depends on the DOM
  being in a certain state must be wrapped in an explicit wait
  (WebDriverWait + expected_conditions). If we skip this, tests are flaky.
- Selenium uses find_element() with a (By, value) locator tuple. Playwright
  uses its own Locator API with auto-waiting.
- Selenium's send_keys() APPENDS text; we must call .clear() first
  (the page object handles this internally).
- Selenium returns WebElement objects; we interact with them via methods
  like .click(), .send_keys(), .is_displayed(), .get_attribute().

Author: Max (Selenium Test Writer)
"""

# ─── Standard library imports ───────────────────────────────────────────
# pytest is the test framework we use. It picks up any function named
# `test_*` in any file named `test_*.py` and runs it as a test.
import pytest

# ─── Selenium imports ───────────────────────────────────────────────────
# WebDriverWait: used to pause test execution until a condition is met,
#   up to a timeout. This is Selenium's primary mechanism for dealing with
#   asynchronous page behavior (e.g., redirects, dynamic content).
from selenium.webdriver.support.ui import WebDriverWait

# TimeoutException: raised by WebDriverWait when the condition is not met
#   within the given timeout. We catch this to provide a clearer error
#   message in our assertions.
from selenium.common.exceptions import TimeoutException

# ─── Page Object import ─────────────────────────────────────────────────
# We import the LoginPage POM, which encapsulates all locators and actions
# for the login page. This keeps the test itself clean and readable,
# and means if the login page's HTML changes, we only update one file.
from pages.login_page import LoginPage


# ─── Test-scoped fixture: login_page ────────────────────────────────────
# A pytest fixture is a reusable piece of setup code. By putting this in
# the test file (rather than conftest.py), it is only available to tests
# in this file. If later we share it across many login test files, we can
# move it into conftest.py.
#
# scope="function" means: create a new LoginPage instance for every test.
#   This matches the `driver` fixture in conftest.py (also function-scoped),
#   so every test gets a fresh browser AND a fresh page object.
@pytest.fixture(scope="function")
def login_page(driver):
    """
    Returns a LoginPage instance bound to the current WebDriver.

    Depends on the `driver` fixture (defined in conftest.py), which
    launches Chrome, maximizes the window, navigates to BASE_URL, and
    yields the driver to the test.
    """
    # We simply instantiate LoginPage with the driver. The LoginPage's
    # __init__ also creates a WebDriverWait for reuse across its methods.
    return LoginPage(driver)


# ─── THE TEST ───────────────────────────────────────────────────────────
# Traces to: TC-SE-001 — Valid Login with Correct Credentials
#
# Naming convention: test_<what>_<expected_outcome>
#   `test_valid_login_redirects_away_from_loginview` tells a reader
#   exactly what the test checks without reading the body.
def test_valid_login_redirects_away_from_loginview(driver, login_page, base_url, credentials):
    """
    TC-SE-001 — Verify that submitting valid credentials authenticates the
    user and redirects the browser away from /LoginView.

    Fixtures used:
        driver       — fresh Chrome WebDriver (from conftest.py)
        login_page   — LoginPage POM bound to the driver (from above)
        base_url     — e.g., "https://portal.danaconnect.com/" (from conftest)
        credentials  — dict with 'company', 'username', 'password' (from conftest,
                       populated from .env — NEVER hardcoded)
    """

    # ── STEP 0: Defensive guard — fail fast if credentials are missing ──
    # If the .env file is missing or incomplete, we want a clear error
    # message BEFORE we start typing empty strings into the form (which
    # would give a misleading failure about "login failed" rather than
    # "credentials not set").
    assert credentials['company'], (
        "COMPANY is missing from .env — cannot run TC-SE-001"
    )
    assert credentials['username'], (
        "USERNAME is missing from .env — cannot run TC-SE-001"
    )
    assert credentials['password'], (
        "PASSWORD is missing from .env — cannot run TC-SE-001"
    )

    # ── STEP 1: Navigate to the login page ──────────────────────────────
    # The driver fixture already navigated to base_url, but the app might
    # redirect us elsewhere if we land on "/". We explicitly navigate to
    # /LoginView to guarantee we start in a known state.
    #
    # LoginPage.navigate() calls driver.get(base_url + "/LoginView").
    # driver.get() BLOCKS until document.readyState == 'complete', so after
    # this line the DOM's initial HTML is loaded.
    login_page.navigate(base_url)

    # Capture the URL BEFORE login. We'll compare against this later to
    # detect the redirect. Using the driver's current_url (not a hardcoded
    # string) makes the test resilient to environment differences (e.g.,
    # staging vs. production base URLs).
    url_before_login = driver.current_url

    # ── STEP 2–5: Fill the form and submit ──────────────────────────────
    # LoginPage.login() is a convenience method that:
    #   1. Types the company code     (uses send_keys with explicit wait)
    #   2. Types the username         (uses send_keys with explicit wait)
    #   3. Types the password         (uses send_keys with explicit wait)
    #   4. Clicks the ENTER button    (waits for element_to_be_clickable)
    #
    # We pass credentials from the fixture — NEVER hardcoded strings.
    login_page.login(
        company=credentials['company'],
        username=credentials['username'],
        password=credentials['password'],
    )

    # ── ASSERTION: Wait for the URL to change ───────────────────────────
    # Post-login, the app should redirect us to the user's dashboard.
    # We don't know the exact dashboard URL (it may vary per account),
    # so we assert that the URL *changed* from /LoginView.
    #
    # WebDriverWait polls a condition repeatedly (every 500ms by default)
    # until either:
    #   (a) the condition returns a truthy value → wait returns that value
    #   (b) the timeout elapses → wait raises TimeoutException
    #
    # We use a timeout of 15 seconds — slightly longer than the default
    # WAIT_TIMEOUT because a real authentication request + redirect can
    # take a few seconds on a slow connection.
    wait = WebDriverWait(driver, timeout=15)

    try:
        # `lambda d: "/LoginView" not in d.current_url`
        # This lambda is evaluated on each poll. It returns True the moment
        # the URL no longer contains "/LoginView", which is our signal that
        # the redirect has happened.
        wait.until(lambda d: "/LoginView" not in d.current_url)
    except TimeoutException:
        # If we time out, capture the current URL and any visible error
        # text to give a useful failure message. pytest.fail() marks the
        # test as failed with a custom message.
        current_url = driver.current_url
        pytest.fail(
            f"TC-SE-001 FAILED: URL did not change away from /LoginView "
            f"within 15s. Current URL: {current_url}. "
            f"Possible causes: invalid credentials in .env, server error, "
            f"slow network, or an error message was shown instead."
        )

    # ── FINAL ASSERTION (belt-and-suspenders) ───────────────────────────
    # Even though WebDriverWait succeeded, we explicitly assert the final
    # state for clarity and to produce a readable failure message if the
    # URL somehow landed back on /LoginView (e.g., via a redirect loop).
    final_url = driver.current_url
    assert "/LoginView" not in final_url, (
        f"Expected to be redirected away from /LoginView, but final URL "
        f"was: {final_url}"
    )
    # Defensive: confirm we actually moved to a different URL, not just
    # a /LoginView variant that somehow passed the 'not in' check.
    assert final_url != url_before_login, (
        f"URL did not change after login. Before: {url_before_login}, "
        f"After: {final_url}"
    )
