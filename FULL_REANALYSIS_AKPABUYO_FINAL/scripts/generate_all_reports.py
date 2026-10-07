import os
import sys

# Generate all 5 Markdown files in FULL_REANALYSIS_AKPABUYO_FINAL/

print("Generating 5 Markdown documentation and report files in FULL_REANALYSIS_AKPABUYO_FINAL/...")

# ------------------------------------------------------------------------------
# 1. DATA_CORRECTIONS_LOG.md
# ------------------------------------------------------------------------------
with open('FULL_REANALYSIS_AKPABUYO_FINAL/DATA_CORRECTIONS_LOG.md', 'w', encoding='utf-8') as f:
    f.write("""# Data Corrections and Audit Log
## Study: Analysis of Poverty Status of Yam Farmers in Akpabuyo LGA, Nigeria
**Primary Source:** `raw_data.csv` (N = 60 households, 46 columns, MD5: `628f44079ed97d91b232533b3c14e014`)  
**Audit Date:** October 2026  
**Auditor:** Antigravity AI Data & Statistical Audit System  

---

### Executive Summary of Forensic Data Audit
This document records every data anomaly, coding inconsistency, arithmetic discrepancy, and analytical decision identified during the independent forensic audit of the raw dataset. In accordance with scientific integrity standards, no raw data values were silently manipulated to force congruence with historical thesis tables.

---

### Log of Specific Data Items Audited

#### 1. Sex of Household Head Coding Anomaly (Respondent 46)
- **Raw Value:** In `raw_data.csv`, Row 46 (Respondent ID 46) has `SEX = 2.0`.
- **Questionnaire & Codebook Standard:** The survey questionnaire specifies two options (`Male [ ]`, `Female [ ]`), and the codebook defines `1 = Male`, `0 = Female`.
- **Historical Thesis Handling:** Previous thesis drafts recoded Respondent 46 from `2.0` to `0.0` (Female) without documentation, solely to obtain the historical frequency of 36 Males (60.0%) and 24 Females (40.0%).
- **Independent Forensic Decision:**
  - There is no authoritative evidence in the raw coding sheet defining `2 = Female`.
  - In the primary empirical re-analysis, Respondent 46 is treated as **unspecified/invalid for sex** (Valid $n = 59$: 36 Male [61.02%], 23 Female [38.98%], 1 Unspecified [1.69%]).
  - A sensitivity distribution showing the historical assumption (36 Male, 24 Female) is provided for full transparency.
  - **Impact on Inference:** Bivariate association between sex and poverty status remains statistically non-significant under both treatments (Empirical $n=59$: $\chi^2 = 0.463, p = 0.496$, Fisher $p = 0.575$; Historical $N=60$: $\chi^2 = 0.266, p = 0.606$, Fisher $p = 0.748$). Sex is not retained in multivariable modeling.

#### 2. Monthly Household Expenditure Reconciliation
- **Audit Procedure:** For every respondent ($i = 1, \dots, 60$), the reported total monthly expenditure (`TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE`) was compared against the arithmetic sum of the five constituent expenditure categories: Food (`EXP_FOOD`) + Education (`EXP_EDUC`) + Medical (`EXP_HEALTH`) + Housing/Utilities (`EXP_HOUSING`) + Transportation/Other (`EXP_TRANS`).
- **Concordance Rate:** Exactly **56 out of 60 households (93.33%)** showed zero discrepancy ($\text{Diff} = ₦0.00$).
- **Discrepant Observations (4 Households, 6.67%):**
  1. **Respondent 14:** Reported Total = ₦118,000.00 | Component Sum = ₦117,000.00 | Signed Discrepancy = $+₦1,000.00$ ($+0.85\%$)
  2. **Respondent 37:** Reported Total = ₦109,000.00 | Component Sum = ₦109,400.00 | Signed Discrepancy = $-₦400.00$ ($-0.37\%$)
  3. **Respondent 39:** Reported Total = ₦103,000.00 | Component Sum = ₦102,500.00 | Signed Discrepancy = $+₦500.00$ ($+0.49\%$)
  4. **Respondent 59:** Reported Total = ₦223,500.00 | Component Sum = ₦113,500.00 | Signed Discrepancy = $+₦110,000.00$ ($+96.92\%$)
- **Aggregate Sample Discrepancy:**
  - Total absolute discrepancy across all 60 households = **₦111,900.00**
  - Mean absolute discrepancy per household = **₦1,865.00**
  - Median discrepancy = **₦0.00**
  - Maximum discrepancy = **₦110,000.00** (Respondent 59)
- **Analytical Handling & Sensitivity Decision:**
  - Reported total expenditure is retained as the **primary welfare measure** because it represents the household's overarching stated monthly budget.
  - A complete parallel sensitivity analysis was executed using the component-sum aggregate (Mean PCHE = ₦20,022.82, Poverty Line = ₦13,348.55, Poor = 12, Non-poor = 48).
  - Classification agreement between the two definitions is **59/60 (98.33%)**, with a Cohen's kappa of **$\kappa = 0.9495$ (near-perfect agreement)**. Only one borderline case (Respondent 25: PCHE = ₦13,500.00) shifts classification.
  - Therefore, poverty classification is highly robust to the expenditure reconciliation alternative examined.

#### 3. Challenge Variable Missing Value (Respondent 46)
- **Finding:** In Section D, Item 8 (`LOW AND UNSTABLE PRICES OF YAM`), Respondent 46 has an empty/NaN cell.
- **Handling:** Pairwise valid-case analysis is applied. Item 8 is computed on **valid $n = 59$** (MSI = 3.1186, SD = 0.8727, Median = 3.0, IQR = 1.0, Rank 9, Moderate Challenge). All other 9 challenge items have $N = 60$ complete responses.

#### 4. Challenge Likert Scale Structure Correction
- **Finding:** Historical thesis text in Chapter 3 mistakenly described the challenge scale as a 4-point Likert scale (with cutoffs like 2.50).
- **Correction:** Inspection of the research instrument (`QUESTIONNAIRE_FINAL.docx`) and raw response values ($1, 2, 3, 4, 5$) confirms an authoritative **5-point Likert scale**:
  - $1 = \text{Not a Challenge}$
  - $2 = \text{Minor Challenge}$
  - $3 = \text{Moderate Challenge}$
  - $4 = \text{Severe Challenge}$
  - $5 = \text{Very Severe Challenge}$
- **Severity Intervals:** $1.00–1.80$ (Not a Challenge), $1.81–2.60$ (Minor), $2.61–3.40$ (Moderate), $3.41–4.20$ (Severe), $4.21–5.00$ (Very Severe).

#### 5. Multicollinearity & VIF Correction
- **Finding:** Previous draft texts reported an impossible combination of $r = 0.6077$ and $\text{VIF} = 1.004$ between Farm Size and Credit Access, erroneously claiming orthogonality.
- **Correction:** Re-computation directly from the predictor matrix establishes:
  - Pearson correlation $r = 0.6077$, Spearman rank correlation $r_s = 0.6561$.
  - $r^2 = 0.3693 \implies \text{VIF} = \frac{1}{1 - 0.3693} = \mathbf{1.5856}$, Tolerance = $\mathbf{0.6307}$.
  - This confirms moderate, non-harmful collinearity well below standard thresholds ($\text{VIF} < 5.0$).
  - Farm Size and Yam Cultivated Area share extreme collinearity ($r = 0.9642, \text{VIF} = 14.2120$), confirming that Yam Area must not be included simultaneously in multivariable models.

---
**END OF DATA CORRECTIONS LOG**
""")
print("1/5: DATA_CORRECTIONS_LOG.md written.")

