// ============================================================
// E2E.JS — Cypress support file (runs before every test)
// ============================================================
// This is like conftest.py in pytest — shared setup code.
// Everything here runs automatically before each test file.
//
// We use it to:
// - Define custom commands (reusable actions)
// - Set up global event handlers
// - Configure test behavior
// ============================================================

// ── Custom Commands ─────────────────────────────────────────
// Cypress lets you create your own commands that work just
// like built-in ones (cy.visit, cy.get, cy.click, etc.)
//
// After defining cy.login() below, any test can call:
//   cy.login('company', 'user', 'pass')
//
// This is Cypress's version of the Page Object pattern.
// ─────────────────────────────────────────────────────────────

Cypress.Commands.add('login', (companyCode, username, password) => {
  // cy.get() finds an element using a CSS selector
  // .clear() removes existing text
  // .type() types new text into the element

  cy.get("input[placeholder*='company' i]").clear().type(companyCode);
  cy.get("input[placeholder*='user' i]").clear().type(username);
  cy.get("input[type='password']").clear().type(password);

  // Find the ENTER button and click it
  cy.contains('button', 'ENTER').click();
});

// ── Handle uncaught exceptions ──────────────────────────────
// By default, Cypress fails the test if the APPLICATION throws
// a JavaScript error. We configure it to log these errors
// instead of failing, since we're testing someone else's app
// and can't control their error handling.
// ─────────────────────────────────────────────────────────────

Cypress.on('uncaught:exception', (err, runnable) => {
  // Log the error for debugging but don't fail the test
  cy.log(`Application error: ${err.message}`);
  return false; // false = don't fail the test
});
