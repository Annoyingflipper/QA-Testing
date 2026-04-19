# Collaboration Rules — DANAConnect Framework Tests

## Golden Rules

1. **CEO approves everything.** No test gets written without CEO approval first.
2. **Write only, never run.** Agents write tests. CEO runs them.
3. **Stay in your lane.** Each agent writes only in their framework directory.
4. **Heavy comments.** Every line of code gets explained for learning purposes.
5. **Traceability.** Every test references a TC-XXX-NNN ID.

## Peer Review Table

When an agent writes a test, the other agents can review for consistency:

| Writer | Reviewers | What They Check |
|--------|-----------|----------------|
| Luna (Playwright) | Max, Kai | Same scenarios covered in Selenium/Cypress? |
| Max (Selenium) | Luna, Kai | Same scenarios covered in Playwright/Cypress? |
| Kai (Cypress) | Luna, Max | Same scenarios covered in Playwright/Selenium? |

## Handoff Format

When one agent discovers something relevant to another:

```markdown
## Handoff: [From Agent] → [To Agent]
**Date:** YYYY-MM-DD
**Subject:** [Brief description]
**Details:** [What was found and why it matters]
**Action needed:** [What the receiving agent should do]
```

Save handoffs in `docs/handoffs/`.

## File Ownership

| Directory | Owner |
|-----------|-------|
| `automation/playwright/` | Luna |
| `automation/selenium/` | Max |
| `automation/cypress/` | Kai |
| `test-plans/` | Any (CEO assigns) |
| `test-cases/` | Any (use correct prefix) |
| `bug-reports/` | Any |
| `docs/` | Any |
| `CLAUDE.md` | CEO only |
