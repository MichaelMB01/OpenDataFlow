# Import pandas to create a test DataFrame.
import pandas as pd

# Import the function we want to test.
from src.validate_data import validate_data

# Define a test function to check whether valid data passes validation.
def test_valid_data():
    # Create a DataFrame with valid pickup and drop-off timestamps.
    df = pd.DataFrame({
        # Record the pickup time for one taxi trip.
        "tpep_pickup_datetime": ["2024-01-01 10:00:00"],

        # Record the drop-off time 15 minutes after pickup.
        "tpep_dropoff_datetime": ["2024-01-01 10:15:00"]
    })

    # Run the validation function and check that the data is valid.
    # The assertion passes if validate_data(df) returns True.
    # If it returns False, Python raises an AssertionError.
    assert validate_data(df)

# Define a test to check whether missing pickup timestamps are detected.
def test_missing_pickup_timestamp():

    # Create a DataFrame containing one taxi trip.
    df = pd.DataFrame({
            # Use None to represent a missing pickup timestamp.
            "tpep_pickup_datetime": [None],
    
            # Provide a drop-off timestamp that is present.
            "tpep_dropoff_datetime": ["2024-01-01 10:15:00"]
        })

    # Assert that the validator returns False because the pickup timestamp is missing.
    # The test passes if the data is correctly marked as invalid.
    assert not validate_data(df)

# Define a test to check whether missing drop-off timestamps are detected.
def test_missing_dropoff_timestamp():
    # Create a DataFrame containing one taxi trip.
    df = pd.DataFrame({

         # Provide a valid pickup timestamp.
        "tpep_pickup_datetime": ["2024-01-01 10:00:00"],

        # Use None to represent a missing drop-off timestamp.
        "tpep_dropoff_datetime": [None]
    })

    # Check that the validator returns False because the drop-off timestamp is missing.
    # The test passes if the validator correctly identifies the data as invalid.
    assert not validate_data(df)

# Define a test to check whether the required drop-off column is missing.
def test_missing_dropoff_column():

    # Create a DataFrame containing one taxi trip.
    df = pd.DataFrame({

        # Provide a valid pickup timestamp.
        "tpep_pickup_datetime": ["2024-01-01 10:00:00"]
    })

    # Check that the validator returns False because the drop-off column is absent.
    assert not validate_data(df)


# Define a test to check whether zero-duration trips are rejected.
def test_zero_trip_duration():

    # Create a DataFrame containing one taxi trip.
    df = pd.DataFrame({

        # Set the pickup timestamp to 10:00 AM.
        "tpep_pickup_datetime": ["2024-01-01 10:00:00"],
    
        # Set the drop-off timestamp to the exact same time.
        # This makes the trip duration zero minutes.
        "tpep_dropoff_datetime": ["2024-01-01 10:00:00"]
        })

    # Check that the validator returns False for this invalid trip.
    # The test should pass only if zero-duration trips are rejected.
    assert not validate_data(df)

# Define a test to check whether trips with negative duration are rejected.
def test_negative_trip_duration():
    # Create a DataFrame containing one taxi trip.
    df = pd.DataFrame({

         # Set the pickup timestamp to 10:15 AM.
        "tpep_pickup_datetime": ["2024-01-01 10:15:00"],

        # Set the drop-off timestamp to 10:00 AM.
        # Drop-off happens 15 minutes before pickup, making the trip invalid.
        "tpep_dropoff_datetime": ["2024-01-01 10:00:00"]
    })

    # Check that the validator returns False for this invalid trip.
    assert not validate_data(df)