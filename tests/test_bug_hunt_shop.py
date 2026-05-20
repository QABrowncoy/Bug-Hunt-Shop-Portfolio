import pytest
from pages import BugHuntShop2Page
import data
from selenium.webdriver.support import expected_conditions as EC


def test_launch_app(driver):
    # ---Verifies the app opens and has the correct title. ---
    assert "Bug Hunt" in driver.title

def test_search_results_field_initially_empty(driver):
    # ---Verifies that the search results field is empty on page load. ---
    page = BugHuntShop2Page(driver)
    results_box = driver.find_element(*page.SEARCH_RESULTS_BOX_LOCATOR)
    assert results_box.text.strip() == "", "Error: Search results field should be empty at launch."


# ---"Product Search" search cases ---

def test_case_0_search_field_visible(driver):
    # ---Case-0: Verifies the search field is visible. ---
    page = BugHuntShop2Page(driver)
    element = page.wait.until(
        EC.visibility_of_element_located(page.PROD_SEAR_FIELD_LOCATOR)
    )
    assert element.is_displayed()

def test_case_1_search_placeholder_text(driver):
    # ---Case-1: Verifies the placeholder text is displayed. ---
    page = BugHuntShop2Page(driver)
    element = page.wait.until(
        EC.visibility_of_element_located(page.PROD_SEAR_FIELD_LOCATOR)
    )
    assert element.get_attribute("placeholder") == "Search for products..."

def test_case_4_search_button_visible(driver):
    # ---Case-4: Verifies the search button is visible. ---
    page = BugHuntShop2Page(driver)
    element = page.wait.until(
        EC.visibility_of_element_located(page.SEARCH_BUTTON_LOCATOR)
    )
    assert element.is_displayed()

def test_case_5_search_button_clickable(driver):
    # ---Case-5: Verifies the search button is clickable. ---
    page = BugHuntShop2Page(driver)
    element = page.wait.until(
        EC.element_to_be_clickable(page.SEARCH_BUTTON_LOCATOR)
    )
    assert element.is_enabled()

def test_case_6_empty_search_shows_error(driver):
    # ---Case-6: Verifies clicking Search button while field is empty displays error message. ---
    page = BugHuntShop2Page(driver)
    page.click_search_button()
    assert page.get_search_error() != ""

# --- Valid character group (Cases 7,8,11,12,13,14,17) ---
@pytest.mark.parametrize("term, case_id", [
    (data.SEARCH_VALID_LATIN,            "Case-7"),   # Latin characters
    (data.SEARCH_VALID_DASH,             "Case-8"),   # Dashes/Hyphens
    (data.SEARCH_VALID_APOSTROPHE,       "Case-11"),  # Apostrophes
    (data.SEARCH_VALID_SPACE,            "Case-12"),  # Spaces in between
    (data.SEARCH_VALID_SPACE_BEFORE,     "Case-13"),  # Spaces before
    (data.SEARCH_VALID_SPACE_AFTER,      "Case-14"),  # Spaces after
    (data.SEARCH_VALID_NUMBERS,          "Case-17"),  # Numbers
])
def test_case_allows_valid_characters(driver, term, case_id):
    page = BugHuntShop2Page(driver)
    page.enter_product_search(term)
    page.click_search_button()
    assert page.get_search_error() == ""

# --- Invalid character group (Cases 9,10,15,16,18,19,20) ---
@pytest.mark.parametrize("term, case_id", [
    (data.SEARCH_INVALID_PERIOD,         "Case-9"),    #Periods
    (data.SEARCH_INVALID_COMMA,          "Case-10"),   #Commas
    (data.SEARCH_INVALID_NON_LATIN,      "Case-15"),   #Non-Latin characters
    (data.SEARCH_INVALID_UNICODE,        "Case-16"),   #Unicode characters
    (data.SEARCH_INVALID_HTML,           "Case-18"),   #HTML tags
    (data.SEARCH_INVALID_SPECIAL_CHARS,  "Case-19"),   #Special characters
    (data.SEARCH_INVALID_EMPTY,          "Case-20"),   #Nothing/Whitespace
])
def test_cases_rejects_invalid_characters(driver, term, case_id):
    page = BugHuntShop2Page(driver)
    page.enter_product_search(term)
    page.click_search_button()
    assert page.get_search_error() != ""

