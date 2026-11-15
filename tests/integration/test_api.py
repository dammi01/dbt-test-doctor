from pathlib import Path

import pytest
from fastapi.testclient import TestClient

FIXTURE = Path(__file__).parents[1] / "fixtures" / "run_results.json"


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "test.db"))
    from app.main import app
    return TestClient(app)


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_upload_shows_findings_and_persists(client):
    files = {"file": ("run_results.json", FIXTURE.read_bytes(), "application/json")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    assert "2 failing test(s)" in response.text
    assert "not_null" in response.text
    assert "2 failure(s)" in client.get("/").text


def test_upload_rejects_invalid_json(client):
    response = client.post("/upload", files={"file": ("x.json", b"not json", "application/json")})
    assert response.status_code == 400


def test_upload_rejects_non_dbt_json(client):
    response = client.post("/upload", files={"file": ("x.json", b'{"foo": 1}', "application/json")})
    assert response.status_code == 400
    
    
def test_request_id_header_and_log_line(client, caplog):
    response = client.get("/health", headers={"X-Request-ID": "abc12345-test"})
    assert response.headers["X-Request-ID"] == "abc12345-test"
    records = [r for r in caplog.records if getattr(r, "event", None) == "http_request"]
    assert records and records[-1].status == 200
