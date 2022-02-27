import pytest
from django.test import Client

from api.models import InitThread

client: Client = Client()


@pytest.mark.django_db
class TestDeleteInitThread:
    """Tests DELETE /api/v1/thread/partial/{thread_id}"""

    pytestmark = pytest.mark.django_db

    def test_delete_non_existent(self):
        r_1 = client.delete(
            "/api/v1/thread/partial/12345",
        )
        assert r_1.status_code == 200

    def test_delete_existent(self):
        InitThread.objects.create(thread_id=1, help_type="Hi").save()

        assert InitThread.objects.exists()

        r_1 = client.delete(
            "/api/v1/thread/partial/1",
        )
        assert r_1.status_code == 200

        assert not InitThread.objects.exists()
