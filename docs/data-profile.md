# NYC Yellow Taxi Data Profile — January 2024

## 1. Overview

This report summarizes the structure, completeness, and data quality of the January 2024 NYC Yellow Taxi trip dataset used in the OpenDataFlow project.

The profiling script examines the raw Parquet dataset before cleaning, identifies missing values and duplicate records, and calculates trip-duration and financial-quality statistics.

## 2. Dataset Summary

| Metric | Result |
|---|---:|
| Dataset | NYC Yellow Taxi Trip Data |
| Reporting period | January 2024 |
| Source format | Parquet |
| Rows | 2,964,624 |
| Columns | 19 |
| Duplicate rows | 0 |

## 3. Column Structure and Data Types

The dataset contains 19 columns covering trip timestamps, passenger counts, trip distances, pickup and drop-off locations, payment information, fares, taxes, and surcharges.

The profiling script confirms that the pickup and drop-off timestamp columns use the `datetime64[us]` data type, allowing trip durations to be calculated through timestamp subtraction.

Other observed data types include `int32`, `int64`, `float64`, and `str`.

## 4. Missing-Value Analysis

Five columns contain missing values:

| Column | Missing values |
|---|---:|
| `passenger_count` | 140,162 |
| `RatecodeID` | 140,162 |
| `store_and_fwd_flag` | 140,162 |
| `congestion_surcharge` | 140,162 |
| `Airport_fee` | 140,162 |

No missing values were reported for the pickup or drop-off timestamps.

The profiling script also counted 140,162 rows where all five listed columns were missing simultaneously. This indicates that these missing values occur together in the same rows in this dataset.

These records should be assessed according to the project's cleaning rules rather than automatically removed solely because optional fields are missing.

## 5. Duplicate Records

The profiling run found **0 exact duplicate rows** in the raw dataset.

This check identifies records whose values match across all columns. It does not establish whether every trip represents a unique real-world journey.

## 6. Trip-Duration Analysis

Trip duration was calculated as the difference between drop-off and pickup timestamps, expressed in minutes.

| Metric | Result |
|---|---:|
| Average duration | 15.61 minutes |
| Median duration | 11.63 minutes |
| 99th percentile | 60.45 minutes |
| Longest observed duration | 9,455.4 minutes |
| Trips longer than 24 hours | 16 |
| Negative-duration trips | 56 |

The average duration is greater than the median, suggesting that longer trips influence the average.

The 16 trips exceeding 24 hours and the 56 trips with negative durations warrant further investigation. Negative-duration trips are invalid under the project's cleaning rules.

## 7. Financial and Distance Checks

The profiling run identified the following records:

| Check | Count |
|---|---:|
| Negative trip distance | 0 |
| Zero trip distance | 37,448 |
| Negative fare amount | 37,448 |
| Negative total amount | 35,504 |

Zero-distance trips and negative financial values should be investigated before deciding whether they are invalid. Negative amounts may reflect adjustments or refunds rather than data errors, so they should not be removed without a documented business rule.

## 8. Quality Report

The profiling script writes a JSON summary to:

`data/processed/quality_report.json`

The current report contains counts for:

- Duplicate rows
- Negative-duration trips
- Trips longer than 24 hours
- Negative fare rows
- Negative total-amount rows

The JSON report provides a machine-readable summary that can be used in later pipeline stages and automated quality checks.

## 9. Limitations and Next Steps

This profile describes the raw January 2024 dataset and the checks currently implemented in the profiling script.

Recommended follow-up work:

1. Review the unusually long and negative-duration trips.
2. Investigate zero-distance trips and negative financial values.
3. Document which missing fields are permitted and which should cause records to be rejected.
4. Expand automated tests to cover profiling outputs and quality-report contents.
5. Compare raw and cleaned dataset statistics to measure the effect of cleaning.

## 10. Reproducibility

The profile was generated using the project's Python profiling script and pandas. Counts and statistics in this report reflect the observed output from the January 2024 raw Parquet dataset.
