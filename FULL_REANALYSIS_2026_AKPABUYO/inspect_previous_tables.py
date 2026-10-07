import pandas as pd
import numpy as np

# Inspect previous tables in AKPABUYO_YAM_FARMERS_FINAL_PROJECT/03_DATA_AND_STATISTICAL_FILES
files = [
    'Table_4_1_Socio_Economic_Characteristics.xlsx',
    'Table_4_2_Quantitative_Socio_Economic_Characteristics.xlsx',
    'Table_4_3_Monthly_Household_Expenditure.xlsx',
    'Table_4_4_Per_Capita_Expenditure.xlsx',
    'Table_4_5_Expenditure_Composition.xlsx',
    'Table_4_6_Poverty_Line_Determination.xlsx',
    'Table_4_7_Poverty_Status_Distribution.xlsx',
    'Table_4_8_FGT_Poverty_Indices.xlsx',
    'Table_4_9_Objective_2_Extended.xlsx',
    'Table_4_10_Logistic_Regression_Factors_Poverty.xlsx',
    'Table_4_11_Challenge_Frequency_Distribution.xlsx',
    'Table_4_11_Challenge_Severity_Ranking.xlsx'
]

base_path = 'AKPABUYO_YAM_FARMERS_FINAL_PROJECT/03_DATA_AND_STATISTICAL_FILES/'
for f in files:
    try:
        df_t = pd.read_excel(base_path + f)
        print(f"=== {f} ===")
        print(df_t.to_string())
        print("\n")
    except Exception as e:
        print(f"Error reading {f}: {e}")

