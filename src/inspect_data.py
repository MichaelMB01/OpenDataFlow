
from pathlib import Path

import pandas as pd

# Locate the downloaded dataset.
data_path = Path("data/raw/yellow_tripdata_2024-01.parquet")

# Load the Parquet file into a DataFrame.
df = pd.read_parquet(data_path)

# Display basic information about the dataset.
print("Dataset loaded successfully!")
print(f"Number of rows: {len(df):,}")
print(f"Number of columns: {len(df.columns)}")

print("\nColumn names:")
print(df.columns.tolist())

print("\nColumn data types:")
print(df.dtypes)

print("\nFirst five rows:")
print(df.head())
