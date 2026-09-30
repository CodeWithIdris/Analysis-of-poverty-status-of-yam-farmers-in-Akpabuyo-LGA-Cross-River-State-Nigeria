import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

df = pd.read_csv("raw_data.csv")
print("Data columns:")
for i, col in enumerate(df.columns):
    print(f"{i}: {col} (non-null: {df[col].notna().sum()}, unique: {df[col].nunique()})")

print("\nHead of data:")
print(df.head())
