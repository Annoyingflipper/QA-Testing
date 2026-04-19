# TC-PW-002 / TC-SE-002 / TC-CY-002 — Verify All Login Page Elements Are Present

## Info

| Field | Value |
|-------|-------|
| Priority | High |
| Type | UI Verification |
| Feature | Login Page |
| Automated | Pending (all 3 frameworks) |

## Preconditions
- Browser is open
- No cached session (fresh page load without company pre-filled)

## Steps

| # | Action | Expected Result |
|---|--------|----------------|
| 1 | Navigate to `https://portal.danaconnect.com/` | Login page loads |
| 2 | Verify Company input field is visible | Field is present with label "COMPANY" |
| 3 | Verify Username input field is visible | Field is present with label "USERNAME" |
| 4 | Verify Password input field is visible | Field is present with label "PASSWORD" |
| 5 | Verify ENTER button is visible | Button is present with text "ENTER" |
| 6 | Verify Privacy Policy link is visible | Link text "Privacy Policy" is displayed |
| 7 | Verify Terms of Use link is visible | Link text "Terms of Use of the Service" is displayed |
| 8 | Verify footer text is visible | "DANAConnect Corp. All Rights Reserved" is displayed |

## Expected Result
All 7 elements are present and visible on the login page.
