# -*- coding: utf-8 -*-
import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('raw_data.csv')
tot_exp = pd.to_numeric(df['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE'], errors='coerce')
hh_size = pd.to_numeric(df['HOUSE HOLD SIZE'], errors='coerce')
df['pche'] = tot_exp / hh_size
mean_pche = df['pche'].mean()
pov_line = (2/3) * mean_pche
df['poor'] = (df['pche'] < pov_line).astype(int)

print(f"Mean PCHE: {mean_pche:.2f}")
print(f"Poverty line: {pov_line:.2f}")
print(f"Poor count: {df['poor'].sum()} ({df['poor'].mean()*100:.2f}%)")
print(f"Non-poor count: {(1-df['poor']).sum()} ({(1-df['poor']).mean()*100:.2f}%)")

print("\n============================================================")
print("1. SOCIOECONOMIC CATEGORICAL CHARACTERISTICS BY POVERTY STATUS")
print("============================================================")
cat_cols = [
    ('SEX', 'Gender'),
    ('MARITAL STATUS', 'Marital Status'),
    ('HIGHEST LEVEL OF EDUCATION', 'Education Level'),
    ('OTHER SOURCE OF INCOME', 'Other Income Source'),
    ('ACCESS TO CREDIT FOR YAM FARMING DURING LAST SEASON', 'Access to Credit'),
    ('ACCESS TO AGRICULTURAL EXTENSION', 'Extension Contact'),
    ('DO YOU USE IMPROVE YAM VARIETIES', 'Improved Yam Varieties'),
    ('DO  YOU APPLY FERTILIZER OR MANURE ON YOUR YAM FARM', 'Fertilizer / Manure Use'),
    ('DO YOU USE MODERN FARM TOOLS OR IMPROVED TECHNOLOGIES IN YAM PRODUCTION', 'Modern Tools / Technology'),
    ('MEMBER OF OOPERATIVE SOCIETY', 'Cooperative Membership')
]

for col_name, label in cat_cols:
    print(f"\n--- {label} ({col_name}) ---")
    vals = df[col_name].unique()
    for v in vals:
        sub = df[df[col_name] == v]
        p_sub = sub[sub['poor'] == 1]
        np_sub = sub[sub['poor'] == 0]
        
        p_n = len(p_sub)
        p_pct = (p_n / 13) * 100 # percentage within poor or percentage of total?
        # Let's check: in profile tables, usually we report n and % within poverty group, or within category, or of group total.
        print(f"  Category '{v}': Poor = {p_n} ({p_n/13*100:.2f}% of poor, {p_n/60*100:.2f}% of total) | Non-poor = {len(np_sub)} ({len(np_sub)/47*100:.2f}% of non-poor, {len(np_sub)/60*100:.2f}% of total) | Total = {len(sub)} ({len(sub)/60*100:.2f}%)")

print("\n============================================================")
print("2. CONTINUOUS CHARACTERISTICS BY POVERTY STATUS (MEAN +/- SD)")
print("============================================================")
num_cols = [
    ('AGE', 'Age (years)'),
    ('HOUSE HOLD SIZE', 'Household Size (persons)'),
    ('YEARS OF FARMING EXPERIENCE', 'Farming Experience (years)'),
    ('WHAT IS YOUR TOTAL FARM SIZE', 'Total Farm Size (ha)'),
    ('HOW MANY HECTARES ARE USED SPECIFICALLY FOR YAM FARMING', 'Yam Farm Area (ha)'),
    ('TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE', 'Total Monthly Expenditure (NGN)'),
    ('pche', 'Per-Capita Monthly Household Expenditure (PCHE, NGN)')
]

for col_name, label in num_cols:
    s = pd.to_numeric(df[col_name], errors='coerce')
    poor_vals = s[df['poor'] == 1]
    non_poor_vals = s[df['poor'] == 0]
    print(f"{label}:")
    print(f"  Poor (n=13):     Mean = {poor_vals.mean():.2f}, SD = {poor_vals.std():.2f}, Min = {poor_vals.min():.2f}, Max = {poor_vals.max():.2f}")
    print(f"  Non-poor (n=47): Mean = {non_poor_vals.mean():.2f}, SD = {non_poor_vals.std():.2f}, Min = {non_poor_vals.min():.2f}, Max = {non_poor_vals.max():.2f}")
    print(f"  Overall (N=60):  Mean = {s.mean():.2f}, SD = {s.std():.2f}, Min = {s.min():.2f}, Max = {s.max():.2f}")
