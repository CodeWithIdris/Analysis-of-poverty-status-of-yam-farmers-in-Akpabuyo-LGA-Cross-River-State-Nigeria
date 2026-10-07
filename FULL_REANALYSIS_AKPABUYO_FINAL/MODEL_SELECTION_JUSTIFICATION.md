# Objective III: Multivariable Model Selection and Rationale
## Study: Analysis of Poverty Status of Yam Farmers in Akpabuyo LGA, Nigeria

---

### 1. Econometric Context and Methodological Constraints
In analyzing factors associated with household poverty status, four critical empirical realities dictate the modeling strategy:
1. **Sample Size and Event Count:** The sample comprises $N = 60$ households with exactly $q = 13$ poor households ($21.67\%$).
2. **Events-per-Variable (EPV):** To maintain statistical power and parameter stability, models must be strictly parsimonious ($2-3$ predictors, yielding $4.3-6.5$ EPV).
3. **Quasi-Complete Separation:** Several potential institutional predictors (e.g. extension contact, modern tools, improved varieties) have zero poor adopters ($0/21$ poor had extension contact; $0/6$ had modern tools). In standard Newton-Raphson Maximum Likelihood Estimation (MLE), this causes unbounded parameters ($eta 	o -\infty$) and infinite standard errors.
4. **Mechanical Endogeneity:** Predictors that are arithmetic components of the dependent variable (Household Size in the denominator of PCHE; Total Expenditure in the numerator) must be excluded from multivariable regression to avoid mathematical circularity.

---

### 2. Evaluation of Candidate Firth Models

| Evaluation Dimension | Model A: Farm Size + Credit Access | Model B: Farm Size + Credit Access + Age | Model C: Farm Size + Credit Access + Extension | Model D: Farm Size + Credit Access + Other Income |
| :--- | :--- | :--- | :--- | :--- |
| **Number of Parameters ($k$)** | 3 (Intercept + 2 slopes) | 4 (Intercept + 3 slopes) | 4 (Intercept + 3 slopes) | 4 (Intercept + 3 slopes) |
| **Events per Variable (EPV)** | **6.5 EPV** | 4.3 EPV | 4.3 EPV | 4.3 EPV |
| **Penalized Log-Likelihood** | -24.2882 | -23.7744 | -23.4651 | -24.2709 |
| **Model LR $\chi^2$ ($p$-value)** | **14.234 ($p = 0.00081$)** | 15.262 ($p = 0.00161$) | 15.881 ($p = 0.00120$) | 14.269 ($p = 0.00256$) |
| **Akaike Info Criterion (AIC)** | **54.576** | 55.549 | 54.930 | 56.542 |
| **Bayesian Info Criterion (BIC)** | **60.860** | 63.927 | 63.309 | 64.920 |
| **Nagelkerke Pseudo $R^2$** | 0.3253 (32.53%) | 0.3452 (34.52%) | 0.3570 (35.70%) | 0.3260 (32.60%) |
| **Credit Access Odds Ratio** | **0.1099 ($p = 0.0386$)** | 0.1017 ($p = 0.0340$) | 0.1444 ($p = 0.0772$) | 0.1118 ($p = 0.0407$) |
| **Wald 95% CI for Credit** | **$[0.0136, 0.8905]$** | $[0.0123, 0.8415]$ | $[0.0169, 1.2334]$ | $[0.0137, 0.9103]$ |
| **Profile 95% CI for Credit** | **$[0.0087, 0.7014]$** | $[0.0076, 0.6558]$ | $[0.0094, 1.0482]$ | $[0.0088, 0.7225]$ |
| **Farm Size Odds Ratio** | **0.7421 ($p = 0.6835$)** | 0.8143 ($p = 0.7845$) | 0.8038 ($p = 0.7694$) | 0.7454 ($p = 0.6888$) |
| **Additional Predictor OR** | — | Age: 1.0504 ($p = 0.3159$) | Ext: 0.1602 ($p = 0.1415$) | Other: 0.9328 ($p = 0.9300$) |

---

### 3. Comprehensive Justification for Selecting Model A as the Final Empirical Model

**Model A (Poverty Status ~ Total Farm Size + Access to Credit)** is selected as the primary empirical model based on the following six criteria:

1. **Optimal Information Criteria and Parsimony:** Model A achieves the lowest penalized AIC ($54.576$) and lowest penalized BIC ($60.860$) among all four candidate models. Adding third variables (Age, Extension, Other Income) increases both AIC and BIC without providing statistically significant marginal explanatory power.
2. **Adherence to Small-Sample Diagnostics (EPV):** With 13 poverty events, Model A maintains $6.5$ events per variable, which is the most defensible ratio available in this sample. Models B, C, and D reduce EPV to $4.3$, increasing the risk of overfitting.
3. **Parameter Stability:** Across Models A, B, and D, the estimated odds ratio for credit access is remarkably stable ($	ext{OR} pprox 0.10 - 0.11$, all $p < 0.05$).
4. **Separation Safeguard:** In Model C, Extension Contact exhibits quasi-complete separation ($0/21$ poor had extension contact). While Firth penalization allows Model C to converge, the collinearity between institutional support variables widens the confidence interval for credit ($	ext{OR} = 0.1444, p = 0.0772$). Presenting Extension Contact in the bivariate profile (Fisher $p = 0.0021$) and retaining Credit Access in the parsimonious multivariable model is the most statistically sound strategy.
5. **Absence of Multicollinearity:** The correlation between Total Farm Size and Credit Access is moderate ($r = 0.6077, 	ext{VIF} = 1.5856$, Tolerance = $0.6307$), well within safe econometric limits ($	ext{VIF} < 5.0$).
6. **Robustness across Inference Types:** In Model A, Credit Access is statistically significant under both Wald-type inference ($p = 0.0386$, $95\%	ext{ CI: } [0.0136, 0.8905]$) and Profile Penalized-Likelihood inference ($95\%	ext{ CI: } [0.0087, 0.7014]$, upper bound strictly below 1.0).

---
**END OF MODEL SELECTION JUSTIFICATION**
