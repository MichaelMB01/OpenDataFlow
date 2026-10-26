import psycopg2
from src.config import DATABASE_CONFIG

def check_database_empty():
    # Connect to the PostgreSQL database using the settings from config.py.
    conn = psycopg2.connect(**DATABASE_CONFIG)

    try:

        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM cleaned_trips")
            actual_rows = cur.fetchone()[0]

            if actual_rows > 0:
                raise ValueError(
                    "The cleaned_trips table is already populated. "
                    "Stopping to prevent duplicate data."
                )

            return True

    finally:
        conn.close()