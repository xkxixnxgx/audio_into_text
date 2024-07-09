import os
import uuid
from typing import Any
from django.db import models


def upload_video_to(instance, filename):
    ext = filename.split(".")[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("videos", new_filename)


def upload_audio_to(instance, filename):
    ext = filename.split(".")[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("audios", new_filename)


class Translator(models.Model):
    day = models.IntegerField("Day", blank=True, null=True)
    set_name = models.CharField("Set Name", max_length=255, blank=True, null=True)
    action_name = models.CharField("Action Name", max_length=255)
    description = models.TextField("Description", blank=True, null=True)
    video = models.FileField("Video URL", upload_to=upload_video_to, blank=True, null=True)
    audio = models.FileField("Audio URL", upload_to=upload_audio_to, blank=True, null=True)
    transcript = models.TextField("Transcript", blank=True, null=True)
    translated_text = models.TextField("Translated Text", blank=True, null=True)

    def __str__(self) -> Any:
        return self.action_name
