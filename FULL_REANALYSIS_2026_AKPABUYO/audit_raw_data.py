import os
import pandas as pd
import numpy as np

# Load raw dataset
df = pd.read_csv('raw_data.csv')
print("Shape of raw_data.csv:", df.shape)
print("\nColumns and non-null counts:")
for i, col in enumerate(df.columns):
    val_cnt = df[col].count()
    null_cnt = df[col].isnull().sum()
    dtype = df[col].dtype
    unique_vals = df[col].dropna().unique()
    sample_vals = unique_vals[:5] if len(unique_vals) > 5 else unique_vals
    print(f"{i:2d} | {col:55s} | NonNull: {val_cnt:2d} | Null: {null_cnt:2d} | Dtype: {str(dtype):7s} | Unique: {len(unique_vals):2d} | Samples: {sample_vals}")

print("\n--- Detailed Summary of First 10 rows ---")
print(df.head(5).to_string())

