"""DANAConnect login page object (Selenium, Vaadin/GWT)."""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
)


class LoginPage:
    """Page Object for the /LoginView login form."""

    URL_PATH = "/LoginView"

    # Positional XPath — labels change language, DOM order doesn't.
    COMPANY_INPUT = (By.XPATH, "(//input[@type='text'])[1]")
    USERNAME_INPUT = (By.XPATH, "(//input[@type='text'])[2]")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    # ENTER is a Vaadin <div>, not a native <button>.
    ENTER_BUTTON = (By.CSS_SELECTOR, ".v-button[role='button']")
    PRIVACY_POLICY_LINK = (
        By.XPATH,
        "//*[contains(@class, 'v-caption-label-signIn-company')"
        " and (contains(., 'Privacy') or contains(., 'Política'))]",
    )
    TERMS_OF_USE_LINK = (
        By.XPATH,
        "//*[contains(@class, 'v-caption-label-signIn-company')"
        " and (contains(., 'Terms') or contains(., 'Términos'))]",
    )
    FOOTER_TEXT = (By.CSS_SELECTOR, ".v-label-Corp")

    WAIT_TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.WAIT_TIMEOUT)

    def navigate(self, base_url):
        self.driver.get(base_url.rstrip("/") + self.URL_PATH)

    def wait_for_form_rendered(self):
        # Selenium has no networkidle — wait for the first input instead.
        self.wait.until(EC.presence_of_element_located(self.COMPANY_INPUT))

    def _wait_and_find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def enter_company(self, company):
        element = self._wait_and_find(self.COMPANY_INPUT)
        element.clear()
        element.send_keys(company)

    def enter_username(self, username):
        element = self._wait_and_find(self.USERNAME_INPUT)
        element.clear()
        element.send_keys(username)

    def enter_password(self, password):
        # TAB triggers blur -> Vaadin fires 'change' and commits the value.
        element = self._wait_and_find(self.PASSWORD_INPUT)
        element.clear()
        element.send_keys(password)
        element.send_keys(Keys.TAB)

    def click_enter(self):
        # JS fallback — Vaadin ENTER is a <div role="button">, native click may not fire GWT handler.
        button = self.wait.until(EC.element_to_be_clickable(self.ENTER_BUTTON))
        try:
            button.click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            self.driver.execute_script("arguments[0].click();", button)

    def login(self, company, username, password):
        self.enter_company(company)
        self.enter_username(username)
        self.enter_password(password)
        self.click_enter()

    def _is_visible(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except Exception:
            return False

    def is_company_field_visible(self):
        return self._is_visible(self.COMPANY_INPUT)

    def is_username_field_visible(self):
        return self._is_visible(self.USERNAME_INPUT)

    def is_password_field_visible(self):
        return self._is_visible(self.PASSWORD_INPUT)

    def is_enter_button_visible(self):
        return self._is_visible(self.ENTER_BUTTON)

    def is_privacy_policy_visible(self):
        return self._is_visible(self.PRIVACY_POLICY_LINK)

    def is_terms_of_use_visible(self):
        return self._is_visible(self.TERMS_OF_USE_LINK)

    def is_footer_visible(self):
        return self._is_visible(self.FOOTER_TEXT)

    # Vaadin inputs have no placeholder — these return None on DANAConnect.
    def get_company_placeholder(self):
        return self._wait_and_find(self.COMPANY_INPUT).get_attribute("placeholder")

    def get_username_placeholder(self):
        return self._wait_and_find(self.USERNAME_INPUT).get_attribute("placeholder")

    def get_password_placeholder(self):
        return self._wait_and_find(self.PASSWORD_INPUT).get_attribute("placeholder")
