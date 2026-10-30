
import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

from src.load_data import load_data, COLUMN_MAPPING


def test_load_data_refuses_nonempty_table(tmp_path):
    # Create a small Parquet file with all required columns.
    data = {
        column: [1]
        for column in COLUMN_MAPPING
    }

    file_path = tmp_path / "test_data.parquet"
    pd.DataFrame(data).to_parquet(file_path)

    # Create mocks for the database connection and cursor.
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Configure the cursor context manager.
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    # Simulate a database table that already contains five rows.
    mock_cursor.fetchone.return_value = (5,)

    # Replace the real database connection with our mock.
    with patch("src.load_data.psycopg2.connect", return_value=mock_conn):
        with pytest.raises(
            ValueError,
            match="cleaned_trips is not empty"
        ):
            load_data(file_path)

    # Confirm that the loader checked the table before inserting.
    mock_cursor.execute.assert_called_once_with(
        "SELECT COUNT(*) FROM cleaned_trips"
    )

    # Confirm that the connection was closed.
    mock_conn.close.assert_called_once()

def test_load_data_rejects_empty_file(tmp_path):
    empty_df = pd.DataFrame(columns=COLUMN_MAPPING.keys())
    file_path = tmp_path / "empty_data.parquet"
    empty_df.to_parquet(file_path)

    # Mock the connection to prevent any real database access.
    with patch("src.load_data.psycopg2.connect") as mock_connect:
        with pytest.raises(ValueError, match="contains no rows"):
            load_data(file_path)

        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = (0,)

        # The loader should reject the empty file before connecting.
        mock_connect.assert_not_called()

def test_load_data_rolls_back_on_insert_failure(tmp_path):
    # Create a small Parquet file with all required columns.
    data = {
        column: [1]
        for column in COLUMN_MAPPING
    }

    file_path = tmp_path / "test_data.parquet"
    pd.DataFrame(data).to_parquet(file_path)

    # Create mocks for the database connection and cursor.
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Configure the cursor context manager.
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    # Simulate a database table that already contains zero rows.
    mock_cursor.fetchone.return_value = (0,)

    with patch("src.load_data.psycopg2.connect", return_value=mock_conn):
        # Mock the connection to prevent any real database access.
        with patch(
            "src.load_data.execute_values",
            side_effect=RuntimeError("Simulated insert failure")
        ) as mock_execute_values:
            with pytest.raises(
                RuntimeError, match="Simulated insert failure"
            ):
                load_data(file_path)

        mock_execute_values.assert_called_once()
    assert mock_conn.__exit__.call_args.args[0] is RuntimeError