def test_case_21_invalid_search_shows_not_found_message(driver):
    # ---Case-21: Verify invalid input displays "No products found for {invalid input}." message. ---
    # --- and product grid is empty. ---
    page = BugHuntShop2Page(driver)
    search_term = "camera"
    page.enter_product_search(search_term)
    page.click_search_button()
    results = page.driver.find_element(*page.SEARCH_RESULTS_BOX_LOCATOR)
    assert "No products found" in results.text
    assert f'"{search_term}"' in results.text
    search_cards = page.get_search_result_cards()
    assert len(search_cards) == 0, f"Expected 0 search results, but found {len(search_cards)}"

# --- Boundary value group (Cases 23,24,25) ---
@pytest.mark.parametrize("term, case_id", [
    (data.SEARCH_BOUNDARY_1_CHAR,     "Case-23"),
    (data.SEARCH_BOUNDARY_2_CHAR,     "Case-23"),
    (data.SEARCH_BOUNDARY_3_CHAR,     "Case-24"),
    (data.SEARCH_BOUNDARY_14_CHAR,    "Case-24"),
    (data.SEARCH_BOUNDARY_97_CHAR,    "Case-24"),
])
def test_search_boundary_values(driver, term, case_id):
    # --- Cases 23,24,25: Verify boundary values in Products Search field ---
    page = BugHuntShop2Page(driver)
    page.enter_product_search(term)
    page.click_search_button()
    if case_id == "Case-24":
        # Valid length - no error expected
        assert page.get_search_error() == ""
    elif case_id == "Case-23":
        # Invalid length - error expected
        assert page.get_search_error() != ""
    else:
        raise ValueError(f"Unexpected case_id: {case_id}")

@pytest.mark.xfail(reason="BHS2-17: Field silently caps at 100 characters, no error shown")
def test_case_25_over_limit_shows_error(driver):
    # ---Case-25: Verify input over 100 characters is rejected with an error message ---
    page = BugHuntShop2Page(driver)
    page.enter_product_search(data.SEARCH_BOUNDARY_101_CHAR)
    page.click_search_button()
    assert page.get_search_error() != ""

# ---Our Products & Shopping Cart Test Cases ---

@pytest.mark.xfail(reason="BHS2-1: Only 3 of 5 products are displayed in product grid.")
def test_case_26_all_products_present(driver):
    # ---Case-26: Verify all {product} selections are present in design ---
    page = BugHuntShop2Page(driver)
    assert len(page.get_product_cards()) == 5

def test_case_28_products_spelling_is_correct(driver):
    # ---Case-28: Verify product's spelling is correct on display ---
    page = BugHuntShop2Page(driver)
    names = page.get_product_names()
    assert "Gaming Laptop" in names
    assert "Smartphone" in names
    assert "Tablet" in names

def test_case_29_product_prices_correct(driver):
    # ---Case-29: Verify price of {product} is correct by requirements ---
    page = BugHuntShop2Page(driver)
    prices = page.get_product_prices()
    assert "$999.99" in prices
    assert "$599.99" in prices
    assert "$299.99" in prices

def test_case_30_subtotal_empty_cart(driver):
    # ---Case-30: Verify "Subtotal" displays "0.00" when "Shopping Cart" is empty ---
    page = BugHuntShop2Page(driver)
    subtotal = page.driver.find_element(*page.SUBTOTAL_SUM_LOCATOR).text.strip()
    assert subtotal == "0.00"

@pytest.mark.xfail(reason="BHS2-18: Tax calculated as subtotal + 0.085 instead of subtotal * 0.085")
def test_case_31_tax_correct_empty_cart(driver):
    # ---Case-31: Verify "Tax" percentage is correct by requirements ---
    page = BugHuntShop2Page(driver)
    page.click_gaming_laptop_from_products_box()
    subtotal = float(page.driver.find_element(*page.SUBTOTAL_SUM_LOCATOR).text.strip())
    expected_tax = round(subtotal * 0.085, 2)
    actual_tax = float(page.driver.find_element(*page.TAX_SUM_LOCATOR).text.strip())
    assert actual_tax == expected_tax

def test_case_32_shipping_cost_correct(driver):
    # ---Case-32: Verify "Shipping" shows $5.99" ---
    page = BugHuntShop2Page(driver)
    shipping = page.driver.find_element(*page.SHIPPING_TOTAL_LOCATOR).text.strip()
    assert shipping == "5.99"

