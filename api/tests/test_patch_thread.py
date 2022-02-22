import pytest
from django.test import Client

client: Client = Client()


@pytest.mark.django_db
class TestPatchThread:
    """Tests POST /api/v1/thread"""

    pytestmark = pytest.mark.django_db

    def test_patch_non_existent(self):
        r_1 = client.patch(
            "/api/v1/thread/12345",
            data={"generic_topic": "Test"},
            content_type="application/json",
        )
        assert r_1.status_code == 404
