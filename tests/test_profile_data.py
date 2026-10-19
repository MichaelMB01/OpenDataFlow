import json
from pathlib import Path

def test_quality_report_exists():
    report_path = Path("data/processed/quality_report.json")
    assert report_path.exists()