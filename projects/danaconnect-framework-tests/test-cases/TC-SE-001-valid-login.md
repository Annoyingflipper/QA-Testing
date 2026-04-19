# TC-SE-001 — Valid Login with Correct Credentials (Selenium)

## Info

| Field | Value |
|-------|-------|
| ID | TC-SE-001 |
| Framework | Selenium |
| Priority | Critical |
| Type | Positive / Functional |
| Feature | Login Page |
| Automated | Yes — `automation/selenium/tests/test_login_valid.py::test_valid_login_redirects_away_from_loginview` |
| Author | Max (Selenium Test Writer) |

## Preconditions
- Chrome browser is installed
- `.env` file contains `BASE_URL`, `COMPANY`, `USERNAME`, and `PASSWORD` (non-empty)
- User has no existing authenticated session in Chrome
- `portal.danaconnect.com` is reachable from the test runner

## Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Launch Chrome (via Selenium WebDriver) and navigate to `BASE_URL + /LoginView` | Login page loads; Company, Username, Password fields and ENTER button are present |
| 2 | Enter the valid `COMPANY` value into the Company input | Text appears in the field |
| 3 | Enter the valid `USERNAME` value into the Username input | Text appears in the field |
| 4 | Enter the valid `PASSWORD` value into the Password input | Password is masked (dots/asterisks) |
| 5 | Click the `ENTER` button | Form submits; browser is redirected to a non-`/LoginView` URL (the user's main dashboard) |

## Expected Result
The browser's current URL **no longer contains `/LoginView`** within a reasonable timeout (10 seconds). This indicates the user has been authenticated and redirected away from the login page.

## Assertion Strategy (Selenium-specific)
- Use `WebDriverWait` with `EC.url_changes()` or a custom lambda to wait for the URL to change from the login URL.
- Avoid asserting a specific destination URL until the exact dashboard path is confirmed, because it may vary per user account.

## Notes
- **Never** hardcode credentials in the test. All values come from the `credentials` fixture in `conftest.py`, which reads from `.env`.
- After first successful run, we can tighten the assertion to check for a specific dashboard URL pattern.
- This test is the "gate" — if it fails, most other login tests are invalid (they assume we CAN reach the login page).
