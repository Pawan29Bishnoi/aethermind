"""Run with:  pytest -q   (no AI key needed - tests the validation layer)"""
import datetime as dt
from main import validate_extraction, mask_sensitive

def soon(n=3):
    return (dt.date.today() + dt.timedelta(days=n)).isoformat()

def test_valid_case():
    r = validate_extraction({"title": "Submit DBMS assignment", "due_date": soon(),
                             "priority": "High", "category": "Study"})
    assert r["status"] == "valid" and r["missing_fields"] == []

def test_missing_due_date():
    r = validate_extraction({"title": "Call the dentist", "due_date": None})
    assert r["status"] == "needs_review" and "due_date" in r["missing_fields"]

def test_not_a_task():
    r = validate_extraction({"title": None, "due_date": None})
    assert set(r["missing_fields"]) == {"title", "due_date"}

def test_past_date_rejected():
    past = (dt.date.today() - dt.timedelta(days=2)).isoformat()
    r = validate_extraction({"title": "Pay fees", "due_date": past})
    assert "due_date" in r["missing_fields"] and r["errors"]

def test_invalid_priority_rejected():
    r = validate_extraction({"title": "Gym", "due_date": soon(), "priority": "Super"})
    assert r["errors"] and r["data"]["priority"] is None

def test_optional_defaults_reported():
    r = validate_extraction({"title": "Gym", "due_date": soon()})
    assert set(r["defaults_used"]) == {"priority", "category"} and r["status"] == "valid"

def test_long_number_masked():
    assert "9876543210" not in mask_sensitive("call 9876543210 tomorrow")
