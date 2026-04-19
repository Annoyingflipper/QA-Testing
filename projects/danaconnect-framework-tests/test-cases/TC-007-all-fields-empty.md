# TC-PW-007 / TC-SE-007 / TC-CY-007 — Login with All Fields Empty

## Info

| Field | Value |
|-------|-------|
| Priority | High |
| Type | Negative / Validation |
| Feature | Login Page |
| Automated | Pending (all 3 frameworks) |

## Preconditions
- Browser is open
- No cached session

## Steps

| # | Action | Expected Result |
|---|--------|----------------|
| 1 | Navigate to `https://portal.danaconnect.com/` | Login page loads |
| 2 | Leave all fields empty | All fields are blank |
| 3 | Click the ENTER button | Validation error is displayed — user is not logged in |

## Expected Result
Login is prevented. A validation message or error is shown indicating that fields are required. User remains on the login page.

## Notes
- Need to confirm whether validation is client-side (HTML5 required attribute) or server-side.
- Capture exact validation behavior during first manual run.
