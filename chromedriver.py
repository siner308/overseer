from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from config import CHROME_DRIVER_PATH


def setup_chrome() -> WebDriver:
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("headless")
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, chrome_options=chrome_options)
    return driver
