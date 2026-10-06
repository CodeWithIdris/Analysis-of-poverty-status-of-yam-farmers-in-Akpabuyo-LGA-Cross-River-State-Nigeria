import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

cwd = os.getcwd()
target_dir = os.path.join(cwd, "AKPABUYO_YAM_FARMERS_FINAL_PROJECT")
os.makedirs(target_dir, exist_ok=True)

# Subfolders
folders = {
    "01_FINAL_THESIS": os.path.join(target_dir, "01_FINAL_THESIS"),
    "02_ANALYSIS_DOCUMENTS": os.path.join(target_dir, "02_ANALYSIS_DOCUMENTS"),
    "03_DATA_AND_STATISTICAL_FILES": os.path.join(target_dir, "03_DATA_AND_STATISTICAL_FILES"),
    "04_TABLES_AND_FIGURES": os.path.join(target_dir, "04_TABLES_AND_FIGURES"),
    "05_QUESTIONNAIRE_AND_INSTRUMENTS": os.path.join(target_dir, "05_QUESTIONNAIRE_AND_INSTRUMENTS"),
    "06_QC_AND_SUPPORTING_DOCUMENTS": os.path.join(target_dir, "06_QC_AND_SUPPORTING_DOCUMENTS")
}

for folder in folders.values():
    os.makedirs(folder, exist_ok=True)

