"""DANAConnect login page object (Vaadin/GWT)."""


class LoginPage:
    """Page Object for the /LoginView login form."""

    URL_PATH = "/LoginView"

    # Positional selectors — labels change language, DOM order doesn't.
    COMPANY_INPUT = ':nth-match(input[type="text"], 1)'
    USERNAME_INPUT = ':nth-match(input[type="text"], 2)'
    PASSWORD_INPUT = 'input[type="password"]'
    # ENTER button is a Vaadin <div>, not a native <button>.
    ENTER_BUTTON = '.v-button[role="button"]'
    PRIVACY_POLICY_LINK = '.v-caption-label-signIn-company:has-text("Privacy Policy"), .v-caption-label-signIn-company:has-text("Política")'
    TERMS_OF_USE_LINK = '.v-caption-label-signIn-company:has-text("Terms of Use"), .v-caption-label-signIn-company:has-text("Términos")'
    FOOTER_TEXT = '.v-label-Corp'

    def __init__(self, page):
        self.page = page

    def navigate(self, base_url):
        self.page.goto(base_url.rstrip("/") + self.URL_PATH)

    def enter_company(self, company):
        self.page.fill(self.COMPANY_INPUT, company)

    def enter_username(self, username):
        self.page.fill(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        self.page.fill(self.PASSWORD_INPUT, password)

    def click_enter(self):
        self.page.click(self.ENTER_BUTTON)

    def login(self, company, username, password):
        self.enter_company(company)
        self.enter_username(username)
        self.enter_password(password)
        self.click_enter()

    def is_company_field_visible(self):
        return self.page.is_visible(self.COMPANY_INPUT)

    def is_username_field_visible(self):
        return self.page.is_visible(self.USERNAME_INPUT)

    def is_password_field_visible(self):
        return self.page.is_visible(self.PASSWORD_INPUT)

    def is_enter_button_visible(self):
        return self.page.is_visible(self.ENTER_BUTTON)

    def is_privacy_policy_visible(self):
        return self.page.is_visible(self.PRIVACY_POLICY_LINK)

    def is_terms_of_use_visible(self):
        return self.page.is_visible(self.TERMS_OF_USE_LINK)

    def is_footer_visible(self):
        return self.page.is_visible(self.FOOTER_TEXT)

    def get_company_placeholder(self):
        return self.page.get_attribute(self.COMPANY_INPUT, 'placeholder')

    def get_username_placeholder(self):
        return self.page.get_attribute(self.USERNAME_INPUT, 'placeholder')

    def get_password_placeholder(self):
        return self.page.get_attribute(self.PASSWORD_INPUT, 'placeholder')
