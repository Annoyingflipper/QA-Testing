"""
DANAConnect — Selenium Tests — Login Page Elements Present
===========================================================
Automated test for **TC-SE-002**: verify that all seven required
elements of the login page are rendered and visible on a fresh
browser context. This is the Selenium counterpart to Luna's
Playwright ``TC-PW-002`` in ``automation/playwright/tests/test_login.py``.

What this test checks (and what it deliberately does NOT check)
---------------------------------------------------------------
This is a **pure UI verification** — no form submission, no
credentials. It asserts that all seven mandatory page elements
are actually drawn:

    1. Company input field
    2. Username input field
    3. Password input field
    4. ENTER button
    5. Privacy Policy link
    6. Terms of Use link
    7. Copyright footer ("DANAConnect Corp. All Rights Reserved")

Because it does not submit the form, the test is fast, safe to
run in CI on every commit, and doesn't require ``.env`` credentials
— we deliberately do NOT include the ``credentials`` fixture in the
parameter list.

Why a fresh browser context matters
-----------------------------------
DANAConnect caches the company code after the first successful
login. A cached-context visitor sees a **2-field form** (Username
+ Password only) with no Company field. This test expects the
**3-field form**, so we rely on pytest's function-scoped ``driver``
fixture which starts a fresh Chrome every test.

Selenium implementation note
----------------------------
We use ``EC.visibility_of_element_located`` — not just
``presence_of_element_located`` — because a field that lives in
the DOM but is hidden via CSS is invisible to a real user. Tests
should agree with the user's perspective.
"""

import allure                                                        # Allure adapter — emits per-test labels
import pytest                                                        # Test framework + markers
from selenium.webdriver.support.ui import WebDriverWait              # Explicit wait
from selenium.webdriver.support import expected_conditions as EC     # Readable conditions
from selenium.common.exceptions import TimeoutException              # Debuggable failures

from pages.login_page import LoginPage                               # Our POM


# ── Allure feature label (applies to every test in this module) ────────
# Module-level `pytestmark` applies `@allure.feature("Login")` to every
# test in this file. In the Behaviors tab they show up under "Login"
# next to the valid-login test from test_login_valid.py.
pytestmark = [allure.feature("Login")]


# ── Test-scoped fixture: login_page ────────────────────────────────────
# Duplicated from ``test_login_valid.py`` because pytest fixtures
# defined at module scope are only visible in that module. When a
# third login test file appears, we'll promote this to conftest.py.
@pytest.fixture(scope="function")
def login_page(driver):
    """Return a ``LoginPage`` POM bound to the current ``driver``."""
    return LoginPage(driver)


# ── THE TEST ───────────────────────────────────────────────────────────
# This test is ``smoke`` (runs on every commit) and ``login`` (feature
# group), but NOT ``critical``. A missing privacy-link regression
# should not block a release the way a broken login would.
@allure.story("Login page renders all 7 required elements")
# Same story label as Playwright's elements test — lets the report
# pivot on "same scenario across frameworks".
@allure.severity(allure.severity_level.CRITICAL)
# CRITICAL (not BLOCKER) because a missing element is a serious
# regression but doesn't break the system the way a broken login
# would. The choice matches the absence of `@pytest.mark.critical`
# below: this test is smoke, not release-blocking.
@allure.title("All 7 login page elements are visible on a fresh visit")
@pytest.mark.smoke
@pytest.mark.login
def test_all_login_page_elements_are_visible(driver, login_page, base_url):
    """
    Traces to: TC-SE-002 — Verify All Login Page Elements Are Present

    Scenario:
        Given a fresh browser context (no cached company)
        When the user navigates to /LoginView
        Then all 7 required elements are visible:
            Company input, Username input, Password input,
            ENTER button, Privacy Policy link, Terms of Use link,
            Copyright footer.

    Fixtures used:
        driver       — fresh Chrome WebDriver (from conftest.py)
        login_page   — LoginPage POM bound to the driver
        base_url     — app root URL (for navigation)
    """
    # ── STEP 1: Navigate to /LoginView ─────────────────────────────────
    login_page.navigate(base_url)

    # ── STEP 2: Wait for the Vaadin form to finish rendering ───────────
    # The form is drawn by GWT client-side JavaScript. This waits
    # for the Company input to be present in the DOM — a reliable
    # "form ready" signal.
    login_page.wait_for_form_rendered()

    # ── STEP 3: Assert every required element is visible ───────────────
    # We iterate over the 7 expected elements in a single loop so
    # the test body stays small and easy to audit. We wait up to 10s
    # per element — each element gets its own WebDriverWait so a
    # slow-rendering footer can't steal budget from an earlier input.
    #
    # Using ``visibility_of_element_located`` (not just presence)
    # because an invisible element fails the "is visible to a user"
    # contract this test is asserting.
    required_elements = [
        ("Company input", LoginPage.COMPANY_INPUT),
        ("Username input", LoginPage.USERNAME_INPUT),
        ("Password input", LoginPage.PASSWORD_INPUT),
        ("ENTER button", LoginPage.ENTER_BUTTON),
        ("Privacy Policy link", LoginPage.PRIVACY_POLICY_LINK),
        ("Terms of Use link", LoginPage.TERMS_OF_USE_LINK),
        ("Copyright footer", LoginPage.FOOTER_TEXT),
    ]

    wait = WebDriverWait(driver, timeout=10)

    for name, locator in required_elements:
        try:
            element = wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            # pytest.fail() produces a clean, readable message that
            # names WHICH element failed. Without the custom message
            # we'd get a generic TimeoutException with only the
            # locator tuple, forcing the reader to cross-reference.
            pytest.fail(
                f"TC-SE-002 FAILED: '{name}' was not visible within 10s. "
                f"Locator: {locator}. The login page may be partially "
                "rendered or this element may have been removed from "
                "the build."
            )

        # Belt-and-suspenders: visibility_of_element_located already
        # calls is_displayed() internally, but asserting explicitly
        # here produces a crisper failure message if the element went
        # from visible → hidden between the wait and this check.
        assert element.is_displayed(), (
            f"TC-SE-002 FAILED: '{name}' was found but is_displayed()"
            f" returned False. Locator: {locator}."
        )
