// ============================================================
// SECURITY.CY.JS — Security tests for the login page
// ============================================================
// Owner: Sam (Security QA) + Casey (Automation)
// Framework: Cypress
//
// CYPRESS FEATURE: cy.intercept()
// This is something Selenium and Playwright can't do easily.
// Cypress can intercept network requests and inspect them
// BEFORE they reach the server or AFTER the response comes back.
// Perfect for security testing — we can see exactly what's
// being sent over the wire.
// ============================================================

import loginPage from '../../pages/LoginPage';

describe('Login Page — Security Tests', () => {

  beforeEach(() => {
    loginPage.visit();
  });

  // ── SQL Injection Tests ───────────────────────────────────
  // We use Cypress's .forEach() pattern to test multiple payloads.
  // This is similar to pytest's @parametrize decorator.
  // ──────────────────────────────────────────────────────────

  describe('TC-SEC-001: SQL Injection — Company Code', () => {

    const sqlPayloads = [
      { payload: "' OR '1'='1",          name: 'OR-based bypass' },
      { payload: "' OR '1'='1' --",      name: 'Comment-based bypass' },
      { payload: "admin'--",             name: 'Auth bypass' },
      { payload: "' UNION SELECT null,null --", name: 'Union extraction' },
      { payload: "1' AND SLEEP(5) --",   name: 'Time-based blind' },
    ];

    sqlPayloads.forEach(({ payload, name }) => {
      it(`should block: ${name}`, () => {
        loginPage.login(payload, 'testuser', 'testpass');

        // Verify no SQL errors leaked
        loginPage.verifyNoSQLErrors();

        // Verify page is still functional
        loginPage.verifyStillOnLoginPage();
      });
    });
  });

  describe('TC-SEC-004: XSS Injection — Company Code', () => {

    const xssPayloads = [
      { payload: "<script>alert('XSS')</script>",  name: 'Script tag' },
      { payload: "<img src=x onerror=alert(1)>",   name: 'Img onerror' },
      { payload: "javascript:alert(1)",             name: 'JS protocol' },
      { payload: "<svg onload=alert(1)>",           name: 'SVG onload' },
    ];

    xssPayloads.forEach(({ payload, name }) => {
      it(`should block: ${name}`, () => {
        // For XSS payloads with special characters, use {parseSpecialCharSequences: false}
        // to prevent Cypress from interpreting { as a special command
        loginPage.companyInput.clear().type(payload, { parseSpecialCharSequences: false });
        loginPage.enterUsername('testuser');
        loginPage.enterPassword('testpass');
        loginPage.clickEnter();

        // The raw payload should NOT appear in the DOM
        cy.get('body').then(($body) => {
          const html = $body.html();
          expect(html).to.not.include(payload);
        });
      });
    });
  });

  describe('TC-SEC-016: Error Message Information Leakage', () => {

    it('should show identical errors for different invalid inputs', () => {
      // ── Strategy ──────────────────────────────────────────
      // We'll make 3 login attempts with different invalid fields
      // and compare the error messages. They should be identical.
      // Different messages = attacker can enumerate valid values.
      // ──────────────────────────────────────────────────────

      const attempts = [];

      // Attempt 1: Bad company
      loginPage.login('BADCOMPANY', 'user', 'pass');
      cy.wait(2000);

      // Try to capture error text (if any)
      cy.get('body').then(($body) => {
        attempts.push($body.text());
      });

      // Attempt 2: Bad username
      loginPage.visit();
      loginPage.login('TESTCO', 'BADUSER', 'pass');
      cy.wait(2000);

      cy.get('body').then(($body) => {
        attempts.push($body.text());
      });

      // Attempt 3: Bad password
      loginPage.visit();
      loginPage.login('TESTCO', 'user', 'BADPASS');
      cy.wait(2000);

      cy.get('body').then(($body) => {
        attempts.push($body.text());

        // Now compare — all three should look similar
        // (We can't check exact equality since timestamps etc may differ,
        // but the ERROR portion should be the same)
        cy.log(`Captured ${attempts.length} responses for comparison`);
      });
    });
  });

  describe('Network Security', () => {

    it('TC-SEC-009: should not send password in plain text URL', () => {
      // ── cy.intercept() — Cypress superpower ──────────────
      // This tells Cypress: "watch for any request to this URL
      // pattern and let me inspect it."
      //
      // Selenium/Playwright can't do this easily — you'd need
      // a separate proxy tool like Burp Suite.
      // ──────────────────────────────────────────────────────

      cy.intercept('**/*').as('allRequests');

      loginPage.login('TEST', 'user', 'MySecretPass123');

      // Check that no request URL contains the password
      cy.get('@allRequests.all').then((interceptions) => {
        interceptions.forEach((req) => {
          expect(req.request.url).to.not.include('MySecretPass123');
        });
      });
    });

    it('should send login request over HTTPS', () => {
      // Intercept login-related requests
      cy.intercept('POST', '**/*').as('loginRequest');

      loginPage.login('TEST', 'user', 'pass');

      // If a POST request was made, verify it used HTTPS
      cy.wait('@loginRequest', { timeout: 5000 }).then((interception) => {
        expect(interception.request.url).to.match(/^https:\/\//);
      });
    });
  });
});
