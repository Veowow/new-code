import importlib.util

import pytest


fastapi_available = importlib.util.find_spec("fastapi") is not None

if not fastapi_available:
    pytest.skip("fastapi not installed in environment", allow_module_level=True)

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_page() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "字幕提取与翻译" in response.text
    assert "<form" in response.text
