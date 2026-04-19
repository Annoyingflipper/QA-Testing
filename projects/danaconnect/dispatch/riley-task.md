# Task Assignment: Riley — UI/UX QA Engineer
## Assigned By: Alex (QA Lead)
## Date: 2026-04-16
## Priority: P0

## Mission
The CEO wants a complete test of the DANAConnect login page at https://portal.danaconnect.com/. Your job is to cover all UI, visual, and accessibility testing.

## Your Assignment
1. Read the existing test case `test-cases/TC-UI-001.md` for context
2. Using the browser, navigate to https://portal.danaconnect.com/
3. Inspect the login page visually at desktop viewport (1920x1080)
4. Document all CSS values: colors, fonts, spacing, border-radius for every element
5. Check responsive behavior — resize to tablet (768px) and mobile (375px) viewports
6. Run an accessibility audit:
   - Do all form fields have proper labels (not just placeholders)?
   - Is the form navigable with keyboard only (Tab, Enter)?
   - Are focus indicators visible?
   - Check color contrast ratios (WCAG 2.1 AA requires 4.5:1 for text)
   - Does the page have proper heading hierarchy?
7. Check the ENTER button states: default, hover, active, disabled
8. Look for layout shift (CLS) when the page loads

## Expected Deliverables
- New test case files for any accessibility issues found: `test-cases/TC-A11Y-*.md`
- Visual baseline documentation with specific CSS values
- Results written to `dispatch/results/riley-results.md`
- Handoff to Jordan if you find functional issues: write to `docs/handoffs/HANDOFF-riley-to-jordan.md`
- Handoff to Casey with element selectors for automation: write to `docs/handoffs/HANDOFF-riley-to-casey.md`

## Write Results To
`dispatch/results/riley-results.md`

## Cross-Team Notes
- Jordan flagged the password placeholder "Enter your password DANA" — check if this looks intentional from a design perspective
- Casey needs reliable CSS selectors for automation — document the best selectors for each element
- Morgan is measuring page load — if you see any large unoptimized assets, flag them

## Deadline
End of session