@pytest.mark.xfail(reason="BHS2-19: Total should reflect $0.00 subtotal + $0.00 tax + $5.99 shipping only after a product is added")
def test_case_33_zero_total_with_no_product(driver):
    # ---Case-33: Verify  "Total" is "0.00" with no {product} is added. ---
    page = BugHuntShop2Page(driver)
    total = page.driver.find_element(*page.FULL_TOTAL_LOCATOR).text.strip()
    assert total == "0.00"

def test_case_34_prod_can_be_added_to_cart(driver):
    # ---Case-34: Verify a clickable {product} can be added to the "Shopping Cart". ---
    page = BugHuntShop2Page(driver)
    page.click_gaming_laptop_from_products_box()
    assert page.get_cart_item_count() == 1

@pytest.mark.parametrize("products, case_id", [
    (data.CART_BOUNDARY_0_PRODUCTS, "Case-35"),
    (data.CART_BOUNDARY_1_PRODUCT,  "Case-36"),
    (data.CART_BOUNDARY_2_PRODUCTS, "Case-36"),
    (data.CART_BOUNDARY_3_PRODUCTS, "Case-36"),
    (data.CART_BOUNDARY_7_PRODUCTS, "Case-37"),
])
def test_cases_35_36_37_products_boundary_values(driver, products, case_id):
    page = BugHuntShop2Page(driver)
    for p in range(products):
        page.click_gaming_laptop_from_products_box()
    assert page.get_cart_item_count() == products

def test_case_38_product_added_message_appears(driver):
    # ---Case-38: Verify when {product} is added to "Cart", the message "{product} is added to cart!" appears. ---
    page = BugHuntShop2Page(driver)
    page.click_tablet_from_products_box()
    notification = page.get_add_to_cart_notification("Tablet")
    assert notification.is_displayed()

def test_case_39_prod_displayed_in_cart(driver):
    # ---Case-39: Verify {product} is displayed in "Shopping Cart". ---
    page = BugHuntShop2Page(driver)
    page.click_gaming_laptop_from_products_box()
    assert "Gaming Laptop" in page.get_cart_item_names()

def test_case_40_prod_price_displayed_correctly(driver):
    # ---Case-40: Verify price of {product} displays to the right in the same row. ---
    page = BugHuntShop2Page(driver)
    page.click_gaming_laptop_from_products_box()
    page.click_smartphone_from_products_box()
    page.click_tablet_from_products_box()
    prices = page.get_cart_item_prices()
    assert "$999.99" in prices
    assert "$599.99" in prices
    assert "$299.99" in prices

def test_case_41_subtotal_displayed_correctly(driver):
    # ---Case-41: Verify "Subtotal" shows base price of product. ---
    page = BugHuntShop2Page(driver)
    page.click_tablet_from_products_box()
    subtotal = page.driver.find_element(*page.SUBTOTAL_SUM_LOCATOR).text.strip()
    assert subtotal == "299.99"

@pytest.mark.xfail(reason="BHS2-18: Tax calculated as subtotal + 0.085 instead of subtotal * 0.085")
def test_case_42_sum_of_subtotal_and_tax_correct(driver):
    # ---Case-42: Verify SUM of "Subtotal" and "Tax" is correct. ---
    page = BugHuntShop2Page(driver)
    page.click_smartphone_from_products_box()
    subtotal = page.get_subtotal()
    actual_tax = round(page.get_tax(), 2)
    expected_sum = round(subtotal + round(subtotal * 0.085, 2), 2)
    actual_sum = round(subtotal + actual_tax, 2)
    assert actual_sum == expected_sum

@pytest.mark.xfail(reason="BHS2-18: Total is incorrect due to tax bug(subtotal + 0.085 instead of subtotal * 0.085)")
def test_case_43_sum_of_subtotal_tax_and_shipping_correct(driver):
    # ---Case-43: Verify SUM of "Subtotal", "Tax", and "Shipping" is correct. ---
    page = BugHuntShop2Page(driver)
    page.click_gaming_laptop_from_products_box()
    subtotal = page.get_subtotal()
    actual_tax = round(page.get_tax(), 2)
    shipping = round(page.get_shipping(), 2)
    expected_total = round(subtotal + round(subtotal * 0.085, 2) + shipping, 2)
    actual_total = round(subtotal + actual_tax + shipping, 2)
    assert actual_total == expected_total

def test_case_44_shopping_cart_initial_state_no_message(driver):
    # ---Case-44: Verify "Shopping Cart" shows no message before {product} is added. ---
    page = BugHuntShop2Page(driver)
    assert page.get_cart_message() == ""

