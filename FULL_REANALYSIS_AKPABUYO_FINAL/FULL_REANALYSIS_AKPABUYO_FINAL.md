# Full Independent Re-Analysis and Statistical Audit (Final Examiner-Ready Edition)
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
- [`FINAL_QC_REPORT.md`](FINAL_QC_REPORT.md)

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
The poverty headcount ratio was 21.67%, indicating that 13 of the 60 sampled yam-farming households were classified as poor under the study's relative poverty threshold.
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
Baseline descriptive statistics for the sample ($N = 60$) are provided in [Table 4.1](THESIS_TABLES_FINAL.md) and [Table 4.2](THESIS_TABLES_FINAL.md).

---

## 8. Objective II: Poverty Status Profile

Objective II provides a **descriptive poverty status profile** comparing poor ($n = 13$) and non-poor ($n = 47$) households across demographic, farm, institutional, and welfare characteristics. No causal claims are asserted in this profile.

- **Demographics:** Poor household heads were older (mean $51.31 \pm 8.99$ vs $44.57 \pm 8.04$ years), had more farming experience ($25.77 \pm 10.48$ vs $16.98 \pm 6.94$ years), and household size showed the largest observed difference between poor and non-poor households (mean $8.31 \pm 1.70$ vs $5.66 \pm 1.43$ persons).
- **Landholdings:** Poor households operated smaller total farms ($1.98 \pm 0.48$ vs $2.56 \pm 0.82$ ha) and yam areas ($1.43 \pm 0.37$ vs $1.73 \pm 0.56$ ha).
- **Institutional Access:** Credit access was markedly lower among poor households ($7.69\%$ vs $61.70\%$), as was extension contact ($0.00\%$ vs $44.68\%$).
- **Budget Shares:** Food consumed **61.11%** of poor household expenditure vs **50.38%** among non-poor households.

> **Methodological Caution on Household Size:**  
> Household size should be interpreted cautiously because it forms the denominator of the per-capita household expenditure measure used to classify poverty. Therefore, its observed association with poverty status does not by itself establish an independent causal effect.

---

## 9. Objective III: Factors Associated with Poverty

### 9.1 Bivariate Analysis
To avoid unwarranted distributional assumptions for the small poor subgroup ($n = 13$), non-parametric **Mann–Whitney U tests** were conducted for continuous variables (supplemented by rank-biserial effect sizes $r_{rb}$), while **Pearson Chi-Square** and **Fisher's Exact tests** were used for categorical variables.

*Methodological Note:* Outcome-derived variables (PCHE, total expenditure, poverty line) were strictly excluded from the predictor set. Household size is recognized as a welfare divisor and omitted from multivariable models.

| Characteristic / Factor | Test Type Applied | Test Statistic | df | $p$-value | Effect Size Metric | Effect Size Value |
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
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Model A (Recommended)** | **Farm Size + Credit (2)** | **6.5** | **-24.2882** | **14.234 (2, p=0.0008)** | **54.576** | **60.860** | **0.3253** | **0.1099 [0.0136–0.8905] (p=0.0386)** |
| **Model B** | Farm Size + Credit + Age (3) | 4.3 | -23.7744 | 15.262 (3, p=0.0016) | 55.549 | 63.927 | 0.3452 | 0.1017 [0.0123–0.8415] (p=0.0340) |
| **Model C** | Farm Size + Credit + Extension (3) | 4.3 | -23.4651 | 15.881 (3, p=0.0012) | 54.930 | 63.309 | 0.3570 | 0.1444 [0.0169–1.2334] (p=0.0772) |
| **Model D** | Farm Size + Credit + Other Income (3)| 4.3 | -24.2709 | 14.269 (3, p=0.0026) | 56.542 | 64.920 | 0.3260 | 0.1118 [0.0137–0.9103] (p=0.0407) |

### 9.4 Final Recommended Model (Model A)
**Model A** is selected based on theoretical coherence, parsimony, optimal information criteria (lowest AIC = $54.576$, lowest BIC = $60.860$), superior EPV ($6.5$), and absence of separation anomalies.

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
- **Validated Severity Intervals:**
  - $1.00–1.80$: Not a Challenge
  - $1.81–2.60$: Minor Challenge
  - $2.61–3.40$: Moderate Challenge
  - $3.41–4.20$: Severe Challenge
  - $4.21–5.00$: Very Severe Challenge

