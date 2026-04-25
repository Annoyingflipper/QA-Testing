"""Selenium valid-login test (lean — for learning version see tests/test_login_valid.py)."""

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.lean.login_page import LoginPage


@pytest.fixture(scope="function")
def login_page(driver):
    return LoginPage(driver)


@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.login
def test_valid_login_reaches_main_view(driver, login_page, base_url, credentials):
    # Traces to: TC-SE-001 — Valid Login with Correct Credentials
    assert credentials['company'], "COMPANY is not set in .env"
    assert credentials['username'], "USERNAME is not set in .env"
    assert credentials['password'], "PASSWORD is not set in .env"

    login_page.navigate(base_url)
    login_page.wait_for_form_rendered()

    login_page.login(
        company=credentials['company'],
        username=credentials['username'],
        password=credentials['password'],
    )

    # Vaadin SPA uses hash routing — "#!MainView" is the logged-in signal.
    try:
        WebDriverWait(driver, timeout=15).until(EC.url_contains("#!MainView"))
    except TimeoutException:
        pytest.fail(
            f"TC-SE-001 FAILED: URL did not reach '#!MainView' within 15s. "
            f"Current URL: {driver.current_url}"
        )

    assert "#!MainView" in driver.current_url, (
        f"Expected '#!MainView' in URL, got: {driver.current_url}"
    )