def test_case_45_clear_cart_button_present(driver):
    # ---Case-45: Verify "Clear Cart" button is clear and visible. ---
    page = BugHuntShop2Page(driver)
    element = page.wait.until(EC.visibility_of_element_located(page.CLEAR_CART_BUTTON_LOCATOR))
    assert element.is_displayed()

def test_case_46_clear_cart_button_clickable(driver):
    # ---Case-46: Verify "Clear Cart" button is clickable. ---
    page = BugHuntShop2Page(driver)
    element = page.wait.until(EC.element_to_be_clickable(page.CLEAR_CART_BUTTON_LOCATOR))
    assert element.is_enabled()

# ---Cases (47,48): Both messages appear at the same time. ---
def test_case_47_cart_is_empty_message(driver):
    # ---Case-47: Verify "Shopping Cart" displays message "Your cart is empty" when {product} added and "Clear Cart" button clicked. ---
    page = BugHuntShop2Page(driver)
    page.click_gaming_laptop_from_products_box()
    page.click_clear_cart_button()
    assert page.get_cart_message() == "Your cart is empty"

def test_case_48_cart_cleared_message(driver):
    # ---Case-48: Verify "Cart cleared" message appears when {product} is in "Shopping Cart" and "Clear Cart" button is clicked. ---
    page = BugHuntShop2Page(driver)
    page.enter_product_search("Wireless Headphones")
    page.click_search_button()
    page.sear_results_added("Wireless Headphones")
    page.click_clear_cart_button()
    notification = page.get_cart_cleared_notification()
    assert notification.is_displayed()

# ---Remove Button Boundary Values: (Cases 49,50,51) ---
@pytest.mark.parametrize("products, case_id",[
    (data.CART_BOUNDARY_0_PRODUCTS,   "Case-49"), # - Remove button absent
    (data.CART_BOUNDARY_1_PRODUCT,    "Case-50"), # - Remove button present
    (data.CART_BOUNDARY_2_PRODUCTS,   "Case-50"), # - Remove button present
    (data.CART_BOUNDARY_3_PRODUCTS,   "Case-51"), # - Remove button present
    (data.CART_BOUNDARY_4_PRODUCTS,   "Case-51"), # - Remove button present
    (data.CART_BOUNDARY_5_PRODUCTS,   "Case-51"), # - Remove button present
])
def test_cases_49_50_51_remove_button_boundary_values(driver, products, case_id):
    # ---Cases 49,50,51: Verify remove button appears with or without products. ---
    page = BugHuntShop2Page(driver)
    for i in range(products):
        if i == 0:
            page.click_tablet_from_products_box()
        elif i == 1:
            page.click_gaming_laptop_from_products_box()
        elif i >= 2:
            page.click_smartphone_from_products_box()
        else:
            raise ValueError(f"Unexpected product index: {i} for {products}) total product")

    remove_buttons = page.get_remove_buttons()

    if case_id == "Case-49":
        # - Remove button does not appear ---
        assert len(remove_buttons) == 0, f"Expected 0 remove buttons, but found {len(remove_buttons)}"
    elif case_id in ("Case-50", "Case-51"):
        # - Remove button appears for all products ---
        assert len(remove_buttons) == products, f"Expected {products} remove buttons, but found {len(remove_buttons)}"

def test_case_52_remove_button_removes_prod(driver):
    # ---Case-52: Verify clicking "Remove" button removes a {product}. ---
    page = BugHuntShop2Page(driver)
    page.click_smartphone_from_products_box()
    assert page.get_cart_item_count() == 1
    page.shop_cart_result_cleared("Smartphone")
    assert page.get_cart_item_count() == 0

def test_case_53_no_price_when_cart_is_empty(driver):
    # ---Case-53: Verify when < 1 product is in "Shopping Cart", no price is displayed. ---
    page = BugHuntShop2Page(driver)
    page.click_clear_cart_button()
    assert page.get_cart_item_count() == 0
    assert page.get_subtotal() == 0.00

