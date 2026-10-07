import pandas as pd
import numpy as np

df = pd.read_csv('raw_data.csv')
print("Columns count:", len(df.columns))
for i, col in enumerate(df.columns):
    print(f"{i:2d}: {repr(col)}")
