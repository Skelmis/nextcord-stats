import pytest
from django.test import Client

from api.models import Thread, ThreadMessage
from api.tests import get_aware_time

client: Client = Client()


@pytest.mark.django_db
class TestPostThreadMessages:
    """Tests POST /api/v1/thread/{thread_id}/messages"""

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
        r_1 = client.post(
            "/api/v1/thread/12345/messages",
            data={
                "thread_id": 890,
                "message_id": 456,
                "author_id": 123,
                "time_sent": get_aware_time(),
                "is_helper": False,
            },
            content_type="application/json",
        )
        assert r_1.status_code == 400

    def test_patch_no_data(self):
        r_1 = client.post(
            "/api/v1/thread/12345/messages",
            data={},
            content_type="application/json",
        )
        assert r_1.status_code == 422

    def test_mismatched_ids(self):
        r_1 = client.post(
            "/api/v1/thread/12345/messages",
            data={
                "thread_id": 890,
                "message_id": 456,
                "author_id": 123,
                "time_sent": get_aware_time(),
                "is_helper": False,
            },
            content_type="application/json",
        )
        assert r_1.status_code == 400

    def test_valid(self):
        self.make_thread()
        r_1 = client.post(
            "/api/v1/thread/123/messages",
            data={
                "thread_id": 123,
                "message_id": 456,
                "author_id": 123,
                "time_sent": get_aware_time(),
                "is_helper": False,
            },
            content_type="application/json",
        )
        assert r_1.status_code == 201
