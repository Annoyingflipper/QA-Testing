/**
 * DANAConnect — Login Page Object (Cypress)
 * ==========================================
 * Page Object Model (POM) for the /LoginView page.
 *
 * About the target app
 * --------------------
 * DANAConnect is a Vaadin 7-style, GWT-compiled single-page app.
 * That forces a very specific locator strategy (see TP-LOGIN-001):
 *
 *   1. Inputs have NO `placeholder`, `name`, or `aria-label` attributes.
 *      — So [data-testid], [data-cy], and [placeholder] selectors all
 *        fail. This is why the previous version of this file (which
 *        used `input[placeholder="Enter your company code"]`) could
 *        never work against the real site.
 *
 *   2. Element IDs look like `gwt-uid-9`, `gwt-uid-11` — auto-generated
 *      at compile time and DIFFERENT between deploys. Never pin locators
 *      to these IDs.
 *
 *   3. The "ENTER" button is a `<div class="v-button" role="button">`,
 *      NOT a native `<button>`. So `cy.get('button').contains('ENTER')`
 *      will never find it.
 *
 *   4. Field labels render in the session locale — fresh en-US sessions
 *      see "COMPANY / USERNAME / PASSWORD / ENTER"; cached Spanish
 *      sessions see "COMPANY / Usuario / Contraseña / ENTRAR". So
 *      locators must NOT pin to label text.
 *
 * Locator strategy (mirrors Luna's Playwright page object)
 * --------------------------------------------------------
 *   - Text inputs:     positional — 1st text input = Company,
 *                      2nd text input = Username.
 *   - Password input:  input[type="password"] (only one on the page).
 *   - ENTER button:    .v-button[role="button"] (only one on the page).
 *   - Privacy / Terms: .v-caption-label-signIn-company filtered by an
 *                      English-or-Spanish regex substring.
 *   - Copyright footer: .v-label-Corp (stable Vaadin class unique to
 *                      the "DANAConnect Corp. All Rights Reserved"
 *                      element; won't collide with the "Welcome to
 *                      DANAConnect" greeting).
 *
 * About the POM pattern used here
 * -------------------------------
 * Getter-based Page Objects. Each getter returns a FRESH `cy.get()`
 * chain, so the element reference is re-queried on every access. This
 * avoids stale references and integrates cleanly with Cypress's
 * automatic retry-ability.
 *
 * Action methods (enterCompany, login, …) compose those getters and
 * return `this` for chaining.
 */

class LoginPage {

  // ── URL ──────────────────────────────────────────────────────────────
  // Relative path — Cypress prepends baseUrl from cypress.config.js.
  URL_PATH = '/LoginView';

  // ── SELECTORS ────────────────────────────────────────────────────────
  // Exposed as static class members so specs can import them directly
  // if they ever need to drive cy.get() themselves (e.g., to handle a
  // custom multi-match scenario).
  static TEXT_INPUT   = 'input[type="text"]';       // paired with .eq(0) / .eq(1)
  static PASSWORD_INP = 'input[type="password"]';
  static ENTER_BUTTON = '.v-button[role="button"]';
  static FOOTER_TEXT  = '.v-label-Corp';
  // Both the Privacy and Terms links are rendered as spans with this
  // Vaadin class. We filter the matched set by text to pick the right one.
  static CAPTION_LINK = '.v-caption-label-signIn-company';

  // ── ELEMENT GETTERS ──────────────────────────────────────────────────
  // Getters return live `cy.get()` / `cy.contains()` chains. Each access
  // re-queries the DOM, which is exactly what Cypress's retry logic
  // wants — elements never go "stale" the way they can in Selenium.

  /**
   * First text input on the page = the Company code field.
   *
   * `.eq(0)` is Cypress's 0-indexed equivalent of Playwright's
   * `:nth-match(input[type="text"], 1)`.
   */
  get companyInput() {
    return cy.get(LoginPage.TEXT_INPUT).eq(0);
  }

  /**
   * Second text input on the page = the Username field.
   */
  get usernameInput() {
    return cy.get(LoginPage.TEXT_INPUT).eq(1);
  }

  /**
   * The only `input[type="password"]` on the page.
   */
  get passwordInput() {
    return cy.get(LoginPage.PASSWORD_INP);
  }

  /**
   * The Vaadin ENTER "button" — actually a `<div class="v-button">`
   * with `role="button"`. There's only one such element on the login
   * page, so the selector is unambiguous.
   */
  get enterButton() {
    return cy.get(LoginPage.ENTER_BUTTON);
  }

  /**
   * Privacy Policy link.
   *
   * The label text varies by locale, so we scope by the stable Vaadin
   * class and filter with a regex that matches both English
   * ("Privacy Policy") and Spanish ("Política de Privacidad").
   *
   * `cy.contains(selector, content)` yields the first element matching
   * both the selector AND the content — ideal for disambiguating
   * siblings that share the same class.
   */
  get privacyPolicyLink() {
    return cy.contains(LoginPage.CAPTION_LINK, /Privacy|Pol[íi]tica/);
  }

  /**
   * Terms of Use link — same multi-locale strategy as Privacy.
   */
  get termsOfUseLink() {
    return cy.contains(LoginPage.CAPTION_LINK, /Terms|T[ée]rminos/);
  }

  /**
   * Copyright footer. `.v-label-Corp` is a stable Vaadin class unique
   * to the "DANAConnect Corp. All Rights Reserved" element.
   */
  get footer() {
    return cy.get(LoginPage.FOOTER_TEXT);
  }

  // ── NAVIGATION ───────────────────────────────────────────────────────

  /**
   * Navigate to the login view.
   *
   * Why `cy.visit('/LoginView')` and not `cy.visit('/')`?
   * The DANAConnect root URL does NOT auto-redirect to /LoginView —
   * Luna discovered this empirically during the first Playwright run.
   * Going directly is both faster and more deterministic.
   */
  visit() {
    cy.visit(this.URL_PATH);
    return this;
  }

  // ── ACTIONS ──────────────────────────────────────────────────────────

  /**
   * Type the company code into the Company field.
   *
   * `.clear()` first removes any pre-filled value (e.g., if the browser
   * somehow kept a company from a prior run); `.type()` then enters the
   * new value. Cypress auto-waits for the input to be actionable before
   * either call.
   */
  enterCompany(company) {
    this.companyInput.clear().type(company);
    return this;
  }

  enterUsername(username) {
    this.usernameInput.clear().type(username);
    return this;
  }

  enterPassword(password) {
    this.passwordInput.clear().type(password);
    return this;
  }

  /**
   * Click the ENTER button. Cypress auto-waits for the element to be
   * visible and actionable before clicking — no explicit wait needed.
   */
  clickEnter() {
    this.enterButton.click();
    return this;
  }

  /**
   * Full login flow: fill all three fields and click ENTER.
   *
   * Tests that only care about "get me logged in" call this in one line:
   *   loginPage.login(company, username, password);
   */
  login(company, username, password) {
    this.enterCompany(company);
    this.enterUsername(username);
    this.enterPassword(password);
    this.clickEnter();
    return this;
  }
}

// Export a singleton instance. Tests use:
//   import loginPage from '../pages/LoginPage';
//   loginPage.visit();
//
// Matches the existing project style (default export, instance not class)
// so specs don't need `new LoginPage()` boilerplate everywhere.
export default new LoginPage();
