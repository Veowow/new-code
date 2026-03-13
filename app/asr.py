from __future__ import annotations

import os

from app.models import SubtitleSegment


class ASREngine:
    def transcribe(self, wav_path: str, source_lang: str = "auto") -> list[SubtitleSegment]:
        use_whisper = os.getenv("USE_WHISPER", "0") == "1"
        if use_whisper:
            return self._transcribe_whisper(wav_path, source_lang)
        return self._mock_segments()

    def _transcribe_whisper(self, wav_path: str, source_lang: str) -> list[SubtitleSegment]:
        try:
            from faster_whisper import WhisperModel
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError("faster-whisper is not installed") from exc

        model_size = os.getenv("ASR_MODEL_SIZE", "base")
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        language = None if source_lang == "auto" else source_lang
        segments, _ = model.transcribe(wav_path, language=language)

        output: list[SubtitleSegment] = []
        for idx, seg in enumerate(segments, start=1):
            output.append(
                SubtitleSegment(
                    index=idx,
                    start=float(seg.start),
                    end=float(seg.end),
                    text=seg.text.strip(),
                )
            )
        return output

    def _mock_segments(self) -> list[SubtitleSegment]:
        return [
            SubtitleSegment(index=1, start=0, end=2.0, text="Hello and welcome."),
            SubtitleSegment(index=2, start=2.0, end=5.0, text="This is a demo transcription."),
        ]
