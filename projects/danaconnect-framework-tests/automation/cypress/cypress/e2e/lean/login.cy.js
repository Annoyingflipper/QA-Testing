// Cypress login tests (lean — for the learning version see ../login.cy.js).

import loginPage from '../../pages/lean/LoginPage';
import * as allure from 'allure-js-commons';

describe('Login', () => {
  beforeEach(() => {
    loginPage.visit();
  });

  // Traces to: TC-CY-001
  it('logs in with valid credentials and routes to #!MainView', () => {
    allure.parentSuite('Cypress');
    allure.feature('Login');
    allure.story('Valid login routes user to MainView');
    allure.severity('blocker');
    allure.displayName('Valid credentials authenticate and route to #!MainView');

    const company  = Cypress.env('COMPANY');
    const username = Cypress.env('USERNAME');
    const password = Cypress.env('PASSWORD');

    expect(company,  'COMPANY env var is not set').to.be.a('string').and.not.be.empty;
    expect(username, 'USERNAME env var is not set').to.be.a('string').and.not.be.empty;
    expect(password, 'PASSWORD env var is not set').to.be.a('string').and.not.be.empty;

    loginPage.companyInput.should('be.visible');
    loginPage.usernameInput.should('be.visible');
    loginPage.passwordInput.should('be.visible');
    loginPage.enterButton.should('be.visible');

    loginPage.login(company, username, password);

    // Vaadin SPA uses hash routing — "#!MainView" is the logged-in signal.
    cy.url().should('include', '#!MainView');
  });

  // Traces to: TC-CY-002
  it('shows all 7 login page elements on a fresh visit', () => {
    allure.parentSuite('Cypress');
    allure.feature('Login');
    allure.story('Login page renders all 7 required elements');
    allure.severity('critical');
    allure.displayName('All 7 login page elements are visible on a fresh visit');

    loginPage.companyInput.should('be.visible');
    loginPage.usernameInput.should('be.visible');
    loginPage.passwordInput.should('be.visible');
    loginPage.enterButton.should('be.visible');
    loginPage.privacyPolicyLink.should('be.visible');
    loginPage.termsOfUseLink.should('be.visible');
    loginPage.footer.should('be.visible');
  });
});
