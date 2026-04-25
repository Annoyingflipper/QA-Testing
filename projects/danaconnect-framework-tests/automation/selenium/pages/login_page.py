"""
DANAConnect — Login Page Object (Selenium)
===========================================
Page Object Model for the DANAConnect login page, implemented with
Selenium WebDriver. This class is the Selenium counterpart to Luna's
Playwright POM at ``automation/playwright/pages/login_page.py`` and
reuses the exact same locator strategy so the two frameworks describe
the page identically.

Why the locators look the way they do
-------------------------------------
DANAConnect is a **Vaadin 7-style, GWT-compiled single-page app**.
Luna's 2026-04-21 reconnaissance (documented in
``test-plans/feature-login.md``) confirmed the following facts about
the rendered DOM — facts that directly dictate every locator below:

1. Inputs have NO ``placeholder``, ``name``, or ``aria-label``
   attributes. Any selector that pins to a placeholder (e.g. the
   ``input[placeholder="Enter your company code"]`` we originally
   wrote) will NEVER match anything on this page.
2. Element IDs look like ``gwt-uid-9``, ``gwt-uid-11`` — those are
   auto-generated at GWT compile time and change between deploys.
   Pinning to them guarantees future flake, so we deliberately do
   not use IDs.
3. The "ENTER" button is a ``<div class="v-button" role="button">``,
   NOT a native ``<button>`` element. A ``By.TAG_NAME, 'button'``
   or ``By.CSS_SELECTOR, 'button'`` selector finds nothing.
4. Labels ("COMPANY", "USERNAME", "PASSWORD", "ENTER") are rendered
   in different languages depending on session locale ("Usuario" /
   "Contraseña" / "ENTRAR" in a Spanish session). So we avoid
   pinning to label text unless we alternate-match both languages.
5. The post-login URL uses **hash-based routing** — the path stays
   ``/LoginView`` forever; only the hash fragment changes from empty
   to ``#!MainView``. Tests should look for ``#!MainView``, not a
   path change.

Translating Luna's Playwright locators to Selenium
--------------------------------------------------
Playwright ships CSS extensions that Selenium does not support
natively (``:nth-match()``, ``:has-text()``). Selenium's equivalent
is XPath. The table below shows every translation:

=========================  ============================================  =========================
Element                    Playwright (Luna)                              Selenium (this file)
=========================  ============================================  =========================
Company input              ``:nth-match(input[type="text"], 1)``          ``(//input[@type='text'])[1]`` via XPath
Username input             ``:nth-match(input[type="text"], 2)``          ``(//input[@type='text'])[2]`` via XPath
Password input             ``input[type="password"]``                     identical via CSS
ENTER button               ``.v-button[role="button"]``                   identical via CSS
Privacy link               ``.v-caption-label-signIn-company:has-text("Privacy"/"Política")``  XPath with class+text alternation
Terms link                 same pattern                                   XPath with class+text alternation
Copyright footer           ``.v-label-Corp``                              identical via CSS
=========================  ============================================  =========================

Why an implicit wait still works underneath
-------------------------------------------
The ``conftest.py`` fixture currently sets ``driver.implicitly_wait(10)``.
That is technical debt we will pay down later — the /qa-selenium skill
recommends ``implicitly_wait(0)`` with explicit waits only. For now the
POM still uses ``WebDriverWait`` on every interaction (the right way),
so the implicit wait acts only as a safety net and does not change
correctness.
"""

from selenium.webdriver.common.by import By                       # Locator strategies
from selenium.webdriver.common.keys import Keys                   # Keyboard keys (TAB, ENTER, ...)
from selenium.webdriver.support.ui import WebDriverWait           # Explicit-wait utility
from selenium.webdriver.support import expected_conditions as EC  # Readable wait conditions
from selenium.common.exceptions import (                           # Specific exceptions to catch
    ElementClickInterceptedException,
    ElementNotInteractableException,
)


