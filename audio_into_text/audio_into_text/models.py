from typing import Any
from django.db import models


class Translator(models.Model):
    video_url = models.URLField("Video URL", blank=True, null=True)
    audio_url = models.URLField("Audio URL", blank=True, null=True)
    transcript = models.TextField("Transcript", blank=True, null=True)
    translated_text = models.TextField("Translated Text", blank=True, null=True)

    def __str__(self) -> Any:
        return self.video_url if self.video_url else self.audio_url
