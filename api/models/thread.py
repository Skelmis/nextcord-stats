from django.db import models


class Thread(models.Model):
    """Represents a Nextcord help thread"""

    thread_id = models.PositiveBigIntegerField(
        help_text="The id of this thread.", primary_key=True
    )
    time_opened = models.DateTimeField(
        help_text="When the thread was opened.", editable=False
    )
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
    topic = models.TextField(
        help_text="The topic for this thread.", default="", blank=True
    )

    class Meta:
        ordering = ("time_opened",)
