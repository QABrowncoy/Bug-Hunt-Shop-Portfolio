import pytest
from pages import BugHuntShop2Page
import data
from selenium.webdriver.support import expected_conditions as EC


def test_launch_app(driver):
    """Verifies the app opens and has the correct title."""
    assert "Bug Hunt" in driver.title

# ---"Product Search" search cases ---

def test_case_1_search_field_visible(driver):
    """Case-1: Verifies the search field is visible."""
    page = BugHuntShop2Page(driver)
    element = page.wait.until(
        EC.visibility_of_element_located(page.PROD_SEAR_FIELD_LOCATOR)
    )
    assert element.is_displayed()

def test_case_2_search_placeholder_text(driver):
    """Case-2: Verifies the placeholder text is displayed."""
    page = BugHuntShop2Page(driver)
    element = page.wait.until(
        EC.visibility_of_element_located(page.PROD_SEAR_FIELD_LOCATOR)
    )
    assert element.get_attribute("placeholder") == "Search for products..."

def test_case_5_search_button_visible(driver):
    """Case-5: Verifies the search button is visible."""
    page = BugHuntShop2Page(driver)
    element = page.wait.until(
        EC.visibility_of_element_located(page.SEARCH_BUTTON_LOCATOR)
    )
    assert element.is_displayed()

def test_case_6_search_button_clickable(driver):
    """Case-6: Verifies the search button is clickable."""
    page = BugHuntShop2Page(driver)
    element = page.wait.until(
        EC.element_to_be_clickable(page.SEARCH_BUTTON_LOCATOR)
    )
    assert element.is_enabled()

def test_case_7_empty_search_shows_error(driver):
    """Case-7: Verifies clicking Search button while field is empty displays error message."""
    page = BugHuntShop2Page(driver)
    page.click_search_button()
    assert page.get_search_error() != ""

# --- Valid character group (Cases 8,9,12,15,16,17,20) ---
@pytest.mark.parametrize("term, case_id", [
    (data.SEARCH_VALID_LATIN,            "Case-8"),   # Latin characters
    (data.SEARCH_VALID_DASH,             "Case-9"),   # Dashes/Hyphens
    (data.SEARCH_VALID_APOSTROPHE,       "Case-12"),  # Apostrophes
    (data.SEARCH_VALID_SPACE,            "Case-15"),  # Spaces in between
    (data.SEARCH_VALID_SPACE_BEFORE,     "Case-16"),  # Spaces before
    (data.SEARCH_VALID_SPACE_AFTER,      "Case-17"),  # Spaces after
    (data.SEARCH_VALID_NUMBERS,          "Case-20"),  # Numbers
])
def test_case_allows_valid_characters(driver, term, case_id):
    page = BugHuntShop2Page(driver)
    page.enter_product_search(term)
    page.click_search_button()
    assert page.get_search_error() == ""

# --- Invalid character group (Cases 10,11,18,19,21,22,23) ---
@pytest.mark.parametrize("term, case_id", [
    (data.SEARCH_INVALID_PERIOD,         "Case-10"),   #Periods
    (data.SEARCH_INVALID_COMMA,          "Case-11"),   #Commas
    (data.SEARCH_INVALID_NON_LATIN,      "Case-18"),   #Non-Latin characters
    (data.SEARCH_INVALID_UNICODE,        "Case-19"),   #Unicode characters
    (data.SEARCH_INVALID_HTML,           "Case-21"),   #HTML tags
    (data.SEARCH_INVALID_SPECIAL_CHARS,  "Case-22"),   #Special characters
    (data.SEARCH_INVALID_EMPTY,          "Case-23"),   #Nothing/Whitespace
])
def test_cases_rejects_invalid_characters(driver, term, case_id):
    page = BugHuntShop2Page(driver)
    page.enter_product_search(term)
    page.click_search_button()
    assert page.get_search_error() != ""

def test_case_24_invalid_search_shows_not_found_message(driver):
    # --- Case-24: Verify invalid input displays "Not found for {invalid input}" message.---
    page = BugHuntShop2Page(driver)
    page.enter_product_search("camera")
    page.click_search_button()
    results = page.driver.find_element(*page.SEARCH_RESULTS_BOX_LOCATOR)
    assert "No products found" in results.text

