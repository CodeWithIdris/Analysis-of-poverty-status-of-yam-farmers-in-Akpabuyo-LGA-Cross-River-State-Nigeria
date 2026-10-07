# Final Quality-Control (QC) Audit and Verification Report
## Study: Analysis of Poverty Status of Yam Farmers in Akpabuyo LGA, Cross River State, Nigeria

**Audit Date:** October 2026  
**Auditing Entity:** Antigravity AI Data & Statistical Audit System  
**Scope of Review:** Independent verification of computational integrity, scale harmonization, non-causal language compliance, econometric robustness, and cross-file consistency across all deliverables in `FULL_REANALYSIS_AKPABUYO_FINAL/`.

---

## A. Checks Completed

A comprehensive, multi-stage forensic audit was executed directly against `raw_data.csv` ($N = 60$ households, 46 columns, MD5: `628f44079ed97d91b232533b3c14e014`) and cross-checked across all final deliverables (`FULL_REANALYSIS_AKPABUYO_FINAL.xlsx`, `FULL_REANALYSIS_AKPABUYO_FINAL.md`, `THESIS_TABLES_FINAL.md`, `DATA_CORRECTIONS_LOG.md`, `MODEL_SELECTION_JUSTIFICATION.md`, and `REPRODUCIBILITY_NOTES.md`):

1. **File Inventory & Delivery Verification:**
   - Confirmed existence, formatting, and structural integrity of all 7 required deliverables in `FULL_REANALYSIS_AKPABUYO_FINAL/`.
2. **Raw-Data Expenditure Audit:**
   - Evaluated reported total monthly household expenditure against the arithmetic sum of the 5 constituent categories (Food, Education, Health, Housing/Utilities, Transportation/Other) across all 60 households.
   - Mean reported total expenditure = **₦115,837.50** (Total sum = ₦6,950,250.00).
   - Component means verified: Food (**₦60,703.33**), Education (**₦14,528.33**), Health (**₦8,631.67**), Housing/Utilities (**₦18,246.67**), Transportation/Other (**₦11,875.83**).
   - Sum of component means = **₦113,985.83**; Mean of row-level component sums = **₦113,985.83** (Total sum = ₦6,839,150.00).
   - Confirmed exactly 56 out of 60 households (93.33%) have zero discrepancy. Documented all 4 respondent-level discrepancies: Resp 14 (+₦1,000.00), Resp 37 (-₦400.00), Resp 39 (+₦500.00), Resp 59 (+₦110,000.00).
3. **Poverty Measurement & Sensitivity Verification:**
   - **Primary Baseline (Reported Total):** Mean PCHE = **₦20,289.03**, Poverty Line $z = \mathbf{₦13,526.02}$, Poor $n = \mathbf{13}$ ($21.67\%$), Non-poor $n = \mathbf{47}$ ($78.33\%$), $P_0 = \mathbf{0.2167}$, $P_1 = \mathbf{0.0232}$, $P_2 = \mathbf{0.0034}$.
   - **Sensitivity Benchmark (Component Sum):** Mean PCHE = **₦20,022.82**, Poverty Line $z = \mathbf{₦13,348.55}$, Poor $n = \mathbf{12}$ ($20.00\%$), Non-poor $n = \mathbf{48}$ ($80.00\%$), $P_0 = \mathbf{0.2000}$, $P_1 = \mathbf{0.0208}$, $P_2 = \mathbf{0.0029}$.
   - Classification concordance = **59/60 exact matches (98.33%)**, Cohen's $\kappa = \mathbf{0.9495}$ (near-perfect agreement).
4. **Challenge Likert Scale Harmonization:**
   - Verified validated 5-point Likert scale intervals: $1.00–1.80$ (Not a Challenge), $1.81–2.60$ (Minor), $2.61–3.40$ (Moderate), $3.41–4.20$ (Severe), $4.21–5.00$ (Very Severe).
   - Confirmed exact classification of all 10 items: 7 Severe (Labour 4.15, Inputs 4.00, Storage 3.88, Climate 3.70, Stakes 3.57, Credit 3.53, Extension 3.52) and 3 Moderate (Pests 3.38, Prices 3.12 on valid $n=59$, Market 2.90).
   - Confirmed complete absence of arbitrary "Mean $\ge 3.00 = \text{Severe}$" rule and confirmed 2.90 is strictly categorized as Moderate.