class LoginPage:
    """
    Page Object for the DANAConnect ``/LoginView`` page.

    Each method represents a single user-facing action or query
    (enter the company, click ENTER, check if the footer is visible,
    …). Locators are declared as class-level tuples so they are
    trivial to find, reuse, and update when the UI changes.

    API parity with Luna's Playwright ``LoginPage`` is intentional:
    tests written against either POM should read nearly identically,
    which makes cross-framework comparison easier for learning.
    """

    # ── URL ────────────────────────────────────────────────────────────
    # The path portion of the login page URL. We always navigate
    # explicitly — the DANAConnect root does NOT auto-redirect to
    # ``/LoginView``, a fact Luna's reconnaissance confirmed.
    URL_PATH = "/LoginView"

    # ── LOCATORS ───────────────────────────────────────────────────────
    # Selenium locators are (By.STRATEGY, "value") tuples. We keep them
    # at class scope (not inside __init__) so they are easy to import
    # and reuse from tests (e.g., ``LoginPage.ENTER_BUTTON``).

    # Company input — the FIRST ``<input type="text">`` on the page in
    # a fresh context's 3-field form. XPath positional indexing is
    # 1-based. ``(//input[@type='text'])[1]`` groups the result set
    # first, then picks element #1; the inner ``//input[@type='text'][1]``
    # form would incorrectly pick "first text input per parent".
    COMPANY_INPUT = (By.XPATH, "(//input[@type='text'])[1]")

    # Username input — the SECOND ``<input type="text">``.
    USERNAME_INPUT = (By.XPATH, "(//input[@type='text'])[2]")

    # Password input — there is only one password input on the page,
    # so a type-based CSS selector is the cleanest identifier.
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")

    # ENTER button — a Vaadin ``<div class="v-button" role="button">``.
    # We pin to class + role; we deliberately do NOT pin to the text
    # "ENTER" because a Spanish session renders the same element as
    # "ENTRAR".
    ENTER_BUTTON = (By.CSS_SELECTOR, ".v-button[role='button']")

    # Privacy Policy link — rendered as a ``<span>`` (or similar) with
    # the stable Vaadin class ``v-caption-label-signIn-company`` and
    # text "Privacy Policy" (English) or "Política de Privacidad"
    # (Spanish). XPath lets us express "class contains X AND text
    # matches one of these variants" in a single locator.
    PRIVACY_POLICY_LINK = (
        By.XPATH,
        "//*[contains(@class, 'v-caption-label-signIn-company')"
        " and (contains(., 'Privacy') or contains(., 'Política'))]",
    )

    # Terms of Use link — same pattern as Privacy. Text variants are
    # "Terms of Use" (English) and "Términos" (Spanish).
    TERMS_OF_USE_LINK = (
        By.XPATH,
        "//*[contains(@class, 'v-caption-label-signIn-company')"
        " and (contains(., 'Terms') or contains(., 'Términos'))]",
    )

    # Copyright footer — ``<div class="v-label v-label-Corp">`` with
    # text "DANAConnect Corp. All Rights Reserved". The Vaadin class
    # ``v-label-Corp`` is stable and unique, so this beats any text
    # match — and avoids colliding with the "Welcome to DANAConnect"
    # caption that also contains the brand name.
    FOOTER_TEXT = (By.CSS_SELECTOR, ".v-label-Corp")

    # ── Wait timeout (seconds) ─────────────────────────────────────────
    # How long any single WebDriverWait will poll before giving up.
    # 10s matches Luna's Playwright default and is comfortably above
    # DANAConnect's typical render time (~1–2s).
    WAIT_TIMEOUT = 10

    def __init__(self, driver):
        """
        Bind this page object to a Selenium WebDriver instance.

        Args:
            driver: The Selenium WebDriver provided by the pytest
                ``driver`` fixture in ``conftest.py``.

        We construct a single ``WebDriverWait`` for the instance and
        reuse it across methods — creating a new ``WebDriverWait`` per
        call is harmless but wasteful, and centralising it here makes
        the timeout easy to adjust.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, self.WAIT_TIMEOUT)

    def navigate(self, base_url):
        """
        Navigate directly to ``<base_url>/LoginView``.

        Args:
            base_url (str): e.g. ``"https://portal.danaconnect.com/"``.

        We strip any trailing slash so we never produce the double-slash
        URL ``"https://portal.danaconnect.com//LoginView"``. Selenium's
        ``driver.get()`` blocks until ``document.readyState == 'complete'``,
        so once this call returns the initial HTML is loaded — but note
        that Vaadin then renders the form via JS, so callers should wait
        for ``COMPANY_INPUT`` before interacting.
        """
        self.driver.get(base_url.rstrip("/") + self.URL_PATH)

    def wait_for_form_rendered(self):
        """
        Block until the login form is actually drawn on the page.

        This replaces Playwright's ``page.wait_for_load_state("networkidle")``
        — Selenium has no true "network idle" signal, so the idiomatic
        alternative is "wait for the first element we're about to
        interact with". Waiting on ``COMPANY_INPUT`` is sufficient
        because it is the slowest of the three inputs to render (it
        appears first, but Vaadin draws the whole FormLayout in one
        paint pass).

        Using ``presence_of_element_located`` (not visibility) here
        is intentional: we only need to know the DOM exists before
        we start interacting; the individual ``enter_*`` methods each
        do their own visibility-aware wait via ``WebDriverWait``.
        """
        self.wait.until(EC.presence_of_element_located(self.COMPANY_INPUT))

    # ── Private helper ─────────────────────────────────────────────────
    # The underscore prefix is a Python convention meaning "internal —
    # not part of the public API". Tests should not call this directly.

    def _wait_and_find(self, locator):
        """
        Wait for ``locator`` to be present in the DOM and return the
        resulting ``WebElement``.

        Why this helper exists: every ``enter_*`` method needs the
        same three-line "wait, then find" pattern. Extracting it keeps
        each action method short and single-purpose.

        Raises:
            TimeoutException: if the element is still not in the DOM
                after ``WAIT_TIMEOUT`` seconds. We let this bubble up
                so pytest shows a clean, specific failure.
        """
        return self.wait.until(EC.presence_of_element_located(locator))

    # ── Interaction methods ────────────────────────────────────────────

    def enter_company(self, company):
        """
        Type ``company`` into the Company input field.

        Selenium's ``send_keys`` APPENDS by default, so we call
        ``clear()`` first to guarantee the field starts empty. Without
        that call, running this method twice in the same test would
        double up the input.
        """
        element = self._wait_and_find(self.COMPANY_INPUT)
        element.clear()
        element.send_keys(company)

    def enter_username(self, username):
        """Type ``username`` into the Username input field."""
        element = self._wait_and_find(self.USERNAME_INPUT)
        element.clear()
        element.send_keys(username)

    def enter_password(self, password):
        """
        Type ``password`` into the Password input field and blur it.

        We append ``Keys.TAB`` after the password. Why? Vaadin 7
        buffers input changes and only fires the ``change`` event on
        blur — not on each keystroke. If we skip the blur, the
        subsequent click on ENTER can submit before Vaadin has
        committed the password value, producing a silent "empty
        password" failure on the server. TAB moves focus off the
        field, triggering blur, which triggers Vaadin's change
        event, which commits the value.
        """
        element = self._wait_and_find(self.PASSWORD_INPUT)
        element.clear()
        element.send_keys(password)
        element.send_keys(Keys.TAB)

    def click_enter(self):
        """
        Click the ENTER button to submit the login form.

        Why ``element_to_be_clickable``?
            Being "in the DOM" is not enough — Vaadin may add an
            ``aria-disabled`` while the form is validating, and
            clicking in that window does nothing.
            ``element_to_be_clickable`` waits until the element is
            visible AND enabled, which matches the precondition a
            human user would observe before clicking.

        Why the JavaScript-click fallback?
            The ENTER control is a ``<div class="v-button" role="button">``
            — not a native HTML button. Selenium's native ``.click()``
            dispatches a real mouse-click, but in a few edge cases
            (sticky footer overlay, an animation mid-transition,
            ``pointer-events`` briefly set to ``none``) the click is
            intercepted or produces no effect on the GWT event
            handler. Falling back to a JS click via
            ``arguments[0].click()`` bypasses the interceptability
            check and calls the element's ``onclick`` directly,
            which is enough to trigger Vaadin's login handler.
            We do NOT use JS click by default — native click gives
            a better guarantee that the element is truly interactive.
        """
        button = self.wait.until(EC.element_to_be_clickable(self.ENTER_BUTTON))
        try:
            button.click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            # Something is covering or temporarily disabling the
            # button. Fall back to a JS click, which ignores
            # interceptability and pointer-events.
            self.driver.execute_script("arguments[0].click();", button)

    def login(self, company, username, password):
        """
        Convenience method — fill all three fields and click ENTER.

        Tests that only care about "the user logged in" should call
        this instead of the four individual methods.
        """
        self.enter_company(company)
        self.enter_username(username)
        self.enter_password(password)
        self.click_enter()

    # ── Visibility checks ──────────────────────────────────────────────
    # These return True/False and are intended for boolean assertions
    # in tests (e.g. ``assert login_page.is_footer_visible()``).
    #
    # We use ``EC.visibility_of_element_located`` (not just
    # ``presence_of_element_located``) because a field that is in the
    # DOM but hidden via CSS is functionally invisible to a real user.
    # Tests should agree with the user's perspective.

    def is_company_field_visible(self):
        """Return True iff the Company input is rendered and visible."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.COMPANY_INPUT)
            ).is_displayed()
        except Exception:
            # If WebDriverWait times out, the element is not visible
            # within our budget — treat that as "not visible" rather
            # than letting the TimeoutException bubble up.
            return False

    def is_username_field_visible(self):
        """Return True iff the Username input is rendered and visible."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.USERNAME_INPUT)
            ).is_displayed()
        except Exception:
            return False

    def is_password_field_visible(self):
        """Return True iff the Password input is rendered and visible."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.PASSWORD_INPUT)
            ).is_displayed()
        except Exception:
            return False

    def is_enter_button_visible(self):
        """Return True iff the ENTER button is rendered and visible."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.ENTER_BUTTON)
            ).is_displayed()
        except Exception:
            return False

    def is_privacy_policy_visible(self):
        """Return True iff the Privacy Policy link is rendered and visible."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.PRIVACY_POLICY_LINK)
            ).is_displayed()
        except Exception:
            return False

    def is_terms_of_use_visible(self):
        """Return True iff the Terms of Use link is rendered and visible."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.TERMS_OF_USE_LINK)
            ).is_displayed()
        except Exception:
            return False

    def is_footer_visible(self):
        """Return True iff the copyright footer is rendered and visible."""
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.FOOTER_TEXT)
            ).is_displayed()
        except Exception:
            return False

    # ── Attribute getters ──────────────────────────────────────────────
    # Kept for API parity with Luna's Playwright POM. On DANAConnect
    # these will return ``None`` because Vaadin inputs have no
    # ``placeholder`` attribute — the methods exist so a test that
    # wants to ASSERT that absence can do so cleanly.

    def get_company_placeholder(self):
        """Return the ``placeholder`` attribute of the Company input (usually None on Vaadin)."""
        return self._wait_and_find(self.COMPANY_INPUT).get_attribute("placeholder")

    def get_username_placeholder(self):
        """Return the ``placeholder`` attribute of the Username input (usually None on Vaadin)."""
        return self._wait_and_find(self.USERNAME_INPUT).get_attribute("placeholder")

    def get_password_placeholder(self):
        """Return the ``placeholder`` attribute of the Password input (usually None on Vaadin)."""
        return self._wait_and_find(self.PASSWORD_INPUT).get_attribute("placeholder")
