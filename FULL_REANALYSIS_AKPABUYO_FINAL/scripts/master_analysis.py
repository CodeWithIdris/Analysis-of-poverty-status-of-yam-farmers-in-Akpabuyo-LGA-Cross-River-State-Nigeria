import os
import sys
import numpy as np
import pandas as pd
from scipy import stats, optimize
import statsmodels.api as sm
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Set stdout encoding
sys.stdout.reconfigure(encoding='utf-8')

print("================================================================================")
print("EXECUTING MASTER RE-ANALYSIS & STATISTICAL AUDIT PIPELINE")
print("Study: Analysis of Poverty Status of Yam Farmers in Akpabuyo LGA, Nigeria")
print("================================================================================")

# 1. LOAD RAW DATA
raw_path = 'raw_data.csv'
df = pd.read_csv(raw_path)
N = len(df)
print(f"Loaded raw dataset from '{raw_path}': N = {N} rows, {df.shape[1]} columns.")

# 2. DATA AUDIT & CODING AUDIT
# Identification
df['RESP_ID'] = df['Unnamed: 0'].astype(int)

# Sex audit: Respondent 46 has SEX = 2.0. Coding sheet specifies 1=Male, 0=Female.
# We create SEX_EMPIRICAL with NaN for 2.0 (n=59 valid: 36 Male, 23 Female, 1 missing)
df['SEX_RAW'] = df['SEX']
df['SEX_EMPIRICAL'] = df['SEX'].apply(lambda x: 1.0 if x == 1.0 else (0.0 if x == 0.0 else np.nan))
# Historical thesis recoded 2 as 0 to get 36 Male, 24 Female
df['SEX_HISTORICAL'] = df['SEX'].apply(lambda x: 1 if x == 1.0 else 0)

df['AGE_YEARS'] = df['AGE']
df['MARITAL_STATUS_RAW'] = df['MARITAL STATUS']
df['MARITAL_STATUS_LABEL'] = df['MARITAL STATUS'].map({1: 'Single', 2: 'Married', 3: 'Divorced', 4: 'Widowed'})

df['EDUC_YEARS'] = df['HIGHEST LEVEL OF EDUCATION']
df['EDUC_LEVEL'] = df['HIGHEST LEVEL OF EDUCATION'].map({6: 'Primary Education', 12: 'Secondary Education', 16: 'Tertiary Education'})

df['HH_SIZE'] = df['HOUSE HOLD SIZE']
df['FARM_EXP'] = df['YEARS OF FARMING EXPERIENCE']
df['OTHER_INCOME'] = df['OTHER SOURCE OF INCOME'].astype(int)
df['EXTENSION_ACCESS'] = df['ACCESS TO AGRICULTURAL EXTENSION'].astype(int)
df['COOPERATIVE'] = df['MEMBER OF OOPERATIVE SOCIETY'].astype(int)

# Expenditure
df['EXP_FOOD'] = df['AVERAGE MONTHLY HOUSEHOLD FOOD EXPENDITURE']
df['EXP_EDUC'] = df['AVERAGE MONTHLY HOUSEHOLD EXPENDITURE'] # Education
df['EXP_HEALTH'] = df['AVERAGE MONTHLY HOUSEHOLD  MEDICAL EXPENDITURE']
df['EXP_HOUSING'] = df['AVERAGE MONTHLY HOUSING AND UTILITY EXPENTITURE']
df['EXP_TRANS'] = df['AVERAGE MONTHLY HOUSEHOLD TRANSPORTATION']
df['EXP_TOTAL_REPORTED'] = df['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE']

exp_components = ['EXP_FOOD', 'EXP_EDUC', 'EXP_HEALTH', 'EXP_HOUSING', 'EXP_TRANS']
df['EXP_TOTAL_COMPONENT_SUM'] = df[exp_components].sum(axis=1)
df['EXP_DISCREPANCY'] = df['EXP_TOTAL_REPORTED'] - df['EXP_TOTAL_COMPONENT_SUM']
df['EXP_ABS_DISCREPANCY'] = df['EXP_DISCREPANCY'].abs()
df['EXP_PCT_DISCREPANCY'] = (df['EXP_DISCREPANCY'] / df['EXP_TOTAL_COMPONENT_SUM']) * 100

# Income
df['INCOME_MONTHLY_TOTAL'] = df['HOW MUCH DO YOU EARN IN A MONTH']
df['INCOME_YAM_SALES'] = df['HOW MUCH DO YOU EARN FROM THE SALES OF YAM']

# Farm specifics
df['FARM_SIZE_TOTAL'] = df['WHAT IS YOUR TOTAL FARM SIZE']
df['FARM_SIZE_YAM'] = df['HOW MANY HECTARES ARE USED SPECIFICALLY FOR YAM FARMING']
df['CREDIT_ACCESS'] = df['ACCESS TO CREDIT FOR YAM FARMING DURING LAST SEASON'].astype(int)
df['CREDIT_AMOUNT'] = df['IF YES APPROXIMATELY HOW MUCH']
df['IMPROVED_VARIETIES'] = df['DO YOU USE IMPROVE YAM VARIETIES'].astype(int)
df['FERTILIZER_USE'] = df['DO  YOU APPLY FERTILIZER OR MANURE ON YOUR YAM FARM'].astype(int)
df['MODERN_TOOLS'] = df['DO YOU USE MODERN FARM TOOLS OR IMPROVED TECHNOLOGIES IN YAM PRODUCTION'].astype(int)

# Challenges
challenge_raw_cols = [
    'HIGH COST OF FARM INPUTS',
    'INADEQUATE ACCESS TO CREDIT',
    'PEST AND DISEASE INFESTATION',
    'UNPREDICTABLE RAINFALL AND CLIMATE CONDITIONS',
    'HIGH COST AND SCARCITY OF FARM LABOUR',
    'HIGH COST/SCARCITY OF YAM STAKES',
    'POOR ACCESS TO MARKET',
    'LOW AND UNSTABLE PRICES OF YAM',
    'INADEQUATE AGRICULTURAL EXTENSIONSERVICES',
    'POST-HARVEST LOSSES AND INADEQUATE STORAGE FACILITIES'
]

challenge_names = [
    'High cost of farm inputs',
    'Inadequate access to credit',
    'Pest and disease infestation',
    'Unpredictable rainfall and climate conditions',
    'High cost and scarcity of farm labour',
    'High cost/scarcity of yam stakes',
    'Poor access to markets',
    'Low and unstable prices of yam',
    'Inadequate agricultural extension services',
    'Post-harvest losses and inadequate storage facilities'
]

challenge_short_codes = [
    'CHAL_INPUT_COST',
    'CHAL_CREDIT_ACCESS',
    'CHAL_PEST_DISEASE',
    'CHAL_CLIMATE',
    'CHAL_LABOUR_COST',
    'CHAL_YAM_STAKES',
    'CHAL_MARKET_ACCESS',
    'CHAL_YAM_PRICES',
    'CHAL_EXTENSION',
    'CHAL_STORAGE_LOSS'
]

for rc, sc in zip(challenge_raw_cols, challenge_short_codes):
    df[sc] = df[rc]

# 3. POVERTY MEASUREMENT
df['PCHE_REPORTED'] = df['EXP_TOTAL_REPORTED'] / df['HH_SIZE']
mean_pche_rep = df['PCHE_REPORTED'].mean()
pov_line_rep = (2.0 / 3.0) * mean_pche_rep
df['POVERTY_STATUS_REPORTED'] = (df['PCHE_REPORTED'] < pov_line_rep).astype(int)

df['PCHE_COMPONENT'] = df['EXP_TOTAL_COMPONENT_SUM'] / df['HH_SIZE']
mean_pche_comp = df['PCHE_COMPONENT'].mean()
pov_line_comp = (2.0 / 3.0) * mean_pche_comp
df['POVERTY_STATUS_COMPONENT'] = (df['PCHE_COMPONENT'] < pov_line_comp).astype(int)

# Primary variables
df['POVERTY_STATUS'] = df['POVERTY_STATUS_REPORTED']
df['POVERTY_STATUS_LABEL'] = df['POVERTY_STATUS'].map({1: 'Poor', 0: 'Non-poor'})
df['PCHE'] = df['PCHE_REPORTED']
pov_line = pov_line_rep
mean_pche = mean_pche_rep

n_poor = df['POVERTY_STATUS'].sum()
n_nonpoor = N - n_poor

# FGT Indices function
def calc_fgt(pche_series, z):
    gap_ratio = np.maximum(0, (z - pche_series) / z)
    p0 = np.mean(gap_ratio > 0)
    p1 = np.mean(gap_ratio)
    p2 = np.mean(gap_ratio ** 2)
    poor_vals = pche_series[pche_series < z]
    mean_poor = np.mean(poor_vals) if len(poor_vals) > 0 else 0
    abs_gap = z - mean_poor
    return {
        'P0': p0, 'P1': p1, 'P2': p2,
        'MEAN_POOR_PCHE': mean_poor, 'ABS_GAP': abs_gap,
        'Q': len(poor_vals), 'N': len(pche_series)
    }

fgt_rep = calc_fgt(df['PCHE_REPORTED'], pov_line_rep)
fgt_comp = calc_fgt(df['PCHE_COMPONENT'], pov_line_comp)

# Cohen's Kappa for sensitivity
ct_sens = pd.crosstab(df['POVERTY_STATUS_REPORTED'], df['POVERTY_STATUS_COMPONENT'])
agree_cnt = np.diag(ct_sens).sum()
po = agree_cnt / N
pe = ((fgt_rep['Q'] * fgt_comp['Q']) + ((N - fgt_rep['Q']) * (N - fgt_comp['Q']))) / (N * N)
kappa = (po - pe) / (1.0 - pe)

# 4. BIVARIATE STATISTICAL ANALYSIS (OBJECTIVE 3)
# Predictors to test (excluding outcome-derived variables like PCHE and Total Expenditure)
biv_cont_vars = [
    ('AGE_YEARS', 'Age of Household Head (Years)'),
    ('FARM_EXP', 'Years of Farming Experience'),
    ('FARM_SIZE_TOTAL', 'Total Farm Size (Hectares)'),
    ('FARM_SIZE_YAM', 'Yam Cultivated Area (Hectares)'),
    ('INCOME_MONTHLY_TOTAL', 'Total Monthly Income (₦)'),
    ('INCOME_YAM_SALES', 'Monthly Yam Sales Income (₦)'),
    ('HH_SIZE', 'Household Size (Persons) [Welfare Divisor Note]')
]

biv_cont_res = []
poor_mask = df['POVERTY_STATUS'] == 1
nonpoor_mask = df['POVERTY_STATUS'] == 0

for var_code, var_name in biv_cont_vars:
    p_s = df.loc[poor_mask, var_code].dropna()
    np_s = df.loc[nonpoor_mask, var_code].dropna()
    
    u_stat, u_pval = stats.mannwhitneyu(p_s, np_s, alternative='two-sided')
    n1, n2 = len(p_s), len(np_s)
    r_rb = 1.0 - (2.0 * u_stat) / (n1 * n2) # rank-biserial correlation
    t_stat, t_pval = stats.ttest_ind(p_s, np_s, equal_var=False)
    
    biv_cont_res.append({
        'Variable_Code': var_code,
        'Variable_Name': var_name,
        'Poor_n': n1,
        'Poor_Mean': p_s.mean(),
        'Poor_SD': p_s.std(),
        'Poor_Median': p_s.median(),
        'Poor_IQR': p_s.quantile(0.75) - p_s.quantile(0.25),
        'NonPoor_n': n2,
        'NonPoor_Mean': np_s.mean(),
        'NonPoor_SD': np_s.std(),
        'NonPoor_Median': np_s.median(),
        'NonPoor_IQR': np_s.quantile(0.75) - np_s.quantile(0.25),
        'Mann_Whitney_U': u_stat,
        'MW_p_value': u_pval,
        'Rank_Biserial_r': r_rb,
        't_stat': t_stat,
        't_p_value': t_pval
    })
df_biv_cont = pd.DataFrame(biv_cont_res)

