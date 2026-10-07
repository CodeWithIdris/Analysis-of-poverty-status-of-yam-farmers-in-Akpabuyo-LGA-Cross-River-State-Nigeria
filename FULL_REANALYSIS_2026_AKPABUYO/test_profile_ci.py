import numpy as np
import pandas as pd
from scipy import stats, optimize
import statsmodels.api as sm

# Firth profile penalized-likelihood CI implementation
def log_pen_lik(beta, X, y):
    pi = 1.0 / (1.0 + np.exp(-X @ beta))
    pi = np.clip(pi, 1e-15, 1 - 1e-15)
    W = np.diag(pi * (1.0 - pi))
    info_mat = X.T @ W @ X
    log_lik_unpen = np.sum(y * np.log(pi) + (1.0 - y) * np.log(1.0 - pi))
    sign, log_det = np.linalg.slogdet(info_mat)
    if sign <= 0:
        return -1e10
    return log_lik_unpen + 0.5 * log_det

def profile_ci_firth(X, y, param_idx, beta_hat, max_pen_ll, alpha=0.05):
    """
    Computes profile penalized-likelihood confidence interval for parameter param_idx.
    Target: 2 * (max_pen_ll - pen_ll(beta_k)) = chi2(1, 1-alpha) = 3.841459
    """
    cutoff = max_pen_ll - 0.5 * stats.chi2.ppf(1 - alpha, 1)
    p = X.shape[1]
    
    # Profile function: for fixed beta[param_idx], maximize over other parameters
    def prof_ll(val):
        other_indices = [i for i in range(p) if i != param_idx]
        if len(other_indices) == 0:
            return log_pen_lik(np.array([val]), X, y)
        
        def obj(other_betas):
            b = np.zeros(p)
            b[param_idx] = val
            for idx, oi in enumerate(other_indices):
                b[oi] = other_betas[idx]
            return -log_pen_lik(b, X, y)
        
        init_guess = beta_hat[other_indices]
        res = optimize.minimize(obj, init_guess, method='BFGS')
        return -res.fun

    # Find lower bound
    def root_lower(val):
        return prof_ll(val) - cutoff

    # Find upper bound
    def root_upper(val):
        return prof_ll(val) - cutoff

    # Bracketing
    se_approx = 1.0
    # Search lower
    step = 0.5
    b_low = beta_hat[param_idx] - step
    while root_lower(b_low) > 0 and b_low > beta_hat[param_idx] - 15:
        b_low -= step
    try:
        lower_limit = optimize.brentq(root_lower, b_low, beta_hat[param_idx])
    except Exception:
        lower_limit = beta_hat[param_idx] - 1.96 * se_approx

    # Search upper
    b_high = beta_hat[param_idx] + step
    while root_upper(b_high) > 0 and b_high < beta_hat[param_idx] + 15:
        b_high += step
    try:
        upper_limit = optimize.brentq(root_upper, beta_hat[param_idx], b_high)
    except Exception:
        upper_limit = beta_hat[param_idx] + 1.96 * se_approx

    return lower_limit, upper_limit

# Test on data
df = pd.read_csv('raw_data.csv')
df['pche'] = df['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE'] / df['HOUSE HOLD SIZE']
z = (2/3) * df['pche'].mean()
y = (df['pche'] < z).astype(int).values

X_A = sm.add_constant(df[['WHAT IS YOUR TOTAL FARM SIZE', 'ACCESS TO CREDIT FOR YAM FARMING DURING LAST SEASON']].values)

# Find max pen log lik
def neg_log_pen(beta):
    return -log_pen_lik(beta, X_A, y)

res_opt = optimize.minimize(neg_log_pen, np.zeros(3), method='BFGS')
beta_opt = res_opt.x
max_ll = -res_opt.fun
print("Beta opt:", beta_opt)
print("Max penalized LL:", max_ll)

for i, name in enumerate(['Intercept', 'Farm Size', 'Credit']):
    low, high = profile_ci_firth(X_A, y, i, beta_opt, max_ll)
    print(f"{name:15s} Beta: {beta_opt[i]:.4f} | Profile 95% CI: [{low:.4f}, {high:.4f}] | OR: {np.exp(beta_opt[i]):.4f} [{np.exp(low):.4f}, {np.exp(high):.4f}]")

