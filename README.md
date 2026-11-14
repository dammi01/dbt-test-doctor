# dbt-test-doctor

## Problem
When `dbt test` fails, the output lists SQL-level failures, and engineers have to open
compiled SQL to find the cause. dbt-test-doctor reads the dbt `run_results.json` file,
lists every failing or erroring test, classifies it (not_null, unique, relationships,
accepted_values, other) and suggests a fix.

## How to run
```bash
docker compose up --build
```
Open http://localhost:8000 and upload `tests/fixtures/run_results.json`.

## Run tests
```bash
pip install -r requirements.txt
pytest
```

## Deployment (described, not deployed)
The image is a single container with SQLite stored in a Docker volume. To deploy on any
container host (e.g. Render, Fly.io, Railway): create a web service from this repo, build
with the Dockerfile, set port 8000, and mount a persistent disk at `/app/data`.

## Specification
See `docs/SPEC.md`. Agent workflow: `docs/PROCESS.md`. Agent rules: `AGENTS.md`.
