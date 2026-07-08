import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture()
def driver():
    # SETUP
    options = webdriver.ChromeOptions()
    # These 4 options are required for Docker
    # --headless     = no visible browser window (Docker has no screen)
    # --no-sandbox   = required for Chrome inside Linux containers
    # --disable-dev-shm-usage = prevents Chrome crashes in Docker
    # --disable-gpu  = no GPU needed in headless mode
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # Set window size via options — works in both headless and normal mode
    # maximize_window() crashes in headless mode so we avoid it
    options.add_argument("--window-size=1920,1080")

    # os.environ.get("DOCKER") checks if we are running inside Docker
    # In Dockerfile we set ENV DOCKER=true
    # Locally this variable does not exist so it returns None

    if os.environ.get("DOCKER"):
        # Inside Docker — chromedriver is already installed at /usr/bin/chromedriver
        # We do not need webdriver-manager here
        # options.add_argument("--headless=new")
        # options.add_argument("--remote-debugging-port=9222")
        # options.binary_location = "/usr/bin/chromium"
        # service = Service("/usr/bin/chromedriver")
        # from selenium.webdriver.remote.webdriver import WebDriver as RemoteDriver
        hub_url = os.environ.get(
            "SELENIUM_HUB_URL", "http://chrome:4444/wd/hub")
        driver = webdriver.Remote(command_executor=hub_url, options=options)
        driver.set_page_load_timeout(60)

    else:
        # ChromeOptions = a configuration object for Chrome.
        # We add nothing to it now. Later we will add --headless
        # so Docker can run Chrome without a visible screen.
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options)

    # Maximize the window and set an implicit wait time of 10 seconds
    # driver.maximize_window()
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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            os.makedirs("reports/screenshots", exist_ok=True)
            screenshot_path = f"reports/screenshots/{item.name}.png"
            driver.save_screenshot(screenshot_path)
            print(f"\nScreenshot saved: {screenshot_path}")
