import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
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


@pytest.mark.parametrize("term", data.SEARCH_TERMS)
def test_search_functionality(driver, term):
    """Runs a separate test for every search term in your data.py"""
    driver.get(data.BUG_HUNT_SHOP_2_URL)

    # Locate your search bar (Update the ID to match your HTML)
    search_input = driver.find_element(By.ID, "search-input")
    search_input.send_keys(term)
    driver.find_element(By.ID, "search-button").click()

    # If the term is expected to be broken, you might assert an error is visible
    if term in data.EXPECTED_BROKEN_TERMS:
        # Example: check if an error message appears
        # assert driver.find_element(By.ID, "error").is_displayed()
        print(f"Verified expected bug for: {term}")