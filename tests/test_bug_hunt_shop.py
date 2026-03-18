import pytest
from pages import BugHuntShop2Page
import data


def test_launch_app(driver):
    """Verifies the app opens and has the correct title."""
    assert "Bug Hunt" in driver.title


@pytest.mark.parametrize("term", [
    data.SEARCH_VALID_LATIN,
    data.SEARCH_VALID_DASH,
    data.SEARCH_VALID_NUMBERS
])
def test_search_functionality(driver, term):
    """Verifies valid search terms return results without errors."""
    page = BugHuntShop2Page(driver)
    page.enter_product_search(term)
    page.click_search_button()
    assert page.get_search_error() == ""