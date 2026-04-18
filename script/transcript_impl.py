#!/usr/bin/env .venv/bin/python
import argparse
import sys
from app.tts import TTSEngine


def main():
    parser = argparse.ArgumentParser(description="Convert text to speech")
    parser.add_argument("-i", "--input", required=True, help="Input text")
    parser.add_argument("-o", "--output", required=True, help="Output WAV file path")
    parser.add_argument("-p", "--provider", default="silero", help="TTS provider")
    parser.add_argument("-l", "--language", default="ru", help="Language code")
    parser.add_argument("-r", "--ref-audio", default=None, help="Reference audio for voice cloning (qwen)")
    args = parser.parse_args()

    kwargs = {"language": args.language}
    if args.ref_audio:
        kwargs["ref_audio"] = args.ref_audio
    tts = TTSEngine(provider=args.provider, **kwargs)
    tts.synthesize(args.input, args.output)
    print(f"Audio saved to {args.output}")


if __name__ == "__main__":
    main()