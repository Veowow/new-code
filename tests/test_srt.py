from app.models import SubtitleSegment
from app.srt import to_srt


def test_to_srt_formats_block() -> None:
    content = to_srt([SubtitleSegment(index=1, start=0, end=1.5, text="Hi")])
    assert "00:00:00,000 --> 00:00:01,500" in content
    assert "Hi" in content
