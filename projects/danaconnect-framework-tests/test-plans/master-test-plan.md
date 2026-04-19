# Master Test Plan — DANAConnect Framework Tests

## Document Info

| Field | Value |
|-------|-------|
| Document ID | TP-MASTER-001 |
| Project | DANAConnect Framework Tests |
| Target | https://portal.danaconnect.com/ |
| Created | 2026-04-17 |
| Author | QA Team Builder 2.0 |
| Status | Active |

## Objective

Write front-end E2E tests for the DANAConnect platform across three automation frameworks (Playwright, Selenium, Cypress) for learning and comparison. Tests are written by AI agents and run manually by the CEO.

## Scope

### In Scope
- Front-end E2E testing of the DANAConnect web portal
- Login page functionality (initial scope)
- Additional pages/features as directed by the CEO
- Three parallel implementations per test scenario (Playwright, Selenium, Cypress)

### Out of Scope
- API testing
- Performance/load testing
- Security penetration testing
- Mobile-specific testing
- Backend/database testing

## Test Strategy

Each test scenario is implemented in all three frameworks:
1. **Playwright** (Python + pytest) — written by Luna
2. **Selenium** (Python + pytest) — written by Max
3. **Cypress** (JavaScript) — written by Kai

All agents ask the CEO before writing any test. The CEO runs all tests.

## Test Environments

| Environment | URL | Purpose |
|-------------|-----|---------|
| Production | https://portal.danaconnect.com/ | Primary test target |

## Test Data

- Credentials stored in `.env` file
- Company: configured per environment
- Test user: configured per environment

## Features to Test

Features are added incrementally as directed by the CEO.

### Phase 1: Login Page (`/LoginView`)
- Valid login flow (company + username + password)
- Invalid credentials (wrong company, wrong user, wrong password)
- Empty field validation
- UI elements presence and state
- Links (Privacy Policy, Terms of Use)
- Field placeholder text verification

### Future Phases
- To be determined by CEO as we explore the platform

## Traceability

| Framework | Prefix | Example |
|-----------|--------|---------|
| Playwright | TC-PW | TC-PW-001 |
| Selenium | TC-SE | TC-SE-001 |
| Cypress | TC-CY | TC-CY-001 |

## Entry / Exit Criteria

### Entry
- Target URL is accessible
- Credentials are configured in `.env`
- Framework dependencies are installed

### Exit
- All planned test cases are written
- All tests pass when run by CEO
- No critical bugs remain open

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Production-only testing | Could affect real users | Tests use dedicated test account, read-only where possible |
| UI changes without notice | Tests break | Agents use Page Object Model for easy maintenance |
| Language/locale changes | Selectors break | Use data attributes or stable selectors where available |
