# -*- coding: utf-8 -*-
"""
Generate Chapter_4_Objective_2_Integration.docx
Complete Integrated Chapter Four incorporating the new Specific Objective II:
Objective I: Determine poverty status using appropriate poverty measures.
Objective II: Analyze poverty status of yam farmers in the study area (Poverty Status Profile).
Objective III: Analyze factors influencing poverty in the study area.
Objective IV: Measure the challenges faced by yam farmers in the study area.
"""

import os
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
    
    # Clear other borders
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

def format_cell(cell, text, align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, italic=False, font_size=10.5):
    cell.text = text
    set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    if len(p.runs) > 0:
        run = p.runs[0]
        run.font.name = 'Times New Roman'
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = RGBColor(0, 0, 0)

def add_academic_p(doc, text, space_after=6, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = bold
    run.font.italic = italic
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

def add_table_source(doc, source_text="Source: Field Survey Data Analysis, 2026."):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(source_text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10.5)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_figure_image(doc, img_path, caption_text, width=Inches(5.8)):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(12)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(12)
        p_cap.paragraph_format.line_spacing = 1.15
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = 'Times New Roman'
        run_cap.font.size = Pt(11)
        run_cap.font.bold = True
        run_cap.font.color.rgb = RGBColor(0, 0, 0)

def generate_chapter_4_integrated():
    doc = Document()
    
    # 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Chapter Title
    add_heading_1(doc, "CHAPTER FOUR")
    add_heading_1(doc, "RESULTS AND DISCUSSION")
    
    # Opening Paragraph
    add_academic_p(doc, "This chapter presents the empirical results and detailed academic discussion of the study based on field survey data collected from 60 yam-farming households in Akpabuyo Local Government Area, Cross River State. The presentation is systematically structured in accordance with the study's four specific research objectives: (i) determining the poverty status of yam farmers using the relative poverty line and Foster-Greer-Thorbecke (FGT) poverty indices; (ii) analyzing the poverty status profile across socioeconomic, farm asset, and expenditure characteristics; (iii) analyzing the factors influencing household poverty status using bivariate tests and binary logistic regression; and (iv) evaluating the severity of production and institutional challenges faced by yam farmers. The chapter concludes with formal hypothesis testing and an integrated discussion of findings.")
    
    # -------------------------------------------------------------
    # 4.1 Socio-Economic Characteristics of Yam Farmers
    # -------------------------------------------------------------
    add_heading_2(doc, "4.1 Socio-Economic Characteristics of Yam Farmers")
    add_academic_p(doc, "The socio-economic attributes of farming households are fundamental determinants of their managerial capabilities, resource allocation efficiency, technology adoption, and overall economic welfare. In this study, the socio-economic characteristics investigated include sex, age, marital status, educational attainment, household size, yam farming experience, and engagement in supplementary (off-farm) income-generating activities. Table 4.1 presents a consolidated summary of these socio-economic characteristics for the 60 sampled yam-farming households in Akpabuyo Local Government Area.")
    
    add_table_title(doc, "Table 4.1: Socio-Economic Characteristics of Yam Farmers in Akpabuyo LGA (N = 60)")
    table1 = doc.add_table(rows=1, cols=4)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table1)
    
    hdr_cells = table1.rows[0].cells
    format_cell(hdr_cells[0], "Variable / Characteristic", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True)
    format_cell(hdr_cells[1], "Frequency (n)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr_cells[2], "Percentage (%)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr_cells[3], "Summary Statistics", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(table1.rows[0])
    
    rows_data = [
        ("Sex", "", "", ""),
        ("  Male", "36", "60.00", "—"),
        ("  Female", "24", "40.00", "—"),
        ("  Total", "60", "100.00", "—"),
        ("Age of farmer (years)", "60", "100.00", "Mean = 46.03 ± 8.64 (Min = 30, Max = 63)"),
        ("Marital Status", "", "", ""),
        ("  Single", "5", "8.33", "—"),
        ("  Married", "49", "81.67", "—"),
        ("  Divorced", "0", "0.00", "—"),
        ("  Widowed", "6", "10.00", "—"),
        ("  Total", "60", "100.00", "—"),
        ("Educational Attainment", "", "", ""),
        ("  No Formal Education", "0", "0.00", "—"),
        ("  Primary Education (6 years)", "18", "30.00", "—"),
        ("  Secondary Education (12 years)", "27", "45.00", "—"),
        ("  Tertiary Education (16 years)", "15", "25.00", "—"),
        ("  Total", "60", "100.00", "—"),
        ("Household Size (persons)", "60", "100.00", "Mean = 6.23 ± 1.84 (Min = 3, Max = 10)"),
        ("Yam Farming Experience (years)", "60", "100.00", "Mean = 18.88 ± 8.56 (Min = 6, Max = 40)"),
        ("Other Sources of Income", "", "", ""),
        ("  Yes (Engaged in supplementary income)", "49", "81.67", "—"),
        ("  No (Solely dependent on farming)", "11", "18.33", "—"),
        ("  Total", "60", "100.00", "—")
    ]
    for item in rows_data:
        row = table1.add_row()
        is_category_header = (item[1] == "" and item[2] == "" and item[3] == "")
        format_cell(row.cells[0], item[0], align=WD_ALIGN_PARAGRAPH.LEFT, bold=is_category_header)
        format_cell(row.cells[1], item[1], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_category_header)
        format_cell(row.cells[2], item[2], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_category_header)
        format_cell(row.cells[3], item[3], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_category_header)
        
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026.")
    
    add_heading_3(doc, "4.1.1 Sex of Respondents")
    add_academic_p(doc, "Table 4.1 shows that 36 respondents (60.00%) were male, while 24 respondents (40.00%) were female. This distribution reveals that yam farming in Akpabuyo LGA is actively pursued by both genders, with male farmers comprising the majority of enterprise decision-makers. The substantial 40.00% female participation rate underscores the prominent contribution of women to agricultural production and household food security in the area.")
    
    add_heading_3(doc, "4.1.2 Age of Respondents")
    add_academic_p(doc, "The chronological age of respondents averaged 46.03 ± 8.64 years, spanning from 30 to 63 years. This indicates that yam farming in the study area is dominated by middle-aged individuals who remain in their economically active and productive years.")
    add_figure_image(doc, "Figure_4_1_Age_Distribution.png", "Figure 4.1: Age Distribution of Yam Farmers in Akpabuyo LGA")
    
    add_heading_3(doc, "4.1.3 Marital Status of Respondents")
    add_academic_p(doc, "The marital status distribution indicates that 81.67% (n = 49) of the farmers were married, 10.00% (n = 6) were widowed, and 8.33% (n = 5) were single, with no divorced respondents recorded. The predominance of married household heads facilitates family labour mobilization for arduous yam cultivation operations.")
    
    add_heading_3(doc, "4.1.4 Educational Attainment")
    add_academic_p(doc, "All 60 respondents (100.00%) possessed formal education: 45.00% (n = 27) completed secondary education, 30.00% (n = 18) completed primary education, and 25.00% (n = 15) attained tertiary education. This high literacy level enhances farmers' ability to process agricultural information, adopt agronomic innovations, and manage farm budgets.")
    
    add_heading_3(doc, "4.1.5 Household Size")
    add_academic_p(doc, "Household size averaged 6.23 ± 1.84 persons, ranging between 3 and 10 persons. In agrarian settings, larger household size supplies critical domestic farm labour but simultaneously imposes higher food and non-food consumption demands on household income.")
    
    add_heading_3(doc, "4.1.6 Yam Farming Experience")
    add_academic_p(doc, "Respondents had an average of 18.88 ± 8.56 years of yam farming experience (ranging from 6 to 40 years), indicating extensive practical familiarity with local soils, rainfall regimes, and crop management practices.")
    
    add_heading_3(doc, "4.1.7 Other Sources of Income")
    add_academic_p(doc, "A large majority of respondents (81.67%, n = 49) participated in off-farm or non-farm secondary income activities (such as petty trading, agro-processing, and artisanal trades), while 18.33% (n = 11) depended exclusively on yam farming, demonstrating substantial livelihood diversification.")

    # -------------------------------------------------------------
    # 4.2 Household Expenditure Pattern
    # -------------------------------------------------------------
    add_heading_2(doc, "4.2 Household Expenditure Pattern of Yam Farmers")
    add_academic_p(doc, "In smallholder agricultural settings where income flows are seasonal and non-continuous, household consumption expenditure provides an observable, robust measure of household economic welfare. Table 4.2 outlines the mean monthly household expenditure across major budgetary categories for the 60 sampled households in Akpabuyo LGA.")
    
    add_table_title(doc, "Table 4.2: Mean Monthly Household Expenditure by Category (N = 60)")
    table2 = doc.add_table(rows=1, cols=3)
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table2)
    
    hdr2 = table2.rows[0].cells
    format_cell(hdr2[0], "Expenditure Category", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True)
    format_cell(hdr2[1], "Mean Monthly Expenditure (₦)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr2[2], "Budget Share (%)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(table2.rows[0])
    
    exp_data = [
        ("Food and groceries", "60,703.33", "52.40"),
        ("Housing and utilities", "18,246.67", "15.75"),
        ("Education", "14,528.33", "12.54"),
        ("Transportation and other", "11,875.83", "10.25"),
        ("Health and medical care", "8,631.67", "7.45"),
        ("Reported Total Household Expenditure", "115,837.50", "100.00")
    ]
    for row_idx, item in enumerate(exp_data):
        row = table2.add_row()
        is_total = (row_idx == len(exp_data) - 1)
        format_cell(row.cells[0], item[0], align=WD_ALIGN_PARAGRAPH.LEFT, bold=is_total)
        format_cell(row.cells[1], item[1], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_total)
        format_cell(row.cells[2], item[2], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_total)
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026.")
    
    add_academic_p(doc, "As shown in Table 4.2, total monthly household expenditure averaged ₦115,837.50. Food consumption constituted the single largest expenditure item (₦60,703.33; 52.40% of total budget), consistent with Engel's law in rural agrarian economies. Non-food expenses absorbed the remaining 47.60%, led by housing/utilities (15.75%), education (12.54%), transportation (10.25%), and healthcare (7.45%).")
    add_figure_image(doc, "Figure_4_2_Mean_Monthly_Expenditure.png", "Figure 4.2: Mean Monthly Household Expenditure by Category among Yam Farmers")

    # -------------------------------------------------------------
    # 4.3 Poverty Status of Yam Farmers (Objective 1)
    # -------------------------------------------------------------
    add_heading_2(doc, "4.3 Poverty Status of Yam Farmers (Objective I)")
    add_academic_p(doc, "In accordance with Specific Objective I, the poverty status of yam-farming households in Akpabuyo LGA was determined using the relative poverty line method and Foster, Greer, and Thorbecke (FGT, 1984) poverty indices.")
    
    add_heading_3(doc, "4.3.1 Determination of the Poverty Line")
    add_academic_p(doc, "The mean Per-Capita Monthly Household Expenditure (PCHE) across all 60 sampled households was ₦20,289.03 per person per month. Following standard national and international poverty analysis conventions, the relative poverty threshold (z) was established at exactly two-thirds (2/3) of the mean PCHE:")
    add_academic_p(doc, "Poverty Line (z) = 2/3 × Mean PCHE = 2/3 × ₦20,289.03 = ₦13,526.02 per person per month.", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    
    add_table_title(doc, "Table 4.3: Determination of the Relative Poverty Line among Yam Farmers")
    table3 = doc.add_table(rows=1, cols=2)
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table3)
    
    hdr3 = table3.rows[0].cells
    format_cell(hdr3[0], "Parameter / Metric", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True)
    format_cell(hdr3[1], "Value", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(table3.rows[0])
    
    poverty_line_rows = [
        ("Total Sample Size (N)", "60 households"),
        ("Mean Per-Capita Monthly Expenditure (Mean PCHE)", "₦20,289.03"),
        ("Standard Deviation of PCHE", "₦8,181.80"),
        ("Minimum PCHE", "₦10,833.33"),
        ("Maximum PCHE", "₦42,000.00"),
        ("Poverty Line Definition", "Two-thirds (2/3) of Mean PCHE"),
        ("Established Relative Poverty Threshold (z)", "₦13,526.02 per person/month")
    ]
    for item in poverty_line_rows:
        row = table3.add_row()
        format_cell(row.cells[0], item[0], align=WD_ALIGN_PARAGRAPH.LEFT, bold=(item[0].startswith("Established")))
        format_cell(row.cells[1], item[1], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=(item[0].startswith("Established")))
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026.")
    
    add_heading_3(doc, "4.3.2 Poverty Incidence, Depth and Severity")
    add_academic_p(doc, "Households with PCHE below ₦13,526.02 were categorized as poor, while those with PCHE equal to or exceeding ₦13,526.02 were categorized as non-poor. FGT poverty indices were estimated for headcount (P0), gap (P1), and severity (P2), as shown in Table 4.4.")
    
    add_table_title(doc, "Table 4.4: Poverty Status Distribution and Foster-Greer-Thorbecke (FGT) Poverty Indices (N = 60)")
    table4 = doc.add_table(rows=1, cols=4)
    table4.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table4)
    
    hdr4 = table4.rows[0].cells
    format_cell(hdr4[0], "Poverty Measure / Category", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True)
    format_cell(hdr4[1], "Frequency (n)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr4[2], "Index Value (P_α)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr4[3], "Percentage (%)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(table4.rows[0])
    
    fgt_rows = [
        ("A. Poverty Status Classification", "", "", ""),
        ("  Non-poor (PCHE ≥ ₦13,526.02)", "47", "—", "78.33"),
        ("  Poor (PCHE < ₦13,526.02)", "13", "—", "21.67"),
        ("  Total", "60", "—", "100.00"),
        ("B. FGT Poverty Indices", "", "", ""),
        ("  Poverty Headcount Index (P0)", "13", "0.2167", "21.67"),
        ("  Poverty Gap Index (P1)", "—", "0.0232", "2.32"),
        ("  Squared Poverty Gap / Severity (P2)", "—", "0.0034", "0.34")
    ]
    for item in fgt_rows:
        row = table4.add_row()
        is_subhdr = (item[1] == "" and item[2] == "" and item[3] == "")
        format_cell(row.cells[0], item[0], align=WD_ALIGN_PARAGRAPH.LEFT, bold=is_subhdr)
        format_cell(row.cells[1], item[1], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_subhdr)
        format_cell(row.cells[2], item[2], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_subhdr)
        format_cell(row.cells[3], item[3], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_subhdr)
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026.")
    add_figure_image(doc, "Figure_4_3_Poverty_Status.png", "Figure 4.3: Poverty Status Distribution of Yam Farmers in Akpabuyo LGA")
    
    add_academic_p(doc, "The results indicate that 13 households (21.67%) were poor, yielding a poverty headcount index (P0) of 0.2167. The poverty gap index (P1) was 0.0232 (2.32%), representing an average monthly expenditure deficit of ₦313.42 per person across the entire sample. The poverty severity index (P2) was 0.0034 (0.34%), indicating low inequality among the poor.")

    # -------------------------------------------------------------
    # 4.4 Poverty Status Profile of Yam Farmers (Objective 2 - NEW)
    # -------------------------------------------------------------
    add_heading_2(doc, "4.4 Poverty Status Profile of Yam Farmers (Objective II)")
    add_academic_p(doc, "In accordance with Specific Objective II, this section presents a descriptive poverty status profile comparing poor (n = 13) and non-poor (n = 47) yam-farming households across demographic, human capital, farm asset, and expenditure welfare dimensions. This descriptive profile details the characteristics of each poverty stratum prior to the formal inferential factor analysis conducted under Objective III.")
    
    add_heading_3(doc, "4.4.1 Socioeconomic and Institutional Profile by Poverty Status")
    add_academic_p(doc, "Table 4.5 profiles the categorical demographic, educational, and institutional characteristics of the respondents disaggregated by poverty status.")
    
    add_table_title(doc, "Table 4.5: Distribution of Yam Farmers by Poverty Status and Socioeconomic Characteristics")
    table5 = doc.add_table(rows=1, cols=7)
    table5.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table5)
    
    h5 = table5.rows[0].cells
    format_cell(h5[0], "Socioeconomic Variable", bold=True)
    format_cell(h5[1], "Category", bold=True)
    format_cell(h5[2], "Poor (n = 13)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h5[3], "Poor (%)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h5[4], "Non-Poor (n = 47)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h5[5], "Non-Poor (%)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h5[6], "Total (N = 60)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(table5.rows[0])
    
    t5_data = [
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
    for row_data in t5_data:
        r = table5.add_row()
        format_cell(r.cells[0], row_data[0], bold=(row_data[0] != ""))
        format_cell(r.cells[1], row_data[1])
        format_cell(r.cells[2], row_data[2], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[3], row_data[3], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[4], row_data[4], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[5], row_data[5], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[6], row_data[6], align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026. Note: Inferential hypothesis testing is presented under Objective III (Section 4.5).")

    add_heading_3(doc, "4.4.2 Mean Characteristics and Farm Asset Profile by Poverty Status")
    add_academic_p(doc, "Table 4.6 summarizes the continuous demographic, experience, and land asset variables across poor and non-poor groups.")
    
    add_table_title(doc, "Table 4.6: Mean Characteristics of Yam Farmers by Poverty Status")
    table6 = doc.add_table(rows=1, cols=4)
    table6.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table6)
    
    h6 = table6.rows[0].cells
    format_cell(h6[0], "Continuous Variable", bold=True)
    format_cell(h6[1], "Poor (n = 13) Mean ± SD", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h6[2], "Non-Poor (n = 47) Mean ± SD", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h6[3], "Overall (N = 60) Mean ± SD", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(table6.rows[0])
    
    t6_data = [
        ("Farmer Chronological Age (years)", "51.31 ± 8.99", "44.57 ± 8.04", "46.03 ± 8.64"),
        ("Household Size (persons)", "8.31 ± 1.70", "5.66 ± 1.43", "6.23 ± 1.84"),
        ("Yam Farming Experience (years)", "25.77 ± 10.48", "16.98 ± 6.94", "18.88 ± 8.56"),
        ("Total Farm Size (hectares)", "1.98 ± 0.48", "2.56 ± 0.82", "2.43 ± 0.79"),
        ("Yam Cultivated Area (hectares)", "1.43 ± 0.37", "1.73 ± 0.56", "1.67 ± 0.53")
    ]
    for row_data in t6_data:
        r = table6.add_row()
        format_cell(r.cells[0], row_data[0])
        format_cell(r.cells[1], row_data[1], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[2], row_data[2], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[3], row_data[3], align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026. Continuous values reported as arithmetic mean ± sample standard deviation (SD).")

    add_heading_3(doc, "4.4.3 Expenditure Welfare Profile by Poverty Status")
    add_academic_p(doc, "Table 4.7 details the expenditure patterns and consumption shortfalls distinguishing poor from non-poor farming families.")
    
    add_table_title(doc, "Table 4.7: Expenditure Welfare Profile of Yam Farmers by Poverty Status")
    table7 = doc.add_table(rows=1, cols=4)
    table7.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table7)
    
    h7 = table7.rows[0].cells
    format_cell(h7[0], "Welfare & Budgetary Indicator", bold=True)
    format_cell(h7[1], "Poor (n = 13)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h7[2], "Non-Poor (n = 47)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(h7[3], "Overall (N = 60)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(table7.rows[0])
    
    t7_data = [
        ("Mean Total Monthly Household Expenditure", "₦101,000.00 ± ₦24,782.39", "₦119,941.49 ± ₦27,223.37", "₦115,837.50 ± ₦27,652.42"),
        ("Mean Household Size (persons)", "8.31 ± 1.70", "5.66 ± 1.43", "6.23 ± 1.84"),
        ("Mean Per-Capita Expenditure (PCHE)", "₦12,079.49 ± ₦919.97", "₦22,559.76 ± ₦7,830.98", "₦20,289.03 ± ₦8,181.80"),
        ("Monthly Relative Poverty Line (z)", "₦13,526.02", "₦13,526.02", "₦13,526.02"),
        ("Mean Monthly Expenditure Deficit / Surplus", "Shortfall: -₦1,446.53", "Surplus: +₦9,033.74", "Mean Shortfall: ₦313.42")
    ]
    for row_data in t7_data:
        r = table7.add_row()
        format_cell(r.cells[0], row_data[0])
        format_cell(r.cells[1], row_data[1], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[2], row_data[2], align=WD_ALIGN_PARAGRAPH.RIGHT)
        format_cell(r.cells[3], row_data[3], align=WD_ALIGN_PARAGRAPH.RIGHT)
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026. Relative poverty threshold z = (2/3) × Mean PCHE = ₦13,526.02 per person per month.")

    # Narrative Interpretation
    add_academic_p(doc, "The descriptive poverty profile demonstrates that poor and non-poor yam-farming households in Akpabuyo LGA exhibit distinctly contrasting structural profiles. Poor households recorded a mean per-capita monthly expenditure of ₦12,079.49, falling ₦1,446.53 below the poverty line, whereas non-poor households achieved a mean per-capita expenditure of ₦22,559.76 (a monthly per-capita surplus of ₦9,033.74). Although total monthly household outlays differed moderately (₦101,000.00 among the poor versus ₦119,941.49 among the non-poor), the substantial divergence in individual welfare is heavily shaped by family size: poor households averaged 8.31 members compared to 5.66 members in non-poor households.")
    
    add_academic_p(doc, "Demographically, the poor group was characterized by older household heads (mean age 51.31 ± 8.99 years versus 44.57 ± 8.04 years for non-poor) and longer farming experience (25.77 ± 10.48 years versus 16.98 ± 6.94 years). In terms of productive land assets, non-poor farmers operated larger total holdings (2.56 ± 0.82 ha versus 1.98 ± 0.48 ha) and devoted more land to yam (1.73 ± 0.56 ha versus 1.43 ± 0.37 ha). Furthermore, non-poor farmers maintained higher livelihood diversification, with 85.11% engaged in off-farm income generation compared to 69.23% among the poor.")
    
    add_academic_p(doc, "The most striking descriptive differences emerged in institutional support and modern technology adoption. Over 61% (61.70%) of non-poor farmers had access to agricultural credit compared to only 7.69% of poor farmers. Similarly, 44.68% of non-poor farmers received agricultural extension advisory visits, whereas zero (0.00%) poor farmers reported extension contact. Use of modern tools (12.77%) and improved yam varieties (4.26%) was confined entirely to non-poor households. This descriptive profile provides the essential background for Objective III, where these observed associations are formally tested using inferential statistics.")

    # -------------------------------------------------------------
    # 4.5 Factors Associated with Poverty Status (Objective 3)
    # -------------------------------------------------------------
    add_heading_2(doc, "4.5 Factors Associated with Poverty Status (Objective III)")
    add_academic_p(doc, "In accordance with Specific Objective III, this section provides formal inferential evaluation of the factors influencing household poverty status. Section 4.5.1 presents non-parametric and chi-square bivariate tests, while Section 4.5.2 presents a multivariable binary logistic regression model.")
    
    add_heading_3(doc, "4.5.1 Bivariate Analysis of Factors Associated with Poverty Status")
    add_academic_p(doc, "Table 4.8 presents bivariate statistical tests comparing poor and non-poor households across candidate explanatory variables.")
    
    add_table_title(doc, "Table 4.8: Bivariate Analysis of Factors Associated with Poverty Status (N = 60)")
    table8 = doc.add_table(rows=1, cols=6)
    table8.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table8)
    
    hdr8 = table8.rows[0].cells
    format_cell(hdr8[0], "Variable / Indicator", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True)
    format_cell(hdr8[1], "Poor (n = 13)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr8[2], "Non-Poor (n = 47)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr8[3], "Overall (N = 60)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr8[4], "Test Statistic", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr8[5], "p-value", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(table8.rows[0])
    
    bivariate_rows = [
        ("A. Demographic & Human Capital", "", "", "", "", ""),
        ("  Age of farmer (years)", "51.31 ± 8.99", "44.57 ± 8.04", "46.03 ± 8.64", "Mann-Whitney U = 432.00", "0.024*"),
        ("  Household size (persons)", "8.31 ± 1.70", "5.66 ± 1.43", "6.23 ± 1.84", "Mann-Whitney U = 536.00", "< 0.001*"),
        ("  Educational attainment", "", "", "", "Chi-Square = 2.673 (df=2)", "0.263"),
        ("    Primary education (6 yrs)", "5 (38.5%)", "13 (27.7%)", "18 (30.0%)", "—", "—"),
        ("    Secondary education (12 yrs)", "7 (53.8%)", "20 (42.6%)", "27 (45.0%)", "—", "—"),
        ("    Tertiary education (16 yrs)", "1 (7.7%)", "14 (29.8%)", "15 (25.0%)", "—", "—"),
        ("B. Land Assets & Production Scale", "", "", "", "", ""),
        ("  Total farm size (ha)", "1.98 ± 0.48", "2.56 ± 0.82", "2.43 ± 0.79", "Mann-Whitney U = 170.50", "0.016*"),
        ("  Yam cultivated area (ha)", "1.43 ± 0.37", "1.73 ± 0.56", "1.67 ± 0.53", "Mann-Whitney U = 205.00", "0.072"),
        ("C. Institutional & Modern Technology", "", "", "", "", ""),
        ("  Access to credit (Yes = 1)", "1 (7.7%)", "29 (61.7%)", "30 (50.0%)", "Chi-Square = 9.820 (df=1)", "0.002*"),
        ("  Extension contact in 12 mos (Yes)", "0 (0.0%)", "21 (44.7%)", "21 (35.0%)", "Fisher's exact test", "0.002*"),
        ("  Improved yam varieties (Yes)", "0 (0.0%)", "2 (4.3%)", "2 (3.3%)", "Fisher's exact test", "1.000"),
        ("  Fertilizer / manure use (Yes)", "9 (69.2%)", "39 (83.0%)", "48 (80.0%)", "Chi-Square = 0.497 (df=1)", "0.481"),
        ("  Modern tools / tech (Yes)", "0 (0.0%)", "6 (12.8%)", "6 (10.0%)", "Fisher's exact test", "0.324"),
        ("  Cooperative membership (Yes)", "10 (76.9%)", "39 (83.0%)", "49 (81.7%)", "Chi-Square = 0.009 (df=1)", "0.925")
    ]
    for item in bivariate_rows:
        row = table8.add_row()
        is_sec = (item[1] == "" and item[2] == "" and item[3] == "" and item[4] == "" and item[5] == "")
        format_cell(row.cells[0], item[0], align=WD_ALIGN_PARAGRAPH.LEFT, bold=is_sec)
        format_cell(row.cells[1], item[1], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_sec)
        format_cell(row.cells[2], item[2], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_sec)
        format_cell(row.cells[3], item[3], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_sec)
        format_cell(row.cells[4], item[4], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_sec)
        format_cell(row.cells[5], item[5], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_sec)
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026. * Significant at p < 0.05.\nMethodological Note: Household size is the arithmetic denominator in per-capita expenditure calculation.")
    
    add_academic_p(doc, "Bivariate tests indicate statistically significant associations with poverty status for farmer age (U = 432.00, p = 0.024), household size (U = 536.00, p < 0.001), total farm size (U = 170.50, p = 0.016), access to credit (χ² = 9.820, p = 0.002), and agricultural extension contact (Fisher's exact p = 0.002).")

    # 4.5.2 Logistic Regression
    add_heading_3(doc, "4.5.2 Logistic Regression Analysis of Factors Associated with Poverty Status")
    add_academic_p(doc, "To evaluate multivariable associations while respecting events-per-variable (EPV) constraints (n = 13 poor events in N = 60), a parsimonious binary logistic regression model was estimated with total farm size (ha) and access to credit (Yes = 1) as key predictors.")
    
    add_table_title(doc, "Table 4.9: Binary Logistic Regression Model of Factors Associated with Poverty Status")
    table9 = doc.add_table(rows=1, cols=3)
    table9.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table9)
    
    hdr9 = table9.rows[0].cells
    format_cell(hdr9[0], "Predictor Variable", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True)
    format_cell(hdr9[1], "Odds Ratio (OR)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr9[2], "p-value", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(table9.rows[0])
    
    logit_rows = [
        ("Total farm size (ha)", "0.6505", "0.5979"),
        ("Access to credit (Yes = 1)", "0.0744", "0.0369*")
    ]
    for item in logit_rows:
        row = table9.add_row()
        format_cell(row.cells[0], item[0], align=WD_ALIGN_PARAGRAPH.LEFT, bold=False)
        format_cell(row.cells[1], item[1], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        format_cell(row.cells[2], item[2], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026. * Significant at p < 0.05.\nModel Diagnostics: Likelihood Ratio χ² = 13.861 (df = 2, p = 0.000978); Nagelkerke R² = 0.3181; Log-Likelihood = -24.719.")
    
    add_academic_p(doc, "The omnibus likelihood ratio test was highly significant (χ² = 13.861, df = 2, p = 0.000978), with Nagelkerke R² = 0.3181, indicating the model's relative explanatory performance based on the Nagelkerke pseudo-R² measure. Access to credit was statistically significant (OR = 0.0744, p = 0.0369; Firth sensitivity OR = 0.110, p = 0.039), indicating 92.56% lower odds of poverty for credit recipients holding farm size constant. Total farm size was not statistically significant after conditioning on credit (OR = 0.6505, p = 0.5979).")
    add_figure_image(doc, "Chapter_4_Analysis/Analysis_4_Factors_Poverty/Figure_4_4_Odds_Ratios_Factors_Poverty.png", "Figure 4.4: Odds Ratios from Binary Logistic Regression Model (95% CIs)")

    # -------------------------------------------------------------
    # 4.6 Challenges Faced by Yam Farmers (Objective 4)
    # -------------------------------------------------------------
    add_heading_2(doc, "4.6 Challenges Faced by Yam Farmers (Objective IV)")
    add_academic_p(doc, "In accordance with Specific Objective IV, ten production, institutional, and marketing constraints were evaluated using a 5-point Likert scale (1 = Not a Challenge to 5 = Very Severe). Table 4.10 presents the ranked challenges.")
    
    add_table_title(doc, "Table 4.10: Severity Ranking of Challenges Faced by Yam Farmers in Akpabuyo LGA (N = 60)")
    table10 = doc.add_table(rows=1, cols=7)
    table10.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table10)
    
    hdr10 = table10.rows[0].cells
    format_cell(hdr10[0], "Rank", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    format_cell(hdr10[1], "Constraint / Challenge", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True)
    format_cell(hdr10[2], "Mean Score", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr10[3], "Std. Dev.", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr10[4], "Median", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr10[5], "IQR", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr10[6], "Severity Level", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(table10.rows[0])
    
    challenges_rows = [
        ("1st", "High cost and scarcity of farm labour", "4.15", "0.80", "4.00", "1.00", "Severe"),
        ("2nd", "High cost of farm inputs (fertilizer, seeds, chemicals)", "4.00", "0.96", "4.00", "2.00", "Severe"),
        ("3rd", "Post-harvest losses and inadequate storage facilities", "3.88", "0.99", "4.00", "2.00", "Severe"),
        ("4th", "Unpredictable rainfall and climate conditions", "3.70", "0.85", "4.00", "1.00", "Severe"),
        ("5th", "High cost and scarcity of yam stakes", "3.57", "0.89", "4.00", "1.00", "Severe"),
        ("6th", "Inadequate access to agricultural credit", "3.53", "0.98", "3.00", "1.00", "Severe"),
        ("7th", "Inadequate agricultural extension services", "3.52", "1.07", "4.00", "1.00", "Severe"),
        ("8th", "Pest and disease infestation", "3.38", "0.83", "3.00", "1.00", "Moderate"),
        ("9th", "Low and unstable prices of yam (n = 59)", "3.12", "0.87", "3.00", "1.00", "Moderate"),
        ("10th", "Poor access to output markets", "2.90", "1.02", "3.00", "2.00", "Moderate")
    ]
    for item in challenges_rows:
        row = table10.add_row()
        format_cell(row.cells[0], item[0], align=WD_ALIGN_PARAGRAPH.CENTER, bold=False)
        format_cell(row.cells[1], item[1], align=WD_ALIGN_PARAGRAPH.LEFT, bold=False)
        format_cell(row.cells[2], item[2], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        format_cell(row.cells[3], item[3], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        format_cell(row.cells[4], item[4], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        format_cell(row.cells[5], item[5], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        format_cell(row.cells[6], item[6], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026. Severity intervals: 1.00–1.80 = Not a Challenge; 1.81–2.60 = Minor; 2.61–3.40 = Moderate; 3.41–4.20 = Severe; 4.21–5.00 = Very Severe.")
    add_figure_image(doc, "Chapter_4_Analysis/Analysis_5_Challenges/Figure_4_5_Challenge_Severity_Ranking.png", "Figure 4.5: Severity Ranking of Challenges Faced by Yam Farmers in Akpabuyo LGA")
    
    add_academic_p(doc, "The top three constraints were high cost/scarcity of farm labour (mean = 4.15 ± 0.80, Rank 1st; Severe), high input costs (mean = 4.00 ± 0.96, Rank 2nd; Severe), and post-harvest storage losses (mean = 3.88 ± 0.99, Rank 3rd; Severe). Institutional constraints including inadequate credit access (mean = 3.53, Rank 6th) and extension inadequacy (mean = 3.52, Rank 7th) were also categorized as severe.")

    # -------------------------------------------------------------
    # 4.7 Test of Hypothesis
    # -------------------------------------------------------------
    add_heading_2(doc, "4.7 Test of Hypothesis")
    add_academic_p(doc, "To provide formal statistical evaluation of the study's framework, the research hypothesis was tested:")
    add_academic_p(doc, "H0: Socio-economic variables do not significantly influence the poverty status of yam farmers in Akpabuyo Local Government Area.", space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    
    add_academic_p(doc, "The parsimonious binary logistic regression model reported in Table 4.9 served as the principal multivariable test of the hypothesis. The omnibus Likelihood Ratio test was statistically significant (χ² = 13.861, df = 2, p = 0.000978), indicating that the specified two-predictor model provided a statistically significant improvement over the null model. Accordingly, the null hypothesis was rejected with respect to the specified multivariable model.")
    add_academic_p(doc, "Within the model, access to credit was significantly associated with poverty status (OR = 0.0744, p = 0.0369), whereas total farm size was not statistically significant (OR = 0.6505, p = 0.5979). Therefore, the findings indicate that the specified multivariable model was statistically significant overall, with access to credit demonstrating the primary significant association.")

    # -------------------------------------------------------------
    # 4.8 Discussion of Major Findings
    # -------------------------------------------------------------
    add_heading_2(doc, "4.8 Discussion of Major Findings")
    add_academic_p(doc, "This section presents an integrated discussion of findings across the four specific research objectives:")
    
    add_academic_p(doc, "Regarding Objective I (Poverty Measurement), establishing the relative poverty line at ₦13,526.02 per person per month classified 21.67% of households as poor (P0 = 0.2167) and 78.33% as non-poor. The poverty gap (P1 = 0.0232) and severity (P2 = 0.0034) indicate moderate poverty depth and low expenditure inequality. Food expenditure absorbed 52.40% of household budgets, underscoring the dominance of subsistence food needs.")
    
    add_academic_p(doc, "Regarding Objective II (Poverty Status Profile), descriptive comparisons revealed that poor households were older (mean age 51.31 years), had larger family sizes (8.31 persons), operated smaller total farm holdings (1.98 ha), and faced acute institutional exclusion (only 7.69% had credit access and 0.00% received extension visits). In contrast, non-poor households maintained smaller families (5.66 persons), larger farm holdings (2.56 ha), higher secondary income diversification (85.11%), and substantially greater credit access (61.70%).")
    
    add_academic_p(doc, "Regarding Objective III (Factors Associated with Poverty), binary logistic regression confirmed that access to credit is significantly associated with lower odds of poverty (OR = 0.0744, p = 0.0369; Firth OR = 0.110, p = 0.039), providing crucial liquidity to finance seasonal input purchases and hired labour. Bivariate tests further highlighted extension contact (p = 0.002) and farm size (p = 0.016) as protective factors.")
    
    add_academic_p(doc, "Regarding Objective IV (Challenges Faced by Yam Farmers), high labour costs (mean = 4.15), high input costs (mean = 4.00), and post-harvest losses (mean = 3.88) were identified as the most severe constraints, reinforcing the econometric finding that liquidity and credit constraints severely hinder smallholder farm performance and living standards.")

    out_file = "Chapter_4_Objective_2_Integration.docx"
    doc.save(out_file)
    print(f"Saved {out_file}")

if __name__ == "__main__":
    generate_chapter_4_integrated()

