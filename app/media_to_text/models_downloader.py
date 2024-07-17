import os
from pathlib import Path
from transformers import Wav2Vec2ForCTC, MarianMTModel
from django.conf import settings


def download_or_load_models():
    models = {
        "en": {"model_name": "facebook/wav2vec2-base-960h", "class": Wav2Vec2ForCTC},
        "ru": {"model_name": "Helsinki-NLP/opus-mt-en-ru", "class": MarianMTModel},
    }
    base_dir = Path(settings.BASE_DIR)
    for lang, info in models.items():
        model_dir = base_dir / f"ml_models/{lang}" / info["model_name"]

        if not model_dir.exists():
            print(f"Model for {lang} not found. Downloading...")
            model_dir.mkdir(parents=True, exist_ok=True)
            model = info["class"].from_pretrained(info["model_name"])
            model.save_pretrained(model_dir)
            print(f"Model for {lang} downloaded and saved in {model_dir}")
        else:
            print(f"Model for {lang} already exists in {model_dir}")
