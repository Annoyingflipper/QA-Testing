# DANAConnect Framework Tests

Multi-framework front-end test suite for the DANAConnect platform.

## Project Info

| Field | Value |
|-------|-------|
| Project | DANAConnect Framework Tests |
| Target URL | https://portal.danaconnect.com/ |
| Created | 2026-04-17 |
| CEO | vmaniglia |
| Purpose | Write front-end E2E tests across three frameworks for learning and comparison |

## Team Roster

| Name | Role | Specialist Skill | ID Prefix | Status |
|------|------|-----------------|-----------|--------|
| Luna | Playwright Test Writer | `/qa-playwright` | TC-PW | Active |
| Max | Selenium Test Writer | `/qa-selenium` | TC-SE | Active |
| Kai | Cypress Test Writer | `/qa-cypress` | TC-CY | Active |

## Critical Rules for All Agents

1. **WRITE tests only — NEVER run them.** The CEO runs all tests manually.
2. **ASK before creating any test.** Describe what you plan to write and wait for approval.
3. **Follow CEO Protocol** (ANNOUNCE, EXPLAIN, ASK, DO, REPORT, FLAG, PUSH) in every interaction.
4. **Use your specialist skill** (`/qa-playwright`, `/qa-selenium`, `/qa-cypress`) when writing tests.
5. **Heavy comments** — explain everything line by line for learning purposes.
6. **Traceability** — every automated test must include a comment referencing its test case ID (`# TC-PW-001`).

## Automation Frameworks

| Framework | Language | Location | Config |
|-----------|----------|----------|--------|
| Playwright | Python + pytest | `automation/playwright/` | `requirements.txt` |
| Selenium | Python + pytest | `automation/selenium/` | `requirements.txt` |
| Cypress | JavaScript | `automation/cypress/` | `package.json`, `cypress.config.js` |

## CI/CD

- **Platform:** Jenkins
- **Config:** `ci-cd/Jenkinsfile`

## Reporting

- **Tool:** Allure Report
- **Results:** `reports/allure-results/`
- **Generated report:** `reports/allure-report/`

## Credentials

- Stored in `.env` (gitignored, NEVER committed)
- Template in `.env.example`
- All tests read credentials from environment variables

## Directory Structure

```
danaconnect-framework-tests/
├── CLAUDE.md                    ← This file
├── .env                         ← Credentials (gitignored)
├── .env.example                 ← Credential template
├── .gitignore
├── agents/                      ← Agent role files
│   ├── luna-playwright.md
│   ├── max-selenium.md
│   └── kai-cypress.md
├── test-plans/                  ← Test plans
│   └── master-test-plan.md
├── test-cases/                  ← Detailed test cases
│   └── TC-XXX-NNN-*.md
├── regression-suites/           ← Regression suites
│   └── smoke-suite.md
├── bug-reports/                 ← Bug reports
├── automation/
│   ├── playwright/              ← Python + Playwright + pytest
│   │   ├── conftest.py
│   │   ├── pages/
│   │   ├── tests/
│   │   └── requirements.txt
│   ├── selenium/                ← Python + Selenium + pytest
│   │   ├── conftest.py
│   │   ├── pages/
│   │   ├── tests/
│   │   └── requirements.txt
│   └── cypress/                 ← JavaScript + Cypress
│       ├── cypress.config.js
│       ├── package.json
│       └── cypress/
│           ├── e2e/
│           ├── support/
│           └── pages/
├── ci-cd/
│   └── Jenkinsfile
├── reports/
│   └── (Allure results and reports)
├── docs/
│   ├── team-structure.md
│   ├── collaboration-rules.md
│   └── handoffs/
├── sessions/                    ← Shutdown/resume backups
├── launch-team.sh
└── shutdown-team.sh
```

## Dual-File Comment Convention

Every test file AND every page object is produced in TWO versions:

1. **Heavy-comment version** (default location — `tests/test_x.py`, `pages/x.py`):
   - Full module docstring
   - Paragraph-level docstrings on classes and methods
   - Inline comments explaining WHAT and WHY for learners
   - This is the canonical learning artifact

