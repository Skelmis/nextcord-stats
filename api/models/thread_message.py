from django.db import models

from api.models import Thread


class ThreadMessage(models.Model):
    """A single message within a Thread"""

    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, help_text="The thread to attach this to."
    )
    message_id = models.PositiveBigIntegerField(
        help_text="The message id.", db_index=True
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

    class Meta:
        ordering = ("time_sent",)
        verbose_name = "Thread Message"
        verbose_name_plural = "Thread Messages"
