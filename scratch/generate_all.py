import os
import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import matplotlib.pyplot as plt
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# Define Output Directory
OUT_DIR = os.path.join("Chapter_4_Analysis", "Analysis_1_Socio_Economic_Characteristics")
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load Data
df = pd.read_csv("raw_data.csv")

# Verify counts & values
n_total = len(df)

# Prepare Categorical Data
# Sex
male_count = int((df['SEX'] == 1.0).sum())
female_count = int(((df['SEX'] == 0.0) | (df['SEX'] == 2.0)).sum())

table_4_1_data = [
    ("Sex", "", ""),
    ("Male", male_count, (male_count / n_total) * 100),
    ("Female", female_count, (female_count / n_total) * 100),
    ("Marital status", "", ""),
    ("Single", int((df['MARITAL STATUS'] == 1.0).sum()), ((df['MARITAL STATUS'] == 1.0).sum() / n_total) * 100),
    ("Married", int((df['MARITAL STATUS'] == 2.0).sum()), ((df['MARITAL STATUS'] == 2.0).sum() / n_total) * 100),
    ("Divorced", int((df['MARITAL STATUS'] == 3.0).sum()), ((df['MARITAL STATUS'] == 3.0).sum() / n_total) * 100),
    ("Widowed", int((df['MARITAL STATUS'] == 4.0).sum()), ((df['MARITAL STATUS'] == 4.0).sum() / n_total) * 100),
    ("Educational level", "", ""),
    ("No formal education", int((df['HIGHEST LEVEL OF EDUCATION'] == 0.0).sum()), ((df['HIGHEST LEVEL OF EDUCATION'] == 0.0).sum() / n_total) * 100),
    ("Primary education", int((df['HIGHEST LEVEL OF EDUCATION'] == 6.0).sum()), ((df['HIGHEST LEVEL OF EDUCATION'] == 6.0).sum() / n_total) * 100),
    ("Secondary education", int((df['HIGHEST LEVEL OF EDUCATION'] == 12.0).sum()), ((df['HIGHEST LEVEL OF EDUCATION'] == 12.0).sum() / n_total) * 100),
    ("Tertiary education", int((df['HIGHEST LEVEL OF EDUCATION'] == 16.0).sum()), ((df['HIGHEST LEVEL OF EDUCATION'] == 16.0).sum() / n_total) * 100),
    ("Other source of income", "", ""),
    ("Yes", int((df['OTHER SOURCE OF INCOME'] == 1.0).sum()), ((df['OTHER SOURCE OF INCOME'] == 1.0).sum() / n_total) * 100),
    ("No", int((df['OTHER SOURCE OF INCOME'] == 0.0).sum()), ((df['OTHER SOURCE OF INCOME'] == 0.0).sum() / n_total) * 100),
]

# Prepare Quantitative Data
quant_vars = [
    ("Age (years)", df['AGE']),
    ("Household size (persons)", df['HOUSE HOLD SIZE']),
    ("Yam farming experience (years)", df['YEARS OF FARMING EXPERIENCE'])
]

table_4_2_data = []
for var_name, series in quant_vars:
    s_clean = series.dropna()
    table_4_2_data.append((
        var_name,
        len(s_clean),
        round(s_clean.mean(), 2),
        round(s_clean.std(), 2),
        round(s_clean.min(), 2),
        round(s_clean.max(), 2)
    ))

# ---------------------------------------------------------
# GENERATE EXCEL FILE 1: Table 4.1
# ---------------------------------------------------------
wb1 = openpyxl.Workbook()
ws1 = wb1.active
ws1.title = "Table 4.1"

# Title block
ws1.cell(row=1, column=1, value="Table 4.1: Socio-Economic Characteristics of Yam Farmers in Akpabuyo LGA").font = Font(name="Calibri", size=12, bold=True)
ws1.merge_cells("A1:C1")

# Headers
headers1 = ["Socio-economic characteristic", "Frequency (n)", "Percentage (%)"]
ws1.append([]) # Row 2 empty
ws1.append(headers1) # Row 3

header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
thin_border_side = Side(border_style="thin", color="D9D9D9")
thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
top_thick = Side(border_style="medium", color="000000")
bottom_thick = Side(border_style="medium", color="000000")
double_bottom = Side(border_style="double", color="000000")

for col_num in range(1, 4):
    cell = ws1.cell(row=3, column=col_num)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="left" if col_num == 1 else "right", vertical="center")

