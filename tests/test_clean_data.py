# Import pandas to create and compare DataFrames.
import pandas as pd

# Import the transform function that cleans the raw data.
from src.clean_data import transform

# Test that trips with zero duration are removed.
def test_remove_zero_duration_trip():

    # Create a small DataFrame with two trips.
    # The first trip has zero duration.
    # The second trip lasts 15 minutes.
    raw_data = pd.DataFrame({
        "tpep_pickup_datetime": pd.to_datetime([
            "2024-01-01 10:00:00",	
	        "2024-01-01 11:00:00",
        ]),

        "tpep_dropoff_datetime": pd.to_datetime([
            "2024-01-01 10:00:00",
            "2024-01-01 11:15:00",
        ]),
    })

    # Run the cleaning function on the test data.
    clean_data = transform(raw_data)

    # Confirm that only one trip remains.
    assert len(clean_data) == 1

    # Confirm that the remaining trip lasts exactly 15 minutes.
    assert clean_data["trip_duration_minutes"].iloc[0] == 15

# Test that trips with drop-off before pickup are removed.
def test_remove_dropoff_before_pickup_trip():

    # Create two trips.
    # The first trip has drop-off 10 minutes before pickup.
    # The second trip has a valid duration of 15 minutes.
    raw_data = pd.DataFrame({
        "tpep_pickup_datetime": pd.to_datetime([
            "2024-01-01 10:00:00",	
            "2024-01-01 11:00:00",
        ]),

        "tpep_dropoff_datetime": pd.to_datetime([
            "2024-01-01 09:50:00",
            "2024-01-01 11:15:00",
        ]),
    })

    # Clean the test data.
    clean_data = transform(raw_data)

    # Confirm that the invalid trip was removed.
    assert len(clean_data) == 1

    # Confirm that the remaining trip lasts 15 minutes.
    assert clean_data["trip_duration_minutes"].iloc[0] == 15

# Test that trips with missing timestamps are removed.
def test_remove_missing_timestamps_trip():

    # Create two trips.
    # The first trip has a missing pickup timestamp.
    # The second trip has valid timestamps.
    raw_data = pd.DataFrame({
        "tpep_pickup_datetime": pd.to_datetime([
            None,	
            "2024-01-01 11:00:00",
        ]),

        "tpep_dropoff_datetime": pd.to_datetime([
            "2024-01-01 10:15:00",
            "2024-01-01 11:15:00",
        ]),
    })


    # Clean the test data.
    clean_data = transform(raw_data)

    # Confirm that only the trip with valid timestamps remains.
    assert len(clean_data) == 1

    # Confirm that the remaining trip lasts 15 minutes.
    assert clean_data["trip_duration_minutes"].iloc[0] == 15


# Test that transform() does not modify the original DataFrame.
def test_transform_does_not_modify_original_data():

    # Create a DataFrame containing one zero-duration trip
    # and one valid 15-minute trip.
    raw_data = pd.DataFrame({
        "tpep_pickup_datetime": pd.to_datetime([
            "2024-01-01 10:00:00",	
            "2024-01-01 11:00:00",
        ]),

        "tpep_dropoff_datetime": pd.to_datetime([
            "2024-01-01 10:00:00",
            "2024-01-01 11:15:00",
        ]),
    })


    # Make a separate copy of the original data for comparison.
    original_data = raw_data.copy()

    # Run the cleaning function.
    clean_data = transform(raw_data)

    # Check that raw_data is still exactly the same as before.
    # This verifies that transform() did not change the input DataFram
    pd.testing.assert_frame_equal(original_data, raw_data)