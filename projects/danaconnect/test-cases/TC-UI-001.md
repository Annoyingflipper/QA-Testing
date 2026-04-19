## TC-UI-001: Login Page Renders Correctly on Desktop

**Priority:** P0 (Critical)
**Type:** UI/Visual
**Status:** Not Run
**Owner:** Riley (UI/UX QA)
**Reviewer:** Jordan (Functional QA)
**Test Plan:** TP-AUTH-001

---

### Objective
Verify the login page renders correctly on standard desktop viewports with all elements properly positioned, styled, and visible.

### Preconditions
- Browser: Chrome (latest), viewport 1920x1080 and 1440x900
- No active session
- Default zoom level (100%)

### Test Steps

1. Navigate to https://portal.danaconnect.com/ at 1920x1080
   **Expected:** Page loads without visual errors, no layout shift.

2. Verify the COMPANY label and input field
   **Expected:**
   - Label text "COMPANY" is visible above or beside the input
   - Placeholder text "Enter your company code" is visible
   - Input field has consistent styling (border, padding, font)
   - Field is full-width within its container

3. Verify the USERNAME label and input field
   **Expected:**
   - Label text "USERNAME" is visible
   - Placeholder text "Enter your user name" is visible
   - Consistent styling with Company field

4. Verify the PASSWORD label and input field
   **Expected:**
   - Label text "PASSWORD" is visible
   - Placeholder text "Enter your password DANA" is visible
   - Input type is password (characters masked on entry)
   - Consistent styling with other fields

5. Verify the ENTER button
   **Expected:**
   - "ENTER" text is visible on the button
   - Button is visually distinct (clear call-to-action)
   - Button is positioned below the form fields
   - Hover state provides visual feedback

6. Verify footer elements
   **Expected:**
   - "Privacy Policy" link is visible and clickable
   - "Terms of Use of the Service" link is visible and clickable
   - "DANAConnect Corp. All Rights Reserved" text visible
   - Footer is positioned at the bottom

7. Check overall layout
   **Expected:**
   - Form is centered on the page (or follows design spec)
   - No horizontal scrollbar
   - No overlapping elements
   - Consistent spacing between all elements
   - Background/branding consistent with DANAConnect identity

8. Resize viewport to 1440x900 and repeat visual checks
   **Expected:** All elements still visible and properly positioned, no clipping or overflow.

### Post-conditions
- Screenshot captured for visual baseline (for Casey's automation)

### Handoff Notes
- **→ Casey:** Capture a screenshot at each viewport for visual regression baseline. Use Playwright's screenshot comparison for future runs.
- **→ Jordan:** Confirm the placeholder text "Enter your password DANA" is intentional or a possible bug. The "DANA" suffix is unusual.

### Observations to Document
- [ ] Color values for all text and backgrounds (hex codes via DevTools)
- [ ] Font family, size, weight for all text
- [ ] Spacing values (padding, margin) between form elements
- [ ] Border styles on input fields
- [ ] Button dimensions and border-radius
