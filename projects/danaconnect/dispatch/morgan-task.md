# Task Assignment: Morgan — Performance QA Engineer
## Assigned By: Alex (QA Lead)
## Date: 2026-04-16
## Priority: P1

## Mission
The CEO wants a complete test of the DANAConnect login page at https://portal.danaconnect.com/. Your job is to establish performance baselines and identify any bottlenecks.

## Your Assignment
1. Read the existing test case `test-cases/TC-PERF-001.md` for context and targets
2. Using the browser, navigate to https://portal.danaconnect.com/
3. Open DevTools Network tab (disable cache) and measure:
   - DOMContentLoaded time
   - Full page load time
   - Total transfer size
   - Number of requests
   - Time to First Byte (TTFB)
4. Open DevTools Lighthouse tab and run a Performance audit:
   - Capture LCP (Largest Contentful Paint)
   - Capture CLS (Cumulative Layout Shift)
   - Capture overall Performance score
   - Note any specific recommendations Lighthouse gives
5. Identify the largest assets (images, CSS, JS bundles) and whether they're optimized
6. Check for render-blocking resources
7. Measure login submission response time — how long from clicking ENTER to getting a response (even with invalid credentials)
8. Run 5 measurements and calculate averages

## Expected Deliverables
- Performance baseline report with all metrics in a table
- Pass/fail assessment against targets from TC-PERF-001
- List of optimization recommendations
- Results written to `dispatch/results/morgan-results.md`
- Handoff to Casey for CI integration: write to `docs/handoffs/HANDOFF-morgan-to-casey.md`
- Handoff to Sam if response time differences suggest timing attacks: write to `docs/handoffs/HANDOFF-morgan-to-sam.md`

## Write Results To
`dispatch/results/morgan-results.md`

## Cross-Team Notes
- Riley is checking for layout shift (CLS) from the UI side — compare notes
- Sam needs to know if failed vs successful logins have different response times (timing attack vector)
- Casey will integrate Lighthouse into CI — provide the specific metrics and thresholds to check

## Deadline
End of session
