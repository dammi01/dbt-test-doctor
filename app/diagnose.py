"""Classify failing dbt tests and suggest a fix. Pure logic, no network calls."""
from dataclasses import dataclass

SUGGESTIONS = {
    "not_null": "Find the rows with NULL in the column. Fill them upstream or relax the test if NULL is valid.",
    "unique": "Find the duplicated keys and deduplicate upstream, e.g. ROW_NUMBER() ... WHERE rn = 1.",
    "relationships": "Find orphan foreign keys. Check the join logic and the load order of the parent table.",
    "accepted_values": "Compare the unexpected values with the accepted list. Add them or fix the mapping.",
}
DEFAULT_SUGGESTION = "Open the compiled SQL in target/compiled and run it to see the failing rows."


@dataclass
class Diagnosis:
    test: str
    status: str
    category: str
    suggestion: str
    message: str


def classify(unique_id: str) -> str:
    """dbt generic tests look like test.<project>.<name>.<hash>; singular tests have no generic name."""
    parts = unique_id.split(".")
    name = parts[-2] if len(parts) >= 4 else unique_id
    for category in SUGGESTIONS:
        if name.startswith(category):
            return category
    return "other"


def diagnose(run_results: dict) -> list[Diagnosis]:
    findings = []
    for result in run_results.get("results", []):
        if result.get("status") not in ("fail", "error"):
            continue
        category = classify(result["unique_id"])
        findings.append(Diagnosis(
            test=result["unique_id"],
            status=result["status"],
            category=category,
            suggestion=SUGGESTIONS.get(category, DEFAULT_SUGGESTION),
            message=result.get("message") or "",
        ))
    return findings
