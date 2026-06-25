from selenium.webdriver.common.by import By

# By is how you tell Selenium WHICH type of locator you're using.
# By.ID means find by the HTML id attribute.
# By.CSS_SELECTOR means find by CSS selector.
# By.XPATH means find by XML path.
# We'll use all three — each for a different reason.


class LoginPage:
    # This is a Python class. Think of it as a blueprint.
    # Every time a test needs to work with the login page,
    # it creates one instance of this class and uses it.

    # STEP 1: THE URL
    URL = "https://www.saucedemo.com/"
    # A class-level constant. We define URL once here.
    # If the URL ever changes, we update ONE line.

    # STEP 2: LOCATORS
    # Locators are the ADDRESSES of elements on the page.
    # We store them as tuples at the top of the class,
    # NOT inside methods. Why? So if an ID changes,
    # you update it in one place, not inside every method.

    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    PRODUCTS_TITLE = (By.CLASS_NAME, "title")
    # Why By.ID for the first three?
    # ID is the fastest and most reliable locator.
    # Every HTML element can have only ONE id on a page.
    # So By.ID "user-name" will always find exactly one element.

    # Why By.CSS_SELECTOR for error message?
    # The error element has no id. But it has a data-test attribute.
    # data-test attributes are added BY developers FOR testers.
    # They never change for styling. Very stable locator.

    # Why By.CLASS_NAME for products title?
    # The title element uses a class. CLASS_NAME is the
    # cleanest way to target it here.

    # ── STEP 3: Constructor ───────────────────────────
    def __init__(self, driver):
        self.driver = driver
        # __init__ runs when you create a LoginPage object.
        # It receives the driver (Chrome browser) and stores it.
        # self.driver means "this object's driver".
        # Every method below will use self.driver to control Chrome.

    # ── STEP 4: Actions ──────────────────────────────
    # Actions are WHAT YOU CAN DO on this page.
    # Each action is one small, focused method.
    # They never assert. They never decide pass/fail.
    # They just do the action and return.
    def open(self):
        self.driver.get(self.URL)
        # get() = open a URL in the browser

    def enter_username(self, username):
        field = self.driver.find_element(*self.USERNAME_FIELD)
        # find_element(*self.USERNAME_FIELD) unpacks the tuple.
        # (By.ID, "user-name") becomes find_element(By.ID, "user-name")
        # The * is the unpacking operator. Without it you'd get an error.
        field.clear()
        # clear() wipes any existing text first.
        # Without this, if a field has default text, your
        # username gets appended to it, not replacing it.
        field.send_keys(username)
        # send_keys() types the text into the field.

    def enter_password(self, password):
        field = self.driver.find_element(*self.PASSWORD_FIELD)
        field.clear()
        field.send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def login(self, username, password):
        # This is a convenience method.
        # Instead of calling three methods separately,
        # tests can call just this one.
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ── STEP 5: State readers ─────────────────────────
    # These methods READ what's on the page.
    # Tests use these to know WHAT to assert.
    def get_error_message(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text

    def is_login_successful(self):
        elements = self.driver.find_elements(*self.PRODUCTS_TITLE)
        # find_elements (plural) returns a LIST.
        # If the element doesn't exist, it returns empty list [].
        # find_element (singular) would throw an exception instead.
        # We use plural here so we can safely check length.
        return len(elements) > 0 and elements[0].text == "Products"
     # Returns True only if:
        # 1. The title element exists on the page, AND
        # 2. Its text is exactly "Products"
        # This is how we confirm login succeeded.
