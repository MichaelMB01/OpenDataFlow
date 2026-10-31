
# OpenDataFlow

OpenDataFlow is a Python data engineering portfolio project built around the NYC Yellow Taxi trip dataset for January 2024. It demonstrates data profiling, data quality checks, data cleaning, automated testing, Parquet storage, PostgreSQL integration components, and an Apache Airflow DAG.

The project is being developed incrementally, with an emphasis on reproducibility, validation, and safe data processing.

## Project Goals

- Build a maintainable data processing pipeline.
- Identify and investigate data quality issues.
- Clean and validate taxi trip records.
- Store processed data in Parquet format.
- Add automated tests for data processing and validation.
- Integrate PostgreSQL for structured data storage.
- Orchestrate pipeline steps with Apache Airflow.
- Document technical decisions and validation results.

## Technology Stack

- Python
- pandas
- PyArrow / Parquet
- pytest
- PostgreSQL
- psycopg2
- Apache Airflow
- Docker
- Git

## Dataset

This project uses NYC Yellow Taxi trip data for January 2024.

Download the dataset from the official NYC Taxi & Limousine Commission data portal:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Place the downloaded file at:

`data/raw/yellow_tripdata_2024-01.parquet`

The raw and processed datasets are excluded from Git using `.gitignore`.

## Current Features

- Data inspection and profiling.
- JSON data quality reporting.
- Detection of missing values, duplicates, unusual distances, negative fares, and invalid trip durations.
- Cleaning of records with missing timestamps or invalid trip durations.
- Parquet output and saved-file consistency checks.
- Data validation functions.
- PostgreSQL schema initialization and data-loading modules.
- Database validation and a pre-load safety check.
- An Airflow DAG defining the intended pipeline task dependencies.
- Automated tests for profiling, cleaning, validation, database-related behavior, and DAG structure.

## Project Structure

```text
OpenDataFlow/
├── dags/
│   └── opendataflow_dag.py
├── data/                    # Local data; excluded from Git
├── docs/
│   ├── cleaning_rules.md
│   └── data-profile.md
├── sql/
│   └── schema.sql
├── src/
│   ├── clean_data.py
│   ├── config.py
│   ├── init_db.py
│   ├── inspect_data.py
│   ├── load_data.py
│   ├── pipeline_checks.py
│   ├── profile_data.py
│   ├── run_cleaning.py
│   ├── run_pipeline.py
│   ├── validate_data.py
│   └── validate_database.py
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup

Run these commands from the project root in Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Ensure the January 2024 Parquet dataset is available at the path specified above.

## Run Data Cleaning

From the project root, with the virtual environment activated:

```powershell
python -m src.run_cleaning
```

This runs the local data-cleaning workflow. It is separate from running the complete database and Airflow pipeline.

## Run Tests

Run the test suite with:

```powershell
python -m pytest -v
```

At the latest recorded checkpoint, all 28 tests passed. Test results should be rerun after subsequent code changes.

## Configuration and Security

Database connection settings are read from environment variables:

- `PGHOST`
- `PGPORT`
- `PGDATABASE`
- `PGUSER`
- `PGPASSWORD`

Do not commit passwords, tokens, `.env` files, or other credentials. Local datasets and generated data files are excluded through `.gitignore`.

## Project Status

Implemented components include data profiling, data cleaning, validation functions, Parquet output, automated tests, PostgreSQL-related modules, and an Airflow DAG definition.

The automated test suite has passed at the latest recorded checkpoint. However, the actual Airflow DAG import and task graph still require validation in an Airflow environment. Full end-to-end execution against PostgreSQL has not been confirmed in this checkpoint.

The next milestones are to validate the DAG in a suitable environment, verify database integration safely, and establish automated checks through continuous integration.
