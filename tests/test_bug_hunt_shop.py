import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages import BugHuntShop2Page
import data  # Your data.py file



@pytest.fixture
def driver():
    # webdriver-manager handles the driver download for you automatically
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_launch_app(driver):
    """Verifies the app opens and has the correct title."""
    driver.get(data.BUG_HUNT_SHOP_2_URL)
    assert "Bug Hunt" in driver.title


@pytest.mark.parametrize("term", [
    data.SEARCH_VALID_LATIN,
    data.SEARCH_VALID_DASH,
    data.SEARCH_VALID_NUMBERS
])
def test_search_functionality(driver, term):
    """Verifies valid search terms return results without errors."""
    driver.get(data.BUG_HUNT_SHOP_2_URL)
    page = BugHuntShop2Page(driver)
    page.enter_product_search(term)
    page.click_search_button()
    assert page.get_search_error() == ""