"""
fixtures/browser_fixture.py

Browser factory utilities for Selenium WebDriver creation and teardown.

Responsibilities:
- Create browser instances
- Configure browser options
- Provide reusable driver lifecycle helpers
"""

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from config.environment import config
from utils.logger import get_logger

logger = get_logger(__name__)


def create_driver(browser_name: str = "chrome") -> WebDriver:
    """
    Creates and returns a Selenium WebDriver instance.

    Args:
        browser_name: Browser to launch (currently supports Chrome).

    Returns:
        Selenium WebDriver instance.
    """

    logger.info(f"Launching browser: {browser_name}")

    options = webdriver.ChromeOptions()

    if config.browser.headless:
        options.add_argument("--headless=new")

    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    logger.info("Browser launched successfully")

    return driver


def quit_driver(driver: WebDriver) -> None:
    """
    Safely quits the browser instance.

    Args:
        driver: Selenium WebDriver instance.
    """

    if driver:
        logger.info("Closing browser")
        driver.quit()
