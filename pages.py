from secrets import token_urlsafe

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
import json
import time

class BugHuntShop2Page:
    PROD_SEAR_FIELD_LOCATOR = (By.ID, "searchInput")
    SEARCH_BUTTON_LOCATOR = (By.ID, "searchBtn")
    SEARCH_RESULTS_BOX_LOCATOR = (By.ID, "searchResults")
    GAMING_LAPTOP_BUTTON_LOCATOR = (By.XPATH, "//div[@class='product-card']//h3[text()='Gaming Laptop']/following-sibling::button")
    SMARTPHONE_BUTTON_LOCATOR = (By.XPATH, "//div[@class='product-card']//h3[text()='Smartphone']/following-sibling::button")
    TABLET_BUTTON_LOCATOR = (By.XPATH, "//div[@class='products-card']//h3[text()='Tablet']/following-sibling::button")
    WIRELESS_PHONES_BUTTON_LOCATOR = (By.XPATH, "//div[@id='searchResults']//strong[text()='Wireless Headphones']/following-sibling::button")
    SMART_WATCH_BUTTON_LOCATOR = (By.XPATH, "//div[@id='searchResults']//strong[text()='Smart Watch']/following-sibling::button")
    CART_CONTAINER_LOCATOR = (By.XPATH, "//div[@class='cart-container']")
    # When testing, REMOVE_BUTTON_LOCATOR needs list number in the parenthesis at end
    REMOVE_BUTTON_LOCATOR = (By.XPATH, "//div[@id='cartItems']//button[contains('@onclick', 'removeFromCart()')]")
    CLEAR_CART_BUTTON_LOCATOR = (By.ID, "clearCartBtn")
    SUBTOTAL_SUM_LOCATOR = (By.ID, "subtotal")
    TAX_SUM_LOCATOR = (By.ID, "tax")
    SHIPPING_TOTAL_LOCATOR = (By.ID, "shipping")
    FULL_TOTAL_LOCATOR = (By.ID, "total")
    NAME_LOCATOR = (By.ID, "name")
    EMAIL_LOCATOR = (By.ID, "email")
    PHONE_LOCATOR = (By.ID, "phone")
    MESSAGE_LOCATOR = (By.ID, "message")
    SEND_MESSAGE_BUTTON_LOCATOR = (By.CSS_SELECTOR, "#contactForm button[type='submit']")
    USERNAME_LOCATOR = (By.ID, "username")
    PASSWORD_LOCATOR = (By.ID, "password")
    REMEMBER_ME_LOCATOR = (By.ID, "rememberMe")
    LOGIN_BUTTON_LOCATOR = (By.CSS_SELECTOR, "#loginForm button[type='submit']")
    TEST_INPUT_FIELD_LOCATOR = (By.ID, "testInput")
    TEST_SELECTOR_DROPDOWN_LOCATOR = (By.ID, "testType")
    TEST_VALIDATION_BUTTON_LOCATOR = (By.XPATH, "//button[contains(@onclick, 'testInput()')]")
    TEST_RESULTS_FIELD_LOCATOR = (By.ID, "testResults")

    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 10)
        self.driver = driver





