# Import MagicMock to create fake objects for testing.
# Import patch to temporarily replace the real database connection.
from unittest.mock import MagicMock, patch

# Import pytest, a Python testing framework.
# We use it to write tests and check whether expected errors occur.
import pytest

# Import the module containing the function we want to test.
import src.pipeline_checks as pipeline_checks

# Replace psycopg2.connect with a mock during this test.
# pytest passes the mock connection function into mock_connect.
@patch("src.pipeline_checks.psycopg2.connect")
def test_check_database_empty_returns_true(mock_connect):

    # Create a fake database connection.
    # This prevents the test from connecting to the real database.
    mock_conn = MagicMock()

    # Make the mocked connect() function return our fake connection.
    mock_connect.return_value = mock_conn

    # Configure the fake cursor so fetchone() returns (0,).
    # The zero represents a table containing no rows.
    # __enter__.return_value represents the cursor inside the
    # 'with conn.cursor() as cur:' block in the production function.
    mock_conn.cursor.return_value.__enter__.return_value.fetchone.return_value = (0,)

    # Call the actual function we are testing.
    # It should detect the empty table and return True.
    result = pipeline_checks.check_database_empty()

    # Verify that the function returned True.
    # If it returns anything else, the test fails
    assert result is True

    # Verify that the function closed the database connection
    # exactly once, including its cleanup behavior.
    mock_conn.close.assert_called_once()

# Replace the real PostgreSQL connection with a mock during this test.
# The mock prevents the test from accessing the actual database.
@patch("src.pipeline_checks.psycopg2.connect")
def test_check_database_empty_raises_when_rows_exist(mock_connect):

    # Create a fake database connection for the test.
    mock_conn = MagicMock()

    # Make the mocked connect() function return our fake connection.
    mock_connect.return_value = mock_conn

    # Configure the fake cursor to return (10,).
    # The number 10 represents a table that already contains 10 rows.
    # This simulates the situation where loading must be blocked.
    mock_conn.cursor.return_value.__enter__.return_value.fetchone.return_value = (10,)

    # Tell pytest that ValueError is the expected outcome.
    # The test passes if check_database_empty() raises ValueError.
    # It fails if the function does not raise the expected exception.
    with pytest.raises(ValueError):
        pipeline_checks.check_database_empty()

    # Verify that the database connection was closed exactly once,
    # even though the function raised an exception.
    mock_conn.close.assert_called_once()
