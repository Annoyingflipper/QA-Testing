# Dispatch Plan: Full Login Page Test

**Issued by:** Alex (QA Lead)
**Date:** 2026-04-16
**Target:** https://portal.danaconnect.com/ — Login Page
**Reference Plan:** TP-AUTH-001
**Smoke Gate:** RS-SMOKE-AUTH
**Status:** ACTIVE

---

## Mission

Full coverage test of the DANAConnect login page across four disciplines: functional, security, UI/accessibility, and performance. All P0 test cases must be executed and results documented before the team moves past the login page into the platform interior.

---

## Preconditions (Blockers)

| # | Requirement | Status | Owner |
|---|-------------|--------|-------|
| B1 | Valid test credentials (company code, username, password) | **WAITING — CEO to provide** | Alex |
| B2 | Test environment accessible (portal.danaconnect.com reachable) | To verify | Morgan |
| B3 | All engineers have Chrome latest + DevTools access | To verify | Each engineer |

> **Nothing executes until B1 is resolved.** Engineers may begin non-credential work (page load, visual checks, HTTPS check, accessibility audit of the unauthenticated page) while waiting.

---

## Phase 1: Smoke Gate (Day 1, first 2 hours)

**Purpose:** Validate that the login page is alive and basic auth works before committing the full team.

| Order | Test Case | Owner | Depends On |
|-------|-----------|-------|------------|
| 1 | TC-PERF-001 — Page loads < 3s | Morgan | B2 |
| 2 | TC-UI-001 — Page renders correctly (desktop) | Riley | B2 |
| 3 | TC-FUNC-001 — Valid login succeeds | Jordan | B1 |
| 4 | TC-FUNC-002 — Invalid company code rejected | Jordan | B1 |
| 5 | TC-SEC-010 — HTTPS enforced | Sam | B2 |

**Gate rule:** If TC-FUNC-001 fails → STOP ALL WORK. Escalate to Alex and CEO immediately.

---

## Phase 2: Full Parallel Execution (Day 1–2)

Once smoke passes, all engineers execute in parallel within their domain.

---

### Jordan — Functional Testing

**Scope:** 20 test cases (TC-FUNC-001 through TC-FUNC-020)
**Priority order:** P0 first, then P1, then P2

| Block | Test Cases | Priority | Description |
|-------|-----------|----------|-------------|
| A | TC-FUNC-001 to 005 | P0 | Valid login + core negative cases (invalid company, user, password, empty fields) |
| B | TC-FUNC-006 to 009 | P1 | Partial field combos, correct company wrong credentials |
| C | TC-FUNC-010 to 014 | P1 | Field validation: max length, spaces, special chars, case sensitivity |
| D | TC-FUNC-015 to 017 | P1–P2 | Button state, Enter key submit, tab order |
| E | TC-FUNC-018 to 020 | P1–P2 | Privacy Policy link, Terms link, redirect after login |

**Deliverables:**
- Execute all 20 test cases, update status in each TC file
- File bug reports for any failures (BUG-xxx.md)
- Document exact error messages for each negative case (handoff to Sam for SEC-016 user enumeration check)
- Document actual redirect URL after successful login (handoff to Riley for UI continuity)
- Note any client-side validation behavior (handoff to Sam)

**Handoffs OUT:**
- → Sam: Error message text from TC-FUNC-002/003/004 (for user enumeration analysis)
- → Riley: Post-login redirect page layout (for UI continuity check)
- → Casey: Confirmed locators and field behaviors for automation
- → Morgan: Valid login flow timing observations

**Write test cases:** TC-FUNC-003 through TC-FUNC-020 need to be written in detail (only 001 and 002 exist). Use TC-FUNC-001 and TC-FUNC-002 as templates.

---

### Sam — Security Testing

**Scope:** 20 test cases (TC-SEC-001 through TC-SEC-020)
**Priority order:** P0 first (injection, brute force, HTTPS, session, info leakage)

| Block | Test Cases | Priority | Description |
|-------|-----------|----------|-------------|
| A | TC-SEC-001 to 006 | P0 | SQL injection + XSS injection across all 3 fields |
| B | TC-SEC-007, 008 | P0 | Brute force protection + rate limiting |
| C | TC-SEC-009, 010 | P0 | Password not in plaintext + HTTPS enforcement |
| D | TC-SEC-011 to 015 | P0–P1 | Session token flags, fixation, concurrent sessions, timeout, CSRF |
| E | TC-SEC-016 to 020 | P1–P2 | User enumeration, autocomplete, mixed content, directory traversal, response headers |

