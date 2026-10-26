
# Import the function that initializes the PostgreSQL database schema.
# It creates the required tables if they do not already exist.
from src.init_db import init_db

# Import the main function from run_cleaning.py.
# This function cleans the raw taxi data and saves the cleaned dataset.
from src.run_cleaning import main as run_cleaning

# Import the function that loads the cleaned Parquet data into PostgreSQL.
from src.load_data import load_data

# Import the function that checks whether the database data is valid.
# It will compare the actual database row count with the expected row count.
from src.validate_database import validate_database

# Import a safety check that prevents the pipeline from loading data
# into a database table that already contains records.
from src.pipeline_checks import check_database_empty

# Define the main function that controls the entire pipeline.
def main():
    """Run the OpenDataFlow pipeline in a controlled order."""

    # STEP 1: Check that the cleaned_trips table is empty.
    # If it already contains rows, this function raises an error
    # and stops the pipeline before other operations begi
    check_database_empty()

    # STEP 2: Initialize the database schema.
    # Make sure the required database tables exist.
    init_db()

    # STEP 3: Run the data-cleaning workflow.
    # Store the number of cleaned rows returned by run_cleaning().
    # This number becomes the expected row count for database validation.
    expected_rows = run_cleaning() 

    # STEP 4: Load the cleaned dataset into PostgreSQL.
    # The loader inserts the cleaned records into the database table.
    load_data()

    # STEP 5: Validate the data stored in PostgreSQL.
    # Check that the actual row count matches expected_rows
    # and that the database passes the configured validation checks.
    validate_database(expected_rows)

    # STEP 6: Print this message only if all previous steps succeed.
    print("OpenDataFlow pipeline completed successfully.")

# Check whether this Python file is being run directly as a script.
# If it is, call main() to start the pipeline.
# This also allows other Python files to import this module
# without automatically running the entire pipeline.
if __name__ == "__main__":
    main()