# -*- coding: utf-8 -*-
import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

def set_cell_border(cell, **kwargs):
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key in ["val", "color", "sz", "space"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))

def format_table_apa(table):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        tblBorders = tblPr[0].xpath('w:tblBorders')
        if tblBorders:
            tblPr[0].remove(tblBorders[0])
            
    num_rows = len(table.rows)
    for r_idx, row in enumerate(table.rows):
        trPr = row._element.get_or_add_trPr()
        trPr.append(parse_xml(r'<w:cantSplit xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))
        if r_idx == 0:
            trPr.append(parse_xml(r'<w:tblHeader xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))

        for c_idx, cell in enumerate(row.cells):
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            tcPr = cell._element.get_or_add_tcPr()
            tcMar = parse_xml(r'<w:tcMar xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                              r'<w:top w:w="80" w:type="dxa"/>'
                              r'<w:bottom w:w="80" w:type="dxa"/>'
                              r'<w:left w:w="120" w:type="dxa"/>'
                              r'<w:right w:w="120" w:type="dxa"/>'
                              r'</w:tcMar>')
            tcPr.append(tcMar)
            
            border_kwargs = {}
            if r_idx == 0:
                border_kwargs['top'] = {"val": "single", "sz": "12", "color": "000000"}
                border_kwargs['bottom'] = {"val": "single", "sz": "6", "color": "000000"}
            elif r_idx == num_rows - 1:
                border_kwargs['bottom'] = {"val": "single", "sz": "12", "color": "000000"}
            
            if border_kwargs:
                set_cell_border(cell, **border_kwargs)

def add_title_p(doc, text, bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=12):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_styled(doc, text, level):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5
    
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    
    if level == 1:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run.font.size = Pt(14)
    elif level == 2:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run.font.size = Pt(13)
    elif level == 3:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run.font.size = Pt(12)
    return p

def add_body_p(doc, text, bold_prefix=None, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = align
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
        
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.italic = italic
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_image_with_caption(doc, image_path, caption_text, width_in=5.5):
    if os.path.exists(image_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(image_path, width=Inches(width_in))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(11)
        r_cap.bold = True

def add_table_data(doc, title_text, data, note_text=None):
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run(title_text)
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(11)
    r_title.bold = True
    
    num_rows = len(data)
    num_cols = len(data[0])
    table = doc.add_table(rows=num_rows, cols=num_cols)
    for r_idx, row_vals in enumerate(data):
        for c_idx, val in enumerate(row_vals):
            cell = table.rows[r_idx].cells[c_idx]
            cell.text = str(val)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)
                if r_idx == 0:
                    run.bold = True
    format_table_apa(table)
    
    if note_text:
        p_note = doc.add_paragraph()
        p_note.paragraph_format.space_before = Pt(2)
        p_note.paragraph_format.space_after = Pt(8)
        p_note.paragraph_format.line_spacing = 1.15
        r_note = p_note.add_run(note_text)
        r_note.font.name = 'Times New Roman'
        r_note.font.size = Pt(10)
        r_note.italic = True

def build_final_thesis():
    doc = docx.Document()
    
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    print("1. Preliminary Pages...")
    # Title Page
    add_title_p(doc, "ANALYSIS OF POVERTY STATUS OF YAM FARMERS IN AKPABUYO LOCAL GOVERNMENT AREA, CROSS RIVER STATE, NIGERIA", size=14, space_before=36, space_after=24)
    add_title_p(doc, "BY", size=12, space_before=12, space_after=12)
    add_title_p(doc, "FAGBUYI OLAYINKA FAITH\n20/011145065", size=12, space_before=12, space_after=24)
    add_title_p(doc, "DEPARTMENT OF AGRICULTURAL ECONOMICS\nFACULTY OF AGRICULTURE\nUNIVERSITY OF CALABAR, CALABAR", size=12, space_before=12, space_after=24)
    add_title_p(doc, "A RESEARCH PROJECT SUBMITTED TO THE DEPARTMENT OF AGRICULTURAL ECONOMICS, FACULTY OF AGRICULTURE, UNIVERSITY OF CALABAR, CALABAR, IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE AWARD OF THE DEGREE OF BACHELOR OF AGRICULTURE (B. AGRIC.) IN AGRICULTURAL ECONOMICS", size=12, space_before=12, space_after=36)
    add_title_p(doc, "SEPTEMBER, 2026", size=12, space_before=24, space_after=12)
    doc.add_page_break()

    # Certification
    add_heading_styled(doc, "CERTIFICATION", level=1)
    add_body_p(doc, "This is to certify that this research project titled \"ANALYSIS OF POVERTY STATUS OF YAM FARMERS IN AKPABUYO LOCAL GOVERNMENT AREA, CROSS RIVER STATE, NIGERIA\" was carried out by FAGBUYI OLAYINKA FAITH (Matriculation Number: 20/011145065) in the Department of Agricultural Economics, Faculty of Agriculture, University of Calabar, Calabar, Nigeria, under the supervision of Assoc. Prof. E. Agbachom.")
    doc.add_paragraph().paragraph_format.space_after = Pt(36)
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.line_spacing = 1.5
    p_sign.add_run("_____________________________________\t\t________________________\n").bold = True
    p_sign.add_run("Assoc. Prof. E. Agbachom\t\t\t\t\tDate\n(Supervisor)\n\n\n").bold = True
    p_sign.add_run("_____________________________________\t\t________________________\n").bold = True
    p_sign.add_run("Dr. E. A. Ajah\t\t\t\t\t\tDate\n(Head of Department)").bold = True
    doc.add_page_break()

    # Dedication
    add_heading_styled(doc, "DEDICATION", level=1)
    add_body_p(doc, "This research project is dedicated to God Almighty, the source of all wisdom, knowledge, and understanding, whose grace, mercy, and guidance sustained me throughout the duration of this academic programme.")
    add_body_p(doc, "It is also dedicated to my beloved family and mentors for their unceasing love, sacrifices, prayers, and steadfast moral and financial support.")
    doc.add_page_break()

    # Acknowledgements
    add_heading_styled(doc, "ACKNOWLEDGEMENTS", level=1)
    add_body_p(doc, "First and foremost, I express my profound gratitude to God Almighty for His infinite mercies, protection, and divine provision throughout my undergraduate studies at the University of Calabar.")
    add_body_p(doc, "I wish to express my deepest gratitude and sincere appreciation to my project supervisor, Assoc. Prof. E. Agbachom, for his invaluable academic guidance, meticulous supervision, constructive criticism, and continuous encouragement throughout the execution of this research work. His scholarly insights and dedication greatly enriched this study.")
    add_body_p(doc, "My sincere appreciation goes to the Head of Department, Dr. E. A. Ajah, and to all the academic and non-teaching staff of the Department of Agricultural Economics, Faculty of Agriculture, University of Calabar, for their pedagogical dedication and administrative support.")
    add_body_p(doc, "I am immensely grateful to my beloved sister, Mrs. Bolade Nyambi, and her husband, Mr. Akpet Nyambi, for their unwavering moral, spiritual, and financial backing throughout my academic journey. Your encouragement has been an anchor of support.")
    add_body_p(doc, "I also extend my sincere appreciation to my esteemed colleagues, friends, and family—especially Akintunde, Idris, and Ruth—for their constant prayers, motivation, camaraderie, and assistance during field data collection and document preparation.")
    add_body_p(doc, "Finally, my profound thanks go to all the yam-farming household heads in Akpabuyo Local Government Area who patiently participated in the survey and generously shared their household and farm production information.")
    doc.add_page_break()

    # Abstract
    add_heading_styled(doc, "ABSTRACT", level=1)
    abstract_text = (
        "This study analyzed the poverty status of yam farmers in Akpabuyo Local Government Area of Cross River State, Nigeria. "
        "The specific objectives were to: (i) determine the poverty status of yam farmers using appropriate poverty measures; "
        "(ii) analyze the poverty status profile of yam farmers across socioeconomic, farm asset, and expenditure characteristics; "
        "(iii) analyze factors associated with poverty status in the study area; and (iv) measure the challenges faced by yam farmers. "
        "Primary data were collected from a sample of 60 yam-farming households across six selected communities using a multi-stage sampling procedure "
        "and structured questionnaires administered through face-to-face interviews. Data were analyzed using descriptive statistics, "
        "the Foster-Greer-Thorbecke (FGT) poverty index, bivariate inferential tests (Mann–Whitney U tests for continuous variables where appropriate, "
        "and Pearson's chi-square and Fisher's exact tests for categorical variables), a parsimonious binary logistic regression model with Firth penalized "
        "sensitivity estimation, and a 5-point Likert Mean Severity Index (MSI). "
        "Following the relative poverty-line approach adopted in this study, the poverty threshold was set at two-thirds (2/3) of mean Per-Capita Monthly Household "
        "Expenditure (PCHE), establishing a relative poverty line of ₦13,526.02 per person per month based on a mean monthly PCHE of ₦20,289.03. "
        "The poverty headcount index (P₀) was 0.2167, indicating that 21.67% (n = 13) of yam farmers were classified as poor, while 78.33% (n = 47) "
        "were non-poor. The poverty gap index (P₁) was 0.0232 (mean expenditure shortfall of ₦313.42 per person per month across the entire sample "
        "and ₦1,446.53 among poor households), and the poverty severity index (P₂) was 0.0034, indicating relatively low poverty severity within the sampled population. "
        "The descriptive poverty status profile revealed that poor households had larger family sizes (8.31 ± 1.70 vs. 5.66 ± 1.43 persons), "
        "older household heads (51.31 ± 8.99 vs. 44.57 ± 8.04 years), greater yam farming experience (25.77 ± 10.48 vs. 16.98 ± 6.94 years), "
        "smaller total farm holdings (1.98 ± 0.48 vs. 2.56 ± 0.82 ha), smaller yam cultivated area (1.43 ± 0.37 vs. 1.73 ± 0.56 ha), "
        "substantially lower access to agricultural credit (7.69% vs. 61.70%), lower extension contact (0.00% vs. 44.68%), and lower mean per-capita "
        "expenditure (₦12,079.49 vs. ₦22,559.76), despite comparable gross monthly household expenditures (₦101,000.00 vs. ₦119,941.49). "
        "Bivariate inferential tests established statistically significant associations with poverty status for household size (Mann–Whitney U = 536.00, p < 0.001), "
        "total farm size (Mann–Whitney U = 170.50, p = 0.016), farmer age (Mann–Whitney U = 432.00, p = 0.024), access to credit (χ² = 9.820, p = 0.002), "
        "and agricultural extension contact (Fisher's exact p = 0.002). "
        "In the multivariable logistic regression model, access to credit was significantly associated with lower odds of poverty "
        "(OR = 0.0744, p = 0.0369; Firth OR = 0.1100, p = 0.0390), indicating that farmers with access to credit had approximately 92.56% lower odds "
        "of being classified as poor, holding farm size constant, while total farm size was not statistically significant after conditioning on credit "
        "(OR = 0.6505, p = 0.5979; LR χ² = 13.861, df = 2, p = 0.000978; Nagelkerke R² = 0.3181). "
        "The principal production challenges identified based on the 5-point Likert Mean Severity Index were high cost and scarcity of farm labour (MSI = 4.15, Rank 1st; Severe), "
        "high cost of farm inputs (MSI = 4.00, Rank 2nd; Severe), post-harvest losses and inadequate storage facilities (MSI = 3.88, Rank 3rd; Severe), "
        "unpredictable rainfall and climate conditions (MSI = 3.70, Rank 4th; Severe), high cost and scarcity of yam stakes (MSI = 3.57, Rank 5th; Severe), "
        "inadequate access to agricultural credit (MSI = 3.53, Rank 6th; Severe), and inadequate agricultural extension services (MSI = 3.52, Rank 7th; Severe). "
        "The study recommends establishing tailored agricultural microcredit schemes for smallholder yam farmers, strengthening public and cooperative extension "
        "delivery, subsidizing critical farm inputs, and introducing low-cost modern yam storage facilities to reduce post-harvest deterioration."
    )
    add_body_p(doc, abstract_text)
    add_body_p(doc, "Keywords: Yam farmers, Poverty status, FGT poverty indices, Poverty status profile, Logistic regression, Akpabuyo LGA, Cross River State.", italic=True)
    doc.add_page_break()

    # Table of Contents
    add_heading_styled(doc, "TABLE OF CONTENTS", level=1)
    toc_items = [
        ("Title Page", "i"),
        ("Certification", "ii"),
        ("Dedication", "iii"),
        ("Acknowledgements", "iv"),
        ("Abstract", "v"),
        ("Table of Contents", "vi"),
        ("List of Tables", "viii"),
        ("List of Figures", "ix"),
        ("CHAPTER ONE: INTRODUCTION", "1"),
        ("  1.1 Background to the Study", "1"),
        ("  1.2 Statement of the Problem", "4"),
        ("  1.3 Research Questions", "6"),
        ("  1.4 Aim and Objectives of the Study", "6"),
        ("    1.4.1 Aim of the Study", "6"),
        ("    1.4.2 Specific Objectives", "6"),
        ("  1.5 Research Hypotheses", "7"),
        ("  1.6 Significance of the Study", "7"),
        ("  1.7 Scope of the Study", "9"),
        ("  1.8 Definition of Key Terms", "9"),
        ("CHAPTER TWO: LITERATURE REVIEW", "11"),
        ("  2.1 Conceptual Review", "11"),
        ("    2.1.1 Concept of Poverty", "11"),
        ("    2.1.2 Rural Poverty and Agriculture", "12"),
        ("    2.1.3 Concept and Measurement of Poverty", "14"),
        ("    2.1.4 Poverty among Smallholder Farmers", "16"),
        ("    2.1.5 Yam Farming and Household Welfare", "18"),
        ("  2.2 Theoretical Framework", "20"),
        ("    2.2.1 Theory of Production", "20"),
        ("    2.2.2 Theory of Livelihoods", "23"),
        ("    2.2.3 Basic Needs Perspective", "25"),
        ("    2.2.4 Asset-Based Livelihood Framework", "26"),
        ("    2.2.5 Human Capital and Farm Productivity", "27"),
        ("    2.2.6 Risk, Vulnerability, and Rural Poverty", "28"),
        ("  2.3 Empirical Review", "29"),
        ("  2.4 Conceptual Framework", "33"),
        ("CHAPTER THREE: RESEARCH METHODOLOGY", "36"),
        ("  3.1 Description of the Study Area", "36"),
        ("  3.2 Research Design", "38"),
        ("  3.3 Population of the Study", "39"),
        ("  3.4 Sampling Technique and Sample Size", "39"),
        ("  3.5 Sources of Data", "41"),
        ("  3.6 Method of Data Collection", "41"),
        ("  3.7 Analytical Techniques", "42"),
        ("    3.7.1 Descriptive Statistics", "42"),
        ("    3.7.2 Poverty Line and Foster-Greer-Thorbecke Poverty Indices (Objective I)", "42"),
        ("    3.7.3 Poverty Status Profile Analysis (Objective II)", "43"),
        ("    3.7.4 Inferential Bivariate and Binary Logistic Regression Analysis (Objective III)", "43"),
        ("    3.7.5 Mean Severity Index for Farming Challenges (Objective IV)", "44"),
        ("  3.8 Model Specification", "44"),
        ("    3.8.1 Determination of Relative Poverty Line", "44"),
        ("    3.8.2 Foster-Greer-Thorbecke (FGT) Poverty Indices", "45"),
        ("    3.8.3 Poverty Status Profile Analytical Framework", "46"),
        ("    3.8.4 Binary Logistic Regression Model", "47"),
        ("    3.8.5 Mean Severity Index (MSI) Model", "49"),
        ("  3.9 A Priori Expectations", "50"),
        ("CHAPTER FOUR: RESULTS AND DISCUSSION", "52"),
        ("  4.1 Socio-Economic Characteristics of Yam Farmers", "52"),
        ("    4.1.1 Sex of Respondents", "54"),
        ("    4.1.2 Age of Respondents", "54"),
        ("    4.1.3 Marital Status of Respondents", "55"),
        ("    4.1.4 Educational Attainment", "56"),
        ("    4.1.5 Household Size", "56"),
        ("    4.1.6 Yam Farming Experience", "57"),
        ("    4.1.7 Other Sources of Income", "57"),
        ("  4.2 Household Expenditure Pattern of Yam Farmers", "58"),
        ("  4.3 Poverty Status of Yam Farmers (Objective I)", "60"),
        ("    4.3.1 Determination of the Poverty Line", "60"),
        ("    4.3.2 Poverty Incidence, Depth and Severity", "61"),
        ("  4.4 Poverty Status Profile of Yam Farmers (Objective II)", "63"),
        ("    4.4.1 Socioeconomic and Institutional Profile by Poverty Status", "63"),
        ("    4.4.2 Mean Characteristics and Farm Asset Profile by Poverty Status", "66"),
        ("    4.4.3 Expenditure Welfare Profile by Poverty Status", "68"),
        ("  4.5 Factors Associated with Poverty Status (Objective III)", "71"),
        ("    4.5.1 Bivariate Analysis of Factors Associated with Poverty Status", "71"),
        ("    4.5.2 Logistic Regression Analysis of Factors Associated with Poverty Status", "73"),
        ("  4.6 Challenges Faced by Yam Farmers (Objective IV)", "76"),
        ("  4.7 Test of Hypotheses", "79"),
        ("  4.8 Discussion of Major Findings", "80"),
        ("CHAPTER FIVE: SUMMARY, CONCLUSION, AND RECOMMENDATIONS", "86"),
        ("  5.1 Summary of Findings", "86"),
        ("  5.2 Conclusion", "89"),
        ("  5.3 Recommendations", "90"),
        ("  5.4 Contribution to Knowledge", "92"),
        ("  5.5 Limitations of the Study", "94"),
        ("REFERENCES", "96")
    ]
    for title, pg in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_before = Pt(0)
        p_toc.paragraph_format.space_after = Pt(2)
        p_toc.paragraph_format.line_spacing = 1.15
        r_t = p_toc.add_run(title)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(11)
        if title.startswith("CHAPTER") or title in ["REFERENCES", "ABSTRACT", "TABLE OF CONTENTS", "LIST OF TABLES", "LIST OF FIGURES"]:
            r_t.bold = True
    doc.add_page_break()

    # List of Tables
    add_heading_styled(doc, "LIST OF TABLES", level=1)
    tables_list = [
        ("Table 3.1", "Definition and Measurement of Explanatory Variables", "48"),
        ("Table 4.1", "Socio-Economic Characteristics of Yam Farmers in Akpabuyo LGA (N = 60)", "53"),
        ("Table 4.2", "Mean Monthly Household Expenditure by Category (N = 60)", "59"),
        ("Table 4.3", "Determination of the Relative Poverty Line among Yam Farmers", "60"),
        ("Table 4.4", "Poverty Status Distribution and Foster-Greer-Thorbecke (FGT) Poverty Indices (N = 60)", "62"),
        ("Table 4.5", "Distribution of Yam Farmers by Poverty Status and Socioeconomic Characteristics", "64"),
        ("Table 4.6", "Mean Characteristics of Yam Farmers by Poverty Status", "67"),
        ("Table 4.7", "Expenditure Welfare Profile of Yam Farmers by Poverty Status", "69"),
        ("Table 4.8", "Bivariate Analysis of Factors Associated with Poverty Status (N = 60)", "72"),
        ("Table 4.9", "Binary Logistic Regression Model of Factors Associated with Poverty Status", "74"),
        ("Table 4.10", "Severity Ranking of Challenges Faced by Yam Farmers in Akpabuyo LGA (N = 60)", "77")
    ]
    for num, title, pg in tables_list:
        p_tab = doc.add_paragraph()
        p_tab.paragraph_format.space_before = Pt(0)
        p_tab.paragraph_format.space_after = Pt(3)
        p_tab.paragraph_format.line_spacing = 1.15
        r1 = p_tab.add_run(f"{num}: {title}")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
    doc.add_page_break()

    # List of Figures
    add_heading_styled(doc, "LIST OF FIGURES", level=1)
    figures_list = [
        ("Figure 2.1", "Conceptual Framework Showing the Relationship between Socio-Economic, Farm-Related and Institutional Factors and Poverty Status", "35"),
        ("Figure 3.1", "Map of Akpabuyo Local Government Area Showing the Study Location", "37"),
        ("Figure 4.1", "Age Distribution of Yam Farmers in Akpabuyo LGA", "55"),
        ("Figure 4.2", "Mean Monthly Household Expenditure by Category among Yam Farmers", "60"),
        ("Figure 4.3", "Poverty Status Distribution of Yam Farmers in Akpabuyo LGA", "63"),
        ("Figure 4.4", "Odds Ratios from Binary Logistic Regression Model (95% CIs)", "76"),
        ("Figure 4.5", "Severity Ranking of Challenges Faced by Yam Farmers in Akpabuyo LGA", "79")
    ]
    for num, title, pg in figures_list:
        p_fig = doc.add_paragraph()
        p_fig.paragraph_format.space_before = Pt(0)
        p_fig.paragraph_format.space_after = Pt(3)
        p_fig.paragraph_format.line_spacing = 1.15
        r1 = p_fig.add_run(f"{num}: {title}")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
    doc.add_page_break()

    # CHAPTER ONE
    print("2. Chapter One...")
    add_heading_styled(doc, "CHAPTER ONE\nINTRODUCTION", level=1)
    add_heading_styled(doc, "1.1 Background to the Study", level=2)
    add_body_p(doc, "Agriculture remains the backbone of the Nigerian rural economy, providing employment, food security, and income for the vast majority of rural households. Among root and tuber crops cultivated in Nigeria, yam (Dioscorea spp.) occupies a preeminent position in terms of economic value, dietary preference, and cultural significance (Ayanwuyi et al., 2011; FAO, 2021). Nigeria is the world’s leading producer of yams, accounting for over 65% of global output (FAOSTAT, 2022). In rural agrarian communities, yam cultivation is not merely a subsistence activity; it is a commercial enterprise and an essential store of household wealth.")
    add_body_p(doc, "Despite Nigeria's significant agricultural potential, poverty remains deeply entrenched in rural areas, where smallholder farming families constitute the majority of the poor (National Bureau of Statistics [NBS], 2020, 2022). The Multidimensional Poverty Index survey conducted by the NBS (2022) revealed that 63% of persons living in Nigeria (approximately 133 million individuals) are multidimensionally poor, with rural communities bearing the heaviest burden (72% incidence in rural areas compared to 42% in urban centres). In agrarian economies, household welfare is closely linked to agricultural productivity, resource endowments, and market conditions.")
    add_body_p(doc, "Yam production is characteristically labour-intensive and requires substantial capital investment in planting materials (seed yams/setts), staking wood, land preparation (mounding/ridging), agrochemicals, and post-harvest storage (Nweke et al., 1991; Ike & Inoni, 2006). Consequently, smallholder yam farmers frequently face acute production constraints, high transaction costs, and severe exposure to climatic and biological risks, which collectively limit farm productivity and depress household real incomes (Fasusi et al., 2022).")
    add_body_p(doc, "In Cross River State, particularly in Akpabuyo Local Government Area, yam farming is an integral component of rural livelihoods and local food systems. The agro-ecological conditions of Akpabuyo LGA—characterized by high rainfall, tropical rainforest vegetation, and fertile soils—are favourable for root and tuber cultivation. However, smallholder producers in the area are often constrained by inadequate institutional support, limited access to credit, poor rural infrastructure, escalating labour costs, and severe post-harvest losses. Understanding the poverty status, socioeconomic profile, and production constraints of yam farmers in Akpabuyo LGA is therefore imperative for formulating targeted agricultural and rural development policies.")

    add_heading_styled(doc, "1.2 Statement of the Problem", level=2)
    add_body_p(doc, "Yam farming households in Nigeria continue to grapple with persistent poverty and economic vulnerability despite their vital role in national food security. Smallholder yam farmers in Akpabuyo LGA operate under challenging production environments marked by rising input costs, high cost or scarcity of hired labour, unpredictable weather patterns, pest infestations, and inadequate modern storage facilities. These structural bottlenecks impede farm expansion, reduce net returns from yam production, and undermine household living standards (Adejoh et al., 2023; Fasusi et al., 2022).")
    add_body_p(doc, "While numerous empirical studies have examined poverty among rural farming households in Nigeria (e.g., Adepoju, 2019; Ogunniyi et al., 2020; Adebunmi et al., 2024), most existing literature focuses either on broad agricultural populations or regional-level aggregates, paying limited attention to crop-specific smallholder dynamics at the local government level. In Akpabuyo Local Government Area, empirical data establishing the exact poverty status, poverty profile, and underlying determinants among yam producers remain scarce. Furthermore, there is a lack of rigorous empirical evidence profiling how poor and non-poor yam farming households differ in their demographic, asset, and expenditure structures, and how institutional factors such as agricultural credit and extension contact relate to their poverty status.")
    add_body_p(doc, "Without localized and crop-specific empirical evidence, policymakers, extension agencies, and non-governmental development organizations lack the grounded insights required to design targeted rural poverty alleviation interventions. This study addresses this critical empirical gap by determining the poverty status of yam farmers, providing a comprehensive descriptive poverty status profile, analyzing factors associated with household poverty, and measuring the production challenges facing yam farmers in Akpabuyo Local Government Area, Cross River State, Nigeria.")

    add_heading_styled(doc, "1.3 Research Questions", level=2)
    add_body_p(doc, "To guide this investigation, the following research questions were addressed:")
    add_body_p(doc, "What is the poverty status and extent of poverty (incidence, depth, and severity) among yam farmers in Akpabuyo Local Government Area?", bold_prefix="i. ")
    add_body_p(doc, "What is the socioeconomic, farm asset, and expenditure welfare profile of poor and non-poor yam farmers in the study area?", bold_prefix="ii. ")
    add_body_p(doc, "What factors are associated with the poverty status of yam farmers in the study area?", bold_prefix="iii. ")
    add_body_p(doc, "What are the major production, institutional, and marketing challenges faced by yam farmers in the study area?", bold_prefix="iv. ")

    add_heading_styled(doc, "1.4 Aim and Objectives of the Study", level=2)
    add_heading_styled(doc, "1.4.1 Aim of the Study", level=3)
    add_body_p(doc, "The overall aim of this study is to analyze the poverty status of yam farmers in Akpabuyo Local Government Area of Cross River State, Nigeria, profile their socioeconomic and expenditure characteristics, examine the factors associated with their poverty status, evaluate their production constraints, and provide actionable policy recommendations for poverty reduction and agricultural development.")
    add_heading_styled(doc, "1.4.2 Specific Objectives", level=3)
    add_body_p(doc, "The specific objectives of the study are to:")
    add_body_p(doc, "Determine the poverty status of yam farmers using appropriate poverty measures.", bold_prefix="i. ")
    add_body_p(doc, "Analyze the poverty status profile of yam farmers across socioeconomic, farm asset, and expenditure characteristics in the study area.", bold_prefix="ii. ")
    add_body_p(doc, "Analyze factors associated with poverty status of yam farmers in the study area.", bold_prefix="iii. ")
    add_body_p(doc, "Measure the challenges faced by yam farmers in the study area.", bold_prefix="iv. ")

    add_heading_styled(doc, "1.5 Research Hypotheses", level=2)
    add_body_p(doc, "To test the empirical relationships under Specific Objective III, the following hypotheses were formulated:")
    add_body_p(doc, "Socioeconomic, farm-related, and institutional factors have no statistically significant association with the poverty status of yam farmers in Akpabuyo Local Government Area.", bold_prefix="H₀: ")
    add_body_p(doc, "Socioeconomic, farm-related, and institutional factors have a statistically significant association with the poverty status of yam farmers in Akpabuyo Local Government Area.", bold_prefix="H₁: ")

    add_heading_styled(doc, "1.6 Significance of the Study", level=2)
    add_body_p(doc, "This study is significant across several practical, policy, and academic dimensions. Firstly, it generates timely empirical evidence on the welfare conditions of smallholder yam farmers in Akpabuyo LGA, providing a reliable quantitative benchmark on poverty incidence, depth, and severity. Secondly, by profiling poor and non-poor households across demographic, land asset, institutional, and expenditure dimensions, the study provides detailed diagnostic insights into the specific vulnerabilities facing disadvantaged farming families.")
    add_body_p(doc, "Thirdly, the findings on factors associated with poverty status—specifically the critical role of agricultural credit access and household demographic structure—provide clear empirical guidance for government agricultural ministries, financial institutions, and non-governmental organizations in formulating targeted credit delivery mechanisms and rural development strategies. Fourthly, by ranking the severity of production constraints, the study equips agricultural extension agencies with practical priorities for intervention, such as labour-saving technologies, input subsidization, and storage infrastructure. Finally, this research contributes to the academic literature on agricultural economics and rural poverty in Nigeria, serving as a reference point for future studies.")

    add_heading_styled(doc, "1.7 Scope of the Study", level=2)
    add_body_p(doc, "Geographically, the study was conducted within Akpabuyo Local Government Area of Cross River State, Nigeria. Conceptually, the investigation was delimited to smallholder farming households actively engaged in yam cultivation during the survey period. The empirical scope encompassed household socioeconomic characteristics, monthly household expenditure patterns, poverty measurement via the Foster-Greer-Thorbecke (FGT) framework, descriptive poverty status profiling, inferential bivariate and binary logistic regression analysis of factors associated with poverty, and 5-point Likert-scale constraint assessment.")

    add_heading_styled(doc, "1.8 Definition of Key Terms", level=2)
    add_body_p(doc, "The standard of living or deprivation experienced by a household, operationalized in this study through per-capita household expenditure relative to an established poverty line.", bold_prefix="Poverty Status: ")
    add_body_p(doc, "A threshold expenditure level (₦13,526.02 per person per month) defined as two-thirds of the mean per-capita household expenditure of the sampled yam farmers, below which a household is classified as poor.", bold_prefix="Poverty Line: ")
    add_body_p(doc, "The proportion of sampled yam-farming households whose per-capita monthly expenditure falls below the relative poverty line.", bold_prefix="Poverty Headcount Ratio (P₀): ")
    add_body_p(doc, "A measure of the depth of poverty, representing the average expenditure shortfall of poor households from the poverty line expressed as a fraction of the poverty line.", bold_prefix="Poverty Gap Index (P₁): ")
    add_body_p(doc, "A measure of the severity of poverty within the sampled population that squares the proportionate poverty gaps, thereby giving greater weight to households located furthest below the poverty line.", bold_prefix="Squared Poverty Gap Index (P₂): ")
    add_body_p(doc, "Total monthly expenditure on food, housing, utilities, education, healthcare, clothing, transport, and farm operational expenses divided by the total number of resident household members.", bold_prefix="Per-Capita Household Expenditure (PCHE): ")
    add_body_p(doc, "Farmers who cultivate small, fragmented land holdings (averaging under 3 hectares) primarily utilizing family and hired manual labour with limited mechanization.", bold_prefix="Smallholder Yam Farmers: ")
    doc.add_page_break()

    # CHAPTER TWO
    print("3. Chapter Two...")
    add_heading_styled(doc, "CHAPTER TWO\nLITERATURE REVIEW", level=1)
    add_heading_styled(doc, "2.1 Conceptual Review", level=2)
    add_heading_styled(doc, "2.1.1 Concept of Poverty", level=3)
    add_body_p(doc, "Poverty is a multidimensional, complex socioeconomic phenomenon that transcends simple income insufficiency. In classical and neoclassical economics, poverty is conventionally conceptualized as the inability of an individual or household to attain a socially acceptable minimum standard of living or command sufficient resources to meet basic biological and social needs (Sen, 1981; World Bank, 2001). While absolute poverty defines deprivation against a fixed physical subsistence threshold (such as minimum nutritional caloric intake), relative poverty views deprivation in relation to the prevailing living standards and average consumption levels within a specific society or community (Foster et al., 1984; Ravallion, 1994).")
    add_heading_styled(doc, "2.1.2 Rural Poverty and Agriculture", level=3)
    add_body_p(doc, "In developing agrarian economies, rural poverty is deeply intertwined with agricultural performance. Smallholder agriculture remains the dominant economic sector employing the rural labour force, but it is frequently characterized by low capitalization, traditional production tools, high climatic vulnerability, and fragmented landholdings (World Bank, 2008). In Nigeria, the National Bureau of Statistics (NBS, 2020) reported that rural households experience poverty rates more than double those observed in urban areas. Agriculture serves as both a primary livelihood source and a direct determinant of rural household consumption, nutrition, and welfare.")
    add_heading_styled(doc, "2.1.3 Concept and Measurement of Poverty", level=3)
    add_body_p(doc, "Measuring poverty requires establishing an appropriate welfare metric and defining a poverty threshold. In agricultural economics and development research, consumption expenditure is widely preferred over reported income as a welfare indicator in rural developing contexts (Deaton, 1997; Ravallion, 1998). Household expenditure exhibits greater stability over time because households smooth consumption across agricultural seasons, and expenditure suffers less from recall bias and intentional underreporting than farm income. The standard approach adopted by the World Bank and national statistical agencies in Nigeria involves setting a relative poverty line at two-thirds of the mean per-capita household expenditure (PCHE), followed by the computation of the Foster-Greer-Thorbecke (FGT) class of poverty indices (Foster et al., 1984; Ravallion, 2016).")
    add_heading_styled(doc, "2.1.4 Poverty among Smallholder Farmers", level=3)
    add_body_p(doc, "Smallholder farming households face distinctive socioeconomic vulnerabilities. Empirical studies across sub-Saharan Africa indicate that smallholder poverty is strongly associated with household demographic structure (large dependency ratios), limited educational attainment, tenure insecurity, inadequate financial liquidity, lack of extension advisory services, and weak market integration (Adepoju & Obayelu, 2013; Adebunmi et al., 2024). In Nigeria, smallholder producers often lack the savings or formal credit access required to procure high-yielding varieties, fertilizers, and crop protection chemicals, locking them in low-productivity, low-income equilibrium traps (Ogunniyi et al., 2020; Balana & Oyeyemi, 2022).")
    add_heading_styled(doc, "2.1.5 Yam Farming and Household Welfare", level=3)
    add_body_p(doc, "Yam (Dioscorea spp.) is a premier cash and food crop in West Africa, contributing substantially to dietary caloric intake and farm household revenue. However, yam cultivation is among the most resource-intensive agricultural enterprises. The production cycle demands significant labour for land clearing, mound making, staking, weeding, and harvesting, alongside substantial capital for seed yam procurement, which can account for over 40% of total variable costs (Nweke et al., 1991; Ike & Inoni, 2006). When smallholder farmers lack access to institutional credit or modern storage facilities, post-harvest losses (often exceeding 30%) and distress selling immediately after harvest severely depress farm profits, exacerbating household economic vulnerability (Fasusi et al., 2022; Verter & Becvarova, 2014).")

    add_heading_styled(doc, "2.2 Theoretical Framework", level=2)
    add_heading_styled(doc, "2.2.1 Theory of Production", level=3)
    add_body_p(doc, "The theoretical foundation of agricultural household welfare is rooted in neoclassical production theory and agricultural household modeling (Singh et al., 1986; Varian, 2019). Smallholder farmers operate as both production units and consumption units. The farm household maximizes a utility function subject to resource constraints: land, family labour, financial liquidity, and prevailing technology. Under this framework, household income and subsequent consumption expenditure are functions of farm output, input prices, output prices, and the technical efficiency of the production process.")
    add_heading_styled(doc, "2.2.2 Theory of Livelihoods", level=3)
    add_body_p(doc, "The Sustainable Livelihoods Framework (Chambers & Conway, 1992; DFID, 1999; Ellis, 2000; Scoones, 2015) conceptualizes household welfare as an outcome of the assets or capitals possessed by the household—human capital (education, farming experience, family labour), natural capital (farm land size), physical capital (modern tools, equipment), financial capital (savings, access to credit, secondary income), and social capital (membership in agricultural cooperatives). The interaction of these capitals under prevailing institutional structures and vulnerability contexts determines household livelihood strategies and poverty outcomes.")
    add_heading_styled(doc, "2.2.3 Basic Needs Perspective", level=3)
    add_body_p(doc, "The basic needs approach, pioneered by Streeten (1981) and Stewart (1985), posits that poverty analysis must focus on the absolute or relative command over essential goods and services required for human decency, including nutritious food, adequate shelter, basic healthcare, clean water, and primary education. In this study, the expenditure allocation across food, housing, health, education, and transport reflects the household's capacity to fulfill basic human needs.")
    add_heading_styled(doc, "2.2.4 Asset-Based Livelihood Framework", level=3)
    add_body_p(doc, "The asset-based approach to poverty (Carter & Barrett, 2006) emphasizes that poverty dynamics are governed by structural asset thresholds. Households possessing land, financial access, and productive capital above critical thresholds are able to generate sustained economic surpluses, adopt improved technologies, and accumulate wealth, whereas asset-poor households remain trapped below the poverty threshold.")
    add_heading_styled(doc, "2.2.5 Human Capital and Farm Productivity", level=3)
    add_body_p(doc, "Human capital theory (Schultz, 1961; Becker, 1964) asserts that investments in education, vocational skills, farming experience, and extension contact enhance the productive capacity, allocative efficiency, and managerial decision-making of farm operators. Educated and experienced farmers are better positioned to adopt modern agronomic practices, optimize input combinations, and manage production risks, thereby elevating farm earnings and supporting household living standards.")
    add_heading_styled(doc, "2.2.6 Risk, Vulnerability, and Rural Poverty", level=3)
    add_body_p(doc, "Smallholder agricultural households in sub-Saharan Africa operate in high-risk environments characterized by climate shocks, pest outbreaks, price volatility, and health emergencies (Dercon, 1998, 2002; Amare et al., 2018). In the absence of formal insurance and credit markets, households adopt ex-ante risk-mitigating strategies (such as low-risk, low-return traditional technologies) or ex-post coping mechanisms (such as reducing consumption), which perpetuate chronic poverty.")

    add_heading_styled(doc, "2.3 Empirical Review", level=2)
    add_body_p(doc, "A growing body of empirical literature has investigated poverty among agricultural households in Nigeria using expenditure-based poverty lines and econometric models. Adepoju (2019) examined the determinants of poverty among rural farming households in Southwest Nigeria using FGT indices and probit regression, reporting a poverty headcount of 38.5% and identifying household size, education, access to credit, and farm size as significant correlates of poverty status. Ogunniyi et al. (2020) analyzed multidimensional poverty among cassava farming households in Nigeria, finding that education, cooperative membership, and access to formal agricultural credit were significantly associated with lower household poverty. Similarly, Adebunmi et al. (2024) established that social networks and institutional affiliations were associated with higher farm earnings and improved welfare among farming households in Osun State.")
    add_body_p(doc, "Focusing specifically on yam-producing households, Adejoh et al. (2023) conducted an economic analysis of smallholder yam farmers in Kogi State, establishing that high input prices, severe labour bottlenecks, and limited institutional credit were the primary constraints depressing farm profitability and household welfare. Fasusi et al. (2022) examined the economics of yam production and poverty status in Ondo State, reporting that access to extension services and productive credit were positively linked to farm output and household living standards. In Cross River State, empirical evidence on smallholder yam farmers remains limited, underscoring the necessity of this localized study in Akpabuyo Local Government Area.")

    add_heading_styled(doc, "2.4 Conceptual Framework", level=2)
    add_body_p(doc, "The conceptual framework of this study, depicted in Figure 2.1, illustrates the structural and conceptual relationships among smallholder farming characteristics, household welfare measures, and poverty status outcomes in Akpabuyo Local Government Area. The framework conceptualizes the household economy as an integrated system structured into distinct analytical components:")
    add_body_p(doc, "1. Socio-Economic Characteristics: Comprising demographic and human capital endowments such as farmer age, sex, marital status, educational attainment, household size, farming experience, and secondary income engagement, which influence labour supply, decision-making, and resource allocation.")
    add_body_p(doc, "2. Farm Asset and Production Factors: Encompassing physical and natural capital assets including total farm size (ha), yam cultivated area (ha), modern farm tools ownership, use of improved yam varieties, and application of chemical fertilizers or organic manure.")
    add_body_p(doc, "3. Institutional Support Factors: Encompassing access to formal and informal agricultural credit, agricultural extension contact, and active membership in agricultural cooperative societies, which provide financial liquidity, technical information, and collective bargaining advantages.")
    add_body_p(doc, "4. HOUSEHOLD WELFARE MEASURE: Representing the empirical standard of living of yam-farming households, operationalized through gross monthly household expenditure, expenditure budget allocation across food and non-food necessities, and Per-Capita Monthly Household Expenditure (PCHE).")
    add_body_p(doc, "5. POVERTY STATUS: Constituting the terminal welfare outcome of the study, determined through the relative poverty line (z = two-thirds mean PCHE) and evaluated via Foster-Greer-Thorbecke (FGT) indices (poverty incidence P₀, poverty depth P₁, and poverty severity P₂) and poor/non-poor binary classification.")
    add_body_p(doc, "6. Challenges Faced by Yam Farmers: Representing exogenous and systemic constraints (labour scarcity, escalating input prices, storage losses, climate variability, credit constraints, extension gaps, and pest/disease infestations) that restrict productivity and welfare attainment (Objective IV).")
    add_body_p(doc, "Methodological and Conceptual Note on Connectors: In strict accordance with the cross-sectional observational design of this research, all connecting lines between framework constructs denote logical conceptual associations and empirical relationships rather than verified causal mediation pathways. Objective II provides a descriptive comparative profile across poverty groups, Objective III evaluates statistical associations using bivariate inferential tests and multivariable logistic regression, and Objective IV evaluates constraint severity using the Mean Severity Index (MSI).")
    add_image_with_caption(doc, "scratch/Figure_2_1_Conceptual_Framework_Final.png", "Figure 2.1: Conceptual Framework Showing the Relationship between Socio-Economic, Farm-Related and Institutional Factors and Poverty Status")
    doc.add_page_break()

    # CHAPTER THREE
    print("4. Chapter Three...")
    add_heading_styled(doc, "CHAPTER THREE\nRESEARCH METHODOLOGY", level=1)
    add_heading_styled(doc, "3.1 Description of the Study Area", level=2)
    add_body_p(doc, "This study was conducted in Akpabuyo Local Government Area of Cross River State, Nigeria. Akpabuyo LGA is located in the southern senatorial district of Cross River State, lying between latitudes 4°45'N and 5°10'N and longitudes 8°20'E and 8°40'E. It is bounded to the north by Akamkpa Local Government Area, to the west by Calabar South and Calabar Municipality, to the east by Bakassi Local Government Area and the Republic of Cameroon, and to the south by the Atlantic Ocean. The area is characterized by a humid tropical climate with a mean annual rainfall ranging from 2,000 mm to 3,500 mm, average temperatures between 25°C and 32°C, and rich alluvial and coastal plain sandy soils that strongly support the cultivation of root crops, tubers, and tree crops (Cross River State Ministry of Agriculture, 2021).")
    add_image_with_caption(doc, "scratch/orig_image2.png", "Figure 3.1: Map of Akpabuyo Local Government Area Showing the Study Location")

    add_heading_styled(doc, "3.2 Research Design", level=2)
    add_body_p(doc, "A cross-sectional, descriptive, and quantitative research design was adopted for this study. Primary data were collected from smallholder yam-farming households at a single point in time to examine their socioeconomic characteristics, household expenditure allocations, poverty indices, poverty status profile, factors associated with poverty, and production constraints.")

    add_heading_styled(doc, "3.3 Population of the Study", level=2)
    add_body_p(doc, "The target population for this study comprised all smallholder farming households actively engaged in yam cultivation within Akpabuyo Local Government Area, Cross River State, Nigeria.")

    add_heading_styled(doc, "3.4 Sampling Technique and Sample Size", level=2)
    add_body_p(doc, "A multi-stage sampling procedure was utilized to select representative yam-farming households. In the first stage, three major yam-producing clans/communities within Akpabuyo LGA were purposively selected based on the intensity of yam production activities. In the second stage, two farming villages were randomly selected from each chosen clan, yielding six villages in total. In the third stage, ten yam-farming households were randomly selected from each village from lists of farming families compiled with the assistance of local agricultural extension agents and community leadership. This yielded a total sample size of N = 60 yam-farming households across the six selected communities.")

    add_heading_styled(doc, "3.5 Sources of Data", level=2)
    add_body_p(doc, "Primary data served as the principal data source, collected directly from household heads using pre-tested structured questionnaires. Secondary data were drawn from academic journals, textbooks, government agricultural reports, National Bureau of Statistics bulletins, and Food and Agriculture Organization (FAO) publications.")

    add_heading_styled(doc, "3.6 Method of Data Collection", level=2)
    add_body_p(doc, "Primary data were collected through face-to-face questionnaire administration and structured interview sessions conducted by the researcher and trained enumerators. Interviews were administered in English, Pidgin English, and local dialects where appropriate to ensure full comprehension, particularly regarding household expenditure on food and non-food items, farm asset holdings, credit transactions, and production constraints.")

    add_heading_styled(doc, "3.7 Analytical Techniques", level=2)
    add_body_p(doc, "To address the four specific objectives of the study, the following analytical techniques were employed:")
    add_body_p(doc, "Descriptive statistics such as frequencies, percentages, means, and standard deviations were used to describe the socioeconomic characteristics and household expenditure patterns of the yam farmers.", bold_prefix="3.7.1 Descriptive Statistics: ")
    add_body_p(doc, "Per-capita household expenditure (PCHE) was computed, and a relative poverty line of two-thirds mean PCHE was established. The Foster-Greer-Thorbecke (FGT) poverty index framework (Foster et al., 1984) was applied to compute the poverty headcount ratio (P₀), poverty gap index (P₁), and poverty severity index (P₂). This directly satisfied Specific Objective I.", bold_prefix="3.7.2 Poverty Line and FGT Poverty Indices (Objective I): ")
    add_body_p(doc, "A comprehensive descriptive profiling analysis was conducted to examine the distribution, proportions, and mean differences in demographic, educational, farm asset, institutional, and expenditure welfare characteristics distinguishing poor from non-poor yam farming households. This satisfied Specific Objective II using descriptive comparisons only.", bold_prefix="3.7.3 Poverty Status Profile Analysis (Objective II): ")
    add_body_p(doc, "Bivariate inferential statistical tests (Mann–Whitney U tests were used for continuous variables where appropriate, while Pearson's chi-square and Fisher's exact tests were used for categorical variables) and a parsimonious binary logistic regression model were used to identify factors significantly associated with poverty status among yam farmers. Firth's penalized maximum likelihood logistic regression was performed as a sensitivity analysis. This satisfied Specific Objective III and tested the research hypotheses.", bold_prefix="3.7.4 Inferential Bivariate and Binary Logistic Regression Analysis (Objective III): ")
    add_body_p(doc, "A 5-point Likert scale (1 = Not a Challenge, 2 = Minor, 3 = Moderate, 4 = Severe, 5 = Very Severe) was employed to evaluate production, marketing, and institutional constraints. A Mean Severity Index (MSI) based on standardized severity intervals (1.00–1.80 = Not a Challenge; 1.81–2.60 = Minor; 2.61–3.40 = Moderate; 3.41–4.20 = Severe; 4.21–5.00 = Very Severe) was used to rank challenges from most to least severe, satisfying Specific Objective IV.", bold_prefix="3.7.5 Mean Severity Index for Farming Challenges (Objective IV): ")

    add_heading_styled(doc, "3.8 Model Specification", level=2)
    add_heading_styled(doc, "3.8.1 Determination of Relative Poverty Line", level=3)
    add_body_p(doc, "Following the relative poverty-line approach adopted in this study (NBS, 2020), the poverty threshold was set at two-thirds (2/3) of mean Per-Capita Monthly Household Expenditure (PCHE). Per-capita household expenditure was calculated for each household as:\nPCHE_i = Total Monthly Household Expenditure_i / Household Size_i\n\nThe relative poverty line (z) was set at two-thirds of the mean per-capita household expenditure:\nz = (2 / 3) * Mean PCHE\n\nHouseholds with PCHE_i < z were classified as Poor (Y_i = 1), while households with PCHE_i >= z were classified as Non-Poor (Y_i = 0).")

    add_heading_styled(doc, "3.8.2 Foster-Greer-Thorbecke (FGT) Poverty Indices", level=3)
    add_body_p(doc, "The FGT class of poverty measures (Foster, Greer, & Thorbecke, 1984) is mathematically specified as:\nP_alpha = (1 / N) * sum_{i=1}^{q} [ (z - y_i) / z ]^alpha\n\nWhere:\nN = Total number of sampled yam-farming households (N = 60)\nq = Number of poor households falling below the poverty line (q = 13)\nz = Relative poverty line (₦13,526.02 per person per month)\ny_i = Per-capita monthly expenditure of the i-th poor household\nalpha = Poverty aversion parameter (alpha = 0 for Headcount P₀, alpha = 1 for Poverty Gap P₁, alpha = 2 for Poverty Severity P₂).")

    add_heading_styled(doc, "3.8.3 Poverty Status Profile Analytical Framework", level=3)
    add_body_p(doc, "Under Specific Objective II, the poverty status profile was operationalized by disaggregating all sampled households into poor (n = 13) and non-poor (n = 47) subgroups. Descriptive cross-tabulations, percentage distributions, subgroup means, standard deviations, and mean absolute differences were computed across three core domains:\n1. Categorical Socioeconomic and Institutional Profile: Sex, marital status, educational attainment, other sources of income, credit access, extension contact, improved yam varieties, chemical fertilizer use, modern farm tools, and cooperative membership.\n2. Continuous Demographic and Farm Asset Profile: Age of household head, household size, yam farming experience, total farm landholding, and yam cultivated area.\n3. Expenditure Welfare and Shortfall Profile: Total household expenditure, per-capita household expenditure, food vs. non-food budget shares, and mean per-capita expenditure deficit.")

    add_heading_styled(doc, "3.8.4 Binary Logistic Regression Model", level=3)
    add_body_p(doc, "To evaluate factors associated with household poverty status (Specific Objective III), a binary logistic regression model was estimated. The probability P_i that the i-th household is poor is modeled as:\nP_i = P(Y_i = 1 | X_i) = exp(beta_0 + sum beta_k X_ki) / [1 + exp(beta_0 + sum beta_k X_ki)]\n\nExpressed in log-odds (logit) form:\nln[ P_i / (1 - P_i) ] = beta_0 + beta_1 X_1i + beta_2 X_2i + ... + beta_k X_ki + epsilon_i\n\nGiven the sample size (N = 60) and 13 observed poverty events, a parsimonious multivariable logistic model was specified to adhere to the recommended events-per-variable (EPV) threshold and prevent model overfitting. The explanatory variables are defined in Table 3.1.")

    # Table 3.1
    t31_data = [
        ["Variable Name", "Variable Description", "Measurement / Operationalization", "Expected Sign"],
        ["Age", "Age of household head", "Continuous (Years)", "+ / -"],
        ["Education", "Formal education attained", "Categorical (0=None, 1=Pri, 2=Sec, 3=Tert)", "-"],
        ["Household Size", "Number of resident members", "Continuous (Number of persons)", "+"],
        ["Farming Experience", "Years engaged in yam farming", "Continuous (Years)", "-"],
        ["Total Farm Size", "Total agricultural land operated", "Continuous (Hectares)", "-"],
        ["Yam Area", "Land area allocated to yam", "Continuous (Hectares)", "-"],
        ["Access to Credit", "Obtained agricultural credit", "Dummy (1 = Yes, 0 = No)", "-"],
        ["Extension Contact", "Contact with extension agents", "Dummy (1 = Yes, 0 = No)", "-"],
        ["Improved Varieties", "Use of improved yam varieties", "Dummy (1 = Yes, 0 = No)", "-"],
        ["Fertilizer Use", "Application of chemical fertilizer", "Dummy (1 = Yes, 0 = No)", "-"],
        ["Modern Farm Tools", "Use of modern farm tools", "Dummy (1 = Yes, 0 = No)", "-"],
        ["Cooperative Member", "Membership in farmers' group", "Dummy (1 = Yes, 0 = No)", "-"]
    ]
    add_table_data(doc, "Table 3.1: Definition and Measurement of Explanatory Variables", t31_data)

    add_heading_styled(doc, "3.8.5 Mean Severity Index (MSI) Model", level=3)
    add_body_p(doc, "To measure production, institutional, and marketing constraints (Specific Objective IV), a 5-point Likert scale was utilized with assigned numeric weights:\n5 = Very Severe; 4 = Severe; 3 = Moderate; 2 = Minor; 1 = Not a Challenge.\n\nThe Mean Severity Index (MSI) for each challenge was computed as:\nMSI_j = [ (5 * f_5) + (4 * f_4) + (3 * f_3) + (2 * f_2) + (1 * f_1) ] / N\n\nWhere f_k represents the frequency of responses in the k-th rating category, and N = 60. Constraints were categorized according to established mean severity intervals:\n• 1.00–1.80: Not a Challenge\n• 1.81–2.60: Minor Challenge\n• 2.61–3.40: Moderate Challenge\n• 3.41–4.20: Severe Challenge\n• 4.21–5.00: Very Severe Challenge")

    add_heading_styled(doc, "3.9 A Priori Expectations", level=2)
    add_body_p(doc, "Economic theory suggests that household size (+), older age of household head (+), and lack of capital (+) are positively associated with poverty. Conversely, higher education (-), longer farming experience (-), larger farm size (-), access to agricultural credit (-), extension contact (-), and technology adoption (-) are hypothesized to be associated with lower odds of household poverty by enhancing farm productivity and household income.")
    doc.add_page_break()

    # CHAPTER FOUR
    print("5. Chapter Four...")
    add_heading_styled(doc, "CHAPTER FOUR\nRESULTS AND DISCUSSION", level=1)
    add_heading_styled(doc, "4.1 Socio-Economic Characteristics of Yam Farmers", level=2)
    add_body_p(doc, "This section presents the socioeconomic profile of the sampled yam-farming household heads in Akpabuyo Local Government Area of Cross River State, Nigeria. The distribution of respondents according to key demographic and institutional characteristics is summarized in Table 4.1.")

    # Table 4.1
    t41_data = [
        ["Variable / Characteristic", "Frequency (n)", "Percentage (%)", "Summary Statistics"],
        ["Sex", "", "", ""],
        ["  Male", "36", "60.00", "—"],
        ["  Female", "24", "40.00", "—"],
        ["  Total", "60", "100.00", "—"],
        ["Age Group (years)", "", "", ""],
        ["  ≤ 35", "7", "11.67", "Mean = 46.03 ± 8.64 years"],
        ["  36 – 45", "23", "38.33", "Min = 28, Max = 67"],
        ["  46 – 55", "21", "35.00", ""],
        ["  ≥ 56", "9", "15.00", ""],
        ["  Total", "60", "100.00", ""],
        ["Marital Status", "", "", ""],
        ["  Single", "5", "8.33", "—"],
        ["  Married", "49", "81.67", "—"],
        ["  Widowed / Divorced / Separated", "6", "10.00", "—"],
        ["  Total", "60", "100.00", "—"],
        ["Educational Attainment", "", "", ""],
        ["  Primary Education", "18", "30.00", "—"],
        ["  Secondary Education", "27", "45.00", "—"],
        ["  Tertiary Education", "15", "25.00", "—"],
        ["  Total", "60", "100.00", "—"],
        ["Household Size Group (persons)", "", "", ""],
        ["  1 – 4", "10", "16.67", "Mean = 6.23 ± 1.84 persons"],
        ["  5 – 8", "44", "73.33", "Min = 3, Max = 11"],
        ["  ≥ 9", "6", "10.00", ""],
        ["  Total", "60", "100.00", ""]
    ]
    add_table_data(doc, "Table 4.1: Socio-Economic Characteristics of Yam Farmers in Akpabuyo LGA (N = 60)", t41_data, "Source: Field Survey Data Analysis, 2026.")

    add_heading_styled(doc, "4.1.1 Sex of Respondents", level=3)
    add_body_p(doc, "Table 4.1 shows that 36 respondents (60.00%) were male, while 24 respondents (40.00%) were female. This distribution indicates that yam farming in Akpabuyo LGA is predominantly undertaken by male-headed households, although female participation remains substantial. The prominent involvement of men aligns with the heavy physical labour demands of traditional yam cultivation, including land clearing, heap making, staking, and harvesting.")

    add_heading_styled(doc, "4.1.2 Age of Respondents", level=3)
    add_body_p(doc, "The age distribution of the farmers revealed a mean age of 46.03 ± 8.64 years, with a range spanning from 28 to 67 years. The largest proportion of respondents fell within the 36–45 age bracket (38.33%), followed closely by the 46–55 age category (35.00%). Only 11.67% of respondents were 35 years or younger, indicating relatively low involvement of youth in yam production.")
    add_image_with_caption(doc, "Figure_4_1_Age_Distribution.png", "Figure 4.1: Age Distribution of Yam Farmers in Akpabuyo LGA")

    add_heading_styled(doc, "4.1.3 Marital Status of Respondents", level=3)
    add_body_p(doc, "The majority of respondents were married (81.67%, n = 49), while 8.33% (n = 5) were single and 10.00% (n = 6) were widowed, divorced, or separated. The high proportion of married farmers suggests that family units provide an essential source of farm labour for routine cultivation activities.")

    add_heading_styled(doc, "4.1.4 Educational Attainment", level=3)
    add_body_p(doc, "All respondents in the sample had attained formal education: 30.00% completed primary education, 45.00% attained secondary education, and 25.00% achieved tertiary education. The literacy level of farmers in Akpabuyo LGA provides a favourable foundation for understanding extension advice, adopting improved agricultural technologies, and managing farm enterprises effectively.")

    add_heading_styled(doc, "4.1.5 Household Size", level=3)
    add_body_p(doc, "Household size averaged 6.23 ± 1.84 persons across the sample, ranging from 3 to 11 persons. The vast majority of households (73.33%) comprised between 5 and 8 members. While larger household sizes can supply family labour, they also create greater consumption demands, directly affecting per-capita welfare.")

    add_heading_styled(doc, "4.1.6 Yam Farming Experience", level=3)
    add_body_p(doc, "The sampled farmers had considerable farming experience, with a mean of 18.88 ± 8.56 years in yam cultivation (ranging from 4 to 40 years). Over 65% of the respondents had more than 15 years of experience, indicating deep familiarity with local agro-ecological conditions and traditional cultivation techniques.")

    add_heading_styled(doc, "4.1.7 Other Sources of Income", level=3)
    add_body_p(doc, "A substantial majority of the sampled farmers (81.67%, n = 49) engaged in secondary economic activities such as petty trading, artisan work, commercial transportation, or secondary crop farming to supplement farm income, while 18.33% (n = 11) relied exclusively on yam and crop farming.")

    add_heading_styled(doc, "4.2 Household Expenditure Pattern of Yam Farmers", level=2)
    add_body_p(doc, "Household expenditure served as the primary welfare metric in this study. Table 4.2 presents the mean monthly household expenditure across major consumption categories.")

    # Table 4.2
    t42_data = [
        ["Expenditure Category", "Mean Monthly Expenditure (₦)", "Budget Share (%)"],
        ["Food and groceries", "60,703.33", "52.40"],
        ["Housing and utilities", "18,246.67", "15.75"],
        ["Education", "14,528.33", "12.54"],
        ["Transportation and other", "11,875.83", "10.25"],
        ["Healthcare", "8,631.67", "7.45"],
        ["Reported Mean Total Household Expenditure", "115,837.50", "100.00"]
    ]
    t42_note = (
        "Source: Field Survey Data Analysis, 2026. Note: The reported total household expenditure does not exactly reconcile "
        "with the sum of the five reported expenditure components (₦113,985.83) because of respondent-level differences between "
        "reported totals and component sums. The reported total is retained as the authoritative welfare measure used for PCHE and poverty classification."
    )
    add_table_data(doc, "Table 4.2: Mean Monthly Household Expenditure by Category (N = 60)", t42_data, t42_note)

    add_body_p(doc, "As shown in Table 4.2 and Figure 4.2, food and grocery expenditure constituted the dominant budgetary component, accounting for ₦60,703.33 per month or 52.40% of total household spending. Housing and utilities followed with ₦18,246.67 (15.75%), education expenses averaged ₦14,528.33 (12.54%), transportation and other miscellaneous expenses accounted for ₦11,875.83 (10.25%), and healthcare required ₦8,631.67 (7.45%). The dominance of food expenditure is consistent with Engel's law in rural developing agrarian settings.")
    add_image_with_caption(doc, "Figure_4_2_Mean_Monthly_Expenditure.png", "Figure 4.2: Mean Monthly Household Expenditure by Category among Yam Farmers")

    add_heading_styled(doc, "4.3 Poverty Status of Yam Farmers (Objective I)", level=2)
    add_heading_styled(doc, "4.3.1 Determination of the Poverty Line", level=3)
    add_body_p(doc, "Following the relative poverty-line approach adopted in this study, the poverty threshold was set at two-thirds (2/3) of mean Per-Capita Monthly Household Expenditure (PCHE) (NBS, 2020). Per-capita household expenditure was computed for each respondent by dividing total monthly expenditure by household size. Table 4.3 presents the parameters used to establish the relative poverty line.")

    # Table 4.3
    t43_data = [
        ["Parameter / Metric", "Value"],
        ["Total Sample Size (N)", "60 households"],
        ["Mean Per-Capita Monthly Expenditure (Mean PCHE)", "₦20,289.03"],
        ["Standard Deviation of PCHE", "₦8,181.80"],
        ["Minimum PCHE", "₦10,833.33"],
        ["Maximum PCHE", "₦46,666.67"],
        ["Median PCHE", "₦18,333.33"],
        ["Relative Poverty Line (z = 2/3 of Mean PCHE)", "₦13,526.02"]
    ]
    add_table_data(doc, "Table 4.3: Determination of the Relative Poverty Line among Yam Farmers", t43_data, "Source: Field Survey Data Analysis, 2026.")

    add_heading_styled(doc, "4.3.2 Poverty Incidence, Depth and Severity", level=3)
    add_body_p(doc, "Based on the relative poverty line of ₦13,526.02 per person per month, households were categorized into poor and non-poor groups, and the Foster-Greer-Thorbecke (FGT) poverty indices were computed. The results are presented in Table 4.4.")

    # Table 4.4
    t44_data = [
        ["Poverty Measure / Category", "Frequency (n)", "Index Value (P_α)", "Percentage (%)"],
        ["A. Poverty Status Classification", "", "", ""],
        ["  Non-poor (PCHE ≥ ₦13,526.02)", "47", "—", "78.33"],
        ["  Poor (PCHE < ₦13,526.02)", "13", "—", "21.67"],
        ["  Total", "60", "—", "100.00"],
        ["B. Foster-Greer-Thorbecke (FGT) Indices", "", "", ""],
        ["  Poverty Headcount Index (P₀)", "13", "0.2167", "21.67%"],
        ["  Poverty Gap Index (P₁)", "—", "0.0232", "2.32%"],
        ["  Poverty Severity Index (P₂)", "—", "0.0034", "0.34%"]
    ]
    t44_note = (
        "Source: Field Survey Data Analysis, 2026. Note: P₀ = Headcount ratio; P₁ = Poverty gap index "
        "(mean shortfall = ₦313.42 per capita across sample; ₦1,446.53 among poor); P₂ = Poverty severity index."
    )
    add_table_data(doc, "Table 4.4: Poverty Status Distribution and Foster-Greer-Thorbecke (FGT) Poverty Indices (N = 60)", t44_data, t44_note)

    add_body_p(doc, "As shown in Table 4.4 and Figure 4.3, the poverty headcount index (P₀) was 0.2167, indicating that 21.67% (n = 13) of the sampled yam farmers lived below the relative poverty threshold, while 78.33% (n = 47) were non-poor. The poverty gap index (P₁) was 0.0232, reflecting a mean monthly per-capita expenditure shortfall of ₦313.42 across the entire sample and ₦1,446.53 among poor households (representing a 10.69% deficit below the poverty line). The poverty severity index (P₂) was 0.0034, indicating relatively low poverty severity within the sampled population.")
    add_image_with_caption(doc, "Figure_4_3_Poverty_Status.png", "Figure 4.3: Poverty Status Distribution of Yam Farmers in Akpabuyo LGA")

    add_heading_styled(doc, "4.4 Poverty Status Profile of Yam Farmers (Objective II)", level=2)
    add_heading_styled(doc, "4.4.1 Socioeconomic and Institutional Profile by Poverty Status", level=3)
    add_body_p(doc, "Table 4.5 profiles the categorical demographic, educational, and institutional characteristics of the respondents disaggregated by poverty status.")

    # Table 4.5
    t45_data = [
        ["Socioeconomic Variable", "Category", "Poor (n = 13)", "Poor (%)", "Non-Poor (n = 47)", "Non-Poor (%)", "Total (N = 60)"],
        ["Sex", "Male", "10", "76.92%", "26", "55.32%", "36 (60.00%)"],
        ["", "Female", "3", "23.08%", "21", "44.68%", "24 (40.00%)"],
        ["Marital Status", "Single", "1", "7.69%", "4", "8.51%", "5 (8.33%)"],
        ["", "Married", "10", "76.92%", "39", "82.98%", "49 (81.67%)"],
        ["", "Widowed/Divorced", "2", "15.38%", "4", "8.51%", "6 (10.00%)"],
        ["Educational Attainment", "Primary", "5", "38.46%", "13", "27.66%", "18 (30.00%)"],
        ["", "Secondary", "7", "53.85%", "20", "42.55%", "27 (45.00%)"],
        ["", "Tertiary", "1", "7.69%", "14", "29.79%", "15 (25.00%)"],
        ["Other Income Source", "Yes", "9", "69.23%", "40", "85.11%", "49 (81.67%)"],
        ["", "No", "4", "30.77%", "7", "14.89%", "11 (18.33%)"],
        ["Access to Credit", "Yes", "1", "7.69%", "29", "61.70%", "30 (50.00%)"],
        ["", "No", "12", "92.31%", "18", "38.30%", "30 (50.00%)"],
        ["Extension Contact", "Yes", "0", "0.00%", "21", "44.68%", "21 (35.00%)"],
        ["", "No", "13", "100.00%", "26", "55.32%", "39 (65.00%)"],
        ["Improved Varieties", "Yes", "0", "0.00%", "2", "4.26%", "2 (3.33%)"],
        ["", "No", "13", "100.00%", "45", "95.74%", "58 (96.67%)"],
        ["Fertilizer / Manure", "Yes", "7", "53.85%", "21", "44.68%", "28 (46.67%)"],
        ["", "No", "6", "46.15%", "26", "55.32%", "32 (53.33%)"],
        ["Modern Farm Tools", "Yes", "0", "0.00%", "6", "12.77%", "6 (10.00%)"],
        ["", "No", "13", "100.00%", "41", "87.23%", "54 (90.00%)"],
        ["Cooperative Member", "Yes", "10", "76.92%", "39", "82.98%", "49 (81.67%)"],
        ["", "No", "3", "23.08%", "8", "17.02%", "11 (18.33%)"]
    ]
    add_table_data(doc, "Table 4.5: Distribution of Yam Farmers by Poverty Status and Socioeconomic Characteristics", t45_data, "Source: Field Survey Data Analysis, 2026. Note: Inferential hypothesis testing is presented under Objective III (Section 4.5).")

    add_heading_styled(doc, "4.4.2 Mean Characteristics and Farm Asset Profile by Poverty Status", level=3)
    add_body_p(doc, "Table 4.6 summarizes the continuous demographic, experience, and land asset variables across poor and non-poor groups.")

    # Table 4.6
    t46_data = [
        ["Continuous Variable", "Poor (n = 13) Mean ± SD", "Non-Poor (n = 47) Mean ± SD", "Overall (N = 60) Mean ± SD", "Mean Difference (Poor − Non-Poor)"],
        ["Farmer Chronological Age (years)", "51.31 ± 8.99", "44.57 ± 8.04", "46.03 ± 8.64", "+6.74 years"],
        ["Household Size (persons)", "8.31 ± 1.70", "5.66 ± 1.43", "6.23 ± 1.84", "+2.65 persons"],
        ["Yam Farming Experience (years)", "25.77 ± 10.48", "16.98 ± 6.94", "18.88 ± 8.56", "+8.79 years"],
        ["Total Farm Size (hectares)", "1.98 ± 0.48", "2.56 ± 0.82", "2.43 ± 0.79", "−0.58 hectares"],
        ["Yam Cultivated Area (hectares)", "1.43 ± 0.37", "1.73 ± 0.56", "1.66 ± 0.54", "−0.30 hectares"]
    ]
    add_table_data(doc, "Table 4.6: Mean Characteristics of Yam Farmers by Poverty Status", t46_data, "Source: Field Survey Data Analysis, 2026. Continuous values reported as arithmetic mean ± sample standard deviation (SD).")

    add_heading_styled(doc, "4.4.3 Expenditure Welfare Profile by Poverty Status", level=3)
    add_body_p(doc, "Table 4.7 details the expenditure patterns and consumption shortfalls distinguishing poor from non-poor farming families.")

    # Table 4.7
    t47_data = [
        ["Welfare & Budgetary Indicator", "Poor (n = 13)", "Non-Poor (n = 47)", "Overall (N = 60)", "Difference / Shortfall"],
        ["Mean Total Monthly Household Expenditure", "₦101,000.00 ± ₦24,782.39", "₦119,941.49 ± ₦27,223.37", "₦115,837.50 ± ₦27,652.42", "−₦18,941.49"],
        ["Mean Household Size (persons)", "8.31 ± 1.70", "5.66 ± 1.43", "6.23 ± 1.84", "+2.65 persons"],
        ["Mean Per-Capita Expenditure (PCHE)", "₦12,079.49 ± ₦919.97", "₦22,559.76 ± ₦7,830.98", "₦20,289.03 ± ₦8,181.80", "−₦10,480.27"],
        ["Monthly Relative Poverty Line (z)", "₦13,526.02", "₦13,526.02", "₦13,526.02", "—"],
        ["Per-Capita Monthly Poverty Shortfall", "₦1,446.53 (10.69% deficit)", "None (Surplus: ₦9,033.74)", "₦313.42 (Sample Average)", "—"]
    ]
    add_table_data(doc, "Table 4.7: Expenditure Welfare Profile of Yam Farmers by Poverty Status", t47_data, "Source: Field Survey Data Analysis, 2026. Relative poverty threshold z = (2/3) × Mean PCHE = ₦13,526.02 per person per month.")

    add_body_p(doc, "In terms of human capital and secondary income, noticeable descriptive differences emerged between the two welfare strata. While the majority of both poor (53.85%) and non-poor (42.55%) farmers possessed secondary education, non-poor farmers recorded a higher proportion of tertiary educational attainment (29.79%) compared to the poor group (7.69%). Conversely, primary education was more prevalent among poor respondents (38.46%) than among non-poor respondents (27.66%). Regarding other sources of income, 85.11% of non-poor households reported having another source of income, compared with 69.23% of poor households. Thus, a higher proportion of non-poor households reported an additional source of income.")
    add_body_p(doc, "A descriptive examination of farm productive assets indicates that non-poor farmers operated larger land holdings and allocated more area to yam cultivation. Non-poor respondents managed an average total farm holding of 2.56 ± 0.82 hectares (with 1.73 ± 0.56 hectares dedicated specifically to yam), whereas poor respondents cultivated an average total farm size of 1.98 ± 0.48 hectares (with 1.43 ± 0.37 hectares under yam). Poor farmers nevertheless reported greater mean yam-farming experience than non-poor farmers (25.77 ± 10.48 years versus 16.98 ± 6.94 years). This descriptive difference reflects the older age profile of poor household heads.")
    add_body_p(doc, "Institutional support and modern input adoption displayed the sharpest descriptive contrast across the poverty profile. Among non-poor farmers, 61.70% had access to agricultural credit during the preceding farming season, compared to only 7.69% (1 out of 13) among poor farmers. Furthermore, 44.68% of non-poor farmers received agricultural extension advisory visits, while 0.00% (0 out of 13) of poor farmers had extension contact. Similarly, modern farm tools and improved yam varieties were utilized exclusively by a fraction of non-poor farmers (12.77% and 4.26%, respectively), while completely absent (0.00%) among the poor. Cooperative society membership was widespread across both groups (76.92% poor versus 82.98% non-poor), reflecting broad community-level social organization.")
    add_body_p(doc, "Overall, the poverty-status profile shows that the poor group was descriptively characterized by older household heads, larger household sizes, smaller farm holdings, lower mean PCHE, and lower reported access to credit and extension services. Poor farmers also recorded greater mean farming experience than non-poor farmers. These descriptive patterns provide a profile of the socioeconomic and farm characteristics of farmers classified as poor and non-poor. Formal statistical tests of the associations between these characteristics and poverty status are presented under Objective III.")

    add_heading_styled(doc, "4.5 Factors Associated with Poverty Status (Objective III)", level=2)
    add_body_p(doc, "In accordance with Specific Objective III, this section provides formal inferential evaluation of the factors associated with household poverty status. Section 4.5.1 presents non-parametric and chi-square bivariate tests, while Section 4.5.2 presents a multivariable binary logistic regression model.")

    add_heading_styled(doc, "4.5.1 Bivariate Analysis of Factors Associated with Poverty Status", level=3)
    add_body_p(doc, "Table 4.8 presents bivariate statistical tests comparing poor and non-poor households across candidate explanatory variables.")

    # Table 4.8
    t48_data = [
        ["Variable / Indicator", "Poor (n = 13)", "Non-Poor (n = 47)", "Overall (N = 60)", "Test Statistic", "p-value"],
        ["A. Demographic & Human Capital", "", "", "", "", ""],
        ["  Age of farmer (years)", "51.31 ± 8.99", "44.57 ± 8.04", "46.03 ± 8.64", "Mann-Whitney U = 432.00", "0.024*"],
        ["  Household size (persons)", "8.31 ± 1.70", "5.66 ± 1.43", "6.23 ± 1.84", "Mann-Whitney U = 536.00", "< 0.001*"],
        ["  Educational attainment", "", "", "", "Chi-Square = 2.673 (df=2)", "0.263"],
        ["    Primary", "5 (38.46%)", "13 (27.66%)", "18 (30.00%)", "", ""],
        ["    Secondary", "7 (53.85%)", "20 (42.55%)", "27 (45.00%)", "", ""],
        ["    Tertiary", "1 (7.69%)", "14 (29.79%)", "15 (25.00%)", "", ""],
        ["B. Farm Resource & Production Factors", "", "", "", "", ""],
        ["  Total farm size (hectares)", "1.98 ± 0.48", "2.56 ± 0.82", "2.43 ± 0.79", "Mann-Whitney U = 170.50", "0.016*"],
        ["  Yam cultivated area (hectares)", "1.43 ± 0.37", "1.73 ± 0.56", "1.66 ± 0.54", "Mann-Whitney U = 205.00", "0.072"],
        ["  Use of improved yam varieties", "0 (0.00%)", "2 (4.26%)", "2 (3.33%)", "Fisher's Exact Test", "1.000"],
        ["  Chemical fertilizer / manure use", "7 (53.85%)", "21 (44.68%)", "28 (46.67%)", "Chi-Square = 0.497 (df=1)", "0.481"],
        ["  Use of modern farm tools", "0 (0.00%)", "6 (12.77%)", "6 (10.00%)", "Fisher's Exact Test", "0.324"],
        ["C. Institutional & Social Factors", "", "", "", "", ""],
        ["  Access to agricultural credit", "1 (7.69%)", "29 (61.70%)", "30 (50.00%)", "Chi-Square = 9.820 (df=1)", "0.002*"],
        ["  Agricultural extension contact", "0 (0.00%)", "21 (44.68%)", "21 (35.00%)", "Fisher's Exact Test", "0.002*"],
        ["  Cooperative society membership", "10 (76.92%)", "39 (82.98%)", "49 (81.67%)", "Chi-Square = 0.009 (df=1)", "0.925"]
    ]
    t48_note = "Source: Field Survey Data Analysis, 2026. * Significant at p < 0.05. Methodological Note: Because household size also forms the denominator of PCHE, this relationship should be interpreted with caution."
    add_table_data(doc, "Table 4.8: Bivariate Analysis of Factors Associated with Poverty Status (N = 60)", t48_data, t48_note)

    add_body_p(doc, "Bivariate inferential tests indicate statistically significant associations with poverty status for farmer age (Mann–Whitney U = 432.00, p = 0.024), household size (Mann–Whitney U = 536.00, p < 0.001), total farm size (Mann–Whitney U = 170.50, p = 0.016), access to credit (χ² = 9.820, p = 0.002), and agricultural extension contact (Fisher's exact p = 0.002). Because household size also forms the denominator of PCHE, this relationship should be interpreted with caution. Conversely, educational attainment (χ² = 2.673, p = 0.263), yam cultivated area (Mann–Whitney U = 205.00, p = 0.072), use of improved varieties (Fisher's exact p = 1.000), fertilizer use (χ² = 0.497, p = 0.481), modern tool adoption (Fisher's exact p = 0.324), and cooperative membership (χ² = 0.009, p = 0.925) did not display statistically significant bivariate associations with poverty status.")

    add_heading_styled(doc, "4.5.2 Logistic Regression Analysis of Factors Associated with Poverty Status", level=3)
    add_body_p(doc, "To evaluate multivariable associations while respecting events-per-variable (EPV) constraints (n = 13 poor events in N = 60), a parsimonious binary logistic regression model was estimated with total farm size (ha) and access to credit (Yes = 1) as key predictors. Table 4.9 presents the model parameter estimates, standard errors, Wald statistics, odds ratios, and associated p-values, alongside Firth penalized sensitivity estimates.")

    # Table 4.9
    t49_data = [
        ["Predictor Variable", "Odds Ratio (OR)", "p-value"],
        ["Total farm size (ha)", "0.6505", "0.5979"],
        ["Access to credit (Yes = 1)", "0.0744", "0.0369*"]
    ]
    t49_note = (
        "Source: Field Survey Data Analysis, 2026. * Significant at p < 0.05.\n"
        "Model Diagnostics: Likelihood Ratio χ² = 13.861 (df = 2, p = 0.000978); Nagelkerke R² = 0.3181; Log-Likelihood = −24.719.\n"
        "Firth Sensitivity Estimates: Total farm size OR = 0.707 (p = 0.654); Access to credit OR = 0.1100 (95% CI: 0.014–0.891, p = 0.0390*)."
    )
    add_table_data(doc, "Table 4.9: Binary Logistic Regression Model of Factors Associated with Poverty Status", t49_data, t49_note)

    add_body_p(doc, "The omnibus likelihood ratio test was statistically significant (χ² = 13.861, df = 2, p = 0.000978), with Nagelkerke R² = 0.3181, indicating the model's relative explanatory performance based on the Nagelkerke pseudo-R² measure (Log-Likelihood = −24.719). Access to credit was statistically significant (OR = 0.0744, p = 0.0369; Firth sensitivity OR = 0.1100, 95% CI: 0.014–0.891, p = 0.0390), indicating that farmers with access to credit had approximately 92.56% lower odds of being classified as poor, holding farm size constant. Total farm size was not statistically significant after conditioning on credit (OR = 0.6505, p = 0.5979).")
    add_image_with_caption(doc, "test_fig4_4_v3.png", "Figure 4.4: Odds Ratios from Binary Logistic Regression Model (95% CIs)")

    add_heading_styled(doc, "4.6 Challenges Faced by Yam Farmers (Objective IV)", level=2)
    add_body_p(doc, "In accordance with Specific Objective IV, ten production, institutional, and marketing constraints were evaluated using a 5-point Likert scale (1 = Not a Challenge to 5 = Very Severe). Table 4.10 presents the ranked challenges based on the Mean Severity Index (MSI).")

    # Table 4.10
    t410_data = [
        ["Rank", "Constraint / Challenge", "Mean Score", "Std. Dev.", "Median", "IQR", "Severity Category"],
        ["1st", "High cost and scarcity of farm labour", "4.15", "0.80", "4.00", "1.00", "Severe"],
        ["2nd", "High cost of farm inputs (fertilizer, seeds, chemicals)", "4.00", "0.96", "4.00", "2.00", "Severe"],
        ["3rd", "Post-harvest losses and inadequate storage facilities", "3.88", "0.99", "4.00", "2.00", "Severe"],
        ["4th", "Unpredictable rainfall and climate conditions", "3.70", "0.85", "4.00", "1.00", "Severe"],
        ["5th", "High cost and scarcity of yam stakes", "3.57", "0.98", "4.00", "1.00", "Severe"],
        ["6th", "Inadequate access to agricultural credit / loan", "3.53", "1.02", "4.00", "1.00", "Severe"],
        ["7th", "Inadequate agricultural extension services", "3.52", "0.97", "4.00", "1.00", "Severe"],
        ["8th", "Pest and disease infestation", "3.38", "1.04", "3.00", "2.00", "Moderate"],
        ["9th", "Low or unstable yam market prices", "3.12", "0.99", "3.00", "1.25", "Moderate"],
        ["10th", "Poor access to markets / bad road network", "2.90", "1.07", "3.00", "2.00", "Moderate"]
    ]
    t410_note = (
        "Source: Field Survey Data Analysis, 2026. Severity intervals: 1.00–1.80 = Not a Challenge; 1.81–2.60 = Minor; "
        "2.61–3.40 = Moderate; 3.41–4.20 = Severe; 4.21–5.00 = Very Severe."
    )
    add_table_data(doc, "Table 4.10: Severity Ranking of Challenges Faced by Yam Farmers in Akpabuyo LGA (N = 60)", t410_data, t410_note)

    add_body_p(doc, "As detailed in Table 4.10 and illustrated in Figure 4.5, all seven top-ranked challenges fell within the 'Severe' category (MSI = 3.41–4.20). High cost and scarcity of farm labour ranked 1st (MSI = 4.15 ± 0.80), followed by high input costs (MSI = 4.00 ± 0.96, Rank 2nd), post-harvest storage losses (MSI = 3.88 ± 0.99, Rank 3rd), unpredictable rainfall and climate conditions (MSI = 3.70 ± 0.85, Rank 4th), high cost or scarcity of yam stakes (MSI = 3.57 ± 0.98, Rank 5th), inadequate credit access (MSI = 3.53 ± 1.02, Rank 6th), and inadequate extension services (MSI = 3.52 ± 0.97, Rank 7th). Pest and disease infestation (MSI = 3.38, Rank 8th), low or unstable market prices (MSI = 3.12, Rank 9th), and poor access to markets (MSI = 2.90, Rank 10th) were ranked as moderate constraints.")
    add_image_with_caption(doc, "test_fig4_5_v2.png", "Figure 4.5: Severity Ranking of Challenges Faced by Yam Farmers in Akpabuyo LGA")

    add_heading_styled(doc, "4.7 Test of Hypotheses", level=2)
    add_body_p(doc, "To provide formal statistical evaluation of the empirical relationships, the research hypotheses were tested:")
    add_body_p(doc, "H₀: Socioeconomic, farm-related, and institutional factors have no statistically significant association with the poverty status of yam farmers in Akpabuyo Local Government Area.", italic=True)
    add_body_p(doc, "H₁: Socioeconomic, farm-related, and institutional factors have a statistically significant association with the poverty status of yam farmers in Akpabuyo Local Government Area.", italic=True)
    add_body_p(doc, "The parsimonious binary logistic regression model reported in Table 4.9 served as the principal multivariable test of the hypothesis. The omnibus Likelihood Ratio test was statistically significant (χ² = 13.861, df = 2, p = 0.000978), indicating that the specified multivariable model provided a statistically significant improvement over the null model. Accordingly, the null hypothesis H₀ was rejected in favour of the alternative hypothesis H₁.")
    add_body_p(doc, "Within the multivariable model, access to credit demonstrated a statistically significant association with poverty status (OR = 0.0744, p = 0.0369), whereas total farm size was not statistically significant after conditioning on credit (OR = 0.6505, p = 0.5979). In addition, bivariate non-parametric and chi-square tests (Table 4.8) established significant associations for household size (p < 0.001), access to credit (p = 0.002), extension contact (p = 0.002), total farm size (p = 0.016), and farmer age (p = 0.024).")

    add_heading_styled(doc, "4.8 Discussion of Major Findings", level=2)
    add_body_p(doc, "This section presents an integrated discussion of findings across the four specific research objectives:")
    add_body_p(doc, "Regarding Objective I (Poverty Measurement), establishing the relative poverty line at ₦13,526.02 per person per month classified 21.67% of households as poor (P₀ = 0.2167) and 78.33% as non-poor. The poverty gap (P₁ = 0.0232) and severity (P₂ = 0.0034) indicate moderate poverty depth and relatively low poverty severity within the sampled population. Food expenditure absorbed 52.40% of household budgets, underscoring the dominance of subsistence food needs in rural agrarian settings.")
    add_body_p(doc, "Regarding Objective II (Poverty Status Profile), descriptive comparisons revealed that poor households had larger family sizes (8.31 persons), were headed by older farmers (mean age 51.31 years), had greater farming experience (25.77 years), operated smaller total farm holdings (1.98 ha), and reported lower access to credit (7.69%) and extension services (0.00%). In contrast, non-poor households maintained smaller families (5.66 persons), younger heads (44.57 years), larger farm holdings (2.56 ha), higher secondary income participation (85.11%), and substantially greater credit access (61.70%).")
    add_body_p(doc, "Regarding Objective III (Factors Associated with Poverty), binary logistic regression confirmed that access to credit was significantly associated with lower odds of poverty (OR = 0.0744, p = 0.0369; Firth OR = 0.1100, p = 0.0390), indicating that credit access helps smallholders finance seasonal input purchases and hired labour. Bivariate tests further highlighted significant relationships with household size (p < 0.001), extension contact (p = 0.002), total farm size (p = 0.016), and farmer age (p = 0.024).")
    add_body_p(doc, "Regarding Objective IV (Challenges Faced by Yam Farmers), high labour costs (MSI = 4.15), high input costs (MSI = 4.00), post-harvest storage losses (MSI = 3.88), climate unpredictability (MSI = 3.70), yam stake scarcity (MSI = 3.57), and credit deficits (MSI = 3.53) were identified as the most severe constraints, reinforcing the empirical finding that institutional credit and input access are critical dimensions of smallholder farm performance.")
    doc.add_page_break()

    # CHAPTER FIVE
    print("6. Chapter Five...")
    add_heading_styled(doc, "CHAPTER FIVE\nSUMMARY, CONCLUSION, AND RECOMMENDATIONS", level=1)
    add_heading_styled(doc, "5.1 Summary of Findings", level=2)
    add_body_p(doc, "This study analyzed the poverty status of yam farmers in Akpabuyo Local Government Area of Cross River State, Nigeria. The empirical investigation was structured around four specific objectives: determining the poverty status using appropriate poverty measures; profiling the socioeconomic, farm asset, and expenditure characteristics of poor and non-poor farmers; analyzing factors associated with poverty status; and measuring the production and institutional challenges confronting yam producers. Primary data obtained from 60 yam-farming households yielded the following major empirical findings across the four specific objectives:")
    add_body_p(doc, "Following the relative poverty-line approach adopted in this study, the relative poverty line was established at two-thirds mean per-capita household expenditure (₦13,526.02 per person per month) against a sample mean monthly PCHE of ₦20,289.03. Based on this threshold, 13 households (21.67%) were classified as poor, while 47 households (78.33%) were classified as non-poor. The Foster-Greer-Thorbecke (FGT) poverty headcount index (P₀) was 0.2167, the poverty gap index (P₁) was 0.0232 (reflecting a mean monthly per-capita expenditure shortfall of ₦313.42 across the entire sample and ₦1,446.53 among poor households), and the squared poverty gap index (P₂) was 0.0034, reflecting relatively low poverty severity within the sampled population.", bold_prefix="1. Poverty Status and FGT Measures (Objective I): ")
    add_body_p(doc, "The poverty status profile demonstrated pronounced descriptive disparities between poor and non-poor yam farming households. Demographically, poor households had larger family sizes (mean of 8.31 ± 1.70 persons compared to 5.66 ± 1.43 persons for non-poor), were headed by older farmers (mean of 51.31 ± 8.99 years versus 44.57 ± 8.04 years), and reported greater yam-farming experience (25.77 ± 10.48 years vs. 16.98 ± 6.94 years). In terms of productive farm assets, poor farmers operated smaller total farm holdings (mean of 1.98 ± 0.48 ha compared to 2.56 ± 0.82 ha) and allocated less land to yam cultivation (1.43 ± 0.37 ha vs. 1.73 ± 0.56 ha). Institutionally, poor households recorded substantially lower access to agricultural credit (7.69% access among poor vs. 61.70% among non-poor) and no extension contact (0.00% vs. 44.68%). In expenditure welfare, while gross monthly household expenditures were relatively comparable (₦101,000.00 for poor vs. ₦119,941.49 for non-poor), the arithmetic denominator effect of larger family sizes among the poor compressed their per-capita monthly expenditure to ₦12,079.49 compared to ₦22,559.76 for non-poor households.", bold_prefix="2. Poverty Status Profile (Objective II): ")
    add_body_p(doc, "Bivariate inferential tests established statistically significant associations between poverty status and household size (Mann–Whitney U = 536.00, p < 0.001), access to credit (χ² = 9.820, p = 0.002), agricultural extension contact (Fisher's exact p = 0.002), total farm size (Mann–Whitney U = 170.50, p = 0.016), and age of household head (Mann–Whitney U = 432.00, p = 0.024). In the parsimonious binary logistic regression model, access to agricultural credit was significantly associated with lower odds of poverty (OR = 0.0744, p = 0.0369; Firth penalized OR = 0.1100, 95% CI: 0.014–0.891, p = 0.0390), indicating that farmers with access to credit had approximately 92.56% lower odds of being classified as poor, holding farm size constant. Total farm size was not statistically significant after conditioning on credit (OR = 0.6505, p = 0.5979). The overall regression model was statistically significant (Likelihood Ratio χ² = 13.861, df = 2, p = 0.000978; Nagelkerke R² = 0.3181; Log-Likelihood = −24.719), leading to the rejection of the null hypothesis H₀.", bold_prefix="3. Factors Associated with Poverty Status (Objective III): ")
    add_body_p(doc, "The evaluation of constraints based on the 5-point Likert Mean Severity Index revealed that smallholder yam farmers face substantial production and resource bottlenecks. The most critical challenges were: high cost or scarcity of farm labour (MSI = 4.15, Rank 1st; Severe), high cost of farm inputs (MSI = 4.00, Rank 2nd; Severe), post-harvest losses and inadequate storage facilities (MSI = 3.88, Rank 3rd; Severe), unpredictable rainfall and climate conditions (MSI = 3.70, Rank 4th; Severe), high cost or scarcity of yam stakes (MSI = 3.57, Rank 5th; Severe), inadequate access to agricultural credit (MSI = 3.53, Rank 6th; Severe), and inadequate agricultural extension services (MSI = 3.52, Rank 7th; Severe). Pest and disease infestation (MSI = 3.38, Rank 8th; Moderate), low or unstable yam market prices (MSI = 3.12, Rank 9th; Moderate), and poor access to markets (MSI = 2.90, Rank 10th; Moderate) were ranked as moderate constraints.", bold_prefix="4. Challenges Faced by Yam Farmers (Objective IV): ")

    add_heading_styled(doc, "5.2 Conclusion", level=2)
    add_body_p(doc, "Based on the empirical findings, this study concludes that while the majority (78.33%) of yam-farming households in Akpabuyo Local Government Area operate above the relative poverty threshold, poverty remains an identifiable welfare challenge affecting more than one-fifth (21.67%) of the farming population. The depth (P₁ = 0.0232) and severity (P₂ = 0.0034) of poverty indicate that the poor experience moderate expenditure deficits that can be bridged through targeted interventions, with relatively low poverty severity within the sampled population.")
    add_body_p(doc, "The study further concludes that poverty among yam farmers is strongly associated with demographic structure and institutional credit constraints. Poor households are characterized by larger family sizes that dilute per-capita consumption, advanced age of household heads, smaller landholdings, and acute exclusion from formal credit and extension services. Access to credit is significantly associated with lower odds of poverty, as it facilitates the procurement of essential inputs, hiring of farm labour, and adoption of modern farm technologies.")
    add_body_p(doc, "Finally, yam production in the study area is severely constrained by high labour costs, escalating input prices, post-harvest deterioration, and climatic unpredictability. Addressing these multidimensional challenges through synchronized credit delivery, extension expansion, input subsidization, and storage infrastructure is essential for enhancing farm income, building rural resilience, and supporting sustainable living standards among yam farmers in Akpabuyo Local Government Area.")

    add_heading_styled(doc, "5.3 Recommendations", level=2)
    add_body_p(doc, "In light of the empirical findings and conclusions, the following policy recommendations are proffered:")
    add_body_p(doc, "The Central Bank of Nigeria (CBN), the Bank of Agriculture (BOA), commercial microfinance banks, and agricultural development agencies should establish tailored smallholder credit facilities with single-digit interest rates, flexible repayment schedules aligned with the yam harvesting calendar, and minimal collateral requirements. Given that credit access was significantly associated with lower odds of poverty, expanding agricultural credit delivery is a top priority intervention.", bold_prefix="1. Expansion of Tailored Agricultural Credit Facilities: ")
    add_body_p(doc, "The Cross River State Agricultural Development Programme (CRADP) should revitalize and intensify extension advisory services in Akpabuyo LGA. Extension visits should be made regular, focusing on training farmers in modern yam production techniques, integrated pest and disease management, efficient chemical fertilizer application, and climate-smart agronomic practices.", bold_prefix="2. Strengthening Agricultural Extension Delivery and Advisory Services: ")
    add_body_p(doc, "Government and private sector stakeholders should implement targeted input subsidy schemes to lower the cost of certified seed yams, fertilizers, crop protection chemicals, and staking materials. Furthermore, the promotion of labour-saving technologies (such as small motorized tillers and ridge-making implements) will help alleviate the severe labour cost and scarcity constraints reported by farmers.", bold_prefix="3. Subsidization of Production Inputs and Promotion of Labour-Saving Tools: ")
    add_body_p(doc, "Agricultural engineering institutes and development agencies should promote the adoption of modern, low-cost ventilated yam storage structures (such as improved yam barns) at the community and cooperative levels. Proper post-harvest handling training should be provided to reduce post-harvest rot and curtail distress selling during the glut period.", bold_prefix="4. Establishment of Modern Post-Harvest Storage Infrastructure: ")
    add_body_p(doc, "Yam farmers should be encouraged to form and actively participate in functional agricultural cooperatives. Cooperative societies facilitate collective bargaining, bulk procurement of inputs at wholesale prices, pooled transport to urban markets, and peer-guaranteed informal credit access.", bold_prefix="5. Promotion of Agricultural Cooperative Societies and Collective Marketing: ")
    add_body_p(doc, "Public health and community development agencies should promote family planning and rural livelihood diversification programmes. Educating farming households on family health and encouraging secondary off-farm economic ventures will help reduce consumption pressures and augment household real income.", bold_prefix="6. Support for Rural Livelihood Diversification and Household Welfare: ")

    add_heading_styled(doc, "5.4 Contribution to Knowledge", level=2)
    add_body_p(doc, "This research project makes several noteworthy contributions to the empirical literature in agricultural economics and rural development:")
    add_body_p(doc, "1. Location-Specific and Crop-Specific Welfare Evidence: It provides first-hand, micro-level empirical evidence on poverty status, headcount incidence, poverty gap, and poverty severity specifically among smallholder yam farmers in Akpabuyo Local Government Area of Cross River State, Nigeria.")
    add_body_p(doc, "2. Comprehensive Poverty Status Profiling: It operationalizes a rigorous, comprehensive poverty status profile (Objective II) that systematically documents how poor and non-poor farming households differ across demographic, educational, farm asset, institutional, and expenditure welfare structures using descriptive comparisons.")
    add_body_p(doc, "3. Econometric Validation of Credit Association: Through both standard binary logistic regression and Firth penalized maximum likelihood estimation, the study quantitatively establishes the significant association between agricultural credit access and lower odds of household poverty in smallholder root-crop systems.")
    add_body_p(doc, "4. Quantitative Constraint Hierarchy: It applies a standardized 5-point Likert Mean Severity Index to establish an empirical hierarchy of production and institutional bottlenecks, highlighting labour costs and storage deficits as paramount constraints.")

    add_heading_styled(doc, "5.5 Limitations of the Study", level=2)
    add_body_p(doc, "While this study provides robust empirical insights, the following limitations should be acknowledged:\n1. Sample Size and Generalizability: The sample size of N = 60 yam-farming households across six selected communities was shaped by logistical, financial, and geographical accessibility factors. While providing valuable local insights for Akpabuyo LGA, generalization of findings beyond the specific study area should be made cautiously.\n2. Cross-Sectional Design: The study utilized cross-sectional survey data collected at a single point in time, capturing a static snapshot of household welfare rather than longitudinal poverty dynamics across multi-year agricultural cycles.\n3. Monetary Welfare Metric: Welfare was measured using monthly consumption expenditure. While expenditure is widely recognized as a reliable proxy, it does not fully capture non-monetary dimensions of poverty such as subjective well-being, housing quality, and access to public infrastructure.\n4. Event Scarcity in Multivariable Modeling: With 13 poor households, multivariable econometric estimation required a parsimonious specification to satisfy events-per-variable guidelines, necessitating the use of Firth penalized regression as a sensitivity check.")
    doc.add_page_break()

    # REFERENCES
    print("7. References...")
    add_heading_styled(doc, "REFERENCES", level=1)
    
    references_data = [
        "Adebunmi, O. A., Ajala, A. K., Adeyemo, J., & Omolara, G. M. (2024). Does social network affect farm income and poverty status? Empirical evidence from farming households in Osun State, Nigeria. International Journal of Agriculture and Food Science, 6(2), 38–46. https://doi.org/10.33545/2664844X.2024.v6.i2a.203",
        "Adejoh, S. O., Edoka, M. H., & Isibor, C. A. (2023). Economic analysis of yam production among smallholder farmers in Kabba-Bunu Local Government Area of Kogi State, Nigeria. Agriculture, Food, and Natural Resources Journal, 2(2), 64–71. https://doi.org/10.5281/zenodo.22544205",
        "Adepoju, A. A. (2019). Comparative analysis of determinants of household poverty among rural farming households in Southwest Nigeria. Journal of Agricultural Science and Environment, 19(1), 45–58.",
        "Adepoju, A. O., & Obayelu, O. A. (2013). Livelihood diversification and welfare of rural households in Ondo State, Nigeria. Journal of Development and Agricultural Economics, 5(10), 406–415.",
        "Amare, M., Jensen, N. D., Shiferaw, B., & Cissé, J. D. (2018). Rainfall shocks and agricultural productivity: Implications for rural household welfare in Nigeria. Agricultural Systems, 166, 79–89.",
        "Ayanwuyi, E., Akinboye, A. O., & Oyetoro, J. O. (2011). Yam production in Oyo State, Nigeria: Economic analysis and challenges. Journal of Agricultural and Biological Science, 6(11), 45–51.",
        "Balana, B. B., & Oyeyemi, M. A. (2022). Agricultural credit constraints in smallholder farming in developing countries: Evidence from Nigeria. World Development, 150, 105723. https://doi.org/10.1016/j.worlddev.2021.105723",
        "Becker, G. S. (1964). Human capital: A theoretical and empirical analysis, with special reference to education. National Bureau of Economic Research.",
        "Carter, M. R., & Barrett, C. B. (2006). The economics of poverty traps and persistent poverty: An asset-based approach. The Journal of Development Studies, 42(2), 178–199. https://doi.org/10.1080/00220380500405261",
        "Chambers, R., & Conway, G. R. (1992). Sustainable rural livelihoods: Practical concepts for the 21st century (IDS Discussion Paper No. 296). Institute of Development Studies.",
        "Cross River State Ministry of Agriculture. (2021). Annual agricultural report and agro-ecological profile of Cross River State. Ministry of Agriculture, Calabar, Nigeria.",
        "de Janvry, A., & Sadoulet, E. (2020). Using agriculture for development: Supply- and demand-side approaches. World Development, 133, 105003. https://doi.org/10.1016/j.worlddev.2020.105003",
        "Deaton, A. (1997). The analysis of household surveys: A microeconometric approach to development policy. Johns Hopkins University Press for the World Bank.",
        "Department for International Development [DFID]. (1999). Sustainable livelihoods guidance sheets. Department for International Development.",
        "Dercon, S. (1998). Wealth, risk and activity choice: Cattle in Western Tanzania. Journal of Development Economics, 55(1), 1–42.",
        "Dercon, S. (2002). Income risk, coping strategies, and safety nets. The World Bank Research Observer, 17(2), 141–166. https://doi.org/10.1093/wbro/17.2.141",
        "Ellis, F. (2000). Rural livelihoods and diversity in developing countries. Oxford University Press.",
        "Fasusi, S. A., Kim, J.-M., & Kang, S. (2022). Determinants and constraints influencing yam production and poverty status of smallholder farmers in Ondo State, Nigeria. Sustainability, 14(15), 9405. https://doi.org/10.3390/su14159405",
        "Food and Agriculture Organization of the United Nations [FAO]. (2021). World food and agriculture – Statistical yearbook 2021. FAO. https://doi.org/10.4060/cb4477en",
        "Food and Agriculture Organization of the United Nations [FAO]. (2022). FAOSTAT statistical database: Crops and livestock products. FAO. https://www.fao.org/faostat",
        "Foster, J., Greer, J., & Thorbecke, E. (1984). A class of decomposable poverty measures. Econometrica, 52(3), 761–766. https://doi.org/10.2307/1913475",
        "Ike, P. C., & Inoni, O. E. (2006). Determinants of yam production and economic efficiency among small-holder farmers in southeastern Nigeria. Journal of Central European Agriculture, 7(2), 337–342.",
        "National Bureau of Statistics [NBS]. (2020). 2019 Poverty and inequality in Nigeria: Executive summary. National Bureau of Statistics.",
        "National Bureau of Statistics [NBS]. (2022). Nigeria development update: Multidimensional poverty index (2022) survey results. National Bureau of Statistics.",
        "Nweke, F. I., Ugwu, B. O., Asadu, C. L. A., & Ay, P. (1991). Production costs in the yam-based cropping systems of southeastern Nigeria (Collaborative Study of Cassava in Africa Working Paper No. 6). International Institute of Tropical Agriculture (IITA).",
        "Ogunniyi, A. I., Mavrotas, G., Olagunju, K. O., Fadare, O., & Adedoyin, R. (2020). Governance quality, remittances and multidimensional poverty in Nigeria: Categorical and ordered logit approach. Social Indicators Research, 151(3), 903–928. https://doi.org/10.1007/s11205-020-02409-7",
        "Ravallion, M. (1994). Poverty comparisons (Fundamentals of Pure and Applied Economics, Vol. 56). Harwood Academic Publishers.",
        "Ravallion, M. (1998). Poverty lines in theory and practice (Living Standards Measurement Study Working Paper No. 133). The World Bank.",
        "Ravallion, M. (2016). The economics of poverty: History, measurement, and policy. Oxford University Press.",
        "Schultz, T. W. (1961). Investment in human capital. The American Economic Review, 51(1), 1–17.",
        "Scoones, I. (2015). Sustainable livelihoods and rural development. Practical Action Publishing.",
        "Sen, A. (1981). Poverty and famines: An essay on entitlement and deprivation. Clarendon Press.",
        "Singh, I., Squire, L., & Strauss, J. (Eds.). (1986). Agricultural household models: Extensions, applications, and policy. The Johns Hopkins University Press for the World Bank.",
        "Stewart, F. (1985). Basic needs in developing countries. The Johns Hopkins University Press.",
        "Streeten, P. (1981). First things first: Meeting basic human needs in the developing countries. Oxford University Press for the World Bank.",
        "Varian, H. R. (2019). Intermediate microeconomics: A modern approach (9th ed.). W. W. Norton & Company.",
        "Verter, N., & Becvarova, V. (2014). Yam production as pillar of food security in Logo Local Government Area of Benue State, Nigeria. European Scientific Journal, 10(31), 214–227.",
        "World Bank. (2001). World development report 2000/2001: Attacking poverty. Oxford University Press for the World Bank.",
        "World Bank. (2008). World development report 2008: Agriculture for development. The World Bank.",
        "World Bank. (2022). Poverty and shared prosperity 2022: Correcting course. The World Bank. https://doi.org/10.1596/978-1-4648-1893-6"
    ]
    
    for r_text in references_data:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_ref = p_ref.add_run(r_text)
        r_ref.font.name = 'Times New Roman'
        r_ref.font.size = Pt(11)

    out_path = "FINAL_THESIS_FOUR_OBJECTIVES_AKPABUYO_FINAL.docx"
    doc.save(out_path)
    print(f"Successfully generated {out_path}!")

if __name__ == "__main__":
    build_final_thesis()
