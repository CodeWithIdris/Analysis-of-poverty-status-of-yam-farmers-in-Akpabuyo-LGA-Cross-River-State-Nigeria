# -*- coding: utf-8 -*-
"""
Generate Complete Statistical Analysis Appendix Document (Final Targeted Correction Pass)
Study: Analysis of Poverty Status of Yam Farmers in Akpabuyo Local Government Area, Cross River State, Nigeria
Target Files:
1. Statistical_Analysis_Appendix_Akpabuyo_Yam_Farmers.docx
2. Statistical_Analysis_Appendix_Akpabuyo_Yam_Farmers_FINAL.docx
"""
import os
import csv
import math
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    
    # Top border
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single')
    top.set(qn('w:sz'), '12')
    top.set(qn('w:space'), '0')
    top.set(qn('w:color'), '000000')
    tblBorders.append(top)
    
    # Bottom border
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '12')
    bottom.set(qn('w:space'), '0')
    bottom.set(qn('w:color'), '000000')
    tblBorders.append(bottom)
    
    for side in ['left', 'right', 'insideV', 'insideH']:
        node = OxmlElement(f'w:{side}')
        node.set(qn('w:val'), 'none')
        tblBorders.append(node)
        
    tblPr.append(tblBorders)

def add_header_bottom_border(row):
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '8')
        bottom.set(qn('w:space'), '0')
        bottom.set(qn('w:color'), '000000')
        tcBorders.append(bottom)
        tcPr.append(tcBorders)

def format_cell(cell, text, align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, italic=False, font_size=10.5, font_name="Times New Roman"):
    cell.text = text
    set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    if len(p.runs) > 0:
        run = p.runs[0]
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = RGBColor(0, 0, 0)

