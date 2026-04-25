/**
 * DANAConnect Framework Tests — Cypress Custom Commands
 * ======================================================
 * Custom commands extend Cypress with reusable actions. Instead of
 * repeating the same steps in every test, we define them once here
 * and call `cy.commandName()` from any spec.
 *
 * How custom commands work:
 *   - `Cypress.Commands.add('name', callback)` creates a new command.
 *   - The command becomes available as `cy.name()` in every spec,
 *     everywhere — no import needed in the spec file itself.
 *   - Commands are chainable and integrate with Cypress's command queue.
 *
 * Pattern used here: commands DELEGATE to the Page Object.
 * --------------------------------------------------------
 * Custom commands in this file are thin wrappers — they import the
 * singleton page object and call its methods. That way there is
 * exactly ONE place that knows how to find elements on the login page
 * (`cypress/pages/LoginPage.js`). When Vaadin changes a class name,
 * we update the page object once and both the specs AND this custom
 * command stay in sync.
 *
 * Why this matters here specifically:
 *   The previous version of this file hardcoded selectors like
 *   `input[placeholder="Enter your company code"]`. Vaadin inputs have
 *   NO placeholder attribute (see TP-LOGIN-001), so those selectors
 *   could never match the real site. Routing everything through the
 *   page object prevents that class of bug from recurring.
 */

import loginPage from '../pages/LoginPage';

// ── cy.login() ────────────────────────────────────────────────────────
/**
 * Perform a complete login by filling all three fields and clicking ENTER.
 *
 * Usage:
 *   cy.login('venturestars', 'vmaniglia', 'password')
 *
 *   // ...or (preferred) read from the environment:
 *   cy.login(
 *     Cypress.env('COMPANY'),
 *     Cypress.env('USERNAME'),
 *     Cypress.env('PASSWORD'),
 *   );
 *
 * Note: this command does NOT navigate. The caller is responsible for
 * getting the browser to /LoginView first (usually via
 * `loginPage.visit()` in a `beforeEach`).
 *
 * @param {string} company  — the company code
 * @param {string} username — the username
 * @param {string} password — the password
 */
Cypress.Commands.add('login', (company, username, password) => {
  loginPage.login(company, username, password);
});
