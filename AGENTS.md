# AGENTS.md

## What this project is
dbt-test-doctor reads dbt `target/run_results.json`, finds failing or erroring tests,
classifies each failure, and suggests a fix. Web UI + SQLite, served by FastAPI.

## Where to look
- Problem and README: README.md
- Specification and acceptance criteria: docs/SPEC.md
- Agent team and workflow: docs/PROCESS.md
- Task tracker: GitHub Issues (one issue per task, with acceptance criteria)

## Commands
- Install: `uv venv && uv pip install -r requirements.txt`
- Run tests (unit + integration): `uv run pytest`
- Run the app: `docker compose up --build` then open http://localhost:8001

## Rules for agents
- All code, docs, comments and commit messages are in English.
- Every change maps to a GitHub Issue. Reference it in the commit (e.g. `Closes #1`).
- Run `pytest` before every commit.
- Add new dependencies to requirements.txt in the same commit, pinned to an exact version.
