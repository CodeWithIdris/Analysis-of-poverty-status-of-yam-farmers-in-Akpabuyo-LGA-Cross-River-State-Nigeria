import pandas as pd
import numpy as np

df = pd.read_csv('raw_data.csv')

food = df['AVERAGE MONTHLY HOUSEHOLD FOOD EXPENDITURE']
educ = df['AVERAGE MONTHLY HOUSEHOLD EXPENDITURE'] # education
med = df['AVERAGE MONTHLY HOUSEHOLD  MEDICAL EXPENDITURE']
house = df['AVERAGE MONTHLY HOUSING AND UTILITY EXPENTITURE']
trans = df['AVERAGE MONTHLY HOUSEHOLD TRANSPORTATION']
tot_rep = df['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE']

comp_df = pd.DataFrame({
    'Food': food,
    'Education': educ,
    'Medical': med,
    'Housing': house,
    'Transport': trans
})

comp_sum_row = comp_df.sum(axis=1)

print("=== COMPONENT MEANS ===")
for col in comp_df.columns:
    print(f"{col:12s}: Mean = {comp_df[col].mean():.4f}, Sum = {comp_df[col].sum():.4f}")

print("\n=== SUMMARY OF COMPONENT SUMS ===")
print(f"Mean of row-level component sums: {comp_sum_row.mean():.6f}")
print(f"Sum of component means:           {comp_df.mean().sum():.6f}")
print(f"Total across all 60 households:   {comp_sum_row.sum():.4f}")
print(f"Mean reported total:              {tot_rep.mean():.6f}")
print(f"Total reported across 60 hh:      {tot_rep.sum():.4f}")

# Let's check if 113,985.83 was from something else or how it could be derived
print(f"\nDifference between sum of reported and sum of components: {tot_rep.sum() - comp_sum_row.sum():.4f}")
print(f"Difference in means: {tot_rep.mean() - comp_sum_row.mean():.6f}")

# Check individual components
print(f"Food mean:      {food.mean():.2f}")
print(f"Education mean: {educ.mean():.2f}")
print(f"Medical mean:   {med.mean():.2f}")
print(f"Housing mean:   {house.mean():.2f}")
print(f"Transport mean: {trans.mean():.2f}")
print(f"Sum of means =  {food.mean() + educ.mean() + med.mean() + house.mean() + trans.mean():.2f}")