# ---Subtotal Correct Boundary Values: (Cases 56,57,58) ---
@pytest.mark.parametrize("products, case_id", [
    (data.CART_BOUNDARY_0_PRODUCTS, "Case-56"),
    (data.CART_BOUNDARY_2_PRODUCTS, "Case-57"),
    (data.CART_BOUNDARY_3_PRODUCTS, "Case-57"),
    (data.CART_BOUNDARY_6_PRODUCTS, "Case-58"),
    (data.CART_BOUNDARY_7_PRODUCTS, "Case-58"),
    (data.CART_BOUNDARY_8_PRODUCTS, "Case-58"),
])
def test_cases_56_57_58_correct_subtotal(driver, products, case_id):
    # ---Cases 56,57,58: Verify when product added to "Shopping Cart" or not, "Subtotal" is correct. ---
    page = BugHuntShop2Page(driver)
    page.click_clear_cart_button()
    for p in range(products):
        if p == 0:
            page.click_smartphone_from_products_box()
        elif p == 1:
            page.click_gaming_laptop_from_products_box()
        else:
            page.click_tablet_from_products_box()

    expected_val = 0.0
    if products >= 1:expected_val += 599.99
    if products >= 2:expected_val += 999.99
    if products > 2: expected_val += (products - 2) * 299.99

    expected_val = round(expected_val, 2)

    actual_subtotal = page.get_subtotal()
    assert actual_subtotal == expected_val, (
        f"Failed {case_id}: Expected subtotal to be ${expected_val}, "
        f"but the UI displayed ${actual_subtotal}."
    )

def test_case_59_no_product_and_tax_sum(driver):
    # ---Case-59: Verify the SUM of < 1 products and "Tax" is correct. ---
    page = BugHuntShop2Page(driver)
    subtotal = page.get_subtotal()
    tax = page.get_tax()
    assert round(subtotal + tax, 2) == 0.00

@pytest.mark.xfail(reason="BHS2-19: Shipping/Total does not reset to 0.00 on empty cart.")
def test_case_62_grand_total_with_no_product(driver):
    # ---Case-62: Verify with < 1 product, "Total" equals correct SUM of "Subtotal", "Tax", & "Shipping". ---
    page = BugHuntShop2Page(driver)
    actual_ui_total = page.get_total()
    assert actual_ui_total == 0.00, f"Expected 0.00, but UI showed {actual_ui_total}."

# Interview Talking Points:
# I marked this entire suite as XFAIL because the math logic was fundamentally broken.
# There were only two specific cases where the bug didn't manifest, so
# grouping it all as failures made sense when tracking regression.
@pytest.mark.xfail(reason="BHS2-6, BHS2-7, BHS2-18: Known math logic and total calculations bugs.")
@pytest.mark.parametrize("products, case_id", [
    (data.CART_BOUNDARY_1_PRODUCT,  "Case-60"),
    (data.CART_BOUNDARY_1_PRODUCT,  "Case-63"),
    (data.CART_BOUNDARY_2_PRODUCTS, "Case-60"),
    (data.CART_BOUNDARY_2_PRODUCTS, "Case-63"),
    (data.CART_BOUNDARY_3_PRODUCTS, "Case-64"),
    (data.CART_BOUNDARY_4_PRODUCTS, "Case-61"),
    (data.CART_BOUNDARY_4_PRODUCTS, "Case-64"),
    (data.CART_BOUNDARY_5_PRODUCTS, "Case-61"),
    (data.CART_BOUNDARY_5_PRODUCTS, "Case-64"),
    (data.CART_BOUNDARY_6_PRODUCTS, "Case-61"),
])

def test_cases_60_61_63_64_cart_financial_congruency(driver, products, case_id):
    # ---Cases 60,61,63,64:
    # Verifies subtotal, tax, shipping logic and grand total against all identified boundaries.
    # Maps Specifically to Jira bugs BHS2-6, 7, 18, 19.
    page = BugHuntShop2Page(driver)
    page.click_clear_cart_button()

    # Add products based on parametrization
    for p in range(products):
        if p == 0:
            page.click_gaming_laptop_from_products_box()
        elif p == 1:
            page.click_tablet_from_products_box()
        else:
            page.click_smartphone_from_products_box()

    # Expected Math Logic
    expected_subtotal = 0.0
    if products >= 1: expected_subtotal += 999.99
    if products >= 2: expected_subtotal += 299.99
    if products > 2:  expected_subtotal += (products - 2) * 599.99
    expected_subtotal = round(expected_subtotal, 2)

    # Business Rules: 8.5% Tax, $5.99 Shipping
    tax_rate = 0.085
    shipping_rate = 5.99 if products > 0 else 0.0

    expected_tax = round(expected_subtotal * tax_rate, 2)
    expected_total = round(expected_subtotal + expected_tax + shipping_rate, 2)

    # Capture Actual UI Values
    actual_subtotal = page.get_subtotal()
    actual_total = page.get_total()

    # Assertions
    # Note: If math bugs exist in the UI, these will trigger the XFAIL
    assert actual_subtotal == expected_subtotal, f"{case_id}: Subtotal mismatch"
    assert actual_total == expected_total, f"{case_id}: Grand Total mismatch"

    # In case you get "XPASS" instead of "XFAIL"
    # How to Investigate: The "Loud" Test
    # To see exactly why it is passing, we need to see the numbers.
    # Run the test again with the -s flag in your PyCharm terminal. This allows the print statements to show up in the console.
    #
    # Add this line right before your assertions:
    # print(f"\nDEBUG {case_id}: Products: {products} | Expected Total: {expected_total} | Actual UI Total: {actual_total}")
    # Then run this in your terminal:
    # pytest tests/test_bug_hunt_shop.py::test_cases_59_60_61_cart_financial_congruency -s

