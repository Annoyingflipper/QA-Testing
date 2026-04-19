/**
 * DANAConnect — Login Page Object (Cypress)
 * ==========================================
 * Page Object Model for the login page using Cypress.
 *
 * Key differences from Python (Playwright/Selenium) versions:
 * - Cypress uses cy.get() to find elements (returns Chainable objects)
 * - Cypress auto-waits for elements — no need for explicit waits
 * - Cypress runs INSIDE the browser, so it's faster than Selenium
 * - We use a class with methods, but Cypress commands are asynchronous
 * - Methods return 'this' to allow method chaining
 *
 * Page: Login (/LoginView)
 */

class LoginPage {

  // ── LOCATORS ───────────────────────────────────────────────────────
  // In Cypress, we define locators as methods that return cy.get() chains.
  // This is different from Python where we store selector strings.
  // Using methods ensures Cypress's retry mechanism works correctly.

  /**
   * Returns the Company input field element.
   * cy.get() finds elements using CSS selectors, just like
   * document.querySelector() in plain JavaScript.
   */
  getCompanyInput() {
    return cy.get('input[placeholder="Enter your company code"]');
  }

  /**
   * Returns the Username input field element.
   */
  getUsernameInput() {
    return cy.get('input[placeholder="Enter your user name"]');
  }

  /**
   * Returns the Password input field element.
   */
  getPasswordInput() {
    return cy.get('input[placeholder="Enter your password DANA"]');
  }

  /**
   * Returns the ENTER button element.
   * cy.contains() finds an element that contains the specified text.
   */
  getEnterButton() {
    return cy.get('button').contains('ENTER');
  }

  /**
   * Returns the Privacy Policy link element.
   */
  getPrivacyPolicyLink() {
    return cy.contains('Privacy Policy');
  }

  /**
   * Returns the Terms of Use link element.
   */
  getTermsOfUseLink() {
    return cy.contains('Terms of Use of the Service');
  }

  /**
   * Returns the footer text element.
   */
  getFooterText() {
    return cy.contains('DANAConnect Corp. All Rights Reserved');
  }

  // ── ACTIONS ────────────────────────────────────────────────────────

  /**
   * Navigate to the login page.
   * cy.visit() loads the URL. If you pass just a path like '/LoginView',
   * Cypress prepends the baseUrl from cypress.config.js.
   */
  navigate() {
    cy.visit('/LoginView');
    return this; // Return 'this' to allow method chaining
  }

  /**
   * Type the company code into the Company field.
   * .clear() removes existing text, .type() enters new text.
   * Cypress's .type() automatically waits for the element to be ready.
   *
   * @param {string} company - The company code to enter
   */
  enterCompany(company) {
    this.getCompanyInput().clear().type(company);
    return this;
  }

  /**
   * Type the username into the Username field.
   * @param {string} username - The username to enter
   */
  enterUsername(username) {
    this.getUsernameInput().clear().type(username);
    return this;
  }

  /**
   * Type the password into the Password field.
   * @param {string} password - The password to enter
   */
  enterPassword(password) {
    this.getPasswordInput().clear().type(password);
    return this;
  }

  /**
   * Click the ENTER button to submit the login form.
   */
  clickEnter() {
    this.getEnterButton().click();
    return this;
  }

  /**
   * Perform a complete login by filling all fields and clicking ENTER.
   * This is a convenience method that chains all individual steps.
   *
   * Usage: loginPage.login('venturestars', 'vmaniglia', 'password')
   *
   * @param {string} company  - The company code
   * @param {string} username - The username
   * @param {string} password - The password
   */
  login(company, username, password) {
    this.enterCompany(company);
    this.enterUsername(username);
    this.enterPassword(password);
    this.clickEnter();
    return this;
  }
}

// ── Export the page object ────────────────────────────────────────────
// We export a NEW INSTANCE (not the class) so tests can use it directly:
//   import loginPage from '../pages/LoginPage';
//   loginPage.enterCompany('venturestars');
export default new LoginPage();
