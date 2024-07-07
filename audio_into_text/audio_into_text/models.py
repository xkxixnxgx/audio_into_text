from typing import Any
from django.db import models


class Translator(models.Model):
    day = models.IntegerField("Day")
    action_name = models.CharField("Action Name", max_length=255)
    description = models.TextField("Description", blank=True, null=True)
    video_url = models.URLField("Video URL", blank=True, null=True)
    audio_url = models.URLField("Audio URL", blank=True, null=True)
    transcript = models.TextField("Transcript", blank=True, null=True)
    translated_text = models.TextField("Translated Text", blank=True, null=True)

    def __str__(self) -> Any:
        return self.action_name
