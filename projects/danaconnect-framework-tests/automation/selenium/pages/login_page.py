"""
DANAConnect — Login Page Object (Selenium)
===========================================
Page Object Model for the login page using Selenium WebDriver.

Key differences from Playwright version:
- Selenium uses find_element() with By locator strategies
- Selenium does NOT auto-wait — we use WebDriverWait for explicit waits
- Selenium uses send_keys() instead of fill() to type text
- Selenium uses .click() directly on WebElements
- We must clear() fields before typing (send_keys appends by default)

By locator strategies explained:
- By.CSS_SELECTOR: Find elements using CSS selectors (most flexible)
- By.XPATH: Find elements using XPath expressions (powerful but verbose)
- By.ID: Find elements by their id attribute (fastest, but needs id)
- By.NAME: Find elements by their name attribute
- By.CLASS_NAME: Find elements by CSS class name
- By.LINK_TEXT: Find <a> elements by their visible text

Page: Login (/LoginView)
"""

from selenium.webdriver.common.by import By                   # Locator strategies
from selenium.webdriver.support.ui import WebDriverWait       # Explicit wait utility
from selenium.webdriver.support import expected_conditions as EC  # Wait conditions


class LoginPage:
    """
    Page Object for the DANAConnect login page (Selenium version).

    Uses explicit waits (WebDriverWait) to handle dynamic page loading.
    Each method waits for the element to be ready before interacting with it.
    """

    # ── URL ────────────────────────────────────────────────────────────
    URL_PATH = "/LoginView"

    # ── LOCATORS ───────────────────────────────────────────────────────
    # Defined as tuples of (By strategy, value) for use with find_element().
    # Using CSS selectors with placeholder attributes since the page
    # doesn't have data-testid attributes.
    COMPANY_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Enter your company code"]')
    USERNAME_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Enter your user name"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Enter your password DANA"]')
    ENTER_BUTTON = (By.CSS_SELECTOR, 'button')
    PRIVACY_POLICY_LINK = (By.LINK_TEXT, 'Privacy Policy')
    TERMS_OF_USE_LINK = (By.LINK_TEXT, 'Terms of Use of the Service')
    FOOTER_TEXT = (By.XPATH, '//*[contains(text(), "DANAConnect Corp. All Rights Reserved")]')

    # ── Wait timeout (seconds) ─────────────────────────────────────────
    # How long to wait for elements before throwing a TimeoutException
    WAIT_TIMEOUT = 10

    def __init__(self, driver):
        """
        Initialize the LoginPage with a Selenium WebDriver instance.

        Args:
            driver: A Selenium WebDriver object (controls the browser).
                    This is passed in from the test via the fixture.
        """
        self.driver = driver
        # WebDriverWait is used for explicit waits — we create it once
        # and reuse it across all methods in this page object.
        self.wait = WebDriverWait(driver, self.WAIT_TIMEOUT)

    def navigate(self, base_url):
        """
        Navigate directly to the login page.

        Args:
            base_url (str): The base URL of the application

        Selenium's get() method loads the URL and waits for the page
        to finish loading (document.readyState == 'complete').
        """
        self.driver.get(base_url + self.URL_PATH)

    def _wait_and_find(self, locator):
        """
        Wait for an element to be present, then return it.

        This is a helper method used internally by other methods.
        The underscore prefix (_) is a Python convention meaning
        "this method is for internal use, not meant to be called
        directly by tests."

        Args:
            locator: A tuple of (By strategy, value), e.g. (By.CSS_SELECTOR, 'input')

        Returns:
            WebElement: The found element

        Raises:
            TimeoutException: If the element isn't found within WAIT_TIMEOUT seconds
        """
        # EC.presence_of_element_located waits until the element exists in the DOM
        return self.wait.until(EC.presence_of_element_located(locator))

    def enter_company(self, company):
        """
        Type the company code into the Company input field.

        In Selenium, we must:
        1. Find the element (with explicit wait)
        2. Clear any existing text
        3. Send the new text via send_keys()

        Args:
            company (str): The company code to enter
        """
        element = self._wait_and_find(self.COMPANY_INPUT)
        element.clear()        # Remove any existing text first
        element.send_keys(company)  # Type the company code

    def enter_username(self, username):
        """
        Type the username into the Username input field.

        Args:
            username (str): The username to enter
        """
        element = self._wait_and_find(self.USERNAME_INPUT)
        element.clear()
        element.send_keys(username)

    def enter_password(self, password):
        """
        Type the password into the Password input field.

        Args:
            password (str): The password to enter
        """
        element = self._wait_and_find(self.PASSWORD_INPUT)
        element.clear()
        element.send_keys(password)

    def click_enter(self):
        """
        Click the ENTER button to submit the login form.

        We use EC.element_to_be_clickable instead of presence_of_element_located
        because we want to ensure the button is not just present but also
        enabled and visible before clicking.
        """
        button = self.wait.until(EC.element_to_be_clickable(self.ENTER_BUTTON))
        button.click()

    def login(self, company, username, password):
        """
        Perform a complete login by filling all fields and clicking ENTER.

        Convenience method that combines all individual steps.

        Args:
            company (str): The company code
            username (str): The username
            password (str): The password
        """
        self.enter_company(company)
        self.enter_username(username)
        self.enter_password(password)
        self.click_enter()

    # ── Element Verification Methods ───────────────────────────────────

    def is_company_field_visible(self):
        """Check if the Company input field is visible on the page."""
        try:
            element = self._wait_and_find(self.COMPANY_INPUT)
            return element.is_displayed()
        except Exception:
            return False

    def is_username_field_visible(self):
        """Check if the Username input field is visible on the page."""
        try:
            element = self._wait_and_find(self.USERNAME_INPUT)
            return element.is_displayed()
        except Exception:
            return False

    def is_password_field_visible(self):
        """Check if the Password input field is visible on the page."""
        try:
            element = self._wait_and_find(self.PASSWORD_INPUT)
            return element.is_displayed()
        except Exception:
            return False

    def is_enter_button_visible(self):
        """Check if the ENTER button is visible on the page."""
        try:
            element = self._wait_and_find(self.ENTER_BUTTON)
            return element.is_displayed()
        except Exception:
            return False

    def is_privacy_policy_visible(self):
        """Check if the Privacy Policy link is visible on the page."""
        try:
            element = self._wait_and_find(self.PRIVACY_POLICY_LINK)
            return element.is_displayed()
        except Exception:
            return False

    def is_terms_of_use_visible(self):
        """Check if the Terms of Use link is visible on the page."""
        try:
            element = self._wait_and_find(self.TERMS_OF_USE_LINK)
            return element.is_displayed()
        except Exception:
            return False

    def is_footer_visible(self):
        """Check if the footer text is visible on the page."""
        try:
            element = self._wait_and_find(self.FOOTER_TEXT)
            return element.is_displayed()
        except Exception:
            return False

    def get_company_placeholder(self):
        """Get the placeholder text of the Company input field."""
        element = self._wait_and_find(self.COMPANY_INPUT)
        return element.get_attribute('placeholder')

    def get_username_placeholder(self):
        """Get the placeholder text of the Username input field."""
        element = self._wait_and_find(self.USERNAME_INPUT)
        return element.get_attribute('placeholder')

    def get_password_placeholder(self):
        """Get the placeholder text of the Password input field."""
        element = self._wait_and_find(self.PASSWORD_INPUT)
        return element.get_attribute('placeholder')
