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
import pytest                      # The test framework itself
from dotenv import load_dotenv     # Reads .env file into environment variables
from playwright.sync_api import sync_playwright  # Playwright browser automation

# ── Load environment variables from .env file ──────────────────────────
# This reads the .env file in the project root and makes all variables
# available via os.getenv(). We go up 2 levels from this file's location
# to find the project root where .env lives.
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))


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


@pytest.fixture(scope="session")
def credentials():
    """
    Returns a dictionary with all login credentials from .env.

    We store credentials in a dictionary so tests can easily access
    any credential they need: credentials['company'], etc.

    scope="session" because credentials don't change between tests.
    """
    return {
        'company': os.getenv('COMPANY', ''),
        'username': os.getenv('USERNAME', ''),
        'password': os.getenv('PASSWORD', ''),
    }


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
       - headless=False means you can SEE the browser (useful for debugging)
       - Change to headless=True for CI/CD runs
    3. browser.new_context() creates an isolated browser session
    4. yield gives the context to the test
    5. After the test finishes, we close everything (cleanup)
    """
    with sync_playwright() as p:
        # Launch Chromium browser — set headless=True to run without UI
        browser = p.chromium.launch(headless=False)

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
