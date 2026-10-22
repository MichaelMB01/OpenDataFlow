# Import pandas for working with tabular data using DataFrames.
import pandas as pd

# Import json for reading and writing data in JSON format.
import json

# Load the Parquet file into a DataFrame.
df = pd.read_parquet("data/raw/yellow_tripdata_2024-01.parquet")

# Print the shape of the DataFrame.
# The result contains (number of rows, number of columns).
print(df.shape)

# Count missing values in each column.
missing_values = df.isna().sum()
print(missing_values)

# Display only columns that contain one or more missing values.
print(missing_values[missing_values > 0])

# Count exact duplicate rows in the entire DataFrame.
duplicated_counts = df.duplicated().sum()
print(duplicated_counts)

# Count rows where both passenger_count and RatecodeID are missing.
missing_rows = (
    df["passenger_count"].isna()# Check for missing passenger counts.
    & df["RatecodeID"].isna()# Check missing rate codes.
    & df["store_and_fwd_flag"].isna()# Check missing forwarding flags.
    & df["congestion_surcharge"].isna()# Check missing surcharges.
    & df["Airport_fee"].isna()# Check missing airport fees.
    ) .sum()# Count rows where both conditions are True.

# Display the total number of rows where both values are missing.
print(missing_rows)

# Count trips with a negative distance
n_distance_count = (df["trip_distance"] < 0).sum()
print(n_distance_count)

# Count rows with a negative fare amount.
nf_amount_count = (df["fare_amount"] < 0).sum()
print(nf_amount_count)

# Count rows with a negative total amount.
nt_amount_count = (df["total_amount"] < 0 ).sum()
print(nt_amount_count)

# Count trips with a distance of exactly zero.
# Note: This replaces the previous value of n_distance_count
n_distance_count = (df["trip_distance"] == 0).sum()
print(n_distance_count)

# Count trips where pickup occurs before drop-off.
count_rs = (df["tpep_pickup_datetime"] < df["tpep_dropoff_datetime"]).sum()
print(count_rs)

# Count trips where drop-off occurs before pickup.
count_rsn = (df["tpep_dropoff_datetime"] < df["tpep_pickup_datetime"]).sum()
print(count_rsn)

# Calculate the duration of each trip in minutes.
# Subtract the pickup time from the drop-off time.
# Convert the time difference from seconds into minutes
trip_duration_minutes = (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]).dt.total_seconds() / 60
# Display the first five trip durations.
print(trip_duration_minutes.head())

# Find the longest trip duration in minutes.
longest_trip = trip_duration_minutes.max()
print(longest_trip)

# Count trips lasting longer than 24 hours (1,440 minutes).
count_long_trips = (trip_duration_minutes > 1440).sum()
print(count_long_trips)

# Count trips with a negative duration.
count_neg_trips = (trip_duration_minutes < 0).sum()
print(count_neg_trips)

# Calculate and print the average trip duration in minutes.
average_duration = trip_duration_minutes.mean()
print(average_duration)

# Calculate and print the median trip duration in minutes
median_duration = trip_duration_minutes.median()
print(median_duration)


# Calculate and print the 99th percentile of trip duration.
p99_duration = trip_duration_minutes.quantile(0.99)
print(p99_duration)

# Count trips whose duration exceeds the 99th percentile.
compare_trips_duration = (trip_duration_minutes > p99_duration).sum()
print(compare_trips_duration)

# Create a dictionary containing selected data quality metrics.
# Convert each count to a standard Python integer.
quality_summary = {
    "duplicate_rows": int(duplicated_counts),
    "negative_duration_trips": int(count_neg_trips),
    "trips_over_24_hours": int(count_long_trips),
    "negative_fare_rows": int(nf_amount_count),
    "negative_total_amount_rows": int(nt_amount_count)
}
# Print the quality summary dictionary in the terminal.
# This displays the data quality results.
print(quality_summary)

# Open the JSON report file in write mode ("w").
# If the file does not exist, Python creates it.
# If it already exists, its previous contents are overwritten
with open("data/processed/quality_report.json", "w") as file:
# Write the quality summary dictionary to the JSON file.
# indent=4 makes the JSON file easier to read
    json.dump(quality_summary, file, indent=4)

# Print the names of all columns in the DataFrame.
# This helps us inspect the dataset's structure
print(df.columns)


# Print the data type of each column.
# Examples include integers, floating-point numbers,
# strings, and datetime values.
print(df.dtypes)