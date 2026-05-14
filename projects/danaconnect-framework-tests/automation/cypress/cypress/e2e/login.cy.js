/**
 * DANAConnect — Login Tests (Cypress)
 * =====================================
 * End-to-end tests for the DANAConnect login page.
 *
 * Mirrors Luna's Playwright test file
 * (automation/playwright/tests/test_login.py) one-to-one — same two
 * scenarios, same assertion strategy, different framework.
 *
 * How Cypress discovers this file:
 *   - cypress.config.js `specPattern` = 'cypress/e2e/**\/*.cy.{js,jsx}'
 *   - Each `it()` inside a `describe()` block is one test.
 *   - `beforeEach()` runs before every test (fresh navigation each time).
 *
 * Why Page Object Model:
 *   - The test describes WHAT the user does, not HOW to find each
 *     element. If the UI changes (Vaadin class, DOM order, etc.) we
 *     update pages/LoginPage.js — not every spec.
 *
 * Assertions philosophy (Cypress):
 *   - `.should(...)` is AUTO-RETRYING — Cypress polls up to
 *     `defaultCommandTimeout` (10s in our config) until the assertion
 *     passes or the timeout fires. That built-in retry is our "wait"
 *     for the Vaadin SPA's async render.
 *   - Use `cy.url().should('include', '#!MainView')` after login —
 *     NOT `cy.url().should('not.include', '/LoginView')`. The path
 *     never changes because Vaadin uses HASH-BASED ROUTING (see
 *     TC-CY-001 comment below for details).
 *
 * Credentials:
 *   - Read via `Cypress.env('COMPANY' | 'USERNAME' | 'PASSWORD')`.
 *   - Wired in cypress.config.js from the .env file.
 *   - NEVER hardcode credentials in this file.
 */

import loginPage from '../pages/LoginPage';

// ── Allure labels API ────────────────────────────────────────────────
// `allure-js-commons` is the cross-framework label/step API that
// `allure-cypress` re-exports through its plugin hooks. Importing it
// as a namespace gives us functions like allure.feature(...),
// allure.severity(...), allure.parentSuite(...) — the same vocabulary
// the Python tests use via @allure.feature / @allure.severity.
import * as allure from 'allure-js-commons';

