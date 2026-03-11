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
    CART_ITEM_PRICES_LOCATOR = (By.XPATH, "//div[@id='cartItems']//div[@class='cart-item']//span[contains(text(), '$')]")
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
            buttons = self.driver.find_elements(*self.SEARCH_RESULTS_ADD_BUTTONS_LOCATOR)
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

    def shop_cart_result_cleared(self, product_name):
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

    def shop_cart_results_cleared_by_index(self, index):
        locator = (
            By.XPATH,
            f"//div[@id='cartItems']//div[@class='cart-item'][{index}]//button"
        )
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

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
        element = self.wait.until(EC.element_to_be_clickable(self.CLEAR_CART_BUTTON_LOCATOR))
        element.click()

    def verify_cart_summary_totals(self):
        TAX_RATE = 0.085
        SHIPPING = 5.99
        # ---The notes are for me...---
        # --- Step 1: Grab all item prices from cart and sum them ---
        price_elements = self.driver.find_elements(*self.CART_ITEM_PRICES_LOCATOR)
        item_prices = []
        for pr_el in price_elements:
            raw = pr_el.text.strip().replace("$", "")
            item_prices.append(float(raw))

        expected_subtotal = round(sum(item_prices), 2)
        expected_tax = round(expected_subtotal * TAX_RATE, 2)
        expected_shipping = SHIPPING
        expected_total = round(expected_subtotal + expected_tax + expected_shipping, 2)

        # --- Step 2: Read what the UI is actually showing (no $ stripping needed) ---
        actual_subtotal = float(
            self.wait.until(EC.visibility_of_element_located(self.SUBTOTAL_SUM_LOCATOR)).text.strip()
        )
        actual_tax = float(
            self.wait.until(EC.visibility_of_element_located(self.TAX_SUM_LOCATOR)).text.strip()
        )
        actual_shipping = float(
            self.wait.until(EC.visibility_of_element_located(self.SHIPPING_TOTAL_LOCATOR)).text.strip()
        )
        actual_total = float(
            self.wait.until(EC.visibility_of_element_located(self.FULL_TOTAL_LOCATOR)).text.strip()
        )

        # --- Step 3: Return results dictionary ---
        return {
            "subtotal": {"expected": expected_subtotal, "actual": actual_subtotal,    "pass": expected_subtotal == actual_subtotal},
            "tax": {"expected": expected_tax,           "actual": actual_tax,         "pass": expected_tax == actual_tax},
            "shipping": {"expected": expected_shipping, "actual": actual_shipping,    "pass": expected_shipping == actual_shipping},
            "total": {"expected": expected_total,       "actual": actual_total,       "pass": expected_total == actual_total},
        }
    def cont_us_name(self,name_text):
        try:
            element = self.wait.until(EC.presence_of_element_located(*self.NAME_LOCATOR))
            element = self.wait.until(EC.element_to_be_clickable(aelf.NAME_LOCATOR))
            element.clear()
            element.send_keys(name_text)
        except:
            element = self.driver.find_element(*self.NAME_LOCATOR)
            self.driver.execute_script("arguments[0].click();", element)
            element.clear()
            element.send_keys(name_text)

    def
