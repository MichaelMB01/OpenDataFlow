# Import pandas for working with DataFrames and Parquet files.
import pandas as pd

# Import Python's logging module to record pipeline progress and warnings.
import logging

# Import PyArrow to access its Parquet-related functionality
# and handle specific errors when reading Parquet files.
import pyarrow

from src.config import RAW_DATA_PATH, PROCESSED_DATA_DIR, CLEANED_DATA_PATH

# Configure logging to display INFO-level messages and above.
# The format shows the severity level (INFO, WARNING, ERROR, etc.)
# followed by the log message
logging.basicConfig(level=logging.INFO, format= "%(levelname)s: %(message)s")

# Import the cleaning function from our cleaning module.
from src.clean_data import transform

from src.validate_data import validate_data

def check_input_file(input_path):
    # Define a function that accepts the path of the input file.
    # input_path should be a pathlib.Path object.

    """Check whether the input file exists."""

    # Check if the input file exists at the specified path.
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")


def main():
    # Get the path to the raw January 2024 taxi dataset from the configuration.
    input_path = RAW_DATA_PATH

    # Check whether the input file exists before reading it.
    check_input_file(input_path)


    # Load the Parquet file into a pandas DataFrame.
    # This line runs only if the file exists.
    raw_data = pd.read_parquet(input_path)

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


    # Define the folder where the cleaned data will be saved.
    output_dir = PROCESSED_DATA_DIR

    # Create the output folder if it does not exist.
    # parents=True creates any missing parent folders.
    # exist_ok=True prevents an error if the folder already exists.
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build the complete output file path using the folder and filename.
    output_path = CLEANED_DATA_PATH

    # Attempt to save the cleaned DataFrame to the specified Parquet file.
    try:
        clean_data.to_parquet(output_path)

        # Log a message indicating that the cleaned data was saved successfully.
    except OSError as error:

        # Log the error message to help identify why saving failed.
        logging.error("Failed to save cleaned data: %s", error)

        # Re-raise the original exception to stop the pipeline from continuing.
        raise


    # Attempt to read the saved Parquet file into a new DataFrame.
    try:
        saved_data = pd.read_parquet(output_path)

    # Catch operating-system errors that occur while reading the file.
    except OSError as error:

        # Log the error message to help identify why reading failed.
        logging.error("Failed to read saved data: %s", error)

        # Re-raise the original exception to stop the pipeline from continuing.
        raise

    # Use pandas' built-in testing function to compare the cleaned DataFrame.
    # This checks that the saved data matches the original cleaned data
    pd.testing.assert_frame_equal(clean_data, saved_data)

    # If the assertion passes, log a message confirming that the saved data matches the cleaned data.
    logging.info("Saved data matches cleaned data: True")

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



if __name__ == "__main__":
    main()
