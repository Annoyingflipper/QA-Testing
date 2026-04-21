# TC-PW-001 / TC-SE-001 / TC-CY-001 — Valid Login with Correct Credentials

## Info

| Field | Value |
|-------|-------|
| Priority | Critical |
| Type | Positive / Functional |
| Feature | Login Page |
| Automated | Playwright: ✅ (2026-04-21) / Selenium: Pending / Cypress: Pending |
| Post-login URL | `https://portal.danaconnect.com/LoginView#!MainView` (confirmed) |

## Preconditions
- Browser is open
- No cached session
- Valid credentials available in `.env`

## Steps

| # | Action | Expected Result |
|---|--------|----------------|
| 1 | Navigate to `https://portal.danaconnect.com/` | Login page loads with Company, Username, Password fields and ENTER button |
| 2 | Enter valid company code in the Company field | Company code is displayed in the field |
| 3 | Enter valid username in the Username field | Username is displayed in the field |
| 4 | Enter valid password in the Password field | Password is masked (dots/asterisks) |
| 5 | Click the ENTER button | User is authenticated and URL changes to `/LoginView#!MainView` |

## Expected Result
User successfully logs in. The URL transitions from `/LoginView` to `/LoginView#!MainView` — DANAConnect is a Vaadin/GWT SPA that uses hash-based routing, so the path stays the same and only the hash fragment changes.

## Notes
- **Confirmed post-login URL (2026-04-21):** `https://portal.danaconnect.com/LoginView#!MainView`
- DANAConnect uses Vaadin/GWT hash routing — asserting "URL no longer contains /LoginView" would always fail. The correct assertion is that the URL contains `#!MainView`.
- This is the most critical test case — if login doesn't work, nothing else can be tested.
