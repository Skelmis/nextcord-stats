import datetime

import pytest
from django.test import Client

client: Client = Client()
headers: dict = {"X-API-Key": "TESTING"}


@pytest.mark.django_db
class TestCreateThread:
    """Tests POST /api/v1/thread"""

    pytestmark = pytest.mark.django_db

    def test_create_full_thread(self):
        thread_data = returned_check = {
            "thread_id": 12345,
            "time_opened": datetime.datetime.utcnow(),
            "opened_by": 67890,
            "generic_topic": "A topic",
            "initial_message": {
                "thread_id": 12345,
                "message_id": 123,
                "author_id": 67890,
                "time_sent": datetime.datetime.utcnow(),
                "is_helper": False,
            },
        }

        r_1 = client.post(
            "/api/v1/thread",
            data=thread_data,
            headers=headers,
            content_type="application/json",
        )
        assert r_1.status_code == 201

        returned_check["closed_by"] = None
        returned_check["time_closed"] = None
        returned_check["specific_topic"] = ""
        returned_check.pop("time_opened")
        returned_check["messages"] = [returned_check.pop("initial_message")]
        returned_check["messages"][0].pop("time_sent")

        returned_json: dict = r_1.json()
        assert "time_opened" in returned_json
        returned_json.pop("time_opened")

        assert len(returned_json["messages"]) == 1
        assert "time_sent" in returned_json["messages"][0]
        returned_json["messages"][0].pop("time_sent")

        assert returned_json == thread_data
