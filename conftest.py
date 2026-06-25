import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def driver():
    # SETUP
    options = webdriver.ChromeOptions()

    # ChromeOptions = a configuration object for Chrome.
    # We add nothing to it now. Later we will add --headless
    # so Docker can run Chrome without a visible screen.

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options)

    # ChromeDriverManager().install() downloads the right
    # chromedriver version for your Chrome automatically.
    # No manual download. No version mismatch errors.

    # Maximize the window and set an implicit wait time of 10 seconds
    driver.maximize_window()
    # Full screen so no elements are hidden off-screen.

    driver.implicitly_wait(10)
    # If an element is not found instantly, wait up to
    # 10 seconds before failing. Handles slow page loads.

    # HANDS TO THE TEST FUNCTION
    yield driver
    # Pause here. Give driver to the test. Test runs fully.
    # Then come back here no matter what happened.

    # TEARDOWN
    driver.quit()
    # quit() = close browser window + kill chromedriver process
    # close() = close window only, process keeps running (wrong)