# Define file copy mapping (src_path, dest_folder, dest_filename)
file_map = [
    # 01 FINAL THESIS
    (os.path.join(cwd, "FINAL_THESIS_FOUR_OBJECTIVES_AKPABUYO_FINAL.docx"), 
     folders["01_FINAL_THESIS"], "FINAL_THESIS_FOUR_OBJECTIVES_AKPABUYO_FINAL.docx"),

    # 02 ANALYSIS DOCUMENTS
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_3_Poverty_Status", "Analysis_3_Chapter_4_Results.docx"),
     folders["02_ANALYSIS_DOCUMENTS"], "ANALYSIS_OBJECTIVE_1_POVERTY_MEASUREMENT.docx"),
    (os.path.join(cwd, "Objective_2_Poverty_Status_Profile_Akpabuyo_FINAL.docx"),
     folders["02_ANALYSIS_DOCUMENTS"], "ANALYSIS_OBJECTIVE_2_POVERTY_STATUS_PROFILE.docx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_4_Factors_Poverty", "Analysis_4_Chapter_4_Results.docx"),
     folders["02_ANALYSIS_DOCUMENTS"], "ANALYSIS_OBJECTIVE_3_FACTORS_ASSOCIATED_WITH_POVERTY.docx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_5_Challenges", "Analysis_5_Chapter_4_Results.docx"),
     folders["02_ANALYSIS_DOCUMENTS"], "ANALYSIS_OBJECTIVE_4_CHALLENGES_MSI.docx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_1_Socio_Economic_Characteristics", "Analysis_1_Chapter_4_Results.docx"),
     folders["02_ANALYSIS_DOCUMENTS"], "ANALYSIS_SOCIOECONOMIC_CHARACTERISTICS.docx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_2_Household_Expenditure", "Analysis_2_Chapter_4_Results.docx"),
     folders["02_ANALYSIS_DOCUMENTS"], "ANALYSIS_HOUSEHOLD_EXPENDITURE.docx"),
    (os.path.join(cwd, "Chapter_4_Results_and_Discussion_FINAL_v2.docx"),
     folders["02_ANALYSIS_DOCUMENTS"], "CHAPTER_4_RESULTS_AND_DISCUSSION_FINAL.docx"),
    (os.path.join(cwd, "Statistical_Analysis_Appendix_Akpabuyo_Yam_Farmers_FINAL.docx"),
     folders["02_ANALYSIS_DOCUMENTS"], "STATISTICAL_ANALYSIS_APPENDIX_FINAL.docx"),
    (os.path.join(cwd, "Chapter_4_Objective_2_Integration_FINAL.docx"),
     folders["02_ANALYSIS_DOCUMENTS"], "CHAPTER_4_OBJECTIVE_2_INTEGRATION_REPORT.docx"),

    # 03 DATA AND STATISTICAL FILES
    (os.path.join(cwd, "raw_data.csv"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "raw_data.csv"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_1_Socio_Economic_Characteristics", "Table_4_1_Socio_Economic_Characteristics.xlsx"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "Table_4_1_Socio_Economic_Characteristics.xlsx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_1_Socio_Economic_Characteristics", "Table_4_2_Quantitative_Socio_Economic_Characteristics.xlsx"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "Table_4_2_Quantitative_Socio_Economic_Characteristics.xlsx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_2_Household_Expenditure", "Table_4_3_Monthly_Household_Expenditure.xlsx"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "Table_4_3_Monthly_Household_Expenditure.xlsx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_2_Household_Expenditure", "Table_4_4_Per_Capita_Expenditure.xlsx"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "Table_4_4_Per_Capita_Expenditure.xlsx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_2_Household_Expenditure", "Table_4_5_Expenditure_Composition.xlsx"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "Table_4_5_Expenditure_Composition.xlsx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_3_Poverty_Status", "Table_4_6_Poverty_Line_Determination.xlsx"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "Table_4_6_Poverty_Line_Determination.xlsx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_3_Poverty_Status", "Table_4_7_Poverty_Status_Distribution.xlsx"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "Table_4_7_Poverty_Status_Distribution.xlsx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_3_Poverty_Status", "Table_4_8_FGT_Poverty_Indices.xlsx"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "Table_4_8_FGT_Poverty_Indices.xlsx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_4_Factors_Poverty", "Table_4_9_Poverty_Status_by_Factors.xlsx"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "Table_4_9_Poverty_Status_by_Factors.xlsx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_4_Factors_Poverty", "Table_4_9_Objective_2_Extended.xlsx"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "Table_4_9_Objective_2_Extended.xlsx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_4_Factors_Poverty", "Table_4_10_Logistic_Regression_Factors_Poverty.xlsx"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "Table_4_10_Logistic_Regression_Factors_Poverty.xlsx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_5_Challenges", "Table_4_11_Challenge_Frequency_Distribution.xlsx"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "Table_4_11_Challenge_Frequency_Distribution.xlsx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_5_Challenges", "Table_4_11_Challenge_Severity_Ranking.xlsx"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "Table_4_11_Challenge_Severity_Ranking.xlsx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_4_Factors_Poverty", "Model_Validation_Diagnostic_Worksheet.xlsx"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "Model_Validation_Diagnostic_Worksheet.xlsx"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_5_Challenges", "Data_Validation_Diagnostic_Worksheet.xlsx"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "Data_Validation_Diagnostic_Worksheet.xlsx"),
    (os.path.join(cwd, "objective_2_poverty_profile.py"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "objective_2_poverty_profile.py"),
    (os.path.join(cwd, "statistical_analysis_appendix.py"),
     folders["03_DATA_AND_STATISTICAL_FILES"], "statistical_analysis_appendix.py"),

    # 04 TABLES AND FIGURES
    (os.path.join(cwd, "scratch", "Figure_2_1_Conceptual_Framework_Final.png"),
     folders["04_TABLES_AND_FIGURES"], "Figure_2_1_Conceptual_Framework_Final.png"),
    (os.path.join(cwd, "scratch", "orig_image2.png"),
     folders["04_TABLES_AND_FIGURES"], "Figure_3_1_Study_Area_Map.png"),
    (os.path.join(cwd, "scratch", "orig_image3.png"),
     folders["04_TABLES_AND_FIGURES"], "Figure_4_1_Poverty_Headcount_Distribution.png"),
    (os.path.join(cwd, "Figure_4_2_Mean_Monthly_Expenditure.png"),
     folders["04_TABLES_AND_FIGURES"], "Figure_4_2_Monthly_Household_Expenditure_Allocation.png"),
    (os.path.join(cwd, "Figure_4_3_Poverty_Status.png"),
     folders["04_TABLES_AND_FIGURES"], "Figure_4_3_Farm_Size_and_Yam_Area_by_Poverty_Status.png"),
    (os.path.join(cwd, "scratch", "orig_image7.png"),
     folders["04_TABLES_AND_FIGURES"], "Figure_4_4_Access_to_Institutional_Support_by_Poverty_Status.png"),
    (os.path.join(cwd, "Chapter_4_Analysis", "Analysis_5_Challenges", "Figure_4_5_Challenge_Severity_Ranking.png"),
     folders["04_TABLES_AND_FIGURES"], "Figure_4_5_Mean_Severity_Index_Challenges_Ranking.png"),

    # 05 QUESTIONNAIRE AND INSTRUMENTS
    (os.path.join(os.path.abspath(os.path.join(cwd, "..")), "questionnaire.docx"),
     folders["05_QUESTIONNAIRE_AND_INSTRUMENTS"], "QUESTIONNAIRE_FINAL.docx"),
    (os.path.join(os.path.abspath(os.path.join(cwd, "..")), "questionnaire.pdf"),
     folders["05_QUESTIONNAIRE_AND_INSTRUMENTS"], "QUESTIONNAIRE_FINAL.pdf"),
    (os.path.join(os.path.abspath(os.path.join(cwd, "..")), "MY QUESTIONNIAR(AutoRecovered)_095113.xls"),
     folders["05_QUESTIONNAIRE_AND_INSTRUMENTS"], "QUESTIONNAIRE_CODING_SHEET.xls"),
    (os.path.join(os.path.abspath(os.path.join(cwd, "..")), "DOC-20260903-WA0001.pdf"),
     folders["05_QUESTIONNAIRE_AND_INSTRUMENTS"], "RESEARCH_INSTRUMENT_SCAN.pdf"),

    # 06 QC AND SUPPORTING DOCUMENTS
    (os.path.join(cwd, "FINAL_THESIS_FINAL_QC_AUDIT.txt"),
     folders["06_QC_AND_SUPPORTING_DOCUMENTS"], "FINAL_THESIS_FINAL_QC_AUDIT.txt"),
    (os.path.join(cwd, "FINAL_THESIS_CORRECTION_AUDIT.txt"),
     folders["06_QC_AND_SUPPORTING_DOCUMENTS"], "FINAL_THESIS_CORRECTION_AUDIT.txt")
]

copied_count = 0
missing_count = 0

print(f"=== ORGANIZING FILES INTO: {target_dir} ===\n")
for src, dest_folder, dest_name in file_map:
    if os.path.exists(src):
        dest_path = os.path.join(dest_folder, dest_name)
        shutil.copy2(src, dest_path)
        rel_dest = os.path.relpath(dest_path, cwd)
        print(f"[COPIED] {os.path.basename(src)} -> {rel_dest}")
        copied_count += 1
    else:
        print(f"[MISSING SOURCE] {src}")
        missing_count += 1

print(f"\nSummary:")
print(f"Total files copied: {copied_count}")
print(f"Total missing files: {missing_count}")

