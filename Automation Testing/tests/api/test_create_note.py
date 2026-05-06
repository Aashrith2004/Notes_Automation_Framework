import time
import allure

from api.auth_api import AuthAPI
from api.notes_api import NotesAPI
from config.environment import config


@allure.feature("Notes API")
@allure.story("Create Note API")
class TestCreateNoteAPI:

    @allure.title(
        "TC-API-03 | Verify Create Note API"
    )
    def test_create_note_api(self):

        auth_api = AuthAPI()

        token = auth_api.get_token(
            config.credentials.email,
            config.credentials.password,
        )

        notes_api = NotesAPI()

        note_title = (
            f"API Note {int(time.time())}"
        )

        response = notes_api.create_note(
            token=token,
            title=note_title,
            description="Created via API",
            category="Home",
        )

        # Status validation
        assert response.status_code == 200

        # Performance validation
        response_time = (
            response.elapsed.total_seconds()
        )

        assert response_time < 2, (
            f"Response time exceeded: "
            f"{response_time} seconds"
        )

        response_data = response.json()

        # Functional validations
        assert response_data["success"] is True

        assert (
            response_data["data"]["title"]
            == note_title
        )

        assert (
            response_data["data"]["description"]
            == "Created via API"
        )

        # Attach response time
        allure.attach(
            str(response_time),
            name="Response Time",
            attachment_type=allure.attachment_type.TEXT
        )