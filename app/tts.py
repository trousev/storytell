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


class QwenProvider(TTSProvider):
    def __init__(
        self,
        model: str = "Qwen/Qwen3-TTS-12Hz-0.6B-Base",
        ref_audio: str | None = None,
        **_,
    ):
        from qwen_tts import Qwen3TTSModel

        self.model = Qwen3TTSModel.from_pretrained(
            model,
            device_map="cpu",
            dtype=torch.bfloat16,
        )
        self.ref_audio = ref_audio

    def synthesize(self, text: str, output_path: str):
        if self.ref_audio:
            wavs, sr = self.model.generate_voice_clone(
                text=text,
                ref_audio=self.ref_audio,
            )
        else:
            raise ValueError("Qwen provider requires --ref-audio for voice cloning")
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