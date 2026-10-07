# Data Corrections and Audit Log
## Study: Analysis of Poverty Status of Yam Farmers in Akpabuyo LGA, Nigeria
**Primary Source:** `raw_data.csv` ($N = 60$ households, 46 columns, MD5: `628f44079ed97d91b232533b3c14e014`)  
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
- **Component Means and Arithmetic Reconciliation:**
  - Food Expenditure Mean: **₦60,703.33** (Sum = ₦3,642,200.00)
  - Education Expenditure Mean: **₦14,528.33** (Sum = ₦871,700.00)
  - Health/Medical Expenditure Mean: **₦8,631.67** (Sum = ₦517,900.00)
  - Housing/Utilities Expenditure Mean: **₦18,246.67** (Sum = ₦1,094,800.00)
  - Transportation/Other Expenditure Mean: **₦11,875.83** (Sum = ₦712,550.00)
  - **Arithmetic Sum of Component Means:** **₦113,985.83**
  - **Mean of Row-Level Component Sums:** **₦113,985.83** (Total sum = ₦6,839,150.00 / 60)
  - *Note on Prior Intermediate Text:* An earlier draft cited ₦113,975.00 due to an intermediate rounding artifact ($₦115,837.50 - ₦1,865 = ₦113,972.50 \approx ₦113,975.00$). The exact audited value from the raw data is **₦113,985.83**.
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
- **Correction:** Inspection of the research instrument and raw response values ($1, 2, 3, 4, 5$) confirms an authoritative **5-point Likert scale**:
  - $1 = \text{Not a Challenge}$
  - $2 = \text{Minor Challenge}$
  - $3 = \text{Moderate Challenge}$
  - $4 = \text{Severe Challenge}$
  - $5 = \text{Very Severe Challenge}$
- **Validated Severity Intervals:**
  - $1.00–1.80 = \text{Not a Challenge}$
  - $1.81–2.60 = \text{Minor Challenge}$
  - $2.61–3.40 = \text{Moderate Challenge}$
  - $3.41–4.20 = \text{Severe Challenge}$
  - $4.21–5.00 = \text{Very Severe Challenge}$
- **Classifications under Validated Scale:**
  - Labour Cost (4.15) $\rightarrow$ **Severe** ($3.41 \le 4.15 \le 4.20$)
  - Input Cost (4.00) $\rightarrow$ **Severe** ($3.41 \le 4.00 \le 4.20$)
  - Storage Losses (3.88) $\rightarrow$ **Severe** ($3.41 \le 3.88 \le 4.20$)
  - Climate/Rainfall (3.70) $\rightarrow$ **Severe** ($3.41 \le 3.70 \le 4.20$)
  - Yam Stakes (3.57) $\rightarrow$ **Severe** ($3.41 \le 3.57 \le 4.20$)
  - Credit Access (3.53) $\rightarrow$ **Severe** ($3.41 \le 3.53 \le 4.20$)
  - Extension Services (3.52) $\rightarrow$ **Severe** ($3.41 \le 3.52 \le 4.20$)
  - Pest and Disease (3.38) $\rightarrow$ **Moderate** ($2.61 \le 3.38 \le 3.40$)
  - Yam Prices (3.12) $\rightarrow$ **Moderate** ($2.61 \le 3.12 \le 3.40$)
  - Market Access (2.90) $\rightarrow$ **Moderate** ($2.61 \le 2.90 \le 3.40$) *(Note: 2.90 falls strictly in the Moderate range $2.61–3.40$, not Minor).*

#### 5. Multicollinearity & VIF Correction
- **Finding:** Previous draft texts reported an impossible combination of $r = 0.6077$ and $\text{VIF} = 1.004$ between Farm Size and Credit Access, erroneously claiming orthogonality.
- **Correction:** Re-computation directly from the predictor matrix establishes:
  - Pearson correlation $r = 0.6077$, Spearman rank correlation $r_s = 0.6561$.
  - $r^2 = 0.3693 \implies \text{VIF} = \frac{1}{1 - 0.3693} = \mathbf{1.5856}$, Tolerance = $\mathbf{0.6307}$.
  - This confirms moderate, non-harmful collinearity well below standard thresholds ($\text{VIF} < 5.0$).
  - Farm Size and Yam Cultivated Area share extreme collinearity ($r = 0.9642, \text{VIF} = 14.2120$), confirming that Yam Area must not be included simultaneously in multivariable models.

---
**END OF DATA CORRECTIONS LOG**
