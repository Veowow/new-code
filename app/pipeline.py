from __future__ import annotations

from pathlib import Path

from app.asr import ASREngine
from app.media import extract_wav
from app.models import Job, JobStatus, SubtitleSegment
from app.srt import bilingual_segments, to_srt
from app.storage import JobStore
from app.translation import translate_batch


class JobPipeline:
    def __init__(self, store: JobStore) -> None:
        self.store = store
        self.asr = ASREngine()

    def run(self, job: Job) -> None:
        try:
            job.status = JobStatus.processing
            self.store.save(job)

            wav_path = job.workspace / "audio.wav"
            extract_wav(job.input_path, wav_path)

            source_segments = self.asr.transcribe(str(wav_path), source_lang=job.source_lang)
            texts = [s.text for s in source_segments]
            translated = translate_batch(texts, target_lang=job.target_lang, source_lang=job.source_lang)

            translated_segments: list[SubtitleSegment] = [
                SubtitleSegment(index=s.index, start=s.start, end=s.end, text=t)
                for s, t in zip(source_segments, translated, strict=False)
            ]
            bi_segments = bilingual_segments(source_segments, translated)

            (job.workspace / "original.srt").write_text(to_srt(source_segments), encoding="utf-8")
            (job.workspace / "translated.srt").write_text(to_srt(translated_segments), encoding="utf-8")
            (job.workspace / "bilingual.srt").write_text(to_srt(bi_segments), encoding="utf-8")

            job.status = JobStatus.done
            self.store.save(job)
        except Exception as exc:  # noqa: BLE001
            job.status = JobStatus.failed
            job.error = str(exc)
            self.store.save(job)
