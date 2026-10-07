# Final Quality-Control (QC) Audit and Verification Report
## Study: Analysis of Poverty Status of Yam Farmers in Akpabuyo LGA, Cross River State, Nigeria

**Audit Date:** October 2026  
**Auditing Entity:** Antigravity AI Data & Statistical Audit System  
**Scope of Review:** Verification of numerical consistency, scale harmonization, non-causal language compliance, and methodological rigor across all deliverables in `FULL_REANALYSIS_AKPABUYO_FINAL/`.

---

## 1. Summary of Quality-Control Corrections Made

| QC Item | Prior State / Flagged Issue | Corrected Action Taken | Verification Status |
| :--- | :--- | :--- | :---: |
| **1. Challenge Scale Intervals** | Described as 4-point scale or arbitrary 3.0 cut-off; 2.90 misclassified. | Adopted validated 5-interval scale: $1.00–1.80$ (Not a Challenge), $1.81–2.60$ (Minor), $2.61–3.40$ (Moderate), $3.41–4.20$ (Severe), $4.21–5.00$ (Very Severe). Classified 2.90 as **Moderate**; 7 items as **Severe**, 3 items as **Moderate**. | **RESOLVED & VERIFIED** |
| **2. Component-Sum Expenditure** | Intermediate draft cited ₦113,975.00. | Recalculated exact arithmetic sum of component means ($₦60,703.33 + ₦14,528.33 + ₦8,631.67 + ₦18,246.67 + ₦11,875.83 = ₦113,985.83$) and row-level sum ($₦6,839,150.00 / 60 = ₦113,985.83$). Updated all sensitivity tables and documented the arithmetic origin. | **RESOLVED & VERIFIED** |
| **3. Poverty Classification Phrasing** | Text described 21.67% poverty incidence as "low-to-moderate". | Removed unsupported label. Replaced with exact descriptive statement: *"The poverty headcount ratio was 21.67%, indicating that 13 of the 60 sampled yam-farming households were classified as poor under the study's relative poverty threshold."* | **RESOLVED & VERIFIED** |
| **4. Objective II Narrative Language** | Text referred to household size as "single most pronounced demographic predictor". | Replaced with: *"Household size showed the largest observed difference between poor and non-poor households."* Removed all references to "predictors" in the descriptive poverty profile section. | **RESOLVED & VERIFIED** |
| **5. Household Size Cautionary Note** | Lacked prominent methodological caveat in profile tables. | Added explicit methodological note: *"Household size should be interpreted cautiously because it forms the denominator of the per-capita household expenditure measure used to classify poverty. Therefore, its observed association with poverty status does not by itself establish an independent causal effect."* | **RESOLVED & VERIFIED** |
| **6. Questionnaire Variable Naming** | Challenge labels had slight cosmetic paraphrasing. | Harmonized all 10 challenge labels with exact questionnaire items from `raw_data.csv`. | **RESOLVED & VERIFIED** |
| **7. Multi-Criteria Model Justification** | Rationale relied heavily on $p$-values and AIC. | Expanded `MODEL_SELECTION_JUSTIFICATION.md` to ground Model A in economic theory, parsimony ($6.5$ EPV), sparse-cell separation safeguards, absence of mechanical endogeneity, parameter stability, and profile-likelihood CIs. | **RESOLVED & VERIFIED** |
| **8. Non-Causal Thesis Language** | Some legacy causal terms ("reduced", "determined", "influenced"). | Replaced all causal claims with associative language (*"associated with"*, *"differed significantly"*, *"exhibited lower estimated odds"*). | **RESOLVED & VERIFIED** |

---

## 2. Numerical Discrepancies Found and Resolved

1. **Expenditure Component Mean Sum vs Row Mean:**
   - *Finding:* Sum of 5 component columns = ₦6,839,150.00 across 60 households.
   - *Resolution:* Mean component sum = **₦113,985.83**. Arithmetic sum of component means = **₦113,985.83**. Exact mathematical equality verified.
2. **Poverty Sensitivity Metrics:**
   - *Reported Total (Primary):* Mean PCHE = ₦20,289.03, $z = ₦13,526.02$, Poor = 13 ($21.67\%$), $P_0 = 0.2167, P_1 = 0.0232, P_2 = 0.0034$.
   - *Component Sum (Sensitivity):* Mean PCHE = ₦20,022.82, $z = ₦13,348.55$, Poor = 12 ($20.00\%$), $P_0 = 0.2000, P_1 = 0.0208, P_2 = 0.0029$.
   - *Concordance:* 59/60 ($98.33\%$), Cohen's $\kappa = 0.9495$.
3. **Challenge Classification Reconciliation:**
   - Ranks 1 to 7 (Labour 4.15, Inputs 4.00, Storage 3.88, Climate 3.70, Stakes 3.57, Credit 3.53, Extension 3.52) $\rightarrow$ **Severe Challenge** ($3.41 \le \text{MSI} \le 4.20$).
   - Ranks 8 to 10 (Pests 3.38, Prices 3.12, Market 2.90) $\rightarrow$ **Moderate Challenge** ($2.61 \le \text{MSI} \le 3.40$).
   - Minor ($1.81–2.60$), Not a Challenge ($1.00–1.80$), and Very Severe ($>4.20$) $\rightarrow$ **0 items**.

---

## 3. Cross-File Numerical Identity Verification

An automated verification was conducted across the 4 core documentation files and the 27-tab Excel workbook:
- `FULL_REANALYSIS_AKPABUYO_FINAL.xlsx`
- `FULL_REANALYSIS_AKPABUYO_FINAL.md`
- `THESIS_TABLES_FINAL.md`
- `MODEL_SELECTION_JUSTIFICATION.md`

