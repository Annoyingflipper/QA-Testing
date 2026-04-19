# Team Collaboration Rules & Best Practices

## Ground Rules

1. **No silos.** Every engineer shares findings that touch another domain immediately — don't wait for triage.
2. **Write it down.** If it's not in a file in this repo, it didn't happen. Verbal agreements get formalized.
3. **Review before merge.** Every test plan and test case gets peer-reviewed by at least one other engineer before it's considered final.
4. **Reproduce before reporting.** Every bug must have verified reproduction steps. "It broke" is not a bug report.
5. **Automate what repeats.** If a manual test is run more than 3 times, it becomes a candidate for Casey's automation backlog.
6. **Severity is not negotiable.** Use the severity definitions consistently. Don't inflate or deflate to game priority.

## Peer Review Assignments

| Author   | Primary Reviewer | Secondary Reviewer |
|----------|------------------|--------------------|
| Jordan   | Sam              | Riley              |
| Riley    | Jordan           | Casey              |
| Sam      | Jordan           | Morgan             |
| Morgan   | Sam              | Casey              |
| Casey    | Riley            | Jordan             |

## File Naming Conventions

| Type            | Pattern                                    | Example                          |
|-----------------|--------------------------------------------|----------------------------------|
| Test Plan       | `test-plans/TP-<area>-<name>.md`           | `TP-AUTH-login-flow.md`          |
| Test Case       | `test-cases/TC-<area>-<number>.md`         | `TC-FUNC-001.md`                 |
| Bug Report      | `bug-reports/BUG-<number>.md`              | `BUG-001.md`                     |
| Regression Suite| `regression-suites/RS-<type>-<area>.md`    | `RS-SMOKE-auth.md`               |
| Handoff         | `docs/handoffs/HANDOFF-<from>-to-<to>.md`  | `HANDOFF-jordan-to-sam.md`       |
| Automation      | `automation/<area>/<test-name>.js`         | `automation/auth/login.spec.js`  |

## Definition of Done (for test artifacts)

A test case is "done" when:
- [ ] Steps are specific and reproducible by any team member
- [ ] Expected results are stated for every step
- [ ] Preconditions and test data are documented
- [ ] Priority and type are assigned
- [ ] Peer review is complete
- [ ] Linked to the relevant test plan

A bug report is "done" when:
- [ ] Reproduction steps verified by a second engineer
- [ ] Environment documented
- [ ] Screenshots/evidence attached
- [ ] Severity and priority assigned
- [ ] Assigned to an owner

## Escalation Matrix

| Severity | Response Time | Who Acts                    | Who's Notified      |
|----------|---------------|-----------------------------|---------------------|
| Critical | Immediate     | Discoverer + Alex           | Entire team         |
| High     | < 4 hours     | Assigned owner              | Alex + related eng  |
| Medium   | Next triage   | Assigned owner              | Alex                |
| Low      | Backlog       | Assigned owner              | Logged only         |
