from typing import List

import orjson
from django.core.exceptions import BadRequest, ValidationError
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.parser import Parser
from ninja.renderers import BaseRenderer

from api.auth import ApiKey
from api.exceptions import (
    AlreadyExists,
    Forbidden,
    MissingPatchData,
    ResourceDoesntExist,
)
from api.models import Thread
from api.schema import (
    ThreadCreateSchema,
    ThreadOutSchema,
    ThreadMessageSchema,
    ThreadPatchSchema,
    Message,
)


class ORJSONParser(Parser):
    def parse_body(self, request):
        return orjson.loads(request.body)


class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data)


api = NinjaAPI(
    auth=ApiKey(),
    parser=ORJSONParser(),
    renderer=ORJSONRenderer(),
    title="Nextcord Help Thread Statistics API",
)

handled_4xx_codes = frozenset({401, 409})


@api.exception_handler(AlreadyExists)
def already_exists(request, exc):
    return api.create_response(request, {"message": str(exc)}, status=409)


@api.exception_handler(Forbidden)
def handle_forbidden(request, exc):
    return api.create_response(request, {"message": str(exc)}, status=401)


@api.exception_handler(MissingPatchData)
def handle_missing_patch_data(request, exc):
    return api.create_response(request, {"message": str(exc)}, status=400)


@api.exception_handler(ResourceDoesntExist)
def handle_missing_resource(request, exc):
    return api.create_response(request, {"message": str(exc)}, status=404)


@api.exception_handler(ValidationError)
def handle_validation_error(request, exc):
    return api.create_response(request, {"message": str(exec)}, status=400)


@api.post(
    "thread",
    tags=["Threads"],
    summary="Create a new Thread entry.",
    description="Creates a new thread entry in the database for future usage.",
    response={201: ThreadOutSchema, handled_4xx_codes: Message},
)
def create_new_thread(request: HttpRequest, new_thread: ThreadCreateSchema):
    thread = Thread.objects.create(
        thread_id=new_thread.thread_id,
        time_opened=new_thread.time_opened,
        opened_by=new_thread.opened_by,
        generic_topic=new_thread.generic_topic if new_thread.generic_topic else "",
    )
    thread.full_clean()
    thread.save()

    return 201, thread.as_schema()


@api.get(
    "thread",
    tags=["Threads"],
    summary="Get all Threads.",
    description="Retrieve all the information for all threads.",
    response={200: List[ThreadOutSchema], 401: Message, 404: Message},
)
def list_threads(request: HttpRequest):
    return BadRequest


@api.get(
    "thread/{thread_id}",
    tags=["Threads"],
    summary="Get a specific Thread.",
    description="Retrieve info for a specific thread.",
    response={200: ThreadOutSchema, 401: Message, 404: Message},
)
def retrieve_thread(request: HttpRequest, thread_id: int):
    raise BadRequest


@api.patch(
    "thread/{thread_id}",
    tags=["Threads"],
    summary="Update the given thread.",
    description="Update one of the three possible fields for a thread.",
    response={200: ThreadOutSchema, 400: Message, 401: Message, 404: Message},
)
def patch_thread(request: HttpRequest, thread_id: int, patch_data: ThreadPatchSchema):
    raise BadRequest


@api.post(
    "thread/{thread_id}/messages",
    tags=["Threads"],
    summary="Add a message to a Thread.",
    description="Adds the given message to the associated thread.",
    response={201: List[ThreadMessageSchema], handled_4xx_codes: Message},
)
def create_thread_message(
    request: HttpRequest, thread_id: int, message: ThreadMessageSchema
):
    raise BadRequest


@api.get(
    "thread/{thread_id}/messages",
    tags=["Threads"],
    summary="Get Thread messages.",
    description="Retrieve all the messages for this thread.",
    response={200: List[ThreadMessageSchema], 401: Message, 404: Message},
)
def list_thread_messages(request: HttpRequest, thread_id: int):
    raise BadRequest


@api.get(
    "thread/{thread_id}/messages/{message_id}",
    tags=["Threads"],
    summary="Get a specific Thread message.",
    description="Retrieve a specific message from a thread.",
    response={200: ThreadMessageSchema, 401: Message, 404: Message},
)
def list_thread_messages(request: HttpRequest, thread_id: int, message_id: int):
    raise BadRequest
