import logging
import os

from django.conf import settings
from ninja.security import APIKeyHeader

from api.exceptions import Forbidden

log = logging.getLogger(__name__)

auth_key = os.environ.get("API_KEY_HEADER")
if not auth_key:
    if not settings.DEBUG:
        raise KeyError("API_KEY_HEADER")
    else:
        log.warning("Set API_KEY_HEADER to test default.")
        auth_key = None


class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        if key == auth_key:
            return True

        raise Forbidden
