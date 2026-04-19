# ============================================================
# TEST_LOGIN_SECURITY.PY — Security tests for the login page
# ============================================================
# Owner: Sam (Security QA)
# Framework: Python + Selenium + pytest
#
# These tests cover OWASP Top 10 concerns for the login flow:
# - Injection (SQL, XSS)
# - Broken Authentication
# - Security Misconfiguration
#
# IMPORTANT: These tests are AUTHORIZED testing against
# the DANAConnect platform. They test for vulnerabilities
# by submitting malicious-looking input and verifying the
# application handles it safely. They do NOT exploit or
# cause damage.
# ============================================================

import pytest
from pages.login_page import LoginPage


class TestSQLInjection:
    """
    TC-SEC-001, 002, 003: SQL injection testing on all login fields.

    SQL injection is when an attacker puts SQL database commands
    into an input field, hoping the application will accidentally
    run them. Example: typing ' OR '1'='1 as a password might
    trick a badly-built login into thinking you're authenticated.

    WHAT WE'RE TESTING: That the application does NOT fall for this.
    A passing test means the injection was BLOCKED.
    """

    # ── Parameterized tests ──────────────────────────────────
    # pytest.mark.parametrize lets us run the SAME test function
    # with DIFFERENT inputs, without writing separate functions.
    #
    # Each tuple in the list becomes a separate test run.
    # So this one function actually runs 8 different tests!
    # ─────────────────────────────────────────────────────────

    SQL_PAYLOADS = [
        ("' OR '1'='1", "Classic OR-based bypass"),
        ("' OR '1'='1' --", "Comment-based bypass"),
        ("' UNION SELECT null,null,null --", "Union-based extraction"),
        ("admin'--", "Auth bypass via comment"),
        ("' OR 1=1#", "MySQL comment variation"),
        ("1' AND SLEEP(5) --", "Time-based blind injection"),
        ("'; SELECT * FROM users; --", "Stacked query attempt"),
        ("%27%20OR%20%271%27%3D%271", "URL-encoded injection"),
    ]

    @pytest.mark.security
    @pytest.mark.parametrize("payload,description", SQL_PAYLOADS)
    def test_sql_injection_company_field(self, browser, base_url, payload, description):
        """
        TC-SEC-001: SQL injection in the company code field.

        For each payload, we:
        1. Enter the malicious string as the company code
        2. Submit the form
        3. Verify login was REJECTED (not bypassed)
        4. Verify no SQL error messages leaked to the page
        """
        login_page = LoginPage(browser)
        login_page.navigate(base_url)

        login_page.login(
            company_code=payload,
            username="testuser",
            password="testpass"
        )

        # The page source should NEVER contain database error strings
        page_source = browser.page_source.lower()
        dangerous_strings = [
            "sql", "syntax", "mysql", "postgresql", "oracle",
            "database", "query", "select", "table", "column",
            "exception", "stack trace", "internal server error"
        ]

        for danger in dangerous_strings:
            assert danger not in page_source, \
                f"CRITICAL: SQL error leaked for payload '{description}': found '{danger}' in page"

        # Should still be on login page (injection did not bypass auth)
        assert login_page.is_loaded(), \
            f"CRITICAL: Page crashed or redirected after SQL injection: {description}"

    @pytest.mark.security
    @pytest.mark.parametrize("payload,description", SQL_PAYLOADS)
    def test_sql_injection_username_field(self, browser, base_url, payload, description):
        """TC-SEC-002: SQL injection in the username field."""
        login_page = LoginPage(browser)
        login_page.navigate(base_url)

        login_page.login(
            company_code="TESTCOMPANY",
            username=payload,
            password="testpass"
        )

        page_source = browser.page_source.lower()
        for danger in ["sql", "syntax", "mysql", "database", "exception"]:
            assert danger not in page_source, \
                f"CRITICAL: SQL error leaked in username field: {description}"

        assert login_page.is_loaded(), \
            f"Page crashed after SQL injection in username: {description}"

    @pytest.mark.security
    @pytest.mark.parametrize("payload,description", SQL_PAYLOADS)
    def test_sql_injection_password_field(self, browser, base_url, payload, description):
        """TC-SEC-003: SQL injection in the password field."""
        login_page = LoginPage(browser)
        login_page.navigate(base_url)

        login_page.login(
            company_code="TESTCOMPANY",
            username="testuser",
            password=payload
        )

        page_source = browser.page_source.lower()
        for danger in ["sql", "syntax", "mysql", "database", "exception"]:
            assert danger not in page_source, \
                f"CRITICAL: SQL error leaked in password field: {description}"

        assert login_page.is_loaded(), \
            f"Page crashed after SQL injection in password: {description}"