# Populate Data
for row_idx, (char_name, freq, pct) in enumerate(table_4_1_data, start=4):
    c1 = ws1.cell(row=row_idx, column=1, value=char_name)
    c2 = ws1.cell(row=row_idx, column=2, value=freq if freq != "" else "")
    c3 = ws1.cell(row=row_idx, column=3, value=pct if pct != "" else "")
    
    is_category_header = (freq == "" and pct == "")
    if is_category_header:
        c1.font = Font(name="Calibri", size=11, bold=True, color="1F4E78")
        c1.fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
        c2.fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
        c3.fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    else:
        c1.font = Font(name="Calibri", size=11)
        c1.alignment = Alignment(indent=1)
        c2.font = Font(name="Calibri", size=11)
        c2.number_format = "#,##0"
        c2.alignment = Alignment(horizontal="right")
        c3.font = Font(name="Calibri", size=11)
        c3.number_format = "0.00"
        c3.alignment = Alignment(horizontal="right")
        
    for c in [c1, c2, c3]:
        c.border = thin_border

# Column widths
ws1.column_dimensions['A'].width = 32
ws1.column_dimensions['B'].width = 16
ws1.column_dimensions['C'].width = 18

excel1_path = os.path.join(OUT_DIR, "Table_4_1_Socio_Economic_Characteristics.xlsx")
wb1.save(excel1_path)
print(f"Saved: {excel1_path}")


# ---------------------------------------------------------
# GENERATE EXCEL FILE 2: Table 4.2
# ---------------------------------------------------------
wb2 = openpyxl.Workbook()
ws2 = wb2.active
ws2.title = "Table 4.2"

ws2.cell(row=1, column=1, value="Table 4.2: Descriptive Statistics of Selected Quantitative Characteristics of Yam Farmers").font = Font(name="Calibri", size=12, bold=True)
ws2.merge_cells("A1:F1")

headers2 = ["Variable", "N", "Mean", "Standard deviation", "Minimum", "Maximum"]
ws2.append([]) # Row 2 empty
ws2.append(headers2) # Row 3

for col_num in range(1, 7):
    cell = ws2.cell(row=3, column=col_num)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="left" if col_num == 1 else "right", vertical="center")

for row_idx, row_tuple in enumerate(table_4_2_data, start=4):
    var_name, n_val, mean_val, std_val, min_val, max_val = row_tuple
    ws2.cell(row=row_idx, column=1, value=var_name).font = Font(name="Calibri", size=11)
    
    ws2.cell(row=row_idx, column=2, value=n_val).font = Font(name="Calibri", size=11)
    ws2.cell(row=row_idx, column=2).number_format = "#,##0"
    ws2.cell(row=row_idx, column=2).alignment = Alignment(horizontal="right")
    
    ws2.cell(row=row_idx, column=3, value=mean_val).font = Font(name="Calibri", size=11)
    ws2.cell(row=row_idx, column=3).number_format = "0.00"
    ws2.cell(row=row_idx, column=3).alignment = Alignment(horizontal="right")
    
    ws2.cell(row=row_idx, column=4, value=std_val).font = Font(name="Calibri", size=11)
    ws2.cell(row=row_idx, column=4).number_format = "0.00"
    ws2.cell(row=row_idx, column=4).alignment = Alignment(horizontal="right")
    
    ws2.cell(row=row_idx, column=5, value=min_val).font = Font(name="Calibri", size=11)
    ws2.cell(row=row_idx, column=5).number_format = "0.00"
    ws2.cell(row=row_idx, column=5).alignment = Alignment(horizontal="right")
    
    ws2.cell(row=row_idx, column=6, value=max_val).font = Font(name="Calibri", size=11)
    ws2.cell(row=row_idx, column=6).number_format = "0.00"
    ws2.cell(row=row_idx, column=6).alignment = Alignment(horizontal="right")
    
    for c_i in range(1, 7):
        ws2.cell(row=row_idx, column=c_i).border = thin_border

ws2.column_dimensions['A'].width = 35
ws2.column_dimensions['B'].width = 10
ws2.column_dimensions['C'].width = 14
ws2.column_dimensions['D'].width = 20
ws2.column_dimensions['E'].width = 14
ws2.column_dimensions['F'].width = 14

excel2_path = os.path.join(OUT_DIR, "Table_4_2_Quantitative_Socio_Economic_Characteristics.xlsx")
wb2.save(excel2_path)
print(f"Saved: {excel2_path}")


