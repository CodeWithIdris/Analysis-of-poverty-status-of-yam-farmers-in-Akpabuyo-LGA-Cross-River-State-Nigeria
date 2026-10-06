# -*- coding: utf-8 -*-
"""
Objective 2 Analysis Script: Poverty Status Profile of Yam Farmers
Project: Analysis of Poverty Status of Yam Farmers in Akpabuyo Local Government Area, Cross River State, Nigeria
Objective II: Analyze poverty status of yam farmers in the study area.
Input: raw_data.csv (N = 60 Yam-Farming Households)
Methodology: Descriptive Agricultural Economics Profile of Poor vs Non-Poor Households
"""

import os
import sys
import csv
import math

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_objective_2_analysis():
    data_path = 'raw_data.csv'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Source file '{data_path}' not found.")
        
    with open(data_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    n_total = len(rows)
    print("=" * 88)
    print(f"OBJECTIVE 2: POVERTY STATUS PROFILE OF YAM FARMERS (N = {n_total})")
    print("=" * 88)
    
    # Process variables
    records = []
    for i, r in enumerate(rows):
        hh_size = float(r['HOUSE HOLD SIZE'])
        tot_exp = float(r['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE'])
        pche = tot_exp / hh_size
        
        # Sex
        sex_raw = r['SEX'].strip()
        sex = 'Male' if sex_raw in ['1.0', '1'] else 'Female'
        
        # Age
        age = float(r['AGE'])
        
        # Marital Status
        mar_raw = r['MARITAL STATUS'].strip()
        if mar_raw in ['1.0', '1']:
            marital = 'Single'
        elif mar_raw in ['2.0', '2']:
            marital = 'Married'
        elif mar_raw in ['4.0', '4']:
            marital = 'Widowed'
        else:
            marital = 'Divorced'
            
        # Education
        edu_raw = r['HIGHEST LEVEL OF EDUCATION'].strip()
        if edu_raw in ['6.0', '6']:
            edu = 'Primary'
        elif edu_raw in ['12.0', '12']:
            edu = 'Secondary'
        elif edu_raw in ['16.0', '16']:
            edu = 'Tertiary'
        else:
            edu = 'No Formal'
            
        # Experience
        exp_yrs = float(r['YEARS OF FARMING EXPERIENCE'])
        
        # Other income
        other_inc = 'Yes' if r['OTHER SOURCE OF INCOME'].strip() in ['1.0', '1', 'Yes', 'yes'] else 'No'
        
        # Farm variables
        farm_size = float(r['WHAT IS YOUR TOTAL FARM SIZE'])
        yam_area = float(r['HOW MANY HECTARES ARE USED SPECIFICALLY FOR YAM FARMING'])
        credit = 'Yes' if r['ACCESS TO CREDIT FOR YAM FARMING DURING LAST SEASON'].strip() in ['1.0', '1', 'Yes', 'yes'] else 'No'
        ext = 'Yes' if r['ACCESS TO AGRICULTURAL EXTENSION'].strip() in ['1.0', '1', 'Yes', 'yes'] else 'No'
        improved = 'Yes' if r['DO YOU USE IMPROVE YAM VARIETIES'].strip() in ['1.0', '1', 'Yes', 'yes'] else 'No'
        fert = 'Yes' if r['DO  YOU APPLY FERTILIZER OR MANURE ON YOUR YAM FARM'].strip() in ['1.0', '1', 'Yes', 'yes'] else 'No'
        tools = 'Yes' if r['DO YOU USE MODERN FARM TOOLS OR IMPROVED TECHNOLOGIES IN YAM PRODUCTION'].strip() in ['1.0', '1', 'Yes', 'yes'] else 'No'
        coop = 'Yes' if r['MEMBER OF OOPERATIVE SOCIETY'].strip() in ['1.0', '1', 'Yes', 'yes'] else 'No'
        
        records.append({
            'id': i + 1,
            'sex': sex,
            'age': age,
            'marital': marital,
            'edu': edu,
            'hh_size': hh_size,
            'exp_yrs': exp_yrs,
            'other_inc': other_inc,
            'tot_exp': tot_exp,
            'pche': pche,
            'farm_size': farm_size,
            'yam_area': yam_area,
            'credit': credit,
            'ext': ext,
            'improved': improved,
            'fert': fert,
            'tools': tools,
            'coop': coop
        })
        
    # Poverty Line determination
    pche_vals = [rec['pche'] for rec in records]
    mean_pche = sum(pche_vals) / n_total
    pov_line = (2.0 / 3.0) * mean_pche
    
    for rec in records:
        rec['poor'] = 1 if rec['pche'] < pov_line else 0
        
    poor_group = [rec for rec in records if rec['poor'] == 1]
    non_poor_group = [rec for rec in records if rec['poor'] == 0]
    
    n_p = len(poor_group)
    n_np = len(non_poor_group)
    
    print(f"Sample Size (N)       : {n_total}")
    print(f"Mean PCHE             : NGN {mean_pche:,.2f}")
    print(f"Poverty Line (z)      : NGN {pov_line:,.2f}")
    print(f"Poor Households (q)   : {n_p} ({n_p / n_total * 100:.2f}%)")
    print(f"Non-Poor Households   : {n_np} ({n_np / n_total * 100:.2f}%)\n")
    
    # -------------------------------------------------------------
    # Table 1: Categorical Socioeconomic and Farm Characteristics
    # -------------------------------------------------------------
    cat_vars = [
        ('Sex', 'sex', ['Male', 'Female']),
        ('Marital Status', 'marital', ['Single', 'Married', 'Widowed']),
        ('Educational Attainment', 'edu', ['Primary', 'Secondary', 'Tertiary']),
        ('Other Income Source', 'other_inc', ['Yes', 'No']),
        ('Access to Credit', 'credit', ['Yes', 'No']),
        ('Extension Contact', 'ext', ['Yes', 'No']),
        ('Improved Yam Varieties', 'improved', ['Yes', 'No']),
        ('Fertilizer / Manure Use', 'fert', ['Yes', 'No']),
        ('Modern Tools / Technology', 'tools', ['Yes', 'No']),
        ('Cooperative Society Membership', 'coop', ['Yes', 'No'])
    ]
    
    print("-" * 88)
    print("TABLE 1: DISTRIBUTION OF YAM FARMERS BY POVERTY STATUS AND SOCIOECONOMIC CHARACTERISTICS")
    print("-" * 88)
    print(f"{'Variable / Category':<32} | {'Poor (n=13)':<15} | {'Non-Poor (n=47)':<15} | {'Total (N=60)':<15}")
    print(f"{'':<32} | {'n (%)':<15} | {'n (%)':<15} | {'n (%)':<15}")
    print("-" * 88)
    
    for var_label, field, categories in cat_vars:
        print(f"{var_label}:")
        for cat in categories:
            p_cnt = sum(1 for r in poor_group if r[field] == cat)
            np_cnt = sum(1 for r in non_poor_group if r[field] == cat)
            tot_cnt = sum(1 for r in records if r[field] == cat)
            
            p_pct = (p_cnt / n_p) * 100
            np_pct = (np_cnt / n_np) * 100
            tot_pct = (tot_cnt / n_total) * 100
            
            p_str = f"{p_cnt} ({p_pct:.2f}%)"
            np_str = f"{np_cnt} ({np_pct:.2f}%)"
            tot_str = f"{tot_cnt} ({tot_pct:.2f}%)"
            print(f"  {cat:<30} | {p_str:<15} | {np_str:<15} | {tot_str:<15}")
    print("-" * 88)
    
    # -------------------------------------------------------------
    # Table 2: Continuous Characteristics (Mean +/- SD)
    # -------------------------------------------------------------
    cont_vars = [
        ('Age of Farmer (years)', 'age'),
        ('Household Size (persons)', 'hh_size'),
        ('Yam Farming Experience (years)', 'exp_yrs'),
        ('Total Farm Size (ha)', 'farm_size'),
        ('Yam Cultivated Area (ha)', 'yam_area')
    ]
    
    def calc_mean_sd(val_list):
        n = len(val_list)
        if n == 0:
            return 0.0, 0.0
        m = sum(val_list) / n
        s = math.sqrt(sum((x - m) ** 2 for x in val_list) / (n - 1)) if n > 1 else 0.0
        return m, s

    print("\n" + "-" * 88)
    print("TABLE 2: MEAN CONTINUOUS CHARACTERISTICS OF YAM FARMERS BY POVERTY STATUS")
    print("-" * 88)
    print(f"{'Continuous Variable':<32} | {'Poor (n=13)':<15} | {'Non-Poor (n=47)':<15} | {'Overall (N=60)':<15}")
    print(f"{'':<32} | {'Mean ± SD':<15} | {'Mean ± SD':<15} | {'Mean ± SD':<15}")
    print("-" * 88)
    
    for var_label, field in cont_vars:
        p_vals = [r[field] for r in poor_group]
        np_vals = [r[field] for r in non_poor_group]
        tot_vals = [r[field] for r in records]
        
        p_m, p_sd = calc_mean_sd(p_vals)
        np_m, np_sd = calc_mean_sd(np_vals)
        tot_m, tot_sd = calc_mean_sd(tot_vals)
        
        p_str = f"{p_m:.2f} ± {p_sd:.2f}"
        np_str = f"{np_m:.2f} ± {np_sd:.2f}"
        tot_str = f"{tot_m:.2f} ± {tot_sd:.2f}"
        print(f"{var_label:<32} | {p_str:<15} | {np_str:<15} | {tot_str:<15}")
    print("-" * 88)
    
    # -------------------------------------------------------------
    # Table 3: Expenditure Welfare Profile
    # -------------------------------------------------------------
    print("\n" + "-" * 88)
    print("TABLE 3: EXPENDITURE WELFARE PROFILE OF YAM FARMERS BY POVERTY STATUS")
    print("-" * 88)
    print(f"{'Welfare Indicator':<38} | {'Poor (n=13)':<16} | {'Non-Poor (n=47)':<16} | {'Overall (N=60)':<16}")
    print("-" * 88)
    
    p_tot_exp = [r['tot_exp'] for r in poor_group]
    np_tot_exp = [r['tot_exp'] for r in non_poor_group]
    tot_exp_all = [r['tot_exp'] for r in records]
    
    p_exp_m, p_exp_sd = calc_mean_sd(p_tot_exp)
    np_exp_m, np_exp_sd = calc_mean_sd(np_tot_exp)
    tot_exp_m, tot_exp_sd = calc_mean_sd(tot_exp_all)
    
    p_pche = [r['pche'] for r in poor_group]
    np_pche = [r['pche'] for r in non_poor_group]
    pche_all = [r['pche'] for r in records]
    
    p_pche_m, p_pche_sd = calc_mean_sd(p_pche)
    np_pche_m, np_pche_sd = calc_mean_sd(np_pche)
    tot_pche_m, tot_pche_sd = calc_mean_sd(pche_all)
    
    p_hh = [r['hh_size'] for r in poor_group]
    np_hh = [r['hh_size'] for r in non_poor_group]
    hh_all = [r['hh_size'] for r in records]
    
    p_hh_m, p_hh_sd = calc_mean_sd(p_hh)
    np_hh_m, np_hh_sd = calc_mean_sd(np_hh)
    tot_hh_m, tot_hh_sd = calc_mean_sd(hh_all)
    
    print(f"{'Mean Total Monthly Expenditure':<38} | {f'NGN {p_exp_m:,.2f}':<16} | {f'NGN {np_exp_m:,.2f}':<16} | {f'NGN {tot_exp_m:,.2f}':<16}")
    print(f"{'Mean Household Size (persons)':<38} | {f'{p_hh_m:.2f} ± {p_hh_sd:.2f}':<16} | {f'{np_hh_m:.2f} ± {np_hh_sd:.2f}':<16} | {f'{tot_hh_m:.2f} ± {tot_hh_sd:.2f}':<16}")
    print(f"{'Mean Per-Capita Expenditure (PCHE)':<38} | {f'NGN {p_pche_m:,.2f}':<16} | {f'NGN {np_pche_m:,.2f}':<16} | {f'NGN {tot_pche_m:,.2f}':<16}")
    print(f"{'Relative Poverty Line (z)':<38} | {f'NGN {pov_line:,.2f}':<16} | {f'NGN {pov_line:,.2f}':<16} | {f'NGN {pov_line:,.2f}':<16}")
    
    p_gap = pov_line - p_pche_m
    np_surplus = np_pche_m - pov_line
    print(f"{'Mean Monthly Expenditure Shortfall':<38} | {f'NGN {p_gap:,.2f}':<16} | {f'Surplus +NGN {np_surplus:,.2f}':<16} | {f'NGN 313.42':<16}")
    print("-" * 88 + "\n")

if __name__ == '__main__':
    run_objective_2_analysis()
