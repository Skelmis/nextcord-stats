from typing import List

import orjson
from django.core.exceptions import BadRequest
from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.parser import Parser
from ninja.renderers import BaseRenderer

from api.auth import ApiKey
from api.schema import (
    ThreadCreateSchema,
    ThreadOutSchema,
    ThreadMessageSchema,
    ThreadPatchSchema,
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


@api.post(
    "thread",
    tags=["Threads"],
    summary="Create a new Thread entry.",
    description="Creates a new thread entry in the database for future usage.",
    response={201: ThreadOutSchema},
)
def create_new_thread(request: HttpRequest, new_thread: ThreadCreateSchema):
    raise BadRequest


@api.get(
    "thread",
    tags=["Threads"],
    summary="Get all Threads.",
    description="Retrieve all the information for all threads.",
    response={200: List[ThreadOutSchema]},
)
def list_threads(request: HttpRequest):
    return BadRequest


@api.get(
    "thread/{thread_id}",
    tags=["Threads"],
    summary="Get a specific Thread.",
    description="Retrieve info for a specific thread.",
    response={200: ThreadOutSchema},
)
def retrieve_thread(request: HttpRequest, thread_id: int):
    raise BadRequest


@api.patch(
    "thread/{thread_id}",
    tags=["Threads"],
    summary="Update the given thread.",
    description="Update one of the three possible fields for a thread.",
)
def patch_thread(request: HttpRequest, thread_id: int, patch_data: ThreadPatchSchema):
    raise BadRequest


@api.post(
    "thread/{thread_id}/messages",
    tags=["Threads"],
    summary="Add a message to a Thread.",
    description="Adds the given message to the associated thread.",
    response={201: List[ThreadMessageSchema]},
)
def create_thread_message(request: HttpRequest, message: ThreadMessageSchema):
    raise BadRequest


@api.get(
    "thread/{thread_id}/messages",
    tags=["Threads"],
    summary="Get Thread messages.",
    description="Retrieve all the messages for this thread.",
    response={200: List[ThreadMessageSchema]},
)
def list_thread_messages(request: HttpRequest, thread_id: int):
    raise BadRequest


@api.get(
    "thread/{thread_id}/messages/{message_id}",
    tags=["Threads"],
    summary="Get a specific Thread message.",
    description="Retrieve a specific message from a thread.",
    response={200: ThreadMessageSchema},
)
def list_thread_messages(request: HttpRequest, thread_id: int, message_id: int):
    raise BadRequest
