# DANAConnect Platform — QA Project

QA testing project for the DANAConnect platform (https://portal.danaconnect.com/).
Managed by a 6-person senior QA engineering team with distinct specializations.

## Target Platform

- **URL:** https://portal.danaconnect.com/
- **Auth Model:** Company Code + Username + Password
- **Type:** Enterprise web-based communications platform

## Team

| Name | Role | Domain |
|------|------|--------|
| Alex | QA Lead / Test Manager | Strategy, coordination, sign-off |
| Jordan | Sr. Functional QA | Business logic, workflows, APIs |
| Riley | Sr. UI/UX QA | Visual, responsive, accessibility |
| Sam | Sr. Security QA | Auth, OWASP, penetration testing |
| Morgan | Sr. Performance QA | Load, response times, scalability |
| Casey | Sr. Automation Engineer | Framework, CI/CD, regression automation |

See `docs/team-structure.md` for full role definitions and collaboration map.

## Project Structure

```
danaconnect/
├── CLAUDE.md               ← You are here
├── agents/                 ← AI agent role files (one per team member)
├── automation/
│   ├── selenium-python/    ← Python + Selenium + pytest
│   ├── playwright-python/  ← Python + Playwright + pytest
│   └── cypress-js/         ← JavaScript + Cypress
├── test-plans/             ← High-level test strategies
├── test-cases/             ← Individual test case documents
├── bug-reports/            ← Bug report files
├── regression-suites/      ← Regression suites by area
├── docs/                   ← Team structure, collaboration, handoffs
│   └── handoffs/           ← Cross-team handoff notes
├── dispatch/               ← Task assignments from Alex to agents
│   └── results/            ← Agent work results
├── sessions/               ← Agent session backups (from shutdown)
│   └── latest/             ← Symlink to most recent session
├── Jenkinsfile             ← CI/CD pipeline
├── launch-team.sh          ← Opens 6 terminal windows with agents
├── dispatch-team.sh        ← Sends assignments to all agents
└── shutdown-team.sh        ← Saves progress and closes all agents
```

## Conventions

- Test plans: `TP-<area>-<name>.md`
- Test case IDs: `TC-<area>-<number>` (e.g., `TC-FUNC-001`, `TC-SEC-003`)
- Bug reports: `BUG-<number>.md`
- Regression suites: `RS-<type>-<area>.md`
- Handoffs: `HANDOFF-<from>-to-<to>-<topic>.md`
- Every test case gets peer review (see `docs/collaboration-rules.md`)

## Quick Start

```bash
# Launch all 6 QA agents in terminal windows
./launch-team.sh

# Brief Alex, then send assignments to all agents
./dispatch-team.sh

# Shut down all agents and save their progress
./shutdown-team.sh

# Relaunch — agents resume where they left off
./launch-team.sh

# Run Selenium smoke tests
cd automation/selenium-python && pytest -m smoke

# Run Playwright tests
cd automation/playwright-python && pytest -v

# Run Cypress tests
cd automation/cypress-js && npx cypress run
```

## Session Management

- `sessions/` — Contains timestamped backups from each shutdown
- `sessions/latest/` — Symlink to the most recent session
- When agents launch, they check for a previous session and resume automatically
