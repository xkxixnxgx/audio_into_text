import os
import subprocess
from django.conf import settings
import torch
import torchaudio
import numpy as np
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, MarianMTModel, MarianTokenizer
from googletrans import Translator as GoogleTranslator
from google.cloud import translate_v2 as translate
from google.auth.transport.requests import Request
import google.auth
import os
import requests

print(f"GOOGLE_APPLICATION_CREDENTIALS: {settings.GOOGLE_APPLICATION_CREDENTIALS}")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS


def get_translate_client():
    credentials, project = google.auth.default()
    session = requests.Session()
    session.verify = False
    authed_session = Request(session=session)
    return translate.Client(credentials=credentials, _http=authed_session)


def decode_video_to_audio(translator):
    if translator.video:
        video_filename = os.path.splitext(os.path.basename(translator.video.name))[0]
        audio_dir = os.path.join(settings.MEDIA_ROOT, "audios")
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
        output_audio_file = os.path.join(audio_dir, f"{video_filename}.ogg")
        command = f"ffmpeg -i {translator.video.path} -ar 16000 -q:a 0 -map a {output_audio_file}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error executing ffmpeg command: {result.stderr}")
            return
        translator.audio.name = os.path.join("audios", f"{video_filename}.ogg")
        translator.save()
        print(f"The file was saved successfully: {output_audio_file}")


# def add_pauses(transcription, speech_array, sampling_rate, pause_threshold=5):
#     pause_duration = pause_threshold * sampling_rate
#     transcription_with_pauses = transcription
#     last_index = 0
#     is_pause = False
#     pause_start = 0
#     for i in range(len(speech_array)):
#         if np.all(speech_array[i] == 0):
#             if not is_pause:
#                 pause_start = i
#                 is_pause = True
#         else:
#             if is_pause:
#                 pause_length = i - pause_start
#                 if pause_length > pause_duration:
#                     pause_time = pause_length / sampling_rate
#                     transcription_with_pauses += f"... <pause {pause_time:.1f} sec> "
#                 is_pause = False
#     return transcription_with_pauses


def add_pauses(transcription, speech_array, sampling_rate, pause_threshold=5):
    pause_duration = pause_threshold * sampling_rate
    transcription_with_pauses = ""
    last_index = 0
    is_pause = False
    pause_start = 0
    for i in range(len(speech_array)):
        if np.all(speech_array[i] == 0):
            if not is_pause:
                pause_start = i
                is_pause = True
        else:
            if is_pause:
                pause_length = i - pause_start
                if pause_length > pause_duration:
                    pause_time = pause_length / sampling_rate
                    transcription_with_pauses += f"<pause {pause_time:.1f} sec> "
                is_pause = False
        transcription_with_pauses += transcription[last_index:i]
        last_index = i
    transcription_with_pauses += transcription[last_index:]
    return transcription_with_pauses


# def transcribe_audio(translator):
#     if translator.audio:
#         processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
#         model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
#         audio_path = os.path.join(settings.MEDIA_ROOT, translator.audio.name)
#         speech_array, sampling_rate = torchaudio.load(audio_path)
#         speech_array = speech_array.squeeze().numpy()
#         inputs = processor(speech_array, sampling_rate=sampling_rate, return_tensors="pt", padding=True)
#         with torch.no_grad():
#             logits = model(inputs.input_values).logits
#         predicted_ids = torch.argmax(logits, dim=-1)
#         transcription = processor.batch_decode(predicted_ids)[0]
#         transcription = add_pauses(transcription, speech_array, sampling_rate)
#         translator.transcript = transcription
#         translator.save()
def transcribe_audio(translator):
    if translator.audio:
        processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
        model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
        audio_path = os.path.join(settings.MEDIA_ROOT, translator.audio.name)
        speech_array, sampling_rate = torchaudio.load(audio_path)
        speech_array = speech_array.squeeze().numpy()
        inputs = processor(speech_array, sampling_rate=sampling_rate, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = model(inputs.input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)[0]
        transcription_with_pauses = add_pauses(transcription, speech_array, sampling_rate)
        translator.transcript = transcription_with_pauses
        translator.save()


# def translate_text(text):
#     model_name = "Helsinki-NLP/opus-mt-en-ru"
#     model = MarianMTModel.from_pretrained(model_name)
#     tokenizer = MarianTokenizer.from_pretrained(model_name)
#     inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
#     translated = model.generate(**inputs)
#     translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
#     return translated_text


# def translate_transcript(translator):
#     if translator.transcript:
#         translated_text = translate_text(translator.transcript)
#         translator.translated_text = translated_text
#         translator.save()
# def translate_text(text):
#     translator = GoogleTranslator()
#     sentences = text.split("<pause")
#     translated_sentences = []

#     for sentence in sentences:
#         if "sec>" in sentence:
#             pause_part, text_part = sentence.split("sec>")
#             translated_text = translator.translate(text_part, src='en', dest='ru').text
#             translated_sentences.append(f"<pause{pause_part}sec>{translated_text}")
#         else:
#             translated_text = translator.translate(sentence, src='en', dest='ru').text
#             translated_sentences.append(translated_text)

#     return " ".join(translated_sentences)

# def translate_transcript(translator):
#     if translator.transcript:
#         translator.translated_text = translate_text(translator.transcript)
#         translator.save()


def translate_text(text):
    client = get_translate_client()
    sentences = text.split("<pause")
    translated_sentences = []

    for sentence in sentences:
        if "sec>" in sentence:
            pause_part, text_part = sentence.split("sec>")
            translated_text = client.translate(text_part, target_language="ru")["translatedText"]
            translated_sentences.append(f"<pause{pause_part}sec>{translated_text}")
        else:
            translated_text = client.translate(sentence, target_language="ru")["translatedText"]
            translated_sentences.append(translated_text)

    return " ".join(translated_sentences)


def translate_transcript(translator):
    if translator.transcript:
        translator.translated_text = translate_text(translator.transcript)
        translator.save()
