import pandas as pd
import numpy as np

df = pd.read_csv('raw_data.csv')
hh_size = df['HOUSE HOLD SIZE']

# 1. Reported Total
tot_rep = df['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE']
pche_rep = tot_rep / hh_size
mean_pche_rep = pche_rep.mean()
z_rep = (2/3) * mean_pche_rep
poor_rep = pche_rep < z_rep
q_rep = poor_rep.sum()

p0_rep = q_rep / len(df)
p1_rep = ((z_rep - pche_rep[poor_rep]) / z_rep).sum() / len(df)
p2_rep = (((z_rep - pche_rep[poor_rep]) / z_rep)**2).sum() / len(df)

# 2. Component Sum
comp_cols = ['AVERAGE MONTHLY HOUSEHOLD FOOD EXPENDITURE',
             'AVERAGE MONTHLY HOUSEHOLD EXPENDITURE',
             'AVERAGE MONTHLY HOUSEHOLD  MEDICAL EXPENDITURE',
             'AVERAGE MONTHLY HOUSING AND UTILITY EXPENTITURE',
             'AVERAGE MONTHLY HOUSEHOLD TRANSPORTATION']
comp_sum = df[comp_cols].sum(axis=1)
pche_comp = comp_sum / hh_size
mean_pche_comp = pche_comp.mean()
z_comp = (2/3) * mean_pche_comp
poor_comp = pche_comp < z_comp
q_comp = poor_comp.sum()

p0_comp = q_comp / len(df)
p1_comp = ((z_comp - pche_comp[poor_comp]) / z_comp).sum() / len(df)
p2_comp = (((z_comp - pche_comp[poor_comp]) / z_comp)**2).sum() / len(df)

print("=== REPORTED TOTAL EXPENDITURE ===")
print(f"Mean Household Expenditure: {tot_rep.mean():.2f}")
print(f"Mean PCHE:                 {mean_pche_rep:.2f}")
print(f"Poverty Line z (2/3 Mean): {z_rep:.2f}")
print(f"Poor Count:                {q_rep}")
print(f"Non-Poor Count:            {len(df) - q_rep}")
print(f"Headcount Ratio P0:        {p0_rep:.4f} ({p0_rep*100:.2f}%)")
print(f"Poverty Gap P1:            {p1_rep:.4f} ({p1_rep*100:.2f}%)")
print(f"Poverty Severity P2:       {p2_rep:.4f} ({p2_rep*100:.2f}%)")
print(f"Poor Mean PCHE:            {pche_rep[poor_rep].mean():.2f}")
print(f"Non-Poor Mean PCHE:        {pche_rep[~poor_rep].mean():.2f}")

print("\n=== COMPONENT SUM EXPENDITURE ===")
print(f"Mean Household Expenditure: {comp_sum.mean():.2f}")
print(f"Mean PCHE:                 {mean_pche_comp:.2f}")
print(f"Poverty Line z (2/3 Mean): {z_comp:.2f}")
print(f"Poor Count:                {q_comp}")
print(f"Non-Poor Count:            {len(df) - q_comp}")
print(f"Headcount Ratio P0:        {p0_comp:.4f} ({p0_comp*100:.2f}%)")
print(f"Poverty Gap P1:            {p1_comp:.4f} ({p1_comp*100:.2f}%)")
print(f"Poverty Severity P2:       {p2_comp:.4f} ({p2_comp*100:.2f}%)")
print(f"Poor Mean PCHE:            {pche_comp[poor_comp].mean():.2f}")
print(f"Non-Poor Mean PCHE:        {pche_comp[~poor_comp].mean():.2f}")

# Cross-tabulation of classifications
print("\n=== CLASSIFICATION COMPARISON ===")
crosstab = pd.crosstab(poor_rep.map({True:'Poor', False:'Non-Poor'}),
                       poor_comp.map({True:'Poor', False:'Non-Poor'}),
                       rownames=['Reported Total'], colnames=['Component Sum'])
print(crosstab)

mismatch = df[poor_rep != poor_comp]
print(f"\nMismatched cases count: {len(mismatch)}")
for idx, row in mismatch.iterrows():
    print(f"Respondent {idx+1}: Reported PCHE={pche_rep[idx]:.2f} (Poor={poor_rep[idx]}), Comp PCHE={pche_comp[idx]:.2f} (Poor={poor_comp[idx]})")
