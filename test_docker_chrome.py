from selenium import webdriver
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--user-data-dir=/tmp/chrome-data")
options.binary_location = "/usr/bin/chromium"
service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)
print("SUCCESS - Chrome started")
driver.quit()
