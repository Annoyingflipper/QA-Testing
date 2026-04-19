// ============================================================
// CYPRESS.CONFIG.JS — Cypress configuration
// ============================================================
// This is Cypress's main config file. It tells Cypress:
// - Where to find tests
// - What URL to test against
// - Timeouts, viewport size, and other settings
//
// KEY CONCEPT: Cypress runs INSIDE the browser, not outside it
// like Selenium/Playwright. This means:
// - It's faster (no network lag between test runner and browser)
// - It can intercept network requests (great for testing APIs)
// - But it can only test one browser tab at a time
// ============================================================

const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    // The base URL for all cy.visit() calls
    // cy.visit('/login') becomes cy.visit('https://portal.danaconnect.com/login')
    baseUrl: 'https://portal.danaconnect.com',

    // Where Cypress looks for test files
    specPattern: 'cypress/e2e/**/*.cy.{js,ts}',

    // Where Cypress saves screenshots on failure
    screenshotsFolder: 'reports/screenshots',

    // Where Cypress saves test videos
    videosFolder: 'reports/videos',

    // Record a video of every test run (useful for debugging failures)
    video: true,

    // Browser viewport size (matches our test plan's desktop target)
    viewportWidth: 1920,
    viewportHeight: 1080,

    // How long Cypress waits for elements before failing (milliseconds)
    defaultCommandTimeout: 10000,

    // How long Cypress waits for a page to load
    pageLoadTimeout: 30000,

    // Retry failed tests (helps with flaky tests in CI)
    retries: {
      runMode: 2,    // Retry twice when running in CI (cypress run)
      openMode: 0,   // No retries in interactive mode (cypress open)
    },

    // Reporter for generating HTML test reports
    reporter: 'mochawesome',
    reporterOptions: {
      reportDir: 'reports/mochawesome',
      overwrite: false,
      html: true,
      json: true,
    },
  },
});
