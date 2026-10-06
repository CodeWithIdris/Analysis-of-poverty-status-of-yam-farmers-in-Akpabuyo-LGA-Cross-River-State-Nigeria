# -*- coding: utf-8 -*-
"""
Generate Dedicated Objective 2 Document and Integrated Chapter 4 Document
Project: Analysis of Poverty Status of Yam Farmers in Akpabuyo Local Government Area, Cross River State, Nigeria
Specific Objective II: Analyze poverty status of yam farmers in the study area (Poverty Status Profile)
"""

import os
import sys
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

# -----------------------------------------------------------------------------
# 1. BUILD DEDICATED OBJECTIVE 2 DOCUMENT
# -----------------------------------------------------------------------------
def build_objective_2_standalone():
    doc = Document()
    
    # 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Title Block
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(36)
    p_title.paragraph_format.space_after = Pt(12)
    r1 = p_title.add_run("OBJECTIVE 2: POVERTY STATUS PROFILE OF YAM FARMERS\n")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(16)
    r1.font.bold = True
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(6)
    p_sub.paragraph_format.space_after = Pt(18)
    r2 = p_sub.add_run("Study: Analysis of Poverty Status of Yam Farmers in Akpabuyo Local Government Area, Cross River State, Nigeria\n")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    r2.font.bold = True
    
    p_desc = doc.add_paragraph()
    p_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_desc.paragraph_format.space_before = Pt(6)
    p_desc.paragraph_format.space_after = Pt(24)
    r3 = p_desc.add_run("Department of Agricultural Economics, University of Calabar, Calabar, Nigeria\nSeptember 2026")
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(11)
    
    # Overview & Framework
    add_heading(doc, "1. Methodological Operationalization of Objective II", level=1)
    add_p(doc, "Specific Objective II of this study is to analyze the poverty status of yam farmers in Akpabuyo Local Government Area. In agricultural economics and welfare analysis, this objective is operationalized through a descriptive Poverty Status Profile. While Objective I establishes the formal measurement of poverty via the relative poverty line and Foster-Greer-Thorbecke (FGT) indices, and Objective III conducts inferential hypothesis testing and multivariable econometric modeling of poverty drivers, Objective II bridges measurement and econometric modeling by detailing what the poverty status of yam farmers looks like across their demographic, human capital, farm asset, and institutional characteristics.")
    add_p(doc, "The profile is constructed using the validated respondent-level dataset of N = 60 yam-farming households from raw_data.csv. Per-Capita Monthly Household Expenditure (PCHE) was computed by dividing total monthly household expenditure by household size. Based on the established relative poverty line of two-thirds of the mean PCHE (z = ₦13,526.02 per person per month), 13 households (21.67%) were classified as poor (PCHE < ₦13,526.02), while 47 households (78.33%) were classified as non-poor (PCHE ≥ ₦13,526.02). The profile systematically compares these two welfare groups across all operational variables.")

    # Table 1: Categorical Socioeconomic and Farm Profile
    add_heading(doc, "2. Socioeconomic and Institutional Characteristics by Poverty Status", level=1)
    add_p(doc, "Table 1 profiles the categorical demographic, educational, and institutional characteristics of the sampled yam farmers disaggregated by poverty status.")
    
    add_table_title(doc, "Table 1: Distribution of Yam Farmers by Poverty Status and Socioeconomic Characteristics")
    t1 = doc.add_table(rows=1, cols=7)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t1)
    
    h1 = t1.rows[0].cells
    format_cell(h1[0], "Socioeconomic Variable", bold=True)
    format_cell(h1[1], "Category", bold=True)
    format_cell(h1[2], "Poor (n = 13)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h1[3], "Poor (%)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h1[4], "Non-Poor (n = 47)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h1[5], "Non-Poor (%)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h1[6], "Total (N = 60)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(t1.rows[0])
    
    t1_data = [
        ("Sex", "Male", "10", "76.92%", "26", "55.32%", "36 (60.00%)"),
        ("", "Female", "3", "23.08%", "21", "44.68%", "24 (40.00%)"),
        ("Marital Status", "Single", "1", "7.69%", "4", "8.51%", "5 (8.33%)"),
        ("", "Married", "10", "76.92%", "39", "82.98%", "49 (81.67%)"),
        ("", "Widowed", "2", "15.38%", "4", "8.51%", "6 (10.00%)"),
        ("Educational Attainment", "Primary education (6 yrs)", "5", "38.46%", "13", "27.66%", "18 (30.00%)"),
        ("", "Secondary education (12 yrs)", "7", "53.85%", "20", "42.55%", "27 (45.00%)"),
        ("", "Tertiary education (16 yrs)", "1", "7.69%", "14", "29.79%", "15 (25.00%)"),
        ("Other Income Source", "Yes (Off-farm income)", "9", "69.23%", "40", "85.11%", "49 (81.67%)"),
        ("", "No (Yam/farm only)", "4", "30.77%", "7", "14.89%", "11 (18.33%)"),
        ("Access to Credit", "Yes (Obtained credit)", "1", "7.69%", "29", "61.70%", "30 (50.00%)"),
        ("", "No (No credit access)", "12", "92.31%", "18", "38.30%", "30 (50.00%)"),
        ("Extension Contact", "Yes (Agent visit)", "0", "0.00%", "21", "44.68%", "21 (35.00%)"),
        ("", "No (No extension visit)", "13", "100.00%", "26", "55.32%", "39 (65.00%)"),
        ("Improved Yam Varieties", "Yes (Cultivated improved)", "0", "0.00%", "2", "4.26%", "2 (3.33%)"),
        ("", "No (Local cultivars only)", "13", "100.00%", "45", "95.74%", "58 (96.67%)"),
        ("Fertilizer / Manure Use", "Yes (Applied nutrients)", "9", "69.23%", "39", "82.98%", "48 (80.00%)"),
        ("", "No (No fertilizer applied)", "4", "30.77%", "8", "17.02%", "12 (20.00%)"),
        ("Modern Tools / Tech", "Yes (Used modern tools)", "0", "0.00%", "6", "12.77%", "6 (10.00%)"),
        ("", "No (Traditional tools only)", "13", "100.00%", "41", "87.23%", "54 (90.00%)"),
        ("Cooperative Membership", "Yes (Cooperative member)", "10", "76.92%", "39", "82.98%", "49 (81.67%)"),
        ("", "No (Non-member)", "3", "23.08%", "8", "17.02%", "11 (18.33%)")
    ]
    for row_data in t1_data:
        r = t1.add_row()
        format_cell(r.cells[0], row_data[0], bold=(row_data[0] != ""))
        format_cell(r.cells[1], row_data[1])
        format_cell(r.cells[2], row_data[2], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[3], row_data[3], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[4], row_data[4], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[5], row_data[5], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[6], row_data[6], align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_table_note(doc, "Source: Field Survey Data Analysis, 2026. Percentages represent within-group distributions for poor (n = 13) and non-poor (n = 47) farmers.")

    # Table 2: Continuous Variables
    add_heading(doc, "3. Continuous Demographic and Farm Production Profile", level=1)
    add_p(doc, "Table 2 summarizes the central tendency and dispersion of key continuous demographic, experience, and land asset variables across the poor and non-poor groups.")
    
    add_table_title(doc, "Table 2: Mean Characteristics of Yam Farmers by Poverty Status")
    t2 = doc.add_table(rows=1, cols=4)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t2)
    
    h2 = t2.rows[0].cells
    format_cell(h2[0], "Continuous Variable", bold=True)
    format_cell(h2[1], "Poor (n = 13) Mean ± SD", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h2[2], "Non-Poor (n = 47) Mean ± SD", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h2[3], "Overall (N = 60) Mean ± SD", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(t2.rows[0])
    
    t2_data = [
        ("Farmer Chronological Age (years)", "51.31 ± 8.99", "44.57 ± 8.04", "46.03 ± 8.64"),
        ("Household Size (persons)", "8.31 ± 1.70", "5.66 ± 1.43", "6.23 ± 1.84"),
        ("Yam Farming Experience (years)", "25.77 ± 10.48", "16.98 ± 6.94", "18.88 ± 8.56"),
        ("Total Farm Size (hectares)", "1.98 ± 0.48", "2.56 ± 0.82", "2.43 ± 0.79"),
        ("Yam Cultivated Area (hectares)", "1.43 ± 0.37", "1.73 ± 0.56", "1.67 ± 0.53")
    ]
    for row_data in t2_data:
        r = t2.add_row()
        format_cell(r.cells[0], row_data[0])
        format_cell(r.cells[1], row_data[1], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[2], row_data[2], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[3], row_data[3], align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_table_note(doc, "Source: Field Survey Data Analysis, 2026. Continuous values reported as arithmetic mean ± sample standard deviation (SD).")

    # Table 3: Expenditure Welfare Profile
    add_heading(doc, "4. Expenditure and Living Standards Profile", level=1)
    add_p(doc, "Table 3 details the budgetary welfare indicators and expenditure shortfalls characterizing the poor and non-poor households in the study area.")
    
    add_table_title(doc, "Table 3: Expenditure Welfare Profile of Yam Farmers by Poverty Status")
    t3 = doc.add_table(rows=1, cols=4)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t3)
    
    h3 = t3.rows[0].cells
    format_cell(h3[0], "Welfare & Budgetary Indicator", bold=True)
    format_cell(h3[1], "Poor (n = 13)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h3[2], "Non-Poor (n = 47)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h3[3], "Overall (N = 60)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(t3.rows[0])
    
    t3_data = [
        ("Mean Total Monthly Household Expenditure", "₦101,000.00 ± ₦24,782.39", "₦119,941.49 ± ₦27,223.37", "₦115,837.50 ± ₦27,652.42"),
        ("Mean Household Size (persons)", "8.31 ± 1.70", "5.66 ± 1.43", "6.23 ± 1.84"),
        ("Mean Per-Capita Expenditure (PCHE)", "₦12,079.49 ± ₦919.97", "₦22,559.76 ± ₦7,830.98", "₦20,289.03 ± ₦8,181.80"),
        ("Monthly Relative Poverty Line (z)", "₦13,526.02", "₦13,526.02", "₦13,526.02"),
        ("Mean Monthly Expenditure Deficit / Surplus", "Shortfall: -₦1,446.53", "Surplus: +₦9,033.74", "Mean Shortfall: ₦313.42")
    ]
    for row_data in t3_data:
        r = t3.add_row()
        format_cell(r.cells[0], row_data[0])
        format_cell(r.cells[1], row_data[1], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[2], row_data[2], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[3], row_data[3], align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_table_note(doc, "Source: Field Survey Data Analysis, 2026. Relative poverty threshold z = (2/3) × Mean PCHE = ₦13,526.02 per person per month.")

    # In-Depth Academic Narrative (6 Paragraphs)
    add_heading(doc, "5. Narrative Interpretation of the Poverty Status Profile", level=1)
    
    add_p(doc, "The descriptive poverty profile reveals clear socioeconomic and structural distinctions between poor and non-poor yam-farming households in Akpabuyo Local Government Area. Out of the 60 sampled households, 13 (21.67%) were identified as poor, falling below the relative poverty threshold of ₦13,526.02 per person per month, while 47 households (78.33%) were classified as non-poor. Descriptively, the poor group exhibited a monthly per-capita expenditure averaging ₦12,079.49 (representing a mean monthly consumption deficit of ₦1,446.53 per capita relative to the poverty line), compared to ₦22,559.76 among the non-poor group. Although total monthly household spending was somewhat lower among the poor (₦101,000.00 versus ₦119,941.49), the pronounced divergence in per-capita living standards is heavily driven by demographic composition.")
    
    add_p(doc, "Demographically, poor yam farmers in the study area were characterized by older chronological age and substantially larger household sizes. Farmers classified as poor recorded a mean age of 51.31 ± 8.99 years (with 76.92% being male), compared to an average age of 44.57 ± 8.04 years among non-poor farmers (where females comprised 44.68% of enterprise heads). Furthermore, the poor group had an average household size of 8.31 ± 1.70 persons (ranging from 6 to 10 members), whereas non-poor households averaged 5.66 ± 1.43 members. This descriptive contrast highlights that poor households bear a substantially heavier family dependency burden, spreading their budgetary resources over more members and resulting in depressed per-capita consumption levels.")
    
    add_p(doc, "In terms of human capital and income diversification, noticeable descriptive differences emerged between the two welfare strata. While the majority of both poor (53.85%) and non-poor (42.55%) farmers possessed secondary education, non-poor farmers recorded a higher proportion of tertiary educational attainment (29.79%) compared to the poor group (7.69%). Conversely, primary education was more prevalent among poor respondents (38.46%) than among non-poor respondents (27.66%). Regarding livelihoods, 85.11% of non-poor households engaged in supplementary off-farm income-generating activities, whereas a lower proportion of poor households (69.23%) reported secondary income sources, indicating that non-poor farming families maintained greater income diversification.")
    
    add_p(doc, "A descriptive examination of farm productive assets indicates that non-poor farmers operated larger land holdings and allocated more area to yam cultivation. Non-poor respondents managed an average total farm holding of 2.56 ± 0.82 hectares (with 1.73 ± 0.56 hectares dedicated specifically to yam), whereas poor respondents cultivated an average total farm size of 1.98 ± 0.48 hectares (with 1.43 ± 0.37 hectares under yam). Interestingly, poor farmers recorded longer yam farming experience (25.77 ± 10.48 years versus 16.98 ± 6.94 years among non-poor farmers), reflecting their older demographic profile but demonstrating that length of traditional farming experience alone does not preclude household poverty in the absence of modern farm capital.")
    
    add_p(doc, "Institutional support and modern input adoption displayed the sharpest descriptive contrast across the poverty profile. Among non-poor farmers, 61.70% had access to agricultural credit during the preceding farming season, compared to only 7.69% (1 out of 13) among poor farmers. Furthermore, 44.68% of non-poor farmers received agricultural extension advisory visits, while 0.00% (0 out of 13) of poor farmers had extension contact. Similarly, modern farm tools and improved yam varieties were utilized exclusively by a fraction of non-poor farmers (12.77% and 4.26%, respectively), while completely absent (0.00%) among the poor. Cooperative society membership was widespread across both groups (76.92% poor versus 82.98% non-poor), reflecting broad community-level social organization.")
    
    add_p(doc, "In conclusion, the Objective II poverty profile illustrates that poor yam-farming households in Akpabuyo LGA are descriptively characterized by older household heads, larger domestic dependency burdens, smaller land holdings, lower secondary income diversification, and severe deprivation in agricultural credit access and extension contact. Rather than asserting causal mechanisms, this descriptive profile provides the empirical foundation for Objective III, where bivariate statistical tests and multivariable binary logistic regression formally evaluate the statistical significance and independent associations of these factors with household poverty status.")

    doc.save("Objective_2_Poverty_Status_Profile_Akpabuyo.docx")
    print("Saved Objective_2_Poverty_Status_Profile_Akpabuyo.docx")

if __name__ == "__main__":
    build_objective_2_standalone()

