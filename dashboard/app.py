import os
from pathlib import Path

import streamlit as st

from log_reader import load_requests

LOG_PATH = Path(os.getenv("LOG_PATH", "logs/app.jsonl"))

st.set_page_config(page_title="dbt-test-doctor logs", layout="wide")
st.title("dbt-test-doctor: request logs")

if not LOG_PATH.exists():
    st.warning(f"No log file at `{LOG_PATH}`. Run the app with LOG_PATH set and send some requests.")
    st.stop()

rows = load_requests(LOG_PATH)
if not rows:
    st.info("The log file exists but has no request lines yet.")
    st.stop()

durations = sorted(r["duration_ms"] for r in rows)
p95 = durations[min(len(durations) - 1, int(0.95 * len(durations)))]

col1, col2, col3 = st.columns(3)
col1.metric("Requests", len(rows))
col2.metric("5xx errors", sum(1 for r in rows if r["status"] >= 500))
col3.metric("p95 latency (ms)", round(p95, 2))

st.subheader("By route and status")
counts: dict[tuple, int] = {}
for r in rows:
    key = (r["method"], r["path"], r["status"])
    counts[key] = counts.get(key, 0) + 1
st.dataframe([
    {"method": m, "path": p, "status": s, "count": c}
    for (m, p, s), c in sorted(counts.items())
])

st.subheader("Recent requests")
st.dataframe(sorted(rows, key=lambda r: str(r["ts"]), reverse=True)[:50])
