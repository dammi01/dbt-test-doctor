# Specification: dbt-test-doctor

## Problem
When `dbt test` fails, the output is a list of SQL-level failures. Engineers must open
compiled SQL and guess the cause. dbt-test-doctor reads the run results and explains
each failure with a category and a suggested fix.

## Functional requirements
1. Accept a dbt `run_results.json` file via the web form or `POST /upload`.
2. Return one finding per test with status `fail` or `error`. Passing tests are ignored.
3. Classify findings: `not_null`, `unique`, `relationships`, `accepted_values`, otherwise `other`.
4. Give each finding a suggested fix.
5. Save every diagnosis run to SQLite and list recent runs on the home page.
6. Return HTTP 400 for files that are not valid JSON or not dbt run results.

## Acceptance criteria
- AC1: Uploading `tests/fixtures/run_results.json` shows 2 failing tests.
- AC2: Each finding shows category and suggested fix.
- AC3: Each run appears in the "Recent reports" list after a restart.
- AC4: Invalid input returns 400.
- AC5: `pytest` passes locally and in CI.
- AC6: `docker compose up --build` starts the app on port 8001 with no other steps.