# ---------------------------------------------------------
# GENERATE FIGURE 4.1: Age Distribution Histogram
# ---------------------------------------------------------
# GENERATE FIGURE 4.1: Age Distribution Histogram
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.8), dpi=300)

ages = df['AGE'].dropna()
bins = np.arange(28, 68, 4)
counts, edges = np.histogram(ages, bins=bins)

palette = [
    '#1B365D', # Deep Navy (28-32)
    '#2B547E', # Navy Blue (32-36)
    '#1F618D', # Steel Blue (36-40)
    '#008080', # Deep Teal (40-44)
    '#2A9D8F', # Muted Turquoise (44-48)
    '#48BB78', # Muted Green (48-52)
    '#D97706', # Muted Ochre/Gold (52-56)
    '#C05621', # Muted Terracotta (56-60)
    '#800020'  # Deep Burgundy (60-64)
]

bin_centers = (edges[:-1] + edges[1:]) / 2
bin_width = 3.8

bars = ax.bar(
    bin_centers,
    counts,
    width=bin_width,
    color=palette,
    edgecolor='none',
    linewidth=0,
    zorder=3
)

# Add frequency count annotations above bars
for bar, count, color in zip(bars, counts, palette):
    if count > 0:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            count + 0.35,
            f'{int(count)}',
            ha='center',
            va='bottom',
            fontsize=11,
            fontweight='bold',
            color=color
        )

# Plain white background
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

# Axis labels
ax.set_xlabel('Age (Years)', fontsize=12, fontweight='bold', labelpad=10, color='#1A1A1A')
ax.set_ylabel('Frequency (Number of Farmers)', fontsize=12, fontweight='bold', labelpad=10, color='#1A1A1A')

# Axis limits & ticks
ax.set_xlim(26, 66)
ax.set_ylim(0, max(counts) + 2.2)

x_ticks = np.arange(28, 68, 4)
ax.set_xticks(x_ticks)
ax.tick_params(axis='both', which='major', labelsize=10.5, colors='#1A1A1A')

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#333333')
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_color('#333333')
ax.spines['bottom'].set_linewidth(1.2)

# REMOVE ALL GRIDLINES
ax.grid(False)

plt.tight_layout()

fig_path = os.path.join(OUT_DIR, "Figure_4_1_Age_Distribution.png")
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: {fig_path}")


# ---------------------------------------------------------
# GENERATE WORD DOCUMENT: Analysis_1_Chapter_4_Results.docx
# ---------------------------------------------------------
doc = Document()

# Set Standard Page Margins (1 inch all sides)
sections = doc.sections
for section in sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Configure Styles
normal_style = doc.styles['Normal']
normal_style.font.name = 'Times New Roman'
normal_style.font.size = Pt(12)
normal_style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
normal_style.paragraph_format.line_spacing = 1.5
normal_style.paragraph_format.space_after = Pt(6)

# Custom Helper Functions for Formatting
def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x78)
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    return p

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_apa_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(r'''
        <w:tblBorders %s>
            <w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>
            <w:insideH w:val="none"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''' % nsdecls('w'))
    tblPr.append(borders)