def add_p(doc, text, space_after=6, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, font_size=12, font_name="Times New Roman"):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_mono_p(doc, text, space_after=2):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    if level == 1:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.bold = True
    elif level == 2:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
    elif level == 3:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_table_title(doc, title_text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(title_text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_table_note(doc, note_text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(note_text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10.5)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def create_appendix_doc():
    doc = Document()
    
    # Set default style to Times New Roman 12pt
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)
    
    # 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Title Page
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(72)
    p_title.paragraph_format.space_after = Pt(12)
    r1 = p_title.add_run("STATISTICAL ANALYSIS OUTPUT\n")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(18)
    r1.font.bold = True
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(12)
    p_sub.paragraph_format.space_after = Pt(24)
    r2 = p_sub.add_run("ANALYSIS OF POVERTY STATUS OF YAM FARMERS IN AKPABUYO LOCAL GOVERNMENT AREA, CROSS RIVER STATE, NIGERIA\n")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(13)
    r2.font.bold = True
    
    p_desc = doc.add_paragraph()
    p_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_desc.paragraph_format.space_before = Pt(36)
    p_desc.paragraph_format.space_after = Pt(100)
    r3 = p_desc.add_run("Prepared as a Statistical Analysis Appendix to the Dissertation\n\nDepartment of Agricultural Economics\nFaculty of Agriculture\nUniversity of Calabar, Calabar, Nigeria\n\nSeptember 2026")
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(12)
    r3.font.italic = False
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # APPENDIX 1: DATA VALIDATION AND VARIABLE CODING
    # -------------------------------------------------------------
    add_heading(doc, "APPENDIX 1: DATA VALIDATION AND VARIABLE CODING", level=1)
    
    add_p(doc, "This appendix details the dataset validation, screening results, and operational coding of all variables extracted from raw_data.csv for the 60 sampled yam-farming households in Akpabuyo Local Government Area.")
    
    add_table_title(doc, "Table A1.1: Dataset Screening and Quality Audit Summary")
    t_val = doc.add_table(rows=1, cols=3)
    t_val.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_val)
    
    h = t_val.rows[0].cells
    format_cell(h[0], "Diagnostic Check", bold=True)
    format_cell(h[1], "Screening Result", bold=True)
    format_cell(h[2], "Audit Status", bold=True)
    add_header_bottom_border(t_val.rows[0])
    
    diag_rows = [
        ("Source Dataset File", "raw_data.csv", "Verified"),
        ("Total Sample Size (N)", "60 farming households", "100.0% Complete"),
        ("Missing Values (Demographic & Budgetary)", "0 missing across all primary variables", "Validated"),
        ("Missing Values (Challenge Rating Scale)", "1 missing on item 9 (Prices, n = 59)", "Handled"),
        ("Duplicate Records", "0 duplicate respondent profiles", "Validated"),
        ("Impossible / Out-of-Range Values", "0 negative or invalid entries", "Validated"),
        ("Effective Sample Size for Analysis", "N = 60 valid observations", "Final Analytical N = 60")
    ]
    for row_data in diag_rows:
        r = t_val.add_row()
        format_cell(r.cells[0], row_data[0])
        format_cell(r.cells[1], row_data[1])
        format_cell(r.cells[2], row_data[2])
    add_table_note(doc, "Source: Field Survey Data Screening, 2026.")
    
    add_table_title(doc, "Table A1.2: Operational Variable Coding Dictionary")
    t_dict = doc.add_table(rows=1, cols=4)
    t_dict.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_dict)
    
    h_dict = t_dict.rows[0].cells
    format_cell(h_dict[0], "Variable Identifier", bold=True)
    format_cell(h_dict[1], "Variable Description", bold=True)
    format_cell(h_dict[2], "Data Type", bold=True)
    format_cell(h_dict[3], "Measurement Scale / Coding Rules", bold=True)
    add_header_bottom_border(t_dict.rows[0])
    
    dict_rows = [
        ("SEX", "Gender of farmer", "Categorical", "1 = Male (n = 36, 60.00%); 2/0 = Female (n = 24, 40.00%)"),
        ("AGE", "Farmer chronological age", "Continuous", "Years (Mean = 46.03, SD = 8.64, Range = 30 to 63)"),
        ("MARITAL STATUS", "Marital status", "Categorical", "Single (8.33%); Married (81.67%); Widowed (10.00%)"),
        ("EDUCATION", "Highest education completed", "Categorical", "Primary (30.00%); Secondary (45.00%); Tertiary (25.00%)"),
        ("HOUSE HOLD SIZE", "Number of household members", "Continuous", "Persons (Mean = 6.23, SD = 1.84, Range = 3 to 10)"),
        ("FARMING EXPERIENCE", "Yam farming duration", "Continuous", "Years (Mean = 18.88, SD = 8.56, Range = 6 to 40)"),
        ("OTHER INCOME", "Off-farm / non-farm income", "Binary", "1 = Yes (n = 49, 81.67%); 2/0 = No (n = 11, 18.33%)"),
        ("TOTAL EXPENDITURE", "Reported monthly expenditure", "Continuous", "₦/month (Mean = ₦115,837.50, Range = ₦45,000 to ₦223,500)"),
        ("PCHE", "Per-capita monthly expenditure", "Continuous", "₦/person/month: Total Expenditure / Household Size"),
        ("POVERTY STATUS", "Dependent variable", "Binary", "1 = Poor (PCHE < ₦13,526.02); 0 = Non-poor (PCHE ≥ ₦13,526.02)"),
        ("FARM SIZE", "Total land holdings", "Continuous", "Hectares (Mean = 2.43, SD = 0.79, Range = 1.0 to 4.5 ha)"),
        ("YAM AREA", "Area cultivated with yam", "Continuous", "Hectares (Mean = 1.67, SD = 0.53, Range = 0.8 to 3.0 ha)"),
        ("CREDIT ACCESS", "Access to agricultural credit", "Binary", "1 = Yes (n = 30, 50.00%); 2/0 = No (n = 30, 50.00%)"),
        ("EXTENSION CONTACT", "Extension agent visit in 12 mos", "Binary", "1 = Yes (n = 21, 35.00%); 2/0 = No (n = 39, 65.00%)"),
        ("COOPERATIVE", "Cooperative membership", "Binary", "1 = Yes (n = 49, 81.67%); 2/0 = No (n = 11, 18.33%)")
    ]
    for row_data in dict_rows:
        r = t_dict.add_row()
        format_cell(r.cells[0], row_data[0])
        format_cell(r.cells[1], row_data[1])
        format_cell(r.cells[2], row_data[2])
        format_cell(r.cells[3], row_data[3])
    add_table_note(doc, "Source: Field Survey Data Analysis Coding, 2026.")

    # -------------------------------------------------------------
    # APPENDIX 2: FOSTER-GREER-THORBECKE (FGT) POVERTY INDICES
    # -------------------------------------------------------------
    add_heading(doc, "APPENDIX 2: FOSTER-GREER-THORBECKE (FGT) POVERTY INDICES", level=1)
    
    add_p(doc, "Poverty indices were estimated using the Foster, Greer, and Thorbecke (FGT, 1984) class of decomposable poverty measures across the entire sample and disaggregated by gender group. The poverty threshold (z) was set at two-thirds (2/3) of the mean Per-Capita Monthly Household Expenditure (z = ₦13,526.02).")
    
    add_heading(doc, "2.1 Overall Population FGT Poverty Indices", level=2)
    add_table_title(doc, "Table A2.1: Overall FGT Poverty Indices for Yam Farmers (N = 60)")
    t_fgt_ov = doc.add_table(rows=1, cols=6)
    t_fgt_ov.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_fgt_ov)
    
    h_f = t_fgt_ov.rows[0].cells
    format_cell(h_f[0], "FGT Metric", bold=True)
    format_cell(h_f[1], "Alpha (α)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_f[2], "Estimate", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_f[3], "Standard Error (STE)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_f[4], "95% Conf. Interval", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_f[5], "Poverty Line (z)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(t_fgt_ov.rows[0])
    
    fgt_ov_data = [
        ("Poverty Headcount Index (P0)", "0.00", "0.2167", "0.0536", "[0.1115, 0.3218]", "₦13,526.02"),
        ("Poverty Gap Index (P1)", "1.00", "0.0232", "0.0070", "[0.0095, 0.0368]", "₦13,526.02"),
        ("Squared Poverty Gap / Severity (P2)", "2.00", "0.0034", "0.0012", "[0.0011, 0.0057]", "₦13,526.02")
    ]
    for row_data in fgt_ov_data:
        r = t_fgt_ov.add_row()
        format_cell(r.cells[0], row_data[0])
        format_cell(r.cells[1], row_data[1], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[2], row_data[2], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[3], row_data[3], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[4], row_data[4], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[5], row_data[5], align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_table_note(doc, "Source: Field Survey Data Analysis, 2026. Standard errors (STE) are estimated via the sample standard error of the mean applied to individual respondent-level FGT normalized poverty shortfall weights w_i = [(z - y_i)/z]^α * I(y_i < z): STE(P_α) = s_w / sqrt(n), where s_w = sqrt[ Σ (w_i - P_α)^2 / (n - 1) ]. 95% confidence intervals are given by [max(0.0000, P_α - 1.96 * STE), P_α + 1.96 * STE].")
    
    add_heading(doc, "2.2 FGT Poverty Indices Disaggregated by Gender", level=2)
    add_p(doc, "The output format below presents subgroup decompositions by respondent gender (Group 1 = Male, n = 36; Group 2 = Female, n = 24) across the three FGT alpha parameters (α = 0.00, 1.00, 2.00). Standard errors (STE) and 95% confidence intervals are computed directly from the respondent-level observations using the sample standard error of the mean for individual normalized poverty shortfalls w_i = [(z - y_i)/z]^α * I(y_i < z), where STE(P_α) = s_w / sqrt(n), s_w is the sample standard deviation of w_i, and the 95% Wald confidence bounds are [max(0.0000, P_α - 1.96 * STE), P_α + 1.96 * STE].")
    
    add_table_title(doc, "Table A2.2: FGT Poverty Indices by Gender Group (alpha = 0.00, 1.00, 2.00)")
    t_fgt_g = doc.add_table(rows=1, cols=6)
    t_fgt_g.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_fgt_g)
    
    h_fg = t_fgt_g.rows[0].cells
    format_cell(h_fg[0], "Group Variable: Gender", bold=True)
    format_cell(h_fg[1], "Estimate", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_fg[2], "STE", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_fg[3], "LB", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_fg[4], "UB", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_fg[5], "Pov. Line", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(t_fgt_g.rows[0])
    
    g_data = [
        # alpha = 0
        ("Parameter alpha: 0.00 (Poverty Incidence)", "", "", "", "", ""),
        ("  Male (Group 1, n = 36)", "0.2778", "0.0757", "0.1294", "0.4262", "13526.02"),
        ("  Female (Group 2, n = 24)", "0.1250", "0.0690", "0.0000", "0.2602", "13526.02"),
        ("  Population (Overall, N = 60)", "0.2167", "0.0536", "0.1115", "0.3218", "13526.02"),
        # alpha = 1
        ("Parameter alpha: 1.00 (Poverty Depth)", "", "", "", "", ""),
        ("  Male (Group 1, n = 36)", "0.0293", "0.0096", "0.0105", "0.0481", "13526.02"),
        ("  Female (Group 2, n = 24)", "0.0140", "0.0098", "0.0000", "0.0331", "13526.02"),
        ("  Population (Overall, N = 60)", "0.0232", "0.0070", "0.0095", "0.0368", "13526.02"),
        # alpha = 2
        ("Parameter alpha: 2.00 (Poverty Severity)", "", "", "", "", ""),
        ("  Male (Group 1, n = 36)", "0.0041", "0.0015", "0.0011", "0.0071", "13526.02"),
        ("  Female (Group 2, n = 24)", "0.0024", "0.0018", "0.0000", "0.0059", "13526.02"),
        ("  Population (Overall, N = 60)", "0.0034", "0.0012", "0.0011", "0.0057", "13526.02"),
    ]
    for row_data in g_data:
        r = t_fgt_g.add_row()
        is_subhdr = (row_data[1] == "")
        format_cell(r.cells[0], row_data[0], bold=is_subhdr)
        format_cell(r.cells[1], row_data[1], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_subhdr)
        format_cell(r.cells[2], row_data[2], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_subhdr)
        format_cell(r.cells[3], row_data[3], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_subhdr)
        format_cell(r.cells[4], row_data[4], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_subhdr)
        format_cell(r.cells[5], row_data[5], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_subhdr)
    add_table_note(doc, "Source: Field Survey Data Analysis, 2026. STE = Standard error of the subgroup sample mean (s_w / sqrt(n)); LB = Lower bound of 95% Wald confidence interval (truncated at 0.0000); UB = Upper bound of 95% Wald confidence interval; Pov. Line = ₦13,526.02.")

    # -------------------------------------------------------------
    # APPENDIX 3: BIVARIATE ANALYSIS OF FACTORS ASSOCIATED WITH POVERTY
    # -------------------------------------------------------------
    add_heading(doc, "APPENDIX 3: BIVARIATE STATISTICAL ANALYSIS", level=1)
    
    add_p(doc, "Bivariate statistical tests were conducted to examine differences between poor (n = 13) and non-poor (n = 47) households across demographic, human capital, farm asset, and institutional variables. Non-parametric Mann-Whitney U tests were employed for continuous variables, while Pearson's Chi-square tests (or Fisher's exact tests for 2×2 sparse tables) were used for categorical variables.")
    
    add_table_title(doc, "Table A3.1: Detailed Bivariate Statistical Test Outputs")
    t_biv = doc.add_table(rows=1, cols=6)
    t_biv.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_biv)
    
    h_b = t_biv.rows[0].cells
    format_cell(h_b[0], "Explanatory Variable", bold=True)
    format_cell(h_b[1], "Poor (n = 13)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_b[2], "Non-Poor (n = 47)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_b[3], "Overall (N = 60)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_b[4], "Statistical Test", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_b[5], "p-value", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(t_biv.rows[0])
    
    biv_data = [
        ("A. Demographic & Human Capital", "", "", "", "", ""),
        ("  Age of farmer (years)", "51.31 ± 8.99", "44.57 ± 8.04", "46.03 ± 8.64", "Mann-Whitney U = 432.00", "0.024*"),
        ("  Household size (persons)", "8.31 ± 1.70", "5.66 ± 1.43", "6.23 ± 1.84", "Mann-Whitney U = 536.00", "< 0.001*"),
        ("  Educational attainment", "", "", "", "Pearson Chi2(2) = 2.673", "0.263"),
        ("    Primary education (6 yrs)", "5 (38.5%)", "13 (27.7%)", "18 (30.0%)", "—", "—"),
        ("    Secondary education (12 yrs)", "7 (53.8%)", "20 (42.6%)", "27 (45.0%)", "—", "—"),
        ("    Tertiary education (16 yrs)", "1 (7.7%)", "14 (29.8%)", "15 (25.0%)", "—", "—"),
        ("B. Land Assets & Production Scale", "", "", "", "", ""),
        ("  Total farm size (ha)", "1.98 ± 0.48", "2.56 ± 0.82", "2.43 ± 0.79", "Mann-Whitney U = 170.50", "0.016*"),
        ("  Yam cultivated area (ha)", "1.43 ± 0.37", "1.73 ± 0.56", "1.67 ± 0.53", "Mann-Whitney U = 205.00", "0.072"),
        ("C. Institutional Access & Modern Inputs", "", "", "", "", ""),
        ("  Access to credit (Yes = 1)", "1 (7.7%)", "29 (61.7%)", "30 (50.0%)", "Pearson Chi2(1) = 9.820", "0.002*"),
        ("  Extension contact in 12 mos (Yes)", "0 (0.0%)", "21 (44.7%)", "21 (35.0%)", "Fisher's exact test", "0.002*"),
        ("  Improved yam varieties (Yes)", "0 (0.0%)", "2 (4.3%)", "2 (3.3%)", "Fisher's exact test", "1.000"),
        ("  Fertilizer / manure use (Yes)", "9 (69.2%)", "39 (83.0%)", "48 (80.0%)", "Pearson Chi2(1) = 0.497", "0.481"),
        ("  Modern tools / tech (Yes)", "0 (0.0%)", "6 (12.8%)", "6 (10.0%)", "Fisher's exact test", "0.324"),
        ("  Cooperative membership (Yes)", "10 (76.9%)", "39 (83.0%)", "49 (81.7%)", "Pearson Chi2(1) = 0.009", "0.925")
    ]
    for row_data in biv_data:
        r = t_biv.add_row()
        is_sub = (row_data[1] == "" and row_data[2] == "" and row_data[3] == "")
        format_cell(r.cells[0], row_data[0], bold=is_sub)
        format_cell(r.cells[1], row_data[1], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_sub)
        format_cell(r.cells[2], row_data[2], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_sub)
        format_cell(r.cells[3], row_data[3], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_sub)
        format_cell(r.cells[4], row_data[4], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_sub)
        format_cell(r.cells[5], row_data[5], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_sub)
    add_table_note(doc, "Source: Field Survey Data Analysis, 2026. * Significant at p < 0.05.\nMethodological Note: Household size is the denominator in per-capita expenditure calculation, creating a mechanical negative relationship with PCHE.")

    # -------------------------------------------------------------
    # APPENDIX 4: RESULTS OF LOGISTIC REGRESSION
    # -------------------------------------------------------------
    add_heading(doc, "APPENDIX 4: RESULTS OF LOGISTIC REGRESSION", level=1)
    
    add_p(doc, "This appendix presents the logistic regression outputs evaluating factors associated with household poverty status (1 = Poor, 0 = Non-poor). Section 4.1 documents the exploratory assessment of the candidate predictor set and discusses model diagnostics, while Section 4.2 presents the final parsimonious multivariable logistic regression model.")
    
    add_heading(doc, "4.1 Exploratory Model Evaluation and Sparsity Assessment", level=2)
    add_p(doc, "Prior to finalizing the empirical specification, candidate predictors were evaluated for events-per-variable (EPV) suitability and cell sparsity. In a sample of N = 60 with 13 events of interest (poor households), fitting an unconstrained 9-variable multivariable model yields an EPV ratio of 1.44 (substantially below the standard econometric rule-of-thumb of 10–15 EPV). Furthermore, three institutional/technology covariates exhibited zero-cell frequencies among the poor (0 of 13 poor had extension contact, 0 of 13 used improved varieties, and 0 of 13 used modern tools), creating quasi-complete separation, infinite standard errors, and unstable odds ratios in unpenalized maximum likelihood estimation. Consequently, the final model was restricted to two defensible predictors: total farm size and access to credit.")
    
    add_heading(doc, "4.2 Final Parsimonious Binary Logistic Regression Model", level=2)
    add_p(doc, "The tables below present the software-style statistical output for the final parsimonious logistic regression model.")
    
    add_mono_p(doc, "Logistic regression                               Number of obs   =         60")
    add_mono_p(doc, "                                                  LR chi2(2)      =      13.86")
    add_mono_p(doc, "                                                  Prob > chi2     =     0.0010")
    add_mono_p(doc, "Log likelihood = -24.71887                        Pseudo R2 (Nag) =     0.3181")
    
    add_table_title(doc, "Table A4.1: Logistic Regression Parameter Estimates (Log-Odds Coefficients)")
    t_coef = doc.add_table(rows=1, cols=6)
    t_coef.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_coef)
    
    h_c = t_coef.rows[0].cells
    format_cell(h_c[0], "Poverty Status", bold=True)
    format_cell(h_c[1], "Coef.", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_c[2], "Std. Err.", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_c[3], "z", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_c[4], "P>|z|", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_c[5], "[95% Conf. Interval]", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(t_coef.rows[0])
    
    coef_rows = [
        ("Total farm size (ha)", "-0.4300", "0.8149", "-0.53", "0.598", "[-2.0272,  1.1672]"),
        ("Access to credit (Yes = 1)", "-2.5983", "1.2450", "-2.09", "0.037*", "[-5.0384, -0.1582]"),
        ("_cons (Constant)", "0.4331", "1.6280", "0.27", "0.790", "[-2.7577,  3.6239]")
    ]
    for row_data in coef_rows:
        r = t_coef.add_row()
        format_cell(r.cells[0], row_data[0])
        format_cell(r.cells[1], row_data[1], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[2], row_data[2], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[3], row_data[3], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[4], row_data[4], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[5], row_data[5], align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_table_note(doc, "Source: Field Survey Data Analysis, 2026. * Statistically significant at p < 0.05.")
    
    add_table_title(doc, "Table A4.2: Logistic Regression Odds Ratio Estimates")
    t_or = doc.add_table(rows=1, cols=6)
    t_or.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_or)
    
    h_or = t_or.rows[0].cells
    format_cell(h_or[0], "Poverty Status", bold=True)
    format_cell(h_or[1], "Odds Ratio", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_or[2], "Std. Err.", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_or[3], "z", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_or[4], "P>|z|", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_or[5], "[95% Conf. Interval]", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(t_or.rows[0])
    
    or_rows = [
        ("Total farm size (ha)", "0.6505", "0.5301", "-0.53", "0.598", "[0.1317,  3.2130]"),
        ("Access to credit (Yes = 1)", "0.0744", "0.0926", "-2.09", "0.037*", "[0.0065,  0.8537]"),
        ("_cons (Constant)", "1.5420", "2.5104", "0.27", "0.790", "[0.0634, 37.4834]")
    ]
    for row_data in or_rows:
        r = t_or.add_row()
        format_cell(r.cells[0], row_data[0])
        format_cell(r.cells[1], row_data[1], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[2], row_data[2], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[3], row_data[3], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[4], row_data[4], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[5], row_data[5], align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_table_note(doc, "Source: Field Survey Data Analysis, 2026. * Statistically significant at p < 0.05.")
    
    add_heading(doc, "4.3 Firth Penalized Likelihood Logistic Regression Sensitivity Analysis", level=2)
    add_p(doc, "To verify that the small-sample event rate (13 poor events) did not induce small-sample bias in maximum likelihood estimation, a Firth penalized likelihood logistic regression sensitivity analysis was conducted. The Firth penalized estimate for access to credit yielded OR = 0.110 (95% CI: 0.014–0.891, p = 0.039), confirming the robustness and statistical significance of the protective association between credit access and household non-poor status.")

    # -------------------------------------------------------------
    # APPENDIX 5: MODEL DIAGNOSTICS AND CLASSIFICATION PERFORMANCE
    # -------------------------------------------------------------
    add_heading(doc, "APPENDIX 5: MODEL DIAGNOSTICS AND CLASSIFICATION PERFORMANCE", level=1)
    
    add_p(doc, "Model goodness-of-fit and predictive discrimination were evaluated for the final parsimonious logistic regression model.")
    
    add_table_title(doc, "Table A5.1: Model Diagnostics Summary")
    t_diag = doc.add_table(rows=1, cols=3)
    t_diag.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_diag)
    
    h_d = t_diag.rows[0].cells
    format_cell(h_d[0], "Diagnostic Metric", bold=True)
    format_cell(h_d[1], "Computed Value", bold=True)
    format_cell(h_d[2], "Statistical Interpretation", bold=True)
    add_header_bottom_border(t_diag.rows[0])
    
    # Corrected Nagelkerke interpretation (no claim of explaining 31.81% of variation)
    diag_summary_rows = [
        ("Likelihood Ratio Chi-Square (LR χ²)", "13.861 (df = 2)", "Model statistically significant over null (p = 0.000978)"),
        ("Nagelkerke Pseudo-R²", "0.3181", "Nagelkerke R² = 0.3181, indicating the model’s relative explanatory performance based on the Nagelkerke pseudo-R² measure."),
        ("Cox & Snell Pseudo-R²", "0.2063", "Generalized coefficient of determination"),
        ("Log-Likelihood (Fitted Model)", "-24.719", "Log-likelihood value at convergence"),
        ("Log-Likelihood (Null Intercept Model)", "-31.650", "Log-likelihood of intercept-only baseline model"),
        ("Akaike Information Criterion (AIC)", "55.438", "Information criteria for model selection")
    ]
    for row_data in diag_summary_rows:
        r = t_diag.add_row()
        format_cell(r.cells[0], row_data[0])
        format_cell(r.cells[1], row_data[1])
        format_cell(r.cells[2], row_data[2])
    add_table_note(doc, "Source: Field Survey Data Analysis, 2026.")
    
    add_table_title(doc, "Table A5.2: Classification Matrix at Decision Cutoff Probability = 0.25")
    t_class = doc.add_table(rows=1, cols=4)
    t_class.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_class)
    
    h_cl = t_class.rows[0].cells
    format_cell(h_cl[0], "Observed Status", bold=True)
    format_cell(h_cl[1], "Predicted Non-Poor", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_cl[2], "Predicted Poor", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h_cl[3], "Class Accuracy (%)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(t_class.rows[0])
    
    class_rows = [
        ("Observed Non-Poor (n = 47)", "37 (True Negatives)", "10 (False Positives)", "Specificity = 78.72%"),
        ("Observed Poor (n = 13)", "5 (False Negatives)", "8 (True Positives)", "Sensitivity = 61.54%"),
        ("Total (N = 60)", "42", "18", "Overall Accuracy = 75.00%")
    ]
    for row_data in class_rows:
        r = t_class.add_row()
        format_cell(r.cells[0], row_data[0])
        format_cell(r.cells[1], row_data[1], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[2], row_data[2], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[3], row_data[3], align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_table_note(doc, "Source: Field Survey Data Analysis, 2026. Balanced Accuracy = (Sensitivity + Specificity) / 2 = 70.13%. Decision threshold calibrated to sample base rate (~0.217).")

    # -------------------------------------------------------------
    # APPENDIX 6: STATISTICAL METHODOLOGY NOTES
    # -------------------------------------------------------------
    add_heading(doc, "APPENDIX 6: STATISTICAL METHODOLOGY NOTES", level=1)
    
    notes = [
        ("1. Poverty Line Construction", "Poverty status was determined following the relative poverty line methodology. Per-Capita Monthly Household Expenditure (PCHE) was computed as total reported monthly expenditure divided by household size. The relative poverty threshold (z) was set at exactly two-thirds (2/3) of the sample mean PCHE: z = (2/3) × ₦20,289.03 = ₦13,526.02 per person per month. Households with PCHE < ₦13,526.02 were categorized as poor (n = 13, 21.67%), and those with PCHE ≥ ₦13,526.02 were categorized as non-poor (n = 47, 78.33%)."),
        ("2. FGT Index Estimation & Standard Error Variance Formulation", "The Foster-Greer-Thorbecke (1984) poverty indices P_α = (1/n) * Σ w_i were estimated for α = 0 (headcount ratio), α = 1 (poverty gap index), and α = 2 (poverty severity index), where w_i = [(z - y_i)/z]^α * I(y_i < z) represents the individual normalized poverty shortfall weight for household i at poverty line z = ₦13,526.02. Standard errors (STE) are computed directly from the respondent-level observations using the sample standard error of the mean: STE(P_α) = s_w / sqrt(n), where s_w = sqrt[ Σ (w_i - P_α)^2 / (n - 1) ]. The 95% confidence intervals are constructed using asymptotic normal bounds as [max(0.0000, P_α - 1.96 * STE), P_α + 1.96 * STE]. For simple random samples with a predetermined poverty line, this analytical formulation is mathematically equivalent to the Taylor linearization survey variance estimator implemented in standard econometric poverty routines."),
        ("3. Mechanical Denominator Property of Household Size", "Because household size appears directly in the denominator of the PCHE welfare metric (PCHE = Expenditure / Household Size), larger households mathematically yield lower per-capita expenditure holding total spending constant. The observed statistical association between household size and poverty status must therefore be interpreted recognizing this arithmetic property alongside real dependency burdens."),
        ("4. Events-Per-Variable (EPV) and Model Specification", "In logistic regression, small event counts relative to the number of parameters risk overfitting and severe bias. With 13 poor events in the sample, standard epidemiological and econometric guidelines restrict multivariable estimation to 1–2 key predictors. A parsimonious model retaining Total Farm Size (physical asset) and Access to Credit (institutional liquidity) was specified and verified via Firth penalized likelihood estimation."),
        ("5. Cross-Sectional Associational Interpretation", "Because the survey utilized a cross-sectional observational design, all reported regression odds ratios and bivariate test statistics reflect empirical statistical associations rather than direct causal effects.")
    ]
    
    for title_text, body_text in notes:
        add_heading(doc, title_text, level=2)
        add_p(doc, body_text)
        
    out_file1 = "Statistical_Analysis_Appendix_Akpabuyo_Yam_Farmers.docx"
    out_file2 = "Statistical_Analysis_Appendix_Akpabuyo_Yam_Farmers_FINAL.docx"
    doc.save(out_file1)
    doc.save(out_file2)
    print(f"Successfully generated and saved:\n1. {out_file1}\n2. {out_file2}")

if __name__ == "__main__":
    create_appendix_doc()
