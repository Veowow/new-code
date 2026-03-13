from __future__ import annotations

import shutil
import subprocess
import wave
from pathlib import Path


def _is_16k_mono_wav(path: Path) -> bool:
    if path.suffix.lower() != ".wav":
        return False
    with wave.open(str(path), "rb") as wav:
        return wav.getnchannels() == 1 and wav.getframerate() == 16000


def extract_wav(input_file: Path, output_wav: Path) -> None:
    """Extract 16k mono wav from media.

    Fast path: if input is already 16k mono wav, copy directly and skip ffmpeg.
    """
    if _is_16k_mono_wav(input_file):
        shutil.copyfile(input_file, output_wav)
        return

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_file),
        "-ac",
        "1",
        "-ar",
        "16000",
        str(output_wav),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {proc.stderr.strip()}")
