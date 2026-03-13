from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from app.models import Job
from app.pipeline import JobPipeline


class JobWorker:
    def __init__(self, pipeline: JobPipeline) -> None:
        self.pipeline = pipeline
        self.pool = ThreadPoolExecutor(max_workers=2)

    def submit(self, job: Job) -> None:
        self.pool.submit(self.pipeline.run, job)
