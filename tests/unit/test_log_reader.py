import json

import pytest

duckdb = pytest.importorskip("duckdb")  # skips the module if the dashboard deps are not installed
from dashboard.log_reader import load_requests  # noqa: E402


def test_load_requests_keeps_only_http_lines(tmp_path):
    log = tmp_path / "app.jsonl"
    lines = [
        {"ts": "2026-11-15T18:11:36-0300", "level": "INFO", "msg": "startup", "event": "startup"},
        {
            "ts": "2026-11-15T18:11:37-0300", "level": "INFO", "msg": "request",
            "request_id": "abc12345", "event": "http_request", "method": "GET",
            "path": "/health", "status": 200, "duration_ms": 2.5,
        },
    ]
    log.write_text("\n".join(json.dumps(x) for x in lines) + "\n", encoding="utf-8")

    rows = load_requests(log)

    assert len(rows) == 1
    assert rows[0]["path"] == "/health"
    assert rows[0]["status"] == 200
