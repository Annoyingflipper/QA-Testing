# QA Team Setup — Full Process Walkthrough

**Created:** 2026-04-16
**Project:** DANAConnect Platform QA
**Purpose:** Documents every step we followed to go from an empty directory to a fully operational QA team with automation, test plans, and 6 independent agent terminals.

---

## What We Built

Starting from an empty git repo at `/Users/vmaniglia/Documents/GitHub/QA-Testing`, we built a complete QA testing operation for the DANAConnect web platform (portal.danaconnect.com).

**End result:**
- 6 senior QA engineers (AI agents), each with a defined role
- 3 automation frameworks (Selenium, Playwright, Cypress)
- Jenkins CI/CD pipeline
- Master test plan + feature-specific test plans
- 53 indexed test cases for authentication alone
- Detailed test cases with cross-team handoff notes
- Smoke regression suite
- Team collaboration rules, peer review matrix, escalation protocol
- Launch script to open all 6 agents in separate terminal windows

---

## Step-by-Step Process

### Phase 1: Workspace Setup

**What we did:**
1. Initialized the git repository
2. Created the directory structure:
   ```
   test-plans/          — High-level test strategies
   test-cases/          — Individual test case documents
   bug-reports/         — Bug report files
   regression-suites/   — Regression test suites
   automation/          — Test automation code
   docs/                — Team docs, handoffs, references
   docs/handoffs/       — Cross-team handoff notes
   agents/              — Agent role definition files
   ```
3. Created `.gitignore` (DS_Store, logs, node_modules, .env)
4. Created `CLAUDE.md` with project overview and conventions

**Why this matters:**
A consistent structure means every team member (human or AI) knows exactly where to find and place artifacts. Naming conventions (TC-FUNC-001, BUG-042, TP-AUTH) create traceability from requirements to test results.

---

### Phase 2: Platform Reconnaissance

**What we did:**
1. Opened Chrome browser and navigated to https://portal.danaconnect.com/
2. Read the page's accessibility tree to identify all elements
3. Documented what we found:
   - Login form with 3 fields: Company Code, Username, Password
   - ENTER button for form submission
   - Privacy Policy and Terms of Use links
   - Copyright footer
   - Placeholder text anomaly: "Enter your password DANA"

**Why this matters:**
You can't test what you don't understand. Reconnaissance maps the attack surface (for security), the user surface (for functional/UI), and the interaction points (for automation). This informs every test plan.

---

### Phase 3: Team Design

**What we did:**
1. Defined 6 senior engineering roles:
   - **Alex** — QA Lead / Test Manager (strategy, coordination, sign-off)
   - **Jordan** — Functional QA (business logic, workflows, APIs)
   - **Riley** — UI/UX QA (visual, responsive, accessibility)
   - **Sam** — Security QA (OWASP, auth, injection, penetration testing)
   - **Morgan** — Performance QA (load, speed, Core Web Vitals)
   - **Casey** — Automation Engineer (frameworks, CI/CD, Jenkins)

2. Created collaboration rules:
   - Peer review matrix (who reviews whose work)
   - Handoff protocol (how engineers pass findings across domains)
   - Escalation matrix (response times by severity)
   - Definition of Done (for test cases and bug reports)
   - File naming conventions

3. Mapped cross-team dependencies:
   - Jordan → Sam: Input fields needing security testing
   - Jordan → Riley: UI issues found during functional testing
   - Riley → Casey: Selectors and DOM patterns for automation
   - Sam → Morgan: Endpoints for load-based security testing
   - All → Alex: Risk and coverage reporting
   - All → Casey: Test cases to automate

**Why this matters:**
QA is not a solo activity. Different perspectives catch different bugs. A functional tester thinks about "does it work?" while a security tester thinks about "can it be abused?" Structured collaboration ensures no gaps.

---

### Phase 4: Test Planning

**What we did:**
1. Created the **Master Test Plan** (`TP-MASTER-danaconnect-platform.md`):
   - Scope definition (in/out)
   - Test strategy by level (smoke, functional, integration, UI, security, performance, regression)
   - Environment requirements (browsers, viewports, devices)
   - Entry/exit criteria
   - Risk assessment (6 identified risks with mitigations)
   - 5-phase timeline with ownership

2. Created the **Authentication Test Plan** (`TP-AUTH-login-flow.md`):
   - 20 functional test cases (Jordan)
   - 20 security test cases (Sam)
   - 7 UI/accessibility test cases (Riley)
   - 6 performance test cases (Morgan)
   - Automation candidate prioritization (Casey)

3. Created 5 detailed test cases as exemplars:
   - TC-FUNC-001: Valid login (functional)
   - TC-FUNC-002: Invalid company code (negative functional)
   - TC-SEC-001: SQL injection in company field (security)
   - TC-UI-001: Login page renders on desktop (UI)
   - TC-PERF-001: Login page load time (performance)

