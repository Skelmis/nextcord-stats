import pytest
from django.test import Client

from api.models import Thread, ThreadMessage
from api.tests import get_aware_time

client: Client = Client()


@pytest.mark.django_db
class TestGetThread:
    """Tests GET /api/v1/thread"""

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

    def test_non_existent(self):
        r_1 = client.get("/api/v1/thread/12345")
        assert r_1.status_code == 404

    def test_existent(self):
        t = self.make_thread()

        r_1 = client.get("/api/v1/thread/123")
        assert r_1.status_code == 200

        data: dict = r_1.json()
        assert t.thread_id == data["thread_id"]
        assert t.opened_by == data["opened_by"]
        assert len(data["messages"]) == 1
