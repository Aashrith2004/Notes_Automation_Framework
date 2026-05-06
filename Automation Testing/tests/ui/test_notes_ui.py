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

    def test_create_note_home_category(
    self,
    driver,
):
        """
        SC-007:
        Verify note can be created
        with Home category.
        """

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        notes_page = NotesPage(driver)

        note_title = (
            f"Home Note {int(time.time())}"
        )

        notes_page.create_note(
            note_title,
            "Home category note",
            category="Home",
        )

        assert notes_page.is_note_present(
            note_title
        )

    def test_create_note_work_category(
    self,
    driver,
):
        """
        SC-008:
        Verify note can be created
        with Work category.
        """

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        notes_page = NotesPage(driver)

        note_title = (
            f"Work Note {int(time.time())}"
        )

        notes_page.create_note(
            note_title,
            "Work category note",
            category="Work",
        )

        assert notes_page.is_note_present(
            note_title
        )

    def test_create_note_personal_category(
    self,
    driver,
):
        """
        SC-009:
        Verify note can be created
        with Personal category.
        """

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        notes_page = NotesPage(driver)

        note_title = (
            f"Personal Note {int(time.time())}"
        )

        notes_page.create_note(
            note_title,
            "Personal category note",
            category="Personal",
        )

        assert notes_page.is_note_present(
            note_title
        )
    
    def test_success_banner_after_note_creation(
    self,
    driver,
):
        """
        SC-010:
        Verify success banner/message
        appears after creating a note.
        """

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        notes_page = NotesPage(driver)

        note_title = (
            f"Banner Test {int(time.time())}"
        )

        notes_page.create_note(
            note_title,
            "Success banner validation",
        )

        assert (
            notes_page.is_success_alert_displayed()
        ), (
            "Success banner not displayed "
            "after note creation"
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