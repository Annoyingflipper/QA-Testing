# ============================================================
# CONFTEST.PY — pytest's "shared setup" file
# ============================================================
# This is a special file that pytest automatically loads before
# running any tests. It contains "fixtures" — reusable setup/
# teardown code that tests can request by name.
#
# Think of fixtures like a restaurant kitchen: tests are the
# customers who order food. Fixtures prepare the ingredients
# (open browser, navigate to page) so each test starts ready.
# ============================================================

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os

# Load environment variables from .env file
# This keeps secrets (passwords, URLs) out of the code
load_dotenv()


# ── What is a fixture? ──────────────────────────────────────
# A fixture is a function decorated with @pytest.fixture.
# When a test function has a parameter with the same name as
# a fixture, pytest automatically calls the fixture and passes
# the result to the test. Magic!
#
# Example:
#   def test_login(browser):  ← "browser" matches the fixture name below
#       browser.get(url)       ← pytest gave us a ready-to-use browser
# ─────────────────────────────────────────────────────────────


@pytest.fixture(scope="function")
def browser():
    """
    Creates a fresh Chrome browser for each test function.

    scope="function" means: open a NEW browser for every single test,
    then close it when that test finishes. This ensures tests don't
    affect each other (clean slate every time).

    The 'yield' keyword is important:
    - Everything BEFORE yield = setup (open browser)
    - Everything AFTER yield = teardown (close browser)
    """

    # ── Configure Chrome options ─────────────────────────────
    chrome_options = Options()

    # "--headless" means: run Chrome without showing a window.
    # Useful for CI/CD (Jenkins) where there's no screen.
    # Comment this out if you want to SEE the browser during tests:
    # chrome_options.add_argument("--headless")

    # These options make Chrome more stable in automated environments:
    chrome_options.add_argument("--no-sandbox")           # Required for some Linux environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevents crashes in Docker
    chrome_options.add_argument("--window-size=1920,1080")  # Consistent viewport size

    # ── Create the browser instance ──────────────────────────
    # ChromeDriverManager automatically downloads the correct
    # ChromeDriver version to match your Chrome browser.
    # Without this, you'd have to manually download drivers.
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Set how long Selenium waits for elements before giving up.
    # "Implicit wait" means: if an element isn't found immediately,
    # keep trying for up to 10 seconds before raising an error.
    driver.implicitly_wait(10)

    # ── Hand the browser to the test ─────────────────────────
    yield driver  # ← The test runs here, using 'driver' as 'browser'

    # ── Cleanup after the test finishes ──────────────────────
    driver.quit()  # Close the browser and free resources


@pytest.fixture
def base_url():
    """
    Returns the base URL for the application under test.

    We read it from environment variables (.env file) so we can
    easily switch between environments (staging, production)
    without changing code.
    """
    return os.getenv("BASE_URL", "https://portal.danaconnect.com")


@pytest.fixture
def test_credentials():
    """
    Returns test account credentials from environment variables.

    NEVER hardcode passwords in test files! They go in .env
    (which is in .gitignore, so it never gets committed to git).
    """
    return {
        "company_code": os.getenv("TEST_COMPANY_CODE", ""),
        "username": os.getenv("TEST_USERNAME", ""),
        "password": os.getenv("TEST_PASSWORD", ""),
    }
