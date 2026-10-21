import pandas as pd

def transform(raw_data):
    """Clean taxi trip data and return a cleaned DataFrame."""
    clean_data = raw_data.copy()

    #Remove rows missing pickup or drop-off timestamps.
    clean_data = clean_data.dropna(subset=["tpep_pickup_datetime", "tpep_dropoff_datetime"])

    #Calculate trip duration in minutes.
    clean_data["trip_duration_minutes"] = (
        clean_data["tpep_dropoff_datetime"]
        - clean_data["tpep_pickup_datetime"]
    ) .dt.total_seconds() / 60

    # Remove rows where drop-off is before pickup.
    clean_data = clean_data[
        clean_data["tpep_dropoff_datetime"]
        >= clean_data["tpep_pickup_datetime"]
    ]

    # Remove rows with zero or negative trip duration.
    clean_data = clean_data[
        clean_data["trip_duration_minutes"] > 0
    ]

    return clean_data