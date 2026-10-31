from datetime import datetime, timezone

from airflow.sdk import dag, task


@dag(
    dag_id="opendataflow_pipeline",
    start_date=datetime(2026, 10, 1, tzinfo=timezone.utc),
    schedule=None,
    catchup=False,
)
def opendataflow_pipeline():
    @task
    def check_database_empty_task():
        from src.pipeline_checks import check_database_empty

        return check_database_empty()

    @task
    def initialize_database_task(database_is_empty):
        if not database_is_empty:
            raise ValueError("Database safety check failed")

        from src.init_db import init_db

        init_db()
        return True

    @task
    def clean_and_validate_data_task(schema_initialized):
        if not schema_initialized:
            raise ValueError("Database schema initialization failed")

        from src.run_cleaning import main as run_cleaning

        expected_rows = run_cleaning()
        return expected_rows

    @task
    def load_cleaned_data_task(expected_rows):
        if expected_rows <= 0:
            raise ValueError("Expected row count must be positive")

        from src.load_data import load_data
        loaded_rows = load_data()

        if loaded_rows != expected_rows:
            raise ValueError("Loaded row count does not match expected row count")

        return loaded_rows

    @task
    def validate_database_task(expected_rows, loaded_rows):
        if expected_rows != loaded_rows:
            raise ValueError("Expected and loaded row counts do not match")

        from src.validate_database import validate_database

        return validate_database(expected_rows)

    database_is_empty = check_database_empty_task()
    schema_initialized = initialize_database_task(database_is_empty)
    expected_rows = clean_and_validate_data_task(schema_initialized)
    loaded_rows = load_cleaned_data_task(expected_rows)
    validate_database_task(expected_rows, loaded_rows)

opendataflow_pipeline()
