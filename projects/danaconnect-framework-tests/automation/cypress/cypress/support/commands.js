/**
 * DANAConnect Framework Tests — Cypress Custom Commands
 * ======================================================
 * Custom commands extend Cypress with reusable actions.
 *
 * Instead of writing the same steps over and over in tests,
 * we define them once here as custom commands. Then in tests
 * we can simply write: cy.login('company', 'user', 'pass')
 *
 * How custom commands work:
 * - Cypress.Commands.add('name', callback) creates a new command
 * - The command becomes available as cy.name() in all tests
 * - Commands are chainable — they integrate with Cypress's command queue
 *
 * This is similar to pytest fixtures in Python, but for Cypress.
 */

// ── Login Command ─────────────────────────────────────────────────────
/**
 * Custom command to perform a complete login.
 *
 * Usage in tests:
 *   cy.login('venturestars', 'vmaniglia', 'password123')
 *   // or use environment variables:
 *   cy.login(Cypress.env('COMPANY'), Cypress.env('USERNAME'), Cypress.env('PASSWORD'))
 *
 * @param {string} company  - The company code to enter
 * @param {string} username - The username to enter
 * @param {string} password - The password to enter
 */
Cypress.Commands.add('login', (company, username, password) => {
  // Type the company code into the Company field
  // {force: true} bypasses visibility checks if the field is covered
  cy.get('input[placeholder="Enter your company code"]')
    .clear()           // Clear any existing text
    .type(company);    // Type the company code

  // Type the username into the Username field
  cy.get('input[placeholder="Enter your user name"]')
    .clear()
    .type(username);

  // Type the password into the Password field
  cy.get('input[placeholder="Enter your password DANA"]')
    .clear()
    .type(password);

  // Click the ENTER button to submit the login form
  cy.get('button').contains('ENTER').click();
});
