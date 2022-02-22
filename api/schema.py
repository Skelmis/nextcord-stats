import datetime
from typing import Optional, List

from ninja import Schema
from pydantic import Field


class Message(Schema):
    message: str = Field(..., description="A message describing why this was returned.")


class ThreadMessageSchema(Schema):
    thread_id: int = Field(
        ...,
        description="The id of the thread this message is in.",
    )
    message_id: int = Field(
        ...,
        description="The message id.",
    )
    author_id: int = Field(
        ...,
        description="The id of the person who created this message.",
    )
    time_sent: datetime.datetime = Field(
        ...,
        description="When this message was created.",
    )
    is_helper: Optional[bool] = Field(
        False,
        description="Was the creator of this message a helper when they sent the message?",
    )


class BaseThreadSchema(Schema):
    thread_id: int = Field(
        ...,
        description="The id of the created thread.",
    )
    time_opened: datetime.datetime = Field(
        ...,
        description="When this thread was created.",
    )
    opened_by: int = Field(
        ...,
        description="The id for the person who opened this thread.",
    )
    generic_topic: Optional[str] = Field(
        "",
        description="The generic topic for this thread, likely set based off the button pressed.",
    )


class ThreadCreateSchema(BaseThreadSchema):
    initial_message: ThreadMessageSchema = Field(
        ...,
        description="The initial message in this thread. Not from Previous.",
    )


class ThreadOutSchema(BaseThreadSchema):
    messages: List[ThreadMessageSchema] = Field(
        ...,
        description="All the messages associated with this thread.",
    )
    time_closed: Optional[datetime.datetime] = Field(
        None,
        description="When this thread was closed.",
    )
    closed_by: int = Field(
        None,
        description="The id for the person who closed this thread.",
    )
    specific_topic: str = Field(
        ...,
        description="Specifics for this thread, this is likely the exact issue (And thread name)",
    )


class ThreadPatchSchema(Schema):
    generic_topic: Optional[str] = Field(
        "",
        description="The updated generic_topic for this thread.",
    )
    specific_topic: Optional[str] = Field(
        "",
        description="The updated specific topic for this thread. (This is likely thread name)",
    )
    time_closed: datetime.datetime = Field(
        None,
        description="The time this thread was closed.",
    )
    closed_by: int = Field(
        None,
        description="The id of who closed this thread.",
    )
