# QA-Testing Workspace

Multi-project QA testing workspace. Each project under `projects/` contains its own team, test plans, test cases, automation code, and agent roles.

## Workspace Structure

```
QA-Testing/
├── CLAUDE.md                   ← You are here (workspace overview)
├── .gitignore
├── docs/                       ← General docs (not project-specific)
│   └── process-walkthrough.md
└── projects/
    └── danaconnect/            ← DANAConnect Platform QA project
        ├── CLAUDE.md           ← Project-specific details
        ├── agents/             ← AI agent role files
        ├── automation/         ← Selenium, Playwright, Cypress
        ├── test-plans/
        ├── test-cases/
        ├── bug-reports/
        ├── regression-suites/
        ├── docs/               ← Team structure, collaboration rules
        ├── Jenkinsfile
        └── launch-team.sh
```

## Active Projects

| Project | Target | Team Size | Status |
|---------|--------|-----------|--------|
| [DANAConnect](projects/danaconnect/CLAUDE.md) | portal.danaconnect.com | 6 agents | Active |

## Adding a New Project

Use `/qa-team-builder` to set up a new project interactively, or create a new folder under `projects/` with the standard structure.

## Conventions (all projects)

- Test plans: `TP-<area>-<name>.md`
- Test cases: `TC-<area>-<number>.md`
- Bug reports: `BUG-<number>.md`
- Regression suites: `RS-<type>-<area>.md`
- Agent roles: `agents/<name>-<role>.md`
- Use `/qa-test-planner` for generating test artifacts
- Use `/qa-team-builder` for managing teams and agents
