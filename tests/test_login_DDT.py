import pytest
from pages.login_page import LoginPage


class TestLoginDDT:
    @pytest.mark.parametrize("username, password, expected",
                             [
                                 ("standard_user", "secret_sauce", "success"),
                                 ("locked_out_user", "secret_sauce",
                                  "Epic sadface: Sorry, this user has been locked out."),
                                 ("standard_user", "secret_lab",
                                  "Epic sadface: Username and password do not match any user in this service"),
                                 ("", "secret_sauce", "Username is required"),
                                 ("standard_user", "", "Password is required"),
                             ])
    def test_login_ddt(self, driver, username, password, expected):
        page = LoginPage(driver)
        page.open()
        page.login(username, password)
        if expected == "success":
            assert page.is_login_successful(), \
                f"Expected success but login failed"
        else:
            error = page.get_error_message()
            assert expected in error, \
                f"Expected '{expected}' in error, but got '{error}' "
