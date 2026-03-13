from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from app.models import Job, JobStatus


class JobStore:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _meta_file(self, job_id: str) -> Path:
        return self.base_dir / job_id / "meta.json"

    def save(self, job: Job) -> None:
        job.workspace.mkdir(parents=True, exist_ok=True)
        payload = asdict(job)
        payload["input_path"] = str(job.input_path)
        payload["workspace"] = str(job.workspace)
        payload["status"] = job.status.value
        payload["created_at"] = job.created_at.isoformat()
        self._meta_file(job.id).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def get(self, job_id: str) -> Job | None:
        path = self._meta_file(job_id)
        if not path.exists():
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
        return Job(
            id=payload["id"],
            input_path=Path(payload["input_path"]),
            workspace=Path(payload["workspace"]),
            source_lang=payload["source_lang"],
            target_lang=payload["target_lang"],
            status=JobStatus(payload["status"]),
            error=payload.get("error"),
            created_at=datetime.fromisoformat(payload["created_at"]),
        )
