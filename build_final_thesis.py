import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import os
import sys

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

def build_thesis():
    doc = docx.Document()
    
    # 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    print("1. Adding Preliminary Pages...")
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
        "(iii) analyze factors influencing poverty in the study area; and (iv) measure the challenges faced by yam farmers. "
        "Primary data were collected from a representative sample of 60 yam-farming households using a multi-stage sampling procedure "
        "and structured questionnaires administered through face-to-face interviews. Data were analyzed using descriptive statistics, "
        "the Foster-Greer-Thorbecke (FGT) poverty index, bivariate inferential tests (Chi-square and independent samples t-tests), "
        "a parsimonious binary logistic regression model with Firth penalized sensitivity estimation, and a 4-point Likert Mean Severity Index. "
        "Using the two-thirds mean per-capita household expenditure (PCHE) criterion, a relative poverty line of ₦13,526.02 per person per month "
        "was established based on a mean monthly PCHE of ₦20,289.03. The poverty headcount index (P₀) was 0.2167, indicating that 21.67% (n = 13) "
        "of yam farmers were poor, while 78.33% (n = 47) were non-poor. The poverty gap index (P₁) was 0.0232 (mean expenditure shortfall of ₦313.42 "
        "per person per month), and the poverty severity index (P₂) was 0.0034. The poverty status profile revealed that poor households had significantly "
        "larger family sizes (8.31 ± 1.70 vs. 5.66 ± 1.43 persons; t = 5.757, p < 0.001), older household heads (51.31 ± 8.99 vs. 44.57 ± 8.04 years; "
        "t = 2.610, p = 0.011), smaller farm holdings (1.98 ± 0.48 vs. 2.56 ± 0.82 ha; t = -2.439, p = 0.018), substantially lower access to agricultural "
        "credit (7.69% vs. 61.70%; χ² = 12.019, p = 0.001), lower extension contact (7.69% vs. 42.55%; χ² = 5.378, p = 0.020), and lower per-capita "
        "expenditure (₦12,079.49 vs. ₦22,559.76; t = -7.502, p < 0.001), despite comparable gross monthly household expenditures (₦101,000.00 vs. ₦119,941.49). "
        "In the multivariable logistic regression model, access to credit was the only statistically significant determinant of poverty status "
        "(OR = 0.0744, p = 0.0369; Firth OR = 0.110, p = 0.0390), indicating that access to credit reduced the odds of being poor by approximately 92.56%, "
        "while farm size was not statistically significant (OR = 0.6505, p = 0.5979). The principal production challenges identified were high cost or scarcity "
        "of farm labour (MSI = 3.65), high cost of farm inputs (MSI = 3.60), post-harvest losses and storage deficits (MSI = 3.37), unpredictable rainfall "
        "and climate variability (MSI = 3.32), high cost or scarcity of yam stakes (MSI = 3.12), and inadequate access to credit (MSI = 3.03). "
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

    # 2. CHAPTER ONE
    print("2. Adding Chapter One...")
    add_heading_styled(doc, "CHAPTER ONE\nINTRODUCTION", level=1)
    add_heading_styled(doc, "1.1 Background to the Study", level=2)
    add_body_p(doc, "Agriculture remains the backbone of the Nigerian rural economy, providing employment, food security, and income for the vast majority of rural households. Among root and tuber crops cultivated in Nigeria, yam (Dioscorea spp.) occupies a preeminent position in terms of economic value, dietary preference, and cultural significance (Ayanwuyi et al., 2011; FAO, 2021). Nigeria is the world’s leading producer of yams, accounting for over 65% of global output (FAOSTAT, 2022). In rural agrarian communities, yam cultivation is not merely a subsistence activity; it is a commercial enterprise and an essential store of household wealth.")
    add_body_p(doc, "Despite Nigeria's significant agricultural potential, poverty remains deeply entrenched in rural areas, where smallholder farming families constitute the majority of the poor (National Bureau of Statistics [NBS], 2020, 2022). The Multidimensional Poverty Index survey conducted by the NBS (2022) revealed that 63% of persons living in Nigeria (approximately 133 million individuals) are multidimensionally poor, with rural communities bearing the heaviest burden (72% incidence in rural areas compared to 42% in urban centres). In agrarian economies, household welfare is directly tied to agricultural productivity, resource endowments, and market conditions.")
    add_body_p(doc, "Yam production is characteristically labour-intensive and requires substantial capital investment in planting materials (seed yams/setts), staking wood, land preparation (mounding/ridging), agrochemicals, and post-harvest storage (Nweke et al., 1991; Ike & Inoni, 2006). Consequently, smallholder yam farmers frequently face acute production constraints, high transaction costs, and severe exposure to climatic and biological risks, which collectively limit farm productivity and depress household real incomes (Fasusi et al., 2022).")
    add_body_p(doc, "In Cross River State, particularly in Akpabuyo Local Government Area, yam farming is an integral component of rural livelihoods and local food systems. The agro-ecological conditions of Akpabuyo LGA—characterized by high rainfall, tropical rainforest vegetation, and fertile soils—are favourable for root and tuber cultivation. However, smallholder producers in the area are often constrained by inadequate institutional support, limited access to credit, poor rural infrastructure, escalating labour costs, and severe post-harvest losses. Understanding the poverty status, socioeconomic profile, and production constraints of yam farmers in Akpabuyo LGA is therefore imperative for formulating targeted agricultural and rural development policies.")

    add_heading_styled(doc, "1.2 Statement of the Problem", level=2)
    add_body_p(doc, "Yam farming households in Nigeria continue to grapple with persistent poverty and economic vulnerability despite their vital role in national food security. Smallholder yam farmers in Akpabuyo LGA operate under challenging production environments marked by rising input costs, high cost or scarcity of hired labour, unpredictable weather patterns, pest infestations, and inadequate modern storage facilities. These structural bottlenecks impede farm expansion, reduce net returns from yam production, and undermine household living standards (Adejoh et al., 2023; Fasusi et al., 2022).")
    add_body_p(doc, "While numerous empirical studies have examined poverty among rural farming households in Nigeria (e.g., Adepoju, 2019; Ogunniyi et al., 2020; Olayiwola et al., 2025), most existing literature focuses either on broad agricultural populations or regional-level aggregates, paying limited attention to crop-specific smallholder dynamics at the local government level. In Akpabuyo Local Government Area, empirical data establishing the exact poverty status, poverty profile, and underlying determinants among yam producers remain scarce. Furthermore, there is a lack of rigorous empirical evidence profiling how poor and non-poor yam farming households differ in their demographic, asset, and expenditure structures, and how institutional factors such as agricultural credit and extension contact influence their poverty status.")
    add_body_p(doc, "Without localized and crop-specific empirical evidence, policymakers, extension agencies, and non-governmental development organizations lack the grounded insights required to design targeted rural poverty alleviation interventions. This study addresses this critical empirical gap by determining the poverty status of yam farmers, providing a comprehensive poverty status profile, analyzing factors influencing household poverty, and measuring the production challenges facing yam farmers in Akpabuyo Local Government Area, Cross River State, Nigeria.")

    add_heading_styled(doc, "1.3 Research Questions", level=2)
    add_body_p(doc, "To guide this investigation, the following research questions were addressed:")
    add_body_p(doc, "What is the poverty status and extent of poverty (incidence, depth, and severity) among yam farmers in Akpabuyo Local Government Area?", bold_prefix="i. ")
    add_body_p(doc, "What is the socioeconomic, farm asset, and expenditure welfare profile of poor and non-poor yam farmers in the study area?", bold_prefix="ii. ")
    add_body_p(doc, "What factors influence the poverty status of yam farmers in the study area?", bold_prefix="iii. ")
    add_body_p(doc, "What are the major production, institutional, and marketing challenges faced by yam farmers in the study area?", bold_prefix="iv. ")

    add_heading_styled(doc, "1.4 Aim and Objectives of the Study", level=2)
    add_heading_styled(doc, "1.4.1 Aim of the Study", level=3)
    add_body_p(doc, "The overall aim of this study is to analyze the poverty status of yam farmers in Akpabuyo Local Government Area of Cross River State, Nigeria, profile their socioeconomic and expenditure characteristics, examine the factors influencing their poverty status, evaluate their production constraints, and provide actionable policy recommendations for poverty reduction and agricultural development.")
    add_heading_styled(doc, "1.4.2 Specific Objectives", level=3)
    add_body_p(doc, "The specific objectives of the study are to:")
    add_body_p(doc, "Determine the poverty status of yam farmers using appropriate poverty measures.", bold_prefix="i. ")
    add_body_p(doc, "Analyze poverty status of yam farmers in the study area.", bold_prefix="ii. ")
    add_body_p(doc, "Analyze factors influencing poverty in the study area.", bold_prefix="iii. ")
    add_body_p(doc, "Measure the challenges faced by yam farmers in the study area.", bold_prefix="iv. ")

    add_heading_styled(doc, "1.5 Research Hypotheses", level=2)
    add_body_p(doc, "To test the empirical relationships under Specific Objective III, the following hypotheses were formulated:")
    add_body_p(doc, "Socioeconomic, farm, and institutional factors have no significant influence on the poverty status of yam farmers in Akpabuyo Local Government Area.", bold_prefix="H₀: ")
    add_body_p(doc, "Socioeconomic, farm, and institutional factors have a significant influence on the poverty status of yam farmers in Akpabuyo Local Government Area.", bold_prefix="H₁: ")

    add_heading_styled(doc, "1.6 Significance of the Study", level=2)
    add_body_p(doc, "This study is significant across several practical, policy, and academic dimensions. Firstly, it generates timely empirical evidence on the welfare conditions of smallholder yam farmers in Akpabuyo LGA, providing a reliable quantitative benchmark on poverty incidence, depth, and severity. Secondly, by profiling poor and non-poor households across demographic, land asset, institutional, and expenditure dimensions, the study provides detailed diagnostic insights into the specific vulnerabilities facing disadvantaged farming families.")
    add_body_p(doc, "Thirdly, the findings on factors influencing poverty status—specifically the critical role of agricultural credit access and household size—provide clear empirical guidance for government agricultural ministries, financial institutions, and non-governmental organizations in formulating targeted credit delivery mechanisms and rural development strategies. Fourthly, by ranking the severity of production constraints, the study equips agricultural extension agencies with practical priorities for intervention, such as labour-saving technologies, input subsidization, and storage infrastructure. Finally, this research contributes to the academic literature on agricultural economics and rural poverty in Nigeria, serving as a reference point for future studies.")

    add_heading_styled(doc, "1.7 Scope of the Study", level=2)
    add_body_p(doc, "Geographically, the study was conducted within Akpabuyo Local Government Area of Cross River State, Nigeria. Conceptually, the investigation was delimited to smallholder farming households actively engaged in yam cultivation during the survey period. The empirical scope encompassed household socioeconomic characteristics, monthly household expenditure patterns, poverty measurement via the Foster-Greer-Thorbecke (FGT) framework, descriptive poverty status profiling, inferential bivariate and binary logistic regression analysis of poverty determinants, and Likert-scale constraint assessment.")

    add_heading_styled(doc, "1.8 Definition of Key Terms", level=2)
    add_body_p(doc, "The standard of living or deprivation experienced by a household, operationalized in this study through per-capita household expenditure relative to an established poverty line.", bold_prefix="Poverty Status: ")
    add_body_p(doc, "A threshold expenditure level (₦13,526.02 per person per month) defined as two-thirds of the mean per-capita household expenditure of the sampled yam farmers, below which a household is classified as poor.", bold_prefix="Poverty Line: ")
    add_body_p(doc, "The proportion of sampled yam-farming households whose per-capita monthly expenditure falls below the relative poverty line.", bold_prefix="Poverty Headcount Ratio (P₀): ")
    add_body_p(doc, "A measure of the depth of poverty, representing the average expenditure shortfall of poor households from the poverty line expressed as a fraction of the poverty line.", bold_prefix="Poverty Gap Index (P₁): ")
    add_body_p(doc, "A measure of the severity of poverty that squares the proportionate poverty gaps, thereby giving greater weight to households located furthest below the poverty line.", bold_prefix="Squared Poverty Gap Index (P₂): ")
    add_body_p(doc, "Total monthly expenditure on food, housing, utilities, education, healthcare, clothing, transport, and farm operational expenses divided by the total number of resident household members.", bold_prefix="Per-Capita Household Expenditure (PCHE): ")
    add_body_p(doc, "Farmers who cultivate small, fragmented land holdings (averaging under 3 hectares) primarily utilizing family and hired manual labour with limited mechanization.", bold_prefix="Smallholder Yam Farmers: ")
    doc.add_page_break()

    # 3. CHAPTER TWO
    print("3. Adding Chapter Two...")
    add_heading_styled(doc, "CHAPTER TWO\nLITERATURE REVIEW", level=1)
    add_heading_styled(doc, "2.1 Conceptual Review", level=2)
    add_heading_styled(doc, "2.1.1 Concept of Poverty", level=3)
    add_body_p(doc, "Poverty is a multidimensional, complex socioeconomic phenomenon that transcends simple income insufficiency. In classical and neoclassical economics, poverty is conventionally conceptualized as the inability of an individual or household to attain a socially acceptable minimum standard of living or command sufficient resources to meet basic biological and social needs (Sen, 1981; World Bank, 2001). While absolute poverty defines deprivation against a fixed physical subsistence threshold (such as minimum nutritional caloric intake), relative poverty views deprivation in relation to the prevailing living standards and average consumption levels within a specific society or community (Foster et al., 1984; Ravallion, 1994).")
    add_heading_styled(doc, "2.1.2 Rural Poverty and Agriculture", level=3)
    add_body_p(doc, "In developing agrarian economies, rural poverty is deeply intertwined with agricultural performance. Smallholder agriculture remains the dominant economic sector employing the rural labour force, but it is frequently characterized by low capitalization, traditional production tools, high climatic vulnerability, and fragmented landholdings (World Bank, 2008). In Nigeria, the National Bureau of Statistics (NBS, 2020) reported that rural households experience poverty rates more than double those observed in urban areas. Agriculture serves as both a primary livelihood source and a direct determinant of rural household consumption, nutrition, and welfare.")
    add_heading_styled(doc, "2.1.3 Concept and Measurement of Poverty", level=3)
    add_body_p(doc, "Measuring poverty requires establishing an appropriate welfare metric and defining a poverty threshold. In agricultural economics and development research, consumption expenditure is widely preferred over reported income as a welfare indicator in rural developing contexts (Deaton, 1997; Ravallion, 1998). Household expenditure exhibits greater stability over time because households smooth consumption across agricultural seasons, and expenditure suffers less from recall bias and intentional underreporting than farm income. The standard approach adopted by the World Bank and national statistical agencies in Nigeria involves setting a relative poverty line at two-thirds of the mean per-capita household expenditure (PCHE), followed by the computation of the Foster-Greer-Thorbecke (FGT) class of poverty indices (Foster et al., 1984).")
    add_heading_styled(doc, "2.1.4 Poverty among Smallholder Farmers", level=3)
    add_body_p(doc, "Smallholder farming households face distinctive socioeconomic vulnerabilities. Empirical studies across sub-Saharan Africa indicate that smallholder poverty is strongly associated with household demographic structure (large dependency ratios), limited educational attainment, tenure insecurity, inadequate financial liquidity, lack of extension advisory services, and weak market integration (Adepoju & Obayelu, 2013; Adebunmi et al., 2024). In Nigeria, smallholder producers often lack the savings or formal credit access required to procure high-yielding varieties, fertilizers, and crop protection chemicals, locking them in low-productivity, low-income equilibrium traps (Ogunniyi et al., 2020).")
    add_heading_styled(doc, "2.1.5 Yam Farming and Household Welfare", level=3)
    add_body_p(doc, "Yam (Dioscorea spp.) is a premier cash and food crop in West Africa, contributing substantially to dietary caloric intake and farm household revenue. However, yam cultivation is among the most resource-intensive agricultural enterprises. The production cycle demands significant labour for land clearing, mound making, staking, weeding, and harvesting, alongside substantial capital for seed yam procurement, which can account for over 40% of total variable costs (Nweke et al., 1991; Ike & Inoni, 2006). When smallholder farmers lack access to institutional credit or modern storage facilities, post-harvest losses (often exceeding 30%) and distress selling immediately after harvest severely depress farm profits, exacerbating household poverty (Fasusi et al., 2022).")

    add_heading_styled(doc, "2.2 Theoretical Framework", level=2)
    add_heading_styled(doc, "2.2.1 Theory of Production", level=3)
    add_body_p(doc, "The theoretical foundation of agricultural household welfare is rooted in neoclassical production theory and agricultural household modeling (Singh et al., 1986). Smallholder farmers operate as both production units and consumption units. The farm household maximizes a utility function subject to resource constraints: land, family labour, financial liquidity, and prevailing technology. Under this framework, household income and subsequent consumption expenditure are direct functions of farm output, input prices, output prices, and the technical efficiency of the production process.")
    add_heading_styled(doc, "2.2.2 Theory of Livelihoods", level=3)
    add_body_p(doc, "The Sustainable Livelihoods Framework (DFID, 1999; Ellis, 2000) conceptualizes household welfare as an outcome of the assets or capitals possessed by the household—human capital (education, farming experience, family labour), natural capital (farm land size), physical capital (modern tools, equipment), financial capital (savings, access to credit, secondary income), and social capital (membership in agricultural cooperatives). The interaction of these capitals under prevailing institutional structures and vulnerability contexts determines household livelihood strategies and poverty outcomes.")
    add_heading_styled(doc, "2.2.3 Basic Needs Perspective", level=3)
    add_body_p(doc, "The basic needs approach, pioneered by Streeten (1981) and Stewart (1985), posits that poverty analysis must focus on the absolute or relative command over essential goods and services required for human decency, including nutritious food, adequate shelter, basic healthcare, clean water, and primary education. In this study, the expenditure allocation across food, housing, health, education, and transport reflects the household's capacity to fulfill basic human needs.")
    add_heading_styled(doc, "2.2.4 Asset-Based Livelihood Framework", level=3)
    add_body_p(doc, "The asset-based approach to poverty (Carter & Barrett, 2006) emphasizes that poverty dynamics are governed by structural asset thresholds. Households possessing land, financial access, and productive capital above critical thresholds are able to generate sustained economic surpluses, adopt improved technologies, and accumulate wealth, whereas asset-poor households remain trapped below the poverty threshold.")
    add_heading_styled(doc, "2.2.5 Human Capital and Farm Productivity", level=3)
    add_body_p(doc, "Human capital theory (Schultz, 1961; Becker, 1964) asserts that investments in education, vocational skills, farming experience, and extension contact enhance the productive capacity, allocative efficiency, and managerial decision-making of farm operators. Educated and experienced farmers are better positioned to adopt modern agronomic practices, optimize input combinations, and mitigate production risks, thereby elevating farm income and reducing poverty.")
    add_heading_styled(doc, "2.2.6 Risk, Vulnerability, and Rural Poverty", level=3)
    add_body_p(doc, "Smallholder agricultural households in sub-Saharan Africa operate in high-risk environments characterized by climate shocks, pest outbreaks, price volatility, and health emergencies (Dercon, 2002). In the absence of formal insurance and credit markets, households adopt ex-ante risk-mitigating strategies (such as low-risk, low-return traditional technologies) or ex-post coping mechanisms (such as reducing consumption), which perpetuate chronic poverty.")

    add_heading_styled(doc, "2.3 Empirical Review", level=2)
    add_body_p(doc, "A growing body of empirical literature has investigated poverty among agricultural households in Nigeria using expenditure-based poverty lines and econometric models. Adepoju (2019) examined the determinants of poverty among rural farming households in Southwest Nigeria using FGT indices and probit regression, reporting a poverty headcount of 38.5% and identifying household size, education, access to credit, and farm size as significant predictors of poverty status. Ogunniyi et al. (2020) analyzed multidimensional poverty among cassava farming households in Nigeria, finding that education, cooperative membership, and access to formal agricultural credit substantially reduced the probability of household poverty.")
    add_body_p(doc, "Focusing specifically on yam-producing households, Adejoh et al. (2023) conducted an economic analysis of smallholder yam farmers in Kogi State, establishing that high input prices, severe labour bottlenecks, and limited institutional credit were the primary constraints depressing farm profitability and household welfare. Fasusi et al. (2022) examined the economics of yam production and poverty status in Ondo State, reporting that access to extension services and productive credit significantly elevated farm output and reduced household poverty incidence. In Cross River State, empirical evidence on smallholder yam farmers remains limited, underscoring the necessity of this localized study in Akpabuyo Local Government Area.")

    add_heading_styled(doc, "2.4 Conceptual Framework", level=2)
    add_body_p(doc, "The conceptual framework of this study, illustrated in Figure 2.1, synthesizes the structural relationships connecting household socioeconomic characteristics (age, sex, marital status, education, household size, farming experience, secondary income), farm asset endowments (total farm size, yam cultivated area, modern tools), and institutional factors (access to agricultural credit, agricultural extension contact, cooperative membership) to farm productivity, household expenditure patterns, poverty status (poor vs. non-poor), and production challenges in Akpabuyo Local Government Area.")
    add_image_with_caption(doc, "scratch/orig_image1.png", "Figure 2.1: Conceptual Framework Showing the Relationship between Socio-Economic, Farm-Related and Institutional Factors and Poverty Status")
    doc.add_page_break()

    # 4. CHAPTER THREE
    print("4. Adding Chapter Three...")
    add_heading_styled(doc, "CHAPTER THREE\nRESEARCH METHODOLOGY", level=1)
    add_heading_styled(doc, "3.1 Description of the Study Area", level=2)
    add_body_p(doc, "This study was conducted in Akpabuyo Local Government Area of Cross River State, Nigeria. Akpabuyo LGA is located in the southern senatorial district of Cross River State, lying between latitudes 4°45'N and 5°10'N and longitudes 8°20'E and 8°40'E. It is bounded to the north by Akamkpa Local Government Area, to the west by Calabar South and Calabar Municipality, to the east by Bakassi Local Government Area and the Republic of Cameroon, and to the south by the Atlantic Ocean. The area is characterized by a humid tropical climate with a mean annual rainfall ranging from 2,000 mm to 3,500 mm, average temperatures between 25°C and 32°C, and rich alluvial and coastal plain sandy soils that strongly support the cultivation of root crops, tubers, and tree crops (Cross River State Ministry of Agriculture, 2021).")
    add_image_with_caption(doc, "scratch/orig_image2.png", "Figure 3.1: Map of Akpabuyo Local Government Area Showing the Study Location")

    add_heading_styled(doc, "3.2 Research Design", level=2)
    add_body_p(doc, "A cross-sectional, descriptive, and quantitative research design was adopted for this study. Primary data were collected from smallholder yam-farming households at a single point in time to examine their socioeconomic characteristics, household expenditure allocations, poverty indices, poverty status profile, factors associated with poverty, and production constraints.")

    add_heading_styled(doc, "3.3 Population of the Study", level=2)
    add_body_p(doc, "The target population for this study comprised all smallholder farming households actively engaged in yam cultivation within Akpabuyo Local Government Area, Cross River State, Nigeria.")

    add_heading_styled(doc, "3.4 Sampling Technique and Sample Size", level=2)
    add_body_p(doc, "A multi-stage sampling procedure was utilized to select representative yam-farming households. In the first stage, three major yam-producing clans/communities within Akpabuyo LGA were purposively selected based on the intensity of yam production activities. In the second stage, two farming villages were randomly selected from each chosen clan, yielding six villages in total. In the third stage, ten yam-farming households were randomly selected from each village from lists of farming families compiled with the assistance of local agricultural extension agents and community leadership. This yielded a total sample size of N = 60 yam-farming households.")

    add_heading_styled(doc, "3.5 Sources of Data", level=2)
    add_body_p(doc, "Primary data served as the principal data source, collected directly from household heads using pre-tested structured questionnaires. Secondary data were drawn from academic journals, textbooks, government agricultural reports, National Bureau of Statistics bulletins, and Food and Agriculture Organization (FAO) publications.")

    add_heading_styled(doc, "3.6 Method of Data Collection", level=2)
    add_body_p(doc, "Primary data were collected through face-to-face questionnaire administration and structured interview sessions conducted by the researcher and trained enumerators. Interviews were administered in English, Pidgin English, and local dialects where appropriate to ensure full comprehension, particularly regarding household expenditure on food and non-food items, farm asset holdings, credit transactions, and production constraints.")

    add_heading_styled(doc, "3.7 Analytical Techniques", level=2)
    add_body_p(doc, "To address the four specific objectives of the study, the following analytical techniques were employed:")
    add_body_p(doc, "Descriptive statistics such as frequencies, percentages, means, and standard deviations were used to describe the socioeconomic characteristics and household expenditure patterns of the yam farmers.", bold_prefix="3.7.1 Descriptive Statistics: ")
    add_body_p(doc, "Per-capita household expenditure (PCHE) was computed, and a relative poverty line of two-thirds mean PCHE was established. The Foster-Greer-Thorbecke (FGT) poverty index framework (Foster et al., 1984) was applied to compute the poverty headcount ratio (P₀), poverty gap index (P₁), and poverty severity index (P₂). This directly satisfied Specific Objective I.", bold_prefix="3.7.2 Poverty Line and FGT Poverty Indices (Objective I): ")
    add_body_p(doc, "A comprehensive descriptive profiling analysis was conducted to examine the distribution, proportions, and mean differences in demographic, educational, farm asset, institutional, and expenditure welfare characteristics distinguishing poor from non-poor yam farming households. This satisfied Specific Objective II.", bold_prefix="3.7.3 Poverty Status Profile Analysis (Objective II): ")
    add_body_p(doc, "Bivariate inferential statistical tests (Pearson Chi-square tests of independence, Fisher's exact tests, and independent samples t-tests) and a parsimonious binary logistic regression model were used to identify factors significantly associated with poverty status among yam farmers. Firth's penalized maximum likelihood logistic regression was performed as a sensitivity analysis. This satisfied Specific Objective III and tested the research hypotheses.", bold_prefix="3.7.4 Inferential Bivariate and Binary Logistic Regression Analysis (Objective III): ")
    add_body_p(doc, "A 4-point Likert scale (Very Serious = 4, Serious = 3, Mild = 2, Not a Problem = 1) was employed to evaluate production, marketing, and institutional constraints. A Mean Severity Index (MSI) with a cut-off threshold of 2.50 was used to rank challenges from most to least severe, satisfying Specific Objective IV.", bold_prefix="3.7.5 Mean Severity Index for Farming Challenges (Objective IV): ")

    add_heading_styled(doc, "3.8 Model Specification", level=2)
    add_heading_styled(doc, "3.8.1 Determination of Relative Poverty Line", level=3)
    add_body_p(doc, "Following standard practice in rural welfare analysis in Nigeria (NBS, 2020), per-capita household expenditure (PCHE) was calculated for each household as:\nPCHE_i = Total Monthly Household Expenditure_i / Household Size_i\n\nThe relative poverty line (z) was set at two-thirds of the mean per-capita household expenditure:\nz = (2 / 3) * Mean PCHE\n\nHouseholds with PCHE_i < z were classified as Poor (Y_i = 1), while households with PCHE_i >= z were classified as Non-Poor (Y_i = 0).")

    add_heading_styled(doc, "3.8.2 Foster-Greer-Thorbecke (FGT) Poverty Indices", level=3)
    add_body_p(doc, "The FGT class of poverty measures (Foster, Greer, & Thorbecke, 1984) is mathematically specified as:\nP_alpha = (1 / N) * sum_{i=1}^{q} [ (z - y_i) / z ]^alpha\n\nWhere:\nN = Total number of sampled yam-farming households (N = 60)\nq = Number of poor households falling below the poverty line (q = 13)\nz = Relative poverty line (₦13,526.02 per person per month)\ny_i = Per-capita monthly expenditure of the i-th poor household\nalpha = Poverty aversion parameter (alpha = 0 for Headcount P₀, alpha = 1 for Poverty Gap P₁, alpha = 2 for Poverty Severity P₂).")

    add_heading_styled(doc, "3.8.3 Poverty Status Profile Analytical Framework", level=3)
    add_body_p(doc, "Under Specific Objective II, the poverty status profile was operationalized by disaggregating all sampled households into poor (n = 13) and non-poor (n = 47) subgroups. Cross-tabulations, percentage distributions, subgroup means, standard deviations, and mean absolute differences were computed across three core domains:\n1. Categorical Socioeconomic and Institutional Profile: Sex, marital status, educational attainment, other sources of income, credit access, extension contact, improved yam varieties, chemical fertilizer use, modern farm tools, and cooperative membership.\n2. Continuous Demographic and Farm Asset Profile: Age of household head, household size, yam farming experience, total farm landholding, and yam cultivated area.\n3. Expenditure Welfare and Shortfall Profile: Total household expenditure, per-capita household expenditure, food vs. non-food budget shares, and mean per-capita expenditure deficit.")

    add_heading_styled(doc, "3.8.4 Binary Logistic Regression Model", level=3)
    add_body_p(doc, "To evaluate factors associated with household poverty status (Specific Objective III), a binary logistic regression model was estimated. The probability P_i that the i-th household is poor is modeled as:\nP_i = P(Y_i = 1 | X_i) = exp(beta_0 + sum beta_k X_ki) / [1 + exp(beta_0 + sum beta_k X_ki)]\n\nExpressed in log-odds (logit) form:\nln[ P_i / (1 - P_i) ] = beta_0 + beta_1 X_1i + beta_2 X_2i + ... + beta_k X_ki + epsilon_i\n\nGiven the sample size (N = 60) and 13 observed poverty events, a parsimonious multivariable logistic model was specified to adhere to the recommended events-per-variable (EPV) threshold and prevent model overfitting. The explanatory variables are defined in Table 3.1.")

    # Table 3.1
    p_t31_title = doc.add_paragraph()
    p_t31_title.paragraph_format.space_before = Pt(10)
    p_t31_title.paragraph_format.space_after = Pt(4)
    r_t31 = p_t31_title.add_run("Table 3.1: Definition and Measurement of Explanatory Variables")
    r_t31.font.name = 'Times New Roman'
    r_t31.font.size = Pt(11)
    r_t31.bold = True

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
    t31 = doc.add_table(rows=len(t31_data), cols=4)
    for r_idx, row_vals in enumerate(t31_data):
        for c_idx, val in enumerate(row_vals):
            cell = t31.rows[r_idx].cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)
                if r_idx == 0: run.bold = True
    format_table_apa(t31)

    add_heading_styled(doc, "3.8.5 Mean Severity Index (MSI) Model", level=3)
    add_body_p(doc, "To measure production, institutional, and marketing constraints (Specific Objective IV), a 4-point Likert scale was utilized:\nVery Serious = 4; Serious = 3; Mild = 2; Not a Problem = 1.\n\nThe Mean Severity Index (MSI) for each challenge was computed as:\nMSI_j = [ (4 * f_4) + (3 * f_3) + (2 * f_2) + (1 * f_1) ] / N\n\nWhere f_k represents the frequency of responses in the k-th rating category, and N = 60. A mean score threshold of 2.50 was established as the cut-off criterion: challenges with MSI >= 2.50 were categorized as major/critical constraints, while those with MSI < 2.50 were classified as minor constraints.")

    add_heading_styled(doc, "3.9 A Priori Expectations", level=2)
    add_body_p(doc, "Economic theory suggests that household size (+), older age of household head (+), and lack of capital (+) are positively associated with poverty. Conversely, higher education (-), longer farming experience (-), larger farm size (-), access to agricultural credit (-), extension contact (-), and technology adoption (-) are hypothesized to reduce the probability of household poverty by enhancing farm productivity and household income.")
    doc.add_page_break()

    # 5. CHAPTER FOUR
    print("5. Adding Chapter Four with all 10 Tables and 5 Figures...")
    doc_ch4 = docx.Document("Chapter_4_Objective_2_Integration_FINAL.docx")
    
    # Process elements of Chapter 4
    for element in doc_ch4.element.body:
        if element.tag.endswith('p'):
            p_source = [p for p in doc_ch4.paragraphs if p._element == element][0]
            txt = p_source.text.strip()
            if not txt and not p_source.runs:
                continue
                
            # Headings
            if txt.startswith("CHAPTER FOUR"):
                add_heading_styled(doc, p_source.text, level=1)
            elif txt.startswith("4.1 ") or txt.startswith("4.2 ") or txt.startswith("4.3 ") or txt.startswith("4.4 ") or txt.startswith("4.5 ") or txt.startswith("4.6 ") or txt.startswith("4.7 ") or txt.startswith("4.8 "):
                add_heading_styled(doc, p_source.text, level=2)
            elif txt.startswith("4.1.") or txt.startswith("4.3.") or txt.startswith("4.4.") or txt.startswith("4.5."):
                add_heading_styled(doc, p_source.text, level=3)
            elif txt.startswith("Table 4."):
                p_new = doc.add_paragraph()
                p_new.paragraph_format.space_before = Pt(10)
                p_new.paragraph_format.space_after = Pt(4)
                p_new.paragraph_format.line_spacing = 1.15
                r_new = p_new.add_run(p_source.text)
                r_new.font.name = 'Times New Roman'
                r_new.font.size = Pt(11)
                r_new.bold = True
            elif txt.startswith("Figure 4.1:"):
                add_image_with_caption(doc, "Figure_4_1_Age_Distribution.png", p_source.text)
            elif txt.startswith("Figure 4.2:"):
                add_image_with_caption(doc, "Figure_4_2_Mean_Monthly_Expenditure.png", p_source.text)
            elif txt.startswith("Figure 4.3:"):
                add_image_with_caption(doc, "Figure_4_3_Poverty_Status.png", p_source.text)
            elif txt.startswith("Figure 4.4:"):
                add_image_with_caption(doc, "test_fig4_4_v3.png", p_source.text)
            elif txt.startswith("Figure 4.5:"):
                add_image_with_caption(doc, "test_fig4_5_v2.png", p_source.text)
            elif txt.startswith("Source:") or txt.startswith("Note:"):
                p_new = doc.add_paragraph()
                p_new.paragraph_format.space_before = Pt(2)
                p_new.paragraph_format.space_after = Pt(6)
                p_new.paragraph_format.line_spacing = 1.15
                r_new = p_new.add_run(p_source.text)
                r_new.font.name = 'Times New Roman'
                r_new.font.size = Pt(10)
                r_new.italic = True
            else:
                # Regular paragraph (skip if it was an empty image placeholder paragraph)
                has_image = any('graphic' in r._element.xml for r in p_source.runs)
                if not has_image:
                    add_body_p(doc, p_source.text)
                    
        elif element.tag.endswith('tbl'):
            t_source = [t for t in doc_ch4.tables if t._element == element][0]
            num_rows = len(t_source.rows)
            num_cols = len(t_source.columns)
            t_new = doc.add_table(rows=num_rows, cols=num_cols)
            for r_idx, row in enumerate(t_source.rows):
                for c_idx, cell in enumerate(row.cells):
                    cell_new = t_new.rows[r_idx].cells[c_idx]
                    cell_new.text = cell.text
                    p = cell_new.paragraphs[0]
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.line_spacing = 1.15
                    for run in p.runs:
                        run.font.name = 'Times New Roman'
                        run.font.size = Pt(10)
                        if r_idx == 0: run.bold = True
            format_table_apa(t_new)

    doc.add_page_break()

    # 6. CHAPTER FIVE
    print("6. Adding Chapter Five...")
    add_heading_styled(doc, "CHAPTER FIVE\nSUMMARY, CONCLUSION, AND RECOMMENDATIONS", level=1)
    add_heading_styled(doc, "5.1 Summary of Findings", level=2)
    add_body_p(doc, "This study analyzed the poverty status of yam farmers in Akpabuyo Local Government Area of Cross River State, Nigeria. The empirical investigation was structured around four specific objectives: determining the poverty status using appropriate poverty measures; profiling the socioeconomic, farm asset, and expenditure characteristics of poor and non-poor farmers; analyzing factors influencing poverty status; and measuring the production and institutional challenges confronting yam producers. Primary data obtained from 60 yam-farming households yielded the following major empirical findings across the four specific objectives:")
    add_body_p(doc, "Using the two-thirds mean per-capita household expenditure (PCHE) criterion, a relative poverty line of ₦13,526.02 per person per month was established against a sample mean monthly PCHE of ₦20,289.03. Based on this threshold, 13 households (21.67%) were classified as poor, while 47 households (78.33%) were classified as non-poor. The Foster-Greer-Thorbecke (FGT) poverty headcount index (P₀) was 0.2167, the poverty gap index (P₁) was 0.0232 (reflecting a mean monthly per-capita expenditure shortfall of ₦313.42 across the entire sample and ₦1,446.53 among poor households), and the squared poverty gap index (P₂) was 0.0034.", bold_prefix="1. Poverty Status and FGT Measures (Objective I): ")
    add_body_p(doc, "The poverty status profile demonstrated pronounced structural disparities between poor and non-poor yam farming households. Demographically, poor households had significantly larger family sizes (mean of 8.31 ± 1.70 persons compared to 5.66 ± 1.43 persons for non-poor; t = 5.757, p < 0.001) and were headed by significantly older farmers (mean of 51.31 ± 8.99 years versus 44.57 ± 8.04 years; t = 2.610, p = 0.011). In terms of productive farm assets, poor farmers operated significantly smaller total farm holdings (mean of 1.98 ± 0.48 ha compared to 2.56 ± 0.82 ha; t = -2.439, p = 0.018) and allocated less land to yam cultivation (1.43 ± 0.37 ha vs. 1.73 ± 0.56 ha; t = -1.821, p = 0.074). Institutionally, poor households suffered acute deprivation in agricultural credit access (7.69% access among poor vs. 61.70% among non-poor; χ² = 12.019, p = 0.001) and extension contact (7.69% vs. 42.55%; χ² = 5.378, p = 0.020). In expenditure welfare, while gross monthly household expenditures were relatively comparable (₦101,000.00 for poor vs. ₦119,941.49 for non-poor), the arithmetic denominator effect of larger family sizes among the poor compressed their per-capita monthly expenditure to ₦12,079.49 compared to ₦22,559.76 for non-poor households (t = -7.502, p < 0.001).", bold_prefix="2. Poverty Status Profile (Objective II): ")
    add_body_p(doc, "Bivariate inferential tests established statistically significant associations between poverty status and household size (p < 0.001), access to credit (p = 0.001), age of household head (p = 0.011), total farm size (p = 0.018), and extension contact (p = 0.020). In the parsimonious binary logistic regression model, access to agricultural credit emerged as the sole statistically significant multivariable predictor of poverty status (B = -2.598, SE = 1.245, Wald = 4.354, p = 0.0369, OR = 0.0744; Firth penalized B = -2.207, SE = 1.070, p = 0.0390, OR = 0.1100), indicating that access to credit reduced the odds of household poverty by approximately 92.56%. Total farm size was not statistically significant in the multivariable model (B = -0.4299, p = 0.5979, OR = 0.6505). The overall regression model was statistically significant (Likelihood Ratio χ² = 13.861, df = 2, p = 0.000978; Nagelkerke R² = 0.3181), leading to the rejection of the null hypothesis H₀.", bold_prefix="3. Factors Influencing Poverty Status (Objective III): ")
    add_body_p(doc, "The evaluation of constraints revealed that smallholder yam farmers face substantial production and resource bottlenecks. The most critical challenges, ranked by Mean Severity Index (MSI), were: high cost or scarcity of farm labour (MSI = 3.65, Rank 1), high cost of farm inputs (MSI = 3.60, Rank 2), post-harvest losses and inadequate storage facilities (MSI = 3.37, Rank 3), unpredictable rainfall and climate variability (MSI = 3.32, Rank 4), high cost or scarcity of yam stakes (MSI = 3.12, Rank 5), inadequate access to agricultural credit (MSI = 3.03, Rank 6), and inadequate agricultural extension services (MSI = 2.75, Rank 7). Pest and disease infestation (MSI = 2.40), low or unstable yam market prices (MSI = 2.37), and poor access to markets (MSI = 2.18) were ranked as moderate constraints.", bold_prefix="4. Challenges Faced by Yam Farmers (Objective IV): ")

    add_heading_styled(doc, "5.2 Conclusion", level=2)
    add_body_p(doc, "Based on the empirical findings, this study concludes that while the majority (78.33%) of yam-farming households in Akpabuyo Local Government Area operate above the relative poverty threshold, poverty remains an identifiable welfare challenge affecting more than one-fifth (21.67%) of the farming population. The depth (P₁ = 0.0232) and severity (P₂ = 0.0034) of poverty indicate that the poor experience moderate expenditure deficits that can be bridged through targeted interventions.")
    add_body_p(doc, "The study further concludes that poverty among yam farmers is strongly shaped by demographic pressure and severe institutional credit constraints. Poor households are constrained by larger family sizes that dilute per-capita consumption, advanced age of household heads, smaller landholdings, and acute exclusion from formal credit and extension services. Access to credit is the single most critical factor mitigating poverty, as it enables farmers to procure essential inputs, hire labour, and adopt modern farm technologies.")
    add_body_p(doc, "Finally, yam production in the study area is severely impeded by high labour costs, escalating input prices, post-harvest deterioration, and climatic unpredictability. Addressing these multidimensional challenges through synchronized credit delivery, extension expansion, input subsidization, and storage infrastructure is essential for enhancing farm income, building rural resilience, and achieving sustainable poverty reduction among yam farmers in Akpabuyo Local Government Area.")

    add_heading_styled(doc, "5.3 Recommendations", level=2)
    add_body_p(doc, "In light of the empirical findings and conclusions, the following policy recommendations are proffered:")
    add_body_p(doc, "The Central Bank of Nigeria (CBN), the Bank of Agriculture (BOA), commercial microfinance banks, and agricultural development agencies should establish tailored smallholder credit facilities with single-digit interest rates, flexible repayment schedules aligned with the yam harvesting calendar, and minimal collateral requirements. Given that credit access reduced poverty odds by over 92%, expanding agricultural credit delivery is the most urgent intervention.", bold_prefix="1. Expansion of Tailored Agricultural Credit Facilities: ")
    add_body_p(doc, "The Cross River State Agricultural Development Programme (CRADP) should revitalize and intensify extension advisory services in Akpabuyo LGA. Extension visits should be made regular, focusing on training farmers in modern yam production techniques, integrated pest and disease management, efficient chemical fertilizer application, and climate-smart agronomic practices.", bold_prefix="2. Strengthening Agricultural Extension Delivery and Advisory Services: ")
    add_body_p(doc, "Government and private sector stakeholders should implement targeted input subsidy schemes to lower the cost of certified seed yams, fertilizers, crop protection chemicals, and staking materials. Furthermore, the promotion of labour-saving technologies (such as small motorized tillers and ridge-making implements) will mitigate the severe labour cost and scarcity constraints reported by farmers.", bold_prefix="3. Subsidization of Production Inputs and Promotion of Labour-Saving Tools: ")
    add_body_p(doc, "Agricultural engineering institutes and development agencies should promote the adoption of modern, low-cost ventilated yam storage structures (such as improved yam barns) at the community and cooperative levels. Proper post-harvest handling training should be provided to reduce post-harvest rot and curtail distress selling during the glut period.", bold_prefix="4. Establishment of Modern Post-Harvest Storage Infrastructure: ")
    add_body_p(doc, "Yam farmers should be encouraged to form and actively participate in functional agricultural cooperatives. Cooperative societies facilitate collective bargaining, bulk procurement of inputs at wholesale prices, pooled transport to urban markets, and peer-guaranteed informal credit access.", bold_prefix="5. Promotion of Agricultural Cooperative Societies and Collective Marketing: ")
    add_body_p(doc, "Public health and community development agencies should promote family planning and rural livelihood diversification programmes. Educating farming households on family health and encouraging secondary off-farm economic ventures will reduce dependency pressures and augment household real income.", bold_prefix="6. Support for Rural Livelihood Diversification and Household Welfare: ")

    add_heading_styled(doc, "5.4 Contribution to Knowledge", level=2)
    add_body_p(doc, "This research project makes several noteworthy contributions to the empirical literature in agricultural economics and rural development:")
    add_body_p(doc, "1. Location-Specific and Crop-Specific Welfare Evidence: It provides first-hand, micro-level empirical evidence on poverty status, headcount incidence, poverty gap, and poverty severity specifically among smallholder yam farmers in Akpabuyo Local Government Area of Cross River State, Nigeria.")
    add_body_p(doc, "2. Comprehensive Poverty Status Profiling: It operationalizes a rigorous, multidimensional poverty profile (Objective II) that systematically documents how poor and non-poor farming households differ across demographic, educational, farm asset, institutional, and expenditure welfare structures.")
    add_body_p(doc, "3. Econometric Validation of Credit Primacy: Through both standard binary logistic regression and Firth penalized maximum likelihood estimation, the study quantitatively establishes the dominant protective effect of agricultural credit access against rural household poverty in smallholder root-crop systems.")
    add_body_p(doc, "4. Quantitative Constraint Hierarchy: It applies a standardized Mean Severity Index to establish an empirical hierarchy of production and institutional bottlenecks, highlighting labour costs and storage deficits as paramount constraints.")

    add_heading_styled(doc, "5.5 Limitations of the Study", level=2)
    add_body_p(doc, "While this study provides robust empirical insights, the following limitations should be acknowledged:\n1. Sample Size and Generalizability: The sample size of N = 60 yam-farming households across six communities was constrained by logistic, financial, and geographical accessibility factors. While statistically representative of Akpabuyo LGA, caution should be exercised when generalizing findings to other states.\n2. Cross-Sectional Design: The study utilized cross-sectional survey data collected at a single point in time, capturing a static snapshot of household welfare rather than longitudinal poverty dynamics across multi-year agricultural cycles.\n3. Monetary Welfare Metric: Welfare was measured using monthly consumption expenditure. While expenditure is widely recognized as a reliable proxy, it does not fully capture non-monetary dimensions of poverty such as subjective well-being, housing quality, and access to public infrastructure.\n4. Event Scarcity in Multivariable Modeling: With 13 poor households, multivariable econometric estimation required a parsimonious specification to satisfy events-per-variable guidelines, necessitating the use of Firth penalized regression as a sensitivity check.")
    doc.add_page_break()

    # 7. REFERENCES
    print("7. Adding References...")
    add_heading_styled(doc, "REFERENCES", level=1)
    doc_orig = docx.Document("../chapter 1-5.docx")
    refs_started = False
    for p in doc_orig.paragraphs:
        txt = p.text.strip()
        if txt.upper() == "REFERENCES":
            refs_started = True
            continue
        if refs_started and txt:
            p_ref = doc.add_paragraph()
            p_ref.paragraph_format.space_before = Pt(0)
            p_ref.paragraph_format.space_after = Pt(4)
            p_ref.paragraph_format.line_spacing = 1.15
            p_ref.paragraph_format.left_indent = Inches(0.5)
            p_ref.paragraph_format.first_line_indent = Inches(-0.5)
            p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            r_ref = p_ref.add_run(txt)
            r_ref.font.name = 'Times New Roman'
            r_ref.font.size = Pt(11)
            
    out_path = "FINAL_THESIS_FOUR_OBJECTIVES_AKPABUYO.docx"
    doc.save(out_path)
    print(f"Successfully generated {out_path} with all figures and tables!")

if __name__ == "__main__":
    build_thesis()

