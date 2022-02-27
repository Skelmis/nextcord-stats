from django.db import models


class InitThread(models.Model):
    thread_id = models.PositiveBigIntegerField(primary_key=True)
    help_type = models.TextField(help_text="The help type based on the button pressed.")
    created_at = models.DateTimeField(auto_now_add=True)
