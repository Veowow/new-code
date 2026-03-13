from __future__ import annotations

import shutil
import sys
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

from app.models import Job
from app.pipeline import JobPipeline
from app.storage import JobStore
from app.worker import JobWorker

BASE_DIR = Path("data/jobs")
store = JobStore(BASE_DIR)
pipeline = JobPipeline(store)
worker = JobWorker(pipeline)

app = FastAPI(title="Subtitle Extractor & Translator MVP")


def _ui_html_path() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "app" / "static" / "index.html"
    return Path(__file__).parent / "static" / "index.html"


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return _ui_html_path().read_text(encoding="utf-8")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/jobs")
async def create_job(
    file: UploadFile = File(...),
    target_lang: str = Form("zh-CN"),
    source_lang: str = Form("auto"),
) -> dict[str, str]:
    job_id = str(uuid.uuid4())
    workspace = BASE_DIR / job_id
    workspace.mkdir(parents=True, exist_ok=True)

    input_path = workspace / file.filename
    with input_path.open("wb") as out:
        shutil.copyfileobj(file.file, out)

    job = Job(
        id=job_id,
        input_path=input_path,
        workspace=workspace,
        source_lang=source_lang,
        target_lang=target_lang,
    )
    store.save(job)
    worker.submit(job)
    return {"id": job_id, "status": job.status.value}


@app.get("/jobs/{job_id}")
def get_job(job_id: str) -> dict[str, str | None]:
    job = store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    return {
        "id": job.id,
        "status": job.status.value,
        "error": job.error,
    }


@app.get("/jobs/{job_id}/artifacts/{name}")
def get_artifact(job_id: str, name: str) -> FileResponse:
    if name not in {"original.srt", "translated.srt", "bilingual.srt"}:
        raise HTTPException(status_code=400, detail="invalid artifact")
    job = store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    path = job.workspace / name
    if not path.exists():
        raise HTTPException(status_code=404, detail="artifact not found")
    return FileResponse(path)
