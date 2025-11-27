# QA Test Target: Bug Hunt Shop - Intentional Bugs Documentation

## Overview
This web application contains **47 intentional bugs** across 7 major categories, designed to simulate real-world QA testing scenarios you'll encounter in professional environments.

## How to Use This Test Target
1. **Open index.html** in a web browser
2. **Test each feature** systematically
3. **Document bugs you find** using proper QA reporting format
4. **Compare your findings** with this reference document
5. **Create test cases** for each scenario

---

## Bug Categories & Details

### 🔍 **CATEGORY 1: Search Functionality (5 bugs)**

**BUG #1 - Case Sensitivity**
- **Location:** Search input field
- **Issue:** Search is case-sensitive (should be case-insensitive)
- **Steps to Reproduce:** Search for "laptop" vs "Laptop" vs "LAPTOP"
- **Expected:** All should return results
- **Actual:** Only exact case matches work

**BUG #2 - No Whitespace Handling**
- **Location:** Search input field  
- **Issue:** Doesn't trim whitespace from search terms
- **Steps to Reproduce:** Search for " laptop " (with spaces)
- **Expected:** Should find results
- **Actual:** No results due to exact match requirement

**BUG #3 - Exact Match Only**
- **Location:** Search function
- **Issue:** Only finds exact name matches, no partial matching
- **Steps to Reproduce:** Search for "Gaming" instead of "Gaming Laptop"
- **Expected:** Should find "Gaming Laptop"
- **Actual:** No results found

**BUG #4 - Misleading Error Message**
- **Location:** Search results display
- **Issue:** Shows "Database connection failed" for no results
- **Steps to Reproduce:** Search for "xyz123"
- **Expected:** "No products found" message
- **Actual:** False database error message

**BUG #5 - Enter Key Not Working**
- **Location:** Search input field
- **Issue:** Pressing Enter doesn't trigger search
- **Steps to Reproduce:** Type search term and press Enter
- **Expected:** Search should execute
- **Actual:** Nothing happens

---

### 🛒 **CATEGORY 2: Shopping Cart (8 bugs)**

**BUG #6 - No Quantity Tracking**
- **Location:** Add to Cart functionality
- **Issue:** Can add same item multiple times without quantity counter
- **Steps to Reproduce:** Click "Add to Cart" multiple times on same product
- **Expected:** Quantity should increase
- **Actual:** Creates duplicate entries

**BUG #7 - No Add Confirmation**
- **Location:** Add to Cart button
- **Issue:** No visual feedback when item is added
- **Steps to Reproduce:** Add any item to cart
- **Expected:** Success message or visual indication
- **Actual:** No feedback provided

**BUG #8 - Wrong Tax Calculation**
- **Location:** Cart summary calculations
- **Issue:** Tax = subtotal + 0.085 instead of subtotal * 0.085
- **Steps to Reproduce:** Add $100 item, check tax calculation
- **Expected:** Tax should be $8.50 (8.5%)
- **Actual:** Tax shows $100.085

**BUG #9 - Backwards Shipping Logic**
- **Location:** Shipping calculation
- **Issue:** Charges shipping for orders over $100 (should be free)
- **Steps to Reproduce:** Add items totaling over $100
- **Expected:** Free shipping (shows $0.00)
- **Actual:** Still charges $5.99

**BUG #10 - Total Excludes Tax**
- **Location:** Total calculation
- **Issue:** Total = subtotal + shipping (missing tax)
- **Steps to Reproduce:** Add items and check total calculation
- **Expected:** Total should include tax
- **Actual:** Tax amount not added to total

**BUG #11 - Inconsistent Decimal Formatting**
- **Location:** Cart summary display
- **Issue:** Tax shows 3 decimal places instead of 2
- **Steps to Reproduce:** Add items and observe tax display
- **Expected:** All amounts show 2 decimal places
- **Actual:** Tax shows 3 decimal places

**BUG #12 - Clear Cart Doesn't Reset**
- **Location:** Clear Cart button
- **Issue:** Doesn't reset shipping cost to initial state
- **Steps to Reproduce:** Add items, then clear cart
- **Expected:** All values reset to $0.00, shipping to $5.99
- **Actual:** Calculations remain partially incorrect

**BUG #13 - Currency Symbol Missing**
- **Location:** formatCurrency function
- **Issue:** No dollar sign in currency formatting function
- **Steps to Reproduce:** Check helper function implementation
- **Expected:** Should include $ symbol
- **Actual:** Only shows numbers

---

### 📝 **CATEGORY 3: Contact Form (7 bugs)**

**BUG #14 - Weak Email Validation**
- **Location:** Email input validation
- **Issue:** Only checks for @ symbol presence
- **Steps to Reproduce:** Enter "test@" or "@test"
- **Expected:** Should reject incomplete emails
- **Actual:** Accepts invalid email formats

**BUG #15 - Phone Validation Too Strict**
- **Location:** Phone input validation
- **Issue:** Requires exactly 10 digits, rejects valid formats
- **Steps to Reproduce:** Enter "(555) 123-4567" or "555-123-4567"
- **Expected:** Should accept standard phone formats
- **Actual:** Rejects formatted phone numbers

