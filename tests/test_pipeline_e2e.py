from __future__ import annotations

import os
import uuid
import wave
from pathlib import Path

from app.models import Job, JobStatus
from app.pipeline import JobPipeline
from app.storage import JobStore


def _create_wav(path: Path, seconds: int = 1) -> None:
    sample_rate = 16000
    frames = b"\x00\x00" * sample_rate * seconds
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(frames)


def test_pipeline_e2e_with_real_wav_input(tmp_path: Path) -> None:
    os.environ["USE_WHISPER"] = "0"

    base_dir = tmp_path / "jobs"
    store = JobStore(base_dir)
    pipeline = JobPipeline(store)

    job_id = str(uuid.uuid4())
    workspace = base_dir / job_id
    workspace.mkdir(parents=True, exist_ok=True)
    wav = workspace / "input.wav"
    _create_wav(wav)

    job = Job(id=job_id, input_path=wav, workspace=workspace)
    store.save(job)

    pipeline.run(job)

    loaded = store.get(job_id)
    assert loaded is not None
    assert loaded.status == JobStatus.done
    assert (workspace / "original.srt").exists()
    assert (workspace / "translated.srt").exists()
    assert (workspace / "bilingual.srt").exists()
