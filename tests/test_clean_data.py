import pandas as pd
from src.clean_data import transform

def test_remove_zero_duration_trip():
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

    clean_data = transform(raw_data)
    assert len(clean_data) == 1

    assert clean_data["trip_duration_minutes"].iloc[0] == 15


def test_remove_dropoff_before_pickup_trip():
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


    clean_data = transform(raw_data)

    assert len(clean_data) == 1

    assert clean_data["trip_duration_minutes"].iloc[0] == 15


def test_remove_missing_timestamps_trip():
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


    
    clean_data = transform(raw_data)

    assert len(clean_data) == 1

    assert clean_data["trip_duration_minutes"].iloc[0] == 15



def test_transform_does_not_modify_original_data():
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


    original_data = raw_data.copy()

    clean_data = transform(raw_data)

    pd.testing.assert_frame_equal(original_data, raw_data)