# --- Boundary value group (Cases 26,27,28) ---
@pytest.mark.parametrize("term, case_id", [
    (data.SEARCH_BOUNDARY_1_CHAR,     "Case-26"),
    (data.SEARCH_BOUNDARY_2_CHAR,     "Case-26"),
    (data.SEARCH_BOUNDARY_3_CHAR,     "Case-27"),
    (data.SEARCH_BOUNDARY_14_CHAR,    "Case-27"),
    (data.SEARCH_BOUNDARY_97_CHAR,    "Case-27"),
])
def test_search_boundary_values(driver, term, case_id):
    # --- Cases 26,27,28: Verify boundary values in Products Search field ---
    page = BugHuntShop2Page(driver)
    page.enter_product_search(term)
    page.click_search_button()
    if case_id == "Case-27":
        # Valid length - no error expected
        assert page.get_search_error() == ""
    elif case_id == "Case-26":
        # Invalid length - error expected
        assert page.get_search_error() != ""
    else:
        raise ValueError(f"Unexpected case_id: {case_id}")

@pytest.mark.xfail(reason="BHS2-17: Field silently caps at 100 characters, no error shown")
def test_case_28_over_limit_shows_error(driver):
    # ---Case-28: Verify input over 100 characters is rejected with an error message ---
    page = BugHuntShop2Page(driver)
    page.enter_product_search(data.SEARCH_BOUNDARY_101_CHAR)
    page.click_search_button()
    assert page.get_search_error() != ""

# ---Our Products & Shopping Cart Test Cases ---

@pytest.mark.xfail(reason="BHS2-1: Only 3 of 5 products are displayed in product grid.")
def test_case_29_all_products_present(driver):
    # ---Case-29: Verify all {product} selections are present in design ---
    page = BugHuntShop2Page(driver)
    assert len(page.get_product_cards()) == 5

def test_case_30_products_aligned_in_a_row(driver):
    # ---Case-30: Verify {product} selections are aligned in a row on the display ---
    page = BugHuntShop2Page(driver)
    products = page.get_product_cards()
    y_positions = [p.location['y'] for p in products]
    assert max(y_positions) - min(y_positions) <= 5

def test_case_31_products_spelling_is_correct(driver):
    # ---Case-31: Verify product's spelling is correct on display ---
    page = BugHuntShop2Page(driver)
    names = page.get_product_names()
    assert "Gaming Laptop" in names
    assert "Smartphone" in names
    assert "Tablet" in names

def test_case_32_product_prices_correct(driver):
    # ---Verify price of {product} is correct by requirements ---
    page = BugHuntShop2Page(driver)
    prices = page.get_product_prices()
    assert "$999.99" in prices
    assert "$599.99" in prices
    assert "$299.99" in prices

def test_case_33_subtotal_empty_cart(driver):
    # ---Verify "Subtotal" displays "0.00" when "Shopping Cart" is empty ---
    page = BugHuntShop2Page(driver)
    subtotal = page.driver.find_element(*page.SUBTOTAL_SUM_LOCATOR).text.strip()
    assert subtotal == "0.00"

@pytest.mark.xfail(reason="BHS2-18: Tax calculated as subtotal + 0.085 instead of subtotal * 0.085")
def test_case_34_tax_correct_empty_cart(driver):
    # ---Verify "Tax" percentage is correct by requirements ---
    page = BugHuntShop2Page(driver)
    page.click_gaming_laptop_from_products_box()
    subtotal = float(page.driver.find_element(*page.SUBTOTAL_SUM_LOCATOR).text.strip())
    expected_tax = round(subtotal * 0.085, 2)
    actual_tax = float(page.driver.find_element(*page.TAX_SUM_LOCATOR).text.strip())
    assert actual_tax == expected_tax

def test_case_35_shipping_cost_correct(driver):
    # ---Verify "Shipping" shows $5.99" ---
    page = BugHuntShop2Page(driver)
    shipping = page.driver.find_element(*page.SHIPPING_TOTAL_LOCATOR).text.strip()
    assert shipping == "5.99"