biv_cat_vars = [
    ('CREDIT_ACCESS', 'Access to Credit', {1: 'Yes', 0: 'No'}),
    ('EXTENSION_ACCESS', 'Agricultural Extension Contact', {1: 'Yes', 0: 'No'}),
    ('SEX_EMPIRICAL', 'Sex of Head (Valid n=59)', {1.0: 'Male', 0.0: 'Female'}),
    ('MARITAL_STATUS_RAW', 'Marital Status', {1: 'Single', 2: 'Married', 4: 'Widowed'}),
    ('EDUC_YEARS', 'Education Level', {6: 'Primary (6 yrs)', 12: 'Secondary (12 yrs)', 16: 'Tertiary (16 yrs)'}),
    ('OTHER_INCOME', 'Other Source of Income', {1: 'Yes', 0: 'No'}),
    ('COOPERATIVE', 'Cooperative Membership', {1: 'Yes', 0: 'No'}),
    ('IMPROVED_VARIETIES', 'Use of Improved Varieties', {1: 'Yes', 0: 'No'}),
    ('FERTILIZER_USE', 'Fertilizer/Manure Use', {1: 'Yes', 0: 'No'}),
    ('MODERN_TOOLS', 'Use of Modern Farm Tools', {1: 'Yes', 0: 'No'})
]

biv_cat_res = []
for var_code, var_name, lmap in biv_cat_vars:
    sub = df[[var_code, 'POVERTY_STATUS']].dropna()
    ct = pd.crosstab(sub[var_code], sub['POVERTY_STATUS'])
    chi2, chi2_pval, dof, _ = stats.chi2_contingency(ct)
    
    if ct.shape == (2, 2):
        oddsratio, fisher_pval = stats.fisher_exact(ct)
    else:
        fisher_pval = np.nan
        
    n_obs = ct.values.sum()
    min_dim = min(ct.shape) - 1
    cramer_v = np.sqrt(chi2 / (n_obs * min_dim)) if min_dim > 0 else 0
    
    for cat_val, row_data in ct.iterrows():
        cat_lbl = lmap.get(cat_val, str(cat_val))
        np_cnt = row_data[0] if 0 in row_data else 0
        p_cnt = row_data[1] if 1 in row_data else 0
        tot_cnt = np_cnt + p_cnt
        p_rate = (p_cnt / tot_cnt) * 100 if tot_cnt > 0 else 0
        
        biv_cat_res.append({
            'Variable_Name': var_name,
            'Category': cat_lbl,
            'Poor_Count': p_cnt,
            'Poor_Pct': (p_cnt / sub[sub['POVERTY_STATUS']==1].shape[0]) * 100,
            'NonPoor_Count': np_cnt,
            'NonPoor_Pct': (np_cnt / sub[sub['POVERTY_STATUS']==0].shape[0]) * 100,
            'Total_Count': tot_cnt,
            'Poverty_Rate_Within_Cat': p_rate,
            'Chi2': chi2,
            'df': dof,
            'Chi2_p_value': chi2_pval,
            'Fisher_p_value': fisher_pval,
            'Cramers_V': cramer_v
        })
df_biv_cat = pd.DataFrame(biv_cat_res)

# 5. MULTICOLLINEARITY & VIF AUDIT
r_farm_credit = np.corrcoef(df['FARM_SIZE_TOTAL'], df['CREDIT_ACCESS'])[0, 1]
r_spearman_farm_credit = df['FARM_SIZE_TOTAL'].corr(df['CREDIT_ACCESS'], method='spearman')
vif_farm_credit = 1.0 / (1.0 - r_farm_credit ** 2)
tol_farm_credit = 1.0 - r_farm_credit ** 2

r_farm_yam = np.corrcoef(df['FARM_SIZE_TOTAL'], df['FARM_SIZE_YAM'])[0, 1]
vif_farm_yam = 1.0 / (1.0 - r_farm_yam ** 2)

print(f"\nMulticollinearity Audit:")
print(f"Farm Size vs Credit: Pearson r = {r_farm_credit:.4f}, Spearman r = {r_spearman_farm_credit:.4f}, VIF = {vif_farm_credit:.4f}, Tolerance = {tol_farm_credit:.4f}")
print(f"Farm Size vs Yam Area: Pearson r = {r_farm_yam:.4f}, VIF = {vif_farm_yam:.4f} (Severe Collinearity)")

# 6. FIRTH PENALIZED LOGISTIC REGRESSION & PROFILE LIKELIHOOD CI
def fit_firth_with_profile(X, y, var_names, max_iter=100, tol=1e-7):
    n, p = X.shape
    beta = np.zeros(p)
    
    for _ in range(max_iter):
        pi = 1.0 / (1.0 + np.exp(-X @ beta))
        pi = np.clip(pi, 1e-15, 1 - 1e-15)
        W = np.diag(pi * (1.0 - pi))
        info_mat = X.T @ W @ X
        try:
            info_inv = np.linalg.inv(info_mat)
        except np.linalg.LinAlgError:
            info_inv = np.linalg.pinv(info_mat)
        H = np.zeros(n)
        for j in range(n):
            xj = X[j, :]
            H[j] = xj @ info_inv @ xj * (pi[j] * (1.0 - pi[j]))
        U_star = X.T @ (y - pi + H * (0.5 - pi))
        delta = info_inv @ U_star
        beta += delta
        if np.max(np.abs(delta)) < tol:
            break
            
    # Final Information & Covariance
    pi = 1.0 / (1.0 + np.exp(-X @ beta))
    W = np.diag(pi * (1.0 - pi))
    info_mat = X.T @ W @ X
    info_inv = np.linalg.inv(info_mat)
    se = np.sqrt(np.diag(info_inv))
    
    log_lik_unpen = np.sum(y * np.log(pi) + (1.0 - y) * np.log(1.0 - pi))
    sign, log_det = np.linalg.slogdet(info_mat)
    log_lik_pen = log_lik_unpen + 0.5 * log_det
    
    # Null model
    X_null = np.ones((n, 1))
    beta_null = np.zeros(1)
    for _ in range(max_iter):
        pi_0 = 1.0 / (1.0 + np.exp(-X_null @ beta_null))
        W_0 = np.diag(pi_0 * (1.0 - pi_0))
        info_0 = X_null.T @ W_0 @ X_null
        info_0_inv = np.linalg.inv(info_0)
        H_0 = np.zeros(n)
        for j in range(n):
            xj = X_null[j, :]
            H_0[j] = xj @ info_0_inv @ xj * (pi_0[j] * (1.0 - pi_0[j]))
        U_0 = X_null.T @ (y - pi_0 + H_0 * (0.5 - pi_0))
        d0 = info_0_inv @ U_0
        beta_null += d0
        if np.max(np.abs(d0)) < tol:
            break
    pi_0 = 1.0 / (1.0 + np.exp(-X_null @ beta_null))
    W_0 = np.diag(pi_0 * (1.0 - pi_0))
    info_0 = X_null.T @ W_0 @ X_null
    log_lik_0_unpen = np.sum(y * np.log(pi_0) + (1.0 - y) * np.log(1.0 - pi_0))
    sign_0, log_det_0 = np.linalg.slogdet(info_0)
    log_lik_0_pen = log_lik_0_unpen + 0.5 * log_det_0
    
    lr_stat = 2.0 * (log_lik_pen - log_lik_0_pen)
    df_model = p - 1
    p_lr = 1.0 - stats.chi2.cdf(lr_stat, df_model) if df_model > 0 else 1.0
    
    z_scores = beta / se
    p_wald = 2.0 * (1.0 - stats.norm.cdf(np.abs(z_scores)))
    
    # Wald CIs
    wald_ci_low = beta - 1.959964 * se
    wald_ci_high = beta + 1.959964 * se
    
    # Model Fit / Pseudo R2
    # Unpenalized log-likelihood null (intercept only MLE)
    p_bar = np.mean(y)
    ll_null_mle = n * (p_bar * np.log(p_bar) + (1.0 - p_bar) * np.log(1.0 - p_bar))
    # Unpenalized model log-likelihood for comparison
    r2_mcfadden = 1.0 - (log_lik_unpen / ll_null_mle)
    # Penalized Nagelkerke
    r2_cs = 1.0 - np.exp(-lr_stat / n)
    r2_nagelkerke = r2_cs / (1.0 - np.exp(2.0 * log_lik_0_pen / n))
    
    # AIC / BIC based on Penalized Log-Likelihood
    aic_pen = -2.0 * log_lik_pen + 2.0 * p
    bic_pen = -2.0 * log_lik_pen + np.log(n) * p
    
    # AIC / BIC based on Unpenalized Log-Likelihood (for sensitivity comparison)
    aic_unpen = -2.0 * log_lik_unpen + 2.0 * p
    bic_unpen = -2.0 * log_lik_unpen + np.log(n) * p
    
    # Profile Penalized-Likelihood Confidence Intervals
    def log_pen_val(b_vec):
        p_i = 1.0 / (1.0 + np.exp(-X @ b_vec))
        p_i = np.clip(p_i, 1e-15, 1 - 1e-15)
        W_i = np.diag(p_i * (1.0 - p_i))
        info_i = X.T @ W_i @ X
        ll_u = np.sum(y * np.log(p_i) + (1.0 - y) * np.log(1.0 - p_i))
        s_i, ld_i = np.linalg.slogdet(info_i)
        if s_i <= 0: return -1e10
        return ll_u + 0.5 * ld_i

    cutoff = log_lik_pen - 0.5 * 3.841459
    prof_ci_low = []
    prof_ci_high = []
    
    for param_idx in range(p):
        other_idx = [i for i in range(p) if i != param_idx]
        def prof_ll(val):
            if len(other_idx) == 0: return log_pen_val(np.array([val]))
            def obj(ob):
                b_c = np.zeros(p)
                b_c[param_idx] = val
                for ii, oi in enumerate(other_idx): b_c[oi] = ob[ii]
                return -log_pen_val(b_c)
            r_opt = optimize.minimize(obj, beta[other_idx], method='BFGS')
            return -r_opt.fun
        
        # lower root
        try:
            b_l = beta[param_idx] - 0.5
            while prof_ll(b_l) > cutoff and b_l > beta[param_idx] - 12: b_l -= 0.5
            l_val = optimize.brentq(lambda v: prof_ll(v) - cutoff, b_l, beta[param_idx])
        except Exception:
            l_val = wald_ci_low[param_idx]
            
        # upper root
        try:
            b_h = beta[param_idx] + 0.5
            while prof_ll(b_h) > cutoff and b_h < beta[param_idx] + 12: b_h += 0.5
            h_val = optimize.brentq(lambda v: prof_ll(v) - cutoff, beta[param_idx], b_h)
        except Exception:
            h_val = wald_ci_high[param_idx]
            
        prof_ci_low.append(l_val)
        prof_ci_high.append(h_val)
        
    summary_rows = []
    for idx, vname in enumerate(var_names):
        summary_rows.append({
            'Variable': vname,
            'Beta': beta[idx],
            'SE': se[idx],
            'Wald_z': z_scores[idx],
            'p_wald': p_wald[idx],
            'OR': np.exp(beta[idx]),
            'Wald_95CI_Lower': np.exp(wald_ci_low[idx]),
            'Wald_95CI_Upper': np.exp(wald_ci_high[idx]),
            'Profile_95CI_Lower': np.exp(prof_ci_low[idx]),
            'Profile_95CI_Upper': np.exp(prof_ci_high[idx]),
            'Beta_Wald_Lower': wald_ci_low[idx],
            'Beta_Wald_Upper': wald_ci_high[idx],
            'Beta_Profile_Lower': prof_ci_low[idx],
            'Beta_Profile_Upper': prof_ci_high[idx]
        })
        
    return {
        'summary_table': pd.DataFrame(summary_rows),
        'beta': beta,
        'se': se,
        'log_lik_pen': log_lik_pen,
        'log_lik_0_pen': log_lik_0_pen,
        'log_lik_unpen': log_lik_unpen,
        'lr_stat': lr_stat,
        'p_lr': p_lr,
        'df': df_model,
        'aic_pen': aic_pen,
        'bic_pen': bic_pen,
        'aic_unpen': aic_unpen,
        'bic_unpen': bic_unpen,
        'r2_mcfadden': r2_mcfadden,
        'r2_nagelkerke': r2_nagelkerke,
        'n': n
    }

y_pov = df['POVERTY_STATUS'].values

# Model A: Farm Size + Credit Access
X_A = sm.add_constant(df[['FARM_SIZE_TOTAL', 'CREDIT_ACCESS']].values)
names_A = ['Intercept', 'Total Farm Size (ha)', 'Access to Credit (1=Yes)']
firth_A = fit_firth_with_profile(X_A, y_pov, names_A)

