# ============================================================
# TEST_LOGIN.PY — Playwright login tests
# ============================================================
# Owner: Jordan (Functional) + Sam (Security)
# Framework: Python + Playwright + pytest
#
# This covers the same test cases as the Selenium version, but
# demonstrates Playwright's approach. In a real project, you'd
# typically pick ONE framework — we're using both for learning.
#
# NOTICE HOW MUCH SHORTER these tests are compared to Selenium.
# That's Playwright's main advantage: less boilerplate code.
# ============================================================

import pytest
from pages.login_page import LoginPage


class TestLoginPage:
    """Functional tests for the login page using Playwright."""

    @pytest.mark.smoke
    def test_page_loads(self, page, base_url):
        """
        TC-FUNC-020: Login page loads with all elements.

        Notice: 'page' is a built-in Playwright fixture — we didn't
        create it. pytest-playwright gives it to us automatically.
        It's already a fresh browser tab, ready to use.
        """
        login = LoginPage(page)
        login.navigate(base_url)
        assert login.is_loaded()

    @pytest.mark.smoke
    def test_password_masked(self, page, base_url):
        """TC-SEC-009: Password field must be type='password'."""
        login = LoginPage(page)
        login.navigate(base_url)
        assert login.is_password_masked()

    def test_empty_submit_rejected(self, page, base_url):
        """TC-FUNC-005: Empty form submission should not log in."""
        login = LoginPage(page)
        login.navigate(base_url)
        login.click_enter()

        # Playwright's expect API — more readable assertions
        # page.url is a property that returns current URL
        assert "portal.danaconnect.com" in page.url

    def test_invalid_company(self, page, base_url):
        """TC-FUNC-002: Invalid company code rejected."""
        login = LoginPage(page)
        login.navigate(base_url)
        login.login("FAKECOMPANY", "user", "pass")

        # Wait a moment for any redirect or error
        page.wait_for_timeout(2000)
        assert "portal.danaconnect.com" in page.url

    def test_enter_key_submits(self, page, base_url):
        """TC-FUNC-016: Form submits when pressing Enter key."""
        login = LoginPage(page)
        login.navigate(base_url)
        login.enter_company_code("TEST")
        login.enter_username("user")
        login.enter_password("pass")
        login.submit_with_enter_key()
        # If no error, Enter key works

    @pytest.mark.smoke
    def test_screenshot_on_load(self, page, base_url):
        """
        Captures a baseline screenshot for visual regression.

        Handoff → Riley: Use this screenshot to compare against
        future test runs and detect unintended visual changes.

        Handoff → Casey: Integrate Playwright's visual comparison
        (page.screenshot + toMatchSnapshot) into CI pipeline.
        """
        login = LoginPage(page)
        login.navigate(base_url)
        login.take_screenshot("login_page_baseline")


class TestLoginSecurity:
    """Security tests using Playwright."""

    SQL_PAYLOADS = [
        "' OR '1'='1",
        "' OR '1'='1' --",
        "admin'--",
        "' UNION SELECT null --",
    ]

    @pytest.mark.security
    @pytest.mark.parametrize("payload", SQL_PAYLOADS)
    def test_sql_injection_blocked(self, page, base_url, payload):
        """TC-SEC-001-003: SQL injection should be blocked."""
        login = LoginPage(page)
        login.navigate(base_url)
        login.login(payload, payload, payload)

        # Page should not contain SQL error messages
        content = page.content().lower()
        assert "sql" not in content or "syntax" not in content
        assert login.is_loaded()  # Page should still work

    XSS_PAYLOADS = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert(1)>",
        "javascript:alert(1)",
    ]

    @pytest.mark.security
    @pytest.mark.parametrize("payload", XSS_PAYLOADS)
    def test_xss_blocked(self, page, base_url, payload):
        """TC-SEC-004-006: XSS should be blocked."""
        login = LoginPage(page)
        login.navigate(base_url)
        login.login(payload, "user", "pass")

        # The raw payload should not appear unescaped
        content = page.content()
        assert payload not in content

    @pytest.mark.security
    def test_https_enforced(self, page, base_url):
        """TC-SEC-010: Must use HTTPS."""
        login = LoginPage(page)
        login.navigate(base_url)
        assert page.url.startswith("https://")