describe('Login', () => {

  /**
   * Navigate fresh to /LoginView before every test.
   *
   * Why in beforeEach and not inside each `it()`?
   *   - Every test needs the login page loaded.
   *   - Cypress resets the browser context between tests, so the
   *     navigation must be repeated rather than shared.
   *
   * Note: we rely on Cypress's default behavior of clearing cookies
   * and localStorage between tests. That's critical here — if the
   * "login-company" cookie ever leaked between tests, the second test
   * would see the 2-field form (cached) instead of the 3-field form,
   * and positional locators would shift by one.
   */
  beforeEach(() => {
    loginPage.visit();
  });

  // ──────────────────────────────────────────────────────────────────
  // TC-CY-001 — Valid Login with Correct Credentials
  // ──────────────────────────────────────────────────────────────────
  // Traces to: TC-CY-001
  //
  // Mirrors: Luna's Playwright test
  //          test_valid_login_redirects_away_from_login_page (TC-PW-001).
  //
  // Scenario:
  //   Given the user is on the login page
  //   When they enter a valid company, username, and password
  //   And click the ENTER button
  //   Then the URL contains "#!MainView" (Vaadin hash-routed redirect).
  //
  // Why this test matters:
  //   If login is broken, no other authenticated feature can be tested.
  //   This is the tripwire we want CI to fire first on any regression.
  //
  // Why we assert "#!MainView" and not "URL changed away from /LoginView":
  //   DANAConnect is a Vaadin SPA with HASH-BASED ROUTING. The path
  //   /LoginView stays forever — only the hash fragment changes:
  //       Before login:  https://portal.danaconnect.com/LoginView
  //       After login:   https://portal.danaconnect.com/LoginView#!MainView
  //   Any assertion that the URL changes AWAY from /LoginView will
  //   always fail. The only reliable logged-in signal is the presence
  //   of "#!MainView" in the URL.
  it('logs in with valid credentials and routes to #!MainView', () => {

    // ── Allure metadata for this test ────────────────────────────────
    // Mirrors what the Python tests get via decorators:
    //   parentSuite — top-level grouping in the Suites tab (per
    //                 framework: Playwright / Selenium / Cypress).
    //   feature     — feature group in the Behaviors tab.
    //   story       — same string as the Playwright / Selenium twins
    //                 of this test so the report can pivot on
    //                 "same scenario, different framework".
    //   severity    — BLOCKER: login is the front door; system
    //                 unusable if broken.
    //   displayName — readable title in the report's test list.
    allure.parentSuite('Cypress');
    allure.feature('Login');
    allure.story('Valid login routes user to MainView');
    allure.severity('blocker');
    allure.displayName('Valid credentials authenticate and route to #!MainView');

    // ── Sanity check: credentials are actually set ───────────────────
    // If .env is missing a value, Cypress.env() returns '' (per the
    // fallback in cypress.config.js). This check makes that failure
    // explicit instead of showing up later as a mysterious "login
    // failed" when we click ENTER with empty fields.
    const company  = Cypress.env('COMPANY');
    const username = Cypress.env('USERNAME');
    const password = Cypress.env('PASSWORD');

    expect(company,  'COMPANY env var is not set').to.be.a('string').and.not.be.empty;
    expect(username, 'USERNAME env var is not set').to.be.a('string').and.not.be.empty;
    expect(password, 'PASSWORD env var is not set').to.be.a('string').and.not.be.empty;

    // ── Wait for the Vaadin form to finish rendering ────────────────
    // Cypress retries `.should('be.visible')` up to defaultCommandTimeout
    // (10s). Asserting visibility on all four inputs before typing
    // guarantees the form is fully drawn — this replaces Playwright's
    // `page.wait_for_load_state("networkidle")`.
    loginPage.companyInput.should('be.visible');
    loginPage.usernameInput.should('be.visible');
    loginPage.passwordInput.should('be.visible');
    loginPage.enterButton.should('be.visible');

    // ── Act: perform the login ──────────────────────────────────────
    // The page object's login() method fills all three fields and
    // clicks ENTER in one call.
    loginPage.login(company, username, password);

    // ── Assert: URL contains the logged-in hash ─────────────────────
    // `cy.url().should('include', '#!MainView')` is auto-retrying, so
    // it naturally tolerates the small delay between the click and the
    // Vaadin client-side route change.
    cy.url().should('include', '#!MainView');
  });

  // ──────────────────────────────────────────────────────────────────
  // TC-CY-002 — All 7 Login Page Elements Are Visible
  // ──────────────────────────────────────────────────────────────────
  // Traces to: TC-CY-002
  //
  // Mirrors: Luna's Playwright test
  //          test_all_login_page_elements_are_visible (TC-PW-002).
  //
  // Scenario:
  //   Given a fresh browser session (no cached company)
  //   When the user navigates to /LoginView
  //   Then all 7 login-page elements are visible:
  //       1. Company input
  //       2. Username input
  //       3. Password input
  //       4. ENTER button
  //       5. Privacy Policy link
  //       6. Terms of Use link
  //       7. Copyright footer
  //
  // Why this test matters:
  //   Pure UI verification — no login is performed, no credentials
  //   required. It catches regressions where a developer accidentally
  //   hides or removes a required element (footer, privacy link, etc.).
  //   Fast, credential-free, safe to run constantly.
  //
  // Why no credentials are read:
  //   This test never submits the form. It only asserts that the form
  //   is *drawn correctly*. So no Cypress.env() calls.
  it('shows all 7 login page elements on a fresh visit', () => {
    // ── Allure metadata ──────────────────────────────────────────────
    // CRITICAL (not BLOCKER) because a missing element is a regression
    // but not release-blocking the way a broken login would be.
    // Same story string as the Playwright / Selenium twins.
    allure.parentSuite('Cypress');
    allure.feature('Login');
    allure.story('Login page renders all 7 required elements');
    allure.severity('critical');
    allure.displayName('All 7 login page elements are visible on a fresh visit');

    // Each `.should('be.visible')` is an auto-retrying assertion —
    // Cypress polls up to defaultCommandTimeout (10s) waiting for the
    // element to render. On a Vaadin SPA that's exactly the safety
    // net we want.

    // 1. Company input (first text input)
    loginPage.companyInput.should('be.visible');

    // 2. Username input (second text input)
    loginPage.usernameInput.should('be.visible');

    // 3. Password input (input[type="password"])
    loginPage.passwordInput.should('be.visible');

    // 4. ENTER button (Vaadin .v-button[role="button"])
    loginPage.enterButton.should('be.visible');

    // 5. Privacy Policy link. The getter already filters by a regex
    // that matches both English and Spanish labels and yields the
    // first match, so we just assert visibility on the yielded element.
    loginPage.privacyPolicyLink.should('be.visible');

    // 6. Terms of Use link — same multi-locale strategy as Privacy.
    loginPage.termsOfUseLink.should('be.visible');

    // 7. Copyright footer (`.v-label-Corp` — stable Vaadin class).
    loginPage.footer.should('be.visible');
  });
});
