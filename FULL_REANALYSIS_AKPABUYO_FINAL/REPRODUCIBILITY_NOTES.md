# Methodological and Reproducibility Notes
## Study: Analysis of Poverty Status of Yam Farmers in Akpabuyo LGA, Nigeria

---

### 1. Mathematical and Statistical Formulation

#### 1.1 Per Capita Household Expenditure (PCHE)
For each household $i \in \{1, \dots, N\}$:
$$	ext{PCHE}_i = rac{	ext{Total Monthly Household Expenditure}_i}{	ext{Household Size}_i}$$

#### 1.2 Relative Poverty Line ($z$)
$$z = rac{2}{3} 	imes \overline{	ext{PCHE}} = rac{2}{3} 	imes \left( rac{1}{N} \sum_{i=1}^N 	ext{PCHE}_i ight)$$
For the primary reported total expenditure ($N = 60$):
$$\overline{	ext{PCHE}} = ₦20,289.03 \implies z = rac{2}{3} 	imes ₦20,289.03 = \mathbf{₦13,526.02}$$

#### 1.3 Foster–Greer–Thorbecke (FGT, 1984) Poverty Measures
$$P_lpha = rac{1}{N} \sum_{i=1}^q \left( rac{z - y_i}{z} ight)^lpha$$
where $y_i = 	ext{PCHE}_i$, $q = \sum_{i=1}^N \mathbb{I}(y_i < z)$ is the number of poor households, and $lpha \ge 0$.
- **$lpha = 0$ (Headcount Ratio $P_0$):** $P_0 = rac{q}{N} = rac{13}{60} = \mathbf{0.2167 	ext{ (21.67\%)}}$
- **$lpha = 1$ (Poverty Gap Index $P_1$):** $P_1 = rac{1}{N} \sum_{i=1}^q \left( rac{z - y_i}{z} ight) = \mathbf{0.0232 	ext{ (2.32\%)}}$
- **$lpha = 2$ (Poverty Severity Index $P_2$):** $P_2 = rac{1}{N} \sum_{i=1}^q \left( rac{z - y_i}{z} ight)^2 = \mathbf{0.0034 	ext{ (0.34\%)}}$

#### 1.4 Firth (1993) Bias-Reduced Penalized Logistic Regression
To handle sparse events ($q = 13$) and complete separation in institutional variables, Firth's penalized maximum likelihood modifies the log-likelihood by the Jeffreys invariant prior:
$$\ell^*(eta) = \ell(eta) + rac{1}{2} \ln |I(eta)|$$
where $I(eta) = X^T W X$ is the Fisher information matrix and $W = \operatorname{diag}(\pi_i (1 - \pi_i))$.
The modified score equations solved iteratively are:
$$U^*(eta) = X^T \left( y - \pi + h \odot (0.5 - \pi) ight) = 0$$
where $h_i = [X (X^T W X)^{-1} X^T W]_{ii}$ are the diagonal elements of the hat matrix.

#### 1.5 Confidence Interval Procedures
1. **Wald-type 95% Confidence Interval:**
   $$eta_j \pm 1.959964 	imes \operatorname{SE}(eta_j) \implies 	ext{OR 95\% CI: } \left[ \exp(eta_j - 1.96 \cdot 	ext{SE}), \exp(eta_j + 1.96 \cdot 	ext{SE}) ight]$$
2. **Profile Penalized-Likelihood 95% Confidence Interval:**
   Inverting the penalized likelihood ratio test:
   $$\left\{ eta_j : 2 \left( \ell^*(\hat{eta}) - \ell^*(eta_j, \hat{eta}_{-j}(eta_j)) ight) \le \chi^2_{1, 0.95} = 3.841459 ight\}$$
   - For Credit Access: Profile 95% CI is $[-4.7388, -0.3546] \implies 	ext{OR} \in [0.0087, 0.7014]$.
   - For Farm Size: Profile 95% CI is $[-1.9780, 1.0837] \implies 	ext{OR} \in [0.1383, 2.9557]$.

#### 1.6 Mean Severity Index (MSI) for Challenges
$$	ext{MSI} = rac{\sum_{k=1}^5 f_k \cdot k}{\sum_{k=1}^5 f_k} = rac{1(f_1) + 2(f_2) + 3(f_3) + 4(f_4) + 5(f_5)}{n}$$

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
