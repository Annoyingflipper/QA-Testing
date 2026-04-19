# TC-PW-001 / TC-SE-001 / TC-CY-001 — Valid Login with Correct Credentials

## Info

| Field | Value |
|-------|-------|
| Priority | Critical |
| Type | Positive / Functional |
| Feature | Login Page |
| Automated | Pending (all 3 frameworks) |

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
| 5 | Click the ENTER button | User is authenticated and redirected to the dashboard/home page |

## Expected Result
User successfully logs in and is redirected away from the login page.

## Notes
- The post-login destination URL needs to be confirmed after first successful test run.
- This is the most critical test case — if login doesn't work, nothing else can be tested.
