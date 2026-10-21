import pandas as pd
import json

# Load the Parquet file into a DataFrame.
df = pd.read_parquet("data/raw/yellow_tripdata_2024-01.parquet")
print(df.shape)
missing_values = df.isna().sum()
print(missing_values)
print(missing_values[missing_values > 0])
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

n_distance_count = (df["trip_distance"] < 0).sum()
print(n_distance_count)

nf_amount_count = (df["fare_amount"] < 0).sum()
print(nf_amount_count)

nt_amount_count = (df["total_amount"] < 0 ).sum()
print(nt_amount_count)

n_distance_count = (df["trip_distance"] == 0).sum()
print(n_distance_count)

count_rs = (df["tpep_pickup_datetime"] < df["tpep_dropoff_datetime"]).sum()
print(count_rs)

count_rsn = (df["tpep_dropoff_datetime"] < df["tpep_pickup_datetime"]).sum()
print(count_rsn)

trip_duration_minutes = (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]).dt.total_seconds() / 60
print(trip_duration_minutes.head())

longest_trip = trip_duration_minutes.max()
print(longest_trip)

count_long_trips = (trip_duration_minutes > 1440).sum()
print(count_long_trips)

count_neg_trips = (trip_duration_minutes < 0).sum()
print(count_neg_trips)

# Calculate the average duration
average_duration = trip_duration_minutes.mean()
print(average_duration)

# The median duration
median_duration = trip_duration_minutes.median()
print(median_duration)

# The 99th percentile
p99_duration = trip_duration_minutes.quantile(0.99)
print(p99_duration)

# Compare the trips duration
compare_trips_duration = (trip_duration_minutes > p99_duration).sum()
print(compare_trips_duration)

# Quality_summary
quality_summary = {
    "duplicate_rows": int(duplicated_counts),
    "negative_duration_trips": int(count_neg_trips),
    "trips_over_24_hours": int(count_long_trips),
    "negative_fare_rows": int(nf_amount_count),
    "negative_total_amount_rows": int(nt_amount_count)
}
print(quality_summary)

with open("data/processed/quality_report.json", "w") as file:
    json.dump(quality_summary, file, indent=4)

print(df.columns)
print(df.dtypes)