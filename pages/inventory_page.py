from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    # STEP 1: URL
    URL = "https://www.saucedemo.com/inventory.html"

    PRODUCT_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[text()='Add to cart']")
    SHOPPING_CART = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_page_to_load(self):
        self.wait.until(
            EC.visibility_of_element_located(
                self.PRODUCT_TITLE))

    def get_title(self):
        return self.driver.find_element(*self.PRODUCT_TITLE).text

    def get_inventory_items(self):
        return self.driver.find_elements(*self.INVENTORY_ITEMS)

    def get_cart_count(self):
        cart_badge = self.driver.find_elements(*self.CART_BADGE)
        if cart_badge:
            return int(cart_badge[0].text)
        else:
            return 0

    def is_on_inventory_page(self):
        elements = self.driver.find_elements(*self.PRODUCT_TITLE)
        return len(elements) > 0 and elements[0].text == "Products"

    def add_first_item_to_cart(self):
        self.wait.until(
            EC.element_to_be_clickable(
                self.ADD_TO_CART_BUTTON)).click()
        # return add_to_cart_buttons[0].text

    def logout(self):
        self.driver.find_element(*self.BURGER_MENU).click()
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK)).click()
