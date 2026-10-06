# -*- coding: utf-8 -*-
"""
Submission-Ready Rebuild/Correction of Chapter Four
Study: Analysis of Poverty Status of Yam Farmers in Akpabuyo Local Government Area, Cross River State, Nigeria
Target Output: Chapter_4_Results_and_Discussion_FINAL_v2.docx
"""
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
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

def format_cell(cell, text, align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, italic=False, font_size=11):
    cell.text = text
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
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

def add_academic_p(doc, text, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False):
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
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(title_text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_table_source(doc, source_text="Source: Field Survey Data Analysis, 2026."):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(source_text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)
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
    run.font.size = Pt(13)
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

def generate_chapter_4_v2():
    doc = Document()
    
    # Page setup - 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Chapter Title
    add_heading_1(doc, "CHAPTER FOUR")
    add_heading_1(doc, "RESULTS AND DISCUSSION")
    
    # Opening Paragraph
    add_academic_p(doc, "This chapter presents the results and discussion of the study based on the data collected from yam-farming households in Akpabuyo Local Government Area, Cross River State. The presentation is organized in accordance with the specific objectives of the study, covering the socio-economic characteristics of the respondents, household expenditure patterns, poverty status determination, factors associated with poverty, challenges faced by yam farmers, test of the research hypothesis, and a synthesized discussion of the major findings.")
    
    # -------------------------------------------------------------
    # 4.1 Socio-Economic Characteristics of Yam Farmers
    # -------------------------------------------------------------
    add_heading_2(doc, "4.1 Socio-Economic Characteristics of Yam Farmers")
    add_academic_p(doc, "The socio-economic attributes of farming households are fundamental determinants of their decision-making behavior, resource allocation efficiency, technology adoption, and overall economic welfare. In this study, the socio-economic characteristics investigated include sex, age, marital status, educational attainment, household size, yam farming experience, and engagement in supplementary (off-farm) income-generating activities. Table 4.1 presents a consolidated summary of these socio-economic characteristics for the 60 sampled yam-farming households in Akpabuyo Local Government Area.")
    
    # Consolidated Table 4.1
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
        # Sex
        ("Sex", "", "", ""),
        ("  Male", "36", "60.00", "—"),
        ("  Female", "24", "40.00", "—"),
        ("  Total", "60", "100.00", "—"),
        # Age
        ("Age of farmer (years)", "60", "100.00", "Mean = 46.03 ± 8.64 (Min = 30, Max = 63)"),
        # Marital Status
        ("Marital Status", "", "", ""),
        ("  Single", "5", "8.33", "—"),
        ("  Married", "49", "81.67", "—"),
        ("  Divorced", "0", "0.00", "—"),
        ("  Widowed", "6", "10.00", "—"),
        ("  Total", "60", "100.00", "—"),
        # Educational Attainment
        ("Educational Attainment", "", "", ""),
        ("  No Formal Education", "0", "0.00", "—"),
        ("  Primary Education (6 years)", "18", "30.00", "—"),
        ("  Secondary Education (12 years)", "27", "45.00", "—"),
        ("  Tertiary Education (16 years)", "15", "25.00", "—"),
        ("  Total", "60", "100.00", "—"),
        # Household Size
        ("Household Size (persons)", "60", "100.00", "Mean = 6.23 ± 1.84 (Min = 3, Max = 10)"),
        # Farming Experience
        ("Yam Farming Experience (years)", "60", "100.00", "Mean = 18.88 ± 8.56 (Min = 6, Max = 40)"),
        # Other Sources of Income
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
    
    # Subsections 4.1.1 to 4.1.7
    add_heading_3(doc, "4.1.1 Sex of Respondents")
    add_academic_p(doc, "Table 4.1 shows the socio-economic characteristics of the respondents. The results indicate that 36 respondents, representing 60.00% of the sample, were male, while 24 respondents, representing 40.00%, were female. This distribution reveals that yam farming in Akpabuyo Local Government Area is engaged in by both male and female farmers, with male farmers constituting the majority of enterprise managers. The notable representation of female farmers (40.00%) underscores their active role in arable crop production and household agricultural management within the study area.")
    
    add_heading_3(doc, "4.1.2 Age of Respondents")
    add_academic_p(doc, "The age of the sampled yam farmers averaged 46.03 years with a standard deviation of 8.64 years, spanning a minimum of 30 years and a maximum of 63 years. These summary statistics indicate that the sampled respondents were predominantly middle-aged and within an economically active stage of life. Figure 4.1 illustrates the empirical distribution of respondent age across the study sample.")
    
    # Figure 4.1
    add_figure_image(doc, "Figure_4_1_Age_Distribution.png", "Figure 4.1: Age Distribution of Yam Farmers in Akpabuyo LGA")
    
    add_heading_3(doc, "4.1.3 Marital Status of Respondents")
    add_academic_p(doc, "The marital status profile indicates that a substantial majority of the respondents were married (81.67%, n = 49), while 10.00% (n = 6) were widowed and 8.33% (n = 5) were single. No divorced respondents were recorded in the sample. The predominance of married individuals reflects the family-based organizational structure common in rural farming communities, where marital unions often facilitate the mobilization of household labour and joint economic resources for farm operations.")
    
    add_heading_3(doc, "4.1.4 Educational Attainment")
    add_academic_p(doc, "The educational attainment of the respondents reveals that all 60 farmers in the sample had completed some level of formal education (100.00%). Specifically, 45.00% (n = 27) had completed secondary education, 30.00% (n = 18) had completed primary education, and 25.00% (n = 15) had attained tertiary education. This high level of formal literacy provides a favorable foundation for agricultural communication, record-keeping, and the comprehension of farm advisory information.")
    
    add_heading_3(doc, "4.1.5 Household Size")
    add_academic_p(doc, "Household size among the sampled farmers averaged 6.23 persons with a standard deviation of 1.84 persons, ranging from a minimum of 3 persons to a maximum of 10 persons. In rural agrarian households, household size represents both the potential pool of family labour available for farm tasks and the consumption requirements that must be met from household income and agricultural output.")
    
    add_heading_3(doc, "4.1.6 Yam Farming Experience")
    add_academic_p(doc, "The farming experience of respondents averaged 18.88 years with a standard deviation of 8.56 years, ranging from 6 years to 40 years. This indicates that respondents possessed substantial practical experience in yam farming, reflecting long-term familiarity with local agricultural conditions and farming practices in the study area.")
    
    add_heading_3(doc, "4.1.7 Other Sources of Income")
    add_academic_p(doc, "The results in Table 4.1 show that 49 respondents (81.67%) engaged in supplementary or off-farm income-generating activities alongside yam farming, whereas 11 respondents (18.33%) depended solely on farming for their livelihood. This high rate of participation in supplementary income activities indicates widespread income diversification among farming households in Akpabuyo LGA.")

    # -------------------------------------------------------------
    # 4.2 Household Expenditure Pattern
    # -------------------------------------------------------------
    add_heading_2(doc, "4.2 Household Expenditure Pattern")
    add_academic_p(doc, "In smallholder agricultural settings where income flows are seasonal and non-continuous, household consumption expenditure provides an observable measure of household economic welfare and is therefore used in this study as the basis for poverty classification. In this study, monthly household expenditures across food and non-food budgetary categories were recorded to examine expenditure patterns and establish the empirical basis for poverty status measurement. Table 4.2 outlines the mean monthly household expenditure across major categories for the 60 sampled households in Akpabuyo LGA.")
    
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
    
    add_academic_p(doc, "As shown in Table 4.2, the reported total monthly household expenditure averaged ₦115,837.50 across the sampled households. Food and groceries accounted for the largest share of the household budget, averaging ₦60,703.33 per month and representing 52.40% of total expenditure. This dominant allocation to food consumption is consistent with standard household budget patterns in low- and middle-income rural areas. Non-food expenditures constituted 47.60% of total outlays, comprising housing and utilities (₦18,246.67; 15.75%), education expenses (₦14,528.33; 12.54%), transportation and other miscellaneous expenses (₦11,875.83; 10.25%), and health and medical care (₦8,631.67; 7.45%).")
    
    # Figure 4.2
    add_figure_image(doc, "Figure_4_2_Mean_Monthly_Expenditure.png", "Figure 4.2: Mean Monthly Household Expenditure by Category among Yam Farmers")
    
    add_academic_p(doc, "To account for differences in household size, Per-Capita Monthly Household Expenditure (PCHE) was computed by dividing reported monthly total expenditure by household size for each respondent. The mean PCHE across the sample was ₦20,289.03 per person per month, with a standard deviation of ₦9,896.79, ranging from ₦6,800.00 to ₦51,666.67. A neutral data-quality check indicated that for a minor subset of four households (Observations 14, 37, 39, and 59), slight differences existed between the arithmetic sum of the disaggregated expenditure components and the reported overall total expenditure. In accordance with established statistical practice, the reported total monthly expenditure was retained as the primary welfare metric because it represents the comprehensive expenditure figure recorded during survey administration and used in subsequent poverty analysis.")

    # -------------------------------------------------------------
    # 4.3 Poverty Status of Yam Farmers
    # -------------------------------------------------------------
    add_heading_2(doc, "4.3 Poverty Status of Yam Farmers")
    add_academic_p(doc, "In accordance with Objective 1 of the study, the poverty status of yam-farming households in Akpabuyo Local Government Area was determined using the relative poverty line method, followed by the computation of Foster, Greer, and Thorbecke (FGT, 1984) poverty indices.")
    
    add_heading_3(doc, "4.3.1 Determination of the Poverty Line")
    add_academic_p(doc, "Following the relative poverty-line approach adopted in this study, the poverty threshold was set at two-thirds (2/3) of mean Per-Capita Monthly Household Expenditure (PCHE). Given a mean PCHE of ₦20,289.03 per person per month across the 60 sampled households, the relative poverty line was derived as follows:")
    
    add_academic_p(doc, "Poverty Line (z) = 2/3 × Mean PCHE\n= 2/3 × ₦20,289.03\n= ₦13,526.02 per person per month.", space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    
    add_academic_p(doc, "Table 4.3 summarizes the parameters utilized in establishing the relative poverty line threshold.")
    
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
        ("Standard Deviation of PCHE", "₦9,896.79"),
        ("Minimum PCHE", "₦6,800.00"),
        ("Maximum PCHE", "₦51,666.67"),
        ("Poverty Line Definition", "Two-thirds (2/3) of Mean PCHE"),
        ("Established Relative Poverty Threshold (z)", "₦13,526.02 per person/month")
    ]
    
    for item in poverty_line_rows:
        row = table3.add_row()
        format_cell(row.cells[0], item[0], align=WD_ALIGN_PARAGRAPH.LEFT, bold=(item[0].startswith("Established")))
        format_cell(row.cells[1], item[1], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=(item[0].startswith("Established")))
        
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026.")
    
    add_heading_3(doc, "4.3.2 Poverty Incidence, Depth and Severity")
    add_academic_p(doc, "Households whose per-capita monthly expenditure fell below the established threshold of ₦13,526.02 were categorized as poor, while those with per-capita expenditure equal to or exceeding ₦13,526.02 were categorized as non-poor. The Foster-Greer-Thorbecke (FGT, 1984) indices were computed using the standard formula:")
    
    add_academic_p(doc, "P_α = (1 / N) * Σ [(z - y_i) / z]^α  for y_i < z", space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)
    
    add_academic_p(doc, "where N is the total sample size (N = 60), z is the poverty threshold (₦13,526.02), y_i is the per-capita monthly expenditure of the i-th poor household, and α is the poverty aversion parameter (0, 1, or 2). Table 4.4 presents the poverty status distribution and the estimated FGT indices.")
    
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
    
    # Figure 4.3
    add_figure_image(doc, "Figure_4_3_Poverty_Status.png", "Figure 4.3: Poverty Status Distribution of Yam Farmers in Akpabuyo LGA")
    
    add_academic_p(doc, "As shown in Table 4.4, out of the 60 sampled households, 13 households (21.67%) were classified as poor, while 47 households (78.33%) were classified as non-poor. The resulting Poverty Headcount Index (P0) of 0.2167 indicates that 21.67% of the sampled yam-farming households lived below the relative poverty threshold. The Poverty Gap Index (P₁) was 0.0232 (2.32%), indicating that poor households had an average expenditure deficit equivalent to 2.32% of the poverty line (approximately ₦313.42 per person per month). The Squared Poverty Gap Index (P2), which reflects poverty severity, was estimated at 0.0034 (0.34%), indicating low expenditure inequality among the poor households in the sample.")

    # -------------------------------------------------------------
    # 4.4 Factors Associated with Poverty Status
    # -------------------------------------------------------------
    add_heading_2(doc, "4.4 Factors Associated with Poverty Status")
    add_academic_p(doc, "In accordance with Objective 2 of the study, this section examines the socio-economic, asset-based, and institutional factors associated with poverty status among yam farmers. The analysis is presented in two parts: a bivariate analysis examining individual associations between explanatory variables and poverty status, followed by a multivariable binary logistic regression model assessing the simultaneous relationship of key predictors.")
    
    add_heading_3(doc, "4.4.1 Bivariate Analysis of Factors Associated with Poverty Status")
    add_academic_p(doc, "To assess bivariate associations, continuous variables were evaluated using the non-parametric Mann-Whitney U test, while categorical variables were evaluated using Pearson's Chi-square test (or Fisher's exact test for 2×2 tables with low expected cell counts). Table 4.5 presents the bivariate comparison between poor and non-poor yam-farming households across demographic, human capital, farm asset, and institutional variables.")
    
    add_table_title(doc, "Table 4.5: Bivariate Analysis of Factors Associated with Poverty Status (N = 60)")
    table5 = doc.add_table(rows=1, cols=6)
    table5.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table5)
    
    hdr5 = table5.rows[0].cells
    format_cell(hdr5[0], "Variable / Indicator", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True)
    format_cell(hdr5[1], "Poor (n = 13)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr5[2], "Non-Poor (n = 47)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr5[3], "Overall (N = 60)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr5[4], "Test Statistic", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr5[5], "p-value", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(table5.rows[0])
    
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
        row = table5.add_row()
        is_sec = (item[1] == "" and item[2] == "" and item[3] == "" and item[4] == "" and item[5] == "")
        format_cell(row.cells[0], item[0], align=WD_ALIGN_PARAGRAPH.LEFT, bold=is_sec)
        format_cell(row.cells[1], item[1], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_sec)
        format_cell(row.cells[2], item[2], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_sec)
        format_cell(row.cells[3], item[3], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_sec)
        format_cell(row.cells[4], item[4], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_sec)
        format_cell(row.cells[5], item[5], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=is_sec)
        
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026. * Significant at p < 0.05.")
    
    add_academic_p(doc, "Table 4.5 shows several statistically significant bivariate associations with household poverty status. Farmer age was significantly higher among poor households (mean = 51.31 ± 8.99 years) than non-poor households (mean = 44.57 ± 8.04 years; Mann-Whitney U = 432.00, p = 0.024). Household size also differed significantly between poor households (mean = 8.31 ± 1.70 persons) and non-poor households (mean = 5.66 ± 1.43 persons; Mann-Whitney U = 536.00, p < 0.001). Because per-capita expenditure is derived by dividing total household expenditure by household size, an inherent mechanical (arithmetic) negative relationship exists between household size and per-capita expenditure. Thus, the observed statistical association of household size should be interpreted in light of this arithmetic denominator property alongside any substantive dependency burden.")
    
    add_academic_p(doc, "Total farm size was significantly smaller among poor farmers (mean = 1.98 ± 0.48 ha) than non-poor farmers (mean = 2.56 ± 0.82 ha; Mann-Whitney U = 170.50, p = 0.016). Land area dedicated to yam cultivation averaged 1.43 ± 0.37 ha for poor farmers and 1.73 ± 0.56 ha for non-poor farmers, showing a positive difference that was not statistically significant at the 5% level (U = 205.00, p = 0.072).")
    
    add_academic_p(doc, "Among institutional variables, access to agricultural credit showed a statistically significant positive association with non-poor status (Chi-square = 9.820, p = 0.002), as 61.70% (n = 29) of non-poor farmers had credit access compared to 7.70% (n = 1) of poor farmers. Contact with agricultural extension agents in the preceding 12 months also differed significantly between groups (Fisher's exact test, p = 0.002), with 44.70% (n = 21) of non-poor farmers reporting extension contact compared to 0.00% (n = 0) among poor farmers. In contrast, educational attainment (p = 0.263), improved variety use (p = 1.000), fertilizer application (p = 0.481), modern tools (p = 0.324), and cooperative membership (p = 0.925) were not statistically significant at the 5% level. As this is a cross-sectional study, these bivariate findings represent observed empirical associations rather than evidence of direct causality.")

    # 4.4.2 Logistic Regression Analysis
    add_heading_3(doc, "4.4.2 Logistic Regression Analysis of Factors Associated with Poverty Status")
    add_academic_p(doc, "To examine the multivariable relationship between explanatory variables and household poverty status, a binary logistic regression model was estimated. The dependent variable was binary poverty status (1 = Poor, 0 = Non-poor).")
    
    add_academic_p(doc, "In accordance with standard econometric guidelines regarding events-per-variable (EPV) ratios, the model specification was constrained by the number of poor households in the sample (n = 13 events in N = 60). To prevent model overfitting, parameter distortion, and numerical instability, a parsimonious multivariable logistic regression model was specified with two primary predictors: total farm size (physical production asset) and access to credit (institutional capital). Table 4.6 presents the verified odds ratios and significance levels for the model.")
    
    add_table_title(doc, "Table 4.6: Binary Logistic Regression Model of Factors Associated with Poverty Status")
    table6 = doc.add_table(rows=1, cols=3)
    table6.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table6)
    
    hdr6 = table6.rows[0].cells
    format_cell(hdr6[0], "Predictor Variable", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True)
    format_cell(hdr6[1], "Odds Ratio (OR)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr6[2], "p-value", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(table6.rows[0])
    
    logit_rows = [
        ("Total farm size (ha)", "0.6505", "0.5979"),
        ("Access to credit (Yes = 1)", "0.0744", "0.0369*")
    ]
    
    for item in logit_rows:
        row = table6.add_row()
        format_cell(row.cells[0], item[0], align=WD_ALIGN_PARAGRAPH.LEFT, bold=False)
        format_cell(row.cells[1], item[1], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        format_cell(row.cells[2], item[2], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026. * Significant at p < 0.05.\nLikelihood Ratio χ² = 13.861 (df = 2, p = 0.000978); Nagelkerke R² = 0.3181.")
    
    add_academic_p(doc, "The omnibus test of model coefficients indicates that the specified logistic regression model is statistically significant overall (Likelihood Ratio χ² = 13.861, df = 2, p = 0.000978), demonstrating that the two predictors jointly provide a statistically significant fit over the null model. The model yielded a Nagelkerke pseudo-R² of 0.3181.")
    
    # Figure 4.4
    add_figure_image(doc, "Chapter_4_Analysis/Analysis_4_Factors_Poverty/Figure_4_4_Odds_Ratios_Factors_Poverty.png", "Figure 4.4: Odds Ratios from Binary Logistic Regression Model (95% CIs)")
    
    add_academic_p(doc, "Among the predictors, access to agricultural credit was statistically significant at the 5% level (OR = 0.0744, p = 0.0369), indicating that, holding farm size constant, yam-farming households with access to credit had 92.56% lower odds of being poor compared to households without credit access. Firth penalized likelihood logistic regression sensitivity analysis confirmed the association for access to credit (OR = 0.110, 95% CI: 0.014–0.891, p = 0.039). This indicates that access to credit was significantly associated with lower odds of being poor, although this reflects an observed statistical association rather than established direct causality.")
    
    add_academic_p(doc, "Total farm size yielded an odds ratio of 0.6505 but was not statistically significant in the multivariable model (p = 0.5979). While farm size showed a positive association with non-poor status in the bivariate analysis, it did not demonstrate an independent statistically significant association after conditioning on access to credit.")

    # -------------------------------------------------------------
    # 4.5 Challenges Faced by Yam Farmers
    # -------------------------------------------------------------
    add_heading_2(doc, "4.5 Challenges Faced by Yam Farmers")
    add_academic_p(doc, "In accordance with Objective 3 of the study, this section evaluates the severity of production, institutional, and marketing challenges faced by yam farmers in Akpabuyo Local Government Area. Ten potential challenges were rated by respondents using a structured 5-point Likert-type rating scale: 1 = Not a Challenge, 2 = Minor, 3 = Moderate, 4 = Severe, and 5 = Very Severe. Mean severity scores were classified into severity categories using the following intervals: 1.00–1.80 = Not a Challenge; 1.81–2.60 = Minor; 2.61–3.40 = Moderate; 3.41–4.20 = Severe; and 4.21–5.00 = Very Severe. Table 4.7 presents the challenges in descending order of mean severity.")
    
    add_table_title(doc, "Table 4.7: Severity Ranking of Challenges Faced by Yam Farmers in Akpabuyo LGA (N = 60)")
    table7 = doc.add_table(rows=1, cols=7)
    table7.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table7)
    
    hdr7 = table7.rows[0].cells
    format_cell(hdr7[0], "Rank", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    format_cell(hdr7[1], "Constraint / Challenge", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True)
    format_cell(hdr7[2], "Mean Score", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr7[3], "Std. Dev.", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr7[4], "Median", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr7[5], "IQR", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr7[6], "Severity Level", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(table7.rows[0])
    
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
        row = table7.add_row()
        format_cell(row.cells[0], item[0], align=WD_ALIGN_PARAGRAPH.CENTER, bold=False)
        format_cell(row.cells[1], item[1], align=WD_ALIGN_PARAGRAPH.LEFT, bold=False)
        format_cell(row.cells[2], item[2], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        format_cell(row.cells[3], item[3], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        format_cell(row.cells[4], item[4], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        format_cell(row.cells[5], item[5], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        format_cell(row.cells[6], item[6], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026. Severity intervals: 1.00–1.80 = Not a Challenge; 1.81–2.60 = Minor; 2.61–3.40 = Moderate; 3.41–4.20 = Severe; 4.21–5.00 = Very Severe.")
    
    # Figure 4.5
    add_figure_image(doc, "Chapter_4_Analysis/Analysis_5_Challenges/Figure_4_5_Challenge_Severity_Ranking.png", "Figure 4.5: Severity Ranking of Challenges Faced by Yam Farmers in Akpabuyo LGA")
    
    add_academic_p(doc, "As shown in Table 4.7, seven of the ten evaluated challenges fell within the 'Severe' category (mean score 3.41–4.20), while the remaining three challenges fell within the 'Moderate' category (mean score 2.61–3.40):")
    
    add_academic_p(doc, "1. High cost and scarcity of farm labour ranked highest in severity (mean = 4.15 ± 0.80, median = 4.00, Rank 1st; Severe), reflecting the labour-intensive nature of yam production operations including mound preparation, planting, staking, weeding, and harvesting.")
    
    add_academic_p(doc, "2. High cost of farm inputs ranked second (mean = 4.00 ± 0.96, median = 4.00, Rank 2nd; Severe), representing a major financial constraint on purchasing seed yams, fertilizers, and agrochemicals.")
    
    add_academic_p(doc, "3. Post-harvest losses and inadequate storage facilities ranked third (mean = 3.88 ± 0.99, median = 4.00, Rank 3rd; Severe), highlighting difficulties in storing harvested yam tubers safely and minimizing post-harvest spoilage.")
    
    add_academic_p(doc, "4. Unpredictable rainfall and climate conditions ranked fourth (mean = 3.70 ± 0.85, median = 4.00, Rank 4th; Severe), reflecting seasonal weather variability affecting rainfed yam cultivation.")
    
    add_academic_p(doc, "5. High cost and scarcity of yam stakes ranked fifth (mean = 3.57 ± 0.89, median = 4.00, Rank 5th; Severe), indicating constraints in procuring staking materials necessary for yam canopy support.")
    
    add_academic_p(doc, "6. Inadequate access to agricultural credit ranked sixth (mean = 3.53 ± 0.98, median = 3.00, Rank 6th; Severe), while inadequate agricultural extension services ranked seventh (mean = 3.52 ± 1.07, median = 4.00, Rank 7th; Severe), representing key institutional constraints faced by respondents.")
    
    add_academic_p(doc, "7. Pest and disease infestation (mean = 3.38 ± 0.83, Rank 8th; Moderate), low and unstable yam prices (mean = 3.12 ± 0.87, Rank 9th, n = 59; Moderate), and poor access to output markets (mean = 2.90 ± 1.02, Rank 10th; Moderate) were categorized as moderate challenges.")

    # -------------------------------------------------------------
    # 4.6 Test of Hypothesis
    # -------------------------------------------------------------
    add_heading_2(doc, "4.6 Test of Hypothesis")
    add_academic_p(doc, "To provide formal statistical evaluation of the study's framework, the research hypothesis was tested:")
    
    add_academic_p(doc, "H0: Socio-economic variables do not significantly influence the poverty status of yam farmers in Akpabuyo Local Government Area.", space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    
    # Exact wording requested
    add_academic_p(doc, "The parsimonious binary logistic regression model reported in Table 4.6 served as the principal multivariable test of the hypothesis. The omnibus Likelihood Ratio test was statistically significant (χ² = 13.861, df = 2, p = 0.000978), indicating that the specified two-predictor model provided a statistically significant improvement over the null model. Accordingly, the null hypothesis was rejected with respect to the specified multivariable model.")
    
    add_academic_p(doc, "Within the model, access to credit was significantly associated with poverty status (OR = 0.0744, p = 0.0369), whereas total farm size was not statistically significant (OR = 0.6505, p = 0.5979). Therefore, the findings do not imply that all socio-economic variables examined in the study were independently significant in the multivariable model. Rather, they indicate that the specified model was statistically significant overall, with access to credit showing the significant individual association.")

    # -------------------------------------------------------------
    # 4.7 Discussion of Major Findings
    # -------------------------------------------------------------
    add_heading_2(doc, "4.7 Discussion of Major Findings")
    add_academic_p(doc, "This section presents an integrated discussion of the empirical findings in relation to the study's three core research objectives:")
    
    add_academic_p(doc, "Regarding Objective 1 (Poverty Status and Expenditure Profile), the study established a relative poverty line of ₦13,526.02 per person per month (two-thirds of the mean PCHE of ₦20,289.03), resulting in a poverty headcount index (P0) of 21.67% (n = 13 poor households; n = 47 non-poor households). The poverty gap index (P1) of 0.0232 (2.32%) and squared poverty gap index (P2) of 0.0034 (0.34%) indicate that poverty depth and severity are relatively low among the sampled households. The observed poverty distribution shows that 78.33% of the sampled yam-farming households were non-poor, while 21.67% lived below the relative poverty threshold. Food expenditure accounted for 52.40% of the total monthly household budget (₦60,703.33 of ₦115,837.50), reflecting the prominence of food needs in rural household budgets.")
    
    add_academic_p(doc, "Regarding Objective 2 (Factors Associated with Poverty Status), the logistic regression analysis demonstrated that access to agricultural credit was significantly associated with lower odds of being poor (OR = 0.0744, p = 0.0369). Total farm size was not statistically significant in the multivariable model (OR = 0.6505, p = 0.5979). In bivariate evaluations, contact with extension agents (p = 0.002) and total farm size (p = 0.016) were positively associated with non-poor status, while older farmer age (p = 0.024) and larger household size (p < 0.001) were associated with poor status. As noted, the relationship with household size should be interpreted in light of the arithmetic denominator effect inherent in per-capita expenditure calculations.")
    
    add_academic_p(doc, "Regarding Objective 3 (Challenges Faced by Yam Farmers), the severity ranking identified labour cost/scarcity (mean = 4.15), high input prices (mean = 4.00), post-harvest storage losses (mean = 3.88), rainfall unpredictability (mean = 3.70), and stake scarcity (mean = 3.57) as severe constraints (mean score 3.41–4.20). Inadequate credit access (mean = 3.53) and extension services (mean = 3.52) also ranked as severe institutional constraints, while pest/disease infestation (mean = 3.38), price instability (mean = 3.12), and market access (mean = 2.90) were ranked as moderate challenges (mean score 2.61–3.40). Addressing these constraints through improved input accessibility, post-harvest storage support, and strengthened institutional services represents an important avenue for supporting yam-farming households in the study area.")
    
    # Save documents - Exactly as requested, saving Chapter_4_Results_and_Discussion_FINAL_v2.docx without overwriting previous FINAL
    out_final_v2 = "Chapter_4_Results_and_Discussion_FINAL_v2.docx"
    doc.save(out_final_v2)
    print(f"Successfully generated and saved: {out_final_v2}")

if __name__ == "__main__":
    generate_chapter_4_v2()

