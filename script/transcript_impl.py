#!/usr/bin/env .venv/bin/python
import argparse
import sys
from app.tts import TTSEngine


def main():
    parser = argparse.ArgumentParser(description="Convert text to speech")
    parser.add_argument("-i", "--input", required=True, help="Input text")
    parser.add_argument("-o", "--output", required=True, help="Output WAV file path")
    parser.add_argument("-l", "--language", default="ru", help="Language code")
    args = parser.parse_args()

    tts = TTSEngine(language=args.language)
    tts.synthesize(args.input, args.output)
    print(f"Audio saved to {args.output}")


if __name__ == "__main__":
    main()