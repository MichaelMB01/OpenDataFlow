# This file contains configuration settings for the project
#including paths to data files and database connection settings.
import os

# Import Path to work with file and folder paths.
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the folder where the original, uncleaned datasets are stored.
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# Store the filename of the original, uncleaned taxi dataset.
RAW_DATA_FILENAME = "yellow_tripdata_2024-01.parquet"

# Combine the raw-data directory and filename into one complete path.
RAW_DATA_PATH = RAW_DATA_DIR / RAW_DATA_FILENAME


# Store the directory where processed data will be saved.
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

# Store the filename to use for the cleaned taxi dataset.
CLEANED_DATA_FILENAME = "yellow_tripdata_2024-01_clean.parquet"

# Combine the processed-data directory and filename into one complete path.
# The / operator joins the two parts because PROCESSED_DATA_DIR is a Path object.
CLEANED_DATA_PATH = PROCESSED_DATA_DIR / CLEANED_DATA_FILENAME


# PostgreSQL connection settings.
# The default port is 5433 because Windows PostgreSQL uses port 5432.
DB_HOST = os.getenv("PGHOST", "127.0.0.1")
DB_PORT = int(os.getenv("PGPORT", "5433"))
DB_NAME = os.getenv("PGDATABASE", "opendataflow")
DB_USER = os.getenv("PGUSER", "opendataflow")

# Read the password from the environment; do not store it in this file.
DB_PASSWORD = os.getenv("PGPASSWORD")

# Group the settings for use by psycopg2.
DATABASE_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
}