| Rank | Challenge Constraint Item | Valid $n$ | Score 1 $n(\%)$ | Score 2 $n(\%)$ | Score 3 $n(\%)$ | Score 4 $n(\%)$ | Score 5 $n(\%)$ | Mean Severity Index (MSI) | Standard Deviation (SD) | Median (IQR) | Severity Category |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **High cost and scarcity of farm labour** | 60 | 0 (0.0%) | 1 (1.7%) | 12 (20.0%) | 24 (40.0%) | 23 (38.3%) | **4.1500** | 0.7988 | 4.00 (1.00) | **Severe Challenge** |
| **2** | **High cost of farm inputs** | 60 | 0 (0.0%) | 4 (6.7%) | 15 (25.0%) | 18 (30.0%) | 23 (38.3%) | **4.0000** | 0.9567 | 4.00 (2.00) | **Severe Challenge** |
| **3** | **Post-harvest losses and inadequate storage facilities** | 60 | 0 (0.0%) | 6 (10.0%) | 15 (25.0%) | 19 (31.7%) | 20 (33.3%) | **3.8833** | 0.9931 | 4.00 (2.00) | **Severe Challenge** |
| **4** | **Unpredictable rainfall and climate conditions**| 60 | 0 (0.0%) | 5 (8.3%) | 18 (30.0%) | 27 (45.0%) | 10 (16.7%) | **3.7000** | 0.8497 | 4.00 (1.00) | **Severe Challenge** |
| **5** | **High cost/scarcity of yam stakes** | 60 | 0 (0.0%) | 7 (11.7%) | 21 (35.0%) | 23 (38.3%) | 9 (15.0%) | **3.5667** | 0.8900 | 4.00 (1.00) | **Severe Challenge** |
| **6** | **Inadequate access to credit** | 60 | 0 (0.0%) | 8 (13.3%) | 25 (41.7%) | 14 (23.3%) | 13 (21.7%) | **3.5333** | 0.9823 | 3.00 (1.00) | **Severe Challenge** |
| **7** | **Inadequate agricultural extension services** | 60 | 2 (3.3%) | 8 (13.3%) | 19 (31.7%) | 19 (31.7%) | 12 (20.0%) | **3.5167** | 1.0655 | 4.00 (1.00) | **Severe Challenge** |
| **8** | **Pest and disease infestation** | 60 | 0 (0.0%) | 8 (13.3%) | 26 (43.3%) | 21 (35.0%) | 5 (8.3%) | **3.3833** | 0.8253 | 3.00 (1.00) | **Moderate Challenge** |
| **9** | **Low and unstable prices of yam** | 59 | 1 (1.7%) | 12 (20.3%) | 29 (49.2%) | 13 (22.0%) | 4 (6.8%) | **3.1186** | 0.8727 | 3.00 (1.00) | **Moderate Challenge** |
| **10** | **Poor access to markets** | 60 | 4 (6.7%) | 20 (33.3%) | 16 (26.7%) | 18 (30.0%) | 2 (3.3%) | **2.9000** | 1.0201 | 3.00 (2.00) | **Moderate Challenge** |

---

## 11. Hypothesis Audit

