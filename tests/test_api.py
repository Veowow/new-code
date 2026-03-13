import importlib.util

import pytest


fastapi_available = importlib.util.find_spec("fastapi") is not None

if not fastapi_available:
    pytest.skip("fastapi not installed in environment", allow_module_level=True)

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_job_not_found() -> None:
    response = client.get("/jobs/not-found")
    assert response.status_code == 404
