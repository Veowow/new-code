import importlib.util

import pytest


fastapi_available = importlib.util.find_spec("fastapi") is not None

if not fastapi_available:
    pytest.skip("fastapi not installed in environment", allow_module_level=True)

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_cors_header_exists() -> None:
    response = client.get("/health", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "*"
