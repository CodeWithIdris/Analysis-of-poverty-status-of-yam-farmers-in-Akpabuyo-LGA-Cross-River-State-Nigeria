# -*- coding: utf-8 -*-
import csv, math

with open('raw_data.csv', 'r', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

for r in rows:
    hh = float(r['HOUSE HOLD SIZE'])
    tot = float(r['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE'])
    r['pche'] = tot / hh
    r['sex_group'] = 'Male' if r['SEX'].strip() in ['1.0', '1'] else 'Female'

mean_pche = sum(r['pche'] for r in rows) / len(rows)
pov_line = (2.0 / 3.0) * mean_pche

for r in rows:
    r['poor'] = 1 if r['pche'] < pov_line else 0

males = [r for r in rows if r['sex_group'] == 'Male']
females = [r for r in rows if r['sex_group'] == 'Female']

def calc_fgt_exact(subset, z, alpha):
    n = len(subset)
    w_vals = []
    poor_count = 0
    for r in subset:
        y = r['pche']
        if y < z:
            poor_count += 1
            gap = (z - y) / z
            w_vals.append(gap ** alpha)
        else:
            w_vals.append(0.0)
    
    est = sum(w_vals) / n
    var = sum((w - est) ** 2 for w in w_vals) / (n - 1) if n > 1 else 0.0
    ste = math.sqrt(var / n) if n > 0 else 0.0
    lb = max(0.0, est - 1.96 * ste)
    ub = est + 1.96 * ste
    return {
        'n': n,
        'poor': poor_count,
        'estimate': est,
        'ste': ste,
        'lb': lb,
        'ub': ub,
        'pov_line': z
    }

print("=== EXACT FGT ANALYSIS DISAGGREGATED BY GENDER ===")
print(f"Mean PCHE = {mean_pche:.2f}, Poverty line = {pov_line:.2f}\n")

for alpha in [0.0, 1.0, 2.0]:
    print(f"--- Parameter alpha: {alpha:.2f} ---")
    res_m = calc_fgt_exact(males, pov_line, alpha)
    res_f = calc_fgt_exact(females, pov_line, alpha)
    res_pop = calc_fgt_exact(rows, pov_line, alpha)
    
    print(f"{'Group':<25} | {'Estimate':<10} | {'STE':<10} | {'LB':<10} | {'UB':<10} | {'Pov. line':<10}")
    print("-" * 80)
    print(f"{'Male (Group 1, n=36)':<25} | {res_m['estimate']:<10.4f} | {res_m['ste']:<10.4f} | {res_m['lb']:<10.4f} | {res_m['ub']:<10.4f} | {res_m['pov_line']:<10.2f}")
    print(f"{'Female (Group 2, n=24)':<25} | {res_f['estimate']:<10.4f} | {res_f['ste']:<10.4f} | {res_f['lb']:<10.4f} | {res_f['ub']:<10.4f} | {res_f['pov_line']:<10.2f}")
    print(f"{'Population (Overall, N=60)':<25} | {res_pop['estimate']:<10.4f} | {res_pop['ste']:<10.4f} | {res_pop['lb']:<10.4f} | {res_pop['ub']:<10.4f} | {res_pop['pov_line']:<10.2f}\n")