**BUG #16 - No Name Validation**
- **Location:** Name input field
- **Issue:** Required field but no validation implemented
- **Steps to Reproduce:** Submit form with empty name
- **Expected:** Should show error message
- **Actual:** May accept empty names

**BUG #17 - Message Field Too Short**
- **Location:** Message textarea
- **Issue:** maxlength="50" is too restrictive
- **Steps to Reproduce:** Try to type a detailed message
- **Expected:** Should allow reasonable message length
- **Actual:** Cuts off after 50 characters

**BUG #18 - Form Doesn't Reset**
- **Location:** Form submission
- **Issue:** Form fields remain filled after successful submission
- **Steps to Reproduce:** Submit valid form
- **Expected:** Form should clear after success
- **Actual:** Fields retain entered data

**BUG #19 - Always Shows Success**
- **Location:** Form submission logic
- **Issue:** Shows success message even with validation errors
- **Steps to Reproduce:** Submit with various invalid data
- **Expected:** Should show appropriate error messages
- **Actual:** Eventually shows success regardless

**BUG #20 - No HTML Escaping**
- **Location:** Contact form processing
- **Issue:** Potential XSS vulnerability (inputs not sanitized)
- **Steps to Reproduce:** Enter HTML/script tags in form
- **Expected:** Should escape or reject HTML
- **Actual:** No input sanitization implemented

---

### 🔐 **CATEGORY 4: Login Security (10 bugs)**

**BUG #21 - Hardcoded Credentials**
- **Location:** Login authentication
- **Issue:** Username/password hardcoded in JavaScript
- **Steps to Reproduce:** View browser dev tools source
- **Expected:** Credentials should be server-side only
- **Actual:** Visible in client-side code

**BUG #22 - Case Sensitive Username**
- **Location:** Username validation
- **Issue:** "admin" works but "Admin" or "ADMIN" don't
- **Steps to Reproduce:** Try different case variations
- **Expected:** Username should be case-insensitive
- **Actual:** Only exact case match works

**BUG #23 - Information Disclosure**
- **Location:** Failed login messages
- **Issue:** Reveals when username exists ("Incorrect password for user 'admin'")
- **Steps to Reproduce:** Enter "admin" with wrong password
- **Expected:** Generic "Invalid credentials" message
- **Actual:** Confirms username exists

**BUG #24 - No Password Requirements**
- **Location:** Password validation
- **Issue:** Accepts weak passwords, no complexity requirements
- **Steps to Reproduce:** Use simple password like "123"
- **Expected:** Should enforce password complexity
- **Actual:** No password strength validation

**BUG #25 - Remember Me Doesn't Work**
- **Location:** Remember me functionality
- **Issue:** Checkbox doesn't actually implement remember functionality
- **Steps to Reproduce:** Login with remember me checked
- **Expected:** Should stay logged in on return visits
- **Actual:** No persistent session implemented

**BUG #26 - No Session Expiration**
- **Location:** Remember me storage
- **Issue:** localStorage has no expiration date
- **Steps to Reproduce:** Check localStorage after login
- **Expected:** Should expire after specified time
- **Actual:** Persists indefinitely

**BUG #27 - Form Doesn't Clear**
- **Location:** Successful login
- **Issue:** Login form remains filled after success
- **Steps to Reproduce:** Successfully log in
- **Expected:** Form should clear
- **Actual:** Username/password remain visible

**BUG #28 - No Rate Limiting**
- **Location:** Login attempts
- **Issue:** No protection against brute force attacks
- **Steps to Reproduce:** Make multiple failed login attempts
- **Expected:** Should lock account or delay after failures
- **Actual:** Unlimited attempts allowed

**BUG #29 - Password Visible in Dev Tools**
- **Location:** Form handling
- **Issue:** Password values accessible in browser debugging
- **Steps to Reproduce:** Open dev tools, inspect form data
- **Expected:** Password should be protected
- **Actual:** Visible in DOM and JavaScript

**BUG #30 - Generic Error Message**
- **Location:** Unknown user login
- **Issue:** "Login failed" is too vague
- **Steps to Reproduce:** Use non-existent username
- **Expected:** Could be more user-friendly
- **Actual:** Provides no guidance to user

---

### 🎯 **CATEGORY 5: User Experience (8 bugs)**

**BUG #31 - Navigation Doesn't Prevent Default**
- **Location:** Navigation links
- **Issue:** Clicking nav links may cause page jumps
- **Steps to Reproduce:** Click navigation links
- **Expected:** Smooth scroll to sections
- **Actual:** May have jerky scrolling behavior

**BUG #32 - Fixed Header Overlap**
- **Location:** Scroll positioning
- **Issue:** Fixed header covers content when scrolling to sections
- **Steps to Reproduce:** Click nav link to scroll to section
- **Expected:** Content visible below header
- **Actual:** Header covers top of section content

**BUG #33 - Search Input Length Too Restrictive**
- **Location:** Search input field
- **Issue:** maxlength="5" prevents searching longer product names
- **Steps to Reproduce:** Try to search for "Gaming Laptop"
- **Expected:** Should allow full product name entry
- **Actual:** Cuts off at 5 characters