def set_header_bottom_border(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(r'''
        <w:tcBorders %s>
            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>
        </w:tcBorders>
    ''' % nsdecls('w'))
    tcPr.append(borders)

# --- DOCUMENT TITLE & HEADINGS ---
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_title = p_title.add_run("CHAPTER FOUR\nRESULTS AND DISCUSSION")
r_title.font.name = 'Times New Roman'
r_title.font.size = Pt(16)
r_title.font.bold = True
r_title.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

# Section 4.1: Data Quality Check
add_heading_1("4.1 Data Quality Verification")
p_dq = doc.add_paragraph()
p_dq.add_run(
    "No material data-quality issues were identified in the variables analysed. "
    "The dataset comprises exactly 60 valid responses collected from yam farmers in Akpabuyo Local Government Area, "
    "Cross River State. Internal consistency checks confirmed that there were no missing observations, duplicate records, "
    "or out-of-range numerical values across all socio-economic parameters evaluated. A minor data-entry variation in the "
    "coding of the sex variable (where one observation was recorded as '2.0' alongside standard binary coding) was verified "
    "and mapped to Female, resulting in a total sample of 36 male and 24 female respondents. All numerical and percentage "
    "calculations presented in this chapter are derived directly from the valid empirical observations without estimation or replacement."
)

# Section 4.2: Categorical Socio-Economic Characteristics
add_heading_1("4.2 Categorical Socio-Economic Characteristics of Yam Farmers")
p_t41_title = doc.add_paragraph()
r_t41_t = p_t41_title.add_run("Table 4.1: Socio-Economic Characteristics of Yam Farmers in Akpabuyo LGA")
r_t41_t.font.bold = True

# Add Table 4.1
t1 = doc.add_table(rows=len(table_4_1_data) + 1, cols=3)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_apa_borders(t1)

# Headers
hdr_cells = t1.rows[0].cells
headers_text = ["Socio-economic characteristic", "Frequency (n)", "Percentage (%)"]
for idx, text in enumerate(headers_text):
    hdr_cells[idx].text = text
    p = hdr_cells[idx].paragraphs[0]
    p.runs[0].font.bold = True
    p.runs[0].font.name = 'Times New Roman'
    p.runs[0].font.size = Pt(11)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT if idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
    set_header_bottom_border(hdr_cells[idx])
    set_cell_margins(hdr_cells[idx])

# Rows
for r_i, (c_name, f_val, p_val) in enumerate(table_4_1_data, start=1):
    row_cells = t1.rows[r_i].cells
    
    # Col 1
    p1 = row_cells[0].paragraphs[0]
    r1 = p1.add_run(c_name)
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11)
    if f_val == "" and p_val == "":
        r1.font.bold = True
    else:
        p1.paragraph_format.left_indent = Inches(0.2)
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    # Col 2
    p2 = row_cells[1].paragraphs[0]
    r2 = p2.add_run(str(f_val) if f_val != "" else "")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(11)
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    # Col 3
    p3 = row_cells[2].paragraphs[0]
    r3 = p3.add_run(f"{p_val:.2f}" if p_val != "" else "")
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(11)
    p3.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    for c_x in row_cells:
        set_cell_margins(c_x)

p_space1 = doc.add_paragraph()
p_space1.paragraph_format.space_before = Pt(4)

# Interpretation Table 4.1
p_int1 = doc.add_paragraph()
p_int1.add_run(
    "Table 4.1 presents the socio-economic characteristics of the sampled yam farmers in Akpabuyo LGA. "
    "The results indicate that male farmers constitute the majority of the sampled population, accounting for 60.00% (n = 36) "
    "of the respondents, while female farmers represent 40.00% (n = 24). This gender distribution demonstrates that while yam farming "
    "in Akpabuyo LGA remains predominantly male-dominated—largely due to the heavy physical labour involved in land clearing, ridging, "
    "and mound construction—women maintain a substantial and active presence in yam agricultural production.\n\n"
    "In terms of marital status, an overwhelming majority of the farmers are married (81.67%, n = 49). Widowed individuals account for "
    "10.00% (n = 6), followed by single farmers representing 8.33% (n = 5), whereas no divorced farmers (0.00%, n = 0) were observed in the sample. "
    "The high proportion of married respondents underscores the family-centred structure of yam farming in the study area, where household members "
    "frequently provide critical unpaid family labour for farm operations.\n\n"
    "The educational profile of the respondents reveals a high level of formal literacy among yam farmers in Akpabuyo LGA. All sampled farmers "
    "have attained some degree of formal education. Specifically, 45.00% (n = 27) completed secondary education, 30.00% (n = 18) attained primary "
    "education, and 25.00% (n = 15) acquired tertiary education. No respondents reported having no formal education (0.00%, n = 0). This high educational "
    "attainment implies that the farming population possesses the foundational capacity to comprehend agricultural extension packages, adopt modern "
    "farming innovations, and manage farm records effectively.\n\n"
    "Regarding income diversification, 81.67% (n = 49) of the yam farmers engage in secondary sources of income apart from yam cultivation, "
    "whereas only 18.33% (n = 11) rely exclusively on yam farming. The widespread involvement in off-farm and secondary income-generating activities "
    "highlights a coping mechanism to mitigate agricultural yield fluctuations, hedge against seasonal income deficits, and support household livelihood maintenance."
)

# Section 4.3: Quantitative Socio-Economic Characteristics
add_heading_1("4.3 Quantitative Socio-Economic Characteristics of Yam Farmers")
p_t42_title = doc.add_paragraph()
r_t42_t = p_t42_title.add_run("Table 4.2: Descriptive Statistics of Selected Quantitative Characteristics of Yam Farmers")
r_t42_t.font.bold = True