class TestXSSInjection:
    """
    TC-SEC-004, 005, 006: Cross-Site Scripting (XSS) testing.

    XSS is when an attacker injects JavaScript code into a page.
    If the application displays user input without sanitizing it,
    the script runs in other users' browsers — stealing cookies,
    redirecting to phishing sites, etc.

    WHAT WE'RE TESTING: That our injected scripts do NOT execute.
    """

    XSS_PAYLOADS = [
        ("<script>alert('XSS')</script>", "Basic script tag"),
        ("<img src=x onerror=alert('XSS')>", "Image error handler"),
        ("javascript:alert('XSS')", "JavaScript protocol"),
        ("<svg onload=alert('XSS')>", "SVG onload event"),
        ("'><script>alert('XSS')</script>", "Attribute breakout"),
        ("<body onload=alert('XSS')>", "Body onload"),
    ]

    @pytest.mark.security
    @pytest.mark.parametrize("payload,description", XSS_PAYLOADS)
    def test_xss_company_field(self, browser, base_url, payload, description):
        """TC-SEC-004: XSS injection in the company code field."""
        login_page = LoginPage(browser)
        login_page.navigate(base_url)

        login_page.login(
            company_code=payload,
            username="testuser",
            password="testpass"
        )

        # Check that no JavaScript alert was triggered
        # If an alert popped up, Selenium would throw an UnexpectedAlertPresentException
        # But we also check the page source to see if our script was reflected unescaped
        page_source = browser.page_source

        # The payload should NOT appear unescaped in the page source
        # (It might appear HTML-encoded like &lt;script&gt; — that's SAFE)
        assert payload not in page_source, \
            f"CRITICAL: XSS payload reflected unescaped: {description}"

    @pytest.mark.security
    @pytest.mark.parametrize("payload,description", XSS_PAYLOADS)
    def test_xss_username_field(self, browser, base_url, payload, description):
        """TC-SEC-005: XSS injection in the username field."""
        login_page = LoginPage(browser)
        login_page.navigate(base_url)

        login_page.login(
            company_code="TESTCOMPANY",
            username=payload,
            password="testpass"
        )

        page_source = browser.page_source
        assert payload not in page_source, \
            f"CRITICAL: XSS payload reflected in username: {description}"


class TestHTTPSSecurity:
    """
    TC-SEC-010: HTTPS enforcement and transport security.
    """

    @pytest.mark.security
    @pytest.mark.smoke
    def test_https_enforced(self, browser, base_url):
        """
        TC-SEC-010: Verify the site uses HTTPS, not HTTP.

        HTTPS encrypts all traffic between the browser and server.
        Without it, passwords travel as plaintext over the network
        and anyone on the same WiFi could read them.
        """
        login_page = LoginPage(browser)
        login_page.navigate(base_url)

        current_url = login_page.get_current_url()
        assert current_url.startswith("https://"), \
            f"CRITICAL: Site is not using HTTPS! URL: {current_url}"

    @pytest.mark.security
    def test_password_not_in_url(self, browser, base_url):
        """
        Verify login doesn't pass credentials via URL parameters.

        Some badly-built login forms use GET requests, which put
        the username and password in the URL like:
        site.com/login?user=admin&pass=secret

        This is terrible because URLs are stored in browser history,
        server logs, and proxy logs.
        """
        login_page = LoginPage(browser)
        login_page.navigate(base_url)

        login_page.login(
            company_code="TESTCOMPANY",
            username="testuser",
            password="secretpassword123"
        )

        current_url = login_page.get_current_url()
        assert "secretpassword123" not in current_url, \
            "CRITICAL: Password is visible in the URL!"
        assert "testuser" not in current_url, \
            "WARNING: Username is visible in the URL"


class TestErrorMessageSecurity:
    """
    TC-SEC-016: Error messages must not leak information.

    An attacker can use different error messages to figure out
    valid company codes, usernames, etc. For example:
    - "Company not found" → Now they know to try different companies
    - "Wrong password" → Now they know the username IS valid

    The error should always be generic: "Invalid credentials"
    """

    @pytest.mark.security
    def test_error_messages_are_generic(self, browser, base_url):
        """
        TC-SEC-016: All invalid login attempts should show the
        same generic error message, regardless of which field was wrong.
        """
        login_page = LoginPage(browser)

        # Attempt 1: Invalid company
        login_page.navigate(base_url)
        login_page.login("BADCOMPANY", "user", "pass")
        error_bad_company = login_page.get_error_message()

        # Attempt 2: Invalid username
        login_page.navigate(base_url)
        login_page.login("TESTCOMPANY", "BADUSER", "pass")
        error_bad_user = login_page.get_error_message()

        # Attempt 3: Invalid password
        login_page.navigate(base_url)
        login_page.login("TESTCOMPANY", "user", "BADPASS")
        error_bad_pass = login_page.get_error_message()

        # All three error messages should be identical
        # (or all None if errors aren't shown — also acceptable)
        if error_bad_company and error_bad_user and error_bad_pass:
            assert error_bad_company == error_bad_user == error_bad_pass, \
                f"SECURITY: Error messages differ by input type!\n" \
                f"  Bad company: '{error_bad_company}'\n" \
                f"  Bad user:    '{error_bad_user}'\n" \
                f"  Bad pass:    '{error_bad_pass}'"
