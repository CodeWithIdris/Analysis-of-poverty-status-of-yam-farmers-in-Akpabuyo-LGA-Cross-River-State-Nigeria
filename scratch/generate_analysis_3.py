import os
import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# Define Output Directory
OUT_DIR = os.path.join("Chapter_4_Analysis", "Analysis_3_Poverty_Status")
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load Data & Perform Poverty Calculations
df = pd.read_csv("raw_data.csv")

total_exp = df['TOTAL AVERAGE MONTHLY HOUSEHOLD EXPENDITURE']
hh_size = df['HOUSE HOLD SIZE']

# Per-Capita Monthly Household Expenditure (PCHE)
pche = total_exp / hh_size
df['pche'] = pche

mean_pche = pche.mean()
poverty_line = (2.0 / 3.0) * mean_pche

# Poverty Classification (< Poverty Line = Poor; >= Poverty Line = Non-poor)
df['is_poor'] = df['pche'] < poverty_line

poor_count = int(df['is_poor'].sum())
non_poor_count = int((~df['is_poor']).sum())
n_total = len(df)

poor_pct = (poor_count / n_total) * 100
non_poor_pct = (non_poor_count / n_total) * 100

# FGT Measures
P0 = poor_count / n_total

poor_pche = df[df['is_poor']]['pche']
gaps = (poverty_line - poor_pche) / poverty_line

P1 = gaps.sum() / n_total
P2 = (gaps ** 2).sum() / n_total
mean_norm_gap_poor = gaps.mean()

# ---------------------------------------------------------
# GENERATE EXCEL FILE 1: Table 4.6
# ---------------------------------------------------------
wb6 = openpyxl.Workbook()
ws6 = wb6.active
ws6.title = "Table 4.6"

ws6.cell(row=1, column=1, value="Table 4.6: Determination of the Relative Poverty Line among Yam-Farming Households").font = Font(name="Calibri", size=12, bold=True)
ws6.merge_cells("A1:B1")

headers6 = ["Measure", "Value"]
ws6.append([])
ws6.append(headers6)

header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
thin_border_side = Side(border_style="thin", color="D9D9D9")
thin_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

for col_num in range(1, 3):
    cell = ws6.cell(row=3, column=col_num)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="left" if col_num == 1 else "right", vertical="center")

table_4_6_rows = [
    ("Total number of households", n_total, "#,##0"),
    ("Total monthly household expenditure (₦)", total_exp.sum(), "#,##0.00"),
    ("Mean per-capita monthly household expenditure (₦/person/month)", mean_pche, "#,##0.00"),
    ("2/3 of mean per-capita monthly expenditure — Poverty Line (₦/person/month)", poverty_line, "#,##0.00")
]

for row_idx, (m_label, m_val, m_fmt) in enumerate(table_4_6_rows, start=4):
    c1 = ws6.cell(row=row_idx, column=1, value=m_label)
    c2 = ws6.cell(row=row_idx, column=2, value=m_val)
    
    c1.font = Font(name="Calibri", size=11, bold=(row_idx == 7))
    c2.font = Font(name="Calibri", size=11, bold=(row_idx == 7))
    c2.number_format = m_fmt
    c2.alignment = Alignment(horizontal="right")
    
    c1.border = thin_border
    c2.border = thin_border

ws6.column_dimensions['A'].width = 72
ws6.column_dimensions['B'].width = 22

excel6_path = os.path.join(OUT_DIR, "Table_4_6_Poverty_Line_Determination.xlsx")
wb6.save(excel6_path)
print(f"Saved: {excel6_path}")


# ---------------------------------------------------------
# GENERATE EXCEL FILE 2: Table 4.7
# ---------------------------------------------------------
wb7 = openpyxl.Workbook()
ws7 = wb7.active
ws7.title = "Table 4.7"

ws7.cell(row=1, column=1, value="Table 4.7: Poverty Status of Yam-Farming Households in Akpabuyo LGA").font = Font(name="Calibri", size=12, bold=True)
ws7.merge_cells("A1:C1")

headers7 = ["Poverty status", "Frequency (n)", "Percentage (%)"]
ws7.append([])
ws7.append(headers7)

for col_num in range(1, 4):
    cell = ws7.cell(row=3, column=col_num)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="left" if col_num == 1 else "right", vertical="center")

