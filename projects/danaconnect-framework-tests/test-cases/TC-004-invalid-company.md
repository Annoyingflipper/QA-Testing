# TC-PW-004 / TC-SE-004 / TC-CY-004 — Login with Invalid Company Code

## Info

| Field | Value |
|-------|-------|
| Priority | Critical |
| Type | Negative / Functional |
| Feature | Login Page |
| Automated | Pending (all 3 frameworks) |

## Preconditions
- Browser is open
- No cached session

## Steps

| # | Action | Expected Result |
|---|--------|----------------|
| 1 | Navigate to `https://portal.danaconnect.com/` | Login page loads |
| 2 | Enter `invalidcompany` in the Company field | Text is entered |
| 3 | Enter valid username in the Username field | Text is entered |
| 4 | Enter valid password in the Password field | Password is masked |
| 5 | Click the ENTER button | An error message is displayed indicating invalid credentials or company |

## Expected Result
Login fails. An error message is shown. User remains on the login page.

## Notes
- Capture the exact error message text during first manual run to use in assertions.
- The error message behavior (toast, inline, modal) needs to be confirmed.
