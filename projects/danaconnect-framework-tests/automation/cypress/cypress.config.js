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

// ── Import the Allure plugin's node-side hook ─────────────────────────
// allure-cypress has TWO halves: a Node-side hook (this one) that
// listens to Cypress lifecycle events and writes JSON result files,
// and a browser-side import (in support/e2e.js) that captures test
// data while a test is running. Both must be wired up for the report
// to be complete.
const { allureCypress } = require('allure-cypress/reporter');

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
      // ── Allure plugin: writes per-test JSON result files ─────────
      // resultsDir is RELATIVE to this file's directory
      // (automation/cypress/). The path ../../reports/... resolves
      // to <project>/reports/allure-results/cypress — same place the
      // Playwright and Selenium pytest invocations write their
      // results, so all three frameworks share one Allure dataset
      // and the Jenkins post block can merge them into one report.
      allureCypress(on, config, {
        resultsDir: '../../reports/allure-results/cypress',
      });

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
