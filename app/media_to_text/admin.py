from django.contrib import admin
from .models import Translator

from .tasks import decode_video_to_audio, transcribe_audio, translate_transcript


class TranslatorAdmin(admin.ModelAdmin):
    list_display = (
        "day",
        "set_name",
        "action_name",
        "description",
        "short_transcript",
        "short_translated_text",
        "video",
        "audio",
    )
    actions = ["process_video", "process_audio", "translate_text"]
    search_fields = ("set_name", "action_name", "description")
    ordering = ("day",)

    def process_video(self, request, queryset):
        for translator in queryset:
            if translator.video:
                decode_video_to_audio(translator)
        self.message_user(request, "Convert video to audio.")

    def process_audio(self, request, queryset):
        for translator in queryset:
            if translator.audio:
                transcribe_audio(translator)
        self.message_user(request, "Recognize text from audio.")

    def translate_text(self, request, queryset):
        for translator in queryset:
            if translator.transcript:
                translate_transcript(translator)
        self.message_user(request, "Translate eng to rus text.")

    class Media:
        css = {"all": ("css/custom_admin.css",)}
        js = ("js/custom_admin.js",)


admin.site.register(Translator, TranslatorAdmin)
