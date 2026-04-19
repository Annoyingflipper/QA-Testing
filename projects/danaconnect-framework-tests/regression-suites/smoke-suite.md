# Smoke Regression Suite — DANAConnect Framework Tests

## Document Info

| Field | Value |
|-------|-------|
| Document ID | RS-SMOKE-001 |
| Created | 2026-04-17 |
| Purpose | Quick validation that critical paths work |
| Run time | ~2-3 minutes |

## When to Run
- Before starting a new testing session
- After any platform update or deployment
- As a sanity check before deeper testing

## Test Cases in This Suite

| # | Test Case ID | Title | Priority | Status |
|---|-------------|-------|----------|--------|
| 1 | TC-XXX-001 | Valid login with correct credentials | Critical | Pending |
| 2 | TC-XXX-002 | Verify all login page elements are present | High | Pending |
| 3 | TC-XXX-004 | Login with invalid company code | Critical | Pending |
| 4 | TC-XXX-007 | Login with all fields empty | High | Pending |

> **Note:** Replace `TC-XXX` with the framework prefix when running (TC-PW, TC-SE, or TC-CY).

## Pass Criteria
- All Critical tests pass
- No High priority test failures that block further testing
