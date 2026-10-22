# Import Python's built-in JSON module.
# It is used to read and write data in JSON format.
import json

# Import Path to work with file and folder paths.
from pathlib import Path

# Define a test to check whether the quality report exists.
def test_quality_report_exists():
     # Create a Path object pointing to the quality report file.
    report_path = Path("data/processed/quality_report.json")

    # Check whether the file exists at the specified location.
    # If it exists, the test passes.
    # If it does not exist, pytest reports a test failure.
    assert report_path.exists()