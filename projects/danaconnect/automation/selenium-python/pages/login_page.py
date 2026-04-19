# ============================================================
# LOGIN_PAGE.PY — Page Object Model for the Login Page
# ============================================================
# This is the "Page Object Model" (POM) pattern — the single
# most important design pattern in test automation.
#
# THE IDEA: Instead of putting element selectors and actions
# directly in test files, we create a class that represents
# the page. The class knows:
#   - WHERE elements are (selectors/locators)
#   - HOW to interact with them (methods like "enter_username")
#
# WHY? If the login page HTML changes (e.g., a field ID changes),
# we only fix it HERE, in one place — not in 50 test files.
#
# Think of it as a "remote control" for the page. Tests press
# buttons on the remote; the remote knows how to talk to the TV.
# ============================================================

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """
    Page Object for the DANAConnect login page.

    Each page in the application gets its own Page Object class.
    This class encapsulates all interactions with the login page.
    """

    # ── LOCATORS ─────────────────────────────────────────────
    # These tell Selenium HOW to find each element on the page.
    #
    # We identified these from reading the page's accessibility
    # tree (what we saw when we inspected portal.danaconnect.com).
    #
    # By.CSS_SELECTOR — finds elements using CSS selectors
    # By.XPATH — finds elements using XPath expressions
    #
    # We store them as class variables so they're easy to update
    # if the page structure changes.
    # ─────────────────────────────────────────────────────────

    COMPANY_INPUT = (By.CSS_SELECTOR, "input[type='text'][placeholder*='company']")
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[type='text'][placeholder*='user']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    ENTER_BUTTON = (By.XPATH, "//button[.//div[contains(text(),'ENTER')]]")
    PRIVACY_POLICY_LINK = (By.XPATH, "//*[contains(text(),'Privacy Policy')]")
    TERMS_OF_USE_LINK = (By.XPATH, "//*[contains(text(),'Terms of Use')]")
    COPYRIGHT_TEXT = (By.XPATH, "//*[contains(text(),'All Rights Reserved')]")

    def __init__(self, driver):
        """
        Initialize with a Selenium WebDriver instance.

        Args:
            driver: The browser instance (from our conftest fixture)
        """
        self.driver = driver
        # WebDriverWait gives us explicit waits — more precise than
        # implicit waits. We can say "wait up to 15 seconds for THIS
        # SPECIFIC element to be clickable."
        self.wait = WebDriverWait(driver, 15)

    # ── ACTIONS ──────────────────────────────────────────────
    # These are the things a user can DO on this page.
    # Each method represents one user action.
    # ─────────────────────────────────────────────────────────

    def navigate(self, base_url):
        """Open the login page in the browser."""
        self.driver.get(base_url)
        return self  # Return self so we can chain: page.navigate(url).enter_company("X")

    def enter_company_code(self, company_code):
        """
        Type a company code into the company field.

        We use 'explicit wait' here: wait until the element is
        clickable before trying to type. This prevents the common
        "element not yet loaded" error.
        """
        field = self.wait.until(
            EC.element_to_be_clickable(self.COMPANY_INPUT)
        )
        field.clear()          # Clear any existing text first
        field.send_keys(company_code)  # Type the company code
        return self

    def enter_username(self, username):
        """Type a username into the username field."""
        field = self.wait.until(
            EC.element_to_be_clickable(self.USERNAME_INPUT)
        )
        field.clear()
        field.send_keys(username)
        return self

    def enter_password(self, password):
        """Type a password into the password field."""
        field = self.wait.until(
            EC.element_to_be_clickable(self.PASSWORD_INPUT)
        )
        field.clear()
        field.send_keys(password)
        return self

    def click_enter(self):
        """Click the ENTER button to submit the login form."""
        button = self.wait.until(
            EC.element_to_be_clickable(self.ENTER_BUTTON)
        )
        button.click()
        return self

    def submit_with_enter_key(self):
        """
        Submit the form by pressing the Enter key on the keyboard.
        This tests that the form works without clicking the button
        (important for accessibility and keyboard users).
        """
        field = self.driver.find_element(*self.PASSWORD_INPUT)
        field.send_keys(Keys.RETURN)
        return self

    def login(self, company_code, username, password):
        """
        Complete login flow in one call — a convenience method.

        This combines multiple steps into one, so tests that just
        need to "log in and move on" don't repeat the same 4 lines.
        """
        self.enter_company_code(company_code)
        self.enter_username(username)
        self.enter_password(password)
        self.click_enter()
        return self

    # ── ASSERTIONS / STATE CHECKS ────────────────────────────
    # These check the current state of the page.
    # Tests call these to verify expected behavior.
    # ─────────────────────────────────────────────────────────

    def is_loaded(self):
        """Check if the login page is fully loaded and visible."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.COMPANY_INPUT))
            self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
            self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
            self.wait.until(EC.element_to_be_clickable(self.ENTER_BUTTON))
            return True
        except Exception:
            return False

    def get_error_message(self):
        """
        Get the text of any error message displayed after a failed login.

        Returns None if no error message is found (within 5 seconds).
        We use a short timeout here because we don't want the test
        to wait the full 15 seconds when we expect no error.
        """
        try:
            # This is a generic selector — we'll refine it once we
            # see the actual error message element on the page.
            error = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "[class*='error'], [class*='alert'], [role='alert']")
                )
            )
            return error.text
        except Exception:
            return None

    def get_current_url(self):
        """Return the current page URL (to check if login redirected)."""
        return self.driver.current_url

    def get_page_title(self):
        """Return the browser tab title."""
        return self.driver.title

    def is_password_masked(self):
        """
        Verify the password field uses type='password' (shows dots, not text).
        This is a security check — passwords should never be visible.
        """
        field = self.driver.find_element(*self.PASSWORD_INPUT)
        return field.get_attribute("type") == "password"

    def get_placeholder_text(self, field_name):
        """Get the placeholder text for a specific field."""
        locator_map = {
            "company": self.COMPANY_INPUT,
            "username": self.USERNAME_INPUT,
            "password": self.PASSWORD_INPUT,
        }
        field = self.driver.find_element(*locator_map[field_name])
        return field.get_attribute("placeholder")

    def is_privacy_policy_visible(self):
        """Check if the Privacy Policy link is visible."""
        try:
            return self.driver.find_element(*self.PRIVACY_POLICY_LINK).is_displayed()
        except Exception:
            return False

    def is_terms_of_use_visible(self):
        """Check if the Terms of Use link is visible."""
        try:
            return self.driver.find_element(*self.TERMS_OF_USE_LINK).is_displayed()
        except Exception:
            return False