4. Created the **Smoke Regression Suite** (`RS-SMOKE-auth.md`):
   - 10 tests, ~15 min manual / ~2 min automated
   - Gate rules (which failures block the pipeline)

**Why this matters:**
Test plans ensure comprehensive coverage. Without them, testing becomes ad-hoc and misses critical scenarios. The structured format (ID, priority, steps, expected results) makes tests reproducible by anyone.

---

### Phase 5: Automation Framework Setup

**What we did:**

#### Framework 1: Python + Selenium + pytest
- `requirements.txt` — Dependencies with explanations
- `conftest.py` — pytest fixtures (browser setup/teardown, credentials, base URL)
- `pytest.ini` — Test runner configuration (markers, defaults)
- `pages/login_page.py` — Page Object Model with locators and actions
- `tests/test_login_functional.py` — 10 functional tests (Jordan's test cases)
- `tests/test_login_security.py` — SQL injection, XSS, HTTPS, error message tests (Sam's test cases)
- `.env.example` — Template for secrets

#### Framework 2: Python + Playwright + pytest
- Same structure as Selenium, demonstrating Playwright's simpler API
- Built-in screenshot support for visual regression
- Auto-waiting (less flaky than Selenium)

#### Framework 3: JavaScript + Cypress
- `package.json` — Node.js project with Cypress + reporting deps
- `cypress.config.js` — Cypress settings (viewport, timeouts, retries, reporter)
- `cypress/support/e2e.js` — Custom commands (cy.login)
- `cypress/pages/LoginPage.js` — Page Object with chainable methods
- `cypress/e2e/login/smoke.cy.js` — Smoke tests
- `cypress/e2e/login/security.cy.js` — Security tests with network interception

**All code includes inline comments explaining every concept for learning.**

**Why three frameworks:**
Each has strengths. Selenium is the industry standard. Playwright is faster and more modern. Cypress runs inside the browser and can intercept network requests. Learning all three builds a complete understanding.

---

### Phase 6: CI/CD Pipeline (Jenkins)

**What we did:**
- Created `Jenkinsfile` with a multi-stage pipeline:
  1. **Setup** — Install Python + Node dependencies (in parallel)
  2. **Smoke Tests** — Run smoke suite first (gate: fails = stop everything)
  3. **Full Test Suite** — All 3 frameworks run in parallel
  4. **Security Tests** — Dedicated security pass
  5. **Post** — Collect reports, notify team (pass/fail)

**Why Jenkins:**
Jenkins automates the "run tests" step. Instead of manually running pytest, it watches the repo and runs everything automatically. This catches regressions immediately.

---

### Phase 7: Agent Setup

**What we did:**
1. Created 6 role definition files in `agents/`:
   - Each file defines: personality, responsibilities, how they work, workspace rules, test case ID prefixes, what they say when starting
   - Each agent asks permission before doing significant work
   - Each agent explains concepts as they work (teaching mode)

2. Created `launch-team.sh`:
   - Opens 6 Terminal windows via AppleScript
   - Each window runs Claude Code with the role file loaded
   - Each agent introduces itself and asks the CEO for direction

**Why separate agents:**
Specialization produces better results. A focused security tester catches vulnerabilities a functional tester misses. Independent terminals let you manage each role at your own pace.

---

## Key Design Decisions

| Decision | Why |
|----------|-----|
| Page Object Model pattern | Single point of maintenance when UI changes |
| Secrets in .env (not code) | Security best practice — never commit passwords |
| pytest markers (smoke, security) | Run targeted subsets of tests |
| Parameterized tests | One function tests many payloads (DRY) |
| Cross-team handoff notes in test cases | Ensures nothing falls through cracks |
| Smoke tests as pipeline gate | Don't waste time on full suite if basics are broken |
| Parallel pipeline stages | Faster CI — 3 frameworks run simultaneously |
| Agent role files (not hardcoded prompts) | Easy to edit, version-controlled, reviewable |

---

## What's Needed to Run

| Prerequisite | Command |
|-------------|---------|
| Python 3.8+ | `python3 --version` |
| Node.js 18+ | `node --version` |
| Chrome browser | Installed on system |
| Selenium deps | `cd automation/selenium-python && pip install -r requirements.txt` |
| Playwright deps | `cd automation/playwright-python && pip install -r requirements.txt && playwright install` |
| Cypress deps | `cd automation/cypress-js && npm install` |
| Test credentials | Copy `.env.example` to `.env` and fill in values |
| Jenkins (optional) | `brew install jenkins-lts && jenkins-lts` |
| Claude Code | `claude` CLI installed |
