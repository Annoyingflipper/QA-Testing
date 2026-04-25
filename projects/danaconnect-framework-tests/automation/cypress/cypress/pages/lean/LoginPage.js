// DANAConnect login page object (Cypress, Vaadin/GWT — lean version).

class LoginPage {

  URL_PATH = '/LoginView';

  // Positional selectors — labels change language, DOM order doesn't.
  static TEXT_INPUT   = 'input[type="text"]';
  static PASSWORD_INP = 'input[type="password"]';
  // ENTER is a Vaadin <div>, not a native <button>.
  static ENTER_BUTTON = '.v-button[role="button"]';
  static FOOTER_TEXT  = '.v-label-Corp';
  static CAPTION_LINK = '.v-caption-label-signIn-company';

  get companyInput()  { return cy.get(LoginPage.TEXT_INPUT).eq(0); }
  get usernameInput() { return cy.get(LoginPage.TEXT_INPUT).eq(1); }
  get passwordInput() { return cy.get(LoginPage.PASSWORD_INP); }
  get enterButton()   { return cy.get(LoginPage.ENTER_BUTTON); }
  get footer()        { return cy.get(LoginPage.FOOTER_TEXT); }

  // Caption links share a class — filter by locale-agnostic regex.
  get privacyPolicyLink() {
    return cy.contains(LoginPage.CAPTION_LINK, /Privacy|Pol[íi]tica/);
  }
  get termsOfUseLink() {
    return cy.contains(LoginPage.CAPTION_LINK, /Terms|T[ée]rminos/);
  }

  visit() {
    cy.visit(this.URL_PATH);
    return this;
  }

  enterCompany(company)   { this.companyInput.clear().type(company);   return this; }
  enterUsername(username) { this.usernameInput.clear().type(username); return this; }
  enterPassword(password) { this.passwordInput.clear().type(password); return this; }
  clickEnter()            { this.enterButton.click();                  return this; }

  login(company, username, password) {
    this.enterCompany(company);
    this.enterUsername(username);
    this.enterPassword(password);
    this.clickEnter();
    return this;
  }
}

export default new LoginPage();
