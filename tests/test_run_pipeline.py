import pytest
from unittest.mock import Mock, call, patch
import src.run_pipeline as run_pipeline

def test_pipeline_stops_if_database_is_not_empty():
    with patch(
        "src.run_pipeline.check_database_empty",
        side_effect=ValueError("Database is not empty")
    ), patch("src.run_pipeline.init_db") as mock_init_db, \
         patch("src.run_pipeline.run_cleaning") as mock_run_cleaning, \
         patch("src.run_pipeline.load_data") as mock_load_data, \
         patch("src.run_pipeline.validate_database") as mock_validate_database:

        with pytest.raises(ValueError):
            run_pipeline.main()

        mock_init_db.assert_not_called()
        mock_run_cleaning.assert_not_called()
        mock_load_data.assert_not_called()
        mock_validate_database.assert_not_called()



def test_pipeline_runs_all_stages_successfully():
    with patch("src.run_pipeline.check_database_empty") as mock_check, \
         patch("src.run_pipeline.init_db") as mock_init_db, \
         patch("src.run_pipeline.run_cleaning") as mock_run_cleaning, \
         patch("src.run_pipeline.load_data") as mock_load_data, \
         patch("src.run_pipeline.validate_database") as mock_validate_database:

        
        parent = Mock()

    
        parent.attach_mock(mock_check, "check_database_empty")
        parent.attach_mock(mock_init_db, "init_db")
        parent.attach_mock(mock_run_cleaning, "run_cleaning")
        parent.attach_mock(mock_load_data, "load_data")
        parent.attach_mock(mock_validate_database, "validate_database")

        mock_run_cleaning.return_value = 100

        run_pipeline.main()

        assert parent.mock_calls == [
            call.check_database_empty(),
            call.init_db(),
            call.run_cleaning(),
            call.load_data(),
            call.validate_database(100),
        ]

        mock_check.assert_called_once()
        mock_init_db.assert_called_once()
        mock_run_cleaning.assert_called_once()
        mock_load_data.assert_called_once()

        mock_validate_database.assert_called_once_with(100)
        