table_4_7_rows = [
    ("Poor", poor_count, poor_pct),
    ("Non-poor", non_poor_count, non_poor_pct),
    ("Total", n_total, 100.00)
]

for row_idx, (p_status, p_freq, p_pct) in enumerate(table_4_7_rows, start=4):
    c1 = ws7.cell(row=row_idx, column=1, value=p_status)
    c2 = ws7.cell(row=row_idx, column=2, value=p_freq)
    c3 = ws7.cell(row=row_idx, column=3, value=p_pct)
    
    is_total = (row_idx == 6)
    c1.font = Font(name="Calibri", size=11, bold=is_total)
    c2.font = Font(name="Calibri", size=11, bold=is_total)
    c2.number_format = "#,##0"
    c2.alignment = Alignment(horizontal="right")
    
    c3.font = Font(name="Calibri", size=11, bold=is_total)
    c3.number_format = "0.00"
    c3.alignment = Alignment(horizontal="right")
    
    for c in [c1, c2, c3]:
        c.border = thin_border

ws7.column_dimensions['A'].width = 25
ws7.column_dimensions['B'].width = 16
ws7.column_dimensions['C'].width = 18

excel7_path = os.path.join(OUT_DIR, "Table_4_7_Poverty_Status_Distribution.xlsx")
wb7.save(excel7_path)
print(f"Saved: {excel7_path}")


# ---------------------------------------------------------
# GENERATE EXCEL FILE 3: Table 4.8
# ---------------------------------------------------------
wb8 = openpyxl.Workbook()
ws8 = wb8.active
ws8.title = "Table 4.8"

ws8.cell(row=1, column=1, value="Table 4.8: Foster–Greer–Thorbecke Poverty Indices among Yam-Farming Households").font = Font(name="Calibri", size=12, bold=True)
ws8.merge_cells("A1:D1")

headers8 = ["Poverty measure", "FGT parameter (α)", "Index", "Percentage (%)"]
ws8.append([])
ws8.append(headers8)

for col_num in range(1, 5):
    cell = ws8.cell(row=3, column=col_num)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="left" if col_num in [1, 2] else "right", vertical="center")

table_4_8_rows = [
    ("Poverty incidence/headcount (P0)", 0, P0, P0 * 100),
    ("Poverty depth/gap (P1)", 1, P1, P1 * 100),
    ("Poverty severity (P2)", 2, P2, P2 * 100)
]

for row_idx, (fgt_name, fgt_param, fgt_idx, fgt_pct) in enumerate(table_4_8_rows, start=4):
    c1 = ws8.cell(row=row_idx, column=1, value=fgt_name)
    c2 = ws8.cell(row=row_idx, column=2, value=fgt_param)
    c3 = ws8.cell(row=row_idx, column=3, value=fgt_idx)
    c4 = ws8.cell(row=row_idx, column=4, value=fgt_pct)
    
    c1.font = Font(name="Calibri", size=11)
    c2.font = Font(name="Calibri", size=11)
    c2.alignment = Alignment(horizontal="center")
    
    c3.font = Font(name="Calibri", size=11)
    c3.number_format = "0.0000"
    c3.alignment = Alignment(horizontal="right")
    
    c4.font = Font(name="Calibri", size=11)
    c4.number_format = "0.00"
    c4.alignment = Alignment(horizontal="right")
    
    for c in [c1, c2, c3, c4]:
        c.border = thin_border

ws8.column_dimensions['A'].width = 38
ws8.column_dimensions['B'].width = 20
ws8.column_dimensions['C'].width = 16
ws8.column_dimensions['D'].width = 18

excel8_path = os.path.join(OUT_DIR, "Table_4_8_FGT_Poverty_Indices.xlsx")
wb8.save(excel8_path)
print(f"Saved: {excel8_path}")


# ---------------------------------------------------------
# GENERATE FIGURE 4.3: Horizontal Bar Chart
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=300)

categories = ['Non-poor', 'Poor']
counts = [non_poor_count, poor_count]
pcts = [non_poor_pct, poor_pct]
y_positions = np.arange(len(categories))
palette = ['#1B365D', '#C05621'] # Coordinated academic palette

bars = ax.barh(
    y_positions,
    counts,
    height=0.48,
    color=palette,
    edgecolor='none',
    zorder=3
)