@pytest.mark.xfail(reason="BHS2-19: Total should reflect $0.00 subtotal + $0.00 tax + $5.99 shipping only after a product is added")
def test_case_36_zero_total_with_no_product(driver):
    # ---Verify  "Total" is "0.00" with no {product} is added. ---
    page = BugHuntShop2Page(driver)
    total = page.driver.find_element(*page.FULL_TOTAL_LOCATOR).text.strip()
    assert total == "0.00"

def test_case_37_prod_can_be_added_to_cart(driver):
    # --- Verify a clickable {product} can be added to the "Shopping Cart". ---
    page = BugHuntShop2Page(driver)
    page.click_gaming_laptop_from_products_box()
    assert page.get_cart_item_count() == 1

@pytest.mark.parametrize("products, case_id", [
    (data.CART_BOUNDARY_0_PRODUCTS, "Case-38"),
    (data.CART_BOUNDARY_1_PRODUCT,  "Case-39"),
    (data.CART_BOUNDARY_2_PRODUCTS, "Case-39"),
    (data.CART_BOUNDARY_3_PRODUCTS, "Case-39"),
    (data.CART_BOUNDARY_7_PRODUCTS, "Case-40"),
])
def test_products_boundary_values(driver, products, case_id):
    page = BugHuntShop2Page(driver)
    for p in range(products):
        page.click_gaming_laptop_from_products_box()
    assert page.get_cart_item_count() == products

def test_case_41_product_added_message_appears(driver):
    # ---Verify when {product} is added to "Cart", the message "{product} is added to cart!" appears. ---
    page = BugHuntShop2Page(driver)
    page.click_tablet_from_products_box()
    notification = page.get_add_to_cart_notification("Tablet")
    assert notification.is_displayed()

def test_case_42_prod_displayed_in_cart(driver):
    # ---Verify {product} is displayed in "Shopping Cart". ---
    page = BugHuntShop2Page(driver)
    page.click_gaming_laptop_from_products_box()
    assert "Gaming Laptop" in page.get_cart_item_names()

def test_case_43_prod_price_displayed_correctly(driver):
    # ---Verify price of {product} displays to the right in the same row. ---
    page = BugHuntShop2Page(driver)
    page.click_gaming_laptop_from_products_box()
    page.click_smartphone_from_products_box()
    page.click_tablet_from_products_box()
    prices = page.get_cart_item_prices()
    assert "$999.99" in prices
    assert "$599.99" in prices
    assert "$299.99" in prices

def test_case_44_subtotal_displayed_correctly(driver):
    # ---Verify "Subtotal" shows base price of product. ---
    page = BugHuntShop2Page(driver)
    page.click_tablet_from_products_box()
    subtotal = page.driver.find_element(*page.SUBTOTAL_SUM_LOCATOR).text.strip()
    assert subtotal == "299.99"

@pytest.mark.xfail(reason="BHS2-18: Tax calculated as subtotal + 0.085 instead of subtotal * 0.085")
def test_case_45_sum_of_subtotal_and_tax_correct(driver):
    # ---Verify SUM of "Subtotal" and "Tax" is correct. ---
    page = BugHuntShop2Page(driver)
    page.click_smartphone_from_products_box()
    subtotal = page.get_subtotal()
    actual_tax = round(page.get_tax(), 2)
    expected_sum = round(subtotal + round(subtotal * 0.085, 2), 2)
    actual_sum = round(subtotal + actual_tax, 2)
    assert actual_sum == expected_sum

@pytest.mark.xfail(reason="BHS2-18: Total is incorrect due to tax bug(subtotal + 0.085 instead of subtotal * 0.085)")
def test_case_46_sum_of_subtotal_tax_and_shipping_correct(driver):
    # ---Verify SUM of "Subtotal", "Tax", and "Shipping" is correct. ---
    page = BugHuntShop2Page(driver)
    page.click_gaming_laptop_from_products_box()
    subtotal = page.get_subtotal()
    actual_tax = round(page.get_tax(), 2)
    shipping = round(page.get_shipping(), 2)
    expected_total = round(subtotal + round(subtotal * 0.085, 2) + shipping, 2)
    actual_total = round(subtotal + actual_tax + shipping, 2)
    assert actual_total == expected_total



































