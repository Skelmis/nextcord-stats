import datetime
from typing import Optional, List

from ninja import Schema
from pydantic import Field


class ThreadMessageSchema(Schema):
    thread_id: int = Field(..., description="The id of the thread this message is in.")
    author_id: int = Field(
        ..., description="The id of the person who created this message."
    )
    time_sent: datetime.datetime = Field(
        ..., description="When this message was created."
    )
    is_helper: Optional[bool] = Field(
        False,
        description="Was the creator of this message a helper when they sent the message?",
    )


class BaseThreadSchema(Schema):
    thread_id: int = Field(..., description="The id of the created thread.")
    time_opened: datetime.datetime = Field(
        ..., description="When this thread was created."
    )
    opened_by: int = Field(
        ..., description="The id for the person who opened this thread."
    )
    topic: Optional[str] = Field("", description="The topic for this thread.")


class ThreadCreateSchema(BaseThreadSchema):
    initial_message: ThreadMessageSchema = Field(
        ..., description="The initial message in this thread. Not from Previous."
    )


class ThreadOutSchema(BaseThreadSchema):
    messages: List[ThreadMessageSchema] = Field(
        ..., description="All the messages associated with this thread."
    )