ax.invert_yaxis()

for bar, count, pct, color in zip(bars, counts, pcts, palette):
    ax.text(
        count + 0.8,
        bar.get_y() + bar.get_height() / 2,
        f'n = {count} ({pct:.2f}%)',
        va='center',
        ha='left',
        fontsize=10,
        fontweight='semibold',
        color='#222222'
    )

# Plain white background
ax.set_facecolor('white')
fig.patch.set_facecolor('white')

# Category Labels
ax.set_yticks(y_positions)
ax.set_yticklabels(categories, fontsize=10.5, fontweight='normal', color='#1A1A1A')

# X-axis
ax.set_xlabel('Number of Households (n)', fontsize=11, fontweight='bold', labelpad=10, color='#1A1A1A')
ax.set_xlim(0, max(counts) + 12)

# Spines & Ticks
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#333333')
ax.spines['left'].set_linewidth(1.1)
ax.spines['bottom'].set_color('#333333')
ax.spines['bottom'].set_linewidth(1.1)

ax.tick_params(axis='y', which='both', length=0)
ax.tick_params(axis='x', labelsize=9.5, colors='#1A1A1A', length=3.5, width=1.0)

ax.grid(False)

plt.tight_layout()

fig_path = os.path.join(OUT_DIR, "Figure_4_3_Poverty_Status.png")
fig_path_brain = r"C:\Users\idrid\.gemini\antigravity\brain\27a3372d-d772-494e-881c-bafd3ccdf2ee\Figure_4_3_Poverty_Status.png"
fig_path_root = "Figure_4_3_Poverty_Status.png"

plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.savefig(fig_path_brain, dpi=300, bbox_inches='tight')
plt.savefig(fig_path_root, dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: {fig_path}")


# ---------------------------------------------------------
# GENERATE WORD DOCUMENT: Analysis_3_Chapter_4_Results.docx
# ---------------------------------------------------------
doc = Document()

for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

normal_style = doc.styles['Normal']
normal_style.font.name = 'Times New Roman'
normal_style.font.size = Pt(12)
normal_style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
normal_style.paragraph_format.line_spacing = 1.5
normal_style.paragraph_format.space_after = Pt(6)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x78)
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

# --- TITLE ---
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_title = p_title.add_run("CHAPTER FOUR (CONTINUED)\nPOVERTY STATUS OF YAM FARMERS")
r_title.font.name = 'Times New Roman'
r_title.font.size = Pt(16)
r_title.font.bold = True

# Section 4.9: Poverty Line Determination
add_heading_1("4.10 Determination of the Relative Poverty Line")
p_t46_title = doc.add_paragraph()
r_t46_t = p_t46_title.add_run("Table 4.6: Determination of the Relative Poverty Line among Yam-Farming Households")
r_t46_t.font.bold = True

t6 = doc.add_table(rows=len(table_4_6_rows) + 1, cols=2)
t6.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_apa_borders(t6)

hdr_cells6 = t6.rows[0].cells
headers6_text = ["Measure", "Value"]
for idx, text in enumerate(headers6_text):
    hdr_cells6[idx].text = text
    p = hdr_cells6[idx].paragraphs[0]
    p.runs[0].font.bold = True
    p.runs[0].font.name = 'Times New Roman'
    p.runs[0].font.size = Pt(11)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT if idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
    set_header_bottom_border(hdr_cells6[idx])
    set_cell_margins(hdr_cells6[idx])

for r_i, (m_l, m_v, m_f) in enumerate(table_4_6_rows, start=1):
    row_cells = t6.rows[r_i].cells
    v_str = f"{m_v:,.2f}" if m_f == "#,##0.00" else f"{int(m_v):,}"
    
    p1 = row_cells[0].paragraphs[0]
    r1 = p1.add_run(m_l)
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11)
    if r_i == len(table_4_6_rows):
        r1.font.bold = True
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    p2 = row_cells[1].paragraphs[0]
    r2 = p2.add_run(v_str)
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(11)
    if r_i == len(table_4_6_rows):
        r2.font.bold = True
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    set_cell_margins(row_cells[0])
    set_cell_margins(row_cells[1])

doc.add_paragraph().paragraph_format.space_before = Pt(4)

