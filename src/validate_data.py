# Import pandas for working with DataFrames.
import pandas as pd

def validate_data(df):
    """Check the quality of a DataFrame."""

     # Check whether both required timestamp columns exist.
    required_columns_exist = (
        "tpep_pickup_datetime" in df.columns 
        and "tpep_dropoff_datetime" in df.columns
        )

# Start by assuming the data is valid.
    is_valid = True

    # If either required column is missing, mark the data as invalid.
    if not required_columns_exist:
        is_valid = False

        # Explain why the data failed validation.
        print("required timestamp column is missing.")

    # Only check timestamp values if both columns exist.
    else:

        # Count missing pickup timestamps and check for missing drop-off timestamps.
        # If either column has one or more missing values, the condition is True.
        if (
            df["tpep_pickup_datetime"].isna().sum() > 0 
            or  df["tpep_dropoff_datetime"].isna().sum() > 0
            ):

            # Mark the data as invalid if missing timestamps are found.
            is_valid = False

            # Explain why the data failed validation.
            print("Missing timestamp values found.")



    # Convert the pickup timestamp column from strings to datetime values.
        df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])

        # Convert the drop-off timestamp column from strings to datetime values.
        df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])

        # Check whether any trip's drop-off time is earlier than or equal to its pickup time.
        if (df["tpep_dropoff_datetime"] <= df["tpep_pickup_datetime"]).any():

            # Mark the data as invalid if at least one trip has an invalid duration.
            is_valid = False

            # Display a message explaining the data-quality problem.
            print("Invalid trip duration found.")

    # Return the final validation result:
    # True if the data passes all checks, or False if any check fails.
    return is_valid