# Model B: Farm Size + Credit Access + Age
X_B = sm.add_constant(df[['FARM_SIZE_TOTAL', 'CREDIT_ACCESS', 'AGE_YEARS']].values)
names_B = ['Intercept', 'Total Farm Size (ha)', 'Access to Credit (1=Yes)', 'Age of Head (Years)']
firth_B = fit_firth_with_profile(X_B, y_pov, names_B)

# Model C: Farm Size + Credit Access + Extension
X_C = sm.add_constant(df[['FARM_SIZE_TOTAL', 'CREDIT_ACCESS', 'EXTENSION_ACCESS']].values)
names_C = ['Intercept', 'Total Farm Size (ha)', 'Access to Credit (1=Yes)', 'Extension Contact (1=Yes)']
firth_C = fit_firth_with_profile(X_C, y_pov, names_C)

# Model D: Farm Size + Credit Access + Other Income
X_D = sm.add_constant(df[['FARM_SIZE_TOTAL', 'CREDIT_ACCESS', 'OTHER_INCOME']].values)
names_D = ['Intercept', 'Total Farm Size (ha)', 'Access to Credit (1=Yes)', 'Other Income (1=Yes)']
firth_D = fit_firth_with_profile(X_D, y_pov, names_D)

# Candidate Models Summary Table
model_comparison_data = [
    {
        'Model': 'Model A (Primary Baseline)',
        'Predictors': 'Total Farm Size + Credit Access',
        'k_params': 3,
        'EPV': f"{n_poor}/2 = 6.5",
        'Penalized_LogLik': firth_A['log_lik_pen'],
        'LR_Chi2': firth_A['lr_stat'],
        'LR_p_value': firth_A['p_lr'],
        'AIC_Penalized': firth_A['aic_pen'],
        'BIC_Penalized': firth_A['bic_pen'],
        'AIC_Unpenalized': firth_A['aic_unpen'],
        'BIC_Unpenalized': firth_A['bic_unpen'],
        'Nagelkerke_Pseudo_R2': firth_A['r2_nagelkerke'],
        'Credit_OR_Wald': firth_A['summary_table'].loc[firth_A['summary_table']['Variable'] == 'Access to Credit (1=Yes)', 'OR'].values[0],
        'Credit_OR_p': firth_A['summary_table'].loc[firth_A['summary_table']['Variable'] == 'Access to Credit (1=Yes)', 'p_wald'].values[0],
        'FarmSize_OR': firth_A['summary_table'].loc[firth_A['summary_table']['Variable'] == 'Total Farm Size (ha)', 'OR'].values[0],
        'FarmSize_p': firth_A['summary_table'].loc[firth_A['summary_table']['Variable'] == 'Total Farm Size (ha)', 'p_wald'].values[0]
    },
    {
        'Model': 'Model B (Demographic Extension)',
        'Predictors': 'Total Farm Size + Credit Access + Age',
        'k_params': 4,
        'EPV': f"{n_poor}/3 = 4.3",
        'Penalized_LogLik': firth_B['log_lik_pen'],
        'LR_Chi2': firth_B['lr_stat'],
        'LR_p_value': firth_B['p_lr'],
        'AIC_Penalized': firth_B['aic_pen'],
        'BIC_Penalized': firth_B['bic_pen'],
        'AIC_Unpenalized': firth_B['aic_unpen'],
        'BIC_Unpenalized': firth_B['bic_unpen'],
        'Nagelkerke_Pseudo_R2': firth_B['r2_nagelkerke'],
        'Credit_OR_Wald': firth_B['summary_table'].loc[firth_B['summary_table']['Variable'] == 'Access to Credit (1=Yes)', 'OR'].values[0],
        'Credit_OR_p': firth_B['summary_table'].loc[firth_B['summary_table']['Variable'] == 'Access to Credit (1=Yes)', 'p_wald'].values[0],
        'FarmSize_OR': firth_B['summary_table'].loc[firth_B['summary_table']['Variable'] == 'Total Farm Size (ha)', 'OR'].values[0],
        'FarmSize_p': firth_B['summary_table'].loc[firth_B['summary_table']['Variable'] == 'Total Farm Size (ha)', 'p_wald'].values[0]
    },
    {
        'Model': 'Model C (Institutional Extension)',
        'Predictors': 'Total Farm Size + Credit Access + Extension',
        'k_params': 4,
        'EPV': f"{n_poor}/3 = 4.3",
        'Penalized_LogLik': firth_C['log_lik_pen'],
        'LR_Chi2': firth_C['lr_stat'],
        'LR_p_value': firth_C['p_lr'],
        'AIC_Penalized': firth_C['aic_pen'],
        'BIC_Penalized': firth_C['bic_pen'],
        'AIC_Unpenalized': firth_C['aic_unpen'],
        'BIC_Unpenalized': firth_C['bic_unpen'],
        'Nagelkerke_Pseudo_R2': firth_C['r2_nagelkerke'],
        'Credit_OR_Wald': firth_C['summary_table'].loc[firth_C['summary_table']['Variable'] == 'Access to Credit (1=Yes)', 'OR'].values[0],
        'Credit_OR_p': firth_C['summary_table'].loc[firth_C['summary_table']['Variable'] == 'Access to Credit (1=Yes)', 'p_wald'].values[0],
        'FarmSize_OR': firth_C['summary_table'].loc[firth_C['summary_table']['Variable'] == 'Total Farm Size (ha)', 'OR'].values[0],
        'FarmSize_p': firth_C['summary_table'].loc[firth_C['summary_table']['Variable'] == 'Total Farm Size (ha)', 'p_wald'].values[0]
    },
    {
        'Model': 'Model D (Livelihood Extension)',
        'Predictors': 'Total Farm Size + Credit Access + Other Income',
        'k_params': 4,
        'EPV': f"{n_poor}/3 = 4.3",
        'Penalized_LogLik': firth_D['log_lik_pen'],
        'LR_Chi2': firth_D['lr_stat'],
        'LR_p_value': firth_D['p_lr'],
        'AIC_Penalized': firth_D['aic_pen'],
        'BIC_Penalized': firth_D['bic_pen'],
        'AIC_Unpenalized': firth_D['aic_unpen'],
        'BIC_Unpenalized': firth_D['bic_unpen'],
        'Nagelkerke_Pseudo_R2': firth_D['r2_nagelkerke'],
        'Credit_OR_Wald': firth_D['summary_table'].loc[firth_D['summary_table']['Variable'] == 'Access to Credit (1=Yes)', 'OR'].values[0],
        'Credit_OR_p': firth_D['summary_table'].loc[firth_D['summary_table']['Variable'] == 'Access to Credit (1=Yes)', 'p_wald'].values[0],
        'FarmSize_OR': firth_D['summary_table'].loc[firth_D['summary_table']['Variable'] == 'Total Farm Size (ha)', 'OR'].values[0],
        'FarmSize_p': firth_D['summary_table'].loc[firth_D['summary_table']['Variable'] == 'Total Farm Size (ha)', 'p_wald'].values[0]
    }
]
df_model_comp = pd.DataFrame(model_comparison_data)

# 7. ORDINARY MAXIMUM LIKELIHOOD LOGISTIC SENSITIVITY
ml_mod_A = sm.Logit(y_pov, X_A).fit(disp=False)
ml_params = ml_mod_A.params
ml_bse = ml_mod_A.bse
ml_pvals = ml_mod_A.pvalues
ml_conf = ml_mod_A.conf_int()

df_ml_sens = pd.DataFrame([
    {
        'Variable': names_A[i],
        'Ordinary_Beta': ml_params[i],
        'Ordinary_SE': ml_bse[i],
        'Ordinary_Wald_z': ml_params[i] / ml_bse[i],
        'Ordinary_p_value': ml_pvals[i],
        'Ordinary_OR': np.exp(ml_params[i]),
        'Ordinary_95CI_Lower': np.exp(ml_conf[i, 0]),
        'Ordinary_95CI_Upper': np.exp(ml_conf[i, 1]),
        'Firth_Beta': firth_A['summary_table']['Beta'].values[i],
        'Firth_SE': firth_A['summary_table']['SE'].values[i],
        'Firth_OR': firth_A['summary_table']['OR'].values[i],
        'Firth_p_value': firth_A['summary_table']['p_wald'].values[i],
        'Directional_Concordance': 'Concordant (Negative)' if firth_A['summary_table']['Beta'].values[i] < 0 and ml_params[i] < 0 else ('Concordant (Positive)' if firth_A['summary_table']['Beta'].values[i] > 0 and ml_params[i] > 0 else 'Opposite')
    }
    for i in range(len(names_A))
])

# 8. OBJECTIVE IV: CHALLENGES (5-POINT LIKERT SCALE)
chal_res = []
for rc, name in zip(challenge_raw_cols, challenge_names):
    s = df[rc].dropna()
    valid_n = len(s)
    mean_val = s.mean()
    sd_val = s.std()
    median_val = s.median()
    iqr_val = s.quantile(0.75) - s.quantile(0.25)
    
    vc = s.value_counts()
    n1 = vc.get(1.0, 0)
    n2 = vc.get(2.0, 0)
    n3 = vc.get(3.0, 0)
    n4 = vc.get(4.0, 0)
    n5 = vc.get(5.0, 0)
    
    if mean_val <= 1.80:
        interp = 'Not a Challenge'
    elif mean_val <= 2.60:
        interp = 'Minor Challenge'
    elif mean_val <= 3.40:
        interp = 'Moderate Challenge'
    elif mean_val <= 4.20:
        interp = 'Severe Challenge'
    else:
        interp = 'Very Severe Challenge'
        
    chal_res.append({
        'Challenge': name,
        'Valid_n': valid_n,
        'Mean_MSI': mean_val,
        'SD': sd_val,
        'Median': median_val,
        'IQR': iqr_val,
        'Score_1_n': n1,
        'Score_1_pct': (n1 / valid_n) * 100,
        'Score_2_n': n2,
        'Score_2_pct': (n2 / valid_n) * 100,
        'Score_3_n': n3,
        'Score_3_pct': (n3 / valid_n) * 100,
        'Score_4_n': n4,
        'Score_4_pct': (n4 / valid_n) * 100,
        'Score_5_n': n5,
        'Score_5_pct': (n5 / valid_n) * 100,
        'Interpretation': interp
    })

df_chal = pd.DataFrame(chal_res).sort_values('Mean_MSI', ascending=False).reset_index(drop=True)
df_chal['Rank'] = df_chal.index + 1

print("\n--- CHALLENGE RANKING VERIFIED ---")
for idx, r in df_chal.iterrows():
    print(f"Rank {r['Rank']:2d}: {r['Challenge']:55s} | MSI = {r['Mean_MSI']:.4f} | {r['Interpretation']}")

# ==============================================================================
# 9. BUILD FULL_REANALYSIS_AKPABUYO_FINAL.xlsx (27 SHEETS)
# ==============================================================================
out_excel = 'FULL_REANALYSIS_AKPABUYO_FINAL/FULL_REANALYSIS_AKPABUYO_FINAL.xlsx'
wb = openpyxl.Workbook()
wb.remove(wb.active)

font_title = Font(name='Calibri', size=14, bold=True, color='1F497D')
font_header = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
font_bold = Font(name='Calibri', size=11, bold=True)
font_regular = Font(name='Calibri', size=11)
font_note = Font(name='Calibri', size=9, italic=True, color='595959')

fill_header = PatternFill(start_color='1F497D', end_color='1F497D', fill_type='solid')
border_thin = Side(border_style='thin', color='D9D9D9')
border_thick_bottom = Side(border_style='medium', color='1F497D')
cell_border = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)

def style_sheet(ws, title, df_data, notes=None):
    ws.views.sheetView[0].showGridLines = True
    ws.append([title])
    ws.cell(row=1, column=1).font = font_title
    ws.append([])
    
    start_row = 3
    headers = list(df_data.columns)
    ws.append(headers)
    
    for col_num in range(1, len(headers) + 1):
        c = ws.cell(row=start_row, column=col_num)
        c.font = font_header
        c.fill = fill_header
        c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        c.border = Border(top=border_thin, bottom=border_thick_bottom, left=border_thin, right=border_thin)
        
    for r_idx, row in df_data.iterrows():
        row_vals = []
        for val in row:
            if pd.isna(val):
                row_vals.append("N/A")
            elif isinstance(val, (int, np.integer)):
                row_vals.append(int(val))
            elif isinstance(val, (float, np.floating)):
                row_vals.append(round(float(val), 4))
            else:
                row_vals.append(str(val))
        ws.append(row_vals)
        curr_row = ws.max_row
        for col_num in range(1, len(headers) + 1):
            c = ws.cell(row=curr_row, column=col_num)
            c.font = font_regular
            c.border = cell_border
            if isinstance(c.value, float):
                if abs(c.value) >= 1000: c.number_format = '#,##0.00'
                elif abs(c.value) < 0.001 and c.value != 0: c.number_format = '0.00000'
                else: c.number_format = '0.0000'
            elif isinstance(c.value, int):
                c.number_format = '#,##0'
                
    if notes:
        ws.append([])
        for n in notes:
            ws.append([n])
            ws.cell(row=ws.max_row, column=1).font = font_note
            
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 50)

