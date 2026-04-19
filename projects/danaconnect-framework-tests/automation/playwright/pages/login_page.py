"""
DANAConnect — Login Page Object (Playwright)
=============================================
This file implements the Page Object Model (POM) pattern for the login page.

What is Page Object Model?
- It's a design pattern where each web page gets its own Python class.
- The class contains all the locators (how to find elements) and
  actions (what you can do on the page) in one place.
- If the UI changes, you only update THIS file — not every test.

Why use POM?
- Maintainability: Change a locator once, not in 50 test files.
- Readability: Tests read like English: login_page.enter_username("john")
- Reusability: Multiple tests can use the same page object.

Page: Login (/LoginView)
Elements found during reconnaissance:
- Company field: text input, placeholder "Enter your company code"
- Username field: text input, placeholder "Enter your user name"
- Password field: password input, placeholder "Enter your password DANA"
- ENTER button: submits the login form
- Privacy Policy link
- Terms of Use link
- Footer text
"""


class LoginPage:
    """
    Page Object for the DANAConnect login page.

    Each method represents an action a user can take on this page.
    Locators (how to find elements) are defined at the top as constants
    so they're easy to find and update when the UI changes.
    """

    # ── URL ────────────────────────────────────────────────────────────
    # The path portion of the login page URL (appended to base_url)
    URL_PATH = "/LoginView"

    # ── LOCATORS ───────────────────────────────────────────────────────
    # These are CSS selectors or Playwright locators used to find elements.
    # We use placeholder text as locators since the page doesn't have
    # data-testid attributes. If the placeholders change, update here only.
    COMPANY_INPUT = 'input[placeholder="Enter your company code"]'
    USERNAME_INPUT = 'input[placeholder="Enter your user name"]'
    PASSWORD_INPUT = 'input[placeholder="Enter your password DANA"]'
    ENTER_BUTTON = 'button:has-text("ENTER")'
    PRIVACY_POLICY_LINK = 'text=Privacy Policy'
    TERMS_OF_USE_LINK = 'text=Terms of Use of the Service'
    FOOTER_TEXT = 'text=DANAConnect Corp. All Rights Reserved'

    def __init__(self, page):
        """
        Initialize the LoginPage with a Playwright page object.

        Args:
            page: A Playwright Page object (represents a browser tab).
                  This is passed in from the test via the fixture.
        """
        self.page = page

    def navigate(self):
        """
        Navigate directly to the login page.

        Uses page.goto() which loads the URL and waits for the page
        to reach the 'load' state (all resources loaded).
        """
        self.page.goto(self.page.url.split('/LoginView')[0] + self.URL_PATH)

    def enter_company(self, company):
        """
        Type the company code into the Company input field.

        Args:
            company (str): The company code to enter (e.g., "venturestars")

        Playwright's fill() method:
        - First clears any existing text in the field
        - Then types the new text
        - Automatically waits for the element to be visible and enabled
        """
        self.page.fill(self.COMPANY_INPUT, company)

    def enter_username(self, username):
        """
        Type the username into the Username input field.

        Args:
            username (str): The username to enter (e.g., "vmaniglia")
        """
        self.page.fill(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        """
        Type the password into the Password input field.

        Args:
            password (str): The password to enter
        """
        self.page.fill(self.PASSWORD_INPUT, password)

    def click_enter(self):
        """
        Click the ENTER button to submit the login form.

        Playwright's click() method:
        - Waits for the element to be visible and enabled
        - Scrolls the element into view if needed
        - Clicks the center of the element
        """
        self.page.click(self.ENTER_BUTTON)

    def login(self, company, username, password):
        """
        Perform a complete login by filling all fields and clicking ENTER.

        This is a convenience method that combines all the individual
        steps into one call. Tests that just need to log in can call:
            login_page.login("venturestars", "user", "pass")

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
    # These methods check if elements exist on the page.
    # They return True/False and are used in assertion tests.

    def is_company_field_visible(self):
        """Check if the Company input field is visible on the page."""
        return self.page.is_visible(self.COMPANY_INPUT)

    def is_username_field_visible(self):
        """Check if the Username input field is visible on the page."""
        return self.page.is_visible(self.USERNAME_INPUT)

    def is_password_field_visible(self):
        """Check if the Password input field is visible on the page."""
        return self.page.is_visible(self.PASSWORD_INPUT)

    def is_enter_button_visible(self):
        """Check if the ENTER button is visible on the page."""
        return self.page.is_visible(self.ENTER_BUTTON)

    def is_privacy_policy_visible(self):
        """Check if the Privacy Policy link is visible on the page."""
        return self.page.is_visible(self.PRIVACY_POLICY_LINK)

    def is_terms_of_use_visible(self):
        """Check if the Terms of Use link is visible on the page."""
        return self.page.is_visible(self.TERMS_OF_USE_LINK)

    def is_footer_visible(self):
        """Check if the footer text is visible on the page."""
        return self.page.is_visible(self.FOOTER_TEXT)

    def get_company_placeholder(self):
        """Get the placeholder text of the Company input field."""
        return self.page.get_attribute(self.COMPANY_INPUT, 'placeholder')

    def get_username_placeholder(self):
        """Get the placeholder text of the Username input field."""
        return self.page.get_attribute(self.USERNAME_INPUT, 'placeholder')

    def get_password_placeholder(self):
        """Get the placeholder text of the Password input field."""
        return self.page.get_attribute(self.PASSWORD_INPUT, 'placeholder')
