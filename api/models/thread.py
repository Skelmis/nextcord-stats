from django.db import models

from api.schema import ThreadOutSchema, ThreadMessageSchema


class Thread(models.Model):
    """Represents a Nextcord help thread"""

    thread_id = models.PositiveBigIntegerField(
        help_text="The id of this thread.", primary_key=True
    )
    time_opened = models.DateTimeField(help_text="When the thread was opened.")
    time_closed = models.DateTimeField(
        help_text="When the thread was closed.", blank=True, null=True
    )
    closed_by = models.PositiveBigIntegerField(
        help_text="The id of the person who closed this thread.",
        db_index=True,
        null=True,
        blank=True,
    )
    opened_by = models.PositiveBigIntegerField(
        help_text="The id of the person who opened this thread.", db_index=True
    )
    generic_topic = models.TextField(
        help_text="The generic topic for this thread.", default="", blank=True
    )
    specific_topic = models.TextField(
        help_text="Specifics for this thread, this is likely the exact issue (And thread name)",
        default="",
        blank=True,
    )

    def __str__(self):
        return f"Thread(thread_id={self.thread_id})"

    def as_schema(self) -> ThreadOutSchema:
        messages: list[ThreadMessageSchema] = []
        for thread_message in self.threadmessage_set.all():
            messages.append(thread_message.as_schema())

        return ThreadOutSchema(
            messages=messages,
            thread_id=self.thread_id,
            time_opened=self.time_opened,
            time_closed=self.time_closed,
            opened_by=self.opened_by,
            closed_by=self.closed_by,
            generic_topic=self.generic_topic,
            specific_topic=self.specific_topic,
        )

    class Meta:
        ordering = ("time_opened",)
