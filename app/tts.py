import torch
import soundfile as sf
from abc import ABC, abstractmethod


class TTSProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str, output_path: str):
        pass


class SileroProvider(TTSProvider):
    def __init__(
        self,
        language: str = "ru",
        speaker: str = "aidar",
        sample_rate: int = 48000,
        **_,
    ):
        from silero import silero_tts

        self.language = language
        self.speaker = speaker
        self.sample_rate = sample_rate
        self.device = torch.device("cpu")
        torch.set_num_threads(4)
        self.model, _ = silero_tts(language=language, speaker="v5_ru")
        self.model.to(self.device)

    def synthesize(self, text: str, output_path: str):
        audio = self.model.apply_tts(
            text=text,
            speaker=self.speaker,
            sample_rate=self.sample_rate,
        )
        sf.write(output_path, audio, self.sample_rate)


LANGUAGE_MAP = {
    "ru": "russian",
    "en": "english",
    "zh": "chinese",
    "ja": "japanese",
    "ko": "korean",
    "de": "german",
    "fr": "french",
    "es": "spanish",
    "it": "italian",
    "pt": "portuguese",
}


class QwenProvider(TTSProvider):
    def __init__(
        self,
        model: str = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
        ref_audio: str | None = None,
        speaker: str = "Vivian",
        language: str = "en",
        **_,
    ):
        from qwen_tts import Qwen3TTSModel

        self.model = Qwen3TTSModel.from_pretrained(
            model,
            device_map="cpu",
            dtype=torch.bfloat16,
        )
        self.ref_audio = ref_audio
        self.speaker = speaker
        self.language = LANGUAGE_MAP.get(language, language)

    def synthesize(self, text: str, output_path: str):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            if self.ref_audio:
                wavs, sr = self.model.generate_voice_clone(
                    text=text,
                    ref_audio=self.ref_audio,
                )
            else:
                wavs, sr = self.model.generate_custom_voice(
                    text=text,
                    speaker=self.speaker,
                    language=self.language,
                )
        if isinstance(wavs, list):
            wavs = wavs[0]
        sf.write(output_path, wavs, sr)


def get_provider(provider: str, **kwargs) -> TTSProvider:
    providers = {
        "silero": SileroProvider,
        "qwen": QwenProvider,
    }
    if provider not in providers:
        raise ValueError(f"Unknown provider: {provider}")
    return providers[provider](**kwargs)


class TTSEngine:
    def __init__(self, provider: str = "silero", **kwargs):
        self.provider = get_provider(provider, **kwargs)

    def synthesize(self, text: str, output_path: str):
        self.provider.synthesize(text, output_path)