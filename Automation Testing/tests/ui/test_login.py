"""
tests/ui/test_login.py

UI test cases for Login functionality.
"""

import allure

from pages.login_page import LoginPage
from config.environment import config
from utils.wait_utils import (
    wait_for_url_contains,
)


@allure.epic("Notes App Automation")
@allure.feature("UI Authentication")
class TestLogin:
    """
    Login test suite.
    """

    @allure.story("Successful Login")
    @allure.title(
        "TC-UI-01: Valid login redirects user to dashboard"
    )
    @allure.severity(
        allure.severity_level.BLOCKER
    )
    def test_valid_login_redirects_to_dashboard(
        self,
        driver,
    ):
        """
        Verify valid login works successfully.
        """

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        wait_for_url_contains(
            driver,
            "/notes/app",
            timeout=15,
        )

        assert (login_page.is_home_page_displayed()), ("Home page was not displayed after successful login")

    @allure.story("Negative Login")
    @allure.title(
        "TC-NEG-01: Invalid password shows error"
    )
    def test_invalid_password_shows_error(
        self,
        driver,
    ):
        """
        Verify invalid password shows error.
        """

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            "WrongPassword123!",
        )

        assert (
            login_page.is_login_error_displayed()
        ), (
            "Expected login error message "
            "for invalid password"
        )

    @allure.story("Negative Login")
    @allure.title(
        "TC-NEG-02: Invalid email format"
    )
    def test_invalid_email_format(
        self,
        driver,
    ):
        """
        Verify malformed email is rejected.
        """

        login_page = LoginPage(driver)

        login_page.login(
            "invalid-email",
            config.credentials.password,
        )

        assert (
            login_page.is_login_error_displayed()
            or "login" in driver.current_url
        )