class BaseAPIException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = self.__doc__

    def __str__(self):
        return self.message


class AlreadyExists(BaseAPIException):
    """Cannot create resource, already exists."""


class Forbidden(BaseAPIException):
    """You are not authorised to access this content."""


class MissingPatchData(BaseAPIException):
    """At-least one field is required for PATCH requests."""


class ResourceDoesntExist(BaseAPIException):
    """The requested resource does not exist."""
