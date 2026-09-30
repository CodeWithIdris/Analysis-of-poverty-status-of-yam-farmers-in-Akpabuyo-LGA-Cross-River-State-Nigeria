import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

df = pd.read_csv("raw_data.csv")

# Poverty Classification
pche = df['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE'] / df['HOUSE HOLD SIZE']
df['pche'] = pche
mean_pche = pche.mean()
poverty_line = (2.0 / 3.0) * mean_pche
df['is_poor'] = (pche < poverty_line).astype(int)

poor = df[df['is_poor'] == 1]
non_poor = df[df['is_poor'] == 0]

print(f"Total N = {len(df)}")
print(f"Mean PCHE = {mean_pche:.2f}")
print(f"Poverty line = {poverty_line:.2f}")
print(f"Poor N = {len(poor)} ({len(poor)/len(df)*100:.2f}%)")
print(f"Non-poor N = {len(non_poor)} ({len(non_poor)/len(df)*100:.2f}%)")

print("\n" + "="*50)
print("1. CONTINUOUS VARIABLES: AGE & HOUSEHOLD SIZE")
print("="*50)

for var_name, col in [("Age", "AGE"), ("Household size", "HOUSE HOLD SIZE")]:
    print(f"\n--- {var_name} ({col}) ---")
    p_s = poor[col]
    np_s = non_poor[col]
    all_s = df[col]
    
    print(f"Overall: Mean={all_s.mean():.2f} ± {all_s.std():.2f}, Median={all_s.median():.2f}, Min={all_s.min():.2f}, Max={all_s.max():.2f}")
    print(f"Poor:    Mean={p_s.mean():.2f} ± {p_s.std():.2f}, Median={p_s.median():.2f}, Min={p_s.min():.2f}, Max={p_s.max():.2f}")
    print(f"Non-poor:Mean={np_s.mean():.2f} ± {np_s.std():.2f}, Median={np_s.median():.2f}, Min={np_s.min():.2f}, Max={np_s.max():.2f}")
    
    # Normality tests (Shapiro-Wilk)
    sh_p = stats.shapiro(p_s)
    sh_np = stats.shapiro(np_s)
    print(f"Shapiro-Wilk: Poor p={sh_p.pvalue:.4f}, Non-poor p={sh_np.pvalue:.4f}")
    
    # Mann-Whitney U
    mwu = stats.mannwhitneyu(p_s, np_s)
    print(f"Mann-Whitney U = {mwu.statistic:.3f}, p = {mwu.pvalue:.4f}")
    
    # Independent t-test
    tt = stats.ttest_ind(p_s, np_s, equal_var=False)
    print(f"Welch t-test = {tt.statistic:.3f}, p = {tt.pvalue:.4f}")

print("\n" + "="*50)
print("2. CATEGORICAL VARIABLES: EDUCATION, CREDIT, TECH, COOP")
print("="*50)

# Check Education coding in raw data
print("\n--- Education (HIGHEST LEVEL OF EDUCATION) ---")
print("Unique values in raw data:", df['HIGHEST LEVEL OF EDUCATION'].value_counts(dropna=False))
# Let's see crosstab with poverty status
ct_edu = pd.crosstab(df['HIGHEST LEVEL OF EDUCATION'], df['is_poor'], margins=True)
print("Education vs Poverty status crosstab:")
print(ct_edu)

chi2_edu, p_edu, dof_edu, ex_edu = stats.chi2_contingency(pd.crosstab(df['HIGHEST LEVEL OF EDUCATION'], df['is_poor']))
print(f"Pearson Chi2 = {chi2_edu:.4f}, df = {dof_edu}, p = {p_edu:.4f}")
print("Expected frequencies:\n", ex_edu)

# Let's also check binary/ordered educational attainment if applicable
# Notice in Analysis 1, values: 0 = No formal (n=0 in raw?), 6 = Primary, 12 = Secondary, 16 = Tertiary
for val in sorted(df['HIGHEST LEVEL OF EDUCATION'].unique()):
    p_cnt = (poor['HIGHEST LEVEL OF EDUCATION'] == val).sum()
    np_cnt = (non_poor['HIGHEST LEVEL OF EDUCATION'] == val).sum()
    all_cnt = (df['HIGHEST LEVEL OF EDUCATION'] == val).sum()
    print(f"Level {val}: Poor={p_cnt} ({p_cnt/13*100:.1f}%), Non-poor={np_cnt} ({np_cnt/47*100:.1f}%), Overall={all_cnt} ({all_cnt/60*100:.1f}%)")

# Categorical variables in Section C & A
cat_vars = [
    ("Access to credit", "ACCESS TO CREDIT FOR YAM FARMING DURING LAST SEASON"),
    ("Improved yam varieties", "DO YOU USE IMPROVE YAM VARIETIES"),
    ("Fertilizer/manure application", "DO  YOU APPLY FERTILIZER OR MANURE ON YOUR YAM FARM"),
    ("Modern farm tools/tech", "DO YOU USE MODERN FARM TOOLS OR IMPROVED TECHNOLOGIES IN YAM PRODUCTION"),
    ("Cooperative membership", "MEMBER OF OOPERATIVE SOCIETY"),
    ("Agricultural extension", "ACCESS TO AGRICULTURAL EXTENSION")
]

for label, col in cat_vars:
    print(f"\n--- {label} ({col}) ---")
    ct = pd.crosstab(df[col], df['is_poor'], margins=True)
    print(ct)
    
    ct_no_margins = pd.crosstab(df[col], df['is_poor'])
    chi2, p_chi, dof, ex = stats.chi2_contingency(ct_no_margins)
    or_val, p_fish = stats.fisher_exact(ct_no_margins)
    
    p_yes = (poor[col] == 1).sum()
    np_yes = (non_poor[col] == 1).sum()
    all_yes = (df[col] == 1).sum()
    
    print(f"Poor Yes: {p_yes}/13 ({p_yes/13*100:.1f}%), Non-poor Yes: {np_yes}/47 ({np_yes/47*100:.1f}%), Overall Yes: {all_yes}/60 ({all_yes/60*100:.1f}%)")
    print(f"Chi2 = {chi2:.4f}, p = {p_chi:.4f} | Fisher p = {p_fish:.4f} | Min expected = {ex.min():.2f}")

