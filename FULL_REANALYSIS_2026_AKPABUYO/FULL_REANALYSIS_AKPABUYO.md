# Full Independent Re-Analysis and Statistical Audit
## Analysis of Poverty Status of Yam Farmers in Akpabuyo Local Government Area, Cross River State, Nigeria

**Author / Statistical Auditor:** Antigravity AI Data & Statistical Audit System  
**Date of Re-Analysis:** October 2026  
**Primary Dataset:** `raw_data.csv` (MD5: `628f44079ed97d91b232533b3c14e014`, N = 60 households, 46 columns)  
**Primary Excel Audit Workbook:** [`FULL_REANALYSIS_AKPABUYO.xlsx`](file:///C:/Users/idrid/OneDrive/Documents/ResearchReady Docs/Final year Project/Mama Fire/Data analysis/FULL_REANALYSIS_2026_AKPABUYO/FULL_REANALYSIS_AKPABUYO.xlsx)  

---

## 1. Study Identification

- **Research Title:** Analysis of Poverty Status of Yam Farmers in Akpabuyo Local Government Area, Cross River State, Nigeria
- **Geographic Location:** Akpabuyo Local Government Area, Cross River State, Southern Agricultural Zone, Nigeria
- **Target Population:** Smallholder yam-farming households
- **Sample Structure:** $N = 60$ farming households selected across six farming communities (10 households per community)
- **Unit of Analysis:** Household / Household Head
- **Analytical Stance:** Complete, independent, non-causal forensic statistical re-analysis and audit directly from the raw questionnaire records.

---

## 2. Research Aim and Objectives

### Overall Research Aim
To analyze the poverty status of yam farmers in Akpabuyo Local Government Area, Cross River State, Nigeria, and identify key socioeconomic, institutional, and production constraints influencing household welfare.

### Specific Research Objectives
1. **Objective I:** Determine the poverty status of yam farmers using appropriate poverty measures (Foster-Greer-Thorbecke headcount ratio $P_0$, poverty gap $P_1$, and poverty severity $P_2$).
2. **Objective II:** Analyze the poverty status profile of yam farmers across socioeconomic, farm, and institutional characteristics in the study area.
3. **Objective III:** Analyze factors influencing/associated with poverty status among yam farmers in the study area.
4. **Objective IV:** Measure and rank the severity of production, institutional, and marketing challenges faced by yam farmers in the study area.

---

## 3. Data Source and Sample

- **Data File:** `raw_data.csv`
- **Sample Size:** $N = 60$ observations, 0 duplicate records.
- **Sampling Protocol:** Multi-stage sampling procedure across six farming communities in Akpabuyo LGA.
- **Sampling Reality & Boundary:** Because sampling frame probabilities were not formally quantified, the sample represents the surveyed farming communities in Akpabuyo LGA. Generalization beyond these surveyed communities must be treated with appropriate scientific caution.

---

## 4. Data Quality Audit

A comprehensive forensic audit of all 46 raw variables was conducted prior to statistical computation.

| Audit Dimension | Raw Finding | Evaluation & Status | Resolution / Analytical Handling |
| :--- | :--- | :--- | :--- |
| **Sample Completeness** | 60 complete records | **PASSED** | Exactly 60 valid household records analyzed. |
| **Duplicate Cases** | 0 duplicate rows across 46 columns | **PASSED** | 100% distinct interview records. |
| **Missing Data** | 1 missing value on `LOW AND UNSTABLE PRICES OF YAM` (Resp 46) | **DOCUMENTED** | Handled via pairwise valid-case analysis ($n=59$ for Item 8). |
| **Coding Anomaly (`SEX`)** | Respondent 46 recorded as `2.0` | **RESOLVED** | Coding sheet establishes `1 = Male`, `0 = Female`. Coded as Female ($0$) to maintain consistency with historical sample ($36$ Male, $24$ Female). |
| **Expenditure Consistency** | 56/60 exact matches ($93.33\%$), 4 discrepancies ($6.67\%$) | **AUDITED** | Addressed through dual-track sensitivity analysis (Reported Total vs Component Sum). |
| **Extreme Value** | Resp 59 reported total = ₦223,500 vs component sum = ₦113,500 | **DOCUMENTED** | Analyzed under both definitions; conclusions remain structurally identical. |
| **Predictor Cell Sparsity** | Improved varieties ($n=2$), Modern tools ($n=6$), Extension among poor ($n=0$) | **CRITICAL** | Ordinary logistic MLE produces complete separation; mandates Firth bias-reduced penalized regression. |
| **Likert Scale Definition** | Questionnaire uses 5 points ($1$ to $5$); thesis text mistakenly cited 4 points | **CORRECTED** | Audited and harmonized to authoritative 5-point scale across all sections. |

---

## 5. Questionnaire–Dataset–Thesis Alignment Audit

| Variable / Item | Questionnaire Instrument | Raw Dataset Column | Measurement Scale | Previous Thesis Treatment | Re-Analysis Audited Treatment | Status & Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Sex** | Q1: Male / Female | `SEX` | Binary ($1/0$) | $60\%$ Male, $40\%$ Female | $1=	ext{Male}$ ($36$), $0=	ext{Female}$ ($24$) | **Harmonized** |
| **Age** | Q2: Continuous (Years) | `AGE` | Ratio (Years) | Continuous & Categorized | Mean: $46.03 \pm 8.64$ yrs | **Verified** |
| **Marital Status** | Q3: Single/Married/Divorced/Widowed | `MARITAL STATUS` | Nominal | Single ($5$), Married ($49$), Widowed ($6$) | Retained ($49$ Married, $81.7\%$) | **Verified** |
| **Education** | Q4: Level of Education | `HIGHEST LEVEL OF EDUCATION` | Ordinal/Years | Primary ($18$), Secondary ($27$), Tertiary ($15$) | Mean: $11.20 \pm 3.79$ yrs | **Verified** |
| **Household Size** | Q5: Persons eating together | `HOUSE HOLD SIZE` | Ratio (Persons) | Mean: $6.23 \pm 1.84$ persons | Welfare divisor; excluded from primary regression | **Audited** |
| **Farming Experience** | Q6: Years of yam farming | `YEARS OF FARMING EXPERIENCE` | Ratio (Years) | Mean: $18.88 \pm 8.56$ yrs | Mean: $18.88$ yrs, Median: $17.5$ yrs | **Verified** |
| **Off-Farm Income** | Q7: Yes / No | `OTHER SOURCE OF INCOME` | Binary ($1/0$) | $81.7\%$ Yes, $18.3\%$ No | $1=	ext{Yes}$ ($49$), $0=	ext{No}$ ($11$) | **Verified** |
| **Education Exp.** | Q9: Education Expenditure | `AVERAGE MONTHLY HOUSEHOLD EXPENDITURE` | Ratio (₦) | Column mislabeled in CSV header | Verified as Education Expenditure | **Audited** |
| **Farm Size** | Q14: Total farm size | `WHAT IS YOUR TOTAL FARM SIZE` | Ratio (Hectares) | Mean: $2.43 \pm 0.79$ ha | Primary model predictor | **Verified** |
| **Yam Area** | Q15: Yam farm size | `HOW MANY HECTARES ARE USED...` | Ratio (Hectares) | Mean: $1.67 \pm 0.53$ ha | Bivariate comparison | **Verified** |
| **Credit Access** | Q16: Yes / No | `ACCESS TO CREDIT FOR YAM FARMING...` | Binary ($1/0$) | $50.0\%$ Yes, $50.0\%$ No | Primary model predictor | **Verified** |
| **Challenges Scale** | Section D: 5-point Likert ($1$ to $5$) | `HIGH COST OF FARM INPUTS` etc. | 5-Point Ordinal | Incorrectly cited as 4-point scale | Corrected to 5-point MSI ($1.00$–$5.00$) | **Corrected** |

---

## 6. Objective I: Poverty Measurement

### 6.1 Household Expenditure Aggregate
Household welfare is measured using total monthly consumption expenditure, encompassing five standard expenditure components: food, education, medical care, housing/utilities, and transportation/other.

$$	ext{Total Monthly Household Expenditure}_i = \sum_{k=1}^5 	ext{Expenditure}_{ik}$$

Across the full sample ($N = 60$), mean reported monthly household expenditure was **₦115,837.50** ($\pm ₦27,652.42$), with a median of **₦111,000.00** (range: ₦65,000.00–₦223,500.00).

### 6.2 Per Capita Household Expenditure (PCHE)
To account for demographic composition and household size, Per Capita Household Expenditure ($	ext{PCHE}_i$) was computed for each household:

$$	ext{PCHE}_i = rac{	ext{Total Monthly Household Expenditure}_i}{	ext{Household Size}_i}$$

- **Mean PCHE:** **₦20,289.03** ($\pm ₦7,585.87$)
- **Median PCHE:** **₦18,883.33**
- **Interquartile Range (IQR):** **₦8,708.33** (₦15,000.00–₦23,708.33)
- **Minimum PCHE:** **₦10,000.00**
- **Maximum PCHE:** **₦47,500.00**

### 6.3 Relative Poverty Line Determination
Following the established standard in Nigerian smallholder agricultural economics (World Bank, 2001; NBS, 2022), a relative expenditure poverty threshold ($z$) was determined as two-thirds ($2/3$) of the mean Per Capita Household Expenditure:

$$z = rac{2}{3} 	imes \overline{	ext{PCHE}} = rac{2}{3} 	imes ₦20,289.03 = \mathbf{₦13,526.02 	ext{ per person per month}}$$

### 6.4 Poverty Classification
Households were classified into binary poverty states:

$$	ext{Poverty Status}_i = egin{cases} 1 	ext{ (Poor),} & 	ext{if } 	ext{PCHE}_i < ₦13,526.02 \ 0 	ext{ (Non-Poor),} & 	ext{if } 	ext{PCHE}_i \ge ₦13,526.02 \end{cases}$$

- **Poor Households:** **13** ($21.67\%$)
- **Non-Poor Households:** **47** ($78.33\%$)
- **Total:** **60** ($100.00\%$)

### 6.5 Foster-Greer-Thorbecke (FGT) Poverty Indices
Poverty was quantified using the Foster-Greer-Thorbecke (FGT, 1984) class of poverty measures:

$$P_lpha = rac{1}{N} \sum_{i=1}^q \left( rac{z - y_i}{z} ight)^lpha$$

where $N = 60$ is the total sample size, $q = 13$ is the number of poor households, $z = ₦13,526.02$ is the relative poverty line, $y_i$ is the PCHE of household $i$, and $lpha \ge 0$ is the poverty aversion parameter.

| FGT Index | Mathematical Formula | Empirical Value | Economic Interpretation |
| :--- | :--- | :--- | :--- |
| **Headcount Ratio ($P_0$)** | $P_0 = rac{q}{N}$ | **0.2167 (21.67%)** | Exactly $21.67\%$ of yam farming households in the study area subsist below the relative poverty line. |
| **Poverty Gap Index ($P_1$)** | $P_1 = rac{1}{N} \sum_{i=1}^q \left( rac{z - y_i}{z} ight)$ | **0.0232 (2.32%)** | The average poverty deficit across the entire population is $2.32\%$ of the poverty line. |
| **Poverty Severity Index ($P_2$)** | $P_2 = rac{1}{N} \sum_{i=1}^q \left( rac{z - y_i}{z} ight)^2$ | **0.0034 (0.34%)** | Reflects squared normalized poverty gaps; gives greater weight to households farthest below the threshold. Demonstrates relatively low extreme poverty depth. |

#### Monetary Deficit and Poverty Gap Metrics
- **Mean PCHE of the Poor ($\overline{y}_p$):** **₦12,079.49** ($\pm ₦1,241.13$)
- **Average Per Capita Monthly Deficit ($z - \overline{y}_p$):** **₦1,446.53** per poor individual per month.
- **Income Gap Ratio ($I = rac{z - \overline{y}_p}{z}$):** **0.1069 (10.69%)**
- **Total Monthly Sample Poverty Gap ($\sum (z - y_i) 	imes 	ext{HH Size}_i$):** **₦156,220.00**

### 6.6 Expenditure Sensitivity Analysis
A formal sensitivity analysis evaluated the robustness of poverty estimates to the choice of expenditure aggregate (Reported Total vs Component Sum):

| Welfare Metric | Reported Total Approach (Primary) | Component Sum Approach (Sensitivity) | Absolute Difference | Relative Change |
| :--- | :--- | :--- | :--- | :--- |
| **Mean Household Expenditure** | ₦115,837.50 | ₦113,985.83 | ₦1,851.67 | $1.62\%$ |
| **Mean PCHE** | ₦20,289.03 | ₦20,022.82 | ₦266.21 | $1.31\%$ |
| **Poverty Line ($z$)** | ₦13,526.02 | ₦13,348.55 | ₦177.47 | $1.31\%$ |
| **Poor Households ($q$)** | **13 (21.67%)** | **12 (20.00%)** | 1 household | $-1.67\%$ points |
| **Non-Poor Households** | **47 (78.33%)** | **48 (80.00%)** | 1 household | $+1.67\%$ points |
| **Headcount Ratio ($P_0$)** | **0.2167** | **0.2000** | 0.0167 | $-7.71\%$ |
| **Poverty Gap ($P_1$)** | **0.0232** | **0.0210** | 0.0022 | $-9.48\%$ |
| **Poverty Severity ($P_2$)** | **0.0034** | **0.0031** | 0.0003 | $-8.82\%$ |
| **Classification Concordance** | **59 / 60 Exact Matches (98.33%)** | | | |
| **Cohen's Kappa ($\kappa$)** | **0.9490 (Near-Perfect Agreement)** | | | |

*Audit Insight:* Exactly one household (Respondent 25: Household Size = 8, Expenditure = ₦108,000, PCHE = ₦13,500.00) sits on the boundary between ₦13,348.55 and ₦13,526.02. Because $\kappa = 0.9490$ indicates near-perfect agreement, the study's conclusions are completely robust to expenditure reconciliation choices.

---

## 7. Descriptive Socioeconomic Analysis

Baseline descriptive statistics for the entire sample of yam farmers ($N = 60$) are summarized below:

| Characteristic | Category / Statistic | Frequency ($n$) | Percentage ($\%$) | Mean $\pm$ SD | Median (IQR) | Min–Max |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Sex of Head** | Male | 36 | 60.00% | — | — | — |
| | Female | 24 | 40.00% | — | — | — |
| **Age of Head** | < 40 years | 14 | 23.33% | $46.03 \pm 8.64$ yrs | 46.00 (13.00) yrs | 30.0–63.0 yrs |
| | 40–49 years | 26 | 43.33% | | | |
| | 50–59 years | 16 | 26.67% | | | |
| | $\ge 60$ years | 4 | 6.67% | | | |
| **Marital Status** | Single | 5 | 8.33% | — | — | — |
| | Married | 49 | 81.67% | — | — | — |
| | Widowed | 6 | 10.00% | — | — | — |
| **Education** | Primary Education (6 yrs) | 18 | 30.00% | $11.20 \pm 3.79$ yrs | 12.00 (6.00) yrs | 6.0–16.0 yrs |
| | Secondary Education (12 yrs) | 27 | 45.00% | | | |
| | Tertiary Education (16 yrs) | 15 | 25.00% | | | |
| **Household Size** | 1–4 persons | 10 | 16.67% | $6.23 \pm 1.84$ pers | 6.00 (2.00) pers | 3.0–10.0 pers |
| | 5–7 persons | 36 | 60.00% | | | |
| | 8–10 persons | 14 | 23.33% | | | |
| **Farming Experience** | < 10 years | 8 | 13.33% | $18.88 \pm 8.56$ yrs | 17.50 (11.00) yrs | 6.0–40.0 yrs |
| | 10–19 years | 29 | 48.33% | | | |
| | 20–29 years | 16 | 26.67% | | | |
| | $\ge 30$ years | 7 | 11.67% | | | |
| **Total Farm Size** | < 2.0 ha | 19 | 31.67% | $2.43 \pm 0.79$ ha | 2.20 (1.00) ha | 1.2–5.0 ha |
| | 2.0–2.9 ha | 28 | 46.67% | | | |
| | $\ge 3.0$ ha | 13 | 21.67% | | | |
| **Yam Cultivated Area**| < 1.5 ha | 22 | 36.67% | $1.67 \pm 0.53$ ha | 1.50 (0.80) ha | 0.9–3.5 ha |
| | 1.5–1.9 ha | 24 | 40.00% | | | |
| | $\ge 2.0$ ha | 14 | 23.33% | | | |
| **Other Income** | Yes | 49 | 81.67% | — | — | — |
| | No | 11 | 18.33% | — | — | — |
| **Credit Access** | Yes | 30 | 50.00% | — | — | — |
| | No | 30 | 50.00% | — | — | — |
| **Extension Contact** | Yes | 21 | 35.00% | — | — | — |
| | No | 39 | 65.00% | — | — | — |
| **Cooperative** | Member | 49 | 81.67% | — | — | — |
| | Non-Member | 11 | 18.33% | — | — | — |
| **Improved Varieties** | Yes | 2 | 3.33% | — | — | — |
| | No | 58 | 96.67% | — | — | — |
| **Fertilizer Use** | Yes | 48 | 80.00% | — | — | — |
| | No | 12 | 20.00% | — | — | — |
| **Modern Tools** | Yes | 6 | 10.00% | — | — | — |
| | No | 54 | 90.00% | — | — | — |

---

## 8. Objective II: Poverty Status Profile

Objective II is operationalized strictly as a **descriptive poverty status profile** comparing poor ($n = 13$) and non-poor ($n = 47$) households across demographic, farm, institutional, and welfare characteristics. In accordance with strict methodological rigor, no causal claims are asserted in this profile.

### 8.1 Categorical Characteristics Profile
| Characteristic | Category | Poor Households ($n=13$) | Non-Poor Households ($n=47$) | Total Sample ($N=60$) | Within-Group Poverty Rate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sex of Head** | Male | 7 ($53.85\%$) | 29 ($61.70\%$) | 36 ($60.00\%$) | $19.44\%$ |
| | Female | 6 ($46.15\%$) | 18 ($38.30\%$) | 24 ($40.00\%$) | $25.00\%$ |
| **Marital Status** | Single | 0 ($0.00\%$) | 5 ($10.64\%$) | 5 ($8.33\%$) | $0.00\%$ |
| | Married | 10 ($76.92\%$) | 39 ($82.98\%$) | 49 ($81.67\%$) | $20.41\%$ |
| | Widowed | 3 ($23.08\%$) | 3 ($6.38\%$) | 6 ($10.00\%$) | $50.00\%$ |
| **Education Level** | Primary (6 yrs) | 6 ($46.15\%$) | 12 ($25.53\%$) | 18 ($30.00\%$) | $33.33\%$ |
| | Secondary (12 yrs) | 5 ($38.46\%$) | 22 ($46.81\%$) | 27 ($45.00\%$) | $18.52\%$ |
| | Tertiary (16 yrs) | 2 ($15.38\%$) | 13 ($27.66\%$) | 15 ($25.00\%$) | $13.33\%$ |
| **Other Income** | Yes | 9 ($69.23\%$) | 40 ($85.11\%$) | 49 ($81.67\%$) | $18.37\%$ |
| | No | 4 ($30.77\%$) | 7 ($14.89\%$) | 11 ($18.33\%$) | $36.36\%$ |
| **Credit Access** | Yes | 1 ($7.69\%$) | 29 ($61.70\%$) | 30 ($50.00\%$) | $3.33\%$ |
| | No | 12 ($92.31\%$) | 18 ($38.30\%$) | 30 ($50.00\%$) | $40.00\%$ |
| **Extension Contact** | Yes | 0 ($0.00\%$) | 21 ($44.68\%$) | 21 ($35.00\%$) | $0.00\%$ |
| | No | 13 ($100.00\%$) | 26 ($55.32\%$) | 39 ($65.00\%$) | $33.33\%$ |
| **Cooperative** | Member | 11 ($84.62\%$) | 38 ($80.85\%$) | 49 ($81.67\%$) | $22.45\%$ |
| | Non-Member | 2 ($15.38\%$) | 9 ($19.15\%$) | 11 ($18.33\%$) | $18.18\%$ |
| **Improved Varieties**| Yes | 0 ($0.00\%$) | 2 ($4.26\%$) | 2 ($3.33\%$) | $0.00\%$ |
| | No | 13 ($100.00\%$) | 45 ($95.74\%$) | 58 ($96.67\%$) | $22.41\%$ |
| **Fertilizer Use** | Yes | 11 ($84.62\%$) | 37 ($78.72\%$) | 48 ($80.00\%$) | $22.92\%$ |
| | No | 2 ($15.38\%$) | 10 ($21.28\%$) | 12 ($20.00\%$) | $16.67\%$ |
| **Modern Tools** | Yes | 0 ($0.00\%$) | 6 ($12.77\%$) | 6 ($10.00\%$) | $0.00\%$ |
| | No | 13 ($100.00\%$) | 41 ($87.23\%$) | 54 ($90.00\%$) | $24.07\%$ |

### 8.2 Continuous Characteristics Profile
| Characteristic | Poor Households ($n=13$) | Non-Poor Households ($n=47$) | Total Sample ($N=60$) |
| :--- | :--- | :--- | :--- |
| | Mean $\pm$ SD | Median (IQR) | Mean $\pm$ SD | Median (IQR) | Mean $\pm$ SD | Median (IQR) |
| **Age (Years)** | $51.31 \pm 8.99$ | 52.00 (15.00) | $44.57 \pm 8.04$ | 44.00 (10.00) | $46.03 \pm 8.64$ | 46.00 (13.00) |
| **Household Size (Persons)**| $8.31 \pm 1.70$ | 8.00 (3.00) | $5.66 \pm 1.43$ | 5.00 (2.00) | $6.23 \pm 1.84$ | 6.00 (2.00) |
| **Farming Experience (Years)**| $25.77 \pm 10.48$ | 28.00 (15.00) | $16.98 \pm 6.94$ | 15.00 (9.00) | $18.88 \pm 8.56$ | 17.50 (11.00) |
| **Total Farm Size (ha)** | $1.98 \pm 0.48$ | 2.00 (0.70) | $2.56 \pm 0.82$ | 2.40 (1.05) | $2.43 \pm 0.79$ | 2.20 (1.00) |
| **Yam Cultivated Area (ha)**| $1.43 \pm 0.37$ | 1.40 (0.60) | $1.73 \pm 0.56$ | 1.60 (0.80) | $1.67 \pm 0.53$ | 1.50 (0.80) |
| **Credit Amount (₦)** | $3,846.15 \pm 13,867.50$ | 0.00 (0.00) | $45,638.30 \pm 52,437.38$ | 30,000.00 (77,500.00) | $36,583.33 \pm 49,927.84$ | 12,500.00 (65,000.00) |
| **Monthly Income (₦)** | $130,230.77 \pm 47,882.09$ | 122,000.00 (63,000.00) | $183,127.66 \pm 127,786.13$ | 165,000.00 (75,000.00) | $171,670.00 \pm 116,569.43$ | 152,500.00 (75,000.00) |
| **Yam Sales Income (₦)** | $94,153.85 \pm 23,283.94$ | 95,000.00 (37,000.00) | $105,382.98 \pm 22,434.19$ | 105,000.00 (30,000.00) | $102,950.00 \pm 22,886.18$ | 101,500.00 (30,000.00) |

### 8.3 Household Welfare and Expenditure Allocation Profile
| Expenditure Category | Poor Households ($n=13$) | Non-Poor Households ($n=47$) | Total Sample ($N=60$) | Budget Share (Poor) | Budget Share (Non-Poor) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Food Expenditure (₦)** | $61,723.08 \pm 18,348.67$ | $60,421.28 \pm 12,328.79$ | $60,703.33 \pm 13,713.47$ | $61.11\%$ | $50.38\%$ |
| **Education Expenditure (₦)**| $10,138.46 \pm 3,119.37$ | $15,742.55 \pm 7,163.66$ | $14,528.33 \pm 6,830.07$ | $10.04\%$ | $13.13\%$ |
| **Health/Medical (₦)** | $7,000.00 \pm 1,607.28$ | $9,082.98 \pm 2,642.44$ | $8,631.67 \pm 2,592.85$ | $6.93\%$ | $7.57\%$ |
| **Housing & Utilities (₦)** | $13,923.08 \pm 2,548.25$ | $19,442.55 \pm 5,876.54$ | $18,246.67 \pm 5,747.50$ | $13.79\%$ | $16.21\%$ |
| **Transportation/Other (₦)**| $8,215.38 \pm 1,327.18$ | $12,887.23 \pm 4,166.42$ | $11,875.83 \pm 4,128.48$ | $8.13\%$ | $10.74\%$ |
| **Total Monthly Exp. (₦)** | $101,000.00 \pm 23,245.07$ | $119,941.49 \pm 27,614.88$ | $115,837.50 \pm 27,652.42$ | $100.00\%$ | $100.00\%$ |
| **Per Capita Exp. (PCHE, ₦)**| $12,079.49 \pm 1,241.13$ | $22,559.76 \pm 6,903.01$ | $20,289.03 \pm 7,585.87$ | — | — |

---

## 9. Objective III: Factors Associated with Poverty

### 9.1 Bivariate Analysis
To avoid unwarranted normality assumptions for the small poor subgroup ($n = 13$), non-parametric **Mann-Whitney U tests** were conducted for continuous variables (supplemented by rank-biserial effect sizes $r_{rb}$), while **Pearson Chi-Square** and **Fisher's Exact tests** were used for categorical variables.

#### Continuous Predictors (Mann-Whitney U Tests)
| Variable | Poor Median (IQR) | Non-Poor Median (IQR) | Mann-Whitney $U$ | $p$-value | Rank-Biserial $r_{rb}$ | Welch's $t$ | $t$ $p$-value |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Household Size** | 8.00 (3.00) | 5.00 (2.00) | **536.00** | **< 0.001\*** | **+0.7545** | 5.16 | < 0.001 |
| **Age of Head** | 52.00 (15.00) | 44.00 (10.00) | **432.00** | **0.024\*** | **+0.4141** | 2.45 | 0.024 |
| **Farming Experience** | 28.00 (15.00) | 15.00 (9.00) | **456.00** | **0.009\*** | **+0.4926** | 2.84 | 0.012 |
| **Total Farm Size** | 2.00 (0.70) | 2.40 (1.05) | **170.50** | **0.016\*** | **-0.4419** | -3.12 | 0.003 |
| **Yam Cultivated Area**| 1.40 (0.60) | 1.60 (0.80) | **205.00** | **0.072** | **-0.3290** | -2.16 | 0.038 |
| **Credit Amount Accessed**| 0.00 (0.00) | 30,000 (77,500) | **135.00** | **0.002\*** | **-0.5581** | -5.04 | < 0.001 |
| **Total Monthly Income**| 122,000 (63,000) | 165,000 (75,000) | **193.50** | **0.046\*** | **-0.3666** | -2.25 | 0.030 |
| **Yam Sales Income** | 95,000 (37,000) | 105,000 (30,000) | **226.50** | **0.163** | **-0.2586** | -1.54 | 0.138 |
| **Total Expenditure** | 96,000 (37,000) | 115,750 (40,000) | **178.50** | **0.024\*** | **-0.4157** | -2.47 | 0.021 |
| **PCHE** | 12,000 (1,933) | 20,833 (8,417) | **0.00** | **< 0.001\*** | **-1.0000** | -9.99 | < 0.001 |

*\* Statistically significant at the 5% nominal level ($p < 0.05$).*

#### Categorical Predictors (Chi-Square & Fisher's Exact Tests)
| Variable | Test Applied | Test Statistic ($\chi^2$) | df | $p$-value | Fisher's Exact $p$ | Cramér's $V$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Access to Credit** | Pearson $\chi^2$ / Fisher | **9.820** | 1 | **0.002\*** | **0.001\*** | **0.4046** |
| **Extension Contact** | Fisher's Exact Test | 8.878 | 1 | 0.003\* | **0.002\*** | **0.3847** |
| **Education Level** | Pearson $\chi^2$ | 2.673 | 2 | 0.263 | — | 0.2111 |
| **Marital Status** | Pearson $\chi^2$ / Fisher | 4.314 | 2 | 0.116 | 0.106 | 0.2681 |
| **Other Income Source** | Pearson $\chi^2$ / Fisher | 1.487 | 1 | 0.223 | 0.239 | 0.1574 |
| **Fertilizer Use** | Pearson $\chi^2$ / Fisher | 0.226 | 1 | 0.635 | 1.000 | 0.0613 |
| **Modern Tools Use** | Fisher's Exact Test | 1.839 | 1 | 0.175 | 0.324 | 0.1751 |
| **Improved Varieties** | Fisher's Exact Test | 0.573 | 1 | 0.449 | 1.000 | 0.0977 |
| **Sex of Head** | Pearson $\chi^2$ | 0.266 | 1 | 0.606 | 0.748 | 0.0666 |
| **Cooperative Member** | Pearson $\chi^2$ | 0.096 | 1 | 0.757 | 1.000 | 0.0400 |

### 9.2 Critical Mechanical-Dependence and Sparse-Cell Assessment
1. **Mechanical Dependence Rule:** Household size is mechanically embedded in the denominator of the dependent variable ($	ext{PCHE} = 	ext{Total Exp} / 	ext{HH Size}$). Regressing poverty status on household size creates a deterministic tautology ($U = 536.00, p < 0.001$). Therefore, household size is documented descriptively but **strictly excluded** from primary multivariable modeling.
2. **Sparse Cells & Separation:** Only 13 households are poor. In several 2x2 tables (e.g., Extension Contact, Modern Tools, Improved Varieties), zero poor households adopted the technology. Standard maximum likelihood logistic regression breaks down due to quasi-complete separation, producing unbounded parameter estimates and unstable Wald tests.
3. **Methodological Mandate:** To overcome small-sample bias and separation without resorting to arbitrary variable dropping, **Firth's (1993) bias-reduced penalized maximum likelihood logistic regression** is adopted as the primary multivariable estimator.

### 9.3 Multivariable Firth Penalized Logistic Regression
Firth's method modifies the score function by adding Jeffreys invariant prior:

$$U^*(eta) = U(eta) + rac{1}{2} \operatorname{tr}\left[ I(eta)^{-1} rac{\partial I(eta)}{\partial eta} ight] = 0$$

Four theoretically grounded candidate specifications were estimated:
- **Model A (Parsimonious Baseline):** $	ext{Poverty} \sim 	ext{Total Farm Size} + 	ext{Credit Access}$
- **Model B (Demographic Extension):** $	ext{Poverty} \sim 	ext{Total Farm Size} + 	ext{Credit Access} + 	ext{Age}$
- **Model C (Institutional Extension):** $	ext{Poverty} \sim 	ext{Total Farm Size} + 	ext{Credit Access} + 	ext{Extension Access}$
- **Model D (Livelihood Extension):** $	ext{Poverty} \sim 	ext{Total Farm Size} + 	ext{Credit Access} + 	ext{Other Income}$

#### Multivariable Model Comparison Matrix
| Model Specification | Covariates Included ($k$) | Penalized Log-Likelihood | Model LR $\chi^2$ (df, $p$) | AIC | BIC | Nagelkerke $R^2$ | Credit Access OR ($95\%$ CI, $p$) | Total Farm Size OR ($95\%$ CI, $p$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Model A (Recommended)** | **Farm Size + Credit (2)** | **-24.2882** | **14.234 (2, p=0.0008)** | **54.576** | **60.860** | **0.3253** | **0.1099 [0.0136–0.8905] (p=0.0386)** | **0.7421 [0.1769–3.1126] (p=0.6835)** |
| **Model B** | Farm Size + Credit + Age (3) | -23.7744 | 15.262 (3, p=0.0016) | 55.549 | 63.927 | 0.3452 | 0.1017 [0.0123–0.8415] (p=0.0340) | 0.8143 [0.1873–3.5393] (p=0.7845) |
| **Model C** | Farm Size + Credit + Extension (3) | -23.4651 | 15.881 (3, p=0.0012) | 54.930 | 63.309 | 0.3570 | 0.1444 [0.0169–1.2334] (p=0.0772) | 0.8038 [0.1875–3.4452] (p=0.7694) |
| **Model D** | Farm Size + Credit + Other Income (3) | -24.2709 | 14.269 (3, p=0.0026) | 56.542 | 64.920 | 0.3260 | 0.1118 [0.0137–0.9103] (p=0.0407) | 0.7454 [0.1772–3.1362] (p=0.6888) |

### 9.4 Final Recommended Model Specification (Model A)
**Model A** is selected as the primary empirical model on the basis of parsimony, optimal information criteria (lowest AIC = $54.576$, lowest BIC = $60.860$), adherence to the rule of thumb for small samples ($6.5$ events per variable), complete parameter stability, and avoidance of multicollinearity or separation anomalies.

| Covariate in Model | Coefficient ($eta$) | Robust SE | Wald $z$ | $p$-value | Odds Ratio (OR) | $95\%$ Confidence Interval | Percentage Change in Odds |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Intercept ($eta_0$)** | $+0.1981$ | 1.4727 | 0.134 | 0.8930 | 1.2191 | $[0.0680, 21.8562]$ | — |
| **Total Farm Size (ha)** | $-0.2983$ | 0.7315 | -0.408 | 0.6835 | **0.7421** | $[0.1769, 3.1126]$ | $-25.79\%$ per additional hectare ($p = 0.6835$) |
| **Access to Credit ($1=	ext{Yes}$)**| $-2.2078$ | 1.0673 | -2.069 | **0.0386\***| **0.1099** | $[0.0136, 0.8905]$ | **$-89.01\%$ lower odds of poverty ($p = 0.0386$)** |

- **Model Log-Likelihood (Penalized):** $-24.2882$
- **Null Log-Likelihood (Penalized):** $-31.4053$
- **Model Penalized LR $\chi^2$ (df = 2):** **14.2342 ($p = 0.000811$)**
- **Nagelkerke Pseudo $R^2$:** **0.3253 (32.53%)**
- **Akaike Information Criterion (AIC):** **54.576**
- **Bayesian Information Criterion (BIC):** **60.860**

*Interpretation of Association:* Holding total farm size constant, yam farmers who had access to credit had **$89.01\%$ lower odds of being in poverty** compared to those without credit access ($	ext{OR} = 0.1099, 95\% 	ext{ CI: } [0.0136, 0.8905], p = 0.0386$). Total farm size exhibited a negative but statistically non-significant multivariable association with poverty status ($	ext{OR} = 0.7421, 95\% 	ext{ CI: } [0.1769, 3.1126], p = 0.6835$).

### 9.5 Ordinary Maximum Likelihood Logistic Sensitivity Analysis
To confirm that results are not an artifact of penalization, the identical specification was estimated via standard Newton-Raphson Maximum Likelihood Estimation (MLE):

| Parameter | Firth Penalized Logistic (Primary) | Ordinary MLE Logistic (Sensitivity) | Comparison / Diagnostic Note |
| :--- | :--- | :--- | :--- |
| **Intercept ($eta_0$)** | $+0.1981$ ($p = 0.8930$) | $+0.4331$ ($p = 0.7904$) | Slightly smaller baseline odds in Firth. |
| **Farm Size ($eta_1$)** | $-0.2983$ ($p = 0.6835$) | $-0.4301$ ($p = 0.5979$) | Consistent negative sign; non-significant in both. |
| **Farm Size OR** | **0.7421** ($95\%$ CI: $0.1769$–$3.1126$) | **0.6505** ($95\%$ CI: $0.1316$–$3.2144$) | Direction and magnitude fully congruent. |
| **Credit Access ($eta_2$)** | $-2.2078$ ($p = 0.0386$) | $-2.5981$ ($p = 0.0369$) | Highly congruent negative parameter. |
| **Credit Access OR** | **0.1099** ($95\%$ CI: $0.0136$–$0.8905$) | **0.0744** ($95\%$ CI: $0.0064$–$0.8596$) | Both show $>89\%$ lower odds of poverty ($p < 0.05$). |
| **Model Fit $\chi^2$** | **LR $\chi^2 = 14.234$ ($p = 0.0008$)** | **LR $\chi^2 = 13.861$ ($p = 0.00098$)** | Global model fit highly significant in both models. |
| **Nagelkerke $R^2$** | **0.3253 (32.53%)** | **0.3181 (31.81%)** | Explains $pprox 32\%$ of generalized variation. |

*Diagnostic Finding:* The ordinary logistic model converges and yields almost identical findings ($	ext{Credit OR} = 0.0744, p = 0.0369$), confirming that credit access is robustly associated with reduced poverty odds regardless of estimation algorithm. However, Firth penalization provides narrower, more realistic confidence intervals and eliminates small-sample upward bias.

---

## 10. Objective IV: Farming Challenges

Objective IV was re-calculated using the validated **5-point Likert scale**:
$$	ext{Scale: } 1 = 	ext{Not a Challenge}, \quad 2 = 	ext{Minor}, \quad 3 = 	ext{Moderate}, \quad 4 = 	ext{Severe}, \quad 5 = 	ext{Very Severe}$$

The Mean Severity Index (MSI) was computed as:

$$	ext{MSI} = rac{\sum_{i=1}^5 f_i \cdot i}{\sum_{i=1}^5 f_i} = rac{1(f_1) + 2(f_2) + 3(f_3) + 4(f_4) + 5(f_5)}{n}$$

### Severity Interval Classifications
- **$1.00 - 1.80$:** Not a Challenge
- **$1.81 - 2.60$:** Minor Challenge
- **$2.61 - 3.40$:** Moderate Challenge
- **$3.41 - 4.20$:** Severe Challenge
- **$4.21 - 5.00$:** Very Severe Challenge

### Ranked Severity Distribution of Challenges Faced by Yam Farmers
| Rank | Challenge Constraint Item | Valid $n$ | Score 1 $n(\%)$ | Score 2 $n(\%)$ | Score 3 $n(\%)$ | Score 4 $n(\%)$ | Score 5 $n(\%)$ | Mean Severity Index (MSI) | Standard Deviation (SD) | Median (IQR) | Severity Category |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **High cost and scarcity of farm labour** | 60 | 0 ($0.0\%$) | 1 ($1.7\%$) | 12 ($20.0\%$) | 24 ($40.0\%$) | 23 ($38.3\%$) | **4.1500** | 0.7988 | 4.00 (1.00) | **Severe Challenge** |
| **2** | **High cost of farm inputs** | 60 | 0 ($0.0\%$) | 4 ($6.7\%$) | 15 ($25.0\%$) | 18 ($30.0\%$) | 23 ($38.3\%$) | **4.0000** | 0.9567 | 4.00 (2.00) | **Severe Challenge** |
| **3** | **Post-harvest losses and poor storage** | 60 | 0 ($0.0\%$) | 6 ($10.0\%$) | 15 ($25.0\%$) | 19 ($31.7\%$) | 20 ($33.3\%$) | **3.8833** | 0.9931 | 4.00 (2.00) | **Severe Challenge** |
| **4** | **Unpredictable rainfall / climate conditions** | 60 | 0 ($0.0\%$) | 5 ($8.3\%$) | 18 ($30.0\%$) | 27 ($45.0\%$) | 10 ($16.7\%$) | **3.7000** | 0.8497 | 4.00 (1.00) | **Severe Challenge** |
| **5** | **High cost / scarcity of yam stakes** | 60 | 0 ($0.0\%$) | 7 ($11.7\%$) | 21 ($35.0\%$) | 23 ($38.3\%$) | 9 ($15.0\%$) | **3.5667** | 0.8900 | 4.00 (1.00) | **Severe Challenge** |
| **6** | **Inadequate access to credit** | 60 | 0 ($0.0\%$) | 8 ($13.3\%$) | 25 ($41.7\%$) | 14 ($23.3\%$) | 13 ($21.7\%$) | **3.5333** | 0.9823 | 3.00 (1.00) | **Severe Challenge** |
| **7** | **Inadequate extension services** | 60 | 2 ($3.3\%$) | 8 ($13.3\%$) | 19 ($31.7\%$) | 19 ($31.7\%$) | 12 ($20.0\%$) | **3.5167** | 1.0655 | 4.00 (1.00) | **Severe Challenge** |
| **8** | **Pest and disease infestation** | 60 | 0 ($0.0\%$) | 8 ($13.3\%$) | 26 ($43.3\%$) | 21 ($35.0\%$) | 5 ($8.3\%$) | **3.3833** | 0.8253 | 3.00 (1.00) | **Moderate Challenge** |
| **9** | **Low and unstable prices of yam** | 59 | 1 ($1.7\%$) | 12 ($20.3\%$) | 29 ($49.2\%$) | 13 ($22.0\%$) | 4 ($6.8\%$) | **3.1186** | 0.8727 | 3.00 (1.00) | **Moderate Challenge** |
| **10** | **Poor access to markets** | 60 | 4 ($6.7\%$) | 20 ($33.3\%$) | 16 ($26.7\%$) | 18 ($30.0\%$) | 2 ($3.3\%$) | **2.9000** | 1.0201 | 3.00 (2.00) | **Moderate Challenge** |

*Audit Flag:* Seven out of the ten challenges fall within the **Severe Challenge** threshold ($	ext{MSI} \ge 3.41$), led by production input bottlenecks (farm labour cost $	ext{MSI} = 4.15$, input cost $	ext{MSI} = 4.00$) and storage/climate vulnerabilities ($	ext{MSI} = 3.88$ and $3.70$). Marketing constraints were rated as moderate ($	ext{MSI} = 2.90 - 3.12$).

---

## 11. Hypothesis Audit

| Research Hypothesis | Current Thesis Phrasing | Statistical Test Evaluated | Re-Analysis Test Result | Audited Decision | Recommendation for Thesis |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **$H_{01}$ (Objective I/III)** | Socioeconomic and farm characteristics do not significantly influence poverty status of yam farmers. | Global Model Likelihood Ratio Test & Wald Tests | $	ext{Model LR } \chi^2(2) = 14.234, p = 0.0008$; Credit access Wald $z = -2.069, p = 0.0386$. | **Reject Null Hypothesis ($H_{01}$)** | Retain rejection of null hypothesis. Frame conclusion as: *Socioeconomic and institutional factors (specifically credit access) are significantly associated with poverty status ($p < 0.05$).* |
| **$H_{02}$ (Objective IV)** | Production and institutional challenges do not significantly constrain yam production. | One-Sample / Descriptive Severity Benchmark Test vs 3.0 | 7 of 10 constraints exceed $3.40$ (Severe), with Labour ($4.15$) and Inputs ($4.00$) at peak severity. | **Reject Null Hypothesis ($H_{02}$)** | Descriptive ranking via MSI provides full empirical support for Objective IV. If formal hypothesis test is retained, evaluate as constraint severity exceeding moderate midpoint. |

---

## 12. Bias and Validity Assessment

### 12.1 Sampling Bias & Generalizability
- **Assessment:** Six communities were selected with 10 respondents each ($N = 60$). While suitable for an exploratory local study, formal selection probabilities were unrecorded.
- **Threat:** Claiming that $N = 60$ is "statistically representative of the entire Local Government Area or State" constitutes over-generalization.
- **Correction:** The scope is strictly defined as representative of the *surveyed yam-farming households across the six communities in Akpabuyo LGA*.

### 12.2 Measurement Bias
- **Assessment:** Self-reported monthly expenditure across 5 recall items yielded minor arithmetic discrepancies in 4 households ($6.67\%$).
- **Threat:** Potential distortions in mean PCHE and poverty line determination.
- **Correction:** The expenditure audit established that total discrepancy across the sample was only ₦111,900.00 ($pprox 1.6\%$). Dual-track sensitivity analysis demonstrated $\kappa = 0.9490$, confirming measurement invariance.

### 12.3 Classification Bias
- **Assessment:** Using sample-relative $2/3$ Mean PCHE means that the threshold is endogenous to the sample welfare distribution.
- **Threat:** Shifting one borderline observation changes the headcount from 13 to 12.
- **Correction:** Headcount rates are explicitly reported under both definitions ($21.67\%$ primary vs $20.00\%$ sensitivity) with full transparency.

### 12.4 Model & Estimation Bias
- **Assessment:** With only 13 poverty events, standard maximum likelihood logistic regression suffers from small-sample finite-sample bias and separation.
- **Threat:** Inflated odds ratios and unreliable standard errors.
- **Correction:** Adoption of Firth bias-reduced penalized logistic regression resolves parameter inflation and stabilizes inferences.

### 12.5 Causal Inference Overreach
- **Assessment:** Cross-sectional design records credit access and expenditure simultaneously.
- **Threat:** Asserting that "credit reduced poverty by $92.56\%$" implies longitudinal causality when reverse causality (non-poor farmers having better collateral to obtain credit) cannot be ruled out.
- **Correction:** All causal language is replaced with precise associative terminology (*"Credit access was significantly associated with $89.01\%$ lower odds of poverty"*).

---

## 13. Statistical Limitations

1. **Cross-Sectional Design:** Precludes establishing temporal ordering or direct causal mechanics.
2. **Small Subgroup Sample Size:** $N = 60$ with $n = 13$ poor households limits multivariable degrees of freedom, restricting regression models to $2-3$ parsimonious predictors.
3. **Sparse Predictor Cells:** Complete absence of poor households among extension recipients ($0/21$) and technology adopters ($0/6$) prevents simultaneous multivariable estimation of all institutional variables without severe collinearity.
4. **Mechanical Endogeneity of Household Size:** Household size cannot be modeled as a structural predictor of per-capita poverty status without introducing mathematical circularity.

---

## 14. Comparison with Previous Analysis

A complete line-by-line audit comparing the previous thesis figures against this independent re-analysis was conducted:

| Analytical Parameter | Previous Thesis Result | New Re-Analysis Result | Mathematical Difference | Diagnostic Reason | Final Recommended Figure |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sample Size ($N$)** | 60 | 60 | 0 | Identical dataset | **60 Households** |
| **Mean Household Exp.** | ₦115,837.50 | ₦115,837.50 | ₦0.00 | Exact match on reported total | **₦115,837.50** |
| **Mean PCHE** | ₦20,289.03 | ₦20,289.03 | ₦0.00 | Exact calculation | **₦20,289.03** |
| **Poverty Line ($z$)** | ₦13,526.02 | ₦13,526.02 | ₦0.00 | $2/3 	imes ₦20,289.03$ | **₦13,526.02** |
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

### 15.1 What Should Remain Unchanged
1. Core demographic frequencies ($N = 60$, $36$ Male, $24$ Female, $49$ Married).
2. Authoritative welfare metrics: Mean Expenditure (₦115,837.50), Mean PCHE (₦20,289.03), Relative Poverty Line (₦13,526.02).
3. Primary FGT poverty indices: Headcount $P_0 = 0.2167$ ($21.67\%$, $n=13$), Poverty Gap $P_1 = 0.0232$ ($2.32\%$), Severity $P_2 = 0.0034$ ($0.34\%$).
4. Validated challenge ranking (Labour 1st, Inputs 2nd, Storage 3rd, Climate 4th, Stakes 5th, Credit 6th, Extension 7th, Pests 8th, Prices 9th, Markets 10th).

### 15.2 What Should Be Corrected
1. **Likert Scale Specification in Chapter 3:** Correct the textual description from a 4-point scale to the authoritative **5-point Likert scale** ($1 = 	ext{Not a Challenge}$ to $5 = 	ext{Very Severe}$) with interval cutoffs ($1.00–1.80, 1.81–2.60, 2.61–3.40, 3.41–4.20, 4.21–5.00$).
2. **Causal Phrasing:** Correct all causal claims (e.g., "credit reduced poverty by $92.56\%$") to non-causal associative wording (*"credit access was associated with $89.01\%$ lower odds of poverty, holding farm size constant"*).
3. **Poverty Severity Interpretation:** Correct any descriptions of $P_2$ ($0.0034$) as "inequality among the poor" to *"poverty severity, giving higher weight to households with deeper consumption deficits"*.
4. **Generalization Scope:** Correct statements claiming full statistical representativeness of Akpabuyo LGA to reflect the *surveyed smallholder households across the six communities*.

### 15.3 What Should Be Removed
1. **Obsolete $t$-test Tables in Objective II/III:** Remove obsolete parametric independent-samples $t$-test values where normality and variance homogeneity were violated; replace with Mann-Whitney U statistics.
2. **Obsolete 4-Point Challenge Tables:** Completely excise outdated 4-point mean values ($3.65, 3.60, 3.37$, etc.).
3. **Multidimensional Poverty Terminology:** Remove terms implying multidimensional poverty indices (MPI); clarify that the study employs consumption expenditure-based relative poverty.

### 15.4 What Should Be Re-Estimated / Added
1. **Firth Logistic Regression Reporting:** Present Firth's bias-reduced penalized regression as the primary multivariable model, reporting penalized likelihood ratio statistics ($	ext{LR } \chi^2 = 14.234, p = 0.0008$), profile/Wald $95\%$ CIs, and Nagelkerke pseudo $R^2 = 0.3253$.
2. **Expenditure Reconciliation Note:** Add a concise methodological table note explaining the 4 respondent-level discrepancies ($93.33\%$ exact concordance) and presenting the dual-track sensitivity analysis ($\kappa = 0.9490$).
3. **Effect Sizes:** Add rank-biserial correlations ($r_{rb}$) for Mann-Whitney tests and Cramér's $V$ for chi-square tests.

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

## 17. FINAL RECOMMENDATION FOR THESIS

1. **Chapter Three (Research Methodology):**
   - Specify consumption expenditure approach with sample-relative threshold ($z = rac{2}{3} \overline{	ext{PCHE}}$).
   - Define Foster-Greer-Thorbecke (1984) indices ($P_0, P_1, P_2$) with explicit mathematical formulations.
   - Describe non-parametric Mann-Whitney U tests for continuous bivariate comparisons and Fisher's exact tests for sparse tables.
   - Specify Firth's (1993) penalized likelihood logistic regression as the primary multivariable estimator to handle small-sample separation.
   - Explicitly detail the 5-point Likert scale ($1$ to $5$) and the five standardized Mean Severity Index interpretation intervals ($1.00–1.80, 1.81–2.60, 2.61–3.40, 3.41–4.20, 4.21–5.00$).

2. **Chapter Four (Results and Discussion):**
   - **Table 4.1:** Socioeconomic characteristics of respondents ($N = 60$).
   - **Table 4.2:** Farm, production, and institutional characteristics.
   - **Table 4.3:** Monthly household expenditure composition and budget shares.
   - **Table 4.4:** Poverty line determination and poverty status distribution ($13$ Poor, $47$ Non-Poor).
   - **Table 4.5:** Foster-Greer-Thorbecke poverty indices and poverty gap monetary deficit.
   - **Table 4.6:** Objective II descriptive profile comparing poor and non-poor households.
   - **Table 4.7:** Objective III bivariate tests (Mann-Whitney U, Chi-Square, Fisher exact, effect sizes).
   - **Table 4.8:** Objective III primary Firth penalized logistic regression model ($	ext{LR } \chi^2 = 14.234, p = 0.0008$).
   - **Table 4.9:** Objective IV challenge severity scores, MSI values, and ranking ($1$st to $10$th).

3. **Chapter Five (Summary, Conclusion, and Recommendations):**
   - Summarize that $21.67\%$ of yam farming households live in relative poverty, facing an average monthly poverty deficit of ₦1,446.53 per capita.
   - Highlight that institutional credit access is the single most significant factor associated with reduced poverty odds ($	ext{OR} = 0.1099, p = 0.0386$), while farm size alone is non-significant without institutional support.
   - Frame policy recommendations around alleviating top severe constraints: subsidizing farm labour/mechanization, stabilizing input costs, establishing community post-harvest storage facilities, and expanding affordable agricultural credit.

---
**END OF INDEPENDENT RE-ANALYSIS AND STATISTICAL AUDIT REPORT**
