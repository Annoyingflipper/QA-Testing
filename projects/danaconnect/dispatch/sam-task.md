# Task Assignment: Sam — Security QA Engineer
## Assigned By: Alex (QA Lead)
## Date: 2026-04-16
## Priority: P0

## Mission
The CEO wants a complete test of the DANAConnect login page at https://portal.danaconnect.com/. Your job is to cover all security testing — OWASP Top 10, authentication security, and data protection.

## Your Assignment
1. Read the existing test case `test-cases/TC-SEC-001.md` and the security tests in `automation/selenium-python/tests/test_login_security.py`
2. Using the browser, navigate to https://portal.danaconnect.com/
3. Check HTTPS enforcement — try navigating to http:// and verify redirect
4. Inspect response headers using DevTools Network tab:
   - X-Frame-Options (clickjacking protection)
   - Content-Security-Policy
   - X-Content-Type-Options
   - Strict-Transport-Security (HSTS)
5. Test the login form for SQL injection on all 3 fields (company, username, password) — use the payloads from TC-SEC-001
6. Test for XSS on all 3 fields
7. Check error messages after failed login — do they leak information about which field was wrong?
8. Inspect cookies and session tokens in DevTools Application tab — check HttpOnly, Secure, SameSite flags
9. Check if the password is visible in network requests (DevTools Network tab — inspect the POST request payload)
10. Check for rate limiting — submit 5-10 rapid failed logins and see if the system blocks you

## Expected Deliverables
- Security findings documented with severity ratings
- New test case files for any issues found: `test-cases/TC-SEC-*.md`
- Results written to `dispatch/results/sam-results.md`
- If you find a CRITICAL vulnerability, note it clearly at the top of your results
- Handoff to Jordan for any business logic abuse scenarios: write to `docs/handoffs/HANDOFF-sam-to-jordan.md`
- Handoff to Morgan if you find rate-limiting issues: write to `docs/handoffs/HANDOFF-sam-to-morgan.md`

## Write Results To
`dispatch/results/sam-results.md`

## Cross-Team Notes
- Jordan is testing the same form functionally — coordinate so your injection tests don't interfere with functional testing
- Morgan may need your findings on rate limiting for performance testing
- Casey will automate your security test cases — make payloads and expected results precise
- IMPORTANT: All testing is authorized by the CEO. Test defensively — verify the app handles bad input safely, do not attempt to cause damage.

## Deadline
End of session
