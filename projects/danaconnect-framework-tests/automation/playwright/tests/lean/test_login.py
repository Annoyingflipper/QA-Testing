"""Playwright login tests (lean — for learning version see tests/test_login.py)."""

import re

import pytest
from playwright.sync_api import expect

from pages.lean.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.login
def test_valid_login_redirects_away_from_login_page(page, base_url, credentials):
    # Traces to: TC-PW-001 — Valid Login with Correct Credentials
    login_page = LoginPage(page)

    assert credentials.company, "COMPANY is not set in .env"
    assert credentials.username, "USERNAME is not set in .env"
    assert credentials.password, "PASSWORD is not set in .env"

    login_page.navigate(base_url)
    page.wait_for_load_state("networkidle")

    expect(page.locator(LoginPage.COMPANY_INPUT)).to_be_visible()
    expect(page.locator(LoginPage.USERNAME_INPUT)).to_be_visible()
    expect(page.locator(LoginPage.PASSWORD_INPUT)).to_be_visible()
    expect(page.locator(LoginPage.ENTER_BUTTON)).to_be_visible()

    login_page.login(
        company=credentials.company,
        username=credentials.username,
        password=credentials.password,
    )

    # Vaadin SPA uses hash routing — "#!MainView" is the logged-in signal.
    expect(page).to_have_url(re.compile(r"#!MainView"))


@pytest.mark.smoke
@pytest.mark.login
def test_all_login_page_elements_are_visible(page, base_url):
    # Traces to: TC-PW-002 — Verify All Login Page Elements Are Present
    login_page = LoginPage(page)
    login_page.navigate(base_url)
    page.wait_for_load_state("networkidle")

    for selector in (
        LoginPage.COMPANY_INPUT,
        LoginPage.USERNAME_INPUT,
        LoginPage.PASSWORD_INPUT,
        LoginPage.ENTER_BUTTON,
        LoginPage.FOOTER_TEXT,
    ):
        expect(page.locator(selector)).to_be_visible()

    # Privacy/Terms selectors match in multiple languages — pick first.
    expect(page.locator(LoginPage.PRIVACY_POLICY_LINK).first).to_be_visible()
    expect(page.locator(LoginPage.TERMS_OF_USE_LINK).first).to_be_visible()
