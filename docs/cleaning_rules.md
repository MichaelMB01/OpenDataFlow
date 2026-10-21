# OpenDataFlow — Data Cleaning Rules

## 1. Purpose

This document describes the data cleaning and validation process for the January 2024 NYC Yellow Taxi trip dataset in the OpenDataFlow project.

The goal is to transform raw taxi trip data into a cleaned Parquet dataset that can be used for further analysis and downstream data engineering tasks.

## 2. Input

The pipeline reads the original dataset from:

`data/raw/yellow_tripdata_2024-01.parquet`

The input is a Parquet file loaded into a Pandas DataFrame.

## 3. Output

The cleaned dataset is saved to:

`data/processed/yellow_tripdata_2024-01_clean.parquet`

The output is stored in Parquet format to preserve the tabular data structure and support efficient data processing.

## 4. Cleaning Rules

The transform() function applies the following cleaning steps:


1. Copies the raw DataFrame to avoid modifying the original data.

2. Removes rows with missing pickup or drop-off timestamps.

3. Calculates trip duration in minutes and stores it in trip_duration_minutes.

4. Removes trips where the drop-off timestamp is earlier than the pickup timestamp.

5. Removes trips with zero or negative trip duration.
## 5. Validation

The pipeline includes the following data quality checks:

- **Row counts:** Compare the number of rows in the raw and cleaned datasets.
- **Missing pickup timestamps:** Count missing values in `tpep_pickup_datetime`.
- **Missing drop-off timestamps:** Count missing values in `tpep_dropoff_datetime`.
- **Timestamp order:** Count trips where the drop-off timestamp is earlier than the pickup timestamp.
- **Zero-duration trips:** Count trips where pickup and drop-off timestamps are equal.
- **Raw data preservation:** Confirm that the original DataFrame retains its initial row count after transformation.
- **Saved file existence:** Confirm that the cleaned Parquet file exists.
- **Saved row-count validation:** Compare the row counts of `clean_data` and the reloaded `saved_data` DataFrames.
- **Column validation:** Compare the column names and their order between the cleaned and reloaded DataFrames.
- **Duplicate-row check:** Count exact duplicate rows in the cleaned dataset.

## 6. Latest Observed Results

The latest successful pipeline run produced these results:

| Metric | Result |
|---|---:|
| Original rows | 2,964,624 |
| Cleaned rows | 2,963,754 |
| Rows removed | 870 |
| Missing pickup timestamps in raw data | 0 |
| Missing drop-off timestamps in raw data | 0 |
| Drop-off before pickup in raw data | 56 |
| Zero-duration trips in raw data | 814 |
| Raw rows after cleaning | 2,964,624 |
| Saved versus cleaned row counts match | True |
| Saved versus cleaned columns match | True |
| Exact duplicate rows in cleaned data | 0 |

These results describe the latest observed run and should be updated if the pipeline logic or input data changes.

## 7. Limitations and Next Steps

- Review `src/clean_data.py` to document the exact transformation rules.
- Add automated tests for the cleaning function and data quality checks.
- Verify the saved dataset's schema and data types.
- Record any future changes to the cleaning rules in this document.

