# -*- coding: utf-8 -*-
"""
Rebuild Chapter Four: Results and Discussion
Study: Analysis of Poverty Status of Yam Farmers in Akpabuyo Local Government Area, Cross River State, Nigeria
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

def generate_full_chapter_4():
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
    format_cell(hdr_cells[0], "Variable / Category", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True)
    format_cell(hdr_cells[1], "Frequency (n)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr_cells[2], "Percentage (%)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr_cells[3], "Summary Statistics", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(table1.rows[0])
    
    # Table rows
    rows_data = [
        # Sex
        ("Sex", "", "", ""),
        ("  Male", "36", "60.00", "—"),
        ("  Female", "24", "40.00", "—"),
        ("  Total", "60", "100.00", "—"),
        # Age
        ("Age (years)", "", "", ""),
        ("  30 – 39", "15", "25.00", "Mean = 46.03 ± 8.64"),
        ("  40 – 49", "25", "41.67", "Std. Dev. = 8.64"),
        ("  50 – 59", "16", "26.67", "Min = 30, Max = 63"),
        ("  60 and above", "4", "6.67", "—"),
        ("  Total", "60", "100.00", "—"),
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
        ("Household Size (persons)", "", "", ""),
        ("  1 – 4 persons", "10", "16.67", "Mean = 6.23 ± 1.84"),
        ("  5 – 7 persons", "37", "61.67", "Std. Dev. = 1.84"),
        ("  8 – 10 persons", "13", "21.67", "Min = 3, Max = 10"),
        ("  Total", "60", "100.00", "—"),
        # Farming Experience
        ("Yam Farming Experience (years)", "", "", ""),
        ("  1 – 10 years", "12", "20.00", "Mean = 18.88 ± 8.56"),
        ("  11 – 20 years", "27", "45.00", "Std. Dev. = 8.56"),
        ("  21 – 30 years", "16", "26.67", "Min = 6, Max = 40"),
        ("  Above 30 years", "5", "8.33", "—"),
        ("  Total", "60", "100.00", "—"),
        # Other Sources of Income
        ("Other Sources of Income", "", "", ""),
        ("  Yes (Off-farm / Non-farm income)", "49", "81.67", "—"),
        ("  No (Solely farming)", "11", "18.33", "—"),
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
    add_academic_p(doc, "Table 4.1 shows the socio-economic characteristics of the respondents. The results indicate that 36 respondents, representing 60.00% of the sample, were male, while 24 respondents, representing 40.00%, were female. This distribution reveals that yam farming in Akpabuyo Local Government Area is engaged in by both males and females, although male farmers constitute the majority. In many traditional agrarian settings in southeastern and southern Nigeria, yam is historically cultivated under a gender-differentiated division of labour, where men frequently dominate heavy field tasks such as land clearing, mound construction, and staking, while women play indispensable roles in planting, seed selection, weeding, harvesting, processing, and marketing. The substantial proportion of female farmers (40.00%) indicates significant female involvement in direct yam enterprise management, reflecting the economic importance of yam production to female-headed and dual-earner rural households.")
    
    add_heading_3(doc, "4.1.2 Age of Respondents")
    add_academic_p(doc, "The age distribution of the sampled yam farmers shows that the respondents had a mean age of 46.03 years with a standard deviation of 8.64 years, spanning a minimum age of 30 years and a maximum age of 63 years. As shown in Table 4.1, exactly 41.67% of the respondents fell within the 40–49 age bracket, while 25.00% were aged 30–39 years, 26.67% were aged 50–59 years, and only 6.67% were 60 years or older. This demographic structure shows that the respondents were predominantly middle-aged and within their economically active years. Middle-aged farmers generally combine physical vigor with accumulated managerial experience, enabling them to handle the physically demanding operations characteristic of yam cultivation while making sound agronomic and enterprise decisions.")
    
    # Figure 4.1
    add_figure_image(doc, "Figure_4_1_Age_Distribution.png", "Figure 4.1: Age Distribution of Yam Farmers in Akpabuyo LGA")
    
    add_heading_3(doc, "4.1.3 Marital Status of Respondents")
    add_academic_p(doc, "The marital status profile reveals that a large majority of the respondents were married (81.67%, n = 49), followed by widowed individuals (10.00%, n = 6) and single respondents (8.33%, n = 5). No divorced individuals were recorded in the sample. The high prevalence of married farmers underscores the family-centered structure of smallholder agriculture in rural Akpabuyo. Marriage often fosters household stability and provides a vital institutional framework for pooling domestic and agricultural resources, particularly family labour, which is critical for reducing cash outlays on hired labour during peak farming operations such as planting, weeding, and harvesting.")
    
    add_heading_3(doc, "4.1.4 Educational Attainment")
    add_academic_p(doc, "The educational attainment of the respondents indicates a literate farming population. All sampled farmers had completed some level of formal schooling (100.00%), with none reporting no formal education. Specifically, 45.00% (n = 27) had completed secondary education, 30.00% (n = 18) had completed primary education, and 25.00% (n = 15) had attained tertiary education. This high level of educational attainment represents a significant human capital asset. Basic literacy and numeracy enhance farmers' capacity to interpret extension literature, adopt modern agronomic practices, keep farm financial records, and interact effectively with formal agricultural input and credit markets.")
    
    add_heading_3(doc, "4.1.5 Household Size")
    add_academic_p(doc, "Household size among the sampled respondents averaged 6.23 persons with a standard deviation of 1.84 persons, ranging from a minimum of 3 persons to a maximum of 10 persons. The majority of households (61.67%, n = 37) had between 5 and 7 members, while 21.67% (n = 13) had 8 to 10 members, and 16.67% (n = 10) had 1 to 4 members. In rural agricultural communities, larger households often serve a dual socio-economic function: on one hand, they supply essential family labour for farm operations, potentially mitigating labour constraints; on the other hand, larger household size increases consumption dependency, placing higher demands on household food and non-food budgetary resources.")
    
    add_heading_3(doc, "4.1.6 Yam Farming Experience")
    add_academic_p(doc, "The farming experience of respondents averaged 18.88 years with a standard deviation of 8.56 years, ranging from 6 years to 40 years. Nearly three-quarters of the respondents (71.67%, n = 43) had over 10 years of active experience in yam cultivation, comprising 45.00% (n = 27) with 11–20 years and 26.67% (n = 16) with 21–30 years of experience. Prolonged farming experience reflects deep familiarity with local soil types, seasonal rainfall patterns, pest management strategies, and market fluctuations, allowing experienced farmers to make informed production decisions and manage production risks effectively.")
    
    add_heading_3(doc, "4.1.7 Other Sources of Income")
    add_academic_p(doc, "The distribution of supplementary income sources indicates that 49 respondents (81.67%) engaged in off-farm or non-farm income-generating activities in addition to yam cultivation, while only 11 respondents (18.33%) relied solely on farm income. The supplementary income sources identified included petty trading, agro-processing (such as agricultural produce processing and palm oil extraction), artisanal trades, and livestock rearing. Livelihood diversification is a widely recognized risk-mitigation strategy among rural agrarian households, providing supplementary liquidity to finance farm inputs and household consumption during the off-season.")

    # -------------------------------------------------------------
    # 4.2 Household Expenditure Pattern
    # -------------------------------------------------------------
    add_heading_2(doc, "4.2 Household Expenditure Pattern")
    add_academic_p(doc, "In developing rural economies where formal income records are scarce and seasonal earnings fluctuate, household expenditure is widely recognized by development economists as a more reliable and stable proxy for permanent income and household economic welfare. In this study, monthly household expenditures across food and non-food budgetary categories were compiled to evaluate living standards and establish the empirical baseline for poverty status measurement. Table 4.2 outlines the mean monthly household expenditure across major expenditure categories for the 60 sampled households in Akpabuyo LGA.")
    
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
    
    add_academic_p(doc, "As shown in Table 4.2, the reported total monthly household expenditure averaged ₦115,837.50 across the sampled households. Food and groceries accounted for the largest proportion of total household expenditure, averaging ₦60,703.33 per month and representing 52.40% of the household budget. This substantial budget allocation to food is consistent with Engel's law of household expenditure, which posits that low- and middle-income households allocate a dominant share of their budgetary resources to meeting basic dietary requirements. Non-food expenditures constituted the remaining 47.60% of household outlays, comprising housing and utilities (₦18,246.67; 15.75%), education expenses (₦14,528.33; 12.54%), transportation and other miscellaneous needs (₦11,875.83; 10.25%), and health/medical care (₦8,631.67; 7.45%).")
    
    # Figure 4.2
    add_figure_image(doc, "Figure_4_2_Mean_Monthly_Expenditure.png", "Figure 4.2: Mean Monthly Household Expenditure by Category among Yam Farmers")
    
    add_academic_p(doc, "To adjust for variations in household size and establish an individualized measure of economic welfare, Per-Capita Monthly Household Expenditure (PCHE) was computed by dividing each household's reported monthly total expenditure by its corresponding household size. The mean PCHE across the sampled households was ₦20,289.03 per person per month, with a standard deviation of ₦9,896.79, ranging from a minimum of ₦6,800.00 to a maximum of ₦51,666.67. A neutral data-quality audit indicated that for a minor subset of four households (Observations 14, 37, 39, and 59), slight discrepancies existed between the arithmetic sum of disaggregated expenditure components and the reported overall total expenditure. In accordance with established statistical practice, the reported total monthly expenditure was retained as the authoritative primary welfare measure because it represents the comprehensive expenditure figure validated during field enumeration and utilized in subsequent poverty status classification.")

    # -------------------------------------------------------------
    # 4.3 Poverty Status of Yam Farmers
    # -------------------------------------------------------------
    add_heading_2(doc, "4.3 Poverty Status of Yam Farmers")
    add_academic_p(doc, "In accordance with Objective 1 of the study, the poverty status of yam-farming households in Akpabuyo Local Government Area was determined using the relative poverty line approach, followed by the computation of Foster, Greer, and Thorbecke (FGT, 1984) poverty indices.")
    
    add_heading_3(doc, "4.3.1 Determination of the Poverty Line")
    add_academic_p(doc, "The relative poverty threshold was established using the conventional benchmark of two-thirds (2/3) of the mean Per-Capita Monthly Household Expenditure (Mean PCHE), as widely applied in Nigerian poverty studies and the National Bureau of Statistics (NBS) living standards surveys. Given a mean PCHE of ₦20,289.03 per person per month across the 60 sampled households, the relative poverty line was calculated as follows:")
    
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
        ("Poverty Line Formula Definition", "Two-thirds (2/3) of Mean PCHE"),
        ("Established Relative Poverty Threshold (z)", "₦13,526.02 per person/month")
    ]
    
    for item in poverty_line_rows:
        row = table3.add_row()
        format_cell(row.cells[0], item[0], align=WD_ALIGN_PARAGRAPH.LEFT, bold=(item[0].startswith("Established")))
        format_cell(row.cells[1], item[1], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=(item[0].startswith("Established")))
        
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026.")
    
    add_heading_3(doc, "4.3.2 Poverty Incidence, Depth and Severity")
    add_academic_p(doc, "Households whose per-capita monthly household expenditure fell below the established threshold of ₦13,526.02 were categorized as poor, while those with per-capita expenditure equal to or exceeding ₦13,526.02 were categorized as non-poor. To quantify the extent and distribution of poverty, the Foster-Greer-Thorbecke (FGT) class of poverty measures was computed using the standard formulation:")
    
    add_academic_p(doc, "P_α = (1 / N) * Σ [(z - y_i) / z]^α  for y_i < z", space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)
    
    add_academic_p(doc, "where N is the total number of sampled households (N = 60), z is the poverty threshold (₦13,526.02), y_i is the per-capita monthly expenditure of the i-th poor household, and α is the poverty aversion parameter (taking values 0, 1, and 2). Table 4.4 presents the distribution of yam farmers by poverty status and the corresponding FGT poverty indices.")
    
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
    
    add_academic_p(doc, "As shown in Table 4.4, out of the 60 sampled yam-farming households, 13 households (21.67%) were classified as poor, while 47 households (78.33%) were classified as non-poor. The resulting Poverty Headcount Index (P0) of 0.2167 indicates that approximately 21.67% of the yam-farming population in Akpabuyo LGA lived below the relative poverty threshold at the time of the survey. The Poverty Gap Index (P1), which measures the depth of poverty or the average expenditure shortfall of poor households relative to the poverty line, was estimated at 0.0232 (2.32%). This low poverty depth suggests that on average, poor households required an expenditure increase equivalent to only 2.32% of the poverty line (approximately ₦313.80 per capita per month) to bridge their poverty deficit and reach the poverty threshold. Furthermore, the Squared Poverty Gap Index (P2), which reflects poverty severity and captures expenditure inequality among the poor, was estimated at 0.0034 (0.34%). This low severity index demonstrates that extreme destitution and severe within-poor inequality are minimal among the sampled yam-farming households.")

    # -------------------------------------------------------------
    # 4.4 Factors Associated with Poverty Status
    # -------------------------------------------------------------
    add_heading_2(doc, "4.4 Factors Associated with Poverty Status")
    add_academic_p(doc, "In accordance with Objective 2 of the study, this section investigates the socio-economic, asset-based, and institutional factors associated with poverty status among yam farmers. The analysis is presented in two complementary stages: first, a bivariate analysis examining individual associations between explanatory variables and poverty status; and second, a multivariable binary logistic regression model assessing the simultaneous influence of key predictors.")
    
    add_heading_3(doc, "4.4.1 Bivariate Analysis of Factors Associated with Poverty Status")
    add_academic_p(doc, "To identify bivariate patterns without imposing rigid distributional assumptions, continuous variables were evaluated using the non-parametric Mann-Whitney U test, while categorical variables were evaluated using Pearson's Chi-square test (or Fisher's exact test for 2×2 contingency tables with expected cell counts below 5). Table 4.5 presents the bivariate comparison between poor and non-poor yam-farming households across demographic, human capital, farm asset, and institutional variables.")
    
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
    
    add_academic_p(doc, "Table 4.5 demonstrates several statistically significant bivariate associations with household poverty status. Farmer age was significantly higher among poor households (mean = 51.31 ± 8.99 years) compared to non-poor households (mean = 44.57 ± 8.04 years; Mann-Whitney U = 432.00, p = 0.024). Household size also showed a statistically significant difference between the two groups (Mann-Whitney U = 536.00, p < 0.001), with poor households averaging 8.31 ± 1.70 members compared to 5.66 ± 1.43 members for non-poor households. However, it is essential to note a critical methodological consideration regarding household size: because per-capita expenditure is computed by dividing total household expenditure by household size, an inherent mechanical (arithmetic) negative relationship exists between household size and per-capita expenditure. Therefore, the observed statistical significance of household size reflects this arithmetic denominator effect in addition to any substantive economic dependency burden.")
    
    add_academic_p(doc, "Regarding land holdings, total farm size was significantly smaller among poor farmers (mean = 1.98 ± 0.48 ha) than non-poor farmers (mean = 2.56 ± 0.82 ha; Mann-Whitney U = 170.50, p = 0.016), indicating that land holding scale is positively associated with rural household welfare. Land dedicated to yam cultivation averaged 1.43 ± 0.37 ha for poor farmers and 1.73 ± 0.56 ha for non-poor farmers, showing a marginal difference that approached statistical significance (U = 205.00, p = 0.072).")
    
    add_academic_p(doc, "In terms of institutional access, access to agricultural credit exhibited a highly significant positive association with non-poor status (Chi-square = 9.820, p = 0.002). While 61.70% (n = 29) of non-poor farmers had access to credit facilities, only 7.70% (n = 1) of poor farmers reported credit access. Similarly, contact with agricultural extension agents in the preceding 12 months differed significantly between groups (Fisher's exact test, p = 0.002), as 44.70% (n = 21) of non-poor farmers had extension contacts compared to 0.00% (n = 0) among poor farmers. In contrast, educational attainment (p = 0.263), use of improved varieties (p = 1.000), fertilizer application (p = 0.481), modern tools (p = 0.324), and cooperative membership (p = 0.925) did not attain statistical significance at the 5% level. These bivariate findings highlight observed associations across demographic, asset, and institutional dimensions, although they should be interpreted as correlations rather than conclusive evidence of direct causality.")

    # 4.4.2 Logistic Regression Analysis
    add_heading_3(doc, "4.4.2 Logistic Regression Analysis of Factors Associated with Poverty Status")
    add_academic_p(doc, "To evaluate the multivariable relationship between explanatory variables and household poverty status, a binary logistic regression model was estimated. The dependent variable was defined as household poverty status (1 = Poor, 0 = Non-poor).")
    
    add_academic_p(doc, "A critical econometric requirement in logistic regression modeling is the events-per-variable (EPV) ratio. In this study's sample of N = 60 households, exactly 13 households experienced the outcome of interest (poverty, n = 13). Fitting a highly parameterized multivariable model with eight or nine predictors would severely violate the standard EPV guidelines (which recommend 10 to 15 events per predictor variable), leading to severe numerical instability, inflated standard errors, and overfitting. Consequently, a final parsimonious logistic regression model was specified, retaining two theoretically grounded and statistically viable predictors: total farm size (a key physical production asset) and access to credit (a primary institutional capital indicator). Table 4.6 presents the parameter estimates, standard errors, z-statistics, odds ratios, 95% confidence intervals, and goodness-of-fit metrics for the model.")
    
    add_table_title(doc, "Table 4.6: Binary Logistic Regression Model of Factors Associated with Poverty Status")
    table6 = doc.add_table(rows=1, cols=7)
    table6.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table6)
    
    hdr6 = table6.rows[0].cells
    format_cell(hdr6[0], "Predictor Variable", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True)
    format_cell(hdr6[1], "Coefficient (β)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr6[2], "Standard Error", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr6[3], "z-statistic", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr6[4], "Odds Ratio (OR)", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr6[5], "95% CI for OR", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    format_cell(hdr6[6], "p-value", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    add_header_bottom_border(table6.rows[0])
    
    logit_rows = [
        ("Total farm size (ha)", "-0.430", "0.815", "-0.528", "0.651", "0.132 – 3.217", "0.598"),
        ("Access to credit (Yes = 1)", "-2.598", "1.245", "-2.087", "0.074", "0.007 – 0.854", "0.037*"),
        ("Constant (Intercept)", "0.433", "1.628", "0.266", "1.542", "0.063 – 37.458", "0.790")
    ]
    
    for item in logit_rows:
        row = table6.add_row()
        format_cell(row.cells[0], item[0], align=WD_ALIGN_PARAGRAPH.LEFT, bold=False)
        format_cell(row.cells[1], item[1], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        format_cell(row.cells[2], item[2], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        format_cell(row.cells[3], item[3], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        format_cell(row.cells[4], item[4], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        format_cell(row.cells[5], item[5], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        format_cell(row.cells[6], item[6], align=WD_ALIGN_PARAGRAPH.RIGHT, bold=False)
        
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026. * Significant at p < 0.05.\nModel Diagnostics: Likelihood Ratio χ² = 13.861 (df = 2, p = 0.000978); Nagelkerke R² = 0.3181; Cox & Snell R² = 0.2063; Log-Likelihood = -24.719; AIC = 55.438.")
    
    add_academic_p(doc, "The omnibus test of model coefficients indicates that the estimated logistic regression model is statistically significant overall (Likelihood Ratio χ² = 13.861, df = 2, p = 0.000978), confirming that the specified predictors jointly provide a significant fit over the intercept-only null model. The model yielded a Nagelkerke pseudo-R² of 0.3181 and a Cox and Snell pseudo-R² of 0.2063, indicating that approximately 31.81% of the variation in household poverty status is explained by the included covariates.")
    
    # Figure 4.4
    add_figure_image(doc, "Chapter_4_Analysis/Analysis_4_Factors_Poverty/Figure_4_4_Odds_Ratios_Factors_Poverty.png", "Figure 4.4: Odds Ratios from Binary Logistic Regression Model (95% CIs)")
    
    add_academic_p(doc, "Among the individual predictors, access to agricultural credit was negative and statistically significant at the 5% level (β = -2.598, SE = 1.245, z = -2.087, p = 0.0369). The estimated odds ratio of 0.0744 (95% CI: 0.007–0.854) indicates that, holding total farm size constant, yam-farming households with access to credit had 92.56% lower odds of being poor compared to households without credit access. To verify the robustness of this finding against small-sample properties, a Firth penalized likelihood logistic regression sensitivity analysis was conducted; the Firth estimate confirmed a statistically significant protective association for credit access (OR = 0.110, 95% CI: 0.014–0.891, p = 0.039). This finding demonstrates that access to agricultural credit is strongly associated with enhanced household welfare, likely because credit liquidity enables smallholders to purchase essential farm inputs in a timely manner, hire labour during critical operations, and smooth household consumption during inter-harvest periods. However, this result should be understood as an empirical association rather than definitive evidence of direct causation, as credit access may also reflect broader unobserved creditworthiness or entrepreneurial capacity.")
    
    add_academic_p(doc, "In contrast, total farm size exhibited a negative coefficient (β = -0.430, SE = 0.815, OR = 0.6505, 95% CI: 0.132–3.217) but did not attain statistical significance in the multivariable model (p = 0.5979). While larger farm size was associated with non-poor status in the bivariate analysis, its independent statistical effect was attenuated after controlling for credit access. This suggests that the welfare benefits of land ownership in the study area are contingent upon the financial capability to cultivate and manage land holdings effectively.")

    # -------------------------------------------------------------
    # 4.5 Challenges Faced by Yam Farmers
    # -------------------------------------------------------------
    add_heading_2(doc, "4.5 Challenges Faced by Yam Farmers")
    add_academic_p(doc, "In accordance with Objective 3 of the study, this section assesses the severity of production, institutional, and marketing constraints encountered by yam farmers in Akpabuyo Local Government Area. Ten potential challenges were evaluated by respondents using a structured 5-point Likert-type rating scale, coded as: 1 = Not a Problem, 2 = Minor Problem, 3 = Moderate Problem, 4 = Severe Problem, and 5 = Very Severe Problem. Mean severity scores, standard deviations, medians, interquartile ranges (IQR), and overall severity rankings were calculated. Table 4.7 presents the challenges in descending order of mean severity.")
    
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
        ("2nd", "High cost of farm inputs (fertilizer, seeds, agrochemicals)", "4.00", "0.96", "4.00", "2.00", "Severe"),
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
        
    add_table_source(doc, "Source: Field Survey Data Analysis, 2026. Severity classification based on mean scores: 1.00–2.49 = Low; 2.50–3.49 = Moderate; 3.50–5.00 = Severe.")
    
    # Figure 4.5
    add_figure_image(doc, "Chapter_4_Analysis/Analysis_5_Challenges/Figure_4_5_Challenge_Severity_Ranking.png", "Figure 4.5: Severity Ranking of Challenges Faced by Yam Farmers in Akpabuyo LGA")
    
    add_academic_p(doc, "As shown in Table 4.7, seven of the ten evaluated challenges were classified as severe (mean score ≥ 3.50), while the remaining three challenges were classified as moderate (mean score 2.50–3.49). The highest-ranked constraint was the high cost and scarcity of farm labour (mean = 4.15 ± 0.80, median = 4.00, Rank 1st). Yam production is inherently labour-intensive, requiring manual labour for bush clearing, mound making, sett planting, staking, periodic weeding, and harvesting. In Akpabuyo LGA, rural-to-urban youth migration and competition from non-farm employment have depleted the agricultural workforce, inflating daily wage rates and escalating production costs.")
    
    add_academic_p(doc, "The second most severe constraint was the high cost of farm inputs, including seed yams (setts), inorganic fertilizers, and agrochemicals (mean = 4.00 ± 0.96, median = 4.00, Rank 2nd). Seed yams represent the single largest capital outlay in yam enterprise establishment, often accounting for 30% to 50% of total production costs. Coupled with escalating prices of fertilizers and crop protection chemicals, high input costs severely constrain farmers' ability to expand cultivation scale and optimize crop yields.")
    
    add_academic_p(doc, "Post-harvest losses and inadequate storage facilities ranked third in severity (mean = 3.88 ± 0.99, median = 4.00, Rank 3rd). Yam tubers are perishable biological products susceptible to physiological respiration, rotting, nematode damage, and rodent attack during storage. In the absence of modern, ventilated, and pest-resistant barn storage structures, farmers incur substantial physical and economic losses, frequently forcing them to sell their harvest immediately at depressed post-harvest farmgate prices.")
    
    add_academic_p(doc, "Unpredictable rainfall and changing climatic conditions ranked fourth (mean = 3.70 ± 0.85, median = 4.00, Rank 4th), reflecting the vulnerability of rainfed yam production to erratic rainfall onsets, prolonged mid-season dry spells, and excessive precipitation causing waterlogging and tuber rot. High cost and scarcity of yam stakes ranked fifth (mean = 3.57 ± 0.89, median = 4.00, Rank 5th), driven by local deforestation, agricultural land clearance, and competition for wooden poles, which increases staking costs essential for maximizing photosynthetic leaf exposure and tuber yields.")
    
    add_academic_p(doc, "Institutional challenges also featured prominently among the severe constraints: inadequate access to agricultural credit ranked sixth (mean = 3.53 ± 0.98, median = 3.00, Rank 6th), while inadequate agricultural extension services ranked seventh (mean = 3.52 ± 1.07, median = 4.00, Rank 7th). These institutional deficits restrict smallholders' working capital and deny them timely advisory support regarding improved agronomic practices and pest management. Finally, pest and disease infestation (mean = 3.38 ± 0.83, Rank 8th), low and unstable yam prices (mean = 3.12 ± 0.87, Rank 9th, n = 59), and poor access to output markets (mean = 2.90 ± 1.02, Rank 10th) were identified as moderate production and marketing constraints.")

    # -------------------------------------------------------------
    # 4.6 Test of Hypothesis
    # -------------------------------------------------------------
    add_heading_2(doc, "4.6 Test of Hypothesis")
    add_academic_p(doc, "To provide formal inferential verification for the research framework, the approved null hypothesis formulated for this study was tested:")
    
    add_academic_p(doc, "H0: Socio-economic variables do not significantly influence the poverty status of yam farmers in Akpabuyo Local Government Area.", space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    
    add_academic_p(doc, "The binary logistic regression model reported in Table 4.6 served as the principal analytical test for evaluating this hypothesis. The omnibus Likelihood Ratio test yielded a chi-square statistic of χ² = 13.861 with 2 degrees of freedom, which was statistically significant at p = 0.000978 (p < 0.001). Because the omnibus model p-value is substantially below the standard 5% significance threshold (α = 0.05), the null hypothesis (H0) is rejected. It is therefore concluded that socio-economic variables collectively exert a statistically significant influence on the poverty status of yam farmers in Akpabuyo Local Government Area.")
    
    add_academic_p(doc, "At the individual variable level within the multivariable framework, access to agricultural credit demonstrated a statistically significant influence on poverty status (β = -2.598, SE = 1.245, z = -2.087, p = 0.0369, OR = 0.0744), indicating that credit access significantly reduces the odds of being poor. Total farm size, while exhibiting a negative coefficient (β = -0.430, p = 0.5979), was not statistically significant after conditioning on credit access. In addition, supporting bivariate tests demonstrated that farmer age (p = 0.024), household size (p < 0.001), total farm size (p = 0.016), access to credit (p = 0.002), and agricultural extension contact (p = 0.002) were individually associated with household poverty status.")

    # -------------------------------------------------------------
    # 4.7 Discussion of Major Findings
    # -------------------------------------------------------------
    add_heading_2(doc, "4.7 Discussion of Major Findings")
    add_academic_p(doc, "This section presents an integrated discussion of the empirical findings in relation to the study's three core research objectives and relevant empirical literature in Agricultural Economics.")
    
    add_academic_p(doc, "Regarding Objective 1 (Poverty Status and Expenditure Profile), the study established a relative poverty line of ₦13,526.02 per person per month (two-thirds of the mean PCHE of ₦20,289.03), resulting in a poverty headcount index (P0) of 21.67% (n = 13 poor households; n = 47 non-poor households). The poverty gap index (P1) of 0.0232 (2.32%) and squared poverty gap index (P2) of 0.0034 (0.34%) indicate that poverty among the sampled yam farmers is relatively shallow, with low inequality among the poor. The budgetary expenditure analysis demonstrated that food consumption absorbs 52.40% of total household expenditure (₦60,703.33 of ₦115,837.50), reflecting the high vulnerability of rural households to food price inflation in accordance with Engel's law. The moderate poverty headcount rate of 21.67% suggests that commercial yam production provides a viable livelihood base that lifts a substantial majority of participating households above the relative poverty threshold.")
    
    add_academic_p(doc, "Regarding Objective 2 (Factors Associated with Poverty Status), the empirical analysis demonstrated that institutional capital and physical production assets are closely linked to household economic welfare. In the multivariable logistic regression model, access to agricultural credit emerged as a statistically significant predictor (p = 0.0369, OR = 0.0744), confirming that credit-constrained households face markedly higher odds of poverty. Credit liquidity enables farmers to procure quality seed yams, purchase fertilizers and agrochemicals, and hire seasonal labour during peak cultivation windows. Furthermore, bivariate analyses revealed that contact with agricultural extension agents (p = 0.002) and total farm size (p = 0.016) were positively associated with non-poor status, while older farmer age (p = 0.024) and larger household size (p < 0.001) were associated with poor status. However, the apparent effect of household size must be interpreted cautiously due to the arithmetic denominator effect in per-capita expenditure calculations. These findings underscore the importance of targeted institutional support—specifically accessible rural credit facilities and strengthened extension advisory services—in promoting rural welfare.")
    
    add_academic_p(doc, "Regarding Objective 3 (Challenges Faced by Yam Farmers), the severity ranking identified labour scarcity and high labour costs (mean = 4.15), high input prices (mean = 4.00), post-harvest storage losses (mean = 3.88), rainfall unpredictability (mean = 3.70), and stake scarcity (mean = 3.57) as the primary constraints facing yam producers. These production bottlenecks reflect the high labor intensity and biological vulnerabilities of yam cultivation. Addressing these challenges requires concerted policy interventions, including the development and dissemination of low-cost yam storage technologies, promotion of affordable stake-saving cultivation techniques (such as minisetts and trellis systems), establishment of flexible micro-credit delivery mechanisms, and reinforcement of public agricultural extension systems in Akpabuyo Local Government Area.")
    
    # Save documents
    out_path1 = "Chapter_4_Analysis/Chapter_4_Merged.docx"
    out_path2 = "Chapter_4_Results_and_Discussion.docx"
    
    doc.save(out_path1)
    doc.save(out_path2)
    print(f"Successfully generated and saved:\n1. {out_path1}\n2. {out_path2}")

if __name__ == "__main__":
    generate_full_chapter_4()
