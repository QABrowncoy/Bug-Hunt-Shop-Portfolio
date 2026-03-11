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
    SEARCH_RESULTS_ADD_BUTTONS_LOCATOR = (By.XPATH, "//div[@id='searchResults']//button")
    GAMING_LAPTOP_BUTTON_LOCATOR = (By.XPATH, "//div[@class='product-card']//h3[text()='Gaming Laptop']/following-sibling::button")
    SMARTPHONE_BUTTON_LOCATOR = (By.XPATH, "//div[@class='product-card']//h3[text()='Smartphone']/following-sibling::button")
    TABLET_BUTTON_LOCATOR = (By.XPATH, "//div[@class='products-card']//h3[text()='Tablet']/following-sibling::button")
    WIRELESS_PHONES_BUTTON_LOCATOR = (By.XPATH, "//div[@id='searchResults']//strong[text()='Wireless Headphones']/following-sibling::button")
    SMART_WATCH_BUTTON_LOCATOR = (By.XPATH, "//div[@id='searchResults']//strong[text()='Smart Watch']/following-sibling::button")
    CART_CONTAINER_LOCATOR = (By.XPATH, "//div[@class='cart-container']")
    CART_REMOVE_BUTTON_LOCATOR = (By.XPATH, "//div[@id='cartItems']//div[@class='cart-item'][{index}]//button")
    CART_REMOVE_ALL_BUTTONS_LOCATOR = (By.XPATH, "//div[@id='cartItems']//button")
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

    def enter_product_search(self, search_input):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.PROD_SEAR_FIELD_LOCATOR))
            element = self.wait.until(EC.element_to_be_clickable(self.PROD_SEAR_FIELD_LOCATOR))
            element.clear()
            element.send_keys(search_input)
        except:
            element = self.driver.find_element(*self.PROD_SEAR_FIELD_LOCATOR)
            self.driver.execute_script("arguments[0].click();", element)
            element.clear()
            element.send_keys(search_input)

    def click_search_button(self):
        element = self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON_LOCATOR))
        element.click()

    def sear_results_added(self, product_name):
        locator = (
            By.XPATH,
            f"//div[@id='searchResults']//strong[text()='{product_name}']/following-sibling::button"
        )
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except TimeoutException:
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", element)

    def sear_all_results_added(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.SEARCH_RESULTS_BOX_LOCATOR))
            buttons = self.driver.find_elements(*self.SEARCH_RESULTS_BOX_LOCATOR)
            for button in buttons:
                try:
                    self.wait.until(EC.element_to_be_clickable(button))
                    button.click()
                    time.sleep(1)
                except WebDriverException:
                    self.driver.execute_script("arguments[0].click();", button)
        except TimeoutException:
            print("No buttons present")

    def click_gaming_laptop_from_products_box(self):
        element = self.wait.until(EC.element_to_be_clickable(self.GAMING_LAPTOP_BUTTON_LOCATOR))
        element.click()

    def click_smartphone_from_products_box(self):
        element = self.wait.until(EC.element_to_be_clickable(self.SMARTPHONE_BUTTON_LOCATOR))
        element.click()

    def click_tablet_from_products_box(self):
        element = self.wait.until(EC.element_to_be_clickable(self.TABLET_BUTTON_LOCATOR))
        element.click()

    def shop_cart_results_cleared(self, product_name):
        locator = (
            By.XPATH,
            f"//div[@id='cartItems']//span[text()='{product_name}']/following-sibling::button"
        )
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except TimeoutException:
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", element)

    def shop_cart_all_results_cleared(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.CART_CONTAINER_LOCATOR))
            buttons = self.driver.find_elements(*self.CART_REMOVE_ALL_BUTTONS_LOCATOR)
            for button in buttons:
                try:
                    self.wait.until(EC.element_to_be_clickable(button))
                    button.click()
                    time.sleep(1)
                except TimeoutException:
                    self.driver.execute_script("arguments[0].click();", button)
        except TimeoutException:
            print("Cart items not found.")

    def click_clear_cart_button(self):
        element = self.wait.until(EC.element_to_be_clickable(self.CART_REMOVE_BUTTON_LOCATOR))