**BUG #34 - No Search Debouncing**
- **Location:** Search input handling
- **Issue:** No performance optimization for search input
- **Steps to Reproduce:** Type rapidly in search field
- **Expected:** Should debounce input to prevent excessive calls
- **Actual:** No debouncing implemented

**BUG #35 - Event Listeners Not Cleaned**
- **Location:** JavaScript memory management
- **Issue:** Event listeners not properly removed
- **Steps to Reproduce:** Navigate app extensively
- **Expected:** Memory usage should remain stable
- **Actual:** Potential memory leaks from unremoved listeners

**BUG #36 - Global Variables Pollution**
- **Location:** JavaScript scope
- **Issue:** Large objects unnecessarily stored in global scope
- **Steps to Reproduce:** Check global window object
- **Expected:** Minimal global variable usage
- **Actual:** Cart, products, etc. in global scope

**BUG #37 - No Accessibility Features**
- **Location:** Entire application
- **Issue:** Missing ARIA labels, alt texts, keyboard navigation
- **Steps to Reproduce:** Use screen reader or keyboard only
- **Expected:** Should be accessible to all users
- **Actual:** Limited accessibility implementation

**BUG #38 - Inconsistent Error Messaging**
- **Location:** Throughout application
- **Issue:** Different error styles and messaging patterns
- **Steps to Reproduce:** Trigger various errors across features
- **Expected:** Consistent error presentation
- **Actual:** Varied error message formats and styles

---

### ⚡ **CATEGORY 6: API and Performance (5 bugs)**

**BUG #39 - Random API Failures**
- **Location:** simulateApiCall function
- **Issue:** 10% random failure rate not handled gracefully
- **Steps to Reproduce:** Submit forms multiple times
- **Expected:** Graceful error handling and retry logic
- **Actual:** Random failures without proper error handling

**BUG #40 - Inconsistent API Response Format**
- **Location:** API response handling
- **Issue:** Different endpoints return different response structures
- **Steps to Reproduce:** Check API simulation code
- **Expected:** Consistent response format across endpoints
- **Actual:** Mixed response formats (status vs success properties)

**BUG #41 - No Loading States**
- **Location:** Form submissions
- **Issue:** No visual indication during API calls
- **Steps to Reproduce:** Submit contact form
- **Expected:** Loading spinner or disabled button
- **Actual:** No feedback during processing

**BUG #42 - No Error Recovery**
- **Location:** API error handling
- **Issue:** Failed requests don't provide retry options
- **Steps to Reproduce:** Trigger API failure
- **Expected:** Option to retry failed requests
- **Actual:** Fails silently or shows generic error

**BUG #43 - No Input Sanitization**
- **Location:** Data processing
- **Issue:** User inputs not sanitized before processing
- **Steps to Reproduce:** Enter special characters in forms
- **Expected:** Input should be cleaned and validated
- **Actual:** No sanitization implemented

---

### 🔧 **CATEGORY 7: Edge Cases and Data Handling (4 bugs)**

**BUG #44 - Null Value Handling**
- **Location:** formatCurrency function
- **Issue:** Doesn't handle null/undefined values
- **Steps to Reproduce:** Pass null to formatCurrency function
- **Expected:** Should handle edge cases gracefully
- **Actual:** May throw errors with null values

**BUG #45 - Mobile Responsiveness Issues**
- **Location:** CSS media queries
- **Issue:** Some elements may not display correctly on mobile
- **Steps to Reproduce:** View on various screen sizes
- **Expected:** Responsive design across all devices
- **Actual:** Potential layout issues on smaller screens

**BUG #46 - Browser Compatibility**
- **Location:** JavaScript features
- **Issue:** Uses modern JS features that may not work in older browsers
- **Steps to Reproduce:** Test in older browser versions
- **Expected:** Graceful degradation or polyfills
- **Actual:** May fail in unsupported browsers

**BUG #47 - No Global Error Handling**
- **Location:** Application architecture
- **Issue:** No catch-all error handler for unexpected errors
- **Steps to Reproduce:** Cause JavaScript errors
- **Expected:** Graceful error recovery and user notification
- **Actual:** Errors may crash functionality silently

---

## Testing Exercises for You

### **Beginner Level Tests:**
1. Test search functionality with different inputs
2. Verify shopping cart calculations manually
3. Test contact form with various data combinations
4. Check login with different credential combinations

### **Intermediate Level Tests:**
1. Test cross-browser compatibility
2. Verify mobile responsiveness
3. Test with screen readers for accessibility
4. Performance testing with large data sets

### **Advanced Level Tests:**
1. Security testing (XSS, injection attempts)
2. API error simulation and handling
3. Memory leak detection
4. Load testing and stress testing

### **Automation Targets:**
- Search functionality tests
- Shopping cart calculation verification
- Form validation testing
- Login flow automation
- Mobile responsiveness checks

This test target provides realistic bug scenarios you'll encounter in professional QA work, from functional bugs to security issues, UX problems, and performance concerns.
