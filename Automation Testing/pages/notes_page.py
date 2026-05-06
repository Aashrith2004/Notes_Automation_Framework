"""
pages/notes_page.py

Page Object for Notes Dashboard functionality.

Covers:
- Create note
- Validate note visibility
- Read note list
- Refresh notes page
"""

import time
import allure
import time
import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utils.logger import get_logger
from utils.self_healing_locator import (
    find_element_with_fallback,
)

logger = get_logger(__name__)


class NotesPage(BasePage):
    """
    Notes dashboard page object.
    """

    # ──────────────────────────────────────────────────────────────────────────
    # Locators
    # ──────────────────────────────────────────────────────────────────────────

    _ADD_NOTE_BUTTON = [
    (
        By.CSS_SELECTOR,
        "button[data-testid='add-new-note']",
    ),
    (
        By.XPATH,
        "//button[@data-testid='add-new-note']",
    ),
    ]

    _TITLE_INPUT = [
        (
            By.ID,
            "title",
        ),
        (
            By.CSS_SELECTOR,
            "input[name='title']",
        ),
    ]

    _DESCRIPTION_INPUT = [
        (
            By.ID,
            "description",
        ),
        (
            By.CSS_SELECTOR,
            "textarea[name='description']",
        ),
    ]

    _CATEGORY_DROPDOWN = [
        (
            By.ID,
            "category",
        ),
    ]

    _SAVE_BUTTON = [
        (
            By.XPATH,
            "//button[contains(text(),'Create')]",
        ),

    ]

    _NOTE_TITLES = (
    By.CSS_SELECTOR,
    "[data-testid='note-card-title']",
    )

    _EDIT_BUTTON = (
    By.CSS_SELECTOR,
    "[data-testid='note-edit']"
)

    _TITLE_REQUIRED_ERROR = (
        By.XPATH,
        "//div[contains(text(),'Title is required')]"
)
    _DESCRIPTION_REQUIRED_ERROR = (
    By.XPATH,
    "//div[contains(text(),'Description is required')]"
)

    # ──────────────────────────────────────────────────────────────────────────
    # Constructor
    # ──────────────────────────────────────────────────────────────────────────

    def __init__(self, driver: WebDriver):

        super().__init__(driver)

    # ──────────────────────────────────────────────────────────────────────────
    # Actions
    # ──────────────────────────────────────────────────────────────────────────

    @allure.step("Click Add Note button")
    def click_add_note(self) -> None:
        """
        Wait for Add Note button then click.
        """

        locator = (
            By.CSS_SELECTOR,
            "button[data-testid='add-new-note']"
        )

        button = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.element_to_be_clickable(locator)
        )

        try:
            button.click()
        except Exception:
            self.driver.execute_script(
                "arguments[0].click();",
                button,
            )

    @allure.step("Enter note title")
    def enter_title(self, title: str) -> None:
        """
        Enters note title.
        """

        element = find_element_with_fallback(
            self.driver,
            self._TITLE_INPUT,
        )

        element.clear()

        element.send_keys(title)

        logger.info(f"Title entered: {title}")

    @allure.step("Enter note description")
    def enter_description(
        self,
        description: str,
    ) -> None:
        """
        Enters note description.
        """

        element = find_element_with_fallback(
            self.driver,
            self._DESCRIPTION_INPUT,
        )

        element.clear()

        element.send_keys(description)

        logger.info("Description entered")

    @allure.step("Select note category")
    def select_category(
        self,
        category: str,
    ) -> None:
        """
        Selects category from dropdown.
        """

        dropdown = find_element_with_fallback(
            self.driver,
            self._CATEGORY_DROPDOWN,
        )

        dropdown.send_keys(category)

        logger.info(
            f"Category selected: {category}"
        )

    @allure.step("Click Save button")
    def click_save(self) -> None:
        """
        Saves note.
        """

        button = find_element_with_fallback(
            self.driver,
            self._SAVE_BUTTON,
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            button,
        )

        time.sleep(1)

        try:

            button.click()

        except Exception:

            self.driver.execute_script(
                "arguments[0].click();",
                button,
            )

        logger.info("Save/Create button clicked")

    @allure.step("Create new note")
    def create_note(
        self,
        title: str,
        description: str,
        category: str = "Home",
    ) -> None:
        """
        Creates complete note.
        """

        self.click_add_note()

        self.enter_title(title)

        self.enter_description(description)

        self.select_category(category)

        self.click_save()

        logger.info(
            f"Note created: {title}"
        )

    # ──────────────────────────────────────────────────────────────────────────
    # Validations
    # ──────────────────────────────────────────────────────────────────────────

    def get_note_titles(self):
        """
        Returns all note titles.
        """

        elements = self.driver.find_elements(
            *self._NOTE_TITLES
        )

        return [
            element.text
            for element in elements
        ]

    def is_note_present(
        self,
        title: str,
        timeout: int = 10,
    ) -> bool:
        """
        Wait until created note appears in UI.
        """

        end_time = time.time() + timeout

        while time.time() < end_time:

            titles = self.get_note_titles()

            if title in titles:
                return True

            time.sleep(1)

        return False

    def is_success_alert_displayed(
        self,
    ) -> bool:
        """
        Checks success banner visibility.
        """

        return self.is_visible(
            self._SUCCESS_ALERT,
            timeout=5,
        )

    def refresh_notes_page(self) -> None:
        """
        Refreshes notes dashboard.
        """

        self.driver.refresh()

        logger.info("Notes page refreshed")

    def is_title_required_error_displayed(
    self,
) -> bool:
        """
        Checks whether title required
        validation message is shown.
        """

        return self.is_visible(
            self._TITLE_REQUIRED_ERROR,
            timeout=5,
        )
    def is_description_required_error_displayed(
    self,
) -> bool:
        """
        Checks whether description required
        validation message is displayed.
        """

        return self.is_visible(
            self._DESCRIPTION_REQUIRED_ERROR,
            timeout=5,
        )

    @allure.step("Wait for note visible")
    def wait_for_note_visible(
        self,
        title: str,
        timeout: int = 10,
    ):

        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((
                By.XPATH,
                f"//*[text()='{title}']"
            ))
        )

    @allure.step("Delete note")
    def delete_note(self):

        delete_btn = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                "[data-testid='note-delete']"
            ))
        )

        self.driver.execute_script(
        "arguments[0].click();",
        delete_btn
    )
    @allure.step("Confirm delete")
    def confirm_delete(self):

        confirm_btn = WebDriverWait(
            self.driver,
            5
        ).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR,
                "[data-testid='note-delete-confirm']"
            ))
        )

        self.driver.execute_script(
            "arguments[0].click();",
            confirm_btn
        )

    @allure.step("Wait for note removed")
    def wait_for_note_gone(
        self,
        title: str,
        timeout: int = 10,
    ):

        return WebDriverWait(
            self.driver,
            timeout
        ).until(
            EC.invisibility_of_element_located((
                By.XPATH,
                f"//*[text()='{title}']"
            ))
        )
