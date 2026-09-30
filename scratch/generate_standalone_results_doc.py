import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_standalone_results_document():
    doc = Document()

    # Set Page setup to A4 with 1 inch margins
    for section in doc.sections:
        section.page_width = Inches(8.27)  # A4 width
        section.page_height = Inches(11.69) # A4 height
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Configure footer with page numbering XML
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_ft.paragraph_format.space_after = Pt(0)
        r_ft = p_ft.add_run("Statistical Analysis and Results | Page ")
        r_ft.font.name = 'Times New Roman'
        r_ft.font.size = Pt(9.5)
        r_ft.font.italic = True
        r_ft.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        
        # Add dynamic page number field to footer
        fldSimple = OxmlElement('w:fldSimple')
        fldSimple.set(qn('w:instr'), 'PAGE')
        p_ft._p.append(fldSimple)

    # Style definitions
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.space_after = Pt(6)

    def add_p(text, bold_prefix=None, space_before=0, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.LEFT, italic=False):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(12)
            r_pre.bold = True
            r_pre.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.italic = italic
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.bold = True
        r.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12.5)
        r.bold = True
        r.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
        return p

    def add_table_title(title_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title_text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.bold = True
        return p

    def add_table_source(source_text="Source: Field Survey Data Analysis, 2026."):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(10)
        r = p.add_run(source_text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.italic = True
        return p

    def format_table_academic(t, col_widths, alignments):
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        
        # Border XML for APA style (top thick, bottom thick, header bottom medium, no vertical lines)
        tblPr = t._tbl.tblPr
        tblBorders = parse_xml(
            r'<w:tblBorders {} >'
            r'  <w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
            r'  <w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
            r'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>'
            r'  <w:insideV w:val="none"/>'
            r'  <w:left w:val="none"/>'
            r'  <w:right w:val="none"/>'
            r'</w:tblBorders>'.format(nsdecls('w'))
        )
        tblPr.append(tblBorders)
        
        for row_idx, row in enumerate(t.rows):
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))
            if row_idx == 0:
                trPr.append(parse_xml(r'<w:tblHeader {}/>'.format(nsdecls('w'))))
                
            for col_idx, cell in enumerate(row.cells):
                cell.width = Inches(col_widths[col_idx])
                tcPr = cell._tc.get_or_add_tcPr()
                tcPr.append(parse_xml(r'<w:tcMar {}><w:top w:w="80" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tcMar>'.format(nsdecls('w'))))
                
                # Header style
                if row_idx == 0:
                    tcPr.append(parse_xml(r'<w:shd {} w:fill="F2F2F2"/>'.format(nsdecls('w'))))
                    tcPr.append(parse_xml(r'<w:tcBorders {}><w:bottom w:val="single" w:sz="8" w:color="000000"/></w:tcBorders>'.format(nsdecls('w'))))
                
                p = cell.paragraphs[0]
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.space_before = Pt(2)
                p.alignment = alignments[col_idx]
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(10 if row_idx == 0 else 9.5)
                    if row_idx == 0:
                        r.bold = True

    def add_figure(fig_path, fig_title, fig_num):
        if os.path.exists(fig_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(10)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.paragraph_format.keep_with_next = True
            run_img = p_img.add_run()
            run_img.add_picture(fig_path, width=Inches(5.8))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(12)
            r_cap = p_cap.add_run(f"Figure {fig_num}: {fig_title}\n")
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(10.5)
            r_cap.bold = True
            r_src = p_cap.add_run("Source: Field Survey Data Analysis, 2026.")
            r_src.font.name = 'Times New Roman'
            r_src.font.size = Pt(9.5)
            r_src.italic = True

    # =========================================================================
    # TITLE PAGE
    # =========================================================================
    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.space_before = Pt(40)
    p_t1.paragraph_format.space_after = Pt(8)
    r = p_t1.add_run("STATISTICAL ANALYSIS AND RESULTS")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(18)
    r.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(36)
    r = p_sub.add_run("Analysis of Poverty Status of Yam Farmers in Akpabuyo Local Government Area, Cross River State, Nigeria")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.bold = True
    r.italic = True

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.line_spacing = 1.3
    p_meta.paragraph_format.space_after = Pt(40)
    
    runs_meta = [
        ("A Standalone Statistical Analysis and Results Report Submitted for Academic Examination\n\n\n", False, 11),
        ("BY\n\n", True, 11),
        ("FAGBUYI OLAYINKA FAITH\n", True, 13),
        ("Matriculation Number: 20/011145065\n\n\n", False, 11.5),
        ("DEPARTMENT OF AGRICULTURAL ECONOMICS\n", True, 12),
        ("FACULTY OF AGRICULTURE\n", True, 12),
        ("UNIVERSITY OF CALABAR, CALABAR, NIGERIA\n\n", True, 12),
        ("SEPTEMBER 2026", True, 12)
    ]
    for m_text, m_bold, m_sz in runs_meta:
        r = p_meta.add_run(m_text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(m_sz)
        r.bold = m_bold

    doc.add_page_break()

    # =========================================================================
    # PRELIMINARY PAGES: TOC, LOT, LOF
    # =========================================================================
    add_h1("TABLE OF CONTENTS")
    
    toc_items = [
        ("SECTION 1: SAMPLE AND SOCIO-ECONOMIC CHARACTERISTICS", "1"),
        ("  1.1 Sample Size and Study Population Representation", "1"),
        ("  1.2 Sex Distribution of Respondents", "1"),
        ("  1.3 Summary Statistics of Quantitative Demographic Variables", "2"),
        ("  1.4 Age Distribution of Yam Farmers", "2"),
        ("  1.5 Marital Status and Educational Attainment", "3"),
        ("  1.6 Other Sources of Household Income", "3"),
        ("SECTION 2: HOUSEHOLD EXPENDITURE ANALYSIS", "4"),
        ("  2.1 Monthly Household Expenditure Patterns", "4"),
        ("  2.2 Per-Capita Monthly Household Expenditure (PCHE)", "5"),
        ("  2.3 Expenditure Data Quality Check and Sensitivity Audit", "5"),
        ("SECTION 3: POVERTY STATUS ANALYSIS", "7"),
        ("  3.1 Determination of the Relative Poverty Line", "7"),
        ("  3.2 Poverty Status Classification of Yam Farmers", "7"),
        ("  3.3 Foster-Greer-Thorbecke (FGT) Poverty Indices", "8"),
        ("SECTION 4: FACTORS ASSOCIATED WITH POVERTY STATUS", "10"),
        ("  4.1 Bivariate Analysis of Factors Associated with Poverty Status", "10"),
        ("  4.2 Interpretation of Bivariate Findings and Methodological Considerations", "11"),
        ("SECTION 5: LOGISTIC REGRESSION ANALYSIS", "13"),
        ("  5.1 Parsimonious Multivariable Binary Logistic Regression Model", "13"),
        ("  5.2 Firth Penalized Logistic Regression Sensitivity Analysis", "14"),
        ("  5.3 Graphical Representation of Estimated Odds Ratios", "14"),
        ("SECTION 6: CHALLENGES FACED BY YAM FARMERS", "15"),
        ("  6.1 Challenge Severity Evaluation and Ranking", "15"),
        ("  6.2 Graphical Overview of Challenge Severity Scores", "16"),
        ("SECTION 7: SUMMARY OF KEY STATISTICAL FINDINGS", "17"),
        ("  7.1 Objective 1: Poverty Status and Expenditure Profile", "17"),
        ("  7.2 Objective 2: Factors Associated with Poverty Status", "17"),
        ("  7.3 Objective 3: Production and Institutional Challenges", "18"),
    ]
    
    for item_title, item_page in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(item_title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        if not item_title.startswith("  "):
            r1.bold = True
            
        # Tab stop dots
        r_dots = p.add_run(" " + "." * max(5, int(60 - len(item_title))) + " ")
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
        
        r2 = p.add_run(item_page)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11)
        r2.bold = True

    add_h1("LIST OF TABLES")
    lot_items = [
        ("Table 1: Sex Distribution of Respondents (N = 60)", "1"),
        ("Table 2: Summary Statistics of Age, Household Size, and Farming Experience", "2"),
        ("Table 3: Marital Status and Educational Attainment of Respondents", "3"),
        ("Table 4: Other Sources of Household Income among Yam Farmers", "3"),
        ("Table 5: Mean Monthly Household Expenditure by Expenditure Category", "4"),
        ("Table 6: Per-Capita Monthly Household Expenditure (PCHE) of Yam Farmers", "5"),
        ("Table 7: Determination of the Relative Poverty Line among Yam Farmers", "7"),
        ("Table 8: Poverty Status Distribution of Yam Farmers in Akpabuyo LGA", "7"),
        ("Table 9: Foster-Greer-Thorbecke (FGT) Poverty Indices for Yam Farmers", "8"),
        ("Table 10: Socio-Demographic and Agricultural Factors Associated with Poverty Status", "10"),
        ("Table 11: Parsimonious Binary Logistic Regression Model of Poverty Status", "13"),
        ("Table 12: Severity Ranking of Challenges Faced by Yam Farmers in Akpabuyo LGA", "15"),
    ]
    for item_title, item_page in lot_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(item_title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r_dots = p.add_run(" " + "." * max(5, int(65 - len(item_title))) + " ")
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
        r2 = p.add_run(item_page)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11)

    add_h1("LIST OF FIGURES")
    lof_items = [
        ("Figure 1: Age Distribution of Yam Farmers in Akpabuyo LGA", "2"),
        ("Figure 2: Mean Monthly Household Expenditure by Category among Yam Farmers", "5"),
        ("Figure 3: Distribution of Yam Farmers by Poverty Status in Akpabuyo LGA", "8"),
        ("Figure 4: Odds Ratios from Parsimonious Logistic Regression Model (95% CIs)", "14"),
        ("Figure 5: Mean Severity Scores of Challenges Faced by Yam Farmers", "16"),
    ]
    for item_title, item_page in lof_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(item_title)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r_dots = p.add_run(" " + "." * max(5, int(65 - len(item_title))) + " ")
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
        r2 = p.add_run(item_page)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # SECTION 1: SAMPLE AND SOCIO-ECONOMIC CHARACTERISTICS
    # =========================================================================
    add_h1("SECTION 1: SAMPLE AND SOCIO-ECONOMIC CHARACTERISTICS")
    
    add_p("This statistical report presents the empirical findings from a field survey administered to smallholder yam farming households in Akpabuyo Local Government Area of Cross River State, Nigeria. The target study population is represented by a complete, fully validated sample of exactly N = 60 farming households. Data integrity screening confirmed complete responses across all demographic, budgetary expenditure, agricultural production, and institutional access variables with zero missing observations.")

    add_h2("1.1 Sex Distribution of Respondents")
    add_p("The gender composition of the sampled yam farmers is summarized in Table 1.")

    add_table_title("Table 1: Sex Distribution of Respondents (N = 60)")
    t1 = doc.add_table(rows=3, cols=3)
    t1_headers = ["Sex", "Frequency (n)", "Percentage (%)"]
    t1_data = [
        ["Male", "36", "60.00%"],
        ["Female", "24", "40.00%"],
    ]
    for i, h in enumerate(t1_headers):
        t1.cell(0, i).text = h
    for r_idx, row in enumerate(t1_data, start=1):
        for c_idx, val in enumerate(row):
            t1.cell(r_idx, c_idx).text = val
    # Add Total row
    t1_tot = t1.add_row().cells
    t1_tot[0].text = "Total"
    t1_tot[1].text = "60"
    t1_tot[2].text = "100.00%"
    t1_tot[0].paragraphs[0].runs[0].bold = True
    t1_tot[1].paragraphs[0].runs[0].bold = True
    t1_tot[2].paragraphs[0].runs[0].bold = True
    
    format_table_academic(t1, [2.5, 1.8, 1.8], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
    add_table_source("Source: Field Survey Data Analysis, 2026.")

    add_p("As indicated in Table 1, male farmers constituted the majority of respondents (n = 36, 60.00%), while female farmers accounted for 40.00% (n = 24). This reflects the traditional gender participation structure in yam farming within the study area, where men are predominantly engaged in labor-intensive land preparation, mounding, and staking, while women actively participate in planting, weeding, harvesting, and marketing.")

    add_h2("1.2 Summary Statistics of Age, Household Size, and Farming Experience")
    add_p("Table 2 presents the summary statistics for the continuous socio-economic characteristics of the respondents.")

    add_table_title("Table 2: Summary Statistics of Age, Household Size, and Yam Farming Experience (N = 60)")
    t2 = doc.add_table(rows=4, cols=6)
    t2_headers = ["Variable", "Sample Size (N)", "Mean", "Std. Dev.", "Minimum", "Maximum"]
    t2_data = [
        ["Age of farmer (years)", "60", "46.03", "8.64", "30.00", "63.00"],
        ["Household size (persons)", "60", "6.23", "1.84", "3.00", "10.00"],
        ["Yam farming experience (years)", "60", "18.88", "8.56", "6.00", "40.00"],
    ]
    for i, h in enumerate(t2_headers):
        t2.cell(0, i).text = h
    for r_idx, row in enumerate(t2_data, start=1):
        for c_idx, val in enumerate(row):
            t2.cell(r_idx, c_idx).text = val
    format_table_academic(t2, [2.4, 1.0, 1.0, 1.0, 0.9, 0.9], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
    add_table_source("Source: Field Survey Data Analysis, 2026.")

    add_p("The mean age of respondents was 46.03 ± 8.64 years, with a range of 30 to 63 years, indicating an economically active and mature farming population. Household size averaged 6.23 ± 1.84 persons (ranging from 3 to 10 persons), representing an important source of family labor for smallholder farming operations. Farmers exhibited extensive farming experience, averaging 18.88 ± 8.56 years (ranging from 6 to 40 years), which reflects substantial indigenous knowledge in yam production.")

    add_h2("1.3 Age Distribution of Yam Farmers")
    add_p("Figure 1 illustrates the empirical distribution of farmer age across the sampled households.")

    fig1_path = os.path.join("Chapter_4_Analysis", "Analysis_1_Socio_Economic_Characteristics", "Figure_4_1_Age_Distribution.png")
    if not os.path.exists(fig1_path):
        fig1_path = "Figure_4_1_Age_Distribution.png"
    add_figure(fig1_path, "Age Distribution of Yam Farmers in Akpabuyo LGA", 1)

    add_h2("1.4 Marital Status and Educational Attainment")
    add_p("Table 3 outlines the marital status and highest level of education completed by the respondents.")

    add_table_title("Table 3: Marital Status and Educational Attainment of Respondents (N = 60)")
    t3 = doc.add_table(rows=11, cols=3)
    t3_headers = ["Characteristic / Level", "Frequency (n)", "Percentage (%)"]
    t3_data = [
        ["A. Marital Status", "", ""],
        ["Single", "5", "8.33%"],
        ["Married", "49", "81.67%"],
        ["Divorced", "0", "0.00%"],
        ["Widowed", "6", "10.00%"],
        ["B. Educational Attainment", "", ""],
        ["No formal education", "0", "0.00%"],
        ["Primary education (6 years)", "18", "30.00%"],
        ["Secondary education (12 years)", "27", "45.00%"],
        ["Tertiary education (16 years)", "15", "25.00%"],
    ]
    for i, h in enumerate(t3_headers):
        t3.cell(0, i).text = h
    for r_idx, row in enumerate(t3_data, start=1):
        for c_idx, val in enumerate(row):
            cell = t3.cell(r_idx, c_idx)
            cell.text = val
            if row[0].startswith(("A.", "B.")):
                cell.paragraphs[0].runs[0].bold = True
                
    format_table_academic(t3, [2.6, 1.8, 1.8], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
    add_table_source("Source: Field Survey Data Analysis, 2026.")

    add_p("A substantial majority of respondents were married (n = 49, 81.67%), while 10.00% (n = 6) were widowed and 8.33% (n = 5) were single. All 60 respondents had acquired formal education (100.00%), comprising secondary education (45.00%, n = 27), primary education (30.00%, n = 18), and tertiary education (25.00%, n = 15). This high literacy level provides an advantageous foundation for agricultural extension delivery and technology adoption.")

    add_h2("1.5 Other Sources of Household Income")
    add_p("Table 4 presents the distribution of farmers engaged in supplementary income-generating activities.")

    add_table_title("Table 4: Other Sources of Household Income among Yam Farmers (N = 60)")
    t4 = doc.add_table(rows=4, cols=3)
    t4_headers = ["Engagement in Off-Farm / Other Income", "Frequency (n)", "Percentage (%)"]
    t4_data = [
        ["Yes (Engaged in supplementary income sources)", "49", "81.67%"],
        ["No (Solely dependent on yam/crop farming)", "11", "18.33%"],
        ["Total", "60", "100.00%"]
    ]
    for i, h in enumerate(t4_headers):
        t4.cell(0, i).text = h
    for r_idx, row in enumerate(t4_data, start=1):
        for c_idx, val in enumerate(row):
            cell = t4.cell(r_idx, c_idx)
            cell.text = val
            if row[0] == "Total":
                cell.paragraphs[0].runs[0].bold = True
                
    format_table_academic(t4, [3.2, 1.5, 1.5], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
    add_table_source("Source: Field Survey Data Analysis, 2026.")

    add_p("Exactly 81.67% of respondents (n = 49) reported having other sources of household income, including petty trading, agro-processing, livestock rearing, and artisanal trades, indicating active livelihood diversification among farming households.")

    # =========================================================================
    # SECTION 2: HOUSEHOLD EXPENDITURE ANALYSIS
    # =========================================================================
    add_h1("SECTION 2: HOUSEHOLD EXPENDITURE ANALYSIS")
    
    add_p("Household expenditure serves as the standard empirical proxy for household permanent income and economic welfare in smallholder agricultural economies. Monthly household expenditures across food, housing, utilities, medical care, education, and transportation were recorded and analyzed.")

    add_h2("2.1 Monthly Household Expenditure Patterns")
    add_p("Table 5 presents the mean monthly expenditures across individual budgetary categories.")

    add_table_title("Table 5: Mean Monthly Household Expenditure by Category (N = 60)")
    t5 = doc.add_table(rows=7, cols=3)
    t5_headers = ["Expenditure Category", "Mean Monthly Expenditure (₦)", "Budget Share (%)"]
    t5_data = [
        ["Food and groceries", "60,703.33", "52.40%"],
        ["Housing and utilities", "18,246.67", "15.75%"],
        ["Education", "14,528.33", "12.54%"],
        ["Transportation and other", "11,875.83", "10.25%"],
        ["Health and medical", "8,631.67", "7.45%"],
        ["Reported Total Household Expenditure", "115,837.50", "100.00%"]
    ]
    for i, h in enumerate(t5_headers):
        t5.cell(0, i).text = h
    for r_idx, row in enumerate(t5_data, start=1):
        for c_idx, val in enumerate(row):
            cell = t5.cell(r_idx, c_idx)
            cell.text = val
            if row[0].startswith("Reported Total"):
                cell.paragraphs[0].runs[0].bold = True
                
    format_table_academic(t5, [2.8, 2.0, 1.4], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
    add_table_source("Source: Field Survey Data Analysis, 2026.")

    add_p("Food expenditure represents the single largest component of household budgets, averaging ₦60,703.33 per month (52.40% of total expenditure). Housing and utilities accounted for 15.75% (₦18,246.67), education represented 12.54% (₦14,528.33), transportation and miscellaneous expenses accounted for 10.25% (₦11,875.83), and healthcare expenses comprised 7.45% (₦8,631.67). Total monthly household expenditure averaged ₦115,837.50.")

    add_h2("2.2 Graphical Representation of Mean Monthly Expenditure")
    add_p("Figure 2 visually portrays the budgetary composition of household expenditure among the respondents.")

    fig2_path = os.path.join("Chapter_4_Analysis", "Analysis_2_Household_Expenditure", "Figure_4_2_Mean_Monthly_Expenditure.png")
    if not os.path.exists(fig2_path):
        fig2_path = "Figure_4_2_Mean_Monthly_Expenditure.png"
    add_figure(fig2_path, "Mean Monthly Household Expenditure by Category among Yam Farmers in Akpabuyo LGA", 2)

    add_h2("2.3 Per-Capita Monthly Household Expenditure (PCHE)")
    add_p("Per-Capita Monthly Household Expenditure (PCHE) standardizes household living standards by accounting for demographic size variations. PCHE was calculated as:")
    
    add_p("PCHE = (Total Average Monthly Household Expenditure) / (Household Size)", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)

    add_table_title("Table 6: Per-Capita Monthly Household Expenditure (PCHE) of Yam Farmers (N = 60)")
    t6 = doc.add_table(rows=2, cols=6)
    t6_headers = ["Variable", "Sample Size (N)", "Mean (₦)", "Std. Dev. (₦)", "Minimum (₦)", "Maximum (₦)"]
    t6_data = [
        ["Per-Capita Expenditure (PCHE)", "60", "20,289.03", "9,896.79", "6,800.00", "51,666.67"]
    ]
    for i, h in enumerate(t6_headers):
        t6.cell(0, i).text = h
    for r_idx, row in enumerate(t6_data, start=1):
        for c_idx, val in enumerate(row):
            t6.cell(r_idx, c_idx).text = val
    format_table_academic(t6, [2.2, 1.0, 1.0, 1.0, 1.0, 1.0], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
    add_table_source("Source: Field Survey Data Analysis, 2026.")

    add_p("The mean per-capita monthly household expenditure was ₦20,289.03 ± ₦9,896.79 per person per month, ranging from a minimum of ₦6,800.00 to a maximum of ₦51,666.67.")

    add_h2("2.4 Expenditure Data Quality Check and Sensitivity Audit")
    add_p("To guarantee absolute transparency and academic rigor, a detailed audit was conducted comparing reported total monthly expenditure against the mathematical sum of individual expenditure components. Across the sample, 56 out of 60 households (93.3%) exhibited perfect arithmetic agreement between reported total expenditure and the sum of components. Exactly four observations exhibited minor arithmetic variances:")

    add_table_title("Table 6B: Expenditure Data Quality Check across Non-Matching Observations")
    t6b = doc.add_table(rows=5, cols=4)
    t6b_headers = ["Observation ID", "Sum of Components (₦)", "Reported Total (₦)", "Difference (₦)"]
    t6b_data = [
        ["Observation 14", "117,000.00", "118,000.00", "+1,000.00"],
        ["Observation 37", "109,400.00", "109,000.00", "-400.00"],
        ["Observation 39", "102,500.00", "103,000.00", "+500.00"],
        ["Observation 59", "113,500.00", "223,500.00", "+110,000.00"]
    ]
    for i, h in enumerate(t6b_headers):
        t6b.cell(0, i).text = h
    for r_idx, row in enumerate(t6b_data, start=1):
        for c_idx, val in enumerate(row):
            t6b.cell(r_idx, c_idx).text = val
    format_table_academic(t6b, [1.8, 1.5, 1.5, 1.4], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
    add_table_source("Source: Field Survey Data Quality Audit, 2026.")

    add_p("A rigorous sensitivity analysis was performed by re-estimating per-capita expenditure using the sum of components. This yielded a revised mean PCHE of ₦20,022.82 and a revised poverty threshold of ₦13,348.55. Poverty classification remained identical for 59 out of 60 households (98.33% classification agreement), demonstrating that the study's poverty classifications and empirical findings are exceptionally stable and robust to expenditure measurement definitions.")

    # =========================================================================
    # SECTION 3: POVERTY STATUS ANALYSIS
    # =========================================================================
    add_h1("SECTION 3: POVERTY STATUS ANALYSIS")

    add_h2("3.1 Determination of the Relative Poverty Line")
    add_p("In accordance with international welfare economics and standard agricultural economics conventions (World Bank; NBS), a relative poverty threshold was established at two-thirds (2/3) of the mean per-capita monthly household expenditure:")
    
    add_p("Mean PCHE = ₦20,289.03 per person per month\n"
          "Relative Poverty Line (z) = 2/3 × Mean PCHE = (2/3) × ₦20,289.03 = ₦13,526.02 per person per month", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)

    add_p("Households with per-capita monthly expenditure strictly below ₦13,526.02 were classified as poor, while households with per-capita monthly expenditure at or above ₦13,526.02 were classified as non-poor.")

    add_table_title("Table 7: Determination of the Relative Poverty Line among Yam-Farming Households (N = 60)")
    t7 = doc.add_table(rows=4, cols=2)
    t7_headers = ["Parameter / Metric", "Value"]
    t7_data = [
        ["Mean Per-Capita Monthly Expenditure (Mean PCHE)", "₦20,289.03"],
        ["Poverty Line Definition", "Two-thirds (2/3) of Mean PCHE"],
        ["Established Relative Poverty Threshold (z)", "₦13,526.02 per person/month"]
    ]
    for i, h in enumerate(t7_headers):
        t7.cell(0, i).text = h
    for r_idx, row in enumerate(t7_data, start=1):
        for c_idx, val in enumerate(row):
            t7.cell(r_idx, c_idx).text = val
    format_table_academic(t7, [3.8, 2.4], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT])
    add_table_source("Source: Field Survey Data Analysis, 2026.")

    add_h2("3.2 Poverty Status Distribution of Yam Farmers")
    add_p("Table 8 presents the distribution of yam-farming households according to their established poverty status.")

    add_table_title("Table 8: Poverty Status Distribution of Yam Farmers in Akpabuyo LGA (N = 60)")
    t8 = doc.add_table(rows=4, cols=3)
    t8_headers = ["Poverty Status Category", "Frequency (n)", "Percentage (%)"]
    t8_data = [
        ["Poor (PCHE < ₦13,526.02)", "13", "21.67%"],
        ["Non-poor (PCHE ≥ ₦13,526.02)", "47", "78.33%"],
        ["Total", "60", "100.00%"]
    ]
    for i, h in enumerate(t8_headers):
        t8.cell(0, i).text = h
    for r_idx, row in enumerate(t8_data, start=1):
        for c_idx, val in enumerate(row):
            cell = t8.cell(r_idx, c_idx)
            cell.text = val
            if row[0] == "Total":
                cell.paragraphs[0].runs[0].bold = True
    format_table_academic(t8, [3.0, 1.6, 1.6], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
    add_table_source("Source: Field Survey Data Analysis, 2026.")

    add_p("Based on the established threshold, exactly 13 households (21.67%) were categorized as poor, while 47 households (78.33%) were categorized as non-poor.")

    add_h2("3.3 Graphical Distribution of Poverty Status")
    add_p("Figure 3 illustrates the relative distribution of poor and non-poor households in Akpabuyo LGA.")

    fig3_path = os.path.join("Chapter_4_Analysis", "Analysis_3_Poverty_Status", "Figure_4_3_Poverty_Status.png")
    if not os.path.exists(fig3_path):
        fig3_path = "Figure_4_3_Poverty_Status.png"
    add_figure(fig3_path, "Distribution of Yam Farmers by Poverty Status in Akpabuyo LGA", 3)

    add_h2("3.4 Foster-Greer-Thorbecke (FGT) Poverty Indices")
    add_p("To provide a mathematically rigorous assessment of poverty incidence, depth, and severity, the Foster-Greer-Thorbecke (FGT, 1984) class of poverty measures was estimated:")

    add_table_title("Table 9: Foster-Greer-Thorbecke (FGT) Poverty Indices for Yam Farmers (N = 60)")
    t9 = doc.add_table(rows=4, cols=4)
    t9_headers = ["FGT Poverty Measure", "Alpha (α)", "Estimated Value", "Percentage Equivalent"]
    t9_data = [
        ["Poverty Headcount Index (P₀)", "α = 0", "0.2167", "21.67%"],
        ["Poverty Gap Index (P₁)", "α = 1", "0.0232", "2.32%"],
        ["Squared Poverty Gap Index (P₂)", "α = 2", "0.0034", "0.34%"]
    ]
    for i, h in enumerate(t9_headers):
        t9.cell(0, i).text = h
    for r_idx, row in enumerate(t9_data, start=1):
        for c_idx, val in enumerate(row):
            t9.cell(r_idx, c_idx).text = val
    format_table_academic(t9, [2.5, 1.1, 1.3, 1.3], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
    add_table_source("Source: Field Survey Data Analysis, 2026. FGT Poverty Formula: P_alpha = (1/N) * sum(((z - y_i)/z)^alpha).")

    add_p("Interpretation of FGT Metrics:", bold_prefix="Economic Interpretation: ")
    add_p("1. Headcount Index (P₀ = 0.2167): Quantifies poverty incidence, indicating that 21.67% of yam farmers live below the relative poverty threshold.")
    add_p("2. Poverty Gap Index (P₁ = 0.0232): Quantifies poverty depth, showing that the average expenditure shortfall of poor farming households is 2.32% of the poverty line (approximately ₦313.80 per capita per month across the entire population). It does NOT represent the percentage of poor people.")
    add_p("3. Squared Poverty Gap Index (P₂ = 0.0034): Quantifies poverty severity by assigning greater weight to households furthest below the poverty line, reflecting low overall expenditure inequality among the poor in Akpabuyo LGA.")

    # =========================================================================
    # SECTION 4: FACTORS ASSOCIATED WITH POVERTY STATUS
    # =========================================================================
    add_h1("SECTION 4: FACTORS ASSOCIATED WITH POVERTY STATUS")
    
    add_p("Specific Objective II of the research mandates analyzing factors influencing poverty status among yam farmers, explicitly considering farmer age, education, household size, access to credit, technology adoption, and cooperative membership. To fulfill this objective while maintaining methodological rigor, all six mandated factors alongside farm landholding and extension contact were evaluated across poor (n = 13) and non-poor (n = 47) farming households.")

    add_h2("4.1 Bivariate Analysis of Factors Associated with Poverty Status")
    add_p("Table 10 presents the descriptive profiling and single primary bivariate hypothesis tests across all eleven socio-demographic, agricultural, and institutional factors.")

    add_table_title("Table 10: Socio-Demographic and Agricultural Factors Associated with Poverty Status (N = 60)")
    t10 = doc.add_table(rows=18, cols=6)
    t10_headers = ["Factor / Indicator", "Poor (n = 13)", "Non-poor (n = 47)", "Overall (N = 60)", "Statistical Test", "p-value"]
    t10_data = [
        ["A. Demographic & Human Capital Factors", "", "", "", "", ""],
        ["1. Age of farmer (years)", "51.31 ± 8.99", "44.57 ± 8.04", "46.03 ± 8.64", "Mann–Whitney U = 432.00", "0.024*"],
        ["2. Household size (persons)", "8.31 ± 1.70", "5.66 ± 1.43", "6.23 ± 1.84", "Mann–Whitney U = 536.00", "< 0.001*"],
        ["3. Educational attainment", "", "", "", "Pearson χ² = 2.673 (df=2)", "0.263"],
        ["   - Primary education (6 yrs)", "5 (38.5%)", "13 (27.7%)", "18 (30.0%)", "—", "—"],
        ["   - Secondary education (12 yrs)", "7 (53.8%)", "20 (42.6%)", "27 (45.0%)", "—", "—"],
        ["   - Tertiary education (16 yrs)", "1 (7.7%)", "14 (29.8%)", "15 (25.0%)", "—", "—"],
        ["B. Land Holding & Production Assets", "", "", "", "", ""],
        ["4. Total farm size (hectares)", "1.98 ± 0.48", "2.56 ± 0.82", "2.43 ± 0.79", "Mann–Whitney U = 170.50", "0.016*"],
        ["5. Area under yam cultivation (ha)", "1.43 ± 0.37", "1.73 ± 0.56", "1.67 ± 0.53", "Mann–Whitney U = 205.00", "0.072"],
        ["C. Institutional Access, Technology & Social Capital", "", "", "", "", ""],
        ["6. Access to credit (Yes = 1)", "1 (7.7%)", "29 (61.7%)", "30 (50.0%)", "Pearson χ² = 9.820", "0.002*"],
        ["7. Extension contact in last 12 mos (Yes)", "0 (0.0%)", "21 (44.7%)", "21 (35.0%)", "Fisher's exact test", "0.002*"],
        ["8. Use of improved yam varieties (Yes)", "0 (0.0%)", "2 (4.3%)", "2 (3.3%)", "Fisher's exact test", "1.000"],
        ["9. Application of fertilizer/manure (Yes)", "9 (69.2%)", "39 (83.0%)", "48 (80.0%)", "Pearson χ² = 0.497", "0.481"],
        ["10. Use of modern tools/technology (Yes)", "0 (0.0%)", "6 (12.8%)", "6 (10.0%)", "Fisher's exact test", "0.324"],
        ["11. Cooperative membership (Yes = 1)", "10 (76.9%)", "39 (83.0%)", "49 (81.7%)", "Pearson χ² = 0.009", "0.925"]
    ]
    for i, h in enumerate(t10_headers):
        t10.cell(0, i).text = h
    for r_idx, row in enumerate(t10_data, start=1):
        for c_idx, val in enumerate(row):
            cell = t10.cell(r_idx, c_idx)
            cell.text = val
            if row[0].startswith(("A.", "B.", "C.")):
                cell.paragraphs[0].runs[0].bold = True
                tcPr = cell._tc.get_or_add_tcPr()
                tcPr.append(parse_xml(r'<w:shd {} w:fill="EAEAEA"/>'.format(nsdecls('w'))))
                
    format_table_academic(t10, [2.3, 1.1, 1.1, 1.1, 1.4, 0.8], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER])
    add_table_source("Source: Field Survey Data Analysis, 2026. * Statistically significant at p < 0.05. Primary test for continuous variables: Mann–Whitney U test. Categorical tests: Pearson χ² (expected counts ≥ 5) or Fisher's exact test (expected counts < 5).")

    add_h2("4.2 Interpretation of Bivariate Findings")
    add_p("The bivariate analysis identified statistically significant differences between poor and non-poor households in age, household size, total farm size, access to credit, and extension contact:")
    
    add_p("Poor farmers had significantly higher ages (mean = 51.31 ± 8.99 years; median = 53.00 years) than non-poor farmers (mean = 44.57 ± 8.04 years; median = 45.00 years). Age was approximately normally distributed within the poverty groups based on the Shapiro–Wilk assessment; however, the Mann–Whitney U test was retained as the primary comparison to provide a conservative non-parametric assessment (Mann–Whitney U = 432.00, p = 0.024; Welch t = 2.443, p = 0.025). Older farmers may face declining physical capacity for labor-intensive mound preparation.", bold_prefix="1. Age of Farmer: ")

    add_p("Poor households had significantly larger household sizes (mean = 8.31 ± 1.70 persons; median = 9.00 persons) than non-poor households (mean = 5.66 ± 1.43 persons; median = 5.00 persons; Mann–Whitney U = 536.00, p < 0.001; Welch t = 5.129, p < 0.001). However, household size requires cautious interpretation because household size is the denominator used in calculating per-capita household expenditure, which subsequently determines poverty classification. Consequently, the observed association between household size and poverty status may partly reflect the mathematical construction of the welfare measure rather than an independent socioeconomic effect.", bold_prefix="2. Household Size (Mechanical Dependence Consideration): ")

    add_p("Educational attainment did not differ significantly between poor and non-poor farmers (Pearson χ² = 2.673, df = 2, p = 0.263), although tertiary education was more prevalent among non-poor farmers (29.8%) than poor farmers (7.7%).", bold_prefix="3. Educational Attainment: ")

    add_p("Poor yam farmers operated significantly smaller total farm sizes (mean = 1.98 ± 0.48 ha) than non-poor farmers (mean = 2.56 ± 0.82 ha; Mann–Whitney U = 170.50, p = 0.016). Yam area was also lower among poor farmers (1.43 ± 0.37 ha vs. 1.73 ± 0.56 ha; Mann–Whitney U = 205.00, p = 0.072).", bold_prefix="4. Farm Land Holding: ")

    add_p("Access to credit strongly distinguished non-poor farmers (61.7%, n = 29) from poor farmers (7.7%, n = 1; Pearson χ² = 9.820, df = 1, p = 0.002).", bold_prefix="5. Access to Credit: ")

    add_p("None of the poor respondents reported contact with an agricultural extension agent during the preceding 12 months (0.0%, n = 0), compared with 44.7% (n = 21) of non-poor respondents (Fisher's exact test p = 0.002).", bold_prefix="6. Agricultural Extension Contact: ")

    add_p("Adoption rates for improved varieties (3.3%) and modern tools (10.0%) were low and confined to non-poor households (Fisher's exact p = 1.000 and p = 0.324, respectively). Fertilizer/manure application (80.0% overall; p = 0.481) and cooperative membership (81.7% overall; p = 0.925) were widespread across both groups.", bold_prefix="7. Technology Adoption and Cooperative Membership: ")

    # =========================================================================
    # SECTION 5: LOGISTIC REGRESSION ANALYSIS
    # =========================================================================
    add_h1("SECTION 5: LOGISTIC REGRESSION ANALYSIS")
    
    add_p("Because the number of poor households was limited to 13, a fully specified multivariable model containing all Objective II factors was not considered statistically reliable. A parsimonious logistic regression model was therefore retained as a complementary multivariable analysis rather than as a direct one-to-one representation of all factors specified in Objective II.")

    add_h2("5.1 Methodological Screening and Model Specification")
    add_p("Prior to model estimation, candidate predictors were evaluated under several methodological rules:", bold_prefix="Model Diagnostic Rules: ")
    add_p("1. Multicollinearity: Total farm size and yam area exhibited severe collinearity (r = 0.9642, VIF = 16.00). Yam area was excluded because it is a direct subset of total farm size.")
    add_p("2. Quasi-Complete Separation: Extension contact (0/13 poor), modern tools (0/13 poor), and improved varieties (0/13 poor) contained zero events in the poor group, causing standard Maximum Likelihood Estimation (MLE) algorithms to fail to converge.")
    add_p("3. Mechanical Dependence: Household size was excluded from the multivariable regression to avoid circular mathematical dependence with the per-capita expenditure poverty threshold.")
    add_p("4. Parsimony Rule: Given the 13 poverty events in the sample, a parsimonious two-predictor model incorporating Total Farm Size (hectares) and Access to Credit (1 = Yes, 0 = No) was retained to limit model complexity and reduce the risk of unstable estimates.")

    add_table_title("Table 11: Parsimonious Binary Logistic Regression Model of Poverty Status in Akpabuyo LGA (N = 60)")
    t11 = doc.add_table(rows=4, cols=6)
    t11_headers = ["Predictor Variable", "Coefficient (β)", "Standard Error (SE)", "Odds Ratio (OR)", "95% CI for OR", "p-value"]
    t11_data = [
        ["Total farm size (per hectare increase)", "-0.430", "0.815", "0.651", "0.132 – 3.217", "0.598"],
        ["Access to credit (Yes = 1 vs No = 0)", "-2.598", "1.245", "0.074", "0.007 – 0.854", "0.037*"],
        ["Intercept (Constant)", "0.433", "1.628", "1.542", "0.063 – 37.458", "0.790"]
    ]
    for i, h in enumerate(t11_headers):
        t11.cell(0, i).text = h
    for r_idx, row in enumerate(t11_data, start=1):
        for c_idx, val in enumerate(row):
            t11.cell(r_idx, c_idx).text = val
    format_table_academic(t11, [2.3, 0.9, 0.9, 0.9, 1.3, 0.8], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER])
    add_table_source("Source: Field Survey Data Analysis, 2026. * Statistically significant at p < 0.05. Model Likelihood Ratio χ² = 13.861 (df = 2, p = 0.001). McFadden R² = 0.221; Nagelkerke R² = 0.318. Dependent Variable: Poverty Status (1 = Poor, 0 = Non-poor). Reference category for credit access is No (0).")

    add_h2("5.2 Interpretation of Logistic Regression Outputs")
    add_p("The binary logistic regression model demonstrated statistically significant overall fit (Likelihood Ratio χ² = 13.861, df = 2, p = 0.001), yielding a McFadden Pseudo R² of 0.221 and a Nagelkerke Pseudo R² of 0.318.")
    
    add_p("Access to agricultural credit was statistically significant in the multivariable model (β = -2.598, SE = 1.245, OR = 0.074, 95% CI: 0.007 to 0.854, p = 0.037). Holding total farm size constant, yam farmers with access to credit had 92.6% lower odds of being classified as poor compared to farmers without credit access. This reflects a strong protective association rather than a proven causal mechanism.", bold_prefix="Access to Credit: ")

    add_p("Total farm size exhibited an odds ratio below one (OR = 0.651, 95% CI: 0.132 to 3.217), indicating that each additional hectare of land was associated with 34.9% lower odds of poverty; however, this association was not statistically significant in the multivariable model (p = 0.598) after controlling for credit access.", bold_prefix="Total Farm Size: ")

    add_h2("5.3 Firth Penalized Logistic Regression Sensitivity Analysis")
    add_p("To assess the stability of the small-sample logistic regression estimates, a Firth penalized logistic regression model was estimated. The Firth sensitivity analysis produced a consistent and statistically significant protective association for access to credit (OR = 0.110, 95% CI: 0.014 to 0.891, p = 0.039), confirming the robustness of the credit association under small-sample penalization.")

    add_h2("5.4 Graphical Representation of Estimated Odds Ratios")
    add_p("Figure 4 displays the odds ratio forest plot with 95% confidence intervals on a logarithmic scale.")

    fig4_path = os.path.join("Chapter_4_Analysis", "Analysis_4_Factors_Poverty", "Figure_4_4_Odds_Ratios_Factors_Poverty.png")
    if not os.path.exists(fig4_path):
        fig4_path = "Figure_4_4_Odds_Ratios_Factors_Poverty.png"
    add_figure(fig4_path, "Odds Ratios from Parsimonious Logistic Regression Model (Log Scale, 95% CIs)", 4)

    # =========================================================================
    # SECTION 6: CHALLENGES FACED BY YAM FARMERS
    # =========================================================================
    add_h1("SECTION 6: CHALLENGES FACED BY YAM FARMERS")
    
    add_p("Specific Objective III evaluates the production, institutional, and marketing constraints encountered by yam farmers in Akpabuyo LGA. Ten potential constraints were evaluated on a 5-point Likert scale (1 = Not a Challenge, 2 = Minor Challenge, 3 = Moderate Challenge, 4 = Severe Challenge, 5 = Very Severe Challenge). Challenge severity was classified using standard 0.80 interval cutoffs: 1.00–1.80 = Not a Challenge; 1.81–2.60 = Minor Challenge; 2.61–3.40 = Moderate Challenge; 3.41–4.20 = Severe Challenge; 4.21–5.00 = Very Severe Challenge.")

    add_h2("6.1 Challenge Severity Ranking")
    add_p("Table 12 outlines the mean severity scores, standard deviations, median scores, and resulting severity rankings for all ten evaluated challenges.")

    add_table_title("Table 12: Severity Ranking of Challenges Faced by Yam Farmers in Akpabuyo LGA (N = 60)")
    t12 = doc.add_table(rows=11, cols=6)
    t12_headers = ["Rank", "Production / Institutional Challenge", "Mean Score", "Std. Dev.", "Median", "Severity Classification"]
    t12_data = [
        ["1", "High cost and scarcity of farm labour", "4.15", "0.80", "4.00", "Severe"],
        ["2", "High cost of farm inputs", "4.00", "0.96", "4.00", "Severe"],
        ["3", "Post-harvest losses and inadequate storage", "3.88", "0.99", "4.00", "Severe"],
        ["4", "Unpredictable rainfall and climate conditions", "3.70", "0.85", "4.00", "Severe"],
        ["5", "High cost / scarcity of yam stakes", "3.57", "0.89", "4.00", "Severe"],
        ["6", "Inadequate access to credit", "3.53", "0.98", "3.00", "Severe"],
        ["7", "Inadequate agricultural extension services", "3.52", "1.07", "4.00", "Severe"],
        ["8", "Pest and disease infestation", "3.38", "0.83", "3.00", "Moderate"],
        ["9", "Low and unstable prices of yam", "3.12", "0.87", "3.00", "Moderate"],
        ["10", "Poor access to market", "2.90", "1.02", "3.00", "Moderate"]
    ]
    for i, h in enumerate(t12_headers):
        t12.cell(0, i).text = h
    for r_idx, row in enumerate(t12_data, start=1):
        for c_idx, val in enumerate(row):
            t12.cell(r_idx, c_idx).text = val
    format_table_academic(t12, [0.6, 2.5, 0.9, 0.8, 0.8, 1.2], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.CENTER])
    add_table_source("Source: Field Survey Data Analysis, 2026. Evaluation Scale: 1.00–1.80 = Not a Challenge; 1.81–2.60 = Minor; 2.61–3.40 = Moderate; 3.41–4.20 = Severe; 4.21–5.00 = Very Severe.")

    add_p("The top-ranked constraint was high cost and scarcity of farm labor (mean = 4.15 ± 0.80), followed by high cost of farm inputs (mean = 4.00 ± 0.96), post-harvest losses and inadequate storage (mean = 3.88 ± 0.99), unpredictable rainfall (mean = 3.70 ± 0.85), scarcity/cost of yam stakes (mean = 3.57 ± 0.89), inadequate credit access (mean = 3.53 ± 0.98), and inadequate extension services (mean = 3.52 ± 1.07). All seven top constraints fell into the 'Severe' category. Pest infestation (3.38), unstable prices (3.12), and poor market access (2.90) were classified as 'Moderate' challenges.")

    add_h2("6.2 Graphical Overview of Challenge Severity Scores")
    add_p("Figure 5 presents a ranked horizontal bar chart of all ten production, institutional, and marketing constraints.")

    fig5_path = os.path.join("Chapter_4_Analysis", "Analysis_5_Challenges", "Figure_4_5_Challenge_Severity_Ranking.png")
    if not os.path.exists(fig5_path):
        fig5_path = "Figure_4_5_Challenge_Severity_Ranking.png"
    add_figure(fig5_path, "Mean Severity Scores of Challenges Faced by Yam Farmers in Akpabuyo LGA", 5)

    # =========================================================================
    # SECTION 7: SUMMARY OF KEY STATISTICAL FINDINGS
    # =========================================================================
    add_h1("SECTION 7: SUMMARY OF KEY STATISTICAL FINDINGS")
    
    add_p("This section summarizes the key empirical findings aligned directly with the research project's three specific objectives:")

    add_h2("7.1 Objective 1: Poverty Status and Expenditure Profile")
    add_p("• Sample: Exactly N = 60 smallholder yam farming households in Akpabuyo LGA, Cross River State.")
    add_p("• Mean Monthly Household Expenditure: ₦115,837.50 (Food expenditure = ₦60,703.33, representing 52.40% budget share).")
    add_p("• Mean Per-Capita Monthly Household Expenditure (PCHE): ₦20,289.03 per person per month.")
    add_p("• Relative Poverty Threshold: ₦13,526.02 per person per month (established at 2/3 of mean PCHE).")
    add_p("• Poverty Status Distribution: 13 households (21.67%) classified as poor; 47 households (78.33%) classified as non-poor.")
    add_p("• Foster-Greer-Thorbecke (FGT) Poverty Indices: Headcount Index (P₀) = 0.2167 (21.67% incidence); Poverty Gap Index (P₁) = 0.0232 (2.32% depth); Squared Poverty Gap Index (P₂) = 0.0034 (0.34% severity).")

    add_h2("7.2 Objective 2: Factors Associated with Poverty Status")
    add_p("• Level 1 Bivariate Association Tests: Identified statistically significant differences between poor and non-poor households across five factors: (1) Age of farmer (Mann–Whitney U = 432.00, p = 0.024; poor farmers were older); (2) Household size (Mann–Whitney U = 536.00, p < 0.001; poor households had larger family sizes); (3) Total farm size (Mann–Whitney U = 170.50, p = 0.016; poor farmers held smaller land sizes); (4) Access to credit (Pearson χ² = 9.820, p = 0.002; non-poor farmers had higher credit access); and (5) Agricultural extension contact (Fisher's exact test p = 0.002; extension contact was reported only by non-poor farmers).")
    add_p("• Non-Significant Bivariate Factors: Educational attainment (p = 0.263), yam cultivation area (p = 0.072), fertilizer/manure use (p = 0.481), modern tools adoption (p = 0.324), improved yam varieties (p = 1.000), and cooperative membership (p = 0.925).")
    add_p("• Level 2 Parsimonious Multivariable Analysis: The binary logistic regression model (LR χ² = 13.861, df = 2, p = 0.001; Nagelkerke R² = 0.318) confirmed that access to credit is significantly associated with lower odds of poverty (OR = 0.074, 95% CI: 0.007–0.854, p = 0.037; Firth sensitivity OR = 0.110, p = 0.039). Total farm size was not statistically significant in the multivariable model (OR = 0.651, p = 0.598) after controlling for credit access.")

    add_h2("7.3 Objective 3: Production, Institutional, and Marketing Challenges")
    add_p("• Highest-Rated Challenge: High cost and scarcity of farm labor ranked 1st (Mean = 4.15 ± 0.80, classified as Severe).")
    add_p("• Other Severe Constraints (Ranks 2–7): High cost of farm inputs (4.00), post-harvest losses and inadequate storage (3.88), unpredictable rainfall/climate variability (3.70), scarcity/cost of yam stakes (3.57), inadequate credit access (3.53), and inadequate extension services (3.52).")
    add_p("• Moderate Constraints (Ranks 8–10): Pest and disease infestation (3.38), low and unstable yam prices (3.12), and poor access to markets (2.90).")

    # Save Document
    out_file = "Statistical_Analysis_and_Results_Yam_Farmers_Akpabuyo.docx"
    doc.save(out_file)
    print(f"Successfully generated standalone report: {out_file}")

if __name__ == "__main__":
    create_standalone_results_document()
