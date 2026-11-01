# OpenDataFlow

OpenDataFlow is a Python data engineering portfolio project built around the NYC Yellow Taxi trip dataset for January 2024. It demonstrates data profiling, data quality checks, data cleaning, automated testing, Parquet storage, PostgreSQL integration components, and Apache Airflow orchestration.

The project emphasizes reproducibility, validation, maintainable code, and safe data processing. It is developed incrementally, with automated tests and documentation supporting the implementation.

## Project Goals

- Build a maintainable data processing pipeline.
- Identify and investigate data quality issues.
- Clean and validate taxi trip records.
- Store processed data in Parquet format.
- Implement automated tests for data processing and validation.
- Integrate PostgreSQL for structured data storage.
- Define pipeline orchestration using Apache Airflow.
- Use continuous integration to check Airflow DAG structure.
- Document technical decisions, testing results, and known limitations.

## Technology Stack

- **Python** — data processing and pipeline logic
- **pandas** — data manipulation and transformation
- **PyArrow / Parquet** — columnar data storage
- **pytest** — automated testing
- **PostgreSQL** — structured data storage
- **psycopg2** — PostgreSQL connectivity
- **Apache Airflow** — workflow orchestration
- **Docker** — containerized development and database support
- **Git and GitHub** — version control and project hosting
- **GitHub Actions** — automated Airflow DAG validation

## Dataset

This project uses NYC Yellow Taxi trip data for January 2024.

Download the dataset from the official NYC Taxi & Limousine Commission data portal:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Place the downloaded Parquet file at:

`data/raw/yellow_tripdata_2024-01.parquet`

The raw and processed datasets are excluded from Git through `.gitignore`. This keeps large data files out of the repository.

## Current Features

### Data Profiling

- Inspect dataset dimensions, columns, and data types.
- Calculate missing values and identify columns containing missing data.
- Check for duplicate records.
- Investigate unusual trip distances, negative fares, and negative total amounts.
- Examine trip timestamp ordering and duration statistics.
- Generate a JSON data quality report.

### Data Cleaning

- Remove records with missing pickup or drop-off timestamps.
- Calculate trip durations in minutes.
- Exclude trips with invalid timestamp ordering.
- Exclude trips with zero or negative duration.
- Save cleaned data in Parquet format.
- Check saved-file consistency, including row counts and column structure.

### Data Validation

- Check that required timestamp columns exist.
- Detect missing or unparseable timestamps.
- Detect trips with zero or negative duration.
- Return validation results without modifying the original DataFrame.
- Use unit tests to verify expected validation behavior.

### PostgreSQL Integration Components

- Provide database configuration through environment variables.
- Define the database schema.
- Include database initialization and data-loading modules.
- Include database validation and a pre-load safety check.

These components demonstrate the intended database integration. Full end-to-end execution against PostgreSQL has not been confirmed.

### Airflow and Continuous Integration

- Define an Airflow DAG for the intended pipeline workflow.
- Organize tasks for database checks, initialization, cleaning and validation, loading, and database validation.
- Define task dependencies and safety checks.
- Include a GitHub Actions workflow that checks Airflow DAG imports, expected task IDs, and task dependencies.

The GitHub Actions workflow validates DAG structure; it does not execute the complete pipeline against the database.

### Automated Testing

The test suite covers data profiling, cleaning, validation, database-related behavior, pipeline control flow, and DAG structure.

## Project Structure

```text
OpenDataFlow/
├── .github/
│   └── workflows/
│       └── validate-airflow.yml
├── dags/
│   └── opendataflow_dag.py
├── data/
│   └── raw/                  # Local datasets; excluded from Git
├── docs/
│   ├── cleaning_rules.md
│   ├── data-profile.md
│   └── data-validation.md
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

The tree highlights the main project components. The `tests/` directory contains the automated test suite, and the `data/` directory is used for local datasets and generated outputs.

## Setup

Run these commands from the project root in Windows PowerShell.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Ensure the January 2024 Parquet dataset is available at the path specified in the Dataset section.

## Run Data Cleaning

From the project root, with the virtual environment activated, run:

```powershell
python -m src.run_cleaning
```

This runs the local data-cleaning workflow. It is separate from executing the complete database and Airflow pipeline.

The cleaning workflow reads the raw dataset, applies the implemented cleaning and validation logic, and writes the cleaned Parquet output.

## Run Tests

Run the automated test suite with:

```powershell
python -m pytest -v
```

At the most recent recorded local test checkpoint, **29 tests passed**.

This result describes the recorded test run; it is not a claim that tests have been rerun after every subsequent change.

## Configuration and Security

Database connection settings are read from environment variables:

- `PGHOST`
- `PGPORT`
- `PGDATABASE`
- `PGUSER`
- `PGPASSWORD`

Set these variables in the local environment when database connectivity is required.

Do not commit passwords, access tokens, `.env` files, or other credentials to Git.

The `.gitignore` file excludes local datasets, generated data files, and other files that should not be tracked. Review it before adding new files to the repository.

## Project Status

OpenDataFlow has implemented its main portfolio components:

- Data profiling and JSON quality reporting
- Data cleaning and Parquet output
- Data validation functions
- Automated unit tests
- PostgreSQL schema, initialization, loading, and validation modules
- An Apache Airflow DAG definition
- A GitHub Actions workflow for Airflow DAG validation
- Technical documentation

**Testing:** The most recent recorded local test run passed all 29 tests. The GitHub Actions workflow has been implemented to validate Airflow DAG imports, expected tasks, and task dependencies.

**Known limitations:** The Airflow checks validate DAG structure but do not execute its tasks. Full end-to-end execution against PostgreSQL has not been confirmed. Therefore, the project should not be described as a fully verified production pipeline.

**Development status:** Development is paused at the current scope. The existing implementation can be presented as a data engineering portfolio project, with its verified capabilities and remaining limitations clearly documented.

## Future Improvements

If development resumes, possible improvements include:

- Safely verifying the complete pipeline in a suitable test environment.
- Confirming end-to-end PostgreSQL integration.
- Adding further data quality metrics and monitoring.
- Improving pipeline observability and operational documentation.
- Expanding CI checks while keeping local resource requirements manageable.
