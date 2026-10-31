
import pandas as pd

from src.validate_data import validate_data


def make_valid_data():
    """Create a small DataFrame containing valid trips."""
    return pd.DataFrame({
        "tpep_pickup_datetime": [
            "2024-01-01 10:00:00",
            "2024-01-01 11:00:00",
        ],
        "tpep_dropoff_datetime": [
            "2024-01-01 10:15:00",
            "2024-01-01 11:30:00",
        ],
    })


def test_valid_data_returns_true():
    df = make_valid_data()

    assert validate_data(df) is True


def test_missing_required_column_returns_false():
    df = make_valid_data().drop(
        columns=["tpep_pickup_datetime"]
    )

    assert validate_data(df) is False


def test_missing_timestamp_returns_false():
    df = make_valid_data()
    df.loc[0, "tpep_pickup_datetime"] = None

    assert validate_data(df) is False


def test_unparseable_timestamp_returns_false():
    df = make_valid_data()
    df.loc[0, "tpep_pickup_datetime"] = "not-a-date"

    assert validate_data(df) is False


def test_zero_duration_returns_false():
    df = make_valid_data()
    df.loc[0, "tpep_dropoff_datetime"] = (
        df.loc[0, "tpep_pickup_datetime"]
    )

    assert validate_data(df) is False


def test_negative_duration_returns_false():
    df = make_valid_data()
    df.loc[0, "tpep_dropoff_datetime"] = (
        "2024-01-01 09:59:00"
    )

    assert validate_data(df) is False


def test_validation_does_not_modify_original_dataframe():
    df = make_valid_data()
    original_df = df.copy(deep=True)

    validate_data(df)

    pd.testing.assert_frame_equal(df, original_df)
