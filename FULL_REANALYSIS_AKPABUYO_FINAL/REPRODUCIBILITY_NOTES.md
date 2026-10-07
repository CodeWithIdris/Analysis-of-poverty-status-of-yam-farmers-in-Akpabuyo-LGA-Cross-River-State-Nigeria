# Methodological and Reproducibility Notes
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
$$\ell^*(&beta;) = \ell(&beta;) + \frac{1}{2} \ln |I(&beta;)|$$
where $I(&beta;) = X^T W X$ is the Fisher information matrix and $W = \operatorname{diag}(\pi_i (1 - \pi_i))$.
The modified score equations solved iteratively are:
$$U^*(&beta;) = X^T \left( y - \pi + h \odot (0.5 - \pi) \right) = 0$$
where $h_i = [X (X^T W X)^{-1} X^T W]_{ii}$ are the diagonal elements of the hat matrix.

#### 1.5 Confidence Interval Procedures
1. **Wald-type 95% Confidence Interval:**
   $$&beta;_j \pm 1.959964 \times \operatorname{SE}(&beta;_j) \implies \text{OR 95\% CI: } \left[ \exp(&beta;_j - 1.96 \cdot \text{SE}), \exp(&beta;_j + 1.96 \cdot \text{SE}) \right]$$
2. **Profile Penalized-Likelihood 95% Confidence Interval:**
   Inverting the penalized likelihood ratio test:
   $$\left\{ &beta;_j : 2 \left( \ell^*(&#946;) - \ell^*(&beta;_j, &#946;_{-j}(&beta;_j)) \right) \le \chi^2_{1, 0.95} = 3.841459 \right\}$$
   - For Credit Access: Profile 95% CI is $[-4.7388, -0.3546] \implies \text{OR} \in [0.0087, 0.7014]$.
   - For Farm Size: Profile 95% CI is $[-1.9780, 1.0837] \implies \text{OR} \in [0.1383, 2.9557]$.

#### 1.6 Mean Severity Index (MSI) for Challenges
$$\text{MSI} = \frac{\sum_{k=1}^5 f_k \cdot k}{\sum_{k=1}^5 f_k} = \frac{1(f_1) + 2(f_2) + 3(f_3) + 4(f_4) + 5(f_5)}{n}$$
- **Validated Categorization Scale:**
  - $1.00–1.80$: Not a Challenge
  - $1.81–2.60$: Minor Challenge
  - $2.61–3.40$: Moderate Challenge
  - $3.41–4.20$: Severe Challenge
  - $4.21–5.00$: Very Severe Challenge

---

### 2. Computational Software and Execution Environment
- **Platform:** Python 3.14 (Windows 64-bit environment)
- **Key Libraries:**
  - `pandas` (v2.3.3) for tabular data operations
  - `numpy` (v2.4.2) for numerical matrix algebra
  - `scipy` (v1.17.0) for exact non-parametric tests and optimization (`scipy.optimize.brentq`, `scipy.optimize.minimize`)
  - `statsmodels` (v0.14.6) for MLE logit and diagnostic comparisons
  - `openpyxl` (v3.1.5) for Excel XML generation with styling and formatting
- **Primary Script:** [`FULL_REANALYSIS_AKPABUYO_FINAL/scripts/master_analysis.py`](scripts/master_analysis.py)

---
**END OF REPRODUCIBILITY NOTES**