**Deliverables:**
- Execute all 20 test cases, update status in each TC file
- File bug reports for ANY security finding, even low severity
- For critical findings (injection success, session hijack, info disclosure): **immediate escalation to Alex — do not wait for standup**
- Document all response headers from the login endpoint
- Document all cookie/token attributes after successful login

**Handoffs OUT:**
- → Jordan: Any business logic abuse paths discovered
- → Morgan: Rate limiting thresholds observed (for load test calibration)
- → Casey: Injection payloads finalized for automated regression
- → Alex: Vulnerability severity assessment for each finding

**Handoffs IN:**
- ← Jordan: Error message text from negative functional tests (for user enumeration analysis at TC-SEC-016)

**Write test cases:** TC-SEC-002 through TC-SEC-020 need to be written in detail (only 001 exists). Use TC-SEC-001 as template.

---

### Riley — UI/UX & Accessibility Testing

**Scope:** 15 test cases (TC-UI-001 to 008, TC-A11Y-001 to 007)
**Priority order:** P0 first (rendering, password masking, labels, keyboard nav)

| Block | Test Cases | Priority | Description |
|-------|-----------|----------|-------------|
| A | TC-UI-001 to 003 | P0–P1 | Desktop, tablet, mobile rendering |
| B | TC-UI-004 to 006 | P1–P2 | Placeholder text, password masking, button states |
| C | TC-UI-007, 008 | P1–P2 | Error message styling, layout shift |
| D | TC-A11Y-001 to 003 | P0–P1 | Form labels, keyboard nav, focus indicators |
| E | TC-A11Y-004 to 007 | P1–P2 | Screen reader announcements, color contrast, heading hierarchy, ARIA |

**Deliverables:**
- Execute all 15 test cases, update status in each TC file
- Capture screenshots at all 3 viewport sizes (desktop 1920x1080, tablet 768x1024, mobile 375x812)
- Run Axe DevTools accessibility audit and attach findings
- Run Lighthouse accessibility score
- Document all CSS values (fonts, colors, spacing) for the visual baseline
- File bug reports for any failures
- **Flag the "Enter your password DANA" placeholder** — confirm if intentional or a bug (noted in TC-UI-001)

**Handoffs OUT:**
- → Casey: Screenshots for visual regression baseline + confirmed DOM selectors
- → Jordan: Any functional bugs found during UI testing
- → Morgan: CLS value from Lighthouse (if > 0.1, coordinate on which elements shift)
- → Alex: Accessibility blocker assessment (any WCAG AA failures that would block release)

**Write test cases:** TC-UI-002 through TC-UI-008, TC-A11Y-001 through TC-A11Y-007 need detail (only TC-UI-001 exists).

---

### Morgan — Performance Testing

**Scope:** 6 test cases (TC-PERF-001 through TC-PERF-006)
**Priority order:** P0 first (page load, API response time)

| Block | Test Cases | Priority | Description |
|-------|-----------|----------|-------------|
| A | TC-PERF-001 | P0 | Login page load time < 3 seconds |
| B | TC-PERF-002 | P0 | Login API response time < 2 seconds |
| C | TC-PERF-005 | P1 | Failed login response time (no timing difference) |
| D | TC-PERF-003 | P1 | Login under 50 concurrent users |
| E | TC-PERF-004, 006 | P2 | Login under 200 users, asset optimization |

**Deliverables:**
- Execute all 6 test cases, update status in each TC file
- Run Lighthouse Performance audit 5 times, report averages
- Capture network waterfall for the login page
- Measure login API (POST) response times for valid AND invalid credentials (timing attack vector — handoff to Sam)
- Document total transfer size, request count, render-blocking resources
- File bug reports for any SLA misses

**Handoffs OUT:**
- → Sam: Response time delta between valid vs invalid credentials (timing attack analysis)
- → Riley: CLS data if layout shift detected
- → Casey: Performance baselines for CI integration (Lighthouse CI thresholds)
- → Alex: Performance risk summary (any SLA at risk)

