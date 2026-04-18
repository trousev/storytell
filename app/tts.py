import torch

from silero import silero_tts


class TTSEngine:
    def __init__(self, language: str = "ru", speaker: str = "aidar", sample_rate: int = 48000):
        self.language = language
        self.speaker = speaker
        self.sample_rate = sample_rate
        self.device = torch.device("cpu")
        torch.set_num_threads(4)
        self.model, self.example_text = silero_tts(
            language=language, speaker="v5_ru"
        )
        self.model.to(self.device)

    def synthesize(self, text: str, output_path: str):
        audio = self.model.apply_tts(
            text=text,
            speaker=self.speaker,
            sample_rate=self.sample_rate,
        )
        import soundfile as sf
        sf.write(output_path, audio, self.sample_rate)