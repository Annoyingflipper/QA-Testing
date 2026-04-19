# Task Assignment: Casey — Test Automation Engineer
## Assigned By: Alex (QA Lead)
## Date: 2026-04-16
## Priority: P1

## Mission
The CEO wants a complete test of the DANAConnect login page at https://portal.danaconnect.com/. Your job is to review the existing automation code, improve it, and prepare it for execution.

## Your Assignment
1. Review the existing automation code across all 3 frameworks:
   - `automation/selenium-python/` — conftest, page object, test files
   - `automation/playwright-python/` — conftest, page object, test files
   - `automation/cypress-js/` — config, page object, test files
2. Check that the Page Object selectors match what's actually on the login page (visit the URL and verify)
3. If selectors need updating, fix them across all 3 frameworks
4. Review the Jenkinsfile at the project root — make sure paths are correct for the new project structure
5. Set up the `.env` file from `.env.example` (with placeholder values for now)
6. Explain to the CEO what you found and what you fixed
7. Create a README in `automation/` explaining how to install dependencies and run each framework

## Expected Deliverables
- Fixed/validated selectors in all 3 Page Objects if needed
- `.env` file created from `.env.example`
- `automation/README.md` with setup and run instructions
- Results written to `dispatch/results/casey-results.md`
- Read handoffs from Riley (selectors) and Morgan (perf thresholds) when they post them

## Write Results To
`dispatch/results/casey-results.md`

## Cross-Team Notes
- Riley will send you reliable CSS selectors via handoff — use those to update Page Objects
- Morgan will send you Lighthouse thresholds for CI integration
- Jordan and Sam's test cases should map to your automated tests — check that coverage matches
- Wait for other agents to produce handoffs before finalizing automation — you're downstream of their findings

## Deadline
End of session
