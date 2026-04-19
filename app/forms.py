from django import forms

PROVIDER_CHOICES = [
    ("silero", "Silero"),
    ("qwen", "Qwen"),
]

SILERO_VOICES = [
    ("aidar", "Aidar"),
    ("baya", "Baya"),
    ("kseniya", "Kseniya"),
    ("eugene", "Eugene"),
    ("xenia", "Xenia"),
]

QWEN_VOICES = [
    ("Vivian", "Vivian"),
    ("Amy", "Amy"),
    ("Emma", "Emma"),
    ("James", "James"),
]

LANGUAGE_CHOICES = [
    ("ru", "Russian"),
    ("en", "English"),
    ("zh", "Chinese"),
    ("de", "German"),
    ("fr", "French"),
]


class TTSForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5, "cols": 50}),
        label="Text to speak",
    )
    provider = forms.ChoiceField(choices=PROVIDER_CHOICES, label="TTS Provider")
    voice = forms.ChoiceField(choices=SILERO_VOICES, label="Voice")
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, label="Language")