| Parameter / Statistic | Excel Tab Value | Markdown Report Value | Thesis Table Value | Model Justification Value | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Sample Size ($N$) | 60 | 60 | 60 | 60 | **IDENTICAL** |
| Poor Households ($q$) | 13 | 13 | 13 | 13 | **IDENTICAL** |
| Headcount Ratio ($P_0$) | 0.2167 (21.67%) | 0.2167 (21.67%) | 0.2167 (21.67%) | 21.67% | **IDENTICAL** |
| Poverty Gap ($P_1$) | 0.0232 (2.32%) | 0.0232 (2.32%) | 0.0232 (2.32%) | — | **IDENTICAL** |
| Poverty Severity ($P_2$) | 0.0034 (0.34%) | 0.0034 (0.34%) | 0.0034 (0.34%) | — | **IDENTICAL** |
| Relative Poverty Line ($z$) | ₦13,526.02 | ₦13,526.02 | ₦13,526.02 | — | **IDENTICAL** |
| Credit Access $\beta$ | -2.2078 | -2.2078 | -2.2078 | -2.2078 | **IDENTICAL** |
| Credit Access SE | 1.0673 | 1.0673 | 1.0673 | 1.0673 | **IDENTICAL** |
| Credit Access Odds Ratio | 0.1099 | 0.1099 | 0.1099 | 0.1099 | **IDENTICAL** |
| Credit Access $p$-value | 0.0386 | 0.0386 | 0.0386 | 0.0386 | **IDENTICAL** |
| Credit Profile 95% CI | $[0.0087, 0.7014]$ | $[0.0087, 0.7014]$ | $[0.0087, 0.7014]$ | $[0.0087, 0.7014]$ | **IDENTICAL** |
| Farm Size Odds Ratio | 0.7421 | 0.7421 | 0.7421 | 0.7421 | **IDENTICAL** |
| Farm Size $p$-value | 0.6835 | 0.6835 | 0.6835 | 0.6835 | **IDENTICAL** |
| Farm Size Profile 95% CI | $[0.1383, 2.9557]$ | $[0.1383, 2.9557]$ | $[0.1383, 2.9557]$ | — | **IDENTICAL** |
| Model LR $\chi^2$ | 14.2342 | 14.2342 | 14.2342 | 14.234 | **IDENTICAL** |
| Model LR $p$-value | 0.000811 | 0.000811 | 0.000811 | 0.00081 | **IDENTICAL** |
| Nagelkerke Pseudo $R^2$ | 0.3253 | 0.3253 | 0.3253 | 0.3253 | **IDENTICAL** |
| Penalized AIC | 54.576 | 54.576 | 54.576 | 54.576 | **IDENTICAL** |
| Penalized BIC | 60.860 | 60.860 | 60.860 | 60.860 | **IDENTICAL** |
| Labour Challenge MSI | 4.1500 (Severe) | 4.1500 (Severe) | 4.1500 (Severe) | — | **IDENTICAL** |
| Input Challenge MSI | 4.0000 (Severe) | 4.0000 (Severe) | 4.0000 (Severe) | — | **IDENTICAL** |
| Storage Challenge MSI | 3.8833 (Severe) | 3.8833 (Severe) | 3.8833 (Severe) | — | **IDENTICAL** |
| Climate Challenge MSI | 3.7000 (Severe) | 3.7000 (Severe) | 3.7000 (Severe) | — | **IDENTICAL** |
| Stakes Challenge MSI | 3.5667 (Severe) | 3.5667 (Severe) | 3.5667 (Severe) | — | **IDENTICAL** |
| Credit Challenge MSI | 3.5333 (Severe) | 3.5333 (Severe) | 3.5333 (Severe) | — | **IDENTICAL** |
| Extension Challenge MSI | 3.5167 (Severe) | 3.5167 (Severe) | 3.5167 (Severe) | — | **IDENTICAL** |
| Pests Challenge MSI | 3.3833 (Moderate) | 3.3833 (Moderate) | 3.3833 (Moderate) | — | **IDENTICAL** |
| Prices Challenge MSI | 3.1186 (Moderate) | 3.1186 (Moderate) | 3.1186 (Moderate) | — | **IDENTICAL** |
| Market Challenge MSI | 2.9000 (Moderate) | 2.9000 (Moderate) | 2.9000 (Moderate) | — | **IDENTICAL** |

---

## 4. Remaining Unresolved Issues Requiring Human Decision

Zero statistical or arithmetic inconsistencies remain in the dataset or documentation. The following two items represent institutional administrative decisions requiring student/supervisor confirmation:

1. **Physical Questionnaire Confirmation for Respondent 46 (`SEX`):**
   - *Status:* Empirically evaluated as missing/unverified ($n=59$). If the physical paper questionnaire confirms `2` was intended as Female ($0$), the student can note this confirmation in the final thesis text without changing any substantive conclusions ($p=0.496$ vs $p=0.606$).
2. **Departmental Format for Objective IV Hypothesis:**
   - *Status:* Objective IV is fully satisfied and published as a descriptive Mean Severity Index ranking. If the department requires formal hypothesis rejection language, the audit confirms rejecting the null constraint hypothesis based on 7 out of 10 items falling in the Severe category ($3.41–4.20$).

---
**FINAL QUALITY-CONTROL STATUS: FULLY VERIFIED, INTERNALLY CONSISTENT, AND EXAMINER-READY.**