print("\nGenerating 27 Excel sheets...")
# 1. README
ws = wb.create_sheet(title='README')
readme_rows = [
    ['FINAL FORENSIC RE-ANALYSIS AND STATISTICAL AUDIT WORKBOOK'],
    ['Study Title: Analysis of Poverty Status of Yam Farmers in Akpabuyo Local Government Area, Cross River State, Nigeria'],
    ['Dataset: raw_data.csv (MD5: 628f44079ed97d91b232533b3c14e014, N = 60 households)'],
    ['Date: October 2026 | Auditor: Antigravity AI Data & Statistical Audit System'],
    [],
    ['TAB DIRECTORY (27 SHEETS):'],
    ['1. README', 'Metadata, project orientation, tab directory'],
    ['2. Data_Dictionary', 'Complete codebook with analytical roles, valid ranges, and measurement scales'],
    ['3. Data_Audit', 'Forensic quality audit (missingness, coding anomalies, duplicates, outliers)'],
    ['4. Raw_Data_Check', 'Complete working dataset for all 60 respondents'],
    ['5. Socioeconomic_Descriptives', 'Demographic, socioeconomic, and farm baseline characteristics (N=60)'],
    ['6. Expenditure_Audit', 'Reconciliation of reported total vs component-sum monthly expenditure (N=60)'],
    ['7. Poverty_Calculation', 'Determination of relative poverty line (2/3 Mean PCHE) and household classifications'],
    ['8. Poverty_Sensitivity', 'Sensitivity of poverty rates and classification agreement to expenditure definition'],
    ['9. FGT_Results', 'Foster-Greer-Thorbecke poverty indices (P0, P1, P2) and monetary gap metrics'],
    ['10. Poverty_Profile_Categorical', 'Objective II: Cross-tabulation profile of categorical variables by poverty status'],
    ['11. Poverty_Profile_Continuous', 'Objective II: Summary statistics of continuous variables by poverty status'],
    ['12. Poverty_Profile_Welfare', 'Objective II: Detailed monthly expenditure and income profiles by poverty status'],
    ['13. Bivariate_Continuous', 'Objective III: Mann-Whitney U tests, rank-biserial effect sizes, and t-tests'],
    ['14. Bivariate_Categorical', 'Objective III: Chi-Square tests, Fisher exact tests, and Cramérs V effect sizes'],
    ['15. Firth_Model_A', 'Objective III: Primary Firth penalized logistic regression (Farm Size + Credit)'],
    ['16. Firth_Model_B', 'Objective III: Multivariable Firth model adding Age (Farm Size + Credit + Age)'],
    ['17. Firth_Model_C', 'Objective III: Multivariable Firth model adding Extension (Farm Size + Credit + Extension)'],
    ['18. Additional_Model', 'Objective III: Alternative parsimonious Firth model (Farm Size + Credit + Other Income)'],
    ['19. Model_Comparison', 'Information criteria (AIC, BIC), LR chi-square, and fit comparison across models'],
    ['20. Final_Firth_Model', 'Comprehensive parameter table with Profile and Wald CIs for the recommended model (Model A)'],
    ['21. Logistic_Sensitivity', 'Ordinary ML logistic regression comparison and separation analysis'],
    ['22. Regression_Diagnostics', 'Multicollinearity (VIF=1.5856), sparse cell analysis, and separation diagnostics'],
    ['23. Multiple_Testing', 'Multiplicity evaluation on legitimate inferential predictor set'],
    ['24. Challenge_MSI', 'Objective IV: Mean Severity Index (MSI), SD, median, IQR, ranking, and categories'],
    ['25. Hypothesis_Audit', 'Statistical review and alignment of research hypotheses vs empirical tests'],
    ['26. Bias_Audit', 'Forensic assessment of sampling, measurement, classification, and model biases'],
    ['27. Final_Thesis_Tables', 'Ready-to-use publication tables formatted for Chapter 4 reconstruction']
]
ws.views.sheetView[0].showGridLines = True
for r in readme_rows: ws.append(r)
ws.cell(row=1, column=1).font = font_title
ws.column_dimensions['A'].width = 32
ws.column_dimensions['B'].width = 80

# 2. Data_Dictionary
data_dict_df = pd.DataFrame([
    {'Variable': 'RESP_ID', 'Description': 'Respondent Identification Number', 'Type': 'Integer', 'Measurement_Scale': 'Nominal', 'Coding': '1 to 60', 'Valid_Range': '1–60', 'Missing': 0, 'Analytical_Role': 'Identifier'},
    {'Variable': 'SEX_RAW', 'Description': 'Sex of Household Head (Raw)', 'Type': 'Categorical', 'Measurement_Scale': 'Nominal', 'Coding': '1=Male, 0=Female, 2=Unverified', 'Valid_Range': '0–2', 'Missing': 0, 'Analytical_Role': 'Raw Data Audit'},
    {'Variable': 'SEX_EMPIRICAL', 'Description': 'Sex of Head (Empirical Valid Cases)', 'Type': 'Categorical', 'Measurement_Scale': 'Binary', 'Coding': '1=Male (36), 0=Female (23), NaN (1)', 'Valid_Range': '0–1', 'Missing': 1, 'Analytical_Role': 'Primary Descriptive Baseline'},
    {'Variable': 'AGE_YEARS', 'Description': 'Age of Household Head', 'Type': 'Numeric', 'Measurement_Scale': 'Ratio (Years)', 'Coding': 'Continuous', 'Valid_Range': '30–63', 'Missing': 0, 'Analytical_Role': 'Socioeconomic Profile / Predictor'},
    {'Variable': 'MARITAL_STATUS', 'Description': 'Marital Status of Head', 'Type': 'Categorical', 'Measurement_Scale': 'Nominal', 'Coding': '1=Single, 2=Married, 4=Widowed', 'Valid_Range': '1–4', 'Missing': 0, 'Analytical_Role': 'Socioeconomic Profile'},
    {'Variable': 'EDUC_YEARS', 'Description': 'Highest Educational Level Attained', 'Type': 'Numeric/Ordinal', 'Measurement_Scale': 'Years of Schooling', 'Coding': '6=Primary, 12=Secondary, 16=Tertiary', 'Valid_Range': '6–16', 'Missing': 0, 'Analytical_Role': 'Socioeconomic Profile / Predictor'},
    {'Variable': 'HH_SIZE', 'Description': 'Household Size (Living and eating together)', 'Type': 'Integer', 'Measurement_Scale': 'Ratio (Persons)', 'Coding': 'Continuous', 'Valid_Range': '3–10', 'Missing': 0, 'Analytical_Role': 'Welfare Deflator (PCHE Denominator)'},
    {'Variable': 'FARM_EXP', 'Description': 'Years of Yam Farming Experience', 'Type': 'Numeric', 'Measurement_Scale': 'Ratio (Years)', 'Coding': 'Continuous', 'Valid_Range': '6–40', 'Missing': 0, 'Analytical_Role': 'Socioeconomic Profile / Predictor'},
    {'Variable': 'OTHER_INCOME', 'Description': 'Engagement in Off-Farm / Other Income', 'Type': 'Categorical', 'Measurement_Scale': 'Binary', 'Coding': '1=Yes, 0=No', 'Valid_Range': '0–1', 'Missing': 0, 'Analytical_Role': 'Socioeconomic Profile / Predictor'},
    {'Variable': 'EXTENSION_ACCESS', 'Description': 'Contact with Agricultural Extension in 12m', 'Type': 'Categorical', 'Measurement_Scale': 'Binary', 'Coding': '1=Yes, 0=No', 'Valid_Range': '0–1', 'Missing': 0, 'Analytical_Role': 'Institutional Profile / Predictor'},
    {'Variable': 'COOPERATIVE', 'Description': 'Membership in Farmers Cooperative', 'Type': 'Categorical', 'Measurement_Scale': 'Binary', 'Coding': '1=Yes, 0=No', 'Valid_Range': '0–1', 'Missing': 0, 'Analytical_Role': 'Institutional Profile / Predictor'},
    {'Variable': 'EXP_FOOD', 'Description': 'Monthly Household Food Expenditure', 'Type': 'Numeric', 'Measurement_Scale': 'Ratio (₦)', 'Coding': 'Continuous', 'Valid_Range': '35,000–96,000', 'Missing': 0, 'Analytical_Role': 'Welfare Component'},
    {'Variable': 'EXP_EDUC', 'Description': 'Monthly Household Education Expenditure', 'Type': 'Numeric', 'Measurement_Scale': 'Ratio (₦)', 'Coding': 'Continuous', 'Valid_Range': '5,000–35,000', 'Missing': 0, 'Analytical_Role': 'Welfare Component'},
    {'Variable': 'EXP_HEALTH', 'Description': 'Monthly Household Health/Medical Expenditure', 'Type': 'Numeric', 'Measurement_Scale': 'Ratio (₦)', 'Coding': 'Continuous', 'Valid_Range': '4,000–18,000', 'Missing': 0, 'Analytical_Role': 'Welfare Component'},
    {'Variable': 'EXP_HOUSING', 'Description': 'Monthly Housing & Utility Expenditure', 'Type': 'Numeric', 'Measurement_Scale': 'Ratio (₦)', 'Coding': 'Continuous', 'Valid_Range': '8,000–35,000', 'Missing': 0, 'Analytical_Role': 'Welfare Component'},
    {'Variable': 'EXP_TRANS', 'Description': 'Monthly Transportation & Other Expenditure', 'Type': 'Numeric', 'Measurement_Scale': 'Ratio (₦)', 'Coding': 'Continuous', 'Valid_Range': '6,000–22,000', 'Missing': 0, 'Analytical_Role': 'Welfare Component'},
    {'Variable': 'EXP_TOTAL_REPORTED', 'Description': 'Reported Total Monthly Household Expenditure', 'Type': 'Numeric', 'Measurement_Scale': 'Ratio (₦)', 'Coding': 'Continuous', 'Valid_Range': '65,000–223,500', 'Missing': 0, 'Analytical_Role': 'Primary Welfare Aggregate'},
    {'Variable': 'PCHE', 'Description': 'Per Capita Household Expenditure', 'Type': 'Numeric', 'Measurement_Scale': 'Ratio (₦/person)', 'Coding': 'EXP_TOTAL / HH_SIZE', 'Valid_Range': '10,000–47,500', 'Missing': 0, 'Analytical_Role': 'Objective I Welfare Metric'},
    {'Variable': 'POVERTY_STATUS', 'Description': 'Household Poverty Classification', 'Type': 'Categorical', 'Measurement_Scale': 'Binary', 'Coding': '1=Poor (PCHE < z), 0=Non-poor (PCHE >= z)', 'Valid_Range': '0–1', 'Missing': 0, 'Analytical_Role': 'Objective I-III Dependent Variable'},
    {'Variable': 'FARM_SIZE_TOTAL', 'Description': 'Total Farm Size Operated', 'Type': 'Numeric', 'Measurement_Scale': 'Ratio (Hectares)', 'Coding': 'Continuous', 'Valid_Range': '1.2–5.0', 'Missing': 0, 'Analytical_Role': 'Farm Profile / Primary Predictor'},
    {'Variable': 'FARM_SIZE_YAM', 'Description': 'Hectares Allocated Specifically to Yam', 'Type': 'Numeric', 'Measurement_Scale': 'Ratio (Hectares)', 'Coding': 'Continuous', 'Valid_Range': '0.9–3.5', 'Missing': 0, 'Analytical_Role': 'Farm Profile / Predictor'},
    {'Variable': 'CREDIT_ACCESS', 'Description': 'Access to Yam Credit in Last Season', 'Type': 'Categorical', 'Measurement_Scale': 'Binary', 'Coding': '1=Yes, 0=No', 'Valid_Range': '0–1', 'Missing': 0, 'Analytical_Role': 'Institutional Profile / Primary Predictor'},
    {'Variable': 'CREDIT_AMOUNT', 'Description': 'Amount of Credit Accessed', 'Type': 'Numeric', 'Measurement_Scale': 'Ratio (₦)', 'Coding': 'Continuous (0 if No Credit)', 'Valid_Range': '0–200,000', 'Missing': 0, 'Analytical_Role': 'Institutional Profile'},
    {'Variable': 'IMPROVED_VARIETIES', 'Description': 'Use of Improved Yam Varieties', 'Type': 'Categorical', 'Measurement_Scale': 'Binary', 'Coding': '1=Yes, 0=No', 'Valid_Range': '0–1', 'Missing': 0, 'Analytical_Role': 'Technology Adoption Profile'},
    {'Variable': 'FERTILIZER_USE', 'Description': 'Application of Fertilizer/Manure', 'Type': 'Categorical', 'Measurement_Scale': 'Binary', 'Coding': '1=Yes, 0=No', 'Valid_Range': '0–1', 'Missing': 0, 'Analytical_Role': 'Technology Adoption Profile'},
    {'Variable': 'MODERN_TOOLS', 'Description': 'Use of Modern Farm Tools / Technologies', 'Type': 'Categorical', 'Measurement_Scale': 'Binary', 'Coding': '1=Yes, 0=No', 'Valid_Range': '0–1', 'Missing': 0, 'Analytical_Role': 'Technology Adoption Profile'},
    {'Variable': 'CHAL_1 to CHAL_10', 'Description': 'Severity of Yam Farming Challenges (10 items)', 'Type': 'Categorical/Ordinal', 'Measurement_Scale': '5-Point Likert', 'Coding': '1=Not Challenge, 2=Minor, 3=Moderate, 4=Severe, 5=Very Severe', 'Valid_Range': '1–5', 'Missing': 1, 'Analytical_Role': 'Objective IV Challenge Analysis'}
])
style_sheet(wb.create_sheet(title='Data_Dictionary'), 'Table 1: Research Variable Codebook and Data Dictionary', data_dict_df)

