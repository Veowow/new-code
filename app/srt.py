from __future__ import annotations

from app.models import SubtitleSegment


def _to_srt_time(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, r = divmod(ms, 3600000)
    m, r = divmod(r, 60000)
    s, ms = divmod(r, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def to_srt(segments: list[SubtitleSegment]) -> str:
    lines: list[str] = []
    for seg in segments:
        lines.append(str(seg.index))
        lines.append(f"{_to_srt_time(seg.start)} --> {_to_srt_time(seg.end)}")
        lines.append(seg.text.strip())
        lines.append("")
    return "\n".join(lines)


def bilingual_segments(
    source: list[SubtitleSegment],
    translated_texts: list[str],
) -> list[SubtitleSegment]:
    output: list[SubtitleSegment] = []
    for seg, tr in zip(source, translated_texts, strict=False):
        output.append(
            SubtitleSegment(
                index=seg.index,
                start=seg.start,
                end=seg.end,
                text=f"{seg.text.strip()}\n{tr.strip()}",
            )
        )
    return output
