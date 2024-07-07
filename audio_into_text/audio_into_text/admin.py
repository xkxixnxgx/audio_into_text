from django.contrib import admin
from .models import Translator
from .tasks import decode_video_to_audio, transcribe_audio, translate_transcript


class TranslatorAdmin(admin.ModelAdmin):
    list_display = ("video_url", "audio_url", "transcript", "translated_text", "day", "action_name", "description")
    actions = ["process_video", "process_audio", "translate_text"]

    def process_video(self, request, queryset):
        for translator in queryset:
            if translator.video_url:
                decode_video_to_audio(translator)
        self.message_user(request, "Video processing started.")

    def process_audio(self, request, queryset):
        for translator in queryset:
            if translator.audio_url:
                transcribe_audio(translator)
        self.message_user(request, "Audio processing started.")

    def translate_text(self, request, queryset):
        for translator in queryset:
            if translator.transcript:
                translate_transcript(translator)
        self.message_user(request, "Translation started.")


admin.site.register(Translator, TranslatorAdmin)