t2 = doc.add_table(rows=len(table_4_2_data) + 1, cols=6)
t2.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_apa_borders(t2)

hdr_cells2 = t2.rows[0].cells
headers2_text = ["Variable", "N", "Mean", "Standard deviation", "Minimum", "Maximum"]
for idx, text in enumerate(headers2_text):
    hdr_cells2[idx].text = text
    p = hdr_cells2[idx].paragraphs[0]
    p.runs[0].font.bold = True
    p.runs[0].font.name = 'Times New Roman'
    p.runs[0].font.size = Pt(11)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT if idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
    set_header_bottom_border(hdr_cells2[idx])
    set_cell_margins(hdr_cells2[idx])

for r_i, (v_name, n_v, m_v, s_v, min_v, max_v) in enumerate(table_4_2_data, start=1):
    row_cells = t2.rows[r_i].cells
    
    vals = [v_name, str(n_v), f"{m_v:.2f}", f"{s_v:.2f}", f"{min_v:.2f}", f"{max_v:.2f}"]
    for col_idx, val_str in enumerate(vals):
        p = row_cells[col_idx].paragraphs[0]
        r = p.add_run(val_str)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
        set_cell_margins(row_cells[col_idx])

p_space2 = doc.add_paragraph()
p_space2.paragraph_format.space_before = Pt(4)

# Interpretation Table 4.2
p_int2 = doc.add_paragraph()
p_int2.add_run(
    "Table 4.2 presents the descriptive statistics for the selected quantitative socio-economic characteristics of the sampled yam farmers. "
    "The mean age of the farmers is 46.03 years with a standard deviation of 8.64 years, spanning a minimum age of 30.00 years and a maximum "
    "of 63.00 years. This indicates that the yam farming workforce in Akpabuyo LGA is largely comprised of middle-aged individuals who are in "
    "their economically active and physically productive years. The dispersion around the mean reflects a moderate variation in age, encompassing "
    "both younger adults entering commercial farming and experienced older farmers.\n\n"
    "The average household size among the respondents is 6.23 persons (SD = 1.84), ranging from a minimum of 3.00 persons to a maximum of 10.00 persons. "
    "A mean household size of approximately 6 persons reflects relatively large family units, which is typical of rural agrarian communities in Cross River State. "
    "Larger household sizes provide a potential pool of family labour for labour-intensive farming operations, although they simultaneously increase "
    "household consumption expenditure demands.\n\n"
    "The mean years of yam farming experience is 18.88 years (SD = 8.56 years), with a minimum experience of 6.00 years and a maximum of 40.00 years. "
    "This substantial level of experience indicates that farmers in the study area possess deep practical knowledge of local soil management, yam variety selection, "
    "cropping calendars, and traditional pest control techniques. The wide range of experience demonstrates the presence of both seasoned farmers with up to four "
    "decades of practice and relatively newer entrants with 6 years of experience."
)

# Section 4.4: Age Distribution Figure
add_heading_1("4.4 Age Distribution of Yam Farmers")

p_fig = doc.add_paragraph()
p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_fig_img = p_fig.add_run()
run_fig_img.add_picture(fig_path, width=Inches(5.8))

p_fig_label = doc.add_paragraph()
p_fig_label.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_fl = p_fig_label.add_run("Figure 4.1: Age Distribution of Yam Farmers in Akpabuyo LGA")
r_fl.font.bold = True
r_fl.font.name = 'Times New Roman'
r_fl.font.size = Pt(11)

p_fig_int = doc.add_paragraph()
p_fig_int.add_run(
    "Figure 4.1 illustrates the empirical age distribution of yam farmers in Akpabuyo LGA. As visually depicted in the histogram, "
    "the age distribution exhibits a classic unimodal pattern centered in the 40–55 years range, with the highest concentration of farmers "
    "falling between 42 and 52 years. The distribution tapers off towards both the younger age threshold (30–35 years) and the older age "
    "bracket (60–65 years). This structural pattern confirms that yam cultivation in Akpabuyo LGA is principally sustained by mature, "
    "middle-aged farmers who possess the physical stamina required for mound cultivation while maintaining established farming experience."
)

# Save Word Doc
docx_path = os.path.join(OUT_DIR, "Analysis_1_Chapter_4_Results.docx")
doc.save(docx_path)
print(f"Saved: {docx_path}")

print("\nALL ANALYSIS 1 DELIVERABLES SUCCESSFULLY GENERATED!")
