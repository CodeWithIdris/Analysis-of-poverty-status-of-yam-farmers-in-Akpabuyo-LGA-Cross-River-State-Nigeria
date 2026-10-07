import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

# Test Firth logistic regression implementation
def fit_firth_logit(X, y, max_iter=100, tol=1e-6):
    """
    Firth's penalized likelihood logistic regression.
    X: design matrix with intercept (n x p)
    y: binary response (n,)
    """
    n, p = X.shape
    beta = np.zeros(p)
    
    for i in range(max_iter):
        pi = 1.0 / (1.0 + np.exp(-X @ beta))
        pi = np.clip(pi, 1e-15, 1 - 1e-15)
        W = np.diag(pi * (1.0 - pi))
        
        # Information matrix: X^T W X
        XtW = X.T @ W
        info_mat = XtW @ X
        
        try:
            info_inv = np.linalg.inv(info_mat)
        except np.linalg.LinAlgError:
            info_inv = np.linalg.pinv(info_mat)
            
        # Hat matrix diagonals: h_i = [X (X^T W X)^-1 X^T W]_ii
        # Using sqrt(W) X (X^T W X)^-1 X^T sqrt(W)
        H = np.zeros(n)
        for j in range(n):
            xj = X[j, :]
            H[j] = xj @ info_inv @ xj * (pi[j] * (1.0 - pi[j]))
            
        # Modified score vector: U* = X^T (y - pi + h_i * (0.5 - pi))
        U_star = X.T @ (y - pi + H * (0.5 - pi))
        
        # Update: delta = info_inv @ U_star
        delta = info_inv @ U_star
        beta_new = beta + delta
        
        if np.max(np.abs(delta)) < tol:
            beta = beta_new
            break
        beta = beta_new
        
    # Final statistics
    pi = 1.0 / (1.0 + np.exp(-X @ beta))
    W = np.diag(pi * (1.0 - pi))
    info_mat = X.T @ W @ X
    info_inv = np.linalg.inv(info_mat)
    se = np.sqrt(np.diag(info_inv))
    
    # Penalized log-likelihood
    # log L(beta) + 0.5 * log |X^T W X|
    log_lik_unpen = np.sum(y * np.log(pi) + (1.0 - y) * np.log(1.0 - pi))
    sign, log_det = np.linalg.slogdet(info_mat)
    log_lik_pen = log_lik_unpen + 0.5 * log_det
    
    # Null model (intercept only)
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
    
    # Penalized Likelihood Ratio Test
    lr_stat = 2.0 * (log_lik_pen - log_lik_0_pen)
    df_model = p - 1
    p_lr = 1.0 - stats.chi2.cdf(lr_stat, df_model) if df_model > 0 else 1.0
    
    # Wald z and p-values
    z_scores = beta / se
    p_wald = 2.0 * (1.0 - stats.norm.cdf(np.abs(z_scores)))
    
    # 95% Wald CI
    ci_lower = beta - 1.959964 * se
    ci_upper = beta + 1.959964 * se
    
    return {
        'beta': beta,
        'se': se,
        'z': z_scores,
        'p_wald': p_wald,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'or': np.exp(beta),
        'or_ci_lower': np.exp(ci_lower),
        'or_ci_upper': np.exp(ci_upper),
        'log_lik_unpen': log_lik_unpen,
        'log_lik_pen': log_lik_pen,
        'log_lik_0_pen': log_lik_0_pen,
        'lr_stat': lr_stat,
        'p_lr': p_lr,
        'df': df_model
    }

# Test on our data
df = pd.read_csv('raw_data.csv')
exp_cols = [
    'AVERAGE MONTHLY HOUSEHOLD FOOD EXPENDITURE',
    'AVERAGE MONTHLY HOUSEHOLD EXPENDITURE',
    'AVERAGE MONTHLY HOUSEHOLD  MEDICAL EXPENDITURE',
    'AVERAGE MONTHLY HOUSING AND UTILITY EXPENTITURE',
    'AVERAGE MONTHLY HOUSEHOLD TRANSPORTATION'
]
df['pche'] = df['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE'] / df['HOUSE HOLD SIZE']
pov_line = (2/3) * df['pche'].mean()
df['poor'] = (df['pche'] < pov_line).astype(int)

y = df['poor'].values

# Model A: Total Farm Size + Credit
X_A = sm.add_constant(df[['WHAT IS YOUR TOTAL FARM SIZE', 'ACCESS TO CREDIT FOR YAM FARMING DURING LAST SEASON']].values)
res_A = fit_firth_logit(X_A, y)

print("=== Model A (Firth) ===")
var_names_A = ['Intercept', 'Total Farm Size', 'Access to Credit']
for idx, name in enumerate(var_names_A):
    print(f"{name:20s}: Beta={res_A['beta'][idx]:.4f}, SE={res_A['se'][idx]:.4f}, OR={res_A['or'][idx]:.4f}, 95% CI=[{res_A['or_ci_lower'][idx]:.4f}, {res_A['or_ci_upper'][idx]:.4f}], p={res_A['p_wald'][idx]:.4f}")
print(f"LR Chi2({res_A['df']}) = {res_A['lr_stat']:.4f}, p = {res_A['p_lr']:.6f}")

# Compare with statsmodels standard Logit
logit_mod = sm.Logit(y, X_A)
logit_res = logit_mod.fit(disp=False)
print("\n=== Model A (Standard ML Logit) ===")
print(logit_res.summary())

