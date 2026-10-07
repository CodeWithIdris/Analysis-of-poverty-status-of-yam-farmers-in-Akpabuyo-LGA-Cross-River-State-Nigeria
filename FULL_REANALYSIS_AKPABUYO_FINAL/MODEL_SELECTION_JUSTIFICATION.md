# Objective III: Multivariable Model Selection and Econometric Justification
## Study: Analysis of Poverty Status of Yam Farmers in Akpabuyo LGA, Nigeria

---

### 1. Econometric Context and Methodological Constraints
In analyzing factors associated with household poverty status, several critical empirical and statistical considerations dictate the modeling strategy:
1. **Economic Theory:** Smallholder agricultural poverty is fundamentally shaped by productive assets (land operated) and institutional capital (access to credit), which govern farmers' ability to purchase planting setts, hire seasonal labour, and smooth consumption.
2. **Sample Size and Sparse Event Count:** The sample comprises $N = 60$ households with exactly $q = 13$ poor households ($21.67\%$). Standard regression guidelines require maintaining a viable Events-per-Variable (EPV) ratio ($>5$ EPV) to avoid severe parameter instability.
3. **Parsimony:** With 13 events, including more than 2 or 3 parameters causes severe degrees-of-freedom depletion and overfitting.
4. **Quasi-Complete Separation in Institutional Predictors:** Several candidate institutional predictors (e.g., extension contact: $0/21$ poor had contact; modern farm tools: $0/6$ poor used modern tools; improved varieties: $0/2$ poor adopted) exhibit zero poor adopters. In ordinary Newton-Raphson Maximum Likelihood Estimation (MLE), this causes complete separation ($\beta \to -\infty$) and infinite standard errors.
5. **Absence of Outcome Leakage and Mechanical Circularity:** Variables that mechanically define the welfare metric (Household Size in the denominator of PCHE; Total Monthly Expenditure in the numerator; Food Expenditure) must be strictly excluded from multivariable regressions to prevent circular statistical artifacts.
6. **Firth Bias Reduction:** Firth's penalized likelihood logistic regression is employed to resolve small-sample small-event bias and guarantee finite, stable parameter estimates and profile-likelihood confidence intervals.

---

### 2. Multi-Criteria Evaluation of Candidate Firth Models

| Evaluation Criterion | Model A: Farm Size + Credit Access | Model B: Farm Size + Credit Access + Age | Model C: Farm Size + Credit Access + Extension | Model D: Farm Size + Credit Access + Other Income |
| :--- | :--- | :--- | :--- | :--- |
| **Theoretical Grounding** | Asset base (Land) + Institutional liquidity (Credit) | Adds life-cycle demographic factor | Adds advisory institutional factor | Adds off-farm diversification factor |
| **Number of Parameters ($k$)** | 3 (Intercept + 2 slopes) | 4 (Intercept + 3 slopes) | 4 (Intercept + 3 slopes) | 4 (Intercept + 3 slopes) |
| **Events per Variable (EPV)** | **6.5 EPV** (Safest small-sample ratio) | 4.3 EPV (Depleted) | 4.3 EPV (Depleted) | 4.3 EPV (Depleted) |
| **Penalized Log-Likelihood** | -24.2882 | -23.7744 | -23.4651 | -24.2709 |
| **Model LR $\chi^2$ ($p$-value)** | **14.234 ($p = 0.00081$)** | 15.262 ($p = 0.00161$) | 15.881 ($p = 0.00120$) | 14.269 ($p = 0.00256$) |
| **Akaike Info Criterion (AIC)** | **54.576** (Lowest / Best) | 55.549 | 54.930 | 56.542 |
| **Bayesian Info Criterion (BIC)** | **60.860** (Lowest / Best) | 63.927 | 63.309 | 64.920 |
| **Nagelkerke Pseudo $R^2$** | 0.3253 (32.53%) | 0.3452 (34.52%) | 0.3570 (35.70%) | 0.3260 (32.60%) |
| **Credit Access Odds Ratio** | **0.1099 ($p = 0.0386$)** | 0.1017 ($p = 0.0340$) | 0.1444 ($p = 0.0772$) | 0.1118 ($p = 0.0407$) |
| **Wald 95% CI for Credit** | **$[0.0136, 0.8905]$** | $[0.0123, 0.8415]$ | $[0.0169, 1.2334]$ | $[0.0137, 0.9103]$ |
| **Profile 95% CI for Credit** | **$[0.0087, 0.7014]$** | $[0.0076, 0.6558]$ | $[0.0094, 1.0482]$ | $[0.0088, 0.7225]$ |
| **Farm Size Odds Ratio** | **0.7421 ($p = 0.6835$)** | 0.8143 ($p = 0.7845$) | 0.8038 ($p = 0.7694$) | 0.7454 ($p = 0.6888$) |
| **Additional Predictor OR** | — | Age: 1.0504 ($p = 0.3159$) | Ext: 0.1602 ($p = 0.1415$) | Other: 0.9328 ($p = 0.9300$) |
| **Coefficient Stability** | High (Robust across specifications) | Stable | Collinear widening | Stable |
| **Convergence & Separation** | Smooth convergence; no separation | Smooth convergence | Zero cell in poor group ($0/21$) | Smooth convergence |

---

### 3. Justification for Selecting Model A as the Final Inferential Model

Model A is NOT selected merely because of a single $p$-value or information criterion score. Rather, its selection is justified through a comprehensive, multi-criteria econometric assessment:

1. **Theoretical Coherence:** Farm size captures physical productive capacity, while credit access captures liquidity to acquire inputs and hire labour. These represent the primary structural assets in smallholder farming.
2. **Parsimony and Sample Capacity:** With only 13 poverty events in the sample, Model A maintains an Events-per-Variable ratio of **6.5 EPV**, which respects standard econometric guidelines. Adding third variables degrades EPV to 4.3, increasing susceptibility to sample-specific noise.
3. **Absence of Outcome Leakage:** Model A completely excludes mechanically confounding variables (household size, total expenditure, food spending), ensuring all estimated relationships reflect behavioral and institutional patterns rather than mathematical circularity.
4. **Coefficient Stability and Bounded CIs:** The estimated odds ratio for credit access is highly stable ($\text{OR} \approx 0.10 - 0.11$) across Models A, B, and D. Furthermore, in Model A, both the Wald 95% CI ($[0.0136, 0.8905]$) and the Profile Penalized-Likelihood 95% CI ($[0.0087, 0.7014]$) have upper bounds strictly below 1.0, establishing robust statistical significance.
5. **Mitigation of Separation Artifacts:** In Model C, extension contact has zero poor recipients ($0/21$), which widens the confidence interval for credit access ($[0.0169, 1.2334], p = 0.0772$) due to institutional cross-correlation. The appropriate methodological strategy is to present Extension Contact in the descriptive/bivariate profile (Fisher's exact $p = 0.0021$) and retain Credit Access in the stable multivariable model.
6. **Information Criteria Concordance:** Model A achieves the lowest penalized AIC ($54.576$) and lowest penalized BIC ($60.860$), confirming that adding additional predictors does not provide sufficient explanatory gain to offset the model complexity penalty.
7. **Convergence and Global Fit:** Model A converges smoothly in 5 iterations, yielding a highly significant penalized likelihood ratio test ($\chi^2(2) = 14.2342, p = 0.000811$) and explaining $32.53\%$ of generalized variation (Nagelkerke $R^2 = 0.3253$).

---
**END OF MODEL SELECTION JUSTIFICATION**
