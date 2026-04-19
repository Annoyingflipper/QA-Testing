# Test Plan: Authentication & Login Flow

**Document ID:** TP-AUTH-001
**Platform URL:** https://portal.danaconnect.com/
**Created:** 2026-04-16
**Status:** Draft

**Contributing Engineers:**
- Jordan (Functional) — Business logic, field validation, workflow
- Sam (Security) — Auth security, session management, injection
- Riley (UI/UX) — Visual, responsive, accessibility
- Morgan (Performance) — Login response times, concurrent auth load
- Casey (Automation) — Automation candidates flagged

---

## Scope

The login page is the gateway to the entire DANAConnect platform. It uses a three-field authentication model:

1. **Company Code** — Identifies the tenant/organization
2. **Username** — Identifies the user within that company
3. **Password** — Authenticates the user

Additional elements: ENTER button, Privacy Policy link, Terms of Use link, copyright footer.

This plan covers all testing of the login page, authentication flow, session creation, and related security concerns.

---

## Test Case Index

### Functional (Jordan)

| ID | Title | Priority |
|----|-------|----------|
| TC-FUNC-001 | Valid login with correct company/user/password | P0 |
| TC-FUNC-002 | Login with invalid company code | P0 |
| TC-FUNC-003 | Login with invalid username | P0 |
| TC-FUNC-004 | Login with invalid password | P0 |
| TC-FUNC-005 | Login with all fields empty | P0 |
| TC-FUNC-006 | Login with only company code filled | P1 |
| TC-FUNC-007 | Login with only username filled | P1 |
| TC-FUNC-008 | Login with only password filled | P1 |
| TC-FUNC-009 | Login with correct company but wrong user/pass combo | P0 |
| TC-FUNC-010 | Login field max length validation | P1 |
| TC-FUNC-011 | Login with leading/trailing spaces in fields | P1 |
| TC-FUNC-012 | Login with special characters in company code | P1 |
| TC-FUNC-013 | Login with case sensitivity check (username) | P1 |
| TC-FUNC-014 | Login with case sensitivity check (company code) | P1 |
| TC-FUNC-015 | Login button state (enabled/disabled based on input) | P2 |
| TC-FUNC-016 | Login via Enter key (keyboard submit) | P1 |
| TC-FUNC-017 | Tab order through form fields | P1 |
| TC-FUNC-018 | Privacy Policy link navigation | P2 |
| TC-FUNC-019 | Terms of Use link navigation | P2 |
| TC-FUNC-020 | Successful login redirects to expected page | P0 |

### Security (Sam)

| ID | Title | Priority |
|----|-------|----------|
| TC-SEC-001 | SQL injection in company code field | P0 |
| TC-SEC-002 | SQL injection in username field | P0 |
| TC-SEC-003 | SQL injection in password field | P0 |
| TC-SEC-004 | XSS injection in company code field | P0 |
| TC-SEC-005 | XSS injection in username field | P0 |
| TC-SEC-006 | XSS injection in password field | P0 |
| TC-SEC-007 | Brute force protection (account lockout) | P0 |
| TC-SEC-008 | Rate limiting on login attempts | P0 |
| TC-SEC-009 | Password not visible in page source/network | P0 |
| TC-SEC-010 | HTTPS enforcement (no HTTP fallback) | P0 |
| TC-SEC-011 | Session token security (HttpOnly, Secure, SameSite) | P0 |
| TC-SEC-012 | Session fixation prevention | P1 |
| TC-SEC-013 | Concurrent session handling | P1 |
| TC-SEC-014 | Session timeout behavior | P1 |
| TC-SEC-015 | CSRF protection on login form | P1 |
| TC-SEC-016 | Error messages don't leak info (user enumeration) | P0 |
| TC-SEC-017 | Password field autocomplete attribute | P2 |
| TC-SEC-018 | Login over mixed content check | P1 |
| TC-SEC-019 | Directory traversal via company code | P1 |
| TC-SEC-020 | Response header security (X-Frame-Options, CSP, etc.) | P1 |

### UI/UX & Accessibility (Riley)

| ID | Title | Priority |
|----|-------|----------|
| TC-UI-001 | Login page renders correctly on desktop (1920x1080) | P0 |
| TC-UI-002 | Login page renders correctly on tablet (768x1024) | P1 |
| TC-UI-003 | Login page renders correctly on mobile (375x812) | P1 |
| TC-UI-004 | Input field placeholder text visible and correct | P1 |
| TC-UI-005 | Password field masks input characters | P0 |
| TC-UI-006 | ENTER button visual state (default, hover, active, disabled) | P2 |
| TC-UI-007 | Error message display and styling | P1 |
| TC-UI-008 | Login page loads without layout shift (CLS) | P2 |
| TC-A11Y-001 | All form fields have associated labels | P0 |
| TC-A11Y-002 | Form is navigable via keyboard only | P0 |
| TC-A11Y-003 | Focus indicators visible on all interactive elements | P1 |
| TC-A11Y-004 | Error messages announced to screen readers | P1 |
| TC-A11Y-005 | Color contrast meets WCAG 2.1 AA (4.5:1 text) | P1 |
| TC-A11Y-006 | Page has proper heading hierarchy | P2 |
| TC-A11Y-007 | ARIA attributes correctly applied | P1 |

### Performance (Morgan)

| ID | Title | Priority |
|----|-------|----------|
| TC-PERF-001 | Login page load time < 3 seconds | P0 |
| TC-PERF-002 | Login API response time < 2 seconds | P0 |
| TC-PERF-003 | Login under 50 concurrent users | P1 |
| TC-PERF-004 | Login under 200 concurrent users | P2 |
| TC-PERF-005 | Failed login response time (no slower than success) | P1 |
| TC-PERF-006 | Page assets optimized (images, CSS, JS bundle size) | P2 |

---

## Automation Candidates (Casey)

| Test Case | Automation Priority | Reason |
|-----------|--------------------|----|
| TC-FUNC-001 | Immediate | Smoke test — run every build |
| TC-FUNC-002 to 009 | High | Core negative cases, highly repeatable |
| TC-SEC-001 to 006 | High | Injection tests — parameterized automation |
| TC-SEC-010 | High | Simple HTTPS check, easy to automate |
| TC-UI-001 | Medium | Visual snapshot baseline |
| TC-PERF-001, 002 | High | Baseline metrics in CI |
