# Import Path to work with file and folder paths.
from pathlib import Path

# Store the path to the original, uncleaned taxi dataset.
RAW_DATA_PATH = Path("data/raw/yellow_tripdata_2024-01.parquet")

# Store the directory where processed data will be saved.
PROCESSED_DATA_DIR = Path("data/processed")

# Store the filename to use for the cleaned taxi dataset.
CLEANED_DATA_FILENAME = "yellow_tripdata_2024-01_clean.parquet"

# Combine the processed-data directory and filename into one complete path.
# The / operator joins the two parts because PROCESSED_DATA_DIR is a Path object.
CLEANED_DATA_PATH = PROCESSED_DATA_DIR / CLEANED_DATA_FILENAME