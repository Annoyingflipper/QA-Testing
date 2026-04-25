"""
DANAConnect Framework Tests — Selenium Configuration (conftest.py)
==================================================================
This file is automatically loaded by pytest before running any tests.
It provides shared fixtures for Selenium-based tests.

Key differences from Playwright:
- Selenium uses WebDriver to control browsers (older, more established)
- Selenium 4.6+ ships with built-in Selenium Manager, which automatically
  downloads the correct ChromeDriver — no third-party tool required.
- Selenium requires explicit waits (WebDriverWait) — it doesn't auto-wait
- Selenium uses find_element() instead of Playwright's locator system
"""

import os                          # For reading environment variables
import pytest                      # The test framework
from dotenv import load_dotenv     # Reads .env file into environment variables
from selenium import webdriver     # Selenium browser automation

# ── Load environment variables from .env file ──────────────────────────
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))


@pytest.fixture(scope="session")
def base_url():
    """
    Returns the base URL for the application under test.

    scope="session" = created once, shared across all tests.
    """
    return os.getenv('BASE_URL', 'https://portal.danaconnect.com/')


@pytest.fixture(scope="session")
def credentials():
    """
    Returns a dictionary with all login credentials from .env.

    scope="session" because credentials don't change between tests.
    """
    return {
        'company': os.getenv('COMPANY', ''),
        'username': os.getenv('USERNAME', ''),
        'password': os.getenv('PASSWORD', ''),
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Attach the test result to the request node so the ``driver``
    fixture can check whether the test failed during ``call``
    and save a screenshot + the page source before quitting the
    browser. Without this hook, we would have no debugging
    evidence when a test fails.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="function")
def driver(base_url, request):
    """
    Creates a fresh Chrome WebDriver instance for each test.

    scope="function" means EACH test gets its own browser.
    This ensures complete isolation — no shared cookies or state.

    How Selenium's driver setup works:
    1. Selenium Manager (built into Selenium 4.6+) detects the
       installed Chrome version and downloads the matching ChromeDriver
       automatically on first use. No service= argument needed.
    2. webdriver.Chrome() launches Chrome with that driver.
    3. implicitly_wait(10) tells Selenium to wait up to 10 seconds
       when looking for elements before throwing an error.
    4. maximize_window() makes the browser full-screen.
    5. get() navigates to the application URL.

    After the test:
    6. driver.quit() closes the browser and cleans up.
    """
    # ── Set up Chrome options ──
    options = webdriver.ChromeOptions()
    # Add --headless=new for CI/CD runs (no visible browser)
    # options.add_argument('--headless=new')

    # ── Create the WebDriver ──
    # Selenium Manager (built-in, no extra package) resolves and caches
    # the correct ChromeDriver binary under the hood.
    driver = webdriver.Chrome(options=options)

    # ── Configure the driver ──
    # implicit wait: if an element isn't found immediately, Selenium
    # will keep trying for up to 10 seconds before failing
    driver.implicitly_wait(10)

    # Make the browser window full-screen for consistent screenshots
    driver.maximize_window()

    # Navigate to the application's base URL
    driver.get(base_url)

    # Give this driver to the test function
    yield driver

    # ── On failure: capture screenshot and page source BEFORE quit ──
    # The ``pytest_runtest_makereport`` hook above attaches ``rep_call``
    # to the request node with the test's pass/fail status. If the
    # test failed, save artefacts into a ``screenshots/`` folder next
    # to this conftest so we can see what the browser looked like.
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call is not None and rep_call.failed:
        artefacts_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(artefacts_dir, exist_ok=True)
        safe_name = request.node.name.replace("/", "_")
        try:
            driver.save_screenshot(os.path.join(artefacts_dir, f"{safe_name}.png"))
            with open(os.path.join(artefacts_dir, f"{safe_name}.html"), "w") as f:
                f.write(driver.page_source)
            with open(os.path.join(artefacts_dir, f"{safe_name}.url.txt"), "w") as f:
                f.write(driver.current_url)
        except Exception:
            # Never let artefact capture mask the real test failure.
            pass

    # ── Cleanup (runs after the test finishes) ──
    driver.quit()  # Close the browser and end the WebDriver session
