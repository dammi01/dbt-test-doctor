"""SQLite persistence. The DB path comes from DB_PATH so tests can use a temp file."""
import json
import os
import sqlite3
from pathlib import Path


def db_path() -> str:
    return os.getenv("DB_PATH", "data/doctor.db")


def connect() -> sqlite3.Connection:
    Path(db_path()).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            failures INTEGER NOT NULL,
            findings_json TEXT NOT NULL
        )
    """)
    return conn


def save_report(findings: list[dict]) -> int:
    conn = connect()
    try:
        cur = conn.execute(
            "INSERT INTO reports (failures, findings_json) VALUES (?, ?)",
            (len(findings), json.dumps(findings)),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def list_reports(limit: int = 20) -> list[dict]:
    conn = connect()
    try:
        rows = conn.execute(
            "SELECT id, created_at, failures FROM reports ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
