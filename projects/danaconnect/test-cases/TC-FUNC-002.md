## TC-FUNC-002: Login with Invalid Company Code

**Priority:** P0 (Critical)
**Type:** Functional — Negative
**Status:** Not Run
**Owner:** Jordan (Functional QA)
**Reviewer:** Sam (Security QA)
**Test Plan:** TP-AUTH-001

---

### Objective
Verify the system properly rejects login attempts with an invalid company code and displays an appropriate error message.

### Preconditions
- Browser at https://portal.danaconnect.com/
- No active session

### Test Data
- Company Code: `INVALIDCOMPANY999`
- Username: [valid test username]
- Password: [valid test password]

### Test Steps

1. Navigate to https://portal.danaconnect.com/
   **Expected:** Login page loads correctly.

2. Enter `INVALIDCOMPANY999` in the Company Code field
   **Expected:** Field accepts input.

3. Enter a valid username in the Username field
   **Expected:** Field accepts input.

4. Enter a valid password in the Password field
   **Expected:** Field accepts input, characters masked.

5. Click the "ENTER" button
   **Expected:**
   - Login is rejected
   - An error message is displayed to the user
   - Error message is generic (does NOT reveal whether the company code specifically was invalid)
   - User remains on the login page
   - Form fields are either preserved or cleared (document actual behavior)
   - No session token is created

### Post-conditions
- User is NOT authenticated
- No session cookie/token created
- Login page is still accessible for retry

### Handoff Notes
- **→ Sam (TC-SEC-016):** Document the exact error message. Verify it does not enumerate valid vs invalid company codes. The message should be identical whether company, user, or password is wrong.
- **→ Riley (TC-UI-007):** Verify error message styling — visible, readable, appropriate color/icon, accessible to screen readers.

### Notes
- Pay attention to response time — an invalid company code should not take noticeably longer or shorter than a valid company with wrong credentials (timing attack vector).
