import pytest
from pages import BugHuntShop2Page
import data
from selenium.webdriver.support import expected_conditions as EC


def test_launch_app(driver):
    """Verifies the app opens and has the correct title."""
    assert "Bug Hunt" in driver.title

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
    # --- Case-24: Verify invalid input displays "Not found for {invalid input} message.---
    page = BugHuntShop2Page(driver)
    page.enter_product_search("camera")
    page.click_search_button()
    results = page.driver.find_element(*page.SEARCH_RESULTS_BOX_LOCATOR)
    assert "No products found" in results.text

# --- Boundary value group (Cases 26,27,28) ---
@pytest.mark.parametrize("term, case_id", [
    (data.SEARCH_BOUNDARY_1_CHAR,     "Case-26"),
    (data.SEARCH_BOUNDARY_2_CHAR,     "Case-26"),
    (data.SEARCH_BOUNDARY_14_CHAR,    "Case-27"),
    (data.SEARCH_BOUNDARY_97_CHAR,    "Case-27"),
    (data.SEARCH_BOUNDARY_101_CHAR,   "Case-28"),
])
def test_search_boundary_values(driver, term, case_id):
    # --- Cases 26,27,28: Verify boundary values in Products Search field ---
    page = BugHuntShop2Page(driver)
    page.enter_product_search(term)
    page.click_search_button()
    if case_id == "Case-27":
        # Valid length - no error expected
        assert page.get_search_error() == ""
    else:
        # Invalid length - error expected
        assert page.get_search_error() != ""