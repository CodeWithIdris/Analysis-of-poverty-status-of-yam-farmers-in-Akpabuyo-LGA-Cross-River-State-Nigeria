# -*- coding: utf-8 -*-
import csv, math

with open('raw_data.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total rows read: {len(rows)}")

# Extract data
records = []
for i, r in enumerate(rows):
    sex_raw = r.get('SEX', '').strip()
    # Map sex: 1=Male, 2=Female or 'Male'/'Female'
    # Let's inspect
    age = float(r['AGE']) if r['AGE'] else None
    hh_size = float(r['HOUSE HOLD SIZE']) if r['HOUSE HOLD SIZE'] else None
    tot_exp = float(r['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE']) if r['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE'] else None
    pche = tot_exp / hh_size if (tot_exp is not None and hh_size is not None and hh_size > 0) else None
    
    records.append({
        'id': i + 1,
        'sex_raw': sex_raw,
        'age': age,
        'hh_size': hh_size,
        'tot_exp': tot_exp,
        'pche': pche,
        'marital': r.get('MARITAL STATUS', '').strip(),
        'edu': r.get('HIGHEST LEVEL OF EDUCATION', '').strip(),
        'exp_years': float(r['YEARS OF FARMING EXPERIENCE']) if r.get('YEARS OF FARMING EXPERIENCE') else None,
        'other_income': r.get('OTHER SOURCE OF INCOME', '').strip(),
        'ext': r.get('ACCESS TO AGRICULTURAL EXTENSION', '').strip(),
        'coop': r.get('MEMBER OF OOPERATIVE SOCIETY', '').strip(),
        'farm_size': float(r['WHAT IS YOUR TOTAL FARM SIZE']) if r.get('WHAT IS YOUR TOTAL FARM SIZE') else None,
        'yam_area': float(r['HOW MANY HECTARES ARE USED SPECIFICALLY FOR YAM FARMING']) if r.get('HOW MANY HECTARES ARE USED SPECIFICALLY FOR YAM FARMING') else None,
        'credit': r.get('ACCESS TO CREDIT FOR YAM FARMING DURING LAST SEASON', '').strip(),
        'improved_var': r.get('DO YOU USE IMPROVE YAM VARIETIES', '').strip(),
        'fert': r.get('DO  YOU APPLY FERTILIZER OR MANURE ON YOUR YAM FARM', '').strip(),
        'tools': r.get('DO YOU USE MODERN FARM TOOLS OR IMPROVED TECHNOLOGIES IN YAM PRODUCTION', '').strip(),
    })

pches = [rec['pche'] for rec in records]
mean_pche = sum(pches) / len(pches)
pov_line = (2.0 / 3.0) * mean_pche

for rec in records:
    rec['poor'] = 1 if rec['pche'] < pov_line else 0

poor_count = sum(rec['poor'] for rec in records)
non_poor_count = len(records) - poor_count

print(f"Mean PCHE: {mean_pche:.2f}")
print(f"Poverty line: {pov_line:.2f}")
print(f"Poor: {poor_count}, Non-poor: {non_poor_count}")

# Check sex unique values
sex_vals = set(r['sex_raw'] for r in records)
print(f"Sex values: {sex_vals}")

# Group records by sex
males = [r for r in records if str(r['sex_raw']).lower() in ['1', '1.0', 'male', 'm']]
females = [r for r in records if str(r['sex_raw']).lower() in ['2', '2.0', 'female', 'f']]
print(f"Male count: {len(males)}, Female count: {len(females)}")

def get_fgt(rec_list, z, alpha):
    n = len(rec_list)
    if n == 0:
        return 0, 0, 0, 0, 0, 0
    w_list = []
    poor_n = 0
    for r in rec_list:
        y = r['pche']
        if y < z:
            poor_n += 1
            gap = (z - y) / z
            w_list.append(gap ** alpha)
        else:
            w_list.append(0.0)
    est = sum(w_list) / n
    variance = sum((w - est) ** 2 for w in w_list) / (n - 1) if n > 1 else 0.0
    ste = math.sqrt(variance / n) if n > 0 else 0.0
    lb = max(0.0, est - 1.96 * ste)
    ub = est + 1.96 * ste
    return est, ste, lb, ub, n, poor_n

print("\n--- DETAILED FGT BY GENDER ---")
for alpha in [0.0, 1.0, 2.0]:
    print(f"\nParameter alpha: {alpha:.2f}")
    print(f"{'Group':<15} | {'Estimate':<10} | {'STE':<10} | {'LB':<10} | {'UB':<10} | {'Pov. line':<10}")
    print("-" * 75)
    
    # Male
    est_m, ste_m, lb_m, ub_m, n_m, q_m = get_fgt(males, pov_line, alpha)
    print(f"{'Male (Group 1)':<15} | {est_m:<10.4f} | {ste_m:<10.4f} | {lb_m:<10.4f} | {ub_m:<10.4f} | {pov_line:<10.2f}")
    
    # Female
    est_f, ste_f, lb_f, ub_f, n_f, q_f = get_fgt(females, pov_line, alpha)
    print(f"{'Female (Group 2)':<15} | {est_f:<10.4f} | {ste_f:<10.4f} | {lb_f:<10.4f} | {ub_f:<10.4f} | {pov_line:<10.2f}")
    
    # Population
    est_p, ste_p, lb_p, ub_p, n_p, q_p = get_fgt(records, pov_line, alpha)
    print(f"{'Population':<15} | {est_p:<10.4f} | {ste_p:<10.4f} | {lb_p:<10.4f} | {ub_p:<10.4f} | {pov_line:<10.2f}")

