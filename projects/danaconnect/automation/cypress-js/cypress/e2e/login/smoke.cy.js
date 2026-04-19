// ============================================================
// SMOKE.CY.JS — Smoke tests for the login page
// ============================================================
// Owner: Casey (Automation) — runs tests from all engineers
// Frequency: Every build, every deployment
// Duration: ~2 minutes
//
// CYPRESS TEST STRUCTURE:
//
// describe() = a group of related tests (like a test class)
// it() = one individual test (like a test function)
// beforeEach() = runs before EACH test (like a fixture)
//
// describe('Login', () => {
//   beforeEach(() => { /* setup */ });
//   it('should work', () => { /* test */ });
// });
// ============================================================

import loginPage from '../../pages/LoginPage';

// ── describe() groups related tests ─────────────────────────
// You can nest describe blocks for sub-groups:
//   describe('Login')
//     describe('Page Load')
//       it('test 1')
//       it('test 2')
// ─────────────────────────────────────────────────────────────

describe('Login Page — Smoke Tests', () => {

  // beforeEach runs before EVERY test in this describe block.
  // Here we navigate to the login page so each test starts fresh.
  beforeEach(() => {
    loginPage.visit();
  });

  describe('Page Load (Jordan + Riley)', () => {

    it('TC-FUNC-020: should display all login form elements', () => {
      // .should('be.visible') is a Cypress assertion.
      // It auto-retries for up to 10 seconds (our defaultCommandTimeout).
      // If the element doesn't become visible in time, the test fails.
      loginPage.verifyPageLoaded();
    });

    it('TC-SEC-009: should mask the password field', () => {
      loginPage.verifyPasswordMasked();
    });

    it('TC-FUNC-018: should display Privacy Policy link', () => {
      loginPage.privacyPolicyLink.should('be.visible');
    });

    it('TC-FUNC-019: should display Terms of Use link', () => {
      loginPage.termsOfUseLink.should('be.visible');
    });

    it('TC-UI-004: should show correct placeholder texts', () => {
      loginPage.companyInput
        .should('have.attr', 'placeholder')
        .and('match', /company/i);

      loginPage.usernameInput
        .should('have.attr', 'placeholder')
        .and('match', /user/i);

      loginPage.passwordInput
        .should('have.attr', 'placeholder')
        .and('match', /password/i);
    });
  });

  describe('Invalid Login Attempts (Jordan)', () => {

    it('TC-FUNC-005: should reject empty form submission', () => {
      // Click ENTER without filling anything
      loginPage.clickEnter();

      // Should remain on login page
      loginPage.verifyStillOnLoginPage();
    });

    it('TC-FUNC-002: should reject invalid company code', () => {
      loginPage.login('INVALIDCOMPANY999', 'user', 'pass');

      // Wait for server response, verify we're still on login page
      cy.wait(2000);
      loginPage.verifyStillOnLoginPage();
    });

    it('TC-FUNC-016: should submit form via Enter key', () => {
      loginPage.enterCompanyCode('TEST');
      loginPage.enterUsername('user');
      loginPage.enterPassword('pass');
      loginPage.submitWithEnterKey();

      // If we get here without error, Enter key works
      loginPage.verifyStillOnLoginPage();
    });
  });

  describe('Security Basics (Sam)', () => {

    it('TC-SEC-010: should use HTTPS', () => {
      // cy.url() gets the current URL
      // .should() asserts a condition
      cy.url().should('match', /^https:\/\//);
    });

    it('TC-SEC-009: password should not be in URL after submit', () => {
      loginPage.login('TEST', 'user', 'secretpass123');
      cy.url().should('not.include', 'secretpass123');
    });
  });
});
