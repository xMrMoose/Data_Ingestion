"""
transcribe_podcast.py

Transcribes an audio file (e.g. a downloaded podcast episode) to text using
a local Whisper model via faster-whisper. Runs entirely offline/on-CPU --
no API key or internet access required after the model is first downloaded.

Usage:
    python scripts/transcribe_podcast.py Morning_Call_2026-09-23.mp3
    python scripts/transcribe_podcast.py path/to/audio.mp3 --model small --output transcript.txt
"""

import argparse
import time
from pathlib import Path

from faster_whisper import WhisperModel


def format_timestamp(seconds: float) -> str:
    hours, remainder = divmod(int(seconds), 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def transcribe(audio_path: Path, model_size: str) -> list:
    print(f"Loading Whisper model '{model_size}' (CPU, int8)...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print(f"Transcribing {audio_path.name} (this can take a while for long audio)...")
    start_time = time.time()
    segments, info = model.transcribe(str(audio_path), beam_size=5)

    print(f"Detected language: {info.language} (probability {info.language_probability:.2f})")

    results = []
    for segment in segments:
        results.append(segment)
        print(f"[{format_timestamp(segment.start)} -> {format_timestamp(segment.end)}] {segment.text.strip()}")

    print(f"Transcription finished in {time.time() - start_time:.1f}s")
    return results


def save_transcript(segments: list, output_path: Path) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        for segment in segments:
            f.write(f"[{format_timestamp(segment.start)} -> {format_timestamp(segment.end)}] {segment.text.strip()}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe an audio file with faster-whisper.")
    parser.add_argument("audio_path", type=Path, help="Path to the audio file (mp3, wav, m4a, etc.)")
    parser.add_argument("--model", default="base", help="Whisper model size: tiny, base, small, medium, large-v3 (default: base)")
    parser.add_argument("--output", type=Path, default=None, help="Output .txt path (default: same name as audio file, .txt extension)")
    args = parser.parse_args()

    if not args.audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {args.audio_path}")

    output_path = args.output or args.audio_path.with_suffix(".txt")

    segments = transcribe(args.audio_path, args.model)
    save_transcript(segments, output_path)
    print(f"Saved transcript to {output_path}")


if __name__ == "__main__":
    main()
