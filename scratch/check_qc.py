import docx
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document('FINAL_THESIS_FOUR_OBJECTIVES_AKPABUYO_FINAL.docx')
full_text = '\n'.join([p.text for p in doc.paragraphs])
table_text = '\n'.join(['\t'.join([c.text.strip() for c in row.cells]) for t in doc.tables for row in t.rows])
combined = full_text + '\n' + table_text

print("=== CHECKING CONCEPTUAL FRAMEWORK (SECTION A) ===")
# Check for unmeasured variables
unmeasured = [
    'Multidimensional Poverty Profile',
    'Yam Tuber Output & Marketed Surplus',
    'Farm & Non-Farm Income Generation',
]
for item in unmeasured:
    count = len(re.findall(re.escape(item), full_text, re.IGNORECASE))
    print(f"Unmeasured item '{item}': {count} occurrences")

# Check required conceptual framework terms
cf_terms = [
    'POVERTY STATUS',
    'HOUSEHOLD WELFARE MEASURE',
    'Figure 2.1: Conceptual Framework',
    'Relative poverty line',
    'Foster-Greer-Thorbecke',
    'P0', 'P1', 'P2'
]
for item in cf_terms:
    count = len(re.findall(re.escape(item), combined))
    print(f"Required term '{item}': {count} occurrences")

print("\n=== CHECKING EMPIRICAL RESULTS (SECTION B) ===")
empirical_checks = [
    ('Sample size N=60', '60'),
    ('Poor n=13', '13'),
    ('Non-poor n=47', '47'),
    ('Poor percentage 21.67%', '21.67%'),
    ('Non-poor percentage 78.33%', '78.33%'),
    ('Mean PCHE ₦20,289.03', '20,289.03'),
    ('Poverty line ₦13,526.02', '13,526.02'),
    ('P0 = 0.2167', '0.2167'),
    ('P1 = 0.0232', '0.0232'),
    ('P2 = 0.0034', '0.0034'),
    ('Reported total expenditure ₦115,837.50', '115,837.50'),
    ('Sum of components ₦113,985.83', '113,985.83'),
    ('Poor total monthly exp ₦101,000.00', '101,000.00'),
    ('Non-poor total monthly exp ₦119,941.49', '119,941.49'),
    ('Poor PCHE ₦12,079.49', '12,079.49'),
    ('Non-poor PCHE ₦22,559.76', '22,559.76'),
    ('Logistic Total farm size OR=0.6505', '0.6505'),
    ('Logistic Total farm size p=0.5979', '0.5979'),
    ('Logistic Credit OR=0.0744', '0.0744'),
    ('Logistic Credit p=0.0369', '0.0369'),
    ('LR chi2 = 13.861', '13.861'),
    ('LR p-value = 0.000978', '0.000978'),
    ('Nagelkerke R2 = 0.3181', '0.3181'),
    ('Log likelihood = -24.719', '-24.719'),
    ('Firth sensitivity Credit OR=0.110', '0.110'),
    ('Firth 95% CI 0.014–0.891', '0.014'),
    ('Firth p=0.039', '0.039'),
    ('Labour MSI = 4.15', '4.15'),
    ('Inputs MSI = 4.00', '4.00'),
    ('Storage MSI = 3.88', '3.88'),
    ('Climate MSI = 3.70', '3.70'),
    ('Stakes MSI = 3.57', '3.57'),
    ('Credit challenge MSI = 3.53', '3.53'),
    ('Extension challenge MSI = 3.52', '3.52'),
    ('Pest/disease MSI = 3.38', '3.38'),
    ('Prices MSI = 3.12', '3.12'),
    ('Market access MSI = 2.90', '2.90')
]

for label, val in empirical_checks:
    found = val in combined
    print(f"[{'PASS' if found else 'FAIL'}] {label} (found: {found})")

print("\n=== CHECKING OBJECTIVE ALIGNMENT & CAUSAL LANGUAGE (SECTION C & D) ===")
# Check objective II in abstract and 4.4 and 5.1 has no inferential statistics (t=, p=, chi-square in obj 2)
abstract_start = full_text.find("ABSTRACT")
abstract_end = full_text.find("CHAPTER ONE")
abstract_text = full_text[abstract_start:abstract_end] if abstract_start != -1 else ""

print("Abstract length:", len(abstract_text))
print("Abstract contains 'Mann-Whitney':", "Mann-Whitney" in abstract_text)
print("Abstract contains 'chi-square' in Obj II:", "chi-square" in abstract_text.split("Objective II")[0] if "Objective II" in abstract_text else False)

# Check causal wording
causal_prohibitions = [
    r'\bcaused poverty\b',
    r'\bcauses poverty\b',
    r'\bled to poverty\b',
    r'\bresulted in poverty\b',
    r'\breduced poverty\b',
    r'\bincreased poverty\b',
    r'\bprevented poverty\b'
]
for pat in causal_prohibitions:
    m = re.findall(pat, full_text, re.IGNORECASE)
    print(f"Pattern '{pat}': {len(m)} occurrences")

print("\n=== CHECKING TABLES & FIGURES (SECTION E) ===")
for t_num in range(1, 11):
    t_name = f"Table 4.{t_num}"
    found = t_name in combined
    print(f"[{'PASS' if found else 'FAIL'}] {t_name} present")

for f_name in ["Figure 2.1", "Figure 3.1", "Figure 4.1", "Figure 4.2", "Figure 4.3", "Figure 4.4", "Figure 4.5"]:
    found = f_name in combined
    print(f"[{'PASS' if found else 'FAIL'}] {f_name} present")

