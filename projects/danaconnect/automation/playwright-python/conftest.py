# ============================================================
# CONFTEST.PY — Playwright pytest configuration
# ============================================================
# Playwright's pytest plugin (pytest-playwright) provides
# built-in fixtures automatically:
#   - page: a browser tab ready to use
#   - browser: the browser instance
#   - context: the browser context (like an incognito window)
#
# We don't need to create our own browser fixture like we did
# with Selenium — Playwright handles it for us. But we add
# our own fixtures for project-specific things.
#
# KEY DIFFERENCE FROM SELENIUM:
# With Selenium, we wrote: driver.find_element(By.CSS_SELECTOR, "...")
# With Playwright, we write: page.locator("css=...")
# Playwright's locators auto-wait and auto-retry, making tests
# much less flaky (less "element not found" errors).
# ============================================================

import pytest
from dotenv import load_dotenv
import os

load_dotenv()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configure the browser context (like an incognito window).

    scope="session" means this runs ONCE for the entire test session,
    not once per test. All tests share these settings.

    We're overriding the built-in fixture to add our custom settings.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": False,  # We WANT to catch HTTPS issues
    }


@pytest.fixture
def base_url():
    """Base URL for the application under test."""
    return os.getenv("BASE_URL", "https://portal.danaconnect.com")


@pytest.fixture
def test_credentials():
    """Test account credentials from environment variables."""
    return {
        "company_code": os.getenv("TEST_COMPANY_CODE", ""),
        "username": os.getenv("TEST_USERNAME", ""),
        "password": os.getenv("TEST_PASSWORD", ""),
    }