def test_case_65_name_field_visible(driver):
    # ---Case-65: Verify "Name" field is visible and displayed correctly. ---
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    assert page.is_name_field_visible()

def test_case_66_name_field_in_focus(driver):
    # ---Case-66: Verify when clicking in the "Name" field, it is in focus and cursor appears. ---
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.focus_name_field()
    assert page.get_active_element_id()

def test_case_67_name_field_out_of_focus(driver):
    # ---Case-67: Verify when clicking outside the "name" field, it comes out of focus
    # ---and cursor disappears from field. ---
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.focus_name_field()
    page.click_send_message_button()
    assert page.get_active_element_id() != "name"

@pytest.mark.xfail(reason="BHS2-22: Name field is required in HTML but validation fails to trigger.")
def test_case_68_no_input_in_fields_result_error_message(driver):
    # ---Case-68: Verify when all fields empty, and "Send Message" button is pressed, ---
    # --- the message "Please fill out this field" appears. ---
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.click_send_message_button()

    # 1. Check Browser Validation (This part will PASS)
    browser_msg = page.get_browser_validation_message("name")
    assert "please fill out this field" in browser_msg.lower()

    # 2. Check Custom JS Validation (This part is where BUG #16 likely fails)
    # Your JS should create a <div class="error-message">Name is required</div>
    js_errors = page.get_contact_validation_errors()
    assert "Name is required" in js_errors, "BHS2-22: HTML5 worked, but custom js error div is missing!"

# --- To use as a tool, if this were bug free, this is how it would look... ---
# def test_case_68_all_fields_empty_validation(driver):
#   page = BugHuntShop2Page(driver)
#   page.scroll_to_contact_and_verify_empty()
#   page.click_send_message()

#   # Standard Master List of what we are supposed to see
#   expected_errors = {
#        "name": "Name is required",
#        "email": "Email is required",
#        "phone": "Phone is required"
#   }
#   for field_id, expected_text in expected_errors.items():
#       # Check browser layer (Custom JS)
#       browser_validation_message = page.get_browser_validation_message(field_id)
#       assert "fill out" in browser_validation_message
#
#       # Check App Layer (Custom JS)
#       actual_js_errors = page.contact_validation_errors()
#       assert expected_errors in actual_js_errors

@pytest.mark.xfail(
    reason="BHS2-24: Custom JS validation messages are suppressed by native browser tooltips across all Contact fields.")
@pytest.mark.parametrize("missing_field, case_id, name, email, phone, msg", [
    # missing_field |   case_id  |   name   |           email           |     phone     |         msg
    ("name",         "Case-69",    "",          "tester@bug-hunt.com",   "2145551234",    "Validating missing name"),
    ("email",        "Case-89",    "John Doe",  "",                      "2145551234",    "Validating missing email"),

    pytest.param("phone", "Case-118", "John Doe", "tester@bug-hunt.com", "", "Validating missing phone",
                 marks=pytest.mark.xfail(reason="Requirement Bug: Phone field missing 'required' attribute")),
    ("message",      "Case-141",   "John Doe",  "tester@bug-hunt.com",   "2145551234",    "")
])
def test_contact_field_isolation_validation(driver, missing_field, case_id, name, email, phone, msg):
    """Consolidated test for Case-69, 89, 117, and 140.
    Verifies that leaving one field empty while others are valid still triggers validation.
    """
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()

    # Fill out fields using the provided parameters
    # If a parameter is an empty string, the field remains empty
    if name: page.cont_us_name(name)
    if email: page.cont_us_email(email)
    if phone: page.cont_us_phone(phone)
    if msg: page.cont_us_message(msg)

    page.click_send_message_button()

    # 1. Verify Browser Safety Net (Native HTML5 Tooltip)
    # This proves the 'required' attribute is working at the browser level
    browser_msg = page.get_browser_validation_message(missing_field)
    expected_tooltip = "please fill out this field"
    assert expected_tooltip in browser_msg.lower(), f"{case_id}: Browser tooltip missing or incorrect for {missing_field}"

    # 2. Verify Custom JS Bug (The XFAIL part)
    # We check if the custom error <div> exists in the DOM
    js_errors = page.get_contact_validation_errors()
    expected_error_text = f"{missing_field.capitalize()} is required"

    # This assertion is expected to fail until the JS logic is fixed
    assert expected_error_text in js_errors, f"{case_id}: Custom JS error div missing for {missing_field}!"

# --- Valid character group (Cases 70,71,74,75(a,b,c)) ---
@pytest.mark.parametrize("term, case_id", [
    (data.VALID_NAME_LATIN,            "Case-70"),
    (data.VALID_NAME_DASH,             "Case-71"),
    (data.VALID_NAME_APOSTROPHE,       "Case-74"),
    (data.VALID_NAME_SPACE_BETWEEN,    "Case-75a"),
    (data.VALID_NAME_SPACE_BEFORE,     "Case-75b"),
    (data.VALID_NAME_SPACE_AFTER,      "Case-75c"),
])

def test_name_field_valid_characters(driver, term, case_id):
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.cont_us_name(term)
    page.click_send_message_button()
    assert page.get_name_error() == ""

# ---Invalid character group (Cases 72,73,76-81) ---
@pytest.mark.parametrize("term, case_id", [
    (data.INVALID_NAME_PERIOD,         "Case-72"),
    (data.INVALID_NAME_COMMA,          "Case-73"),
    (data.INVALID_NAME_NON_LATIN,      "Case-76"),
    (data.INVALID_NAME_UNICODE,        "Case-77"),
    (data.INVALID_NAME_NUMBERS,        "Case-78"),
    (data.INVALID_NAME_NUMBERS_MIX,    "Case-79"),
    (data.INVALID_NAME_HTML,           "Case-80"),
    (data.INVALID_NAME_SPECIAL,        "Case-81"),
    (data.INVALID_NAME_EMPTY,          "Case-82"),
])

def test_name_field_invalid_characters(driver, term, case_id):
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.cont_us_name(term)
    page.click_send_message_button()

    # Logic to handle both custom JS errors and Browser Native validation
    if case_id == "Case-82":
        # No 'By' here! We just ask the page object if the field is valid.
        assert page.is_field_valid("name") is False
    else:
        # Using your existing getter
        assert page.get_name_error() != ""

# --- Boundary value group (Cases 83,84,85) ---
@pytest.mark.parametrize("term, case_id", [
    (data.VALID_NAME_8_CHAR,             "Case-84"),
    (data.VALID_NAME_40_CHAR,            "Case-84"),
    (data.VALID_NAME_73_CHAR,            "Case-84"),
    (data.INVALID_NAME_1_CHAR,           "Case-83"),
    (data.INVALID_NAME_101_CHAR,         "Case-85"),
    (data.INVALID_NAME_102_CHAR,         "Case-85"),
])

def test_name_field_boundary_values(driver, term, case_id):
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.cont_us_name(term)
    page.click_send_message_button()
    if case_id == "Case-84":
        assert page.get_name_error() == ""
    elif case_id in ["Case-83", "Case-85"]:
        assert page.get_name_error() != ""
    else:
        raise ValueError(f"Case ID {case_id} not recognized in boundary logic")

def test_case_86_email_field_visible(driver):
    # ---Case-86: Verify "Email" field is visible and displayed correctly. ---
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    assert page.is_email_field_visible()


def test_case_87_email_field_in_focus(driver):
    # ---Case-87: Verify when clicking in the "Email" field, it is in focus and cursor appears. ---
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.focus_email_field()
    assert page.get_active_element_id()


def test_case_88_email_field_out_of_focus(driver):
    # ---Case-88: Verify when clicking outside the "email" field, it comes out of focus
    # ---and cursor disappears from field. ---
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.focus_email_field()
    page.click_send_message_button()
    assert page.get_active_element_id() != "email"

