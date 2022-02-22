from django.db import models

from api.models import Thread
from api.schema import ThreadMessageSchema


class ThreadMessage(models.Model):
    """A single message within a Thread"""

    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, help_text="The thread to attach this to."
    )
    message_id = models.PositiveBigIntegerField(
        help_text="The message id.", db_index=True, unique=True
    )
    author_id = models.PositiveBigIntegerField(
        help_text="The id for the author of this message.", db_index=True
    )
    time_sent = models.DateTimeField(help_text="When was this model sent?")
    is_helper = models.BooleanField(
        default=False, help_text="Was the author a helper when they sent this message?"
    )

    def __str__(self):
        return f"ThreadMessage(thread={self.thread})"

    def as_schema(self) -> ThreadMessageSchema:
        return ThreadMessageSchema(
            thread_id=self.thread.thread_id,
            message_id=self.message_id,
            author_id=self.author_id,
            time_sent=self.time_sent,
            is_helper=self.is_helper,
        )

    class Meta:
        ordering = ("time_sent",)
        verbose_name = "Thread Message"
        verbose_name_plural = "Thread Messages"
