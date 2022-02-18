import os

from ninja.security import APIKeyHeader


class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        if key == os.environ["API_KEY_HEADER"]:
            return True

        return False
