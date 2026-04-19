# Task Assignment: Jordan — Functional QA Engineer
## Assigned By: Alex (QA Lead)
## Date: 2026-04-16
## Priority: P0

## Mission
The CEO wants a complete test of the DANAConnect login page at https://portal.danaconnect.com/. Your job is to cover all functional testing.

## Your Assignment
1. Read the existing test plan at `test-plans/TP-AUTH-login-flow.md` to see what's already planned
2. Read the existing test cases `test-cases/TC-FUNC-001.md` and `test-cases/TC-FUNC-002.md`
3. Using the browser, navigate to https://portal.danaconnect.com/ and explore the login page
4. Execute the functional test cases manually — document what you find for each one
5. Write any NEW test cases you discover are needed (beyond what's already planned)
6. Investigate the password placeholder text "Enter your password DANA" — is this intentional or a bug?
7. Test the Tab key order through all form fields
8. Test what happens when you submit with various combinations of empty/filled fields

## Expected Deliverables
- Updated test case files in `test-cases/` for any new cases found
- Results written to `dispatch/results/jordan-results.md`
- Handoff to Sam if you find any input validation concerns: write to `docs/handoffs/HANDOFF-jordan-to-sam.md`
- Handoff to Riley if you find any visual issues: write to `docs/handoffs/HANDOFF-jordan-to-riley.md`

## Write Results To
`dispatch/results/jordan-results.md`

## Cross-Team Notes
- Sam (Security) will be testing injection on the same fields — coordinate so you don't interfere
- Casey (Automation) will automate your test cases — make your steps precise and reproducible
- If you discover the login redirects somewhere after valid credentials, document the exact URL for the whole team

## Deadline
End of session
