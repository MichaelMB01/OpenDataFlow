# This file contains tests to verify the 
# structure of the DAG defined in dags/opendataflow_dag.py.
from pathlib import Path
# This file contains tests to verify 
# the structure of the DAG defined in dags/opendataflow_dag.py.
DAG_PATH = Path("dags/opendataflow_dag.py")

# Test that the DAG file exists and contains the expected structure.
def test_dag_file_exists():
    """Test that the DAG file exists."""
    assert DAG_PATH.exists()

# Test that the DAG file contains the expected DAG definition.
def test_dag_id_is_correct():
    dag_source = DAG_PATH.read_text(encoding="utf-8")

    # Verify that the DAG definition contains the expected dag_id.
    assert 'dag_id="opendataflow_pipeline"' in dag_source

# Test that all expected tasks are present in the DAG.
def test_all_task_names_are_present():
    dag_source = DAG_PATH.read_text(encoding="utf-8")

    # Define the expected task names in the DAG.
    expected_tasks = [
        "check_database_empty_task",
        "initialize_database_task",
        "clean_and_validate_data_task",
        "load_cleaned_data_task",
        "validate_database_task",
    ]

    # Verify that each expected task name is present in the DAG source code.
    for task_name in expected_tasks:
        assert task_name in dag_source

# Test that the database safety check is present in the DAG.
def test_the_database_safety_check_is_present():
    dag_source = DAG_PATH.read_text(encoding="utf-8")

    # Verify that the database safety check is present in the DAG source code.
    assert "Database safety check failed" in dag_source

# Test that the database schema initialization check is present in the DAG.
def test_dags_tasks_are_in_correct_order():
    dag_source = DAG_PATH.read_text(encoding="utf-8")

    # Define the expected order of task calls in the DAG source code.
    expected_order = [
        "database_is_empty = check_database_empty_task()",
        "schema_initialized = initialize_database_task(database_is_empty)",
        "expected_rows = clean_and_validate_data_task(schema_initialized)",
        "loaded_rows = load_cleaned_data_task(expected_rows)",
        "   validate_database_task(expected_rows, loaded_rows)",
    ]
    # Verify that the tasks are in the expected order in the DAG source code.
    for i in range(len(expected_order) - 1):
        first_task = expected_order[i]
        second_task = expected_order[i + 1]

        #Verify that the first task appears before the second task in the DAG source code.   
        first_index = dag_source.find(first_task)
        second_index = dag_source.find(second_task)

        # Assert that both tasks are found and that the first task appears 
        # before the second task.
        assert first_index != -1 and second_index != -1, (
            f"Could not find task call: '{first_task}' or '{second_task}'"
        )
        # Assert that the first task appears before 
        # the second task in the DAG source code.
        assert first_index < second_index, (
            f"Task '{first_task}' should come before '{second_task}'"
        )