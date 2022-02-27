from typing import List

import orjson
from django.core.exceptions import BadRequest, ValidationError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
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
from api.models import Thread, ThreadMessage, InitThread
from api.schema import (
    ThreadCreateSchema,
    ThreadOutSchema,
    ThreadMessageSchema,
    ThreadPatchSchema,
    Message,
    InitThreadSchema,
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

handled_4xx_codes = frozenset({400, 401, 409})


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
    return api.create_response(request, {"message": str(exc)}, status=400)


@api.post(
    "thread",
    tags=["Threads"],
    summary="Create a new Thread entry.",
    description="Creates a new thread entry in the database for future usage.",
    response={201: ThreadOutSchema, handled_4xx_codes: Message},
)
def create_new_thread(request: HttpRequest, new_thread: ThreadCreateSchema):
    if Thread.objects.filter(thread_id=new_thread.thread_id).exists():
        raise AlreadyExists

    try:
        it: InitThread = InitThread.objects.get(thread_id=new_thread.thread_id)
        help_type: str = it.help_type
        it.delete()
    except InitThread.DoesNotExist:
        help_type = new_thread.generic_topic if new_thread.generic_topic else ""

    thread: Thread = Thread.objects.create(
        thread_id=new_thread.thread_id,
        time_opened=new_thread.time_opened,
        opened_by=new_thread.opened_by,
        generic_topic=help_type,
    )
    thread.full_clean()
    thread.save()

    initial_message: ThreadMessage = ThreadMessage.objects.create(
        thread=thread,
        message_id=new_thread.initial_message.message_id,
        author_id=new_thread.initial_message.author_id,
        time_sent=new_thread.initial_message.time_sent,
        is_helper=new_thread.initial_message.is_helper,
    )
    initial_message.full_clean()
    initial_message.save()

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


@api.post(
    "thread/partial",
    tags=["Threads"],
    summary="Init a thread.",
    description="Init a thread, with the interaction button help.",
    response={201: None, handled_4xx_codes: Message},
)
async def init_thread(request: HttpRequest, init_data: InitThreadSchema):
    it: InitThread = InitThread.objects.create(
        thread_id=init_data.thread_id, help_type=init_data.help_type
    )
    it.full_clean()
    it.save()
    return 201, None


@api.delete(
    "thread/partial/{thread_id}",
    tags=["Threads"],
    summary="Delete an init thread.",
    description="Delete the init for a thread.",
    response={200: None, handled_4xx_codes: Message},
)
async def delete_init_thread(request: HttpRequest, thread_id: int):
    try:
        InitThread.objects.get(thread_id=thread_id).delete()
    except InitThread.DoesNotExist:
        pass
    finally:
        return 200, None


@api.get(
    "thread/{thread_id}",
    tags=["Threads"],
    summary="Get a specific Thread.",
    description="Retrieve info for a specific thread.",
    response={200: ThreadOutSchema, 401: Message, 404: Message},
)
def retrieve_thread(request: HttpRequest, thread_id: int):
    thread: Thread = get_object_or_404(Thread, thread_id=thread_id)
    return thread.as_schema()


@api.patch(
    "thread/{thread_id}",
    tags=["Threads"],
    summary="Update the given thread.",
    description="Update one of the three possible fields for a thread.",
    response={200: ThreadOutSchema, 400: Message, 401: Message, 404: Message},
)
def patch_thread(request: HttpRequest, thread_id: int, patch_data: ThreadPatchSchema):
    if (
        not patch_data.specific_topic
        and not patch_data.generic_topic
        and not patch_data.closed_by
        and not patch_data.time_closed
    ):
        raise MissingPatchData

    thread: Thread = get_object_or_404(Thread, thread_id=thread_id)

    # Do we need to stop modification of closed threads. Maybe not?
    if patch_data.generic_topic:
        thread.generic_topic = patch_data.generic_topic

    if patch_data.specific_topic:
        thread.specific_topic = patch_data.specific_topic

    if patch_data.closed_by:
        thread.closed_by = patch_data.closed_by

    if patch_data.time_closed:
        thread.time_closed = patch_data.time_closed

    thread.full_clean()
    thread.save()
    return 200, thread.as_schema()


@api.post(
    "thread/{thread_id}/messages",
    tags=["Threads"],
    summary="Add a message to a Thread.",
    description="Adds the given message to the associated thread.",
    response={201: ThreadMessageSchema, handled_4xx_codes: Message},
)
def create_thread_message(
    request: HttpRequest, thread_id: int, message: ThreadMessageSchema
):
    if thread_id != message.thread_id:
        raise ValidationError(
            "Thread route param did not match provided data thread id."
        )

    thread: Thread = get_object_or_404(Thread, thread_id=thread_id)

    tm: ThreadMessage = ThreadMessage.objects.create(
        thread=thread,
        is_helper=message.is_helper,
        time_sent=message.time_sent,
        author_id=message.author_id,
        message_id=message.message_id,
    )
    tm.full_clean()
    tm.save()

    return 201, tm.as_schema()


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
