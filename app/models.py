from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


class JobStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    done = "done"
    failed = "failed"


@dataclass
class SubtitleSegment:
    index: int
    start: float
    end: float
    text: str


@dataclass
class Job:
    id: str
    input_path: Path
    workspace: Path
    source_lang: str = "auto"
    target_lang: str = "zh-CN"
    status: JobStatus = JobStatus.queued
    error: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