p_int6 = doc.add_paragraph()
p_int6.add_run(
    f"Table 4.6 presents the determination of the relative poverty line for the sampled yam-farming households in Akpabuyo LGA (N = {n_total}). "
    f"The total monthly expenditure across all sampled households amounted to ₦{total_exp.sum():,.2f}. Dividing total household expenditure by household size "
    f"yields a mean per-capita monthly household expenditure (PCHE) of ₦{mean_pche:,.2f} per person per month.\n\n"
    f"In accordance with established relative poverty measurement methodology, the relative poverty line (Z) was constructed as two-thirds (2/3) of the mean per-capita "
    f"monthly household expenditure. This established a relative poverty threshold of ₦{poverty_line:,.2f} per person per month. This relative poverty line represents "
    f"the minimum monthly expenditure required for an individual in a yam-farming household to attain a baseline level of consumption relative to the average living standards of the sampled community."
)

# Section 4.10: Poverty Status Distribution
add_heading_1("4.11 Poverty Status Distribution of Yam Farmers")
p_t47_title = doc.add_paragraph()
r_t47_t = p_t47_title.add_run("Table 4.7: Poverty Status of Yam-Farming Households in Akpabuyo LGA")
r_t47_t.font.bold = True

t7 = doc.add_table(rows=len(table_4_7_rows) + 1, cols=3)
t7.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_apa_borders(t7)

hdr_cells7 = t7.rows[0].cells
headers7_text = ["Poverty status", "Frequency (n)", "Percentage (%)"]
for idx, text in enumerate(headers7_text):
    hdr_cells7[idx].text = text
    p = hdr_cells7[idx].paragraphs[0]
    p.runs[0].font.bold = True
    p.runs[0].font.name = 'Times New Roman'
    p.runs[0].font.size = Pt(11)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT if idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
    set_header_bottom_border(hdr_cells7[idx])
    set_cell_margins(hdr_cells7[idx])

for r_i, (ps_name, ps_f, ps_p) in enumerate(table_4_7_rows, start=1):
    row_cells = t7.rows[r_i].cells
    vals = [ps_name, str(ps_f), f"{ps_p:.2f}"]
    for col_idx, val_str in enumerate(vals):
        p = row_cells[col_idx].paragraphs[0]
        r = p.add_run(val_str)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        if r_i == len(table_4_7_rows):
            r.font.bold = True
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
        set_cell_margins(row_cells[col_idx])

doc.add_paragraph().paragraph_format.space_before = Pt(4)

p_int7 = doc.add_paragraph()
p_int7.add_run(
    f"Table 4.7 presents the distribution of yam-farming households according to their poverty status based on the calculated relative poverty line of ₦{poverty_line:,.2f} per person per month. "
    f"Households with per-capita monthly expenditure strictly below the poverty line (PCHE < ₦{poverty_line:,.2f}) were classified as poor, while households with per-capita monthly expenditure "
    f"at or above the threshold (PCHE ≥ ₦{poverty_line:,.2f}) were classified as non-poor.\n\n"
    f"The empirical results indicate that out of the {n_total} sampled yam-farming households, {poor_count} households are classified as poor, representing a poverty incidence of {poor_pct:.2f}%. "
    f"Conversely, {non_poor_count} households are classified as non-poor, constituting {non_poor_pct:.2f}% of the sampled population. These findings demonstrate that approximately one-fifth of the yam-farming households "
    f"in Akpabuyo LGA live below the community relative poverty threshold, while the remaining four-fifths maintain monthly per-capita expenditure above the relative poverty line."
)

# Section 4.11: FGT Poverty Indices
add_heading_1("4.12 Foster–Greer–Thorbecke (FGT) Poverty Indices")
p_t48_title = doc.add_paragraph()
r_t48_t = p_t48_title.add_run("Table 4.8: Foster–Greer–Thorbecke Poverty Indices among Yam-Farming Households")
r_t48_t.font.bold = True

t8 = doc.add_table(rows=len(table_4_8_rows) + 1, cols=4)
t8.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_apa_borders(t8)

hdr_cells8 = t8.rows[0].cells
headers8_text = ["Poverty measure", "FGT parameter (α)", "Index", "Percentage (%)"]
for idx, text in enumerate(headers8_text):
    hdr_cells8[idx].text = text
    p = hdr_cells8[idx].paragraphs[0]
    p.runs[0].font.bold = True
    p.runs[0].font.name = 'Times New Roman'
    p.runs[0].font.size = Pt(11)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT if idx in [0, 1] else WD_ALIGN_PARAGRAPH.RIGHT
    set_header_bottom_border(hdr_cells8[idx])
    set_cell_margins(hdr_cells8[idx])

