/**
 * DANAConnect Framework Tests — Cypress Support File
 * ====================================================
 * This file runs BEFORE every single test file in Cypress.
 * It's the place to:
 * - Import custom commands (reusable test actions)
 * - Set up global configuration
 * - Add event listeners
 *
 * Think of this like conftest.py in pytest — it's the shared
 * setup that all tests inherit automatically.
 */

// ── Import custom commands ────────────────────────────────────────────
// Custom commands are defined in commands.js and become available
// as cy.commandName() in all test files.
import './commands';

// ── Global error handling ─────────────────────────────────────────────
// Prevent Cypress from failing on uncaught exceptions from the
// application itself. Some apps throw errors in the console that
// aren't related to our tests.
Cypress.on('uncaught:exception', (err, runnable) => {
  // Log the error for debugging but don't fail the test
  console.log('Uncaught exception:', err.message);
  // Return false to prevent Cypress from failing the test
  return false;
});
