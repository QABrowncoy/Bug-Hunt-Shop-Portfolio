import pytest
from pages import BugHuntShop2Page
import data


def test_launch_app(driver):
        """Verifies the app opens and has the correct title."""
        assert "Bug Hunt" in driver.title

def