# ---Valid char group for 'local part' of email (Cases 90-95,98,100,101,103,104) ---
@pytest.mark.parametrize("term, case_id", [
    (data.VALID_EMAIL_LATIN,            "Case-90"),
    (data.VALID_EMAIL_DASH,             "Case-91"),
    (data.VALID_EMAIL_PERIOD,           "Case-92"),
    (data.VALID_EMAIL_COMMA,            "Case-93"),
    (data.VALID_EMAIL_APOSTROPHE,       "Case-94"),
    (data.VALID_EMAIL_SPACE_BEFORE,     "Case-95"),
    (data.VALID_EMAIL_PLUS_TAG_LATIN,   "Case-98"),
    (data.VALID_EMAIL_UNICODE,          "Case-100"),
    (data.VALID_EMAIL_NUMBERS,          "Case-101"),
    (data.VALID_EMAIL_SPECIAL,          "Case-103"),
    (data.VALID_EMAIL_SPECIAL_MIX,      "Case-104"),
])

def test_email_field_valid_characters(driver, term, case_id):
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.cont_us_email(term)
    page.click_send_message_button()
    assert page.get_email_error() == ""


# ---Invalid char group for 'local part' of email (Cases 96,97,99,102,105-108) ---
@pytest.mark.parametrize("term, case_id", [
    (data.INVALID_EMAIL_SPACE_BETWEEN,   "Case-96"),
    (data.INVALID_EMAIL_SPACE_AFTER,     "Case-97"),
    (data.INVALID_EMAIL_NON_LATIN,       "Case-99"),
    (data.INVALID_EMAIL_HTML,            "Case-102"),
    (data.INVALID_EMAIL_NO_LOCAL_NAME,   "Case-105"),
    (data.INVALID_EMAIL_NO_AT,           "Case-106"),
    (data.INVALID_EMAIL_DOUBLE_AT,       "Case-107"),
    (data.INVALID_EMAIL_NO_DOMAIN,       "Case-108"),
])

def test_email_field_invalid_characters(driver, term, case_id):
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.cont_us_email(term)
    page.click_send_message_button()
    assert page.get_email_error() != ""

# ---Boundary value group (Cases 109,110,111) ---
@pytest.mark.parametrize("term, case_id", [
    (data.VALID_EMAIL_8_CHAR,          "Case-110"),
    (data.VALID_EMAIL_121_CHAR,        "Case-110"),
    (data.VALID_EMAIL_254_CHAR,        "Case-110"),
    pytest.param(data.INVALID_EMAIL_0_CHAR,  "Case-109",
                 marks=pytest.mark.xfail(reason="BHS2-25: Browser tooltip blocks custom JS error for empty field.")),
    (data.INVALID_EMAIL_255_CHAR,      "Case-111"),
    (data.INVALID_EMAIL_256_CHAR,      "Case-111"),
    (data.INVALID_EMAIL_257_CHAR,      "Case-111"),
])

def test_email_local_boundary_values(driver, term, case_id):
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.cont_us_email(term)
    page.click_send_message_button()
    if case_id == "Case-110":
        assert page.get_email_error() == ""
    elif case_id in ["Case-109", "Case-111"]:
        assert page.get_email_error() != ""
    else:
        raise ValueError(f"Case ID {case_id} not recognized in boundary logic")

def test_case_112_invalid_email_error(driver):
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.cont_us_email("@gmail.com")
    page.click_send_message_button()
    assert page.get_email_error() == "Please enter a valid email address (example@domain.com)"

def test_case_113_browser_tooltip_with_multiple_button_press(driver):
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.cont_us_email("@gmail.com")
    page.click_send_message_button()
    page.click_send_message_button()
    expected_error_msg = "Please enter a valid email address (example@domain.com)"

    browser_validation_message = page.get_browser_validation_message("email")
    assert "Please enter a part followed by '@'" in browser_validation_message
    actual_js_error = page.get_contact_validation_errors()
    assert expected_error_msg in actual_js_error

def test_case_114_phone_field_visible(driver):
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    assert page.is_phone_field_visible()

def test_case_115_phone_field_in_focus(driver):
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.focus_phone_field()
    assert page.get_active_element_id() == "phone"

def test_case_116_phone_field_out_of_focus(driver):
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.focus_phone_field()
    assert page.get_active_element_id() == "phone"
    page.click_send_message_button()
    assert page.get_active_element_id() != "phone"

def test_case_118_phone_field_extra_error_message(driver):
    page = BugHuntShop2Page(driver)
    page.scroll_to_contact_and_verify_empty()
    page.cont_us_name("name")
    page.cont_us_email("AnaMarie@gmail.com")
    page.cont_us_message("message")
    page.click_send_message_button()
    assert page.get_phone_error() != ""
    assert page.get_phone_error_2() != ""







