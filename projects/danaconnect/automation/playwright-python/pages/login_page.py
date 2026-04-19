# ============================================================
# LOGIN_PAGE.PY — Playwright Page Object for the Login Page
# ============================================================
# Same Page Object Model pattern as Selenium, but using
# Playwright's API. The structure is identical — only the
# "how we find and interact with elements" part changes.
#
# KEY DIFFERENCES FROM SELENIUM VERSION:
#
# Selenium:
#   element = WebDriverWait(driver, 10).until(
#       EC.element_to_be_clickable((By.CSS_SELECTOR, "input"))
#   )
#   element.clear()
#   element.send_keys("text")
#
# Playwright:
#   page.locator("input").fill("text")
#
# That's it. Playwright auto-waits for the element to be ready,
# auto-clears the field, and types the text. Much less code.
# ============================================================


class LoginPage:
    """
    Page Object for the DANAConnect login page (Playwright version).
    """

    def __init__(self, page):
        """
        Initialize with a Playwright Page object.

        'page' in Playwright = a browser tab. It's like Selenium's
        'driver' but with a more modern API.
        """
        self.page = page

        # ── LOCATORS ─────────────────────────────────────────
        # Playwright locators are created once and reused.
        # They don't search the DOM until you interact with them.
        # This is more efficient than Selenium's approach.
        # ─────────────────────────────────────────────────────

        self.company_input = page.locator("input[placeholder*='company' i]")
        self.username_input = page.locator("input[placeholder*='user' i]")
        self.password_input = page.locator("input[type='password']")
        self.enter_button = page.locator("button:has-text('ENTER')")
        self.privacy_policy = page.locator("text=Privacy Policy")
        self.terms_of_use = page.locator("text=Terms of Use")
        self.copyright = page.locator("text=All Rights Reserved")

    def navigate(self, base_url):
        """Open the login page."""
        self.page.goto(base_url)
        return self

    def enter_company_code(self, code):
        """
        Type company code into the field.

        .fill() in Playwright:
        1. Waits for the element to be visible
        2. Clears any existing text
        3. Types the new text
        All in one call. Compare to Selenium where we needed 3 lines.
        """
        self.company_input.fill(code)
        return self

    def enter_username(self, username):
        """Type username."""
        self.username_input.fill(username)
        return self

    def enter_password(self, password):
        """Type password."""
        self.password_input.fill(password)
        return self

    def click_enter(self):
        """Click the ENTER button."""
        self.enter_button.click()
        return self

    def submit_with_enter_key(self):
        """Submit form via keyboard Enter key."""
        self.password_input.press("Enter")
        return self

    def login(self, company_code, username, password):
        """Complete login flow."""
        self.enter_company_code(company_code)
        self.enter_username(username)
        self.enter_password(password)
        self.click_enter()
        return self

    # ── State Checks ─────────────────────────────────────────

    def is_loaded(self):
        """Check if login page is fully loaded."""
        try:
            self.company_input.wait_for(state="visible", timeout=10000)
            self.username_input.wait_for(state="visible", timeout=5000)
            self.password_input.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            return False

    def get_error_message(self):
        """Get error message text, or None if not displayed."""
        try:
            error = self.page.locator("[class*='error'], [class*='alert'], [role='alert']")
            error.wait_for(state="visible", timeout=5000)
            return error.text_content()
        except Exception:
            return None

    def is_password_masked(self):
        """Verify password field type is 'password'."""
        return self.password_input.get_attribute("type") == "password"

    def get_placeholder(self, field_name):
        """Get placeholder text for a field."""
        locators = {
            "company": self.company_input,
            "username": self.username_input,
            "password": self.password_input,
        }
        return locators[field_name].get_attribute("placeholder")

    def take_screenshot(self, name="screenshot"):
        """
        Playwright has built-in screenshot support.
        This is useful for visual regression testing (Riley's domain)
        and for attaching evidence to bug reports.
        """
        self.page.screenshot(path=f"reports/{name}.png", full_page=True)
