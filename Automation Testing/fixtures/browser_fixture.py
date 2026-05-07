"""
fixtures/browser_fixture.py
"""

from selenium import webdriver
from selenium.webdriver.remote.webdriver import (
    WebDriver
)

from config.environment import config
from utils.logger import get_logger

logger = get_logger(__name__)


def create_driver(
    browser_name: str = "chrome"
) -> WebDriver:
    """
    Create Chrome WebDriver.
    """

    logger.info(
        f"Launching browser: {browser_name}"
    )

    options = webdriver.ChromeOptions()

    # Headless mode
    if config.browser.headless:
        options.add_argument(
            "--headless=new"
        )

    # Jenkins/Docker stability
    options.add_argument(
        "--window-size=1920,1080"
    )

    options.add_argument(
        "--disable-dev-shm-usage"
    )

    options.add_argument(
        "--no-sandbox"
    )

    options.add_argument(
        "--disable-gpu"
    )

    options.add_argument(
        "--disable-notifications"
    )

    options.add_argument(
        "--disable-popup-blocking"
    )

    driver = webdriver.Chrome(
        options=options
    )

    driver.maximize_window()

    logger.info(
        "Browser launched successfully"
    )

    return driver


def quit_driver(
    driver: WebDriver
) -> None:
    """
    Close browser safely.
    """

    if driver:

        logger.info(
            "Closing browser"
        )

        try:
            driver.quit()

        except Exception as e:

            logger.error(
                f"Error closing browser: {e}"
            )
