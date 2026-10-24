# OpenDataFlow

OpenDataFlow is a data engineering portfolio project built around the NYC Yellow Taxi trip dataset. It demonstrates data profiling, quality validation, data cleaning, automated testing, and pipeline logging using Python.

## Project Goals

- Work with public transportation data.
- Profile datasets and identify data quality issues.
- Validate raw and cleaned records.
- Transform and clean taxi trip data.
- Write processed data to Parquet files.
- Test data processing and validation behavior.
- Add PostgreSQL storage and Apache Airflow orchestration as future milestones.

## Technology Stack

- Python
- pandas
- PyArrow / Parquet
- pytest
- Git

PostgreSQL, Docker, and Apache Airflow are planned components of the broader project.

## Dataset

The project uses NYC Yellow Taxi trip data for January 2024.

Expected raw file location:

`data/raw/yellow_tripdata_2024-01.parquet`

Obtain the dataset from the official [NYC Taxi & Limousine Commission data portal](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) and place it in the directory above.

## Current Features

- Data inspection and profiling.
- A JSON data quality report.
- Cleaning of trips with missing timestamps, zero or negative durations, and drop-off times earlier than pickup times.
- Validation of raw and cleaned data.
- Parquet output and saved-file consistency checks.
- Logging for pipeline progress and data quality warnings.
- Automated tests using pytest.

## Project Structure

```text
OpenDataFlow/
├── airflow/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── src/
│   ├── clean_data.py
│   ├── inspect_data.py
│   ├── profile_data.py
│   ├── run_cleaning.py
│   └── validate_data.py
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup

Run these commands from the project root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Make sure the January 2024 Parquet dataset is available in `data/raw/`.

## Run the Pipeline

From the project root, with the virtual environment activated:

```powershell
python -m src.run_cleaning
```

## Run Tests

```powershell
python -m pytest tests -v
```

## Project Status

The initial profiling, cleaning, validation, automated testing, and logging milestones are complete.

Next milestones include further pipeline improvements, PostgreSQL integration, Docker-based execution, and Apache Airflow orchestration.
