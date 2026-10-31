# Data Validation

## Purpose

The data validation module checks whether a DataFrame contains valid trip timestamps and durations before the data proceeds through the pipeline.

## Validation Rules

1. **Required columns:** Both `tpep_pickup_datetime` and `tpep_dropoff_datetime` must exist.
2. **Timestamp validity:** Missing timestamps and unparseable timestamp values are rejected.
3. **Trip duration:** Drop-off must occur strictly after pickup. Zero-duration and negative-duration trips are rejected.
4. **Data integrity:** Validation must not modify the original DataFrame.

## Implementation

The validation logic is implemented in `src/validate_data.py` using pandas.

- `pd.to_datetime()` converts timestamps for validation.
- `format="mixed"` supports values with different recognizable datetime formats.
- `errors="coerce"` converts unparseable values into `NaT`.
- Python logging records missing or invalid timestamps and trip durations.

The function returns `True` only when all validation checks pass; otherwise, it returns `False`.

## Testing

Unit tests are located in `tests/test_validate_data.py`. They cover valid data, missing columns, missing timestamps, invalid timestamp strings, zero-duration trips, negative-duration trips, and preservation of the original DataFrame.

The full project test suite currently passes **29 tests**.

## Scope and Limitations

This module validates required timestamp columns and trip durations. It does not validate every field, business rule, or database constraint in the dataset. Passing these checks does not guarantee that every trip record is otherwise correct.
