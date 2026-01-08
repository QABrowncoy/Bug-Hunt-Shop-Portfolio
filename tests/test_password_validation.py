import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestPasswordValidation:
    """Test cases for password requirements"""
    def tes_password_less_than_8_char_invalid:
