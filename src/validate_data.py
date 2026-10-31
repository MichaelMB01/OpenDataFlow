import logging

import pandas as pd


logger = logging.getLogger(__name__)

REQUIRED_TIMESTAMP_COLUMNS = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
]


def validate_data(df):
    """Validate required timestamps and trip durations without modifying df."""

    # Check that both required columns exist.
    missing_columns = [
        column
        for column in REQUIRED_TIMESTAMP_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        logger.error("Required columns are missing: %s", missing_columns)
        return False

    # Convert timestamps into local Series, not back into the original DataFrame.
    pickup = pd.to_datetime(
        df["tpep_pickup_datetime"],
        format="mixed",
        errors="coerce",
    )

    dropoff = pd.to_datetime(
        df["tpep_dropoff_datetime"],
        format="mixed",
        errors="coerce",
    )

    # Missing timestamps and unparseable timestamp strings become NaT.
    invalid_timestamps = pickup.isna() | dropoff.isna()

    if invalid_timestamps.any():
        logger.warning(
            "Found %s rows with missing or invalid timestamps.",
            int(invalid_timestamps.sum()),
        )

    # Check duration only where both timestamps were parsed successfully.
    valid_timestamps = ~invalid_timestamps
    invalid_durations = (
        (dropoff <= pickup) & valid_timestamps
    )

    if invalid_durations.any():
        logger.warning(
            "Found %s trips with zero or negative duration.",
            int(invalid_durations.sum()),
        )

    # Data is valid only when all required timestamps and durations are valid.
    return not (
        invalid_timestamps.any()
        or invalid_durations.any()
    )