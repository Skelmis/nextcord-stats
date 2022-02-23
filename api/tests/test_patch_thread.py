import pytest
from django.test import Client

from api.models import Thread, ThreadMessage
from api.tests import get_aware_time

client: Client = Client()


@pytest.mark.django_db
class TestPatchThread:
    """Tests PATCH /api/v1/thread/{thread_id}"""

    pytestmark = pytest.mark.django_db

    @staticmethod
    def make_thread() -> Thread:
        t = Thread.objects.create(
            thread_id=123,
            time_opened=get_aware_time(),
            opened_by=456,
        )
        t.save()
        ThreadMessage.objects.create(
            thread=t,
            message_id=1,
            author_id=456,
            time_sent=get_aware_time(),
        ).save()
        return t

    def test_patch_non_existent(self):
        r_1 = client.patch(
            "/api/v1/thread/12345",
            data={"generic_topic": "Test"},
            content_type="application/json",
        )
        assert r_1.status_code == 404

    def test_patch_no_fields(self):
        self.make_thread()

        # Error due to content type set but no data
        r_1 = client.patch(
            "/api/v1/thread/123",
            content_type="application/json",
        )
        assert r_1.status_code == 422

        r_2 = client.patch(
            "/api/v1/thread/123",
            data={},
            content_type="application/json",
        )
        assert r_2.status_code == 400

    def test_patch(self):
        t = self.make_thread()

        # Tests
        r_1 = client.patch(
            "/api/v1/thread/123",
            data={"generic_topic": "Test"},
            content_type="application/json",
        )
        assert r_1.status_code == 200
        assert t.generic_topic != "Test"
        assert r_1.json()["generic_topic"] == "Test"

        t.refresh_from_db()
        assert t.generic_topic == "Test"
