import pandas as pd
import numpy as np

df = pd.read_csv('raw_data.csv')

challenge_cols = [
    ('HIGH COST OF FARM INPUTS', 'High cost of farm inputs'),
    ('INADEQUATE ACCESS TO CREDIT', 'Inadequate access to credit'),
    ('PEST AND DISEASE INFESTATION', 'Pest and disease infestation'),
    ('UNPREDICTABLE RAINFALL AND CLIMATE CONDITIONS', 'Unpredictable rainfall and climate conditions'),
    ('HIGH COST AND SCARCITY OF FARM LABOUR', 'High cost and scarcity of farm labour'),
    ('HIGH COST/SCARCITY OF YAM STAKES', 'High cost/scarcity of yam stakes'),
    ('POOR ACCESS TO MARKET', 'Poor access to markets'),
    ('LOW AND UNSTABLE PRICES OF YAM', 'Low and unstable prices of yam'),
    ('INADEQUATE AGRICULTURAL EXTENSIONSERVICES', 'Inadequate agricultural extension services'),
    ('POST-HARVEST LOSSES AND INADEQUATE STORAGE FACILITIES', 'Post-harvest losses and inadequate storage facilities')
]

table_rows = []

for raw_col, label in challenge_cols:
    vals = df[raw_col].dropna()
    n_valid = len(vals)
    mean_val = vals.mean()
    sd_val = vals.std()
    med_val = vals.median()
    q25 = vals.quantile(0.25)
    q75 = vals.quantile(0.75)
    iqr_val = q75 - q25
    
    if 1.00 <= mean_val <= 1.80:
        interp = 'Not a Challenge'
    elif 1.81 <= mean_val <= 2.60:
        interp = 'Minor Challenge'
    elif 2.61 <= mean_val <= 3.40:
        interp = 'Moderate Challenge'
    elif 3.41 <= mean_val <= 4.20:
        interp = 'Severe Challenge'
    elif 4.21 <= mean_val <= 5.00:
        interp = 'Very Severe Challenge'
    else:
        interp = 'Out of Range'
        
    vc = vals.value_counts().to_dict()
    f1, f2, f3, f4, f5 = [int(vc.get(score, 0)) for score in [1.0, 2.0, 3.0, 4.0, 5.0]]
    p1, p2, p3, p4, p5 = [(f / n_valid) * 100 for f in [f1, f2, f3, f4, f5]]
    
    table_rows.append({
        'raw_col': raw_col,
        'Challenge': label,
        'n_valid': n_valid,
        'Mean': mean_val,
        'SD': sd_val,
        'Median': med_val,
        'IQR': iqr_val,
        'Q25': q25,
        'Q75': q75,
        'Interpretation': interp,
        'f1': f1, 'p1': p1,
        'f2': f2, 'p2': p2,
        'f3': f3, 'p3': p3,
        'f4': f4, 'p4': p4,
        'f5': f5, 'p5': p5
    })

res_df = pd.DataFrame(table_rows)
# Sort by Mean descending
res_df = res_df.sort_values(by=['Mean', 'SD'], ascending=[False, True]).reset_index(drop=True)
res_df['Rank'] = range(1, len(res_df) + 1)

print('=== TABLE 4.11: SEVERITY AND RANKING ===')
for idx, r in res_df.iterrows():
    print(f"{r['Rank']:2d} | {r['Challenge']:55s} | n={r['n_valid']:2d} | Mean={r['Mean']:.4f} | SD={r['SD']:.4f} | Median={r['Median']:.2f} (IQR={r['IQR']:.2f}) | {r['Interpretation']}")

print('\n=== FREQUENCY DISTRIBUTION (Counts & %) ===')
for idx, r in res_df.iterrows():
    print(f"{r['Rank']:2d} | {r['Challenge']:55s} | 1: {r['f1']:2d} ({r['p1']:5.1f}%) | 2: {r['f2']:2d} ({r['p2']:5.1f}%) | 3: {r['f3']:2d} ({r['p3']:5.1f}%) | 4: {r['f4']:2d} ({r['p4']:5.1f}%) | 5: {r['f5']:2d} ({r['p5']:5.1f}%)")
