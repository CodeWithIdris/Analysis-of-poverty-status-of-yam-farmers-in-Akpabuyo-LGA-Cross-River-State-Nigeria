import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

df = pd.read_csv("raw_data.csv")
pche = df['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE'] / df['HOUSE HOLD SIZE']
df['pche'] = pche
mean_pche = pche.mean()
poverty_line = (2.0 / 3.0) * mean_pche
df['is_poor'] = (pche < poverty_line).astype(int)

df['age'] = df['AGE']
df['hh_size'] = df['HOUSE HOLD SIZE']
df['education'] = df['HIGHEST LEVEL OF EDUCATION']
df['total_farm_size'] = df['WHAT IS YOUR TOTAL FARM SIZE']
df['yam_farm_size'] = df['HOW MANY HECTARES ARE USED SPECIFICALLY FOR YAM FARMING']
df['credit_access'] = df['ACCESS TO CREDIT FOR YAM FARMING DURING LAST SEASON']
df['extension_contact'] = df['ACCESS TO AGRICULTURAL EXTENSION']
df['improved_varieties'] = df['DO YOU USE IMPROVE YAM VARIETIES']
df['fertilizer_use'] = df['DO  YOU APPLY FERTILIZER OR MANURE ON YOUR YAM FARM']
df['modern_tools'] = df['DO YOU USE MODERN FARM TOOLS OR IMPROVED TECHNOLOGIES IN YAM PRODUCTION']
df['cooperative_membership'] = df['MEMBER OF OOPERATIVE SOCIETY']

# Let's inspect correlation between household size and PCHE / is_poor
print("=== HOUSEHOLD SIZE & POVERTY CONSTRUCTION ===")
print("Correlation hh_size vs total expenditure:", df['hh_size'].corr(df['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE']))
print("Correlation hh_size vs PCHE:", df['hh_size'].corr(df['pche']))
print("Correlation hh_size vs is_poor:", df['hh_size'].corr(df['is_poor']))

# Note: PCHE = Total Expenditure / Household Size
# Household size is in the exact denominator of the dependent variable definition (PCHE)!
print("\n=== MULTIVARIABLE MODELS ===")

# Existing Model
print("\n--- Existing Model: is_poor ~ total_farm_size + credit_access ---")
m0 = smf.logit('is_poor ~ total_farm_size + credit_access', data=df).fit(disp=False)
print(m0.summary())

# Model with Age added
print("\n--- Model with Age: is_poor ~ total_farm_size + credit_access + age ---")
try:
    m_age = smf.logit('is_poor ~ total_farm_size + credit_access + age', data=df).fit(disp=False)
    print(m_age.summary())
except Exception as e:
    print("Error:", e)

# Model with Household Size added
print("\n--- Model with HH Size: is_poor ~ total_farm_size + credit_access + hh_size ---")
try:
    m_hh = smf.logit('is_poor ~ total_farm_size + credit_access + hh_size', data=df).fit(disp=False)
    print(m_hh.summary())
except Exception as e:
    print("Error:", e)

# Full 6 Objective II variables
print("\n--- Full 6 Objective II variables ---")
try:
    m_full = smf.logit('is_poor ~ age + C(education) + hh_size + credit_access + modern_tools + cooperative_membership', data=df).fit(disp=False)
    print(m_full.summary())
except Exception as e:
    print("Error / Warning:", e)

# Check Firth fit for models
def fit_firth_model(X_df, y):
    X = sm.add_constant(X_df).values
    n, p = X.shape
    beta = np.zeros(p)
    max_iter = 200
    tol = 1e-6
    for iteration in range(max_iter):
        pi = 1.0 / (1.0 + np.exp(-X @ beta))
        pi = np.clip(pi, 1e-15, 1 - 1e-15)
        W = np.diag(pi * (1.0 - pi))
        I = X.T @ W @ X
        try:
            I_inv = np.linalg.inv(I)
        except np.linalg.LinAlgError:
            return "Singular matrix"
        H = np.diag(X @ I_inv @ X.T @ W)
        g = X.T @ (y - pi + H * (0.5 - pi))
        delta = I_inv @ g
        beta += delta
        if np.max(np.abs(delta)) < tol:
            break
            
    pi = 1.0 / (1.0 + np.exp(-X @ beta))
    W = np.diag(pi * (1.0 - pi))
    I = X.T @ W @ X
    cov = np.linalg.inv(I)
    se = np.sqrt(np.diag(cov))
    
    res = []
    cols = ['Intercept'] + list(X_df.columns)
    for i, name in enumerate(cols):
        b = beta[i]
        s = se[i]
        or_val = np.exp(b)
        ci_low = np.exp(b - 1.96 * s)
        ci_high = np.exp(b + 1.96 * s)
        z = b / s if s > 0 else 0
        p_val = 2 * (1 - stats.norm.cdf(abs(z)))
        res.append({
            'Predictor': name,
            'beta': b,
            'se': s,
            'OR': or_val,
            'ci_low': ci_low,
            'ci_high': ci_high,
            'z': z,
            'p_val': p_val
        })
    return pd.DataFrame(res)

print("\nFirth on full 6 Objective II variables:")
X_full = df[['age', 'hh_size', 'credit_access', 'fertilizer_use', 'modern_tools', 'cooperative_membership']].copy()
# Add education dummies
X_full['edu_12'] = (df['education'] == 12.0).astype(int)
X_full['edu_16'] = (df['education'] == 16.0).astype(int)
print(fit_firth_model(X_full, df['is_poor'].values))
