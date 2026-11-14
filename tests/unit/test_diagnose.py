import json
from pathlib import Path

from app.diagnose import classify, diagnose

FIXTURE = Path(__file__).parents[1] / "fixtures" / "run_results.json"


def test_classify_generic_tests():
    assert classify("test.shop.not_null_orders_id.abc") == "not_null"
    assert classify("test.shop.unique_orders_id.def") == "unique"


def test_classify_singular_test_is_other():
    assert classify("test.shop.assert_total_positive.123") == "other"


def test_diagnose_ignores_passing_tests():
    findings = diagnose(json.loads(FIXTURE.read_text()))
    assert len(findings) == 2
    assert all(f.status in ("fail", "error") for f in findings)


def test_diagnose_empty_results():
    assert diagnose({"results": []}) == []
