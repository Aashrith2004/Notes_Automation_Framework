"""
tests/ui/test_notes_ui.py

UI test for Add Note functionality.
"""

import time
import allure
import pytest

from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import config


@allure.epic("Notes App Automation")
@allure.feature("Notes Management")
class TestNotesUI:

    @allure.feature("Notes - UI")
    @allure.story("Create Note With Categories")
    class TestCreateNoteCategories:


        @pytest.mark.parametrize(
            "category,description_prefix,scenario_id",
            [
                ("Home", "Home category note", "SC-007"),
                ("Work", "Work category note", "SC-008"),
                ("Personal", "Personal category note", "SC-009"),
            ]
        )
        @allure.title(
            "Verify note creation with {category} category"
        )
        def test_create_note_by_category(
            self,
            driver,
            category,
            description_prefix,
            scenario_id,
        ):
            """
            Verify note can be created
            with different categories.
            """

            login_page = LoginPage(driver)

            login_page.login(
                config.credentials.email,
                config.credentials.password,
            )

            notes_page = NotesPage(driver)

            note_title = (
                f"{category} Note {int(time.time())}"
            )

            notes_page.create_note(
                note_title,
                description_prefix,
                category=category,
            )

            assert notes_page.is_note_present(
                note_title
            ), (
                f"{scenario_id}: "
                f"Note creation failed for "
                f"{category} category"
            )
    
    
    def test_create_note_empty_title(
    self,
    driver,
):
        """
        SC-012:
        Verify validation appears
        when title is empty.
        """

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        notes_page = NotesPage(driver)

        notes_page.click_add_note()

        notes_page.enter_description(
            "Description without title"
        )

        notes_page.select_category("Home")

        notes_page.click_save()

        assert (
            notes_page.is_title_required_error_displayed()
        ), (
            "Title required validation "
            "message not displayed"
        )
    
    def test_create_note_empty_description(
    self,
    driver,
):
        """
        SC-013:
        Verify validation appears
        when description is empty.
        """

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        notes_page = NotesPage(driver)

        note_title = (
            f"No Description {int(time.time())}"
        )

        notes_page.click_add_note()

        notes_page.enter_title(
            note_title
        )

        notes_page.select_category("Home")

        notes_page.click_save()

        assert (
            notes_page.is_description_required_error_displayed()
        ), (
            "Description required validation "
            "message not displayed"
        )
    @pytest.mark.empty
    def test_create_and_delete_note(
    self,
    driver,
    ):
        """
        SC-014:
        Verify created note
        can be deleted successfully.
        """

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        notes_page = NotesPage(driver)

        note_title = (
            f"Delete Note {int(time.time())}"
        )

        # Create note
        notes_page.create_note(
            note_title,
            "Delete note validation",
            category="Home",
        )

        # Verify note created
        assert notes_page.is_note_present(
            note_title
        )

        # Delete note
        notes_page.delete_note()

        # Confirm delete
        notes_page.confirm_delete()

        # Verify note removed
        assert notes_page.wait_for_note_gone(
            note_title
        ), (
            f"Note '{note_title}' "
            "still visible after deletion"
        )