# ------------------------------------------------------------------------------
# 2. REPRODUCIBILITY_NOTES.md
# ------------------------------------------------------------------------------
with open('FULL_REANALYSIS_AKPABUYO_FINAL/REPRODUCIBILITY_NOTES.md', 'w', encoding='utf-8') as f:
    f.write("""# Methodological and Reproducibility Notes
## Study: Analysis of Poverty Status of Yam Farmers in Akpabuyo LGA, Nigeria

---

### 1. Mathematical and Statistical Formulation

#### 1.1 Per Capita Household Expenditure (PCHE)
For each household $i \in \{1, \dots, N\}$:
$$\text{PCHE}_i = \frac{\text{Total Monthly Household Expenditure}_i}{\text{Household Size}_i}$$

#### 1.2 Relative Poverty Line ($z$)
$$z = \frac{2}{3} \times \overline{\text{PCHE}} = \frac{2}{3} \times \left( \frac{1}{N} \sum_{i=1}^N \text{PCHE}_i \right)$$
For the primary reported total expenditure ($N = 60$):
$$\overline{\text{PCHE}} = ₦20,289.03 \implies z = \frac{2}{3} \times ₦20,289.03 = \mathbf{₦13,526.02}$$

#### 1.3 Foster–Greer–Thorbecke (FGT, 1984) Poverty Measures
$$P_\alpha = \frac{1}{N} \sum_{i=1}^q \left( \frac{z - y_i}{z} \right)^\alpha$$
where $y_i = \text{PCHE}_i$, $q = \sum_{i=1}^N \mathbb{I}(y_i < z)$ is the number of poor households, and $\alpha \ge 0$.
- **$\alpha = 0$ (Headcount Ratio $P_0$):** $P_0 = \frac{q}{N} = \frac{13}{60} = \mathbf{0.2167 \text{ (21.67\%)}}$
- **$\alpha = 1$ (Poverty Gap Index $P_1$):** $P_1 = \frac{1}{N} \sum_{i=1}^q \left( \frac{z - y_i}{z} \right) = \mathbf{0.0232 \text{ (2.32\%)}}$
- **$\alpha = 2$ (Poverty Severity Index $P_2$):** $P_2 = \frac{1}{N} \sum_{i=1}^q \left( \frac{z - y_i}{z} \right)^2 = \mathbf{0.0034 \text{ (0.34\%)}}$

#### 1.4 Firth (1993) Bias-Reduced Penalized Logistic Regression
To handle sparse events ($q = 13$) and complete separation in institutional variables, Firth's penalized maximum likelihood modifies the log-likelihood by the Jeffreys invariant prior:
$$\ell^*(\beta) = \ell(\beta) + \frac{1}{2} \ln |I(\beta)|$$
where $I(\beta) = X^T W X$ is the Fisher information matrix and $W = \operatorname{diag}(\pi_i (1 - \pi_i))$.
The modified score equations solved iteratively are:
$$U^*(\beta) = X^T \left( y - \pi + h \odot (0.5 - \pi) \right) = 0$$
where $h_i = [X (X^T W X)^{-1} X^T W]_{ii}$ are the diagonal elements of the hat matrix.

#### 1.5 Confidence Interval Procedures
1. **Wald-type 95% Confidence Interval:**
   $$\beta_j \pm 1.959964 \times \operatorname{SE}(\beta_j) \implies \text{OR 95\% CI: } \left[ \exp(\beta_j - 1.96 \cdot \text{SE}), \exp(\beta_j + 1.96 \cdot \text{SE}) \right]$$
2. **Profile Penalized-Likelihood 95% Confidence Interval:**
   Inverting the penalized likelihood ratio test:
   $$\left\{ \beta_j : 2 \left( \ell^*(\hat{\beta}) - \ell^*(\beta_j, \hat{\beta}_{-j}(\beta_j)) \right) \le \chi^2_{1, 0.95} = 3.841459 \right\}$$
   - For Credit Access: Profile 95% CI is $[-4.7388, -0.3546] \implies \text{OR} \in [0.0087, 0.7014]$.
   - For Farm Size: Profile 95% CI is $[-1.9780, 1.0837] \implies \text{OR} \in [0.1383, 2.9557]$.

#### 1.6 Mean Severity Index (MSI) for Challenges
$$\text{MSI} = \frac{\sum_{k=1}^5 f_k \cdot k}{\sum_{k=1}^5 f_k} = \frac{1(f_1) + 2(f_2) + 3(f_3) + 4(f_4) + 5(f_5)}{n}$$

---

### 2. Computational Software and Execution Environment
- **Platform:** Python 3.14 (Windows 64-bit environment)
- **Key Libraries:**
  - `pandas` (v2.3.3) for tabular data operations
  - `numpy` (v2.4.2) for numerical matrix algebra
  - `scipy` (v1.17.0) for exact non-parametric tests and optimization (`scipy.optimize.brentq`, `scipy.optimize.minimize`)
  - `statsmodels` (v0.14.6) for MLE logit and diagnostic comparisons
  - `openpyxl` (v3.1.5) for Excel XML generation with styling and formatting
- **Primary Script:** [`FULL_REANALYSIS_AKPABUYO_FINAL/scripts/master_analysis.py`](file:///c:/Users/idrid/OneDrive/Documents/ResearchReady%20Docs/Final%20year%20Project/Mama%20Fire/Data%20analysis/FULL_REANALYSIS_AKPABUYO_FINAL/scripts/master_analysis.py)

---
**END OF REPRODUCIBILITY NOTES**
""")
print("2/5: REPRODUCIBILITY_NOTES.md written.")

# ------------------------------------------------------------------------------
# 3. MODEL_SELECTION_JUSTIFICATION.md
# ------------------------------------------------------------------------------
with open('FULL_REANALYSIS_AKPABUYO_FINAL/MODEL_SELECTION_JUSTIFICATION.md', 'w', encoding='utf-8') as f:
    f.write("""# Objective III: Multivariable Model Selection and Rationale
## Study: Analysis of Poverty Status of Yam Farmers in Akpabuyo LGA, Nigeria

---

### 1. Econometric Context and Methodological Constraints
In analyzing factors associated with household poverty status, four critical empirical realities dictate the modeling strategy:
1. **Sample Size and Event Count:** The sample comprises $N = 60$ households with exactly $q = 13$ poor households ($21.67\%$).
2. **Events-per-Variable (EPV):** To maintain statistical power and parameter stability, models must be strictly parsimonious ($2-3$ predictors, yielding $4.3-6.5$ EPV).
3. **Quasi-Complete Separation:** Several potential institutional predictors (e.g. extension contact, modern tools, improved varieties) have zero poor adopters ($0/21$ poor had extension contact; $0/6$ had modern tools). In standard Newton-Raphson Maximum Likelihood Estimation (MLE), this causes unbounded parameters ($\beta \to -\infty$) and infinite standard errors.
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
3. **Parameter Stability:** Across Models A, B, and D, the estimated odds ratio for credit access is remarkably stable ($\text{OR} \approx 0.10 - 0.11$, all $p < 0.05$).
4. **Separation Safeguard:** In Model C, Extension Contact exhibits quasi-complete separation ($0/21$ poor had extension contact). While Firth penalization allows Model C to converge, the collinearity between institutional support variables widens the confidence interval for credit ($\text{OR} = 0.1444, p = 0.0772$). Presenting Extension Contact in the bivariate profile (Fisher $p = 0.0021$) and retaining Credit Access in the parsimonious multivariable model is the most statistically sound strategy.
5. **Absence of Multicollinearity:** The correlation between Total Farm Size and Credit Access is moderate ($r = 0.6077, \text{VIF} = 1.5856$, Tolerance = $0.6307$), well within safe econometric limits ($\text{VIF} < 5.0$).
6. **Robustness across Inference Types:** In Model A, Credit Access is statistically significant under both Wald-type inference ($p = 0.0386$, $95\%\text{ CI: } [0.0136, 0.8905]$) and Profile Penalized-Likelihood inference ($95\%\text{ CI: } [0.0087, 0.7014]$, upper bound strictly below 1.0).

---
**END OF MODEL SELECTION JUSTIFICATION**
""")
print("3/5: MODEL_SELECTION_JUSTIFICATION.md written.")

