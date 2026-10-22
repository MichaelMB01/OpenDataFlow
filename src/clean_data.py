# Import pandas for working with tabular data using DataFrames.
import pandas as pd

def transform(raw_data):
    """Clean taxi trip data and return a cleaned DataFrame."""

    # Make a copy so the original DataFrame is not modified.
    clean_data = raw_data.copy()

    # Remove rows where the pickup or drop-off timestamp is missing.
    clean_data = clean_data.dropna(subset=["tpep_pickup_datetime", "tpep_dropoff_datetime"])

    # Calculate each trip's duration in minutes.
    # Subtract the pickup timestamp from the drop-off timestamp.
    # Convert the time difference from seconds into minutes.
    clean_data["trip_duration_minutes"] = (
        clean_data["tpep_dropoff_datetime"]
        - clean_data["tpep_pickup_datetime"]
    ) .dt.total_seconds() / 60

    # Keep only rows where drop-off is at or after pickup.
    clean_data = clean_data[
        clean_data["tpep_dropoff_datetime"]
        >= clean_data["tpep_pickup_datetime"]
    ]

    # Remove trips with zero or negative durations.
    # Valid trips must last longer than zero minutes.
    clean_data = clean_data[
        clean_data["trip_duration_minutes"] > 0
    ]

    # Return the cleaned DataFrame to the code that called the function.
    return clean_data