## TC-PERF-001: Login Page Load Time Under 3 Seconds

**Priority:** P0 (Critical)
**Type:** Performance
**Status:** Not Run
**Owner:** Morgan (Performance QA)
**Reviewer:** Casey (Automation Engineer)
**Test Plan:** TP-AUTH-001

---

### Objective
Verify the login page loads within 3 seconds under standard network conditions, with acceptable Core Web Vitals scores.

### Preconditions
- Network: Broadband connection (>10 Mbps)
- Browser: Chrome latest, cache cleared
- DevTools Performance / Network tab open
- No active session

### Test Steps

1. Open Chrome DevTools → Network tab, disable cache
   **Expected:** Network tab ready to capture.

2. Navigate to https://portal.danaconnect.com/
   **Expected:** Page loads. Capture the following metrics:

   | Metric | Target | Actual |
   |--------|--------|--------|
   | DOMContentLoaded | < 1.5s | ___ |
   | Full page load | < 3.0s | ___ |
   | Total transfer size | < 2 MB | ___ |
   | Total requests | < 30 | ___ |

3. Open DevTools → Lighthouse → Run Performance audit
   **Expected:**

   | Core Web Vital | Target | Actual |
   |----------------|--------|--------|
   | LCP (Largest Contentful Paint) | < 2.5s | ___ |
   | FID (First Input Delay) | < 100ms | ___ |
   | CLS (Cumulative Layout Shift) | < 0.1 | ___ |
   | TTFB (Time to First Byte) | < 800ms | ___ |
   | Performance Score | > 80 | ___ |

4. Check for render-blocking resources
   **Expected:**
   - CSS is loaded efficiently (inline critical, defer non-critical)
   - JavaScript does not block first paint
   - No unnecessarily large assets

5. Repeat test 5 times and record average
   **Expected:** Average values meet targets consistently (not just once).

### Pass Criteria
- Average page load < 3.0 seconds
- LCP < 2.5 seconds
- CLS < 0.1
- Lighthouse performance score > 80

### Fail Criteria
- Average page load > 3.0 seconds → P1
- LCP > 4.0 seconds → P1
- CLS > 0.25 → P2
- Any single load > 5.0 seconds → P1 (investigate)

### Handoff Notes
- **→ Casey:** Integrate Lighthouse CI into the automation pipeline to track performance over time.
- **→ Riley:** If CLS is high, coordinate on which elements are shifting.
- **→ Sam:** Note the transfer size — large payloads may indicate unnecessary data exposure.

### Tools
- Chrome DevTools (Network, Performance, Lighthouse)
- WebPageTest (for waterfall analysis if needed)
