"""
DANAConnect Framework Tests — Playwright Configuration (conftest.py)
====================================================================
This file is automatically loaded by pytest before running any tests.
It sets up shared fixtures (reusable setup/teardown code) that all
test files can use.

Key concepts:
- A "fixture" is a function that provides test data or setup.
- @pytest.fixture is a decorator that marks a function as a fixture.
- Fixtures can have different "scopes" (how long they live):
    - "session" = created once for the entire test run
    - "function" = created fresh for each individual test (default)
- yield pauses the fixture, runs the test, then resumes for cleanup.
"""

import os                          # For reading environment variables
import allure                      # Allure adapter — emits the per-test result JSON
import pytest                      # The test framework itself
from dotenv import load_dotenv     # Reads .env file into environment variables
from playwright.sync_api import sync_playwright  # Playwright browser automation

# ── Load environment variables from .env file ──────────────────────────
# This reads the .env file in the project root and makes all variables
# available via os.getenv(). We go up 2 levels from this file's location
# to find the project root where .env lives.
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))


@pytest.fixture(autouse=True)
def _allure_parent_suite():
    """
    Tag every test in this folder as belonging to the "Playwright"
    parent suite in the Allure report.

    Why this matters
    ----------------
    Allure's Suites tab has a 3-level hierarchy:
        parent_suite > suite > sub_suite
    Without `parent_suite`, pytest tests collapse into a single suite
    named after the parent directory ("tests"). When the combined
    report is generated from BOTH framework result dirs, the two
    `tests` suites merge — and you can no longer tell which test
    came from Playwright vs Selenium.

    Setting `parent_suite="Playwright"` here puts every test in this
    folder under a top-level "Playwright" group in the Suites tab.

    Why autouse=True
    ----------------
    `autouse=True` means pytest runs this fixture before every test
    automatically, without the test having to request it. Equivalent
    to decorating every test with @allure.parent_suite("Playwright")
    but without touching the test files.

    Why allure.dynamic instead of @allure.parent_suite
    --------------------------------------------------
    The decorator form (`@allure.parent_suite(...)`) is evaluated
    statically at collection time and needs to wrap each test.
    `allure.dynamic.parent_suite(...)` mutates the live test's
    labels at runtime. Either works, but the dynamic form lets us
    apply the label centrally from the conftest.
    """
    allure.dynamic.parent_suite("Playwright")


@pytest.fixture(scope="session")
def base_url():
    """
    Returns the base URL for the application under test.

    scope="session" means this fixture is created ONCE and shared
    across ALL tests in the entire test run. This is efficient because
    the URL doesn't change between tests.

    os.getenv() reads the value from the .env file (loaded above).
    The second argument is the default if the variable isn't set.
    """
    return os.getenv('BASE_URL', 'https://portal.danaconnect.com/')


class Credentials:
    """
    A bundle of login credentials with a SAFE repr.

    Why a class instead of a plain dict?
    ------------------------------------
    When a pytest test fails, pytest prints the values of every fixture
    the test received — including credentials. If credentials is a plain
    dict like {'password': 'mySecret123'}, the password ends up in:
        - Your terminal scrollback
        - CI log files (Jenkins, GitHub Actions, etc.)
        - Any screenshots of failed test output
        - Anywhere a teammate pastes the error message

    That's a real-world incident waiting to happen. This class overrides
    __repr__ to mask the password so failure output shows:
        Credentials(company='venturestars', username='vmaniglia', password='***')
    instead of leaking the real password.

    Tests access fields via attributes: creds.company, creds.password.
    """

    def __init__(self, company, username, password):
        # Store each field as a plain attribute — simple and explicit.
        self.company = company
        self.username = username
        self.password = password

    def __repr__(self):
        # __repr__ is what pytest prints in failure tracebacks.
        # We mask the password here so it NEVER appears in logs.
        # The company and username are considered low-sensitivity
        # so we leave them visible (helpful for debugging env issues).
        return (
            f"Credentials(company={self.company!r}, "
            f"username={self.username!r}, "
            f"password='***')"
        )


@pytest.fixture(scope="session")
def credentials():
    """
    Returns a Credentials object populated from .env.

    scope="session" because credentials don't change between tests —
    we read .env once and reuse the same object for the whole run.

    Usage in tests:
        def test_login(credentials):
            print(credentials.company)   # attribute access
            print(credentials.password)  # returns real password
            print(credentials)           # prints with password masked
    """
    return Credentials(
        company=os.getenv('COMPANY', ''),
        username=os.getenv('USERNAME', ''),
        password=os.getenv('PASSWORD', ''),
    )


@pytest.fixture(scope="function")
def browser_context(base_url):
    """
    Creates a fresh browser context for each test.

    scope="function" means EACH test gets its own browser context.
    This ensures tests don't share cookies, localStorage, or any
    browser state — each test starts completely clean.

    What happens here:
    1. sync_playwright() starts the Playwright engine
    2. p.chromium.launch() opens a Chromium browser
       - Headless is controlled by the HEADLESS env var. Default is
         True (headless), so CI containers without an X server work
         out of the box. For local debugging, run with HEADLESS=false
         to see the browser window — e.g. `HEADLESS=false pytest ...`.
    3. browser.new_context() creates an isolated browser session
    4. yield gives the context to the test
    5. After the test finishes, we close everything (cleanup)
    """
    # Read HEADLESS env var. We compare the lowercased value to 'false'
    # so any case (false/False/FALSE) turns headless OFF. Anything else
    # (including the value being unset entirely) keeps headless ON.
    headless = os.getenv('HEADLESS', 'true').lower() != 'false'

    with sync_playwright() as p:
        # Launch Chromium. headless=True hides the UI (required in CI
        # where there's no X server) and is meaningfully faster.
        # headless=False shows the window when debugging locally.
        browser = p.chromium.launch(headless=headless)

        # Create a new browser context (like an incognito window)
        # Each context has its own cookies, cache, and session storage
        context = browser.new_context()

        # Give this context to the test function
        yield context

        # ── Cleanup (runs after the test finishes) ──
        context.close()   # Close the browser context
        browser.close()   # Close the browser itself


@pytest.fixture(scope="function")
def page(browser_context, base_url):
    """
    Creates a new page (tab) within the browser context.

    This fixture depends on browser_context (it receives it as a parameter).
    pytest automatically figures out the dependency chain:
    1. First, create browser_context
    2. Then, create page using that context

    The page is navigated to the base_url automatically so every test
    starts on the application's home page.
    """
    # Create a new page (like opening a new tab)
    page = browser_context.new_page()

    # Navigate to the application URL before the test starts
    page.goto(base_url)

    # Give this page to the test function
    yield page

    # ── Cleanup ──
    page.close()  # Close the page after the test
