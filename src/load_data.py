
# Load cleaned taxi data into PostgreSQL in batches.

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

from src.config import CLEANED_DATA_PATH, DATABASE_CONFIG


# Number of rows to insert per batch.
BATCH_SIZE = 5000

# Map Parquet column names to PostgreSQL column names.
COLUMN_MAPPING = {
    "VendorID": "vendorid",
    "tpep_pickup_datetime": "tpep_pickup_datetime",
    "tpep_dropoff_datetime": "tpep_dropoff_datetime",
    "passenger_count": "passenger_count",
    "trip_distance": "trip_distance",
    "RatecodeID": "ratecodeid",
    "store_and_fwd_flag": "store_and_fwd_flag",
    "PULocationID": "pulocationid",
    "DOLocationID": "dolocationid",
    "payment_type": "payment_type",
    "fare_amount": "fare_amount",
    "total_amount": "total_amount",
    "congestion_surcharge": "congestion_surcharge",
    "Airport_fee": "airport_fee",
    "extra": "extra",
    "mta_tax": "mta_tax",
    "tip_amount": "tip_amount",
    "tolls_amount": "tolls_amount",
    "improvement_surcharge": "improvement_surcharge",
    "trip_duration_minutes": "trip_duration_minutes",
}


def load_data(file_path=CLEANED_DATA_PATH):
    """Load cleaned Parquet records into PostgreSQL in batches."""

    df = pd.read_parquet(file_path)

    # Confirm all required source columns exist.
    source_columns = list(COLUMN_MAPPING.keys())
    missing_columns = [
        column for column in source_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df.empty:
        raise ValueError("Cleaned data file contains no rows.")

    # Select columns in the required insert order.
    df = df[source_columns]

    # Convert pandas missing values to SQL NULL.
    df = df.astype(object).where(pd.notna(df), None)

    target_columns = list(COLUMN_MAPPING.values())
    column_sql = ", ".join(target_columns)
    insert_sql = f"INSERT INTO cleaned_trips ({column_sql}) VALUES %s"

    conn = psycopg2.connect(**DATABASE_CONFIG)

    try:
        with conn:
            with conn.cursor() as cur:
                # Refuse to append duplicate data on a rerun.
                cur.execute("SELECT COUNT(*) FROM cleaned_trips")
                existing_rows = cur.fetchone()[0]

                if existing_rows > 0:
                    raise ValueError(
                        "cleaned_trips is not empty. "
                        "Refusing to load duplicate data."
                    )

                records = df.itertuples(index=False, name=None)
                total_loaded = 0

                while True:
                    batch = []

                    try:
                        for _ in range(BATCH_SIZE):
                            batch.append(next(records))
                    except StopIteration:
                        pass

                    if not batch:
                        break

                    execute_values(
                        cur,
                        insert_sql,
                        batch,
                        page_size=BATCH_SIZE,
                    )

                    total_loaded += len(batch)
                    print(f"Loaded {total_loaded:,} rows")

        print(f"Finished loading {total_loaded:,} rows.")
        return total_loaded

    finally:
        conn.close()


if __name__ == "__main__":
    load_data()
