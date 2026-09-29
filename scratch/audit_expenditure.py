import pandas as pd
import numpy as np

df = pd.read_csv('raw_data.csv')

food = df['AVERAGE MONTHLY HOUSEHOLD FOOD EXPENDITURE']
edu = df['AVERAGE MONTHLY HOUSEHOLD EXPENDITURE']  # Education expenditure
health = df['AVERAGE MONTHLY HOUSEHOLD  MEDICAL EXPENDITURE']
housing = df['AVERAGE MONTHLY HOUSING AND UTILITY EXPENTITURE']
trans = df['AVERAGE MONTHLY HOUSEHOLD TRANSPORTATION']

reported_total = df['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE']
calculated_sum = food + edu + health + housing + trans

diff = reported_total - calculated_sum
abs_diff = np.abs(diff)

print('=== EXPENDITURE RECONCILIATION AUDIT (N = 60) ===')
print(f'Mean Reported Total Expenditure: NGN {reported_total.mean():,.2f}')
print(f'Mean Calculated Component Sum:   NGN {calculated_sum.mean():,.2f}')
print(f'Sum of Reported Totals:          NGN {reported_total.sum():,.2f}')
print(f'Sum of Component Sums:           NGN {calculated_sum.sum():,.2f}')
print(f'Total Discrepancy (Sum of diffs): NGN {diff.sum():,.2f}')
print(f'Total Absolute Discrepancy:      NGN {abs_diff.sum():,.2f}')
print(f'Mean Discrepancy (Reported - Sum): NGN {diff.mean():,.2f}')
print(f'Exact Matches (diff == 0):       {(diff == 0).sum()} of 60')
print(f'Mismatches (diff != 0):          {(diff != 0).sum()} of 60')
print(f'Min Discrepancy (Reported - Sum): NGN {diff.min():,.2f}')
print(f'Max Discrepancy (Reported - Sum): NGN {diff.max():,.2f}')

mismatch_df = pd.DataFrame({
    'Row': df.index + 1,
    'Respondent_SN': df['Unnamed: 0'],
    'Food': food,
    'Education': edu,
    'Health': health,
    'Housing': housing,
    'Transportation': trans,
    'Calculated_Sum': calculated_sum,
    'Reported_Total': reported_total,
    'Discrepancy': diff
})

mismatches = mismatch_df[mismatch_df['Discrepancy'] != 0]
print(f'\nDetailed Breakdown of Mismatches ({len(mismatches)} rows):')
for idx, r in mismatches.iterrows():
    print(f"Row {int(r['Row']):2d} (S/N {r['Respondent_SN']:4.1f}): Food={r['Food']:,.0f}, Edu={r['Education']:,.0f}, Health={r['Health']:,.0f}, Housing={r['Housing']:,.0f}, Trans={r['Transportation']:,.0f} | Sum={r['Calculated_Sum']:,.0f} | Reported={r['Reported_Total']:,.0f} | Diff={r['Discrepancy']:,.0f}")
