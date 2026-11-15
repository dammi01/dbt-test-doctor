from pathlib import Path


def load_requests(log_path: Path) -> list[dict]:
    """Return one dict per http_request line in a JSONL log file."""
    import duckdb  # imported here so the app itself does not need DuckDB

    relation = duckdb.read_json(
        str(log_path), format="newline_delimited", ignore_errors=True
    ).filter("event = 'http_request'")
    columns = relation.columns
    return [dict(zip(columns, row)) for row in relation.fetchall()]
