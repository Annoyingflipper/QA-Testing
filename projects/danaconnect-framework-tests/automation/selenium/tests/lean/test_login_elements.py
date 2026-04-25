"""Selenium login-elements-present test (lean — for learning version see tests/test_login_elements.py)."""

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.lean.login_page import LoginPage


@pytest.fixture(scope="function")
def login_page(driver):
    return LoginPage(driver)


@pytest.mark.smoke
@pytest.mark.login
def test_all_login_page_elements_are_visible(driver, login_page, base_url):
    # Traces to: TC-SE-002 — Verify All Login Page Elements Are Present
    login_page.navigate(base_url)
    login_page.wait_for_form_rendered()

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
            pytest.fail(f"TC-SE-002 FAILED: '{name}' not visible within 10s. Locator: {locator}")

        assert element.is_displayed(), f"TC-SE-002 FAILED: '{name}' is_displayed() is False"
