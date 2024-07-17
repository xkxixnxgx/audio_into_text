import os
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import Translator


@receiver(pre_delete, sender=Translator)
def delete_files_on_delete(sender, instance, **kwargs):
    if instance.video and os.path.isfile(instance.video.path):
        os.remove(instance.video.path)
    if instance.audio and os.path.isfile(instance.audio.path):
        os.remove(instance.audio.path)


@receiver(pre_save, sender=Translator)
def delete_files_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_instance = Translator.objects.get(pk=instance.pk)
    except Translator.DoesNotExist:
        return
    if old_instance.video and old_instance.video != instance.video:
        if os.path.isfile(old_instance.video.path):
            os.remove(old_instance.video.path)
    if old_instance.audio and old_instance.audio != instance.audio:
        if os.path.isfile(old_instance.audio.path):
            os.remove(old_instance.audio.path)
