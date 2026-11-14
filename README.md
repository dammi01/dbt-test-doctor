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

## Live deployment

- **URL:** https://dbt-test-doctor.onrender.com
- **Health check:** https://dbt-test-doctor.onrender.com/health

## Deployment notes

The app is deployed on Render's free tier. Render sets the `PORT` environment
variable, and the container reads it at startup (`${PORT:-8000}` in the `Dockerfile`).

The free tier has no persistent disk, so the SQLite database (`DB_PATH`) is
ephemeral: data is lost on every new deploy or restart. Persistent storage
would require a paid plan with a disk or an external database.

Free instances spin down after about 15 minutes without traffic. The first
request after that can take around 50 seconds.

## Alerting

An external UptimeRobot monitor checks `/health` every 5 minutes. It sends an
email alert when the service goes down and another when it recovers. This
confirms the application responds; it does not cover failures inside the
database layer.
