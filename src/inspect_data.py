# Import Path to work with file and folder paths.
from pathlib import Path

# Import pandas to load and analyze tabular data.
import pandas as pd

# Define the location of the downloaded Parquet dataset.
data_path = Path("data/raw/yellow_tripdata_2024-01.parquet")

# Read the Parquet file into a pandas DataFrame called df.
df = pd.read_parquet(data_path)

# Print a message confirming that the dataset was loaded.
print("Dataset loaded successfully!")

# Print the total number of rows.
# The comma in : , formats large numbers with thousands separators.
print(f"Number of rows: {len(df):,}")

# Print the total number of columns.
print(f"Number of columns: {len(df.columns)}")

# Print a heading before displaying the column names.
print("\nColumn names:")

# Convert the column names to a regular Python list and display them.
print(df.columns.tolist())

# Print a heading before displaying the column data types.
print("\nColumn data types:")

# Display each column's data type, such as integer, float, or datetime.
print(df.dtypes)

# Print a heading before displaying a sample of the data.
print("\nFirst five rows:")

# Display the first five rows so you can inspect the dataset's contents.
print(df.head())
