# Regression Suite: Authentication Smoke Tests

**Suite ID:** RS-SMOKE-AUTH
**Duration:** ~15 minutes (manual), ~2 minutes (automated)
**Frequency:** Every build / daily
**Owner:** Casey (Automation) + Jordan (Manual fallback)

---

## Purpose
Quick validation that the authentication system is functional. If any smoke test fails, STOP and escalate — do not proceed with further testing.

## Execution Order

| # | Test Case | Owner | Auto? | Pass | Fail | Notes |
|---|-----------|-------|-------|------|------|-------|
| 1 | TC-PERF-001 — Page loads < 3s | Morgan | Yes | [ ] | [ ] | |
| 2 | TC-UI-001 — Page renders correctly | Riley | Yes | [ ] | [ ] | Visual snapshot |
| 3 | TC-FUNC-001 — Valid login succeeds | Jordan | Yes | [ ] | [ ] | **Gate** — stop if fails |
| 4 | TC-FUNC-002 — Invalid company rejected | Jordan | Yes | [ ] | [ ] | |
| 5 | TC-FUNC-003 — Invalid username rejected | Jordan | Yes | [ ] | [ ] | |
| 6 | TC-FUNC-004 — Invalid password rejected | Jordan | Yes | [ ] | [ ] | |
| 7 | TC-FUNC-005 — Empty fields rejected | Jordan | Yes | [ ] | [ ] | |
| 8 | TC-SEC-010 — HTTPS enforced | Sam | Yes | [ ] | [ ] | |
| 9 | TC-SEC-009 — Password not in plaintext | Sam | Yes | [ ] | [ ] | |
| 10 | TC-A11Y-002 — Keyboard navigable | Riley | No | [ ] | [ ] | |

## Gate Rules

- If test #3 (valid login) fails → **STOP ALL TESTING. Escalate to Alex.**
- If test #1 (page load) fails → Continue but flag performance degradation.
- If any security test fails → Escalate to Sam and Alex immediately.
- If 2+ tests fail → Treat as potential build/deployment issue, not individual bugs.

## Run Summary

**Date:** _______________
**Build/Version:** _______________
**Tester:** _______________
**Result:** PASS / FAIL / BLOCKED
**Total:** ___/10 passed
**Notes:** _______________
