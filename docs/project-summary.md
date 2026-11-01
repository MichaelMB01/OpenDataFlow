# OpenDataFlow — Project Summary

## 1. Project Overview

OpenDataFlow is a Python data engineering portfolio project that processes NYC Yellow Taxi trip data. It demonstrates data profiling, data cleaning, validation, automated testing, and the integration of tools commonly used in data engineering workflows.

The project is designed to make the data pipeline more reliable, testable, and maintainable.

## 2. Dataset

- **Source:** NYC Yellow Taxi trip data
- **Period:** January 2024
- **Format:** Parquet
- **Original dataset size:** 2,964,624 rows and 19 columns

The dataset contains trip timestamps, passenger counts, trip distances, fare amounts, payment information, and pickup and drop-off location identifiers.

## 3. Pipeline Architecture

The project is organized into separate modules for profiling, cleaning, validation, database operations, and orchestration.

The intended workflow is:

1. **Profile the raw data** to examine its structure and identify data quality issues.
2. **Clean the data** by applying timestamp and trip-duration rules.
3. **Validate the cleaned data** against defined quality requirements.
4. **Store processed data** in Parquet format and support PostgreSQL loading.
5. **Orchestrate pipeline tasks** using an Apache Airflow DAG.
6. **Run automated tests** to check important functions and pipeline structure.

## 4. Data Quality and Cleaning

Initial profiling identified duplicate rows, missing values, negative fare amounts, zero-distance trips, and invalid trip timestamps.

The cleaning process removes records with missing pickup or drop-off timestamps, trips where drop-off occurs before pickup, and trips with non-positive duration.

For the recorded cleaning run:

- **Original rows:** 2,964,624
- **Cleaned rows:** 2,963,754
- **Rows removed:** 870

The cleaned dataset is saved as a Parquet file under `data/processed/`.

## 5. Testing and Validation

The project includes eight test files covering data cleaning, data validation, profiling, database initialization and loading logic, pipeline checks, pipeline execution logic, and Airflow DAG structure.

The latest recorded local test checkpoint passed **29 tests**. This is a historical checkpoint, not a claim that the test suite was rerun after every subsequent change.

A GitHub Actions workflow checks that the Airflow DAG imports correctly and that its expected task structure and dependencies are present.

## 6. Technology Stack

- Python
- pandas
- PyArrow and Parquet
- PostgreSQL
- Apache Airflow
- pytest
- Git and GitHub
- GitHub Actions
- Docker

## 7. Current Limitations

Successful end-to-end execution against a live PostgreSQL database has not yet been confirmed. The presence of database-related modules and tests should not be interpreted as proof that the complete pipeline has run successfully against PostgreSQL.

The GitHub Actions workflow validates DAG structure; it does not execute the entire pipeline against a live database.

## 8. What This Project Demonstrates

OpenDataFlow provides practical evidence of work with:

- Data profiling and quality reporting
- Pandas-based data transformation
- Modular Python project organization
- Automated testing with pytest
- Parquet data storage
- PostgreSQL integration components
- Airflow DAG design
- Git-based version control and CI checks

## 9. Repository

[OpenDataFlow on GitHub](https://github.com/MichaelMB01/OpenDataFlow)
