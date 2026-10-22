# Import pandas for working with DataFrames and Parquet files.
import pandas as pd

import logging

logging.basicConfig(level=logging.INFO, format= "%(levelname)s: %(message)s")

# Import the cleaning function from our cleaning module.
from src.clean_data import transform

from src.validate_data import validate_data

# Load the original January 2024 taxi dataset from the raw data folder.
raw_data = pd.read_parquet("data/raw/yellow_tripdata_2024-01.parquet")

# Validate the raw DataFrame to check whether it meets
# the data quality rules defined in validate_data().
raw_data_is_valid = validate_data(raw_data)


# Display the number of rows in the original dataset.
logging.info("Original rows: %s", len(raw_data))

# Apply the cleaning function and store the result in a new DataFrame.
clean_data = transform(raw_data)

# Validate the cleaned DataFrame to check whether it meets
# the data quality rules defined in validate_data().
clean_data_is_valid = validate_data(clean_data)

logging.info("Cleaned data is valid: %s", clean_data_is_valid)

# Check whether the cleaned data failed validation.
# The 'not' keyword means this condition is True when
# clean_data_is_valid is False.
if not clean_data_is_valid:

    # Raise an error to stop the pipeline if the cleaned
    # data does not pass validation.
    raise ValueError("Cleaned data validation failed")

# Display the number of rows remaining after cleaning.

logging.info("Cleaned rows: %s", len(clean_data))

# Calculate how many rows were removed during cleaning.
logging.info("Rows removed: %s", len(raw_data) - len(clean_data))

# Count missing pickup timestamps in the original dataset.
raw_data["tpep_pickup_datetime"].isna().sum()
logging.info("Missing pickup timestamps: %s", raw_data["tpep_pickup_datetime"].isna().sum())

# Count missing drop-off timestamps in the original dataset.
raw_data["tpep_dropoff_datetime"].isna().sum()

logging.info("Missing dropoff timestamps: %s", raw_data["tpep_dropoff_datetime"].isna().sum())

# Count trips where the drop-off timestamp is earlier than the pickup timestamp.
dropoff_before_pickup = (raw_data["tpep_dropoff_datetime"] < raw_data["tpep_pickup_datetime"]).sum()

logging.info("Drop-off before pickup: %s", dropoff_before_pickup)

zero_duration_trips = (raw_data["tpep_pickup_datetime"] == raw_data["tpep_dropoff_datetime"] ).sum()

logging.info("Zero_duration_trips: %s", zero_duration_trips)

# Confirm that the original DataFrame still has its initial number of rows.

logging.info("Raw rows after cleaning: %s",  len(raw_data))

# Save the cleaned DataFrame to a Parquet file in the processed data folder
clean_data.to_parquet("data/processed/yellow_tripdata_2024-01_clean.parquet")

# Read the saved Parquet file back into a new DataFrame.
# This checks that the saved file can be loaded successfully.
saved_data = pd.read_parquet("data/processed/yellow_tripdata_2024-01_clean.parquet")

# Compare the number of rows in the original cleaned DataFrame
# with the number of rows in the DataFrame loaded from the saved file.
# True means both DataFrames contain the same number of rows.

logging.info("Saved row count matches: %s", len(clean_data) == len(saved_data))

# Compare the column names and their order in both DataFrames.
# True means the saved data has the same columns in the same order.

logging.info("Saved columns match: %s", saved_data.columns.equals(clean_data.columns))

# Count the number of duplicate rows in the cleaned DataFrame.
# A result of 0 means no exact duplicate rows were found.

logging.info("Duplicate Row: %s", clean_data.duplicated().sum())