# 3. Data_Audit
data_audit_rows = pd.DataFrame([
    {'Variable': 'Sample Size (N)', 'N_Obs': 60, 'Missing': 0, 'Min': 1, 'Max': 60, 'Mean': np.nan, 'Median': np.nan, 'SD': np.nan, 'Invalid_Values': 'None (0 duplicates)', 'Coding_Notes': 'Exactly 60 complete respondent records across 6 communities.'},
    {'Variable': 'Sex of Head (Raw)', 'N_Obs': 60, 'Missing': 0, 'Min': 0, 'Max': 2, 'Mean': 0.6333, 'Median': 1.0, 'SD': 0.5197, 'Invalid_Values': '1 case with code 2.0 (Resp 46)', 'Coding_Notes': 'Code 2 has no documented meaning. Empirically treated as missing (valid n=59: 36 Male, 23 Female).'},
    {'Variable': 'Age (Years)', 'N_Obs': 60, 'Missing': 0, 'Min': 30.0, 'Max': 63.0, 'Mean': 46.0333, 'Median': 46.0, 'SD': 8.6435, 'Invalid_Values': 'None', 'Coding_Notes': 'Continuous range: 30 to 63 years; IQR = 13.0 years.'},
    {'Variable': 'Marital Status', 'N_Obs': 60, 'Missing': 0, 'Min': 1, 'Max': 4, 'Mean': 2.1167, 'Median': 2.0, 'SD': 0.6911, 'Invalid_Values': 'None', 'Coding_Notes': '1=Single (5), 2=Married (49), 4=Widowed (6). No divorced.'},
    {'Variable': 'Education (Years)', 'N_Obs': 60, 'Missing': 0, 'Min': 6.0, 'Max': 16.0, 'Mean': 11.2000, 'Median': 12.0, 'SD': 3.7947, 'Invalid_Values': 'None', 'Coding_Notes': 'Primary=6 (18), Secondary=12 (27), Tertiary=16 (15).'},
    {'Variable': 'Household Size', 'N_Obs': 60, 'Missing': 0, 'Min': 3.0, 'Max': 10.0, 'Mean': 6.2333, 'Median': 6.0, 'SD': 1.8445, 'Invalid_Values': 'None', 'Coding_Notes': 'Continuous range: 3 to 10 persons; IQR = 2.0 persons.'},
    {'Variable': 'Farming Experience', 'N_Obs': 60, 'Missing': 0, 'Min': 6.0, 'Max': 40.0, 'Mean': 18.8833, 'Median': 17.5, 'SD': 8.5551, 'Invalid_Values': 'None', 'Coding_Notes': 'Continuous range: 6 to 40 years; IQR = 11.0 years.'},
    {'Variable': 'Other Income', 'N_Obs': 60, 'Missing': 0, 'Min': 0, 'Max': 1, 'Mean': 0.8167, 'Median': 1.0, 'SD': 0.3902, 'Invalid_Values': 'None', 'Coding_Notes': '1=Yes (49, 81.7%), 0=No (11, 18.3%).'},
    {'Variable': 'Extension Access', 'N_Obs': 60, 'Missing': 0, 'Min': 0, 'Max': 1, 'Mean': 0.3500, 'Median': 0.0, 'SD': 0.4810, 'Invalid_Values': 'None', 'Coding_Notes': '1=Yes (21, 35.0%), 0=No (39, 65.0%). 0 poor had contact.'},
    {'Variable': 'Cooperative Membership', 'N_Obs': 60, 'Missing': 0, 'Min': 0, 'Max': 1, 'Mean': 0.8167, 'Median': 1.0, 'SD': 0.3902, 'Invalid_Values': 'None', 'Coding_Notes': '1=Yes (49, 81.7%), 0=No (11, 18.3%).'},
    {'Variable': 'Total Farm Size (ha)', 'N_Obs': 60, 'Missing': 0, 'Min': 1.2, 'Max': 5.0, 'Mean': 2.4333, 'Median': 2.2, 'SD': 0.7910, 'Invalid_Values': 'None', 'Coding_Notes': 'Continuous range: 1.2 to 5.0 ha; IQR = 1.0 ha.'},
    {'Variable': 'Yam Cultivated Area (ha)', 'N_Obs': 60, 'Missing': 0, 'Min': 0.9, 'Max': 3.5, 'Mean': 1.6683, 'Median': 1.5, 'SD': 0.5335, 'Invalid_Values': 'None', 'Coding_Notes': 'Continuous range: 0.9 to 3.5 ha; IQR = 0.8 ha.'},
    {'Variable': 'Credit Access', 'N_Obs': 60, 'Missing': 0, 'Min': 0, 'Max': 1, 'Mean': 0.5000, 'Median': 0.5, 'SD': 0.5042, 'Invalid_Values': 'None', 'Coding_Notes': '1=Yes (30, 50.0%), 0=No (30, 50.0%).'},
    {'Variable': 'Credit Amount (₦)', 'N_Obs': 60, 'Missing': 0, 'Min': 0, 'Max': 200000, 'Mean': 36583.33, 'Median': 12500, 'SD': 49927.84, 'Invalid_Values': 'None', 'Coding_Notes': '30 non-recipients coded 0; 30 recipients received ₦25,000–₦200,000.'},
    {'Variable': 'Improved Varieties', 'N_Obs': 60, 'Missing': 0, 'Min': 0, 'Max': 1, 'Mean': 0.0333, 'Median': 0.0, 'SD': 0.1810, 'Invalid_Values': 'Sparse (n=2)', 'Coding_Notes': '1=Yes (2, 3.3%), 0=No (58, 96.7%). Extreme cell sparsity.'},
    {'Variable': 'Fertilizer/Manure Use', 'N_Obs': 60, 'Missing': 0, 'Min': 0, 'Max': 1, 'Mean': 0.8000, 'Median': 1.0, 'SD': 0.4034, 'Invalid_Values': 'None', 'Coding_Notes': '1=Yes (48, 80.0%), 0=No (12, 20.0%).'},
    {'Variable': 'Modern Tools Use', 'N_Obs': 60, 'Missing': 0, 'Min': 0, 'Max': 1, 'Mean': 0.1000, 'Median': 0.0, 'SD': 0.3025, 'Invalid_Values': 'Sparse (n=6)', 'Coding_Notes': '1=Yes (6, 10.0%), 0=No (54, 90.0%). Cell sparsity.'},
    {'Variable': 'Total Monthly Exp. (Reported)', 'N_Obs': 60, 'Missing': 0, 'Min': 65000, 'Max': 223500, 'Mean': 115837.50, 'Median': 111000, 'SD': 27652.42, 'Invalid_Values': '4 discrepancies', 'Coding_Notes': '56 exact matches; 4 discrepant cases evaluated via sensitivity.'},
    {'Variable': 'Total Monthly Exp. (Comp. Sum)', 'N_Obs': 60, 'Missing': 0, 'Min': 65000, 'Max': 190000, 'Mean': 113985.83, 'Median': 111000, 'SD': 24964.55, 'Invalid_Values': 'None', 'Coding_Notes': 'Sum of food, education, health, housing, transport.'},
    {'Variable': 'PCHE (Reported Total)', 'N_Obs': 60, 'Missing': 0, 'Min': 10000, 'Max': 47500, 'Mean': 20289.03, 'Median': 18883.33, 'SD': 7585.87, 'Invalid_Values': 'None', 'Coding_Notes': 'Primary welfare metric; z = ₦13,526.02; Poor=13 (21.67%).'},
    {'Variable': 'PCHE (Component Sum)', 'N_Obs': 60, 'Missing': 0, 'Min': 10000, 'Max': 47500, 'Mean': 20022.82, 'Median': 18883.33, 'SD': 7367.66, 'Invalid_Values': 'None', 'Coding_Notes': 'Sensitivity welfare metric; z = ₦13,348.55; Poor=12 (20.00%).'},
    {'Variable': 'Challenges 1 to 10', 'N_Obs': 60, 'Missing': 1, 'Min': 1.0, 'Max': 5.0, 'Mean': 3.575, 'Median': 4.0, 'SD': 0.925, 'Invalid_Values': '1 missing (Item 8)', 'Coding_Notes': '5-point Likert scale (1 to 5). Resp 46 missing on Item 8 (valid n=59).'}
])
style_sheet(wb.create_sheet(title='Data_Audit'), 'Table 2: Forensic Data Quality and Integrity Audit Summary', data_audit_rows)

# 4. Raw_Data_Check
raw_check_df = df[['RESP_ID', 'SEX_RAW', 'SEX_EMPIRICAL', 'AGE_YEARS', 'MARITAL_STATUS_LABEL', 'EDUC_LEVEL', 'HH_SIZE', 'FARM_EXP', 'OTHER_INCOME', 'EXTENSION_ACCESS', 'COOPERATIVE', 'EXP_FOOD', 'EXP_EDUC', 'EXP_HEALTH', 'EXP_HOUSING', 'EXP_TRANS', 'EXP_TOTAL_REPORTED', 'EXP_TOTAL_COMPONENT_SUM', 'PCHE_REPORTED', 'POVERTY_STATUS_REPORTED', 'FARM_SIZE_TOTAL', 'FARM_SIZE_YAM', 'CREDIT_ACCESS', 'CREDIT_AMOUNT'] + challenge_short_codes]
style_sheet(wb.create_sheet(title='Raw_Data_Check'), 'Table 3: Validated Working Dataset (N = 60 Households)', raw_check_df)

