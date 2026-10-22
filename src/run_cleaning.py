# Import pandas for working with DataFrames and Parquet files.
import pandas as pd

# Import the cleaning function from our cleaning module.
from src.clean_data import transform

from src.validate_data import validate_data

# Load the original January 2024 taxi dataset from the raw data folder.
raw_data = pd.read_parquet("data/raw/yellow_tripdata_2024-01.parquet")

# Validate the raw DataFrame to check whether it meets
# the data quality rules defined in validate_data().
raw_data_is_valid =  validate_data(raw_data)


# Display the number of rows in the original dataset.
print("Original rows:",len(raw_data))

# Apply the cleaning function and store the result in a new DataFrame.
clean_data = transform(raw_data)

# Validate the cleaned DataFrame to check whether it meets
# the data quality rules defined in validate_data().
clean_data_is_valid = validate_data(clean_data)

print("Cleaned data is valid:", clean_data_is_valid)

# Check whether the cleaned data failed validation.
# The 'not' keyword means this condition is True when
# clean_data_is_valid is False.
if not clean_data_is_valid:

    # Raise an error to stop the pipeline if the cleaned
    # data does not pass validation.
    raise ValueError("Cleaned data validation failed")

# Display the number of rows remaining after cleaning.
print("Cleaned rows:", len(clean_data))

# Calculate how many rows were removed during cleaning.
print("Rows removed:", len(raw_data) - len(clean_data))

# Count missing pickup timestamps in the original dataset.
raw_data["tpep_pickup_datetime"].isna().sum()
print("Missing pickup timestamps:", raw_data["tpep_pickup_datetime"].isna().sum())

# Count missing drop-off timestamps in the original dataset.
raw_data["tpep_dropoff_datetime"].isna().sum()
print("Missing dropoff timestamps:", raw_data["tpep_dropoff_datetime"].isna().sum())

# Count trips where the drop-off timestamp is earlier than the pickup timestamp.
dropoff_before_pickup = (raw_data["tpep_dropoff_datetime"] < raw_data["tpep_pickup_datetime"]).sum()
print("Drop-off before pickup:", dropoff_before_pickup)
zero_duration_trips = (raw_data["tpep_pickup_datetime"] == raw_data["tpep_dropoff_datetime"] ).sum()
print("Zero_duration_trips:", zero_duration_trips) 

# Confirm that the original DataFrame still has its initial number of rows.
print("Raw rows after cleaning:",  len(raw_data))

# Save the cleaned DataFrame to a Parquet file in the processed data folder
clean_data.to_parquet("data/processed/yellow_tripdata_2024-01_clean.parquet")

# Read the saved Parquet file back into a new DataFrame.
# This checks that the saved file can be loaded successfully.
saved_data = pd.read_parquet("data/processed/yellow_tripdata_2024-01_clean.parquet")

# Compare the number of rows in the original cleaned DataFrame
# with the number of rows in the DataFrame loaded from the saved file.
# True means both DataFrames contain the same number of rows.
print(len(clean_data) == len(saved_data))

# Compare the column names and their order in both DataFrames.
# True means the saved data has the same columns in the same order.
print(saved_data.columns.equals(clean_data.columns))

# Count the number of duplicate rows in the cleaned DataFrame.
# A result of 0 means no exact duplicate rows were found.
print("Duplicate Row:", clean_data.duplicated().sum())