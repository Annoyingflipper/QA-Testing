// ============================================================
// LOGINPAGE.JS — Page Object for Cypress
// ============================================================
// Same Page Object Model concept as Python versions,
// adapted for Cypress's chainable command style.
//
// IMPORTANT DIFFERENCE:
// Cypress commands are ASYNCHRONOUS but you don't use
// async/await or .then(). Cypress queues them up and runs
// them in order automatically. This is unique to Cypress.
//
// So this:
//   cy.get('input').type('hello')
//   cy.get('button').click()
//
// Types "hello" THEN clicks the button, even though there's
// no await or callback. Cypress handles the timing internally.
// ============================================================

class LoginPage {
  // ── Element selectors ─────────────────────────────────────
  // We store selectors as methods that return Cypress chains.
  // This keeps them in one place (DRY principle).
  // ──────────────────────────────────────────────────────────

  get companyInput() {
    return cy.get("input[placeholder*='company' i]");
  }

  get usernameInput() {
    return cy.get("input[placeholder*='user' i]");
  }

  get passwordInput() {
    return cy.get("input[type='password']");
  }

  get enterButton() {
    return cy.contains('button', 'ENTER');
  }

  get privacyPolicyLink() {
    return cy.contains('Privacy Policy');
  }

  get termsOfUseLink() {
    return cy.contains('Terms of Use');
  }

  // ── Actions ───────────────────────────────────────────────

  visit() {
    cy.visit('/');
    return this;
  }

  enterCompanyCode(code) {
    this.companyInput.clear().type(code);
    return this;
  }

  enterUsername(username) {
    this.usernameInput.clear().type(username);
    return this;
  }

  enterPassword(password) {
    // {log: false} prevents the password from appearing in
    // Cypress's command log (security best practice)
    this.passwordInput.clear().type(password, { log: false });
    return this;
  }

  clickEnter() {
    this.enterButton.click();
    return this;
  }

  login(companyCode, username, password) {
    this.enterCompanyCode(companyCode);
    this.enterUsername(username);
    this.enterPassword(password);
    this.clickEnter();
    return this;
  }

  submitWithEnterKey() {
    this.passwordInput.type('{enter}');
    return this;
  }

  // ── Assertions ────────────────────────────────────────────
  // In Cypress, assertions use .should() which auto-retries
  // until the condition is met (or timeout). This makes tests
  // much more resilient than manual assert statements.
  // ──────────────────────────────────────────────────────────

  verifyPageLoaded() {
    this.companyInput.should('be.visible');
    this.usernameInput.should('be.visible');
    this.passwordInput.should('be.visible');
    this.enterButton.should('be.visible');
    return this;
  }

  verifyPasswordMasked() {
    this.passwordInput.should('have.attr', 'type', 'password');
    return this;
  }

  verifyStillOnLoginPage() {
    cy.url().should('include', 'portal.danaconnect.com');
    return this;
  }

  verifyErrorMessage() {
    // Look for any error-related element
    cy.get("[class*='error'], [class*='alert'], [role='alert']")
      .should('be.visible');
    return this;
  }

  verifyNoSQLErrors() {
    // The page body should not contain SQL error strings
    cy.get('body').then(($body) => {
      const text = $body.text().toLowerCase();
      expect(text).to.not.include('sql');
      expect(text).to.not.include('syntax error');
      expect(text).to.not.include('database');
      expect(text).to.not.include('exception');
    });
    return this;
  }
}

// Export as a singleton — every test gets the same instance
export default new LoginPage();
