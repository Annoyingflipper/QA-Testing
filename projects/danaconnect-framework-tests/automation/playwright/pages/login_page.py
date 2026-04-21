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

DANAConnect is a **Vaadin/GWT application**. That shapes our locator
strategy because:
- Inputs have NO `placeholder`, `name`, or `aria-label` attributes.
- IDs look like `gwt-uid-9`, `gwt-uid-11` — auto-generated and will
  change between releases, so we cannot pin to them.
- The "ENTER" button is a `<div class="v-button">` with role="button",
  NOT a native `<button>` element.
- Field labels are rendered as sibling `<span class="v-caption">`
  elements inside a Vaadin FormLayout `<tr>` row:
      <tr>
        <td class="v-formlayout-captioncell"><span class="v-caption">COMPANY*</span></td>
        <td class="v-formlayout-contentcell"><input ...></td>
      </tr>

Fresh-session form (what a new browser context sees) has 3 inputs:
- Company (labelled "COMPANY*")  — text input
- Username (labelled "Usuario*") — text input
- Password (labelled "Contraseña*") — password input
- ENTER button (text "ENTER")

Cached-session form (after login-company cookie is set) shows only
2 inputs (Username + Password), because the company is remembered.
Tests should always use a fresh browser context to guarantee the
3-field form.
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
    # Locator strategy: POSITIONAL for text inputs, TYPE-based for password.
    #
    # Why not label text?
    # DANAConnect renders login labels in different languages depending
    # on the session locale: we've observed "COMPANY"/"Usuario"/"Contraseña"
    # in Spanish-preference sessions and "COMPANY"/"USERNAME"/"PASSWORD" in
    # fresh English sessions (which Playwright's default context uses).
    # Pinning locators to label text is brittle across locales.
    #
    # Why positional is safe here:
    # The 3-field login form always renders inputs in the same DOM order:
    #   Row 1: Company  (first text input)
    #   Row 2: Username (second text input)
    #   Row 3: Password (the only password input)
    # Playwright's `:nth-match(selector, N)` pseudo-class (1-indexed)
    # picks the N-th match across the whole document.
    COMPANY_INPUT = ':nth-match(input[type="text"], 1)'
    USERNAME_INPUT = ':nth-match(input[type="text"], 2)'

    # Password is uniquely identified by input type — there's only one
    # password field on the page, so this is the cleanest selector.
    PASSWORD_INPUT = 'input[type="password"]'

    # The ENTER button is a <div class="v-button" role="button">, NOT a
    # native <button>. There's only one such element on the login page,
    # so we select by class + role. Text could be "ENTER" (English session)
    # or "ENTRAR" (Spanish session), so we deliberately do NOT pin by text.
    ENTER_BUTTON = '.v-button[role="button"]'

    # Footer links are rendered as .v-caption spans with a specific class.
    # We match by partial text to handle both English and Spanish versions
    # ("Privacy Policy" / "Política de Privacidad").
    PRIVACY_POLICY_LINK = '.v-caption-label-signIn-company:has-text("Privacy Policy"), .v-caption-label-signIn-company:has-text("Política")'
    TERMS_OF_USE_LINK = '.v-caption-label-signIn-company:has-text("Terms of Use"), .v-caption-label-signIn-company:has-text("Términos")'

    # Copyright footer — rendered as <div class="v-label Corp v-label-Corp ...">.
    # Text: "DANAConnect Corp. All Rights Reserved". We select by the
    # stable Vaadin class name `.v-label-Corp` to avoid matching other
    # elements on the page that also mention "DANAConnect" (like the
    # "Welcome to DANAConnect" greeting caption).
    FOOTER_TEXT = '.v-label-Corp'

    def __init__(self, page):
        """
        Initialize the LoginPage with a Playwright page object.

        Args:
            page: A Playwright Page object (represents a browser tab).
                  This is passed in from the test via the fixture.
        """
        self.page = page

    def navigate(self, base_url):
        """
        Navigate directly to the login page.

        Args:
            base_url (str): The application's base URL
                            (e.g., "https://portal.danaconnect.com/")

        Uses page.goto() which loads the URL and waits for the page
        to reach the 'load' state (all resources loaded).

        We strip any trailing slash from base_url before appending
        URL_PATH so we never produce double-slash URLs like
        "https://portal.danaconnect.com//LoginView".
        """
        self.page.goto(base_url.rstrip("/") + self.URL_PATH)

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