5. **Multivariable Econometric Model Verification:**
   - Verified final Firth bias-reduced penalized logistic regression model (Model A: Total Farm Size + Access to Credit).
   - Total Farm Size: $\beta = -0.2983, \text{SE} = 0.7315, \text{Wald } z = -0.408, p = 0.6835, \text{OR} = \mathbf{0.7421}$ ($\exp(-0.2983) = 0.7421$), Wald $95\%\text{ CI: } [0.1769, 3.1126]$, Profile Penalized-Likelihood $95\%\text{ CI: } [0.1383, 2.9557]$.
   - Access to Credit ($1=\text{Yes}$): $\beta = -2.2078, \text{SE} = 1.0673, \text{Wald } z = -2.069, p = \mathbf{0.0386}, \text{OR} = \mathbf{0.1099}$ ($\exp(-2.2078) = 0.1099$), Wald $95\%\text{ CI: } [0.0136, 0.8905]$, Profile Penalized-Likelihood $95\%\text{ CI: } [0.0087, 0.7014]$.
   - Intercept: $\beta = +0.1981, \text{SE} = 1.4727, p = 0.8930, \text{OR} = 1.2191$, Wald $95\%\text{ CI: } [0.0680, 21.8562]$, Profile $95\%\text{ CI: } [0.0725, 33.3121]$.
   - Model Fit: Penalized $\text{LR } \chi^2(2) = \mathbf{14.2342} (p = 0.000811)$, Nagelkerke pseudo $R^2 = \mathbf{0.3253}$, Penalized $\text{AIC} = \mathbf{54.576}$, Penalized $\text{BIC} = \mathbf{60.860}$.
6. **Collinearity and Specification Verification:**
   - Farm Size vs Credit Access: Pearson $r = 0.6077$, $\text{VIF} = \mathbf{1.5856}$, $\text{Tolerance} = \mathbf{0.6307}$. Confirmed removal of erroneous $\text{VIF} = 1.004$ claim.
   - Farm Size vs Yam Cultivated Area: Pearson $r = 0.9642$, $\text{VIF} = \mathbf{14.2120}$. Confirmed Yam Area is excluded from multivariable models to prevent severe collinearity.
7. **Descriptive Narrative & Non-Causal Language Compliance:**
   - Confirmed removal of "single most pronounced demographic predictor" from poverty profile.
   - Confirmed standard phrasing: *"Household size showed the largest observed difference between poor and non-poor households."*
   - Confirmed prominent methodological warning that household size forms the denominator of PCHE and cannot be treated as an independent causal determinant.
   - Confirmed complete elimination of unsupported causal claims (*"credit reduced poverty"*, *"credit caused lower poverty"*, *"farm size influenced poverty"*, *"age caused poverty"*), replacing them with precise associative terminology.
8. **Multi-Criteria Model Selection Verification:**
   - Confirmed Model A is grounded in economic theory, parsimony ($6.5$ EPV vs $4.3$ EPV in expanded models), prevention of separation artifacts (mitigating $0/21$ extension zero-cell), absence of mechanical outcome leakage, parameter stability, and optimal information criteria ($\text{AIC} = 54.576, \text{BIC} = 60.860$).
9. **Cross-File Numerical Identity:**
   - Verified that every numerical value across `FULL_REANALYSIS_AKPABUYO_FINAL.xlsx`, `FULL_REANALYSIS_AKPABUYO_FINAL.md`, `THESIS_TABLES_FINAL.md`, and `MODEL_SELECTION_JUSTIFICATION.md` matches with zero divergence.

---

## B. Corrections Made