# ------------------------------------------------------------------------------
# 4. THESIS_TABLES_FINAL.md
# ------------------------------------------------------------------------------
with open('FULL_REANALYSIS_AKPABUYO_FINAL/THESIS_TABLES_FINAL.md', 'w', encoding='utf-8') as f:
    f.write("""# Final Publication Tables for Chapter 4 Thesis Reconstruction
## Analysis of Poverty Status of Yam Farmers in Akpabuyo LGA, Cross River State, Nigeria

---

### Table 4.1: Socio-Economic Characteristics of Yam Farmers in Akpabuyo LGA
| Characteristic | Category | Frequency ($n$) | Percentage ($\%$) | Mean $\pm$ SD | Median (IQR) | Min–Max |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Sex of Household Head** | Male | 36 | 61.02% | — | — | — |
| *(Valid $n = 59$)* | Female | 23 | 38.98% | — | — | — |
| | Unspecified / Invalid (Code 2) | 1 | 1.69% | — | — | — |
| *(Historical Assumption $N=60$)*| Male: 36 (60.00%) | Female: 24 (40.00%) | — | — | — | — |
| **Age of Household Head (Years)**| < 40 years | 14 | 23.33% | $46.03 \pm 8.64$ | 46.00 (13.00) | 30.0–63.0 |
| | 40–49 years | 26 | 43.33% | | | |
| | 50–59 years | 16 | 26.67% | | | |
| | $\ge 60$ years | 4 | 6.67% | | | |
| **Marital Status** | Single | 5 | 8.33% | — | — | — |
| | Married | 49 | 81.67% | — | — | — |
| | Widowed | 6 | 10.00% | — | — | — |
| **Educational Level** | Primary Education (6 yrs) | 18 | 30.00% | $11.20 \pm 3.79$ | 12.00 (6.00) | 6.0–16.0 |
| | Secondary Education (12 yrs) | 27 | 45.00% | | | |
| | Tertiary Education (16 yrs) | 15 | 25.00% | | | |
| **Household Size (Persons)** | 1–4 persons | 10 | 16.67% | $6.23 \pm 1.84$ | 6.00 (2.00) | 3.0–10.0 |
| | 5–7 persons | 36 | 60.00% | | | |
| | 8–10 persons | 14 | 23.33% | | | |
| **Farming Experience (Years)** | < 10 years | 8 | 13.33% | $18.88 \pm 8.56$ | 17.50 (11.00) | 6.0–40.0 |
| | 10–19 years | 29 | 48.33% | | | |
| | 20–29 years | 16 | 26.67% | | | |
| | $\ge 30$ years | 7 | 11.67% | | | |
| **Other Income Source** | Yes | 49 | 81.67% | — | — | — |
| | No | 11 | 18.33% | — | — | — |

*Source: Field Survey, 2026.*

---

### Table 4.2: Farm, Production, and Institutional Characteristics of Yam Farmers
| Characteristic | Category | Frequency ($n$) | Percentage ($\%$) | Mean $\pm$ SD | Median (IQR) | Min–Max |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Total Farm Size (Hectares)** | < 2.0 ha | 19 | 31.67% | $2.43 \pm 0.79$ | 2.20 (1.00) | 1.2–5.0 |
| | 2.0–2.9 ha | 28 | 46.67% | | | |
| | $\ge 3.0$ ha | 13 | 21.67% | | | |
| **Yam Cultivated Area (Hectares)**| < 1.5 ha | 22 | 36.67% | $1.67 \pm 0.53$ | 1.50 (0.80) | 0.9–3.5 |
| | 1.5–1.9 ha | 24 | 40.00% | | | |
| | $\ge 2.0$ ha | 14 | 23.33% | | | |
| **Access to Credit** | Yes | 30 | 50.00% | — | — | — |
| | No | 30 | 50.00% | — | — | — |
| **Credit Amount Accessed (₦)** | Recipient Households ($n=30$) | 30 | 50.00% | $73,166.67 \pm 48,154.91$ | 60,000 (65,000) | 25,000–200,000 |
| | Full Sample ($N=60$) | 60 | 100.00% | $36,583.33 \pm 49,927.84$ | 12,500 (65,000) | 0–200,000 |
| **Extension Contact (in 12m)** | Yes | 21 | 35.00% | — | — | — |
| | No | 39 | 65.00% | — | — | — |
| **Cooperative Membership** | Member | 49 | 81.67% | — | — | — |
| | Non-Member | 11 | 18.33% | — | — | — |
| **Use of Improved Varieties** | Yes | 2 | 3.33% | — | — | — |
| | No | 58 | 96.67% | — | — | — |
| **Fertilizer/Manure Use** | Yes | 48 | 80.00% | — | — | — |
| | No | 12 | 20.00% | — | — | — |
| **Use of Modern Farm Tools** | Yes | 6 | 10.00% | — | — | — |
| | No | 54 | 90.00% | — | — | — |

*Source: Field Survey, 2026.*

---

### Table 4.3: Monthly Household Expenditure Allocation and Budget Shares
| Expenditure Category | Full Sample ($N=60$) Mean $\pm$ SD (₦) | Median (IQR) (₦) | Poor Households ($n=13$) Mean $\pm$ SD (₦) | Non-Poor Households ($n=47$) Mean $\pm$ SD (₦) | Budget Share (Poor) | Budget Share (Non-Poor) | Budget Share (Total Sample) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Food Expenditure** | $60,703.33 \pm 13,713.47$ | 58,100 (15,900) | $61,723.08 \pm 18,348.67$ | $60,421.28 \pm 12,328.79$ | 61.11% | 50.38% | 52.40% |
| **Education Expenditure**| $14,528.33 \pm 6,830.07$ | 13,250 (8,500) | $10,138.46 \pm 3,119.37$ | $15,742.55 \pm 7,163.66$ | 10.04% | 13.13% | 12.54% |
| **Health / Medical Care** | $8,631.67 \pm 2,592.85$ | 8,000 (3,000) | $7,000.00 \pm 1,607.28$ | $9,082.98 \pm 2,642.44$ | 6.93% | 7.57% | 7.45% |
| **Housing & Utilities** | $18,246.67 \pm 5,747.50$ | 18,000 (7,500) | $13,923.08 \pm 2,548.25$ | $19,442.55 \pm 5,876.54$ | 13.79% | 16.21% | 15.75% |
| **Transportation & Other**| $11,875.83 \pm 4,128.48$ | 10,500 (5,000) | $8,215.38 \pm 1,327.18$ | $12,887.23 \pm 4,166.42$ | 8.13% | 10.74% | 10.25% |
| **Total Monthly Expenditure**| $115,837.50 \pm 27,652.42$| 111,000 (38,000)| $101,000.00 \pm 23,245.07$| $119,941.49 \pm 27,614.88$| 100.00% | 100.00% | 100.00% |
| **Per Capita Exp. (PCHE)**| $20,289.03 \pm 7,585.87$ | 18,883 (8,708) | $12,079.49 \pm 1,241.13$ | $22,559.76 \pm 6,903.01$ | — | — | — |

*Note: Component sum average is ₦113,985.83 (56/60 exact matches, 98.33% classification agreement).*

---

### Table 4.4: Poverty Line Determination and Household Poverty Status Distribution
| Poverty Status Category | Monthly Per Capita Expenditure Threshold ($z$) | Frequency ($n$) | Percentage ($\%$) | Mean PCHE (₦) | Standard Deviation (₦) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Poor Households** | $\text{PCHE} < ₦13,526.02$ | **13** | **21.67%** | ₦12,079.49 | ₦1,241.13 |
| **Non-Poor Households** | $\text{PCHE} \ge ₦13,526.02$ | **47** | **78.33%** | ₦22,559.76 | ₦6,903.01 |
| **Total Sample** | Mean PCHE = ₦20,289.03 ($2/3\text{ Mean } = ₦13,526.02$) | **60** | **100.00%** | ₦20,289.03 | ₦7,585.87 |

*Source: Computed from Survey Data, 2026.*

---

### Table 4.5: Foster–Greer–Thorbecke (FGT) Poverty Indices and Gap Analysis
| Poverty Index | Parameter ($\alpha$) | Index Value | Percentage Form ($\%$) | Economic Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| **Headcount Ratio ($P_0$)** | $\alpha = 0$ | **0.2167** | **21.67%** | $21.67\%$ of yam farming households live below the sample-relative poverty threshold. |
| **Poverty Gap Index ($P_1$)** | $\alpha = 1$ | **0.0232** | **2.32%** | The population poverty deficit equals $2.32\%$ of the poverty line. |
| **Poverty Severity Index ($P_2$)**| $\alpha = 2$ | **0.0034** | **0.34%** | Measures poverty severity through squared normalized gaps; reflects low extreme deprivation. |
| **Mean PCHE of Poor** | — | **₦12,079.49** | — | Average monthly consumption expenditure per capita among the 13 poor households. |
| **Average Monthly Poverty Gap** | — | **₦1,446.53** | — | Average monthly transfer required per poor person to eliminate consumption poverty. |
| **Income Gap Ratio ($I$)** | — | **0.1069** | **10.69%** | Average depth of poverty among the poor as a percentage of the poverty line. |

*Source: Computed from Survey Data, 2026.*

---

### Table 4.6: Poverty Status Profile Across Socioeconomic and Farm Characteristics
| Characteristic | Category / Metric | Poor Households ($n=13$) | Non-Poor Households ($n=47$) | Total Sample ($N=60$) | Within-Group Poverty Rate |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Sex of Head** *(n=59)* | Male | 7 (53.85%) | 29 (63.04%) | 36 (61.02%) | 19.44% |
| | Female | 6 (46.15%) | 17 (36.96%) | 23 (38.98%) | 26.09% |
| **Marital Status** | Married | 10 (76.92%) | 39 (82.98%) | 49 (81.67%) | 20.41% |
| | Single / Widowed | 3 (23.08%) | 8 (17.02%) | 11 (18.33%) | 27.27% |
| **Education Level** | Primary Education (6 yrs) | 6 (46.15%) | 12 (25.53%) | 18 (30.00%) | 33.33% |
| | Secondary Education (12 yrs) | 5 (38.46%) | 22 (46.81%) | 27 (45.00%) | 18.52% |
| | Tertiary Education (16 yrs) | 2 (15.38%) | 13 (27.66%) | 15 (25.00%) | 13.33% |
| **Access to Credit** | Yes | 1 (7.69%) | 29 (61.70%) | 30 (50.00%) | 3.33% |
| | No | 12 (92.31%) | 18 (38.30%) | 30 (50.00%) | 40.00% |
| **Extension Contact** | Yes | 0 (0.00%) | 21 (44.68%) | 21 (35.00%) | 0.00% |
| | No | 13 (100.00%) | 26 (55.32%) | 39 (65.00%) | 33.33% |
| **Cooperative Membership** | Member | 11 (84.62%) | 38 (80.85%) | 49 (81.67%) | 22.45% |
| | Non-Member | 2 (15.38%) | 9 (19.15%) | 11 (18.33%) | 18.18% |
| **Age (Years)** | Mean $\pm$ SD [Median, IQR] | $51.31 \pm 8.99$ [52.0, 15.0] | $44.57 \pm 8.04$ [44.0, 10.0] | $46.03 \pm 8.64$ [46.0, 13.0] | — |
| **Household Size (Persons)**| Mean $\pm$ SD [Median, IQR] | $8.31 \pm 1.70$ [8.0, 3.0] | $5.66 \pm 1.43$ [5.0, 2.0] | $6.23 \pm 1.84$ [6.0, 2.0] | — |
| **Farming Experience (Years)**| Mean $\pm$ SD [Median, IQR] | $25.77 \pm 10.48$ [28.0, 15.0]| $16.98 \pm 6.94$ [15.0, 9.0] | $18.88 \pm 8.56$ [17.5, 11.0]| — |
| **Total Farm Size (ha)** | Mean $\pm$ SD [Median, IQR] | $1.98 \pm 0.48$ [2.0, 0.7] | $2.56 \pm 0.82$ [2.4, 1.05] | $2.43 \pm 0.79$ [2.2, 1.0] | — |
| **Yam Cultivated Area (ha)**| Mean $\pm$ SD [Median, IQR] | $1.43 \pm 0.37$ [1.4, 0.6] | $1.73 \pm 0.56$ [1.6, 0.8] | $1.67 \pm 0.53$ [1.5, 0.8] | — |

*Source: Computed from Survey Data, 2026.*

---

### Table 4.7: Bivariate Analysis of Factors Associated with Poverty Status
| Predictor Variable | Test Type Applied | Test Statistic | df | $p$-value | Effect Size Metric | Effect Size Value | Analytical Role & Diagnostic Notes |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: | :--- |
| **Access to Credit** | Fisher's Exact / $\chi^2$ | $\chi^2 = 9.820$ | 1 | **0.0012\*** | Cramér's $V$ | **0.4046** | Primary multivariable candidate ($p < 0.01$). |
| **Extension Contact** | Fisher's Exact Test | $\chi^2 = 8.878$ | 1 | **0.0021\*** | Cramér's $V$ | **0.3847** | Complete separation ($0$ poor with extension). |
| **Farming Experience** | Mann–Whitney U | $U = 456.00$ | — | **0.0090\*** | Rank-biserial $r_{rb}$ | **+0.4926** | Poor farmers had more farming experience. |
| **Total Farm Size** | Mann–Whitney U | $U = 170.50$ | — | **0.0160\*** | Rank-biserial $r_{rb}$ | **-0.4419** | Primary multivariable candidate. |
| **Age of Household Head**| Mann–Whitney U | $U = 432.00$ | — | **0.0240\*** | Rank-biserial $r_{rb}$ | **+0.4141** | Evaluated in candidate Model B. |
| **Total Monthly Income** | Mann–Whitney U | $U = 193.50$ | — | **0.0460\*** | Rank-biserial $r_{rb}$ | **-0.3666** | Proxy for household economic capacity. |
| **Yam Cultivated Area** | Mann–Whitney U | $U = 205.00$ | — | 0.0720 | Rank-biserial $r_{rb}$ | -0.3290 | High collinearity with farm size ($r=0.964$). |
| **Monthly Yam Sales** | Mann–Whitney U | $U = 226.50$ | — | 0.1630 | Rank-biserial $r_{rb}$ | -0.2586 | Non-significant bivariate association. |
| **Modern Tools Use** | Fisher's Exact Test | — | 1 | 0.3240 | Cramér's $V$ | 0.1751 | Cell sparsity ($n=6$ adopters). |
| **Other Income Source** | Fisher's Exact / $\chi^2$ | $\chi^2 = 1.487$ | 1 | 0.2390 | Cramér's $V$ | 0.1574 | Evaluated in candidate Model D. |
| **Education Level** | Pearson $\chi^2$ | $\chi^2 = 2.673$ | 2 | 0.2630 | Cramér's $V$ | 0.2111 | Non-significant categorical association. |
| **Sex of Head** *(n=59)* | Pearson $\chi^2$ / Fisher | $\chi^2 = 0.463$ | 1 | 0.5750 | Cramér's $V$ | 0.0886 | Non-significant gender association. |
| **Fertilizer / Manure Use**| Pearson $\chi^2$ / Fisher | $\chi^2 = 0.226$ | 1 | 0.6350 | Cramér's $V$ | 0.0613 | High adoption baseline ($80.0\%$). |
| **Cooperative Membership**| Pearson $\chi^2$ | $\chi^2 = 0.096$ | 1 | 0.7570 | Cramér's $V$ | 0.0400 | High membership baseline ($81.7\%$). |
| **Improved Varieties** | Fisher's Exact Test | — | 1 | 1.0000 | Cramér's $V$ | 0.0977 | Severe sparsity ($n=2$ adopters). |
| **Household Size** | Mann–Whitney U | $U = 536.00$ | — | < 0.001\* | Rank-biserial $r_{rb}$ | +0.7545 | Excluded from regression (welfare divisor). |

*\* Statistically significant at the 5% nominal level ($p < 0.05$).*

---

### Table 4.8: Final Firth Penalized Logistic Regression Model of Factors Associated with Poverty Status
| Covariate in Model | Coefficient ($\beta$) | Robust SE | Wald $z$ | $p$-value | Odds Ratio (OR) | Wald-Type $95\%$ CI | Profile Penalized-Likelihood $95\%$ CI |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Intercept ($\beta_0$)** | $+0.1981$ | 1.4727 | +0.134 | 0.8930 | 1.2191 | $[0.0680, 21.8562]$ | $[0.0725, 33.3121]$ |
| **Total Farm Size (ha)** | $-0.2983$ | 0.7315 | -0.408 | 0.6835 | **0.7421** | $[0.1769, 3.1126]$ | $[0.1383, 2.9557]$ |
| **Access to Credit ($1=\text{Yes}$)**| $-2.2078$ | 1.0673 | -2.069 | **0.0386\***| **0.1099** | $[0.0136, 0.8905]$ | **$[0.0087, 0.7014]$** |

#### Model Fit and Diagnostic Summary
- **Sample Size ($N$):** 60 households | **Poverty Events ($q$):** 13 households | **Events-per-Variable (EPV):** 6.5
- **Penalized Log-Likelihood:** $-24.2882$ (Null Model Penalized Log-Likelihood: $-31.4053$)
- **Model Penalized Likelihood Ratio $\chi^2$ (df = 2):** **14.2342 ($p = 0.000811$)**
- **Nagelkerke Pseudo $R^2$:** **0.3253 (32.53%)**
- **Akaike Information Criterion (Penalized AIC):** **54.576** | **Bayesian Information Criterion (Penalized BIC):** **60.860**
- **Estimation Algorithm:** Firth (1993) bias-reduced penalized maximum likelihood; converged in 5 iterations.
- **Multicollinearity Diagnostic:** $\text{VIF} = 1.5856$, Tolerance = $0.6307$ (Pearson $r = 0.6077$).

*Interpretation:* Holding total farm size constant, access to agricultural credit was significantly associated with **$89.01\%$ lower estimated odds of poverty** ($\text{OR} = 0.1099$, Wald $95\%\text{ CI: } [0.0136, 0.8905]$, Profile $95\%\text{ CI: } [0.0087, 0.7014]$, $p = 0.0386$). Total farm size exhibited an inverse estimated association with poverty odds, but was not statistically significant after adjustment for credit access ($\text{OR} = 0.7421, p = 0.6835$).

---

### Table 4.9: Methodological Sensitivity Comparison — Ordinary MLE vs Firth Penalized Logistic Regression
| Model Parameter / Metric | Firth Penalized Logistic (Primary Model) | Ordinary MLE Logistic (Sensitivity Model) | Comparison & Methodological Notes |
| :--- | :---: | :---: | :--- |
| **Intercept ($\beta_0$)** | $+0.1981$ ($p = 0.8930$) | $+0.4331$ ($p = 0.7904$) | Directionally consistent; minor baseline calibration difference. |
| **Total Farm Size ($\beta_1$)** | $-0.2983$ ($p = 0.6835$) | $-0.4301$ ($p = 0.5979$) | Consistent negative sign; non-significant in both models. |
| **Total Farm Size OR** | **0.7421** ($95\%$ CI: $0.1769–3.1126$) | **0.6505** ($95\%$ CI: $0.1316–3.2144$) | Concordant magnitude. |
| **Access to Credit ($\beta_2$)** | $-2.2078$ ($p = 0.0386$) | $-2.5981$ ($p = 0.0369$) | Both models confirm significant inverse parameter ($p < 0.05$). |
| **Access to Credit OR** | **0.1099** ($95\%$ CI: $0.0136–0.8905$) | **0.0744** ($95\%$ CI: $0.0064–0.8596$) | Firth eliminates small-sample upward odds reduction bias. |
| **Model Fit Statistic** | $\text{Penalized LR } \chi^2 = 14.234$ ($p = 0.0008$) | $\text{LR } \chi^2 = 13.861$ ($p = 0.00098$) | Highly significant global fit in both frameworks. |
| **Nagelkerke Pseudo $R^2$** | **0.3253 (32.53%)** | **0.3181 (31.81%)** | Explains approximately $32\%$ of generalized model variation. |
| **Convergence Status** | Converged smoothly (5 iterations) | Converged (6 iterations) | Both algorithms converge; Firth provides superior small-sample stability. |

---

### Table 4.10: Severity and Ranking of Challenges Faced by Yam Farmers in Akpabuyo LGA
| Rank | Challenge Constraint Item | Valid $n$ | Score 1 $n(\%)$ | Score 2 $n(\%)$ | Score 3 $n(\%)$ | Score 4 $n(\%)$ | Score 5 $n(\%)$ | Mean Severity Index (MSI) | Standard Deviation (SD) | Median (IQR) | Severity Category |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **High cost and scarcity of farm labour** | 60 | 0 (0.0%) | 1 (1.7%) | 12 (20.0%) | 24 (40.0%) | 23 (38.3%) | **4.1500** | 0.7988 | 4.00 (1.00) | **Severe Challenge** |
| **2** | **High cost of farm inputs** | 60 | 0 (0.0%) | 4 (6.7%) | 15 (25.0%) | 18 (30.0%) | 23 (38.3%) | **4.0000** | 0.9567 | 4.00 (2.00) | **Severe Challenge** |
| **3** | **Post-harvest losses and poor storage** | 60 | 0 (0.0%) | 6 (10.0%) | 15 (25.0%) | 19 (31.7%) | 20 (33.3%) | **3.8833** | 0.9931 | 4.00 (2.00) | **Severe Challenge** |
| **4** | **Unpredictable rainfall / climate conditions**| 60 | 0 (0.0%) | 5 (8.3%) | 18 (30.0%) | 27 (45.0%) | 10 (16.7%) | **3.7000** | 0.8497 | 4.00 (1.00) | **Severe Challenge** |
| **5** | **High cost / scarcity of yam stakes** | 60 | 0 (0.0%) | 7 (11.7%) | 21 (35.0%) | 23 (38.3%) | 9 (15.0%) | **3.5667** | 0.8900 | 4.00 (1.00) | **Severe Challenge** |
| **6** | **Inadequate access to credit** | 60 | 0 (0.0%) | 8 (13.3%) | 25 (41.7%) | 14 (23.3%) | 13 (21.7%) | **3.5333** | 0.9823 | 3.00 (1.00) | **Severe Challenge** |
| **7** | **Inadequate extension services** | 60 | 2 (3.3%) | 8 (13.3%) | 19 (31.7%) | 19 (31.7%) | 12 (20.0%) | **3.5167** | 1.0655 | 4.00 (1.00) | **Severe Challenge** |
| **8** | **Pest and disease infestation** | 60 | 0 (0.0%) | 8 (13.3%) | 26 (43.3%) | 21 (35.0%) | 5 (8.3%) | **3.3833** | 0.8253 | 3.00 (1.00) | **Moderate Challenge** |
| **9** | **Low and unstable prices of yam** | 59 | 1 (1.7%) | 12 (20.3%) | 29 (49.2%) | 13 (22.0%) | 4 (6.8%) | **3.1186** | 0.8727 | 3.00 (1.00) | **Moderate Challenge** |
| **10** | **Poor access to markets** | 60 | 4 (6.7%) | 20 (33.3%) | 16 (26.7%) | 18 (30.0%) | 2 (3.3%) | **2.9000** | 1.0201 | 3.00 (2.00) | **Moderate Challenge** |

*Note: Likert weights: 1 = Not a Challenge, 2 = Minor, 3 = Moderate, 4 = Severe, 5 = Very Severe. Standardized intervals: 1.00–1.80 (Not a Challenge), 1.81–2.60 (Minor), 2.61–3.40 (Moderate), 3.41–4.20 (Severe), 4.21–5.00 (Very Severe). Item 9 evaluated on valid $n=59$ due to one missing response.*

---
**END OF THESIS TABLES DOCUMENT**
""")
print("4/5: THESIS_TABLES_FINAL.md written.")

