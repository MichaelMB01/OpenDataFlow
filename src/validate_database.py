# This file contains functions to validate the database after loading data into it.
import psycopg2

# Import the database connection settings from config.py.
from src.config import DATABASE_CONFIG

# Define a function to validate the cleaned_trips table in the database.
def validate_database(expected_rows):
    """Validate the loaded cleaned_trips table."""
    # Connect to the PostgreSQL database using the settings from config.py.
    with psycopg2.connect(**DATABASE_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM cleaned_trips")
            actual_rows = cur.fetchone()[0]
            # Check for missing trip IDs in the cleaned_trips table.
            cur.execute(
                "SELECT COUNT(*) FROM cleaned_trips "
                "WHERE trip_id IS NULL"
            )
            missing_ids = cur.fetchone()[0]

    results = {
        "expected_rows": expected_rows,
        "actual_rows": actual_rows,
        "row_counts_match": actual_rows == expected_rows,
        "missing_trip_ids": missing_ids,
        "trip_ids_valid": missing_ids == 0,
    }
    # Print the validation results to the console.
    for name, value in results.items():
        print(f"{name}: {value}")

    # Raise an error if the row counts do not match or if there are missing trip IDs.
    if not results["row_counts_match"]:
        raise ValueError("Database row count does not match source.")
    if not results["trip_ids_valid"]:
        raise ValueError("Some trips have missing trip IDs.")

    return results


if __name__ == "__main__":
    validate_database(expected_rows=2_963_754)
