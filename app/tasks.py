import os
from celery import shared_task
from django.conf import settings


@shared_task(bind=True)
def synthesize_speech(self, text: str, provider: str, voice: str, language: str, output_filename: str):
    from app.tts import TTSEngine

    output_path = os.path.join(settings.MEDIA_ROOT, "audio", f"{output_filename}.wav")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    kwargs = {"language": language, "speaker": voice}

    tts = TTSEngine(provider=provider, **kwargs)
    tts.synthesize(text, output_path)

    return f"audio/{output_filename}.wav"