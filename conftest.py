import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os


@pytest.fixture(scope="function")
def driver():
    """Setup and teardown for browser"""
    # Setup
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    # Get the path to your HTML file
    html_file = os.path.abspath("enhanced-index.html")
    driver.get(f"file:///{html_file}")

    yield driver

    # Teardown
    driver.quit()