for r_i, (f_name, f_par, f_idx, f_pct) in enumerate(table_4_8_rows, start=1):
    row_cells = t8.rows[r_i].cells
    vals = [f_name, str(f_par), f"{f_idx:.4f}", f"{f_pct:.2f}"]
    for col_idx, val_str in enumerate(vals):
        p = row_cells[col_idx].paragraphs[0]
        r = p.add_run(val_str)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else (WD_ALIGN_PARAGRAPH.CENTER if col_idx == 1 else WD_ALIGN_PARAGRAPH.RIGHT)
        set_cell_margins(row_cells[col_idx])

doc.add_paragraph().paragraph_format.space_before = Pt(4)

p_int8 = doc.add_paragraph()
p_int8.add_run(
    f"Table 4.8 presents the Foster–Greer–Thorbecke (FGT) poverty indices computed across the sampled yam-farming households in Akpabuyo LGA. "
    f"The FGT class of poverty measures provides quantitative estimates of poverty incidence (P0), poverty depth (P1), and poverty severity (P2).\n\n"
    f"The poverty incidence or headcount ratio (P0, α = 0) is {P0:.4f} ({P0*100:.2f}%), confirming that {poor_pct:.2f}% of the sampled households fall below the relative poverty line of ₦{poverty_line:,.2f}.\n\n"
    f"The poverty depth or gap index (P1, α = 1) is {P1:.4f} ({P1*100:.2f}%). The poverty gap index measures the average shortfall of per-capita expenditure from the poverty line "
    f"expressed as a proportion of the poverty line across the entire sample. A P1 index of {P1:.4f} indicates that, on average, a financial transfer equivalent to {P1*100:.2f}% of the poverty line "
    f"(or approximately ₦{P1 * poverty_line:,.2f} per person per month) across all sampled households would be required to bring all poor households exactly up to the poverty threshold, under perfect targeting.\n\n"
    f"Among poor households specifically, the mean normalized poverty gap is {mean_norm_gap_poor:.4f} ({mean_norm_gap_poor*100:.2f}%). This supplementary descriptive measure reveals that households classified as poor "
    f"incur an average expenditure shortfall of {mean_norm_gap_poor*100:.2f}% relative to the poverty line threshold.\n\n"
    f"The poverty severity index (P2, α = 2) is {P2:.4f} ({P2*100:.2f}%). By squaring the normalized poverty gaps, the P2 index places greater weight on households that experience severe expenditure shortfalls below the poverty line. "
    f"A P2 index of {P2:.4f} reflects a relatively low level of extreme inequality among the poor population in the study area."
)

# Section 4.12: Graphical Representation
add_heading_1("4.13 Graphical Representation of Poverty Status")

p_fig3 = doc.add_paragraph()
p_fig3.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_fig3_img = p_fig3.add_run()
run_fig3_img.add_picture(fig_path, width=Inches(5.8))

p_fig3_label = doc.add_paragraph()
p_fig3_label.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_f3l = p_fig3_label.add_run("Figure 4.3: Poverty Status of Yam-Farming Households in Akpabuyo LGA")
r_f3l.font.bold = True
r_f3l.font.name = 'Times New Roman'
r_f3l.font.size = Pt(11)

p_fig3_int = doc.add_paragraph()
p_fig3_int.add_run(
    f"Figure 4.3 visually presents the distribution of sampled yam-farming households between the non-poor and poor status categories. "
    f"The horizontal bar chart highlights the structural distribution within Akpabuyo LGA, showing that non-poor households constitute the majority "
    f"(n = {non_poor_count}, {non_poor_pct:.2f}%), while poor households account for the minority portion (n = {poor_count}, {poor_pct:.2f}%)."
)

# Save Word Doc
docx_path = os.path.join(OUT_DIR, "Analysis_3_Chapter_4_Results.docx")
doc.save(docx_path)
print(f"Saved: {docx_path}")

print("\nALL ANALYSIS 3 DELIVERABLES SUCCESSFULLY GENERATED!")