2. **Lean version** (under `lean/` subfolder — `tests/lean/test_x.py`, `pages/lean/x.py`):
   - One-line module docstring
   - Docstrings only where the name isn't self-explanatory
   - No inline comments except where the WHY is non-obvious
   - Traceability comment (`# Traces to: TC-XX-NNN`) stays — it is required
   - Same code as the heavy version

### Discovery rules
- `pytest` (default) runs ONLY the heavy-comment versions (lean folders are in `norecursedirs`).
- `pytest tests/lean/` runs the lean versions explicitly.

### Applies to all three frameworks
- Playwright: `automation/playwright/{pages,tests}/lean/`
- Selenium: `automation/selenium/{pages,tests}/lean/`
- Cypress: `automation/cypress/cypress/{pages,e2e}/lean/`

## Traceability Convention

Every test case gets an ID: `TC-<FRAMEWORK>-<NNN>`

| Framework | Prefix | Example |
|-----------|--------|---------|
| Playwright | TC-PW | TC-PW-001 |
| Selenium | TC-SE | TC-SE-001 |
| Cypress | TC-CY | TC-CY-001 |

Automated tests MUST include a traceability comment:
```python
# Traces to: TC-PW-001 — Valid login with correct credentials
def test_valid_login(page, login_page):
    ...
```

## CEO Session Persistence

The CEO (the user) gets a persistent session file alongside the agents at `sessions/latest/ceo-session.md`. This protects against connection drops mid-conversation — the on-disk file is the source of truth, so a dropped session never loses more than the last unflushed turn.

This applies to the **assistant helping the CEO** (i.e., Claude when run from inside this project directory). It does NOT apply to the agents Luna/Max/Kai — they have their own `<name>-session.md` files.

### Start of CEO session — required reading

Before any other work, the assistant MUST:

1. Read `sessions/latest/ceo-session.md` (the CEO live journal)
2. Read each agent's session file (`luna-session.md`, `max-session.md`, `kai-session.md`)
3. Summarize "where we left off" to the CEO in 3-5 lines
4. Ask the CEO whether to continue the prior plan or change direction

If `sessions/latest/ceo-session.md` does not exist, treat this as a fresh start and create the file when the first significant decision or step happens.

### During the session — live journaling

The assistant updates `sessions/latest/ceo-session.md` **incrementally**, not just at the end. Write after each:

- Decision (architectural, scope, process)
- Completed step (file written, command verified, gap diagnosed)
- New blocker
- Change in next-step plan

Sections of the file (keep them up-to-date):

- **Where we left off** — 1-3 lines, current state
- **Decisions log** — `<date> <decision> — <reason>`
- **Completed work** — chronological list
- **In progress** — what's mid-flight + why incomplete
- **Next step (top priority)** — the very next concrete action
- **Open questions / awaiting CEO input** — questions the assistant has parked
- **Blockers** — anything stuck
- **Notes for next session** — gotchas, decisions worth remembering

### End of session — shutdown

`./shutdown-team.sh` carries the CEO journal forward: the existing `sessions/latest/ceo-session.md` is copied into the new timestamped dir AND remains as the new `latest`. Past timestamped dirs hold the CEO snapshot at each shutdown moment.

### Why this exists

Connection drops happen. Without this protocol, every drop loses everything since the last shutdown. With it, the worst case is losing the current turn — everything before it is on disk.

## Safety Rules (All Agents)

1. NEVER delete files without CEO approval
2. NEVER overwrite existing code without showing changes first
3. NEVER modify files outside this workspace
4. NEVER commit .env files or credentials to git
5. NEVER hardcode credentials — use .env
6. NEVER install packages globally
7. NEVER force push or rewrite git history
8. NEVER push without CEO knowledge
9. NEVER purchase anything or sign up for accounts
10. NEVER run tests — CEO runs all tests
11. NEVER make architectural decisions alone
12. NEVER send emails/messages without CEO approval
13. NEVER run rm -rf on any directory
14. NEVER skip failing tests without CEO approval
15. NEVER ship tests without assertions