**Handoffs IN:**
- ← Sam: Rate limiting thresholds (to calibrate concurrent user tests and avoid triggering blocks)

**Write test cases:** TC-PERF-002 through TC-PERF-006 need detail (only TC-PERF-001 exists).

---

### Casey — Automation & CI/CD

**Scope:** Automation framework + pipeline setup (runs parallel to manual testing)

| Block | Task | Priority | Description |
|-------|------|----------|-------------|
| A | Wire up test credentials as env vars / secrets | P0 | Configure for local runs + CI |
| B | Get smoke suite running (RS-SMOKE-AUTH) | P0 | Automate TC-FUNC-001, 002–005, TC-SEC-010, TC-PERF-001 |
| C | Automate injection test suite | High | Parameterized data-driven tests from TC-SEC-001–006 payloads |
| D | Capture visual regression baseline | Medium | Screenshots at 3 viewports from Riley's specs |
| E | CI/CD pipeline operational | P0 | GitHub Actions workflow (convert from Jenkinsfile) |
| F | Test reporting in CI | P1 | HTML reports published as build artifacts |

**Deliverables:**
- Smoke suite runs green locally in at least one framework (Playwright preferred for speed)
- GitHub Actions workflow file committed and passing
- HTML test report generated and accessible from CI
- Visual regression baseline captured
- Document any flaky tests or environment issues

**Handoffs IN:**
- ← Jordan: Confirmed locators, field behaviors, expected error messages
- ← Riley: DOM selectors, screenshots for visual baseline
- ← Sam: Finalized injection payloads for parameterized tests
- ← Morgan: Lighthouse CI thresholds

**Handoffs OUT:**
- → Alex: Automation coverage report (which TCs are automated, which are manual-only)
- → All: CI dashboard URL once pipeline is live

---

## Phase 3: Triage & Reporting (Day 2–3)

| Activity | Owner | When |
|----------|-------|------|
| Collect all test results | Alex | After Phase 2 |
| Bug triage session | Alex + all | Day 2 afternoon |
| Risk register update | Alex | Day 2 |
| Test summary for CEO | Alex | Day 3 |
| Go/no-go for moving past login | Alex | Day 3 (pending results) |

---

## Escalation Rules

| Severity | Action | Timeline |
|----------|--------|----------|
| **Critical** (login bypass, injection success, data leak) | Stop testing. Notify Alex + CEO immediately. | Immediate |
| **High** (session vuln, HTTPS issue, P0 functional failure) | File bug, notify Alex. Continue other tests. | Within 1 hour |
| **Medium** (UI broken at one viewport, perf SLA miss) | File bug, flag at standup. | Next standup |
| **Low** (cosmetic, minor a11y, P2 functional) | File bug, standard triage. | Next triage session |

---

## Test Case Writing Assignments

48 test cases still need detailed write-ups. Each engineer writes their own domain:

| Engineer | Cases to Write | Template |
|----------|---------------|----------|
| Jordan | TC-FUNC-003 through TC-FUNC-020 (18 cases) | Use TC-FUNC-001, TC-FUNC-002 |
| Sam | TC-SEC-002 through TC-SEC-020 (19 cases) | Use TC-SEC-001 |
| Riley | TC-UI-002–008, TC-A11Y-001–007 (14 cases) | Use TC-UI-001 |
| Morgan | TC-PERF-002 through TC-PERF-006 (5 cases) | Use TC-PERF-001 |

**Rule:** Write the test case BEFORE executing it. No ad-hoc testing without documentation.

---

## Success Criteria for Login Phase

- [ ] All 53 P0 test cases executed and passed
- [ ] All 8 P0 smoke tests green
- [ ] Zero open Critical bugs
- [ ] Zero open High security bugs
- [ ] All High functional/UI bugs have a fix plan
- [ ] Performance baselines documented
- [ ] Smoke suite automated and running in CI
- [ ] Alex signs off on login phase completion
- [ ] CEO approves moving to Phase 2 (platform interior)

---

## Current Blocker

**B1: Test credentials are required before any authenticated testing can begin.**

The CEO has offered to provide them. Once received, Phase 1 smoke testing starts immediately.

Engineers: begin non-credential work now (TC-PERF-001, TC-UI-001–003, TC-A11Y-001–007, TC-SEC-010, TC-SEC-020).
