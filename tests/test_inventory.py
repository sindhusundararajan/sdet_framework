import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class TestInventoryPage:

    def test_inventory_page(self, driver):

        login_page = LoginPage(driver)

        login_page.open()

        login_page.login("standard_user", "secret_sauce")

        inventory_page = InventoryPage(driver)

        inventory_items = inventory_page.get_inventory_items()

        actual_count = len(inventory_items)

        assert actual_count == 6, \
            f"Expected 6 inventory items, but found {actual_count}. Items: {[item.text for item in inventory_items]}"

    def test_page_title(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        inventory_page = InventoryPage(driver)
        title = inventory_page.get_title()
        assert title == "Products", \
            f"Expected Title is 'Products', but found {title}"

    def test_add_to_cart(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        inventory_page = InventoryPage(driver)
        inventory_page.add_first_item_to_cart()
        cart_count = inventory_page.get_cart_count()
        assert cart_count == 1, \
            f"Expected Cart value is 1, but found {cart_count}."

    def test_logout(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        inventory_page = InventoryPage(driver)
        inventory_page.logout()
        assert not login_page.is_on_login_page(), \
            f"Logout failed - Login page did not appear"