| Item | Prior / Draft State | Final Audited Correction Applied | Verification Status |
| :--- | :--- | :--- | :---: |
| **1. Likert Scale Harmonization** | Cited as 4-point scale or arbitrary 3.0 cut-off; 2.90 misclassified. | Standardized to authoritative 5-point Likert scale ($1.00–1.80$ Not a Challenge, $1.81–2.60$ Minor, $2.61–3.40$ Moderate, $3.41–4.20$ Severe, $4.21–5.00$ Very Severe). Classified 2.90 strictly as **Moderate**; 7 items as **Severe**, 3 items as **Moderate**. | **CORRECTED & VERIFIED** |
| **2. Component-Sum Arithmetic** | Intermediate draft cited ₦113,975.00. | Calculated exact arithmetic sum of component means ($₦60,703.33 + ₦14,528.33 + ₦8,631.67 + ₦18,246.67 + ₦11,875.83 = \mathbf{₦113,985.83}$) and row-level sum ($₦6,839,150.00 / 60 = \mathbf{₦113,985.83}$). Harmonized all sensitivity tables and documented exact arithmetic origin. | **CORRECTED & VERIFIED** |
| **3. Poverty Classification Narrative** | Text described 21.67% poverty headcount as "low-to-moderate". | Removed subjective label. Replaced with exact factual statement: *"The poverty headcount ratio was 21.67%, indicating that 13 of the 60 sampled yam-farming households were classified as poor under the study's relative poverty threshold."* | **CORRECTED & VERIFIED** |
| **4. Household Size Profile Phrasing** | Text referred to household size as "single most pronounced demographic predictor". | Replaced with: *"Household size showed the largest observed difference between poor and non-poor households."* Removed all references to "predictors" in descriptive profile sections. | **CORRECTED & VERIFIED** |
| **5. Methodological Caution on Household Size** | Missing prominent caveat regarding mathematical endogeneity. | Added explicit caveat across all profile tables and narratives: *"Household size should be interpreted cautiously because it forms the denominator of the per-capita household expenditure measure used to classify poverty. Therefore, its observed association with poverty status does not by itself establish an independent causal effect."* | **CORRECTED & VERIFIED** |
| **6. Multicollinearity & VIF Accuracy** | Erroneously reported $\text{VIF} = 1.004$ alongside $r = 0.6077$. | Corrected to exact matrix values: Pearson $r = 0.6077 \implies \text{VIF} = \mathbf{1.5856}$, $\text{Tolerance} = \mathbf{0.6307}$. Documented Farm Size vs Yam Area collinearity ($\text{VIF} = 14.2120$) to justify excluding Yam Area from multivariable models. | **CORRECTED & VERIFIED** |
| **7. Multi-Criteria Model Justification** | Rationale relied narrowly on $p$-values and AIC. | Expanded justification to encompass economic theory, parsimony ($6.5$ EPV), zero-cell separation safeguards, absence of mechanical endogeneity, parameter direction stability, and profile-likelihood CIs. | **CORRECTED & VERIFIED** |
| **8. Non-Causal Thesis Phrasing** | Contained legacy causal terms ("reduced", "determined", "influenced"). | Systematically replaced all causal claims with precise associative phrasing (*"was associated with"*, *"differed significantly"*, *"exhibited lower estimated odds"*). | **CORRECTED & VERIFIED** |

---

## C. Remaining Inconsistencies

**Zero numerical, arithmetic, or methodological inconsistencies remain in the dataset, calculations, or documentation.**

All cross-file statistics are 100% congruent across the 27-tab Excel workbook (`FULL_REANALYSIS_AKPABUYO_FINAL.xlsx`) and the Markdown thesis deliverables.

Two external administrative / institutional items are noted for supervisor/student confirmation:
1. **Physical Questionnaire Confirmation for Respondent 46 (`SEX`):**
   - In `raw_data.csv`, Row 46 has `SEX = 2.0`. In the primary empirical re-analysis, this is treated as unverified/missing (valid $n = 59$: 36 Male [61.02%], 23 Female [38.98%]). If the student/supervisor inspects the physical paper survey form and confirms `2` was a keypunch entry for Female ($0$), this can be noted in the thesis text without altering any substantive statistical conclusions (gender remains non-significant at $p = 0.496$ / $p = 0.606$).
2. **Objective IV Departmental Hypothesis Format:**
   - Objective IV is fully satisfied and reported as an authoritative descriptive Mean Severity Index (MSI) ranking (7 Severe items, 3 Moderate items). Because the dataset does not contain physical output volume (kg/ha), no econometric production constraint function is fabricated. If the department requires formal null hypothesis rejection text, the audit confirms rejecting the null constraint hypothesis based on 7 out of 10 items exceeding the Severe threshold ($3.41–4.20$).

---

## D. Final Status

STATUS:
**READY FOR THESIS USE**
