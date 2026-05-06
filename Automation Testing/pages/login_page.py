"""
pages/login_page.py

Page Object for the ExpandTesting Notes login page.
"""

import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from config.environment import config
from utils.logger import get_logger
from utils.self_healing_locator import (
    find_element_with_fallback,
)

logger = get_logger(__name__)


class LoginPage(BasePage):
    """
    Encapsulates all interactions with Login page.
    """

    # ──────────────────────────────────────────────────────────────────────────
    # URL
    # ──────────────────────────────────────────────────────────────────────────

    URL = config.app.ui_base_url

    # ──────────────────────────────────────────────────────────────────────────
    # Locators
    # ──────────────────────────────────────────────────────────────────────────

    _LANDING_LOGIN_BUTTON = [
        (
            By.CSS_SELECTOR,
            "a[href='/notes/app/login']",
        ),
        (
            By.XPATH,
            "//a[contains(text(),'Login')]",
        ),
    ]

    _EMAIL_INPUT = [
        (By.ID, "email"),
        (By.CSS_SELECTOR, "input[type='email']"),
        (
            By.XPATH,
            "//input[@placeholder='Email address']",
        ),
    ]

    _PASSWORD_INPUT = [
        (By.ID, "password"),
        (By.CSS_SELECTOR, "input[type='password']"),
        (
            By.XPATH,
            "//input[@placeholder='Password']",
        ),
    ]

    _LOGIN_BUTTON = [
        (
            By.CSS_SELECTOR,
            "button[type='submit']",
        ),
        (
            By.XPATH,
            "//button[normalize-space()='Login']",
        ),
    ]
    _HOME_LOGO = (
    By.CSS_SELECTOR,
    "a[data-testid='home']"
    )
    _ERROR_ALERT = (
        By.CSS_SELECTOR,
        "div[data-testid='alert-message']",
    )

    # ──────────────────────────────────────────────────────────────────────────
    # Constructor
    # ──────────────────────────────────────────────────────────────────────────

    def __init__(self, driver: WebDriver):

        super().__init__(driver)

    # ──────────────────────────────────────────────────────────────────────────
    # Actions
    # ──────────────────────────────────────────────────────────────────────────

    @allure.step("Open Login page")
    def open_login_page(self) -> None:
        """
        Opens Notes application
        and navigates to Login page.
        """

        self.open(self.URL)

        logger.info(
            "Application landing page opened"
        )

        find_element_with_fallback(
            self.driver,
            self._LANDING_LOGIN_BUTTON,
        ).click()

        logger.info(
            "Landing page Login button clicked"
        )

    @allure.step("Enter email")
    def enter_email(self, email: str) -> None:
        """
        Enters email.
        """

        element = find_element_with_fallback(
            self.driver,
            self._EMAIL_INPUT,
        )

        element.clear()

        element.send_keys(email)

        logger.info(f"Email entered: {email}")

    @allure.step("Enter password")
    def enter_password(self, password: str) -> None:
        """
        Enters password.
        """

        element = find_element_with_fallback(
            self.driver,
            self._PASSWORD_INPUT,
        )

        element.clear()

        element.send_keys(password)

        logger.info("Password entered")

    @allure.step("Click Login button")
    def click_login(self) -> None:
        """
        Click Login button with fallback.
        """

        button = find_element_with_fallback(
            self.driver,
            self._LOGIN_BUTTON,
        )

        try:
            button.click()

        except Exception:

            logger.warning(
                "Login click intercepted. "
                "Using JS fallback."
            )

            self.driver.execute_script(
                "arguments[0].click();",
                button,
            )

        logger.info("Login button clicked")

    @allure.step("Perform login")
    def login(
        self,
        email: str,
        password: str,
    ) -> None:
        """
        Performs complete login flow.
        """

        self.open_login_page()

        self.enter_email(email)

        self.enter_password(password)

        self.click_login()

        logger.info(
            f"Login submitted for user: {email}"
        )

    def login_with_defaults(self) -> None:
        """
        Login using config credentials.
        """

        self.login(
            config.credentials.email,
            config.credentials.password,
        )

    # ──────────────────────────────────────────────────────────────────────────
    # Validations
    # ──────────────────────────────────────────────────────────────────────────

    def get_error_message(self) -> str:
        """
        Returns login error message.
        """

        if self.is_visible(
            self._ERROR_ALERT,
            timeout=5,
        ):
            return self.get_text(
                self._ERROR_ALERT
            )

        return ""

    def is_login_error_displayed(self) -> bool:
        """
        Checks if login error appears.
        """

        return self.is_visible(
            self._ERROR_ALERT,
            timeout=5,
        )

    def is_logged_in(self) -> bool:
        """
        Checks successful login.
        """

        return (
            "/notes/app" in self.get_current_url()
        )
    def is_home_page_displayed(self) -> bool:
        """
        Verifies successful login by checking
        MyNotes home/navbar element.
        """

        return self.is_visible(
            self._HOME_LOGO,
            timeout=10,
        )