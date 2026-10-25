from unittest.mock import MagicMock, patch

import src.init_db as init_db_module

@patch("src.init_db.psycopg2.connect")
def test_init_db(mock_connect):
    mock_conn = MagicMock()

    mock_connect.return_value = mock_conn

    init_db_module.init_db()

    mock_cur = mock_conn.cursor.return_value.__enter__.return_value

    mock_connect.assert_called_once_with(**init_db_module.DATABASE_CONFIG)
    mock_cur.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()