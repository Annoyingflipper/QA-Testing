## TC-SEC-001: SQL Injection in Company Code Field

**Priority:** P0 (Critical)
**Type:** Security
**Status:** Not Run
**Owner:** Sam (Security QA)
**Reviewer:** Jordan (Functional QA)
**Test Plan:** TP-AUTH-001

---

### Objective
Verify the company code field is protected against SQL injection attacks. The application must sanitize or parameterize all user input before processing.

### Preconditions
- Browser at https://portal.danaconnect.com/
- DevTools Network tab open to monitor requests/responses
- No active session

### Test Data — Injection Payloads

| # | Payload | Attack Type |
|---|---------|-------------|
| 1 | `' OR '1'='1` | Classic OR-based bypass |
| 2 | `' OR '1'='1' --` | Comment-based bypass |
| 3 | `'; DROP TABLE users; --` | Destructive query (test on staging only) |
| 4 | `' UNION SELECT null,null,null --` | Union-based extraction |
| 5 | `1' AND SLEEP(5) --` | Time-based blind injection |
| 6 | `admin'--` | Auth bypass attempt |
| 7 | `' OR 1=1#` | MySQL comment variation |
| 8 | `%27%20OR%20%271%27%3D%271` | URL-encoded injection |

### Test Steps

1. Navigate to https://portal.danaconnect.com/
   **Expected:** Login page loads.

2. For each payload in the test data table:

   a. Enter the payload into the Company Code field
   b. Enter any value in Username (e.g., `testuser`)
   c. Enter any value in Password (e.g., `testpass`)
   d. Click "ENTER"
   
   **Expected for EACH payload:**
   - Login is rejected with a standard error message
   - No SQL error messages are displayed (no stack traces, no database errors)
   - Response does not indicate query manipulation
   - Response time for payload #5 is NOT delayed by ~5 seconds (would indicate blind injection)
   - No data is returned that shouldn't be (union-based)
   - Application remains stable and functional after each attempt

3. Monitor the Network tab for all requests
   **Expected:**
   - Request payload is properly encoded
   - Response does not contain database error strings
   - Response headers are consistent with normal error responses

### Post-conditions
- Application is stable and login page is functional
- No database state has been modified
- No unauthorized access was granted

### Pass Criteria
- ALL payloads rejected with generic error message
- ZERO SQL error messages exposed to the user
- ZERO successful authentications via injection
- No timing anomalies suggesting blind injection

### Fail Criteria (CRITICAL — Immediate Escalation)
- Any payload results in successful login → **P0 CRITICAL — escalate to Alex immediately**
- SQL error message displayed → **P0 CRITICAL — information disclosure**
- Time-based payload causes delayed response → **P1 HIGH — blind injection possible**
- Application crashes or becomes unresponsive → **P0 CRITICAL — DoS via injection**

### Handoff Notes
- **→ Jordan:** If any input validation is observed (client-side), document it. Sam will verify server-side validation independently.
- **→ Casey:** These payloads should be parameterized in an automated test suite for regression. Create a data-driven test that iterates all payloads.

### References
- OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection
- OWASP Testing Guide: Input Validation
