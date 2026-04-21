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
    # ---Case-1: Verifies the search field is visible. ---
    page = BugHuntShop2Page(driver)
    element = page.wait.until(
        EC.visibility_of_element_located(page.PROD_SEAR_FIELD_LOCATOR)
    )
    assert element.is_displayed()

def test_case_1_search_placeholder_text(driver):
    # ---Case-2: Verifies the placeholder text is displayed. ---
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

def test_case_27_products_aligned_in_a_row(driver):
    # ---Case-27: Verify {product} selections are aligned in a row on the display ---
    page = BugHuntShop2Page(driver)
    products = page.get_product_cards()
    y_positions = [p.location['y'] for p in products]
    assert max(y_positions) - min(y_positions) <= 5

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

@pytest.mark.xfail(reason="BHS2-4,5: Prices in the cart are not vertically aligned (Layout inconsistency).")
def test_cases_54_55_correct_vertical_alignment(driver):
    # ---Cases 54,55: Verify when products added to "Shopping Cart", prices are vertically aligned correctly. ---
    page = BugHuntShop2Page(driver)
    # ---Add 1-3 items (Case-54) or > 3 items (Case-55) ---
    page.click_gaming_laptop_from_products_box()
    page.click_tablet_from_products_box()
    prices = page.get_cart_item_price_elements()
    first_price_x = prices[0].location['x']
    for price in prices:
        actual_x = price.location['x']
        # --- This assertion will fail because of the staggered look on the page. ---
        assert actual_x == first_price_x, f"Price at {price.text} is at X:{actual_x}, expected X:{first_price_x}"

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
    element = page.wait.until(EC.presence_of_element_located(page.NAME_LOCATOR))
    assert element.is_displayed()

def test_case_66_name_field_in_focus(driver):
    # ---Case-66: Verify when clicking in the "Name" field, it is in focus and cursor appears. ---
    page = BugHuntShop2Page(driver)
    element = page.wait.until(EC.element_to_be_clickable(page.NAME_LOCATOR))
    element.click()
    active_element = driver.switch_to.active_element
    assert active_element.get_attribute("id") == "name", "Focus failed: Name field is not the active element."

def test_case_67_name_field_out_of_focus(driver):
    # ---Case-67: Verify when clicking outside the "name" field, it comes out of focus
    # ---and cursor disappears from field. ---
    page = BugHuntShop2Page(driver)
    element = page.wait.until(EC.element_to_be_clickable(page.NAME_LOCATOR))
    element.click()
    send_message_button = page.wait.until(EC.element_to_be_clickable(page.SEND_MESSAGE_BUTTON_LOCATOR))
    assert send_message_button.get_attribute("id") != "name", "Case-67 Fail: Name field should not be in focus."

