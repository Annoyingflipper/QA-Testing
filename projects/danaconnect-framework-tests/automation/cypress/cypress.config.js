/**
 * DANAConnect Framework Tests — Cypress Configuration
 * =====================================================
 * This file configures how Cypress behaves when running tests.
 *
 * Key concepts:
 * - defineConfig(): Cypress's function to create a typed config object
 * - e2e: Configuration specific to End-to-End tests
 * - baseUrl: The starting URL for all tests (cy.visit('/') goes here)
 * - env: Environment variables accessible in tests via Cypress.env()
 *
 * Cypress reads this file before every test run.
 */

// ── Load environment variables from .env ──────────────────────────────
// require('dotenv') loads the .env file from the project root (2 levels up)
// config() reads the file and adds variables to process.env
require('dotenv').config({ path: '../../.env' });

// ── Import Cypress's config helper ────────────────────────────────────
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  projectId: 'jo88tn',

  // ── E2E Test Configuration ──────────────────────────────────────────
  e2e: {

    // The base URL of the application under test.
    // When you write cy.visit('/LoginView'), Cypress prepends this URL.
    baseUrl: process.env.BASE_URL || 'https://portal.danaconnect.com/',

    // Where Cypress looks for test files (spec files)
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx}',

    // Where Cypress looks for support files (custom commands, etc.)
    supportFile: 'cypress/support/e2e.js',

    // Disable Cypress's default video recording (saves disk space)
    video: false,

    // Take a screenshot automatically when a test fails
    screenshotOnRunFailure: true,

    // How long (ms) to wait for commands before timing out
    defaultCommandTimeout: 10000,   // 10 seconds for element commands
    pageLoadTimeout: 30000,         // 30 seconds for page loads

    // Viewport size (browser window dimensions)
    viewportWidth: 1280,
    viewportHeight: 720,

    // ── Setup Node Events ───────────────────────────────────────────
    // This function runs in Node.js (not in the browser).
    // Used to configure plugins like Allure reporting.
    setupNodeEvents(on, config) {
      // Allure reporter plugin (generates rich test reports)
      // Uncomment when allure plugin is installed:
      // const allureWriter = require('@shelex/cypress-allure-plugin/writer');
      // allureWriter(on, config);

      return config;
    },
  },

  // ── Environment Variables ───────────────────────────────────────────
  // These are accessible in tests via Cypress.env('COMPANY'), etc.
  // They come from the .env file loaded at the top of this file.
  env: {
    COMPANY: process.env.COMPANY || '',
    USERNAME: process.env.USERNAME || '',
    PASSWORD: process.env.PASSWORD || '',
  },
});