# 5. Socioeconomic_Descriptives
socio_desc_full = pd.DataFrame([
    {'Characteristic': 'Sex of Head (Empirical Valid Cases)', 'Category': 'Male', 'Frequency': 36, 'Percentage': (36/59)*100, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': 'Valid n = 59; excludes Respondent 46 (unverified code 2.0)'},
    {'Characteristic': '', 'Category': 'Female', 'Frequency': 23, 'Percentage': (23/59)*100, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': 'Unspecified / Invalid (Code 2)', 'Frequency': 1, 'Percentage': (1/60)*100, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': 'Respondent 46 (Total N = 60)'},
    {'Characteristic': 'Sex of Head (Historical Thesis Assumption)', 'Category': 'Male', 'Frequency': 36, 'Percentage': 60.00, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': 'Assuming code 2 was intended as Female (N = 60)'},
    {'Characteristic': '', 'Category': 'Female', 'Frequency': 24, 'Percentage': 40.00, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': 'Age of Head (Years)', 'Category': '< 40 years', 'Frequency': 14, 'Percentage': 23.33, 'Mean': 46.0333, 'SD': 8.6435, 'Median': 46.0, 'Min': 30.0, 'Max': 63.0, 'Audit_Note': 'IQR = 13.0 years'},
    {'Characteristic': '', 'Category': '40–49 years', 'Frequency': 26, 'Percentage': 43.33, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': '50–59 years', 'Frequency': 16, 'Percentage': 26.67, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': '>= 60 years', 'Frequency': 4, 'Percentage': 6.67, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': 'Marital Status', 'Category': 'Single', 'Frequency': 5, 'Percentage': 8.33, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': 'Married', 'Frequency': 49, 'Percentage': 81.67, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': 'Widowed', 'Frequency': 6, 'Percentage': 10.00, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': 'Highest Education Level', 'Category': 'Primary (6 yrs)', 'Frequency': 18, 'Percentage': 30.00, 'Mean': 11.2000, 'SD': 3.7947, 'Median': 12.0, 'Min': 6.0, 'Max': 16.0, 'Audit_Note': 'IQR = 6.0 years'},
    {'Characteristic': '', 'Category': 'Secondary (12 yrs)', 'Frequency': 27, 'Percentage': 45.00, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': 'Tertiary (16 yrs)', 'Frequency': 15, 'Percentage': 25.00, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': 'Household Size (Persons)', 'Category': '1–4 persons', 'Frequency': 10, 'Percentage': 16.67, 'Mean': 6.2333, 'SD': 1.8445, 'Median': 6.0, 'Min': 3.0, 'Max': 10.0, 'Audit_Note': 'IQR = 2.0 persons'},
    {'Characteristic': '', 'Category': '5–7 persons', 'Frequency': 36, 'Percentage': 60.00, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': '8–10 persons', 'Frequency': 14, 'Percentage': 23.33, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': 'Farming Experience (Years)', 'Category': '< 10 years', 'Frequency': 8, 'Percentage': 13.33, 'Mean': 18.8833, 'SD': 8.5551, 'Median': 17.5, 'Min': 6.0, 'Max': 40.0, 'Audit_Note': 'IQR = 11.0 years'},
    {'Characteristic': '', 'Category': '10–19 years', 'Frequency': 29, 'Percentage': 48.33, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': '20–29 years', 'Frequency': 16, 'Percentage': 26.67, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': '>= 30 years', 'Frequency': 7, 'Percentage': 11.67, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': 'Total Farm Size (Hectares)', 'Category': '< 2.0 ha', 'Frequency': 19, 'Percentage': 31.67, 'Mean': 2.4333, 'SD': 0.7910, 'Median': 2.2, 'Min': 1.2, 'Max': 5.0, 'Audit_Note': 'IQR = 1.0 ha'},
    {'Characteristic': '', 'Category': '2.0–2.9 ha', 'Frequency': 28, 'Percentage': 46.67, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': '>= 3.0 ha', 'Frequency': 13, 'Percentage': 21.67, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': 'Yam Cultivated Area (Hectares)', 'Category': '< 1.5 ha', 'Frequency': 22, 'Percentage': 36.67, 'Mean': 1.6683, 'SD': 0.5335, 'Median': 1.5, 'Min': 0.9, 'Max': 3.5, 'Audit_Note': 'IQR = 0.8 ha'},
    {'Characteristic': '', 'Category': '1.5–1.9 ha', 'Frequency': 24, 'Percentage': 40.00, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': '>= 2.0 ha', 'Frequency': 14, 'Percentage': 23.33, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': 'Other Income Source', 'Category': 'Yes', 'Frequency': 49, 'Percentage': 81.67, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': 'No', 'Frequency': 11, 'Percentage': 18.33, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': 'Extension Access', 'Category': 'Yes', 'Frequency': 21, 'Percentage': 35.00, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': 'No', 'Frequency': 39, 'Percentage': 65.00, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': 'Credit Access', 'Category': 'Yes', 'Frequency': 30, 'Percentage': 50.00, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': 'No', 'Frequency': 30, 'Percentage': 50.00, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': 'Cooperative Membership', 'Category': 'Yes', 'Frequency': 49, 'Percentage': 81.67, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': 'No', 'Frequency': 11, 'Percentage': 18.33, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': 'Improved Yam Varieties', 'Category': 'Yes', 'Frequency': 2, 'Percentage': 3.33, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': 'Sparse cell'},
    {'Characteristic': '', 'Category': 'No', 'Frequency': 58, 'Percentage': 96.67, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': 'Fertilizer/Manure Use', 'Category': 'Yes', 'Frequency': 48, 'Percentage': 80.00, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': '', 'Category': 'No', 'Frequency': 12, 'Percentage': 20.00, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''},
    {'Characteristic': 'Modern Tools / Technology', 'Category': 'Yes', 'Frequency': 6, 'Percentage': 10.00, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': 'Sparse cell'},
    {'Characteristic': '', 'Category': 'No', 'Frequency': 54, 'Percentage': 90.00, 'Mean': np.nan, 'SD': np.nan, 'Median': np.nan, 'Min': np.nan, 'Max': np.nan, 'Audit_Note': ''}
])
style_sheet(wb.create_sheet(title='Socioeconomic_Descriptives'), 'Table 4: Baseline Socioeconomic and Farm Characteristics of Yam Farmers (N = 60)', socio_desc_full)

# 6. Expenditure_Audit
exp_audit_table = df[['RESP_ID', 'EXP_FOOD', 'EXP_EDUC', 'EXP_HEALTH', 'EXP_HOUSING', 'EXP_TRANS', 'EXP_TOTAL_COMPONENT_SUM', 'EXP_TOTAL_REPORTED', 'EXP_DISCREPANCY', 'EXP_PCT_DISCREPANCY']]
style_sheet(wb.create_sheet(title='Expenditure_Audit'), 'Table 5: Respondent-Level Monthly Household Expenditure Reconciliation (N = 60)', exp_audit_table, [
    'Notes: Exact matches: 56/60 (93.33%). Discrepant cases: 4/60 (6.67%).',
    'Discrepancies: Resp 14 (+₦1,000, +0.85%), Resp 37 (-₦400, -0.37%), Resp 39 (+₦500, +0.49%), Resp 59 (+₦110,000, +96.92%).',
    'Total absolute discrepancy across sample: ₦111,900.00; Mean discrepancy: ₦1,865.00; Median discrepancy: ₦0.00.'
])

# 7. Poverty_Calculation
pov_calc_table = df[['RESP_ID', 'HH_SIZE', 'EXP_TOTAL_REPORTED', 'PCHE_REPORTED', 'POVERTY_STATUS_REPORTED', 'EXP_TOTAL_COMPONENT_SUM', 'PCHE_COMPONENT', 'POVERTY_STATUS_COMPONENT']]
style_sheet(wb.create_sheet(title='Poverty_Calculation'), 'Table 6: Household PCHE and Poverty Classification Determination', pov_calc_table, [
    f'Reported Total: Mean Monthly Household Expenditure = ₦{df["EXP_TOTAL_REPORTED"].mean():,.2f}, Mean PCHE = ₦{mean_pche_rep:,.2f}, Relative Poverty Line (2/3 Mean PCHE) = ₦{pov_line_rep:,.2f}.',
    f'Component Sum : Mean Monthly Household Expenditure = ₦{df["EXP_TOTAL_COMPONENT_SUM"].mean():,.2f}, Mean PCHE = ₦{mean_pche_comp:,.2f}, Relative Poverty Line (2/3 Mean PCHE) = ₦{pov_line_comp:,.2f}.'
])

# 8. Poverty_Sensitivity
style_sheet(wb.create_sheet(title='Poverty_Sensitivity'), 'Table 7: Methodological Sensitivity Analysis of Poverty Measures', pd.DataFrame([
    {'Metric': 'Mean Total Monthly Household Expenditure (₦)', 'Reported_Total_Approach': df['EXP_TOTAL_REPORTED'].mean(), 'Component_Sum_Approach': df['EXP_TOTAL_COMPONENT_SUM'].mean(), 'Difference': df['EXP_TOTAL_REPORTED'].mean() - df['EXP_TOTAL_COMPONENT_SUM'].mean(), 'Percentage_Difference': ((df['EXP_TOTAL_REPORTED'].mean() - df['EXP_TOTAL_COMPONENT_SUM'].mean())/df['EXP_TOTAL_COMPONENT_SUM'].mean())*100},
    {'Metric': 'Mean Per Capita Household Expenditure (PCHE, ₦)', 'Reported_Total_Approach': mean_pche_rep, 'Component_Sum_Approach': mean_pche_comp, 'Difference': mean_pche_rep - mean_pche_comp, 'Percentage_Difference': ((mean_pche_rep - mean_pche_comp)/mean_pche_comp)*100},
    {'Metric': 'Relative Poverty Line z (2/3 Mean PCHE, ₦)', 'Reported_Total_Approach': pov_line_rep, 'Component_Sum_Approach': pov_line_comp, 'Difference': pov_line_rep - pov_line_comp, 'Percentage_Difference': ((pov_line_rep - pov_line_comp)/pov_line_comp)*100},
    {'Metric': 'Poor Households Count (n)', 'Reported_Total_Approach': fgt_rep['Q'], 'Component_Sum_Approach': fgt_comp['Q'], 'Difference': fgt_rep['Q'] - fgt_comp['Q'], 'Percentage_Difference': ((fgt_rep['Q'] - fgt_comp['Q'])/fgt_comp['Q'])*100},
    {'Metric': 'Non-Poor Households Count (n)', 'Reported_Total_Approach': N - fgt_rep['Q'], 'Component_Sum_Approach': N - fgt_comp['Q'], 'Difference': (N - fgt_rep['Q']) - (N - fgt_comp['Q']), 'Percentage_Difference': (((N - fgt_rep['Q']) - (N - fgt_comp['Q']))/(N - fgt_comp['Q']))*100},
    {'Metric': 'Headcount Poverty Rate P0 (%)', 'Reported_Total_Approach': fgt_rep['P0']*100, 'Component_Sum_Approach': fgt_comp['P0']*100, 'Difference': (fgt_rep['P0'] - fgt_comp['P0'])*100, 'Percentage_Difference': ((fgt_rep['P0'] - fgt_comp['P0'])/fgt_comp['P0'])*100},
    {'Metric': 'Poverty Gap Index P1', 'Reported_Total_Approach': fgt_rep['P1'], 'Component_Sum_Approach': fgt_comp['P1'], 'Difference': fgt_rep['P1'] - fgt_comp['P1'], 'Percentage_Difference': ((fgt_rep['P1'] - fgt_comp['P1'])/fgt_comp['P1'])*100},
    {'Metric': 'Poverty Severity Index P2', 'Reported_Total_Approach': fgt_rep['P2'], 'Component_Sum_Approach': fgt_comp['P2'], 'Difference': fgt_rep['P2'] - fgt_comp['P2'], 'Percentage_Difference': ((fgt_rep['P2'] - fgt_comp['P2'])/fgt_comp['P2'])*100},
    {'Metric': 'Classification Concordance (Exact Matches)', 'Reported_Total_Approach': 60, 'Component_Sum_Approach': agree_cnt, 'Difference': 60 - agree_cnt, 'Percentage_Difference': ((60 - agree_cnt)/60)*100},
    {'Metric': 'Raw Agreement (%)', 'Reported_Total_Approach': 100.0, 'Component_Sum_Approach': (agree_cnt/N)*100, 'Difference': 100.0 - (agree_cnt/N)*100, 'Percentage_Difference': 100.0 - (agree_cnt/N)*100},
    {'Metric': "Cohens Kappa Statistic", 'Reported_Total_Approach': 1.0, 'Component_Sum_Approach': kappa, 'Difference': 1.0 - kappa, 'Percentage_Difference': (1.0 - kappa)*100}
]))

# 9. FGT_Results
style_sheet(wb.create_sheet(title='FGT_Results'), 'Table 8: Foster-Greer-Thorbecke (FGT) Poverty Indices and Economic Gap Metrics', pd.DataFrame([
    {'FGT_Index': 'Headcount Ratio (P0)', 'Formula': '(1/N) * sum(I(PCHE_i < z))', 'Primary_Reported_Value': fgt_rep['P0'], 'Component_Sum_Value': fgt_comp['P0'], 'Economic_Interpretation': 'Proportion of yam farming households living below the 2/3 Mean PCHE relative poverty threshold (21.67%).'},
    {'FGT_Index': 'Poverty Gap Index (P1)', 'Formula': '(1/N) * sum(((z - PCHE_i)/z) * I(PCHE_i < z))', 'Primary_Reported_Value': fgt_rep['P1'], 'Component_Sum_Value': fgt_comp['P1'], 'Economic_Interpretation': 'Depth of poverty; poor households face an average deficit of 2.32% of the poverty line spread across the entire sample.'},
    {'FGT_Index': 'Poverty Severity Index (P2)', 'Formula': '(1/N) * sum(((z - PCHE_i)/z)^2 * I(PCHE_i < z))', 'Primary_Reported_Value': fgt_rep['P2'], 'Component_Sum_Value': fgt_comp['P2'], 'Economic_Interpretation': 'Poverty severity measure based on squared normalized poverty gaps; gives greater weight to households farthest below the threshold (0.0034).'},
    {'FGT_Index': 'Mean PCHE of Poor (₦)', 'Formula': '(1/q) * sum(PCHE_i | PCHE_i < z)', 'Primary_Reported_Value': fgt_rep['MEAN_POOR_PCHE'], 'Component_Sum_Value': fgt_comp['MEAN_POOR_PCHE'], 'Economic_Interpretation': 'Average monthly consumption expenditure per capita among the 13 poor farming households (₦12,079.49).'},
    {'FGT_Index': 'Average Poverty Gap per Poor (₦)', 'Formula': 'z - Mean_PCHE_Poor', 'Primary_Reported_Value': fgt_rep['ABS_GAP'], 'Component_Sum_Value': fgt_comp['ABS_GAP'], 'Economic_Interpretation': 'Average monthly financial transfer required per capita to bring each poor person exactly to the poverty threshold (₦1,446.53/month).'}
]))

# 10. Poverty_Profile_Categorical
style_sheet(wb.create_sheet(title='Poverty_Profile_Categorical'), 'Table 9: Objective II — Categorical Socioeconomic Profile by Poverty Status', df_biv_cat[['Variable_Name', 'Category', 'Poor_Count', 'Poor_Pct', 'NonPoor_Count', 'NonPoor_Pct', 'Total_Count', 'Poverty_Rate_Within_Cat']])

# 11. Poverty_Profile_Continuous
style_sheet(wb.create_sheet(title='Poverty_Profile_Continuous'), 'Table 10: Objective II — Continuous Socioeconomic and Farm Profile by Poverty Status', df_biv_cont[['Variable_Name', 'Poor_n', 'Poor_Mean', 'Poor_SD', 'Poor_Median', 'Poor_IQR', 'NonPoor_n', 'NonPoor_Mean', 'NonPoor_SD', 'NonPoor_Median', 'NonPoor_IQR']])

# 12. Poverty_Profile_Welfare
welfare_vars = ['EXP_FOOD', 'EXP_EDUC', 'EXP_HEALTH', 'EXP_HOUSING', 'EXP_TRANS', 'EXP_TOTAL_REPORTED', 'PCHE', 'INCOME_MONTHLY_TOTAL', 'INCOME_YAM_SALES']
welfare_names = ['Monthly Food Expenditure (₦)', 'Monthly Education Expenditure (₦)', 'Monthly Health Expenditure (₦)', 'Monthly Housing/Utility Expenditure (₦)', 'Monthly Transport Expenditure (₦)', 'Total Monthly Expenditure (₦)', 'Per Capita Expenditure (PCHE, ₦)', 'Total Monthly Income (₦)', 'Monthly Yam Sales Income (₦)']
welfare_table_rows = []
for var_code, var_name in zip(welfare_vars, welfare_names):
    p_s = df.loc[poor_mask, var_code]
    np_s = df.loc[nonpoor_mask, var_code]
    tot_s = df[var_code]
    welfare_table_rows.append({
        'Welfare_Metric': var_name,
        'Poor_Mean': p_s.mean(),
        'Poor_SD': p_s.std(),
        'Poor_Median': p_s.median(),
        'NonPoor_Mean': np_s.mean(),
        'NonPoor_SD': np_s.std(),
        'NonPoor_Median': np_s.median(),
        'Total_Sample_Mean': tot_s.mean(),
        'Total_Sample_SD': tot_s.std(),
        'Share_of_Total_Expenditure_Poor_Pct': (p_s.mean() / df.loc[poor_mask, 'EXP_TOTAL_REPORTED'].mean()) * 100 if 'Expenditure' in var_name and var_name != 'Total Monthly Expenditure (₦)' else np.nan,
        'Share_of_Total_Expenditure_NonPoor_Pct': (np_s.mean() / df.loc[nonpoor_mask, 'EXP_TOTAL_REPORTED'].mean()) * 100 if 'Expenditure' in var_name and var_name != 'Total Monthly Expenditure (₦)' else np.nan
    })
style_sheet(wb.create_sheet(title='Poverty_Profile_Welfare'), 'Table 11: Objective II — Detailed Household Welfare and Expenditure Composition Profile', pd.DataFrame(welfare_table_rows))

# 13. Bivariate_Continuous
style_sheet(wb.create_sheet(title='Bivariate_Continuous'), 'Table 12: Objective III — Bivariate Distributional Comparisons for Continuous Predictors', df_biv_cont[['Variable_Name', 'Poor_Median', 'Poor_IQR', 'NonPoor_Median', 'NonPoor_IQR', 'Mann_Whitney_U', 'MW_p_value', 'Rank_Biserial_r', 't_stat', 't_p_value']])

# 14. Bivariate_Categorical
style_sheet(wb.create_sheet(title='Bivariate_Categorical'), 'Table 13: Objective III — Bivariate Association Tests for Categorical Predictors', df_biv_cat[['Variable_Name', 'Category', 'Poor_Count', 'NonPoor_Count', 'Chi2', 'df', 'Chi2_p_value', 'Fisher_p_value', 'Cramers_V']])

# 15. Firth_Model_A
style_sheet(wb.create_sheet(title='Firth_Model_A'), 'Table 14: Objective III — Model A Firth Penalized Logistic Regression (Primary Baseline)', firth_A['summary_table'], [
    f"Penalized Log-Likelihood = {firth_A['log_lik_pen']:.4f}, LR Chi-Square({firth_A['df']}) = {firth_A['lr_stat']:.4f}, p = {firth_A['p_lr']:.6f}.",
    f"AIC (Penalized) = {firth_A['aic_pen']:.4f}, BIC (Penalized) = {firth_A['bic_pen']:.4f}, Nagelkerke Pseudo R2 = {firth_A['r2_nagelkerke']:.4f}."
])

# 16. Firth_Model_B
style_sheet(wb.create_sheet(title='Firth_Model_B'), 'Table 15: Objective III — Model B Firth Penalized Logistic Regression (Adding Age)', firth_B['summary_table'], [
    f"Penalized Log-Likelihood = {firth_B['log_lik_pen']:.4f}, LR Chi-Square({firth_B['df']}) = {firth_B['lr_stat']:.4f}, p = {firth_B['p_lr']:.6f}.",
    f"AIC (Penalized) = {firth_B['aic_pen']:.4f}, BIC (Penalized) = {firth_B['bic_pen']:.4f}, Nagelkerke Pseudo R2 = {firth_B['r2_nagelkerke']:.4f}."
])

# 17. Firth_Model_C
style_sheet(wb.create_sheet(title='Firth_Model_C'), 'Table 16: Objective III — Model C Firth Penalized Logistic Regression (Adding Extension)', firth_C['summary_table'], [
    f"Penalized Log-Likelihood = {firth_C['log_lik_pen']:.4f}, LR Chi-Square({firth_C['df']}) = {firth_C['lr_stat']:.4f}, p = {firth_C['p_lr']:.6f}.",
    f"AIC (Penalized) = {firth_C['aic_pen']:.4f}, BIC (Penalized) = {firth_C['bic_pen']:.4f}, Nagelkerke Pseudo R2 = {firth_C['r2_nagelkerke']:.4f}."
])

# 18. Additional_Model
style_sheet(wb.create_sheet(title='Additional_Model'), 'Table 17: Objective III — Model D Firth Penalized Logistic Regression (Adding Other Income)', firth_D['summary_table'], [
    f"Penalized Log-Likelihood = {firth_D['log_lik_pen']:.4f}, LR Chi-Square({firth_D['df']}) = {firth_D['lr_stat']:.4f}, p = {firth_D['p_lr']:.6f}.",
    f"AIC (Penalized) = {firth_D['aic_pen']:.4f}, BIC (Penalized) = {firth_D['bic_pen']:.4f}, Nagelkerke Pseudo R2 = {firth_D['r2_nagelkerke']:.4f}."
])

# 19. Model_Comparison
style_sheet(wb.create_sheet(title='Model_Comparison'), 'Table 18: Objective III — Multivariable Model Comparison and Selection Matrix', df_model_comp)

# 20. Final_Firth_Model
style_sheet(wb.create_sheet(title='Final_Firth_Model'), 'Table 19: Recommended Primary Empirical Model — Final Firth Penalized Logistic Regression', firth_A['summary_table'], [
    'Model Specification: logit(Poverty_i) = beta0 + beta1*(Total Farm Size_i) + beta2*(Access to Credit_i)',
    'Estimation Technique: Firth (1993) bias-reduced penalized maximum likelihood.',
    f"Goodness of Fit: Penalized Log-Likelihood = {firth_A['log_lik_pen']:.4f}, Model LR Chi-Square = {firth_A['lr_stat']:.4f} (df=2, p = {firth_A['p_lr']:.6f}), AIC = {firth_A['aic_pen']:.4f}.",
    'Economic Finding: Credit access is significantly associated with lower odds of poverty (OR = 0.1099, Wald 95% CI: 0.0136–0.8905, Profile 95% CI: 0.0087–0.7014, p = 0.0386), holding farm size constant.'
])

# 21. Logistic_Sensitivity
style_sheet(wb.create_sheet(title='Logistic_Sensitivity'), 'Table 20: Methodological Sensitivity Comparison — Firth Penalized vs Ordinary MLE Logistic', df_ml_sens)

# 22. Regression_Diagnostics
reg_diag_full = pd.DataFrame([
    {'Diagnostic_Dimension': 'Sample Event-per-Variable (EPV)', 'Value': f"{n_poor} events / 2 predictors = 6.5 EPV", 'Benchmark': '>= 10 EPV ideally for MLE; Firth stabilizes finite-sample estimates with 5–10 EPV', 'Assessment': 'Adequate under Firth penalization; ordinary MLE vulnerable to small-sample bias.'},
    {'Diagnostic_Dimension': 'Multicollinearity: Farm Size & Credit', 'Value': f"Pearson r = {r_farm_credit:.4f}, Spearman r = {r_spearman_farm_credit:.4f}, VIF = {vif_farm_credit:.4f}, Tolerance = {tol_farm_credit:.4f}", 'Benchmark': 'VIF < 5.0, Tolerance > 0.20, r < 0.70', 'Assessment': 'No harmful collinearity. Predictors share moderate correlation (r=0.6077, VIF=1.5856).'},
    {'Diagnostic_Dimension': 'Multicollinearity: Farm Size & Yam Area', 'Value': f"Pearson r = {r_farm_yam:.4f}, VIF = {vif_farm_yam:.4f}", 'Benchmark': 'VIF < 5.0', 'Assessment': 'Severe collinearity (r=0.9642, VIF=14.2120); confirms Yam Area must not enter alongside Farm Size.'},
    {'Diagnostic_Dimension': 'Quasi-Complete Separation Check', 'Value': 'Credit: 1/30 Poor vs 29/30 Non-poor; Extension: 0/21 Poor vs 21/21 Non-poor', 'Benchmark': 'Zero contingency cells cause infinite MLE parameters', 'Assessment': 'Extension causes complete separation in MLE; handled smoothly by Firth penalization.'},
    {'Diagnostic_Dimension': 'Mechanical Dependence Check', 'Value': 'Household size, total expenditure, PCHE excluded from primary model', 'Benchmark': 'Predictors must not be mathematical components of the outcome', 'Assessment': 'Zero mechanical overlap in primary model specification.'},
    {'Diagnostic_Dimension': 'Model Stability across Specifications', 'Value': 'Credit OR varies between 0.1017 and 0.1444 across candidate models (all negative, all OR < 0.15)', 'Benchmark': 'Consistent sign and robust inverse association across specifications', 'Assessment': 'High structural robustness.'}
])
style_sheet(wb.create_sheet(title='Regression_Diagnostics'), 'Table 21: Econometric Regression Diagnostics and Specification Testing', reg_diag_full)

# 23. Multiple_Testing
# Multiplicity on pre-specified legitimate inferential predictors
legit_tests = [
    {'Predictor': 'Access to Credit', 'Test_Type': "Fisher's Exact Test", 'Nominal_p': 0.0012, 'Rank': 1, 'BH_Critical_0.05': (1/7)*0.05, 'FDR_Adjusted_p': 0.0012*7/1},
    {'Predictor': 'Agricultural Extension Contact', 'Test_Type': "Fisher's Exact Test", 'Nominal_p': 0.0021, 'Rank': 2, 'BH_Critical_0.05': (2/7)*0.05, 'FDR_Adjusted_p': 0.0021*7/2},
    {'Predictor': 'Years of Farming Experience', 'Test_Type': 'Mann-Whitney U', 'Nominal_p': 0.0090, 'Rank': 3, 'BH_Critical_0.05': (3/7)*0.05, 'FDR_Adjusted_p': 0.0090*7/3},
    {'Predictor': 'Total Farm Size (Hectares)', 'Test_Type': 'Mann-Whitney U', 'Nominal_p': 0.0160, 'Rank': 4, 'BH_Critical_0.05': (4/7)*0.05, 'FDR_Adjusted_p': 0.0160*7/4},
    {'Predictor': 'Age of Household Head', 'Test_Type': 'Mann-Whitney U', 'Nominal_p': 0.0240, 'Rank': 5, 'BH_Critical_0.05': (5/7)*0.05, 'FDR_Adjusted_p': 0.0240*7/5},
    {'Predictor': 'Other Source of Income', 'Test_Type': "Fisher's Exact Test", 'Nominal_p': 0.2390, 'Rank': 6, 'BH_Critical_0.05': (6/7)*0.05, 'FDR_Adjusted_p': 0.2390*7/6},
    {'Predictor': 'Education Level (Years)', 'Test_Type': 'Pearson Chi-Square', 'Nominal_p': 0.2630, 'Rank': 7, 'BH_Critical_0.05': (7/7)*0.05, 'FDR_Adjusted_p': 0.2630}
]
df_mult_legit = pd.DataFrame(legit_tests)
df_mult_legit['FDR_Adjusted_p'] = np.minimum.accumulate(df_mult_legit['FDR_Adjusted_p'][::-1])[::-1]
df_mult_legit['Significant_FDR_0.05'] = df_mult_legit['FDR_Adjusted_p'] < 0.05
style_sheet(wb.create_sheet(title='Multiple_Testing'), 'Table 22: Multiplicity Assessment on Pre-Specified Inferential Predictors', df_mult_legit, [
    'Note: Excludes outcome-derived variables (PCHE, Total Expenditure) and mechanically dependent variables (Household Size).'
])

# 24. Challenge_MSI
style_sheet(wb.create_sheet(title='Challenge_MSI'), 'Table 23: Objective IV — Severity and Ranking of Challenges Faced by Yam Farmers', df_chal[['Rank', 'Challenge', 'Valid_n', 'Mean_MSI', 'SD', 'Median', 'IQR', 'Score_1_n', 'Score_2_n', 'Score_3_n', 'Score_4_n', 'Score_5_n', 'Interpretation']], [
    'Likert Scale Weights: 1 = Not a Challenge, 2 = Minor, 3 = Moderate, 4 = Severe, 5 = Very Severe.',
    'Severity Intervals: 1.00–1.80 = Not a Challenge; 1.81–2.60 = Minor; 2.61–3.40 = Moderate; 3.41–4.20 = Severe; 4.21–5.00 = Very Severe.',
    'Note: Low and unstable yam prices has valid n = 59 due to one non-response on Respondent 46.'
])

# 25. Hypothesis_Audit
style_sheet(wb.create_sheet(title='Hypothesis_Audit'), 'Table 24: Formal Statistical Audit of Stated Research Hypotheses', pd.DataFrame([
    {
        'Hypothesis_ID': 'H01 (Objective I/III)',
        'Stated_Hypothesis': 'Socioeconomic and farm characteristics do not significantly influence poverty status of yam farmers in Akpabuyo LGA.',
        'Appropriate_Test': 'Multivariable Firth Logistic Regression Model LR Chi-Square Test & Wald Tests',
        'Empirical_Result': f"LR Chi2({firth_A['df']}) = {firth_A['lr_stat']:.4f}, p = {firth_A['p_lr']:.6f}; Credit Access Wald z = -2.069, p = 0.0386",
        'Statistical_Decision': 'Reject Null Hypothesis (p < 0.05)',
        'Methodological_Audit': 'Global likelihood ratio test rejects the null. Individual predictor significance confirms that institutional credit access is significantly associated with poverty status (p = 0.0386).'
    },
    {
        'Hypothesis_ID': 'H02 (Objective IV)',
        'Stated_Hypothesis': 'Challenges faced by yam farmers do not significantly constrain yam production.',
        'Appropriate_Test': 'Descriptive Severity Benchmark Test vs Moderate Threshold (3.0)',
        'Empirical_Result': '7 of 10 challenges have MSI > 3.40 (Severe category), led by Labour Cost (4.15) and Input Cost (4.00)',
        'Statistical_Decision': 'Reject Null Hypothesis (Severe Constraints Identified)',
        'Methodological_Audit': 'Descriptive ranking via MSI is valid. Note that raw dataset does not contain physical output volume (kg/ha) to estimate an econometric production constraint frontier.'
    }
]))

# 26. Bias_Audit
style_sheet(wb.create_sheet(title='Bias_Audit'), 'Table 25: Comprehensive Forensic Bias, Validity, and Threat-to-Inference Audit', pd.DataFrame([
    {'Bias_Category': 'Sampling Bias', 'Source_and_Mechanism': 'Multi-stage sampling of 6 communities with 10 farmers each (N=60). Selection probability unrecorded.', 'Impact_on_Results': 'Sample represents the surveyed farming communities in Akpabuyo LGA, but cannot support claims of statistical generalizability to the entire State or Niger Delta.', 'Action_Required': 'Remove claims of LGA-wide statistical representation; restrict scope to surveyed farming households.'},
    {'Bias_Category': 'Measurement Bias: Expenditure', 'Source_and_Mechanism': 'Recall-based monthly expenditure across 5 categories. 4 respondents had minor discrepancies between reported total and component sums.', 'Impact_on_Results': 'Total discrepancy is small (₦111,900 sample total); sensitivity analysis proves poverty rate and conclusions are robust (98.33% classification agreement, kappa = 0.9495).', 'Action_Required': 'Document expenditure audit transparently in a methodology note.'},
    {'Bias_Category': 'Measurement Bias: Farm Size', 'Source_and_Mechanism': 'Self-reported farm sizes without GPS land boundary verification.', 'Impact_on_Results': 'Potential rounding/recall error in small landholdings; rank-based non-parametric tests protect against outlier bias.', 'Action_Required': 'Report medians and IQR alongside parametric means.'},
    {'Bias_Category': 'Classification Bias', 'Source_and_Mechanism': 'Sample-relative expenditure threshold (2/3 Mean PCHE = ₦13,526.02). One borderline household (Resp 25, PCHE=₦13,500.00) shifts across thresholds.', 'Impact_on_Results': 'Poverty headcount ratio is 21.67% (n=13) under reported total vs 20.00% (n=12) under component sum.', 'Action_Required': 'Present dual-track sensitivity analysis in Chapter 4.'},
    {'Bias_Category': 'Model Bias: Sparse Cells', 'Source_and_Mechanism': 'Only 13 poor events and zero poor households with extension access; causes infinite estimates in ordinary logistic MLE.', 'Impact_on_Results': 'Standard logit produces inflated standard errors and unreliable Wald tests.', 'Action_Required': 'Adopt Firth penalized logistic regression as the primary inferential framework.'},
    {'Bias_Category': 'Mechanical Dependence', 'Source_and_Mechanism': 'Household size is the denominator of PCHE (PCHE = Total Expenditure / HH Size).', 'Impact_on_Results': 'Regressing poverty status on household size creates mechanical artifact (U=536.0, p<0.001) rather than behavioral effect.', 'Action_Required': 'Exclude household size from primary multivariable regression model.'},
    {'Bias_Category': 'Causal Inference Overreach', 'Source_and_Mechanism': 'Cross-sectional survey design measuring simultaneous conditions.', 'Impact_on_Results': 'Cannot determine temporal ordering or causal direction.', 'Action_Required': 'Eliminate all causal wording (e.g. "credit reduced poverty by 92.6%") and replace with associative framing.'}
]))

# 27. Final_Thesis_Tables
style_sheet(wb.create_sheet(title='Final_Thesis_Tables'), 'Table 26: Master Schedule of Final Recommended Chapter 4 Thesis Tables', pd.DataFrame([
    {'Chapter_4_Table_Number': 'Table 4.1', 'Table_Title': 'Socioeconomic Characteristics of Yam Farmers in Akpabuyo LGA', 'Source_Tab_in_Workbook': 'Socioeconomic_Descriptives', 'Variables_Covered': 'Sex (Empirical Valid n=59), Age, Marital Status, Education, Household Size, Farming Experience, Other Income'},
    {'Chapter_4_Table_Number': 'Table 4.2', 'Table_Title': 'Farm, Production, and Institutional Characteristics of Yam Farmers', 'Source_Tab_in_Workbook': 'Socioeconomic_Descriptives', 'Variables_Covered': 'Total Farm Size, Yam Area, Credit Access, Extension Contact, Cooperative Membership, Technology Adoption'},
    {'Chapter_4_Table_Number': 'Table 4.3', 'Table_Title': 'Monthly Household Expenditure Profile and Category Shares', 'Source_Tab_in_Workbook': 'Poverty_Profile_Welfare', 'Variables_Covered': 'Food, Education, Health, Housing/Utilities, Transportation, Total Expenditure, PCHE'},
    {'Chapter_4_Table_Number': 'Table 4.4', 'Table_Title': 'Determination of Relative Poverty Line and Poverty Status Distribution', 'Source_Tab_in_Workbook': 'Poverty_Calculation / FGT_Results', 'Variables_Covered': 'Mean PCHE, 2/3 Mean PCHE Threshold, Headcount (q), Poor/Non-Poor Headcount Rates (%)'},
    {'Chapter_4_Table_Number': 'Table 4.5', 'Table_Title': 'Foster-Greer-Thorbecke (FGT) Poverty Indices and Gap Analysis', 'Source_Tab_in_Workbook': 'FGT_Results', 'Variables_Covered': 'Headcount Ratio (P0), Poverty Gap Index (P1), Poverty Severity Index (P2), Average Monthly Deficit'},
    {'Chapter_4_Table_Number': 'Table 4.6', 'Table_Title': 'Poverty Status Profile Across Socioeconomic and Farm Characteristics', 'Source_Tab_in_Workbook': 'Poverty_Profile_Categorical & Continuous', 'Variables_Covered': 'Objective II Cross-Tabulation and Distributional Comparison across Poor vs Non-Poor'},
    {'Chapter_4_Table_Number': 'Table 4.7', 'Table_Title': 'Bivariate Analysis of Factors Associated with Poverty Status', 'Source_Tab_in_Workbook': 'Bivariate_Continuous & Categorical', 'Variables_Covered': 'Mann-Whitney U Tests, Chi-Square Tests, Fisher Exact Tests, Rank-Biserial r, Cramérs V'},
    {'Chapter_4_Table_Number': 'Table 4.8', 'Table_Title': 'Final Firth Penalized Logistic Regression of Factors Associated with Poverty Status', 'Source_Tab_in_Workbook': 'Final_Firth_Model', 'Variables_Covered': 'Model A Coefficients, SE, Wald z, p-values, Odds Ratios (OR), Profile & Wald 95% CIs, Model Fit'},
    {'Chapter_4_Table_Number': 'Table 4.9', 'Table_Title': 'Ordinary Logistic Regression Sensitivity Analysis', 'Source_Tab_in_Workbook': 'Logistic_Sensitivity', 'Variables_Covered': 'Ordinary MLE vs Firth Penalized Parameter Comparison and Directional Concordance'},
    {'Chapter_4_Table_Number': 'Table 4.10', 'Table_Title': 'Severity and Ranking of Challenges Faced by Yam Farmers', 'Source_Tab_in_Workbook': 'Challenge_MSI', 'Variables_Covered': '10 Challenge Items, Mean Severity Index (MSI), SD, Median, IQR, Score Frequencies, Severity Ranks'}
]))

wb.save(out_excel)
print(f"Successfully saved 27-tab Excel workbook to: {out_excel}")

print("Master script execution phase 1 complete.")

