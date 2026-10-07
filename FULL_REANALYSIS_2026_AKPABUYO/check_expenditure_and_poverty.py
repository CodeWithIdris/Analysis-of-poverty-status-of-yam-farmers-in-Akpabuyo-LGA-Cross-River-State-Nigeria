import pandas as pd
import numpy as np

df = pd.read_csv('raw_data.csv')

# Check SEX = 2.0
print("--- SEX == 2.0 row ---")
print(df[df['SEX'] == 2][['Unnamed: 0', 'SEX', 'AGE', 'MARITAL STATUS', 'HOUSE HOLD SIZE']])

# Check missing values in challenges
print("\n--- Missing values in challenges ---")
print(df[['LOW AND UNSTABLE PRICES OF YAM']].isnull().sum())
print(df[df['LOW AND UNSTABLE PRICES OF YAM'].isnull()][['Unnamed: 0', 'LOW AND UNSTABLE PRICES OF YAM']])

# Expenditure audit
exp_cols = [
    'AVERAGE MONTHLY HOUSEHOLD FOOD EXPENDITURE',
    'AVERAGE MONTHLY HOUSEHOLD EXPENDITURE', # Education
    'AVERAGE MONTHLY HOUSEHOLD  MEDICAL EXPENDITURE',
    'AVERAGE MONTHLY HOUSING AND UTILITY EXPENTITURE',
    'AVERAGE MONTHLY HOUSEHOLD TRANSPORTATION'
]

df['comp_sum'] = df[exp_cols].sum(axis=1)
df['rep_total'] = df['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE']
df['diff'] = df['rep_total'] - df['comp_sum']
df['abs_diff'] = df['diff'].abs()
df['pct_diff'] = (df['diff'] / df['comp_sum']) * 100

discrepant = df[df['abs_diff'] > 0]
print(f"\n--- Expenditure Discrepancies ({len(discrepant)} / {len(df)}) ---")
print(f"Exact matches: {len(df) - len(discrepant)} ({(len(df) - len(discrepant))/len(df)*100:.2f}%)")
print(f"Total absolute discrepancy: {df['abs_diff'].sum():,.2f}")
print(f"Mean discrepancy: {df['abs_diff'].mean():,.2f}")
print(f"Max discrepancy: {df['abs_diff'].max():,.2f}")

print("\nDiscrepant rows:")
for idx, r in discrepant.iterrows():
    print(f"Respondent {int(r['Unnamed: 0'])}: Food={r[exp_cols[0]]:,.0f}, Educ={r[exp_cols[1]]:,.0f}, Med={r[exp_cols[2]]:,.0f}, House={r[exp_cols[3]]:,.0f}, Trans={r[exp_cols[4]]:,.0f} -> Sum={r['comp_sum']:,.0f} vs Reported={r['rep_total']:,.0f} (Diff={r['diff']:+,.0f}, Pct={r['pct_diff']:+.2f}%)")

# Poverty calculation under reported total
df['pche_rep'] = df['rep_total'] / df['HOUSE HOLD SIZE']
mean_pche_rep = df['pche_rep'].mean()
pov_line_rep = (2/3) * mean_pche_rep
df['poor_rep'] = (df['pche_rep'] < pov_line_rep).astype(int)

# Poverty calculation under component sum
df['pche_comp'] = df['comp_sum'] / df['HOUSE HOLD SIZE']
mean_pche_comp = df['pche_comp'].mean()
pov_line_comp = (2/3) * mean_pche_comp
df['poor_comp'] = (df['pche_comp'] < pov_line_comp).astype(int)

print("\n--- Poverty Classification Comparison ---")
print(f"Reported Total: Mean PCHE = {mean_pche_rep:,.2f}, Line = {pov_line_rep:,.2f}, Poor = {df['poor_rep'].sum()} ({df['poor_rep'].mean()*100:.2f}%), Non-poor = {(1-df['poor_rep']).sum()}")
print(f"Component Sum : Mean PCHE = {mean_pche_comp:,.2f}, Line = {pov_line_comp:,.2f}, Poor = {df['poor_comp'].sum()} ({df['poor_comp'].mean()*100:.2f}%), Non-poor = {(1-df['poor_comp']).sum()}")

# Agreement
crosstab = pd.crosstab(df['poor_rep'], df['poor_comp'], rownames=['Reported'], colnames=['Component'])
print("\nClassification Crosstab:")
print(crosstab)

diff_class = df[df['poor_rep'] != df['poor_comp']]
print(f"\nDiscrepant classification cases ({len(diff_class)}):")
for idx, r in diff_class.iterrows():
    print(f"Respondent {int(r['Unnamed: 0'])}: Size={r['HOUSE HOLD SIZE']}, Rep Total={r['rep_total']:,.0f} (PCHE={r['pche_rep']:,.2f} -> Poor={r['poor_rep']}) vs Comp Sum={r['comp_sum']:,.0f} (PCHE={r['pche_comp']:,.2f} -> Poor={r['poor_comp']})")

