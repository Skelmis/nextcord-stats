import pytest
from django.test import Client

from api.models import InitThread

client: Client = Client()


@pytest.mark.django_db
class TestInitThread:
    """Tests POST /api/v1/thread/partial"""

    pytestmark = pytest.mark.django_db

    def test_creates(self):
        assert not InitThread.objects.exists()

        r_1 = client.post(
            "/api/v1/thread/partial",
            data={"thread_id": 1, "help_type": "Test"},
            content_type="application/json",
        )

        assert r_1.status_code == 201
        assert InitThread.objects.exists()
