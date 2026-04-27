from secrets import token_urlsafe
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import Select
import json
import time

class BugHuntShop2Page:
    PROD_SEAR_FIELD_LOCATOR = (By.ID, "searchInput")
    SEARCH_BUTTON_LOCATOR = (By.ID, "searchBtn")
    SEARCH_RESULTS_BOX_LOCATOR = (By.ID, "searchResults")
    SEARCH_RESULTS_ADD_BUTTONS_LOCATOR = (By.XPATH, "//div[@id='searchResults']//button")
    GAMING_LAPTOP_BUTTON_LOCATOR = (By.XPATH, "//div[@class='product-card']//h3[text()='Gaming Laptop']/following-sibling::button")
    SMARTPHONE_BUTTON_LOCATOR = (By.XPATH, "//div[@class='product-card']//h3[text()='Smartphone']/following-sibling::button")
    TABLET_BUTTON_LOCATOR = (By.XPATH, "//div[@class='product-card']//h3[text()='Tablet']/following-sibling::button")
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
    TEST_RESULTS_FIELD_LOCATOR = (By.ID, "testResult")
    TEST_RESULT_VALIDATION_LOCATOR = (By.CSS_SELECTOR, "#testResult p span")
    TEST_RESULT_LENGTH_LOCATOR = (By.XPATH, "//div[@id='testResult']//p[contains(text(), 'characters')]")

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

    def get_search_result_cards(self):
        """Returns only product card elements found within the search results box."""
        # ---This specificallytargets cards inside the searchResults div ---
        return self.driver.find_elements(By.XPATH, "//div[@id='searchResults']//div[@class='product-card']")

    def click_gaming_laptop_from_products_box(self):
        element = self.wait.until(EC.element_to_be_clickable(self.GAMING_LAPTOP_BUTTON_LOCATOR))
        element.click()

    def click_smartphone_from_products_box(self):
        element = self.wait.until(EC.element_to_be_clickable(self.SMARTPHONE_BUTTON_LOCATOR))
        element.click()

    def click_smart_watch_from_products_box(self):
        element = self.wait.until(EC.element_to_be_clickable(self.SMART_WATCH_BUTTON_LOCATOR))
        element.click()

    def click_tablet_from_products_box(self):
        element = self.wait.until(EC.element_to_be_clickable(self.TABLET_BUTTON_LOCATOR))
        element.click()

    def click_wireless_headphones_from_products(self):
        element = self.wait.until(EC.element_to_be_clickable(self.WIRELESS_PHONES_BUTTON_LOCATOR))
        element.click()

    def get_product_cards(self):
        #--- Returns all product card elements ---
        return self.driver.find_elements(By.XPATH, "//div[@class='product-card']")

    def get_product_names(self):
        # ---Returns list of product name strings ---
        names = self.driver.find_elements(By.XPATH, "//div[@class='product-card']//h3")
        return [n.text for n in names]

    def get_product_prices(self):
        # ---Returns list of product price strings ---
        prices = self.driver.find_elements(By.XPATH, "//div[@class='product-card']//p[@class='price']")
        return [p.text for p in prices]

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

    # ---Cart state getters ---
    def get_cart_items(self):
        return self.driver.find_elements(By.XPATH, "//div[@id='cartItems']//div[@class='cart-item']")

    def get_cart_item_names(self):
        """Returns list of product name strings currently in the cart."""
        items = self.get_cart_items()
        return [item.find_element(By.XPATH, ".//span[1]").text for item in items]

    def get_cart_item_prices(self):
        """Returns list of WebElements for the prices currently in the cart."""
        items = self.get_cart_items()
        return [item.find_element(By.XPATH, ".//span[2]").text for item in items]

    def get_cart_item_prices_as_floats(self):
        """Returns a list of floats for math calculations."""
        elements = self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEM_PRICES_LOCATOR))
        return [float(elements.text.replace('$', '')) for element in elements]

    def get_cart_item_price_elements(self):
        """Returns the raw list of WebElements for UI/Alignment checks"""
        return self.wait.until(EC.visibility_of_all_elements_located(self.CART_ITEM_PRICES_LOCATOR))
        message="Timed out waiting for cart price elements to appear."

    def get_cart_item_count(self):
        """Returns nummber of items currently in cart."""
        return len(self.get_cart_items())

    def get_remove_buttons(self):
        return self.driver.find_elements(*self.CART_REMOVE_ALL_BUTTONS_LOCATOR)

    def get_cart_message(self):
        element = self.wait.until(EC.presence_of_element_located((By.ID, "cartItems")))
        return element.text.strip()

    def get_add_to_cart_notification(self, product_name):
        locator = (By.XPATH, f"//div[contains(text(), '{product_name} added to cart!')]")
        return self.wait.until(EC.visibility_of_element_located(locator))

    def get_cart_cleared_notification(self):
        """Returns the Cart cleared notification element."""
        locator = (By.XPATH, "//div[contains(text(), 'Cart cleared')]")
        return self.wait.until(EC.visibility_of_element_located(locator))

    def get_subtotal(self):
        """Returns subtotal as float."""
        return float(self.wait.until(EC.visibility_of_element_located(self.SUBTOTAL_SUM_LOCATOR)).text.strip())

    def get_tax(self):
        """Returns tax as float."""
        return float(self.wait.until(EC.visibility_of_element_located(self.TAX_SUM_LOCATOR)).text.strip())

    def get_shipping(self):
        """Returns shipping as float."""
        return float(self.wait.until(EC.visibility_of_element_located(self.SHIPPING_TOTAL_LOCATOR)).text.strip())

    def get_total(self):
        """Returns total as float, handling currency symbols and whitespace."""
        element_text = self.wait.until(EC.visibility_of_element_located(self.FULL_TOTAL_LOCATOR)).text
        clean_text = element_text.strip().replace("$", "").replace(",", "").strip()
        return float(clean_text)

    def verify_cart_summary_totals(self):
        TAX_RATE = 0.085
        SHIPPING = 5.99
        # ---The notes are for me (Corey)...---
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
    def scroll_to_contact_and_verify_empty(self):
        """
        Scrolls to the Contact section and verifies all fields are empty.
        Uses IDs: name, email, phone, message from enhanced-index.html.
        """
        contact_section = self.wait.until(EC.presence_of_element_located((By.ID, "contact")))
        self.driver.execute_script("arguments[0].click();", contact_section)
        field_ids = ["name", "email", "phone", "message"]
        for ids in field_ids:
            element = self.driver.find_element(By.ID, ids)
            value = element.get_attribute("value")
            assert value == "", f"Error: Field '{ids} should be empty but found '{value}'"

    def get_contact_validation_errors(self):
        """
        Finds all active messages in the contact form.
        Returns a list of text strings from the .error-message divs.
        """
        # Your script creates <div class="error-message"> elements ---
        errors = self.driver.find_elements(By.CLASS_NAME, "error-message")
        return [error.text for error in errors if error.is_displayed()]

    def get_browser_validation_message(self, field_id):
        """
         Retrieves the HTML5 validation message (e.g., 'Please fill out this filed').
         Verified against enhanced-index.html where the required attribute is present.
        """
        # Find the element by the ID passed from the test (e.g., 'name')
        element = self.driver.find_element(By.ID, field_id)
        # .get_property("validationMessage") is the secret to reading the browser tooltips
        return element.get_property("validationMessage")

    def fill_contact_us_fields(self, locator, text):
        """Internal helper to handle the wait/clear/send_keys logic."""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.clear()
            element.send_keys(text)
        except:
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", element)
            element.clear()
            element.send_keys(text)

    def cont_us_name(self,name_text):
        self.fill_contact_us_fields(self.NAME_LOCATOR, name_text)

    def cont_us_email(self,email_text):
        self.fill_contact_us_fields(self.EMAIL_LOCATOR, email_text)

    def cont_us_phone(self,phone_text):
        self.fill_contact_us_fields(self.PHONE_LOCATOR, phone_text)

    def cont_us_message(self,message_text):
        self.fill_contact_us_fields(self.MESSAGE_LOCATOR, message_text)

    def click_send_message_button(self):
        element = self.wait.until(EC.element_to_be_clickable(self.SEND_MESSAGE_BUTTON_LOCATOR))
        element.click()

    def log_username(self, username_text):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.USERNAME_LOCATOR))
            element = self.wait.until(EC.element_to_be_clickable(self.USERNAME_LOCATOR))
            element.clear()
            element.send_keys(username_text)
        except:
            element = self.driver.find_element(*self.USERNAME_LOCATOR)
            self.driver.execute_script("arguments[0].click();", element)
            element.clear()
            element.send_keys(username_text)

    def log_password(self, password_text):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.PASSWORD_LOCATOR))
            element = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_LOCATOR))
            element.clear()
            element.send_keys(password_text)
        except:
            element = self.driver.find_element(*self.PASSWORD_LOCATOR)
            self.driver.execute_script("arguments[0].click();", element)
            element.clear()
            element.send_keys(password_text)

    def click_remember_button(self):
        element = self.wait.until(EC.element_to_be_clickable(self.REMEMBER_ME_LOCATOR))
        element.click()

    def click_log_in_button(self):
        element = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON_LOCATOR))
        element.click()

    def enter_univ_tester_input(self, univ_tester_input):
        try:
            element = self.wait.until(EC.presence_of_element_located(self.TEST_INPUT_FIELD_LOCATOR))
            element = self.wait.until(EC.element_to_be_clickable(self.TEST_INPUT_FIELD_LOCATOR))
            element.clear()
            element.send_keys(univ_tester_input)
        except:
            element = self.driver.find_element(*self.TEST_INPUT_FIELD_LOCATOR)
            self.driver.execute_script("arguments[0].click();", element)
            element.clear()
            element.send_keys(univ_tester_input)

    def click_univ_tester_dropdown(self, univ_tester_dropdown):
        element = self.wait.until(EC.element_to_be_clickable(self.TEST_SELECTOR_DROPDOWN_LOCATOR))
        Select(element).select_by_visible_text(univ_tester_dropdown)
        # --- How you'd call it in tests using the visible text: ---
        # --- page.click_univ_tester_dropdown("Test as Name")
        # --- page.click_univ_tester_dropdown("Test as Email")
        # --- page.click_univ_tester_dropdown("Test as Phone")
        # --- page.click_univ_tester_dropdown("Test as Search")
        # --- page.click_univ_tester_dropdown("Test as Username") ---

    def click_test_validation_button(self):
        element = self.wait.until(EC.element_to_be_clickable(self.TEST_VALIDATION_BUTTON_LOCATOR))
        element.click()

    def get_test_result_validation(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.TEST_RESULT_VALIDATION_LOCATOR))
        return element.text.strip()

    # --- After going through the "boxes", you would go through the "nav's" and the "errors". ---
    # --- 4 nav click methods ---

    def click_nav_home(self):
        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#home']")))
        element.click()

    def click_nav_products(self):
        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#products']")))
        element.click()

    def click_nav_contact(self):
        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#contact']")))
        element.click()

    def click_nav_login(self):
        element = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#login']")))
        element.click()

    # --- 7 error message getters ---

    def get_search_error(self):
        element = self.wait.until(EC.presence_of_element_located((By.ID, "searchError")))
        return element.text.strip()

    def get_name_error(self):
        element = self.wait.until(EC.presence_of_element_located((By.ID, "nameError")))
        return element.text.strip()

    def get_email_error(self):
        element = self.wait.until(EC.presence_of_element_located((By.ID, "emailError")))
        return element.text.strip()

    def get_phone_error(self):
        element = self.wait.until(EC.presence_of_element_located((By.ID, "phoneError")))
        return element.text.strip()

    def get_message_error(self):
        element = self.wait.until(EC.presence_of_element_located((By.ID, "messageError")))
        return element.text.strip()

    def get_username_error(self):
        element = self.wait.until(EC.presence_of_element_located((By.ID, "usernameError")))
        return element.text.strip()

    def get_password_error(self):
        element = self.wait.until(EC.presence_of_element_located((By.ID, "passwordError")))
        return element.text.strip()

    # --- 2 form result getters ---

    def get_contact_result(self):
        element = self.wait.until(EC.presence_of_element_located((By.ID, "contactResult")))
        return element.text.strip()

    def get_login_result(self):
        element = self.wait.until(EC.presence_of_element_located((By.ID, "loginResult")))
        return element.text.strip()

    # --- 1 character counter getter ---

    def get_message_char_count(self):
        element = self.wait.until(EC.visibility_of_element_located((By.ID, "messageCount")))
        return element.text.strip()

    # --- 1 password strength getter ---

    def get_password_strength(self):
        element = self.wait.until(EC.presence_of_element_located((By.ID, "passwordStrength")))
        return element.get_attribute("class")
        # --- This is where you'll USE it later in test.py...
        # --- def test_password_strength_strong():
        #     page.log_password("Password123")
        #     assert "strength-strong" in page.get_password_strength()
        #
        # def test_password_strength_weak():
        #     page.log_password("abc")
        #     assert "strength-weak" in page.get_password_strength() ---

    # --- 1 test suggestion clicker ---

    def click_test_suggestion(self, button_text):
        locator = (
            By.XPATH,
            f"//div[@class='test-cases']//button[contains(text(), '{button_text}')]"
        )
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    # ---Call like: page.click_test_suggestion("Name with apostrophe") ---
    # ---Suggestion types for testing are: Name with apostrophe, Invalid email, Formatted phone, Unicode text, ---
    # ---XSS attempt, Empty input, Only spaces, Single character, Very long text ---

    # --- 1 test result length getter ---

    def get_test_result_length(self):
        element = self.wait.until(EC.visibility_of_element_located(self.TEST_RESULT_LENGTH_LOCATOR))
        return element.text.strip()













