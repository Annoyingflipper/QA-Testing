## TC-FUNC-001: Valid User Login with Correct Credentials

**Priority:** P0 (Critical)
**Type:** Functional
**Status:** Not Run
**Owner:** Jordan (Functional QA)
**Reviewer:** Sam (Security QA)
**Test Plan:** TP-AUTH-001

---

### Objective
Verify that a user can successfully log into the DANAConnect platform with valid company code, username, and password credentials.

### Preconditions
- Valid test account exists with known company code, username, and password
- User is not currently logged in
- Browser cache/cookies cleared (or incognito mode)
- Network connection is stable

### Test Data
- Company Code: [valid test company code]
- Username: [valid test username]
- Password: [valid test password]

### Test Steps

1. Navigate to https://portal.danaconnect.com/
   **Expected:** Login page loads with three input fields (Company, Username, Password), ENTER button, Privacy Policy link, Terms of Use link, and copyright footer visible.

2. Click on the "Company" input field and enter the valid company code
   **Expected:** Field accepts input. Text is visible in the field.

3. Click on the "Username" input field and enter the valid username
   **Expected:** Field accepts input. Text is visible in the field.

4. Click on the "Password" input field and enter the valid password
   **Expected:** Field accepts input. Characters are masked (dots or asterisks).

5. Click the "ENTER" button
   **Expected:**
   - A loading indicator or transition occurs
   - User is redirected to the main platform page (dashboard or home)
   - Login page is no longer displayed
   - User's session is established (observable via cookies/network tab)

6. Verify the authenticated state
   **Expected:**
   - Platform content is accessible
   - User identity is displayed (name, avatar, or company info)
   - Navigation menu is available
   - No error messages displayed

### Post-conditions
- User is authenticated and has an active session
- Session token/cookie is created
- Subsequent page navigations do not require re-authentication

### Edge Cases (→ Handoff notes)
- **→ Sam:** Verify the session token created in step 5 has Secure, HttpOnly, SameSite flags (TC-SEC-011)
- **→ Riley:** Verify the loading transition/redirect is visually smooth, no layout shift (TC-UI-008)
- **→ Morgan:** Measure the time from ENTER click to dashboard load (TC-PERF-002)
- **→ Casey:** Automate this as the primary smoke test. This is the #1 automation candidate.

### Notes
- This is the single most critical test case for the platform. If login fails, nothing else can be tested.
- Must pass before any other test case execution proceeds.
- Run on all browsers in the compatibility matrix.
