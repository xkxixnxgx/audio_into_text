from django.apps import AppConfig
from media_to_text.models_downloader import download_or_load_models


class MediaToTextConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "media_to_text"

    def ready(self):
        import media_to_text.signals

        download_or_load_models()
