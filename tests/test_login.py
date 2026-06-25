import pytest
from pages.login_page import LoginPage


class TestLogin:

    def test_valid_login(self, driver):

        page = LoginPage(driver)

        page.open()

        page.login("standard_user", "secret_sauce")

        assert page.is_login_successful(), \
            "Valid Login failed - Products page did not load"

    def test_locked_out_user(self, driver):
        page = LoginPage(driver)
        page.open()
        page.login("locked_out", "secret_sauce")
        error = page.get_error_message()
        assert "locked_out" in error, \
            f"Expected error message to contain 'locked_out', but got: {error}"

    def test_invalid_login(self, driver):
        page = LoginPage(driver)
        page.open()
        page.login("invalid_user", "invalid_password")
        error = page.get_error_message()
        assert "Username and password do not match" in error, \
            f"Expected mismatch message, got: {error}"

    # tests/test_login.py


# We import LoginPage from our pages folder.
# This is the ONLY import we need.
# We do NOT import conftest.py — pytest handles that automatically.
# We do NOT import selenium — LoginPage handles that internally.


class TestLogin:
    # We wrap tests in a class to group related tests together.
    # pytest finds any class starting with "Test" automatically.
    # pytest finds any function starting with "test_" automatically.
    # Both rules must be true: class starts with Test,
    # function starts with test_

    def test_valid_login(self, driver):
        # 'driver' in the parameter → pytest sees this word,
        # looks in conftest.py, finds the driver() fixture,
        # runs it, and hands us a ready Chrome browser.
        # We never call driver() ourselves. pytest does it.

        page = LoginPage(driver)
        # Create one LoginPage object for this test.
        # Pass driver in so LoginPage can control the browser.
        # Think of this as: "give me the tools to work
        # with the login page using this browser"

        page.open()
        # Calls open() in LoginPage → driver.get(URL)
        # Chrome navigates to saucedemo.com

        page.login("standard_user", "secret_sauce")
        # Calls login() in LoginPage →
        #   enter_username("standard_user")
        #   enter_password("secret_sauce")
        #   click_login()
        # All three steps, one line in the test.

        assert page.is_login_successful(), \
            "Valid login failed — Products page did not load"
        # is_login_successful() goes to LoginPage →
        # checks if PRODUCTS_TITLE element exists and says "Products"
        # If True  → assert passes → test PASSED
        # If False → assert fails  → test FAILED with our message
        # The message after the comma tells us WHY it failed.
        # Without it you just see "AssertionError" — not helpful.

    def test_locked_out_user(self, driver):
        page = LoginPage(driver)
        page.open()
        page.login("locked_out_user", "secret_sauce")
        # locked_out_user is a built-in test user on saucedemo.
        # The site blocks this user deliberately.

        error = page.get_error_message()
        # get_error_message() reads the red error text on screen.
        # Stores it in variable 'error' so we can inspect it.

        assert "locked out" in error.lower(), \
            f"Expected locked out message, got: {error}"
        # error.lower() converts to lowercase first.
        # Why? So "Locked Out" and "locked out" both match.
        # 'in' checks if "locked out" appears anywhere in the string.
        # f"..." lets us print the actual error in the failure message.
        # If it fails, we see exactly what the page said instead.

    def test_invalid_password(self, driver):
        page = LoginPage(driver)
        page.open()
        page.login("standard_user", "wrong_password")

        error = page.get_error_message()

        assert "Username and password do not match" in error, \
            f"Expected mismatch message, got: {error}"

    def test_empty_username(self, driver):
        page = LoginPage(driver)
        page.open()
        page.login("", "secret_sauce")
        # "" is an empty string — no username entered.
        # send_keys("") types nothing into the field.

        error = page.get_error_message()

        assert "Username is required" in error, \
            f"Expected username required message, got: {error}"

    def test_empty_password(self, driver):
        page = LoginPage(driver)
        page.open()
        page.login("standard_user", "")

        error = page.get_error_message()

        assert "Password is required" in error, \
            f"Expected password required message, got: {error}"