# ------------------------------------------------------------------------------
# 5. FULL_REANALYSIS_AKPABUYO_FINAL.md
# ------------------------------------------------------------------------------
with open('FULL_REANALYSIS_AKPABUYO_FINAL/FULL_REANALYSIS_AKPABUYO_FINAL.md', 'w', encoding='utf-8') as f:
    f.write("""# Full Independent Re-Analysis and Statistical Audit (Final Examiner-Ready Edition)
## Analysis of Poverty Status of Yam Farmers in Akpabuyo Local Government Area, Cross River State, Nigeria

**Author / Statistical Auditor:** Antigravity AI Data & Statistical Audit System  
**Date of Re-Analysis:** October 2026  
**Primary Dataset:** `raw_data.csv` (MD5: `628f44079ed97d91b232533b3c14e014`, $N = 60$ households, 46 columns)  
**Primary Excel Audit Workbook:** [`FULL_REANALYSIS_AKPABUYO_FINAL.xlsx`](FULL_REANALYSIS_AKPABUYO_FINAL.xlsx)  
**Supporting Documentation:**
- [`DATA_CORRECTIONS_LOG.md`](DATA_CORRECTIONS_LOG.md)
- [`MODEL_SELECTION_JUSTIFICATION.md`](MODEL_SELECTION_JUSTIFICATION.md)
- [`REPRODUCIBILITY_NOTES.md`](REPRODUCIBILITY_NOTES.md)
- [`THESIS_TABLES_FINAL.md`](THESIS_TABLES_FINAL.md)

---

## 1. Study Identification

- **Research Title:** Analysis of Poverty Status of Yam Farmers in Akpabuyo Local Government Area, Cross River State, Nigeria
- **Geographic Location:** Akpabuyo Local Government Area, Cross River State, Southern Agricultural Zone, Nigeria
- **Target Population:** Smallholder yam-farming households
- **Sample Structure:** $N = 60$ farming households surveyed across six farming communities (10 households per community)
- **Unit of Analysis:** Household / Household Head
- **Analytical Stance:** Complete, independent, non-causal forensic statistical re-analysis directly from the raw questionnaire records.

---

## 2. Research Aim and Objectives

### Overall Research Aim
To analyze the poverty status of yam farmers in Akpabuyo Local Government Area, Cross River State, Nigeria, and identify key socioeconomic, institutional, and production constraints associated with household welfare.

### Specific Research Objectives
1. **Objective I:** Determine the poverty status of yam farmers using appropriate poverty measures (Foster–Greer–Thorbecke headcount ratio $P_0$, poverty gap $P_1$, and poverty severity $P_2$).
2. **Objective II:** Analyze the poverty status profile of yam farmers across socioeconomic, farm, and institutional characteristics in the study area.
3. **Objective III:** Analyze factors associated with poverty status among yam farmers in the study area.
4. **Objective IV:** Measure and rank the severity of production, institutional, and marketing challenges faced by yam farmers in the study area.

---

## 3. Data Source and Sample

- **Data File:** `raw_data.csv`
- **Sample Size:** $N = 60$ observations, 0 duplicate records.
- **Sampling Reality & Scope:** Multi-stage sampling procedure across six farming communities in Akpabuyo LGA. Because sampling frame probabilities were not formally quantified, the sample represents the *surveyed yam-farming households across the six communities in Akpabuyo LGA*. Generalization beyond these communities should be treated with appropriate scientific caution.

---

## 4. Data Quality Audit

A comprehensive forensic audit of all 46 raw variables was conducted prior to statistical computation.

| Audit Dimension | Raw Finding | Evaluation & Status | Resolution / Analytical Handling |
| :--- | :--- | :--- | :--- |
| **Sample Completeness** | 60 complete records | **PASSED** | Exactly 60 valid household records analyzed. |
| **Duplicate Cases** | 0 duplicate rows across 46 columns | **PASSED** | 100% distinct interview records. |
| **Missing Data** | 1 missing value on `LOW AND UNSTABLE PRICES OF YAM` (Resp 46) | **DOCUMENTED** | Handled via pairwise valid-case analysis ($n=59$ for Item 8). |
| **Coding Anomaly (`SEX`)** | Respondent 46 recorded as `2.0` | **AUDITED & LOGGED** | Codebook defines `1 = Male`, `0 = Female`. Treated empirically as unverified/missing (valid $n=59$: 36 Male [61.02%], 23 Female [38.98%], 1 Unspecified [1.69%]). Historical assumption ($36$ Male, $24$ Female) noted. |
| **Expenditure Consistency** | 56/60 exact matches ($93.33\%$), 4 discrepancies ($6.67\%$) | **AUDITED** | Addressed through dual-track sensitivity analysis (Reported Total vs Component Sum). |
| **Extreme Value** | Resp 59 reported total = ₦223,500 vs component sum = ₦113,500 | **DOCUMENTED** | Analyzed under both definitions; conclusions remain structurally identical. |
| **Predictor Cell Sparsity** | Improved varieties ($n=2$), Modern tools ($n=6$), Extension among poor ($n=0$) | **CRITICAL** | Ordinary logistic MLE produces complete separation; mandates Firth bias-reduced penalized regression. |
| **Likert Scale Definition** | Questionnaire uses 5 points ($1$ to $5$); thesis text mistakenly cited 4 points | **CORRECTED** | Audited and harmonized to authoritative 5-point scale across all sections. |

---

## 5. Questionnaire–Dataset–Thesis Alignment Audit

| Variable / Item | Questionnaire Instrument | Raw Dataset Column | Measurement Scale | Previous Thesis Treatment | Re-Analysis Audited Treatment | Status & Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Sex** | Q1: Male / Female | `SEX` | Binary ($1/0$) | $60\%$ Male, $40\%$ Female | Empirical $n=59$: $61.0\%$ Male, $39.0\%$ Female | **Audited** |
| **Age** | Q2: Continuous (Years) | `AGE` | Ratio (Years) | Continuous & Categorized | Mean: $46.03 \pm 8.64$ yrs | **Verified** |
| **Marital Status** | Q3: Single/Married/Divorced/Widowed | `MARITAL STATUS` | Nominal | Single ($5$), Married ($49$), Widowed ($6$) | Retained ($49$ Married, $81.7\%$) | **Verified** |
| **Education** | Q4: Level of Education | `HIGHEST LEVEL OF EDUCATION` | Ordinal/Years | Primary ($18$), Secondary ($27$), Tertiary ($15$) | Mean: $11.20 \pm 3.79$ yrs | **Verified** |
| **Household Size** | Q5: Persons eating together | `HOUSE HOLD SIZE` | Ratio (Persons) | Mean: $6.23 \pm 1.84$ persons | Welfare divisor; excluded from primary regression | **Audited** |
| **Farming Experience** | Q6: Years of yam farming | `YEARS OF FARMING EXPERIENCE` | Ratio (Years) | Mean: $18.88 \pm 8.56$ yrs | Mean: $18.88$ yrs, Median: $17.5$ yrs | **Verified** |
| **Off-Farm Income** | Q7: Yes / No | `OTHER SOURCE OF INCOME` | Binary ($1/0$) | $81.7\%$ Yes, $18.3\%$ No | $1=\text{Yes}$ ($49$), $0=\text{No}$ ($11$) | **Verified** |
| **Education Exp.** | Q9: Education Expenditure | `AVERAGE MONTHLY HOUSEHOLD EXPENDITURE` | Ratio (₦) | Column mislabeled in CSV header | Verified as Education Expenditure | **Audited** |
| **Farm Size** | Q14: Total farm size | `WHAT IS YOUR TOTAL FARM SIZE` | Ratio (Hectares) | Mean: $2.43 \pm 0.79$ ha | Primary model predictor | **Verified** |
| **Yam Area** | Q15: Yam farm size | `HOW MANY HECTARES ARE USED...` | Ratio (Hectares) | Mean: $1.67 \pm 0.53$ ha | Bivariate comparison | **Verified** |
| **Credit Access** | Q16: Yes / No | `ACCESS TO CREDIT FOR YAM FARMING...` | Binary ($1/0$) | $50.0\%$ Yes, $50.0\%$ No | Primary model predictor | **Verified** |
| **Challenges Scale** | Section D: 5-point Likert ($1$ to $5$) | `HIGH COST OF FARM INPUTS` etc. | 5-Point Ordinal | Incorrectly cited as 4-point scale | Corrected to 5-point MSI ($1.00–5.00$) | **Corrected** |

---

## 6. Objective I: Poverty Measurement

### 6.1 Household Expenditure Aggregate
Household welfare is measured using total monthly consumption expenditure, encompassing five standard expenditure components: food, education, medical care, housing/utilities, and transportation/other. Across the full sample ($N = 60$), mean reported monthly household expenditure was **₦115,837.50** ($\pm ₦27,652.42$), with a median of **₦111,000.00** (range: ₦65,000.00–₦223,500.00).

### 6.2 Per Capita Household Expenditure (PCHE)
$$\text{PCHE}_i = \frac{\text{Total Monthly Household Expenditure}_i}{\text{Household Size}_i}$$
- **Mean PCHE:** **₦20,289.03** ($\pm ₦7,585.87$)
- **Median PCHE:** **₦18,883.33**
- **Interquartile Range (IQR):** **₦8,708.33** (₦15,000.00–₦23,708.33)
- **Range:** **₦10,000.00 – ₦47,500.00**

### 6.3 Relative Poverty Line Determination
Following smallholder agricultural economics standards (World Bank, 2001; NBS, 2022), a relative expenditure poverty threshold ($z$) was determined as two-thirds ($2/3$) of the mean Per Capita Household Expenditure:
$$z = \frac{2}{3} \times \overline{\text{PCHE}} = \frac{2}{3} \times ₦20,289.03 = \mathbf{₦13,526.02 \text{ per person per month}}$$

### 6.4 Poverty Classification
- **Poor Households ($\text{PCHE} < ₦13,526.02$):** **13 (21.67%)**
- **Non-Poor Households ($\text{PCHE} \ge ₦13,526.02$):** **47 (78.33%)**
- **Total Sample ($N$):** **60 (100.00%)**

### 6.5 Foster–Greer–Thorbecke (FGT) Poverty Indices
$$P_\alpha = \frac{1}{N} \sum_{i=1}^q \left( \frac{z - y_i}{z} \right)^\alpha$$

| FGT Index | Formula | Empirical Value | Percentage | Economic Interpretation |
| :--- | :--- | :---: | :---: | :--- |
| **Headcount Ratio ($P_0$)** | $P_0 = \frac{q}{N}$ | **0.2167** | **21.67%** | $21.67\%$ of yam farming households live below the relative poverty threshold. |
| **Poverty Gap Index ($P_1$)** | $P_1 = \frac{1}{N} \sum_{i=1}^q \left( \frac{z - y_i}{z} \right)$ | **0.0232** | **2.32%** | The population poverty deficit equals $2.32\%$ of the poverty line. |
| **Poverty Severity Index ($P_2$)**| $P_2 = \frac{1}{N} \sum_{i=1}^q \left( \frac{z - y_i}{z} \right)^2$ | **0.0034** | **0.34%** | Measures poverty severity through squared normalized gaps; reflects low extreme deprivation. |

#### Monetary Deficit and Poverty Gap Metrics
- **Mean PCHE of the Poor ($\overline{y}_p$):** **₦12,079.49** ($\pm ₦1,241.13$)
- **Average Monthly Poverty Gap per Poor Person ($z - \overline{y}_p$):** **₦1,446.53**
- **Income Gap Ratio ($I = \frac{z - \overline{y}_p}{z}$):** **0.1069 (10.69%)**
- **Total Monthly Sample Poverty Gap:** **₦156,220.00**

### 6.6 Expenditure Sensitivity Analysis
| Welfare Metric | Reported Total Approach (Primary) | Component Sum Approach (Sensitivity) | Absolute Difference | Relative Change |
| :--- | :--- | :--- | :--- | :--- |
| **Mean Household Expenditure** | ₦115,837.50 | ₦113,985.83 | ₦1,851.67 | $1.62\%$ |
| **Mean PCHE** | ₦20,289.03 | ₦20,022.82 | ₦266.21 | $1.31\%$ |
| **Poverty Line ($z$)** | ₦13,526.02 | ₦13,348.55 | ₦177.47 | $1.31\%$ |
| **Poor Households ($q$)** | **13 (21.67%)** | **12 (20.00%)** | 1 household | $-1.67\%$ points |
| **Non-Poor Households** | **47 (78.33%)** | **48 (80.00%)** | 1 household | $+1.67\%$ points |
| **Headcount Ratio ($P_0$)** | **0.2167** | **0.2000** | 0.0167 | $-7.71\%$ |
| **Poverty Gap ($P_1$)** | **0.0232** | **0.0208** | 0.0024 | $-10.34\%$ |
| **Poverty Severity ($P_2$)** | **0.0034** | **0.0029** | 0.0005 | $-14.71\%$ |
| **Classification Concordance** | **59 / 60 Exact Matches (98.33%)** | | | |
| **Cohen's Kappa ($\kappa$)** | **0.9495 (Near-Perfect Agreement)** | | | |

*Sensitivity Finding:* Poverty classification was highly robust to the expenditure reconciliation alternative examined ($\kappa = 0.9495$).

---

## 7. Descriptive Socioeconomic Analysis

Baseline descriptive statistics for the sample ($N = 60$) are provided in [Table 4.1](file:///{os.path.abspath('FULL_REANALYSIS_AKPABUYO_FINAL/THESIS_TABLES_FINAL.md').replace(chr(92), '/')}) and [Table 4.2](file:///{os.path.abspath('FULL_REANALYSIS_AKPABUYO_FINAL/THESIS_TABLES_FINAL.md').replace(chr(92), '/')}).

---

## 8. Objective II: Poverty Status Profile

Objective II provides a **descriptive poverty status profile** comparing poor ($n = 13$) and non-poor ($n = 47$) households across demographic, farm, institutional, and welfare characteristics. No causal claims are asserted in this profile.

- **Demographics:** Poor household heads were older (mean $51.31 \pm 8.99$ vs $44.57 \pm 8.04$ years), had larger households (mean $8.31 \pm 1.70$ vs $5.66 \pm 1.43$ persons), and had more farming experience ($25.77 \pm 10.48$ vs $16.98 \pm 6.94$ years).
- **Landholdings:** Poor households operated smaller total farms ($1.98 \pm 0.48$ vs $2.56 \pm 0.82$ ha) and yam areas ($1.43 \pm 0.37$ vs $1.73 \pm 0.56$ ha).
- **Institutional Access:** Credit access was markedly lower among poor households ($7.69\%$ vs $61.70\%$), as was extension contact ($0.00\%$ vs $44.68\%$).
- **Budget Shares:** Food consumed **61.11%** of poor household expenditure vs **50.38%** among non-poor households.

---

## 9. Objective III: Factors Associated with Poverty

### 9.1 Bivariate Analysis
To avoid unwarranted distributional assumptions for the small poor subgroup ($n = 13$), non-parametric **Mann–Whitney U tests** were conducted for continuous variables (supplemented by rank-biserial effect sizes $r_{rb}$), while **Pearson Chi-Square** and **Fisher's Exact tests** were used for categorical variables.

*Methodological Note:* Outcome-derived variables (PCHE, total expenditure, poverty line) were strictly excluded from the predictor set. Household size is recognized as a welfare divisor and omitted from multivariable models.

| Predictor Variable | Test Type Applied | Test Statistic | df | $p$-value | Effect Size Metric | Effect Size Value |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: |
| **Access to Credit** | Fisher's Exact / $\chi^2$ | $\chi^2 = 9.820$ | 1 | **0.0012\*** | Cramér's $V$ | **0.4046** |
| **Extension Contact** | Fisher's Exact Test | $\chi^2 = 8.878$ | 1 | **0.0021\*** | Cramér's $V$ | **0.3847** |
| **Farming Experience** | Mann–Whitney U | $U = 456.00$ | — | **0.0090\*** | Rank-biserial $r_{rb}$ | **+0.4926** |
| **Total Farm Size** | Mann–Whitney U | $U = 170.50$ | — | **0.0160\*** | Rank-biserial $r_{rb}$ | **-0.4419** |
| **Age of Household Head**| Mann–Whitney U | $U = 432.00$ | — | **0.0240\*** | Rank-biserial $r_{rb}$ | **+0.4141** |
| **Total Monthly Income** | Mann–Whitney U | $U = 193.50$ | — | **0.0460\*** | Rank-biserial $r_{rb}$ | **-0.3666** |
| **Yam Cultivated Area** | Mann–Whitney U | $U = 205.00$ | — | 0.0720 | Rank-biserial $r_{rb}$ | -0.3290 |
| **Other Income Source** | Fisher's Exact / $\chi^2$ | $\chi^2 = 1.487$ | 1 | 0.2390 | Cramér's $V$ | 0.1574 |
| **Education Level** | Pearson $\chi^2$ | $\chi^2 = 2.673$ | 2 | 0.2630 | Cramér's $V$ | 0.2111 |
| **Sex of Head** *(n=59)* | Pearson $\chi^2$ / Fisher | $\chi^2 = 0.463$ | 1 | 0.5750 | Cramér's $V$ | 0.0886 |

### 9.2 Sparse-Cell and Multicollinearity Assessment
- **Sparse Predictor Cells:** Improved varieties ($n=2$), modern tools ($n=6$), and extension contact among the poor ($n=0$) exhibit extreme cell sparsity and complete separation.
- **Multicollinearity:** Total Farm Size and Access to Credit have Pearson $r = 0.6077$ ($r^2 = 0.3693$), yielding $\text{VIF} = \mathbf{1.5856}$ and $\text{Tolerance} = \mathbf{0.6307}$. Farm size and yam area have $r = 0.9642$ ($\text{VIF} = 14.2120$), precluding joint estimation.

### 9.3 Multivariable Firth Penalized Logistic Regression
Firth's (1993) bias-reduced penalized maximum likelihood logistic regression is adopted as the primary inferential framework.

#### Multivariable Candidate Models Comparison
| Model Specification | Covariates Included ($k$) | EPV | Penalized Log-Likelihood | Model LR $\chi^2$ (df, $p$) | Penalized AIC | Penalized BIC | Nagelkerke Pseudo $R^2$ | Credit Access OR ($95\%$ Wald CI, $p$) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Model A (Recommended)** | **Farm Size + Credit (2)** | **6.5** | **-24.2882** | **14.234 (2, p=0.0008)** | **54.576** | **60.860** | **0.3253** | **0.1099 [0.0136–0.8905] (p=0.0386)** |
| **Model B** | Farm Size + Credit + Age (3) | 4.3 | -23.7744 | 15.262 (3, p=0.0016) | 55.549 | 63.927 | 0.3452 | 0.1017 [0.0123–0.8415] (p=0.0340) |
| **Model C** | Farm Size + Credit + Extension (3) | 4.3 | -23.4651 | 15.881 (3, p=0.0012) | 54.930 | 63.309 | 0.3570 | 0.1444 [0.0169–1.2334] (p=0.0772) |
| **Model D** | Farm Size + Credit + Other Income (3)| 4.3 | -24.2709 | 14.269 (3, p=0.0026) | 56.542 | 64.920 | 0.3260 | 0.1118 [0.0137–0.9103] (p=0.0407) |

### 9.4 Final Recommended Model (Model A)
**Model A** is selected based on parsimony, optimal information criteria (lowest AIC = $54.576$, lowest BIC = $60.860$), superior EPV ($6.5$), and absence of separation anomalies.

| Covariate in Model | Coefficient ($\beta$) | Robust SE | Wald $z$ | $p$-value | Odds Ratio (OR) | Wald-Type $95\%$ CI | Profile Penalized-Likelihood $95\%$ CI |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Intercept ($\beta_0$)** | $+0.1981$ | 1.4727 | +0.134 | 0.8930 | 1.2191 | $[0.0680, 21.8562]$ | $[0.0725, 33.3121]$ |
| **Total Farm Size (ha)** | $-0.2983$ | 0.7315 | -0.408 | 0.6835 | **0.7421** | $[0.1769, 3.1126]$ | $[0.1383, 2.9557]$ |
| **Access to Credit ($1=\text{Yes}$)**| $-2.2078$ | 1.0673 | -2.069 | **0.0386\***| **0.1099** | $[0.0136, 0.8905]$ | **$[0.0087, 0.7014]$** |

- **Model Penalized LR $\chi^2$ (df = 2):** **14.2342 ($p = 0.000811$)**
- **Nagelkerke Pseudo $R^2$:** **0.3253 (32.53%)**

*Interpretation of Association:* Access to credit was associated with lower estimated odds of poverty in the final Firth logistic regression model ($\text{OR} = 0.1099$, Wald $95\%\text{ CI: } [0.0136, 0.8905]$, Profile $95\%\text{ CI: } [0.0087, 0.7014]$, $p = 0.0386$). An odds ratio of $0.11$ corresponds to approximately **89% lower estimated odds of poverty relative to those without credit**, conditional on the model specification and holding farm size constant. Farm size showed an inverse estimated association with poverty odds, but the association was not statistically significant in the final model ($\text{OR} = 0.7421, 95\%\text{ CI: } [0.1769, 3.1126], p = 0.6835$).

### 9.5 Ordinary Maximum Likelihood Logistic Sensitivity Analysis
Standard Newton-Raphson MLE yields directionally congruent parameters: Credit Access $\beta = -2.5981, \text{OR} = 0.0744, p = 0.0369$; Farm Size $\beta = -0.4301, \text{OR} = 0.6505, p = 0.5979$; Model LR $\chi^2 = 13.861, p = 0.00098$, Nagelkerke pseudo $R^2 = 0.3181$. Firth penalization removes small-sample upward bias while preserving inference.

---

## 10. Objective IV: Farming Challenges

Objective IV was re-calculated using the validated **5-point Likert scale**:
$$\text{Scale: } 1 = \text{Not a Challenge}, \quad 2 = \text{Minor}, \quad 3 = \text{Moderate}, \quad 4 = \text{Severe}, \quad 5 = \text{Very Severe}$$

| Rank | Challenge Constraint Item | Valid $n$ | Score 1 $n(\%)$ | Score 2 $n(\%)$ | Score 3 $n(\%)$ | Score 4 $n(\%)$ | Score 5 $n(\%)$ | Mean Severity Index (MSI) | Standard Deviation (SD) | Median (IQR) | Severity Category |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **High cost and scarcity of farm labour** | 60 | 0 (0.0%) | 1 (1.7%) | 12 (20.0%) | 24 (40.0%) | 23 (38.3%) | **4.1500** | 0.7988 | 4.00 (1.00) | **Severe Challenge** |
| **2** | **High cost of farm inputs** | 60 | 0 (0.0%) | 4 (6.7%) | 15 (25.0%) | 18 (30.0%) | 23 (38.3%) | **4.0000** | 0.9567 | 4.00 (2.00) | **Severe Challenge** |
| **3** | **Post-harvest losses and poor storage** | 60 | 0 (0.0%) | 6 (10.0%) | 15 (25.0%) | 19 (31.7%) | 20 (33.3%) | **3.8833** | 0.9931 | 4.00 (2.00) | **Severe Challenge** |
| **4** | **Unpredictable rainfall / climate conditions**| 60 | 0 (0.0%) | 5 (8.3%) | 18 (30.0%) | 27 (45.0%) | 10 (16.7%) | **3.7000** | 0.8497 | 4.00 (1.00) | **Severe Challenge** |
| **5** | **High cost / scarcity of yam stakes** | 60 | 0 (0.0%) | 7 (11.7%) | 21 (35.0%) | 23 (38.3%) | 9 (15.0%) | **3.5667** | 0.8900 | 4.00 (1.00) | **Severe Challenge** |
| **6** | **Inadequate access to credit** | 60 | 0 (0.0%) | 8 (13.3%) | 25 (41.7%) | 14 (23.3%) | 13 (21.7%) | **3.5333** | 0.9823 | 3.00 (1.00) | **Severe Challenge** |
| **7** | **Inadequate extension services** | 60 | 2 (3.3%) | 8 (13.3%) | 19 (31.7%) | 19 (31.7%) | 12 (20.0%) | **3.5167** | 1.0655 | 4.00 (1.00) | **Severe Challenge** |
| **8** | **Pest and disease infestation** | 60 | 0 (0.0%) | 8 (13.3%) | 26 (43.3%) | 21 (35.0%) | 5 (8.3%) | **3.3833** | 0.8253 | 3.00 (1.00) | **Moderate Challenge** |
| **9** | **Low and unstable prices of yam** | 59 | 1 (1.7%) | 12 (20.3%) | 29 (49.2%) | 13 (22.0%) | 4 (6.8%) | **3.1186** | 0.8727 | 3.00 (1.00) | **Moderate Challenge** |
| **10** | **Poor access to markets** | 60 | 4 (6.7%) | 20 (33.3%) | 16 (26.7%) | 18 (30.0%) | 2 (3.3%) | **2.9000** | 1.0201 | 3.00 (2.00) | **Moderate Challenge** |

---

## 11. Hypothesis Audit

| Research Hypothesis | Current Thesis Phrasing | Statistical Test Evaluated | Re-Analysis Test Result | Audited Decision | Recommendation for Thesis |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **$H_{01}$ (Objective I/III)** | Socioeconomic and farm characteristics do not significantly influence poverty status of yam farmers. | Multivariable Firth Model Likelihood Ratio Test & Wald Tests | $\text{Model LR } \chi^2(2) = 14.234, p = 0.0008$; Credit access Wald $z = -2.069, p = 0.0386$. | **Reject Null Hypothesis ($H_{01}$)** | Retain rejection of null hypothesis. Frame conclusion as: *Socioeconomic and institutional factors (specifically credit access) are significantly associated with poverty status ($p < 0.05$).* |
| **$H_{02}$ (Objective IV)** | Production and institutional challenges do not significantly constrain yam production. | Descriptive Severity Benchmark Test vs 3.0 | 7 of 10 constraints exceed $3.40$ (Severe), with Labour ($4.15$) and Inputs ($4.00$) at peak severity. | **Reject Null Hypothesis ($H_{02}$)** | Descriptive ranking via MSI provides full empirical support for Objective IV. Note that raw dataset does not contain physical output volume (kg/ha) to estimate an econometric production constraint frontier. |

---

## 12. Bias and Validity Assessment

1. **Sampling Bias & Generalizability:** The sample represents the surveyed farming communities in Akpabuyo LGA. Generalization beyond these communities should be treated with caution.
2. **Measurement Error:** Recall-based expenditure yielded 4 minor discrepancies ($6.67\%$). Sensitivity analysis demonstrated $\kappa = 0.9495$, confirming measurement invariance.
3. **Classification Endogeneity:** Poverty line is sample-relative ($2/3\text{ Mean PCHE}$). Dual-track sensitivity confirms that $21.67\%$ primary vs $20.00\%$ sensitivity headcount rates share $98.33\%$ concordance.
4. **Sparse-Data Bias:** Resolved via Firth penalized likelihood estimation.
5. **Cross-Sectional Inference:** Cross-sectional design precludes establishing temporal causality. All causal language is replaced with precise associative terminology.

---

## 13. Statistical Limitations

1. **Cross-Sectional Observational Design:** Precludes establishing temporal ordering or direct causal mechanics.
2. **Small Subgroup Sample Size:** $N = 60$ with $q = 13$ poor households limits multivariable degrees of freedom, restricting regression models to $2-3$ parsimonious predictors ($6.5$ EPV).
3. **Sparse Predictor Cells:** Complete absence of poor households among extension recipients ($0/21$) and technology adopters ($0/6$) prevents simultaneous multivariable estimation of all institutional variables.
4. **Mechanical Endogeneity of Household Size:** Household size cannot be modeled as an independent predictor of per-capita poverty status without mathematical circularity.

---

## 14. Comparison with Previous Analysis

A complete line-by-line audit comparing the previous thesis figures against this independent re-analysis was conducted:

| Analytical Parameter | Previous Thesis Result | New Re-Analysis Result | Mathematical Difference | Diagnostic Reason | Final Recommended Figure |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sample Size ($N$)** | 60 | 60 | 0 | Identical dataset | **60 Households** |
| **Mean Household Exp.** | ₦115,837.50 | ₦115,837.50 | ₦0.00 | Exact match on reported total | **₦115,837.50** |
| **Mean PCHE** | ₦20,289.03 | ₦20,289.03 | ₦0.00 | Exact calculation | **₦20,289.03** |
| **Poverty Line ($z$)** | ₦13,526.02 | ₦13,526.02 | ₦0.00 | $2/3 \times ₦20,289.03$ | **₦13,526.02** |
| **Poor Households ($q$)** | 13 ($21.67\%$) | 13 ($21.67\%$) | 0 | Exact classification | **13 (21.67%)** |
| **Non-Poor Households** | 47 ($78.33\%$) | 47 ($78.33\%$) | 0 | Exact classification | **47 (78.33%)** |
| **Headcount Ratio ($P_0$)** | 0.2167 | 0.2167 | 0.0000 | Direct FGT calculation | **0.2167 (21.67%)** |
| **Poverty Gap ($P_1$)** | 0.0232 | 0.0232 | 0.0000 | Direct FGT calculation | **0.0232 (2.32%)** |
| **Poverty Severity ($P_2$)**| 0.0034 | 0.0034 | 0.0000 | Direct FGT calculation | **0.0034 (0.34%)** |
| **Farm Size Bivariate** | $U = 170.50, p = 0.016$ | $U = 170.50, p = 0.016$ | 0.000 | Exact Mann-Whitney U | **$U = 170.50, p = 0.016$** |
| **Credit Access $\chi^2$** | $\chi^2 = 9.820, p = 0.002$| $\chi^2 = 9.820, p = 0.002$| 0.000 | Exact Chi-Square | **$\chi^2 = 9.820, p = 0.002$** |
| **Credit Access Fisher** | $p = 0.001$ | $p = 0.0012$ | 0.0002 | Exact Fisher 2-sided | **Fisher $p = 0.0012$** |
| **Extension Contact** | Fisher $p = 0.002$ | Fisher $p = 0.0021$ | 0.0001 | Exact Fisher 2-sided | **Fisher $p = 0.0021$** |
| **Firth Model Credit OR** | 0.1100 ($p = 0.0390$) | 0.1099 ($p = 0.0386$) | 0.0001 | Minor convergence precision | **OR = 0.1099, p = 0.0386** |
| **Firth Farm Size OR** | 0.7421 ($p = 0.6835$) | 0.7421 ($p = 0.6835$) | 0.0000 | Exact parameter match | **OR = 0.7421, p = 0.6835** |
| **Firth Model LR $\chi^2$** | 14.234 ($p = 0.0008$) | 14.234 ($p = 0.00081$) | 0.000 | Penalized likelihood ratio | **LR $\chi^2 = 14.234, p = 0.0008$** |
| **Labour Challenge MSI** | 4.15 | 4.1500 (Rank 1) | 0.000 | Authoritative 5-point MSI | **4.1500 (Rank 1)** |
| **Inputs Challenge MSI** | 4.00 | 4.0000 (Rank 2) | 0.000 | Authoritative 5-point MSI | **4.0000 (Rank 2)** |
| **Storage Challenge MSI**| 3.88 | 3.8833 (Rank 3) | 0.000 | Authoritative 5-point MSI | **3.8833 (Rank 3)** |
| **Climate Challenge MSI**| 3.70 | 3.7000 (Rank 4) | 0.000 | Authoritative 5-point MSI | **3.7000 (Rank 4)** |
| **Stakes Challenge MSI** | 3.57 | 3.5667 (Rank 5) | 0.000 | Authoritative 5-point MSI | **3.5667 (Rank 5)** |
| **Credit Challenge MSI** | 3.53 | 3.5333 (Rank 6) | 0.000 | Authoritative 5-point MSI | **3.5333 (Rank 6)** |
| **Extension Challenge** | 3.52 | 3.5167 (Rank 7) | 0.000 | Authoritative 5-point MSI | **3.5167 (Rank 7)** |
| **Pests Challenge MSI** | 3.38 | 3.3833 (Rank 8) | 0.000 | Authoritative 5-point MSI | **3.3833 (Rank 8)** |
| **Prices Challenge MSI** | 3.12 | 3.1186 (Rank 9) | 0.000 | Authoritative 5-point MSI | **3.1186 (Rank 9)** |
| **Market Challenge MSI** | 2.90 | 2.9000 (Rank 10) | 0.000 | Authoritative 5-point MSI | **2.9000 (Rank 10)** |

---

## 15. What Must Change in the Thesis

1. **Likert Scale Specification in Chapter 3:** Correct textual description from a 4-point scale to the authoritative **5-point Likert scale** ($1 = \text{Not a Challenge}$ to $5 = \text{Very Severe}$) with standardized intervals ($1.00–1.80, 1.81–2.60, 2.61–3.40, 3.41–4.20, 4.21–5.00$).
2. **Causal Phrasing:** Replace causal statements (e.g. "credit reduced poverty by $92.56\%$") with non-causal associative phrasing (*"access to credit was significantly associated with $89.01\%$ lower odds of poverty, holding farm size constant"*).
3. **Poverty Severity Clarification:** Define $P_2$ ($0.0034$) strictly as *poverty severity (squared normalized poverty gap)* rather than "inequality among the poor".
4. **Generalization Scope:** Frame conclusions as representing the *surveyed smallholder farming households across the six communities in Akpabuyo LGA*.
5. **Multicollinearity Correction:** Correct the VIF report to $\text{VIF} = 1.5856$ ($r = 0.6077$).

---

## 16. Final Recommended Analytical Framework

```
                             RAW DATASET (N = 60)
                                      ↓
                     FORENSIC QUALITY & INTEGRITY AUDIT
                       (Coding, Sparsity, Missingness)
                                      ↓
                     HOUSEHOLD EXPENDITURE RECONCILIATION
                  (Reported Total: ₦115,837.50 vs Sum: ₦113,985.83)
                                      ↓
                     OBJECTIVE I: POVERTY MEASUREMENT
                   Mean PCHE = ₦20,289.03 | z = ₦13,526.02
                  P0 = 0.2167 (21.67%) | P1 = 0.0232 | P2 = 0.0034
                                      ↓
                     OBJECTIVE II: DESCRIPTIVE POVERTY PROFILE
                   (Poor n=13 vs Non-Poor n=47 Cross-Tabulations)
                                      ↓
                     OBJECTIVE III: INFERENTIAL MODELLING
                  Bivariate Tests: Mann-Whitney U & Fisher's Exact
                  Multivariable: Firth Penalized Logistic Regression
                      Poverty ~ Farm Size (ha) + Credit Access
                  (Credit OR = 0.1099, p = 0.0386 | LR Chi2 = 14.234)
                                      ↓
                     OBJECTIVE IV: PRODUCTION CHALLENGES
                  Validated 5-Point Mean Severity Index (MSI)
                  (Labour: 4.15 | Inputs: 4.00 | Storage: 3.88)
```

---

## 17. FINAL VERIFIED SUMMARY & ACTIONABLE AUDIT

### A. FINAL VERIFIED RESULTS
- **Sample Size ($N$):** Exactly 60 yam-farming households.
- **Welfare Aggregates:** Mean Monthly Expenditure = ₦115,837.50; Mean PCHE = ₦20,289.03; Relative Poverty Line ($z$) = ₦13,526.02.
- **Poverty Headcount:** 13 Poor households ($21.67\%$), 47 Non-Poor households ($78.33\%$).
- **FGT Indices:** $P_0 = 0.2167$ ($21.67\%$), $P_1 = 0.0232$ ($2.32\%$), $P_2 = 0.0034$ ($0.34\%$).
- **Monthly Poverty Deficit:** Average deficit among the poor is ₦1,446.53 per capita per month.

### B. FINAL MODEL
- **Specification:** Firth Penalized Logistic Regression: $\operatorname{logit}(\text{Poverty}) = \beta_0 + \beta_1 (\text{Total Farm Size}) + \beta_2 (\text{Credit Access})$.
- **Parameter Estimates:**
  - Access to Credit ($1=\text{Yes}$): $\beta = -2.2078, \text{SE} = 1.0673, \text{Wald } z = -2.069, p = 0.0386, \text{OR} = \mathbf{0.1099}$ (Wald $95\%\text{ CI: } [0.0136, 0.8905]$, Profile $95\%\text{ CI: } [0.0087, 0.7014]$).
  - Total Farm Size (ha): $\beta = -0.2983, \text{SE} = 0.7315, \text{Wald } z = -0.408, p = 0.6835, \text{OR} = \mathbf{0.7421}$ (Wald $95\%\text{ CI: } [0.1769, 3.1126]$, Profile $95\%\text{ CI: } [0.1383, 2.9557]$).
- **Model Fit:** Penalized $\text{LR } \chi^2(2) = 14.2342$ ($p = 0.000811$), Nagelkerke pseudo $R^2 = 0.3253$.

### C. FINAL POVERTY RESULTS
- Poverty incidence in the study area is $21.67\%$.
- Depth of poverty is low ($2.32\%$ overall poverty gap ratio).
- Poverty severity is low ($0.0034$), indicating that consumption deprivation among the poor is relatively uniform and clustered close to the threshold.

### D. FINAL CHALLENGE RESULTS
- 7 out of 10 challenges are **Severe** ($\text{MSI} \ge 3.41$), led by Labour Cost ($4.15$), Input Cost ($4.00$), and Storage Losses ($3.88$).
- Marketing and pricing constraints are rated as **Moderate** ($\text{MSI} = 2.90–3.12$).

### E. KEY LIMITATIONS
- Small sample size ($N = 60$) with 13 poverty events.
- Cross-sectional design prevents causal claims.
- Sparse predictor cells necessitate penalized regression.
- Sampling represents surveyed farming communities in Akpabuyo LGA.

### F. DATA CORRECTIONS
- Corrected Likert challenge scale from 4 points to 5 points.
- Documented 4 expenditure discrepancies ($93.33\%$ concordance, $\kappa = 0.9495$).
- Corrected VIF to $1.5856$ ($r = 0.6077$).
- Addressed Respondent 46 sex anomaly empirically ($n=59$).

### G. REMAINING ISSUES REQUIRING HUMAN VERIFICATION
- **REQUIRES HUMAN VERIFICATION:** Confirm whether Respondent 46 was intended as Female on the physical paper questionnaire or whether it was a keypunch error for Female ($0$). If confirmed on the physical survey form, document this confirmation in the final thesis appendix.
- **REQUIRES HUMAN VERIFICATION:** Confirm whether the academic department requires retaining a formal hypothesis for Objective IV (production constraints) or whether Objective IV is accepted as a descriptive Mean Severity Index ranking.

---
**END OF MASTER INDEPENDENT RE-ANALYSIS AND STATISTICAL AUDIT REPORT**
""")
print("5/5: FULL_REANALYSIS_AKPABUYO_FINAL.md written.")

print("\nALL 5 MARKDOWN DOCUMENTATION FILES SUCCESSFULLY GENERATED.")
