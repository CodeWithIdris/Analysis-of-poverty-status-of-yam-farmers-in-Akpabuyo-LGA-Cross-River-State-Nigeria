# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

df = pd.read_csv('raw_data.csv')
print(f"Loaded raw_data.csv with shape: {df.shape}")

# Map columns
sex_col = 'SEX'
age_col = 'AGE'
marital_col = 'MARITAL STATUS'
edu_col = 'HIGHEST LEVEL OF EDUCATION'
hh_size_col = 'HOUSE HOLD SIZE'
exp_years_col = 'YEARS OF FARMING EXPERIENCE'
other_income_col = 'OTHER SOURCE OF INCOME'
ext_col = 'ACCESS TO AGRICULTURAL EXTENSION'
coop_col = 'MEMBER OF OOPERATIVE SOCIETY'

food_exp_col = 'AVERAGE MONTHLY HOUSEHOLD FOOD EXPENDITURE'
edu_exp_col = 'AVERAGE MONTHLY HOUSEHOLD EXPENDITURE'
med_exp_col = 'AVERAGE MONTHLY HOUSEHOLD  MEDICAL EXPENDITURE'
util_exp_col = 'AVERAGE MONTHLY HOUSING AND UTILITY EXPENTITURE'
trans_exp_col = 'AVERAGE MONTHLY HOUSEHOLD TRANSPORTATION'
tot_exp_col = 'TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE'

farm_size_col = 'WHAT IS YOUR TOTAL FARM SIZE'
yam_area_col = 'HOW MANY HECTARES ARE USED SPECIFICALLY FOR YAM FARMING'
credit_col = 'ACCESS TO CREDIT FOR YAM FARMING DURING LAST SEASON'
improved_var_col = 'DO YOU USE IMPROVE YAM VARIETIES'
fert_col = 'DO  YOU APPLY FERTILIZER OR MANURE ON YOUR YAM FARM'
tools_col = 'DO YOU USE MODERN FARM TOOLS OR IMPROVED TECHNOLOGIES IN YAM PRODUCTION'

# Clean data
df['tot_exp'] = pd.to_numeric(df[tot_exp_col], errors='coerce')
df['hh_size'] = pd.to_numeric(df[hh_size_col], errors='coerce')
df['pche'] = df['tot_exp'] / df['hh_size']

mean_pche = df['pche'].mean()
pov_line = (2/3) * mean_pche
df['poor'] = (df['pche'] < pov_line).astype(int)

print(f"Mean PCHE: {mean_pche:.2f}")
print(f"Poverty Line: {pov_line:.2f}")
print(f"Poor count: {df['poor'].sum()} ({df['poor'].mean()*100:.2f}%)")
print(f"Non-poor count: {(1-df['poor']).sum()} ({(1-df['poor']).mean()*100:.2f}%)")

# Gender mapping
print("\nGender unique values:", df[sex_col].value_counts(dropna=False).to_dict())

# FGT calculation function
def calc_fgt(y, z, alpha):
    n = len(y)
    p_ind = (y < z).astype(int)
    gap = np.where(p_ind == 1, (z - y) / z, 0.0)
    w = gap ** alpha
    est = np.mean(w)
    s = np.std(w, ddof=1)
    ste = s / np.sqrt(n)
    lb = max(0.0, est - 1.96 * ste)
    ub = est + 1.96 * ste
    return est, ste, lb, ub, n, np.sum(p_ind)

print("\n--- FGT INDICES ---")
for a in [0.0, 1.0, 2.0]:
    est, ste, lb, ub, n, q = calc_fgt(df['pche'], pov_line, a)
    print(f"Overall alpha={a:.2f}: Estimate={est:.4f}, STE={ste:.4f}, LB={lb:.4f}, UB={ub:.4f}, N={n}, Poor={q}")

print("\n--- FGT BY GENDER ---")
for a in [0.0, 1.0, 2.0]:
    print(f"\nParameter alpha: {a:.2f}")
    for g_val in df[sex_col].unique():
        sub = df[df[sex_col] == g_val]
        est, ste, lb, ub, n, q = calc_fgt(sub['pche'], pov_line, a)
        print(f"Group '{g_val}': Est={est:.4f}, STE={ste:.4f}, LB={lb:.4f}, UB={ub:.4f}, N={n}, Poor={q}")
    est, ste, lb, ub, n, q = calc_fgt(df['pche'], pov_line, a)
    print(f"Population: Est={est:.4f}, STE={ste:.4f}, LB={lb:.4f}, UB={ub:.4f}, N={n}, Poor={q}")

