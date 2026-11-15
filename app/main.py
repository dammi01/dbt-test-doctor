import json
from dataclasses import asdict
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app import db
from app.diagnose import diagnose
from app.logging_setup import RequestIdMiddleware, configure_logging

app = FastAPI(title="dbt-test-doctor")
configure_logging()
app.add_middleware(RequestIdMiddleware)

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

# ... parse_run_results, /health, /, /upload continuam iguais


def parse_run_results(raw: bytes) -> dict:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="File is not valid JSON")
    if not isinstance(data, dict) or "results" not in data:
        raise HTTPException(status_code=400, detail="Not a dbt run_results.json (missing 'results')")
    return data


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"reports": db.list_reports()})


@app.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...)):
    run_results = parse_run_results(await file.read())
    findings = [asdict(d) for d in diagnose(run_results)]
    report_id = db.save_report(findings)
    return templates.TemplateResponse(request, "index.html", {
        "reports": db.list_reports(),
        "findings": findings,
        "report_id": report_id,
    })
