# Test Plan: Login Page — DANAConnect Framework Tests

## Document Info

| Field | Value |
|-------|-------|
| Document ID | TP-LOGIN-001 |
| Feature | Login Page (`/LoginView`) |
| Target URL | https://portal.danaconnect.com/LoginView |
| Created | 2026-04-17 |
| Status | Active |

## Feature Description

The DANAConnect login page is the entry point to the platform. Users must provide three credentials to authenticate:
1. **Company code** — identifies the organization
2. **Username** — identifies the user within the company
3. **Password** — authenticates the user

## Page Elements Discovered (Reconnaissance)

| Element | Type | Placeholder/Label |
|---------|------|-------------------|
| Company field | Text input | "Enter your company code" |
| Username field | Text input | "Enter your user name" |
| Password field | Password input | "Enter your password DANA" |
| ENTER button | Button | "ENTER" |
| Privacy Policy | Link | "Privacy Policy" |
| Terms of Use | Link | "Terms of Use of the Service" |
| Footer | Text | "DANAConnect Corp. All Rights Reserved" |

## Test Case Index

### Positive Tests

| ID (PW/SE/CY) | Title | Priority |
|----------------|-------|----------|
| TC-PW-001 / TC-SE-001 / TC-CY-001 | Valid login with correct credentials | Critical |
| TC-PW-002 / TC-SE-002 / TC-CY-002 | Verify all login page elements are present | High |
| TC-PW-003 / TC-SE-003 / TC-CY-003 | Verify field placeholder text | Medium |

### Negative Tests

| ID (PW/SE/CY) | Title | Priority |
|----------------|-------|----------|
| TC-PW-004 / TC-SE-004 / TC-CY-004 | Login with invalid company code | Critical |
| TC-PW-005 / TC-SE-005 / TC-CY-005 | Login with invalid username | Critical |
| TC-PW-006 / TC-SE-006 / TC-CY-006 | Login with invalid password | Critical |
| TC-PW-007 / TC-SE-007 / TC-CY-007 | Login with all fields empty | High |
| TC-PW-008 / TC-SE-008 / TC-CY-008 | Login with only company field filled | Medium |
| TC-PW-009 / TC-SE-009 / TC-CY-009 | Login with company and username only (no password) | Medium |

### UI / UX Tests

| ID (PW/SE/CY) | Title | Priority |
|----------------|-------|----------|
| TC-PW-010 / TC-SE-010 / TC-CY-010 | Password field masks input | High |
| TC-PW-011 / TC-SE-011 / TC-CY-011 | Privacy Policy link is clickable | Low |
| TC-PW-012 / TC-SE-012 / TC-CY-012 | Terms of Use link is clickable | Low |
| TC-PW-013 / TC-SE-013 / TC-CY-013 | Footer text is displayed | Low |

## Preconditions

- Browser is open to `https://portal.danaconnect.com/`
- No cached session (fresh page load)
- `.env` credentials are configured

## Test Data

| Scenario | Company | Username | Password |
|----------|---------|----------|----------|
| Valid login | (from .env) | (from .env) | (from .env) |
| Invalid company | invalidcompany | (from .env) | (from .env) |
| Invalid username | (from .env) | invaliduser | (from .env) |
| Invalid password | (from .env) | (from .env) | wrongpassword |