| Research Hypothesis | Current Thesis Phrasing | Statistical Test Evaluated | Re-Analysis Test Result | Audited Decision | Recommendation for Thesis |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **$H_{01}$ (Objective I/III)** | Socioeconomic and farm characteristics do not significantly influence poverty status of yam farmers. | Multivariable Firth Model Likelihood Ratio Test & Wald Tests | $\text{Model LR } \chi^2(2) = 14.234, p = 0.0008$; Credit access Wald $z = -2.069, p = 0.0386$. | **Reject Null Hypothesis ($H_{01}$)** | Retain rejection of null hypothesis. Frame conclusion as: *Socioeconomic and institutional factors (specifically credit access) are significantly associated with poverty status ($p < 0.05$).* |
| **$H_{02}$ (Objective IV)** | Production and institutional challenges do not significantly constrain yam production. | Descriptive Severity Benchmark Test vs Validated Scale | 7 of 10 constraints fall in the **Severe category** ($3.41–4.20$), with Labour ($4.15$) and Inputs ($4.00$) at peak severity. | **Reject Null Hypothesis ($H_{02}$)** | Descriptive ranking via MSI provides full empirical support for Objective IV. Note that raw dataset does not contain physical output volume (kg/ha) to estimate an econometric production constraint frontier. |

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
| **Labour Challenge MSI** | 4.15 | 4.1500 (Rank 1) | 0.000 | Authoritative 5-point MSI | **4.1500 (Rank 1, Severe)** |
| **Inputs Challenge MSI** | 4.00 | 4.0000 (Rank 2) | 0.000 | Authoritative 5-point MSI | **4.0000 (Rank 2, Severe)** |
| **Storage Challenge MSI**| 3.88 | 3.8833 (Rank 3) | 0.000 | Authoritative 5-point MSI | **3.8833 (Rank 3, Severe)** |
| **Climate Challenge MSI**| 3.70 | 3.7000 (Rank 4) | 0.000 | Authoritative 5-point MSI | **3.7000 (Rank 4, Severe)** |
| **Stakes Challenge MSI** | 3.57 | 3.5667 (Rank 5) | 0.000 | Authoritative 5-point MSI | **3.5667 (Rank 5, Severe)** |
| **Credit Challenge MSI** | 3.53 | 3.5333 (Rank 6) | 0.000 | Authoritative 5-point MSI | **3.5333 (Rank 6, Severe)** |
| **Extension Challenge** | 3.52 | 3.5167 (Rank 7) | 0.000 | Authoritative 5-point MSI | **3.5167 (Rank 7, Severe)** |
| **Pests Challenge MSI** | 3.38 | 3.3833 (Rank 8) | 0.000 | Authoritative 5-point MSI | **3.3833 (Rank 8, Moderate)** |
| **Prices Challenge MSI** | 3.12 | 3.1186 (Rank 9) | 0.000 | Authoritative 5-point MSI | **3.1186 (Rank 9, Moderate)** |
| **Market Challenge MSI** | 2.90 | 2.9000 (Rank 10) | 0.000 | Authoritative 5-point MSI | **2.9000 (Rank 10, Moderate)** |

---

## 15. What Must Change in the Thesis

1. **Likert Scale Specification in Chapter 3:** Correct textual description from a 4-point scale to the authoritative **5-point Likert scale** ($1 = \text{Not a Challenge}$ to $5 = \text{Very Severe}$) with standardized intervals ($1.00–1.80, 1.81–2.60, 2.61–3.40, 3.41–4.20, 4.21–5.00$).
2. **Causal Phrasing:** Replace causal statements (e.g., "credit reduced poverty by $92.56\%$") with non-causal associative phrasing (*"access to credit was significantly associated with $89.01\%$ lower odds of poverty, holding farm size constant"*).
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
- The poverty headcount ratio was $21.67\%$, indicating that 13 of the 60 sampled households were classified as poor.
- Depth of poverty is low ($2.32\%$ overall poverty gap ratio).
- Poverty severity is low ($0.0034$), indicating that consumption deprivation among the poor is relatively uniform and clustered close to the threshold.

### D. FINAL CHALLENGE RESULTS
- 7 out of 10 challenges are classified as **Severe** ($3.41–4.20$), led by Labour Cost ($4.15$), Input Cost ($4.00$), and Storage Losses ($3.88$).
- 3 out of 10 challenges are classified as **Moderate** ($2.61–3.40$): Pest and Disease ($3.38$), Yam Prices ($3.12$), and Market Access ($2.90$).
- Zero challenges are classified as Very Severe ($>4.20$), Minor ($1.81–2.60$), or Not a Challenge ($1.00–1.80$).

### E. KEY LIMITATIONS
- Small sample size ($N = 60$) with 13 poverty events.
- Cross-sectional design prevents causal claims.
- Sparse predictor cells necessitate penalized regression.
- Sampling represents surveyed farming communities in Akpabuyo LGA.

### F. DATA CORRECTIONS
- Corrected Likert challenge scale from 4 points to 5 points with standardized validated intervals.
- Documented 4 expenditure discrepancies ($93.33\%$ concordance, $\kappa = 0.9495$).
- Corrected VIF to $1.5856$ ($r = 0.6077$).
- Addressed Respondent 46 sex anomaly empirically ($n=59$).

### G. REMAINING ISSUES REQUIRING HUMAN VERIFICATION
- **REQUIRES HUMAN VERIFICATION:** Confirm whether Respondent 46 was intended as Female on the physical paper questionnaire or whether it was a keypunch error for Female ($0$). If confirmed on the physical survey form, document this confirmation in the final thesis appendix.
- **REQUIRES HUMAN VERIFICATION:** Confirm whether the academic department requires retaining a formal hypothesis for Objective IV (production constraints) or whether Objective IV is accepted as a descriptive Mean Severity Index ranking.

---
**END OF MASTER INDEPENDENT RE-ANALYSIS AND STATISTICAL AUDIT REPORT**
