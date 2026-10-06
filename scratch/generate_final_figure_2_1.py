# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_conceptual_framework_final():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Box styles - clean academic palette
    box_blue = dict(boxstyle='round,pad=0.6', facecolor='#F0F4F8', edgecolor='#1D4E89', linewidth=1.5)
    box_green = dict(boxstyle='round,pad=0.6', facecolor='#F0F7F4', edgecolor='#2D6A4F', linewidth=1.5)
    box_purple = dict(boxstyle='round,pad=0.6', facecolor='#F8F0FA', edgecolor='#6B2D82', linewidth=1.5)
    box_amber = dict(boxstyle='round,pad=0.6', facecolor='#FFF8E7', edgecolor='#D97706', linewidth=1.5)
    box_red = dict(boxstyle='round,pad=0.6', facecolor='#FFF1F2', edgecolor='#BE123C', linewidth=1.5)
    box_navy = dict(boxstyle='round,pad=0.6', facecolor='#EEF2F6', edgecolor='#0F2942', linewidth=1.8)

    # 1. Socioeconomic Factors (Left Top)
    t1 = "SOCIOECONOMIC FACTORS\n(Objectives II & III)\n• Age of Household Head\n• Sex & Marital Status\n• Educational Attainment\n• Household Size\n• Yam Farming Experience\n• Other Sources of Income"
    ax.text(21, 80, t1, ha='center', va='center', fontsize=8.5, bbox=box_blue, linespacing=1.35)

    # 2. Farm Asset & Production Factors (Left Mid)
    t2 = "FARM ASSET & PRODUCTION FACTORS\n(Objectives II & III)\n• Total Farm Size (ha)\n• Yam Cultivated Area (ha)\n• Improved Yam Varieties\n• Fertilizer / Manure Application\n• Modern Farm Tools"
    ax.text(21, 51, t2, ha='center', va='center', fontsize=8.5, bbox=box_green, linespacing=1.35)

    # 3. Institutional Support Factors (Left Bottom)
    t3 = "INSTITUTIONAL SUPPORT FACTORS\n(Objectives II & III)\n• Access to Agricultural Credit\n• Agricultural Extension Contact\n• Cooperative Society Membership"
    ax.text(21, 22, t3, ha='center', va='center', fontsize=8.5, bbox=box_purple, linespacing=1.35)

    # 4. Household Welfare Measure (Center Top-Mid)
    t4 = "HOUSEHOLD WELFARE MEASURE\n(Objectives I & II)\n• Monthly Household Expenditure\n• Household Expenditure Allocation\n  (Food, Housing, Education, Transport, Health)\n• Per-Capita Monthly Household\n  Expenditure (PCHE)"
    ax.text(58, 67, t4, ha='center', va='center', fontsize=9.0, bbox=box_amber, linespacing=1.4)

    # 5. Production & Institutional Challenges (Center Bottom)
    t5 = "CHALLENGES FACED BY YAM FARMERS\n(Objective IV)\n• High Cost and Scarcity of Farm Labour\n• High Cost of Farm Inputs (Fertilizer, Seeds, Chemicals)\n• Post-Harvest Losses & Inadequate Storage Facilities\n• Unpredictable Rainfall & Climate Variability\n• High Cost / Scarcity of Yam Stakes\n• Inadequate Access to Credit & Extension Deficits\n• Pest & Disease Infestation, Low Prices & Market Access"
    ax.text(58, 23, t5, ha='center', va='center', fontsize=8.0, bbox=box_red, linespacing=1.35)

    # 6. Poverty Status (Right Top-Mid)
    t6 = "POVERTY STATUS\n(Objectives I, II & III)\n• Relative Poverty Line (z)\n• Poor / Non-Poor Classification\n• P₀: Poverty Incidence (Headcount)\n• P₁: Poverty Depth (Poverty Gap)\n• P₂: Poverty Severity (Squared Gap)"
    ax.text(88, 67, t6, ha='center', va='center', fontsize=9.0, bbox=box_navy, linespacing=1.4)

    # Connectors - Conceptual associations appropriate for a cross-sectional study (no causal mediation)
    arrow = dict(arrowstyle='->', lw=1.5, color='#1F2937')
    assoc_line = dict(arrowstyle='-', lw=1.3, color='#4B5563', linestyle='--')
    dashed_link = dict(arrowstyle='->', lw=1.3, color='#991B1B', linestyle=':')

    # Linkages from Factors to Household Welfare Measure
    ax.annotate('', xy=(43, 73), xytext=(35, 80), arrowprops=arrow)
    ax.annotate('', xy=(43, 67), xytext=(36, 51), arrowprops=arrow)
    ax.annotate('', xy=(43, 61), xytext=(35, 27), arrowprops=arrow)

    # Linkage from Welfare Measure to Poverty Status determination
    ax.annotate('', xy=(76, 67), xytext=(73, 67), arrowprops=arrow)

    # Non-directional conceptual association line connecting Factors and Poverty Status (Bivariate / Multivariable Association)
    ax.annotate('', xy=(76, 76), xytext=(35, 87), arrowprops=assoc_line)

    # Challenges contextual associations
    ax.annotate('', xy=(58, 54), xytext=(58, 38), arrowprops=dashed_link)
    ax.annotate('', xy=(36, 42), xytext=(44, 30), arrowprops=dashed_link)

    plt.tight_layout()
    out_img = 'scratch/Figure_2_1_Conceptual_Framework_Final.png'
    plt.savefig(out_img, dpi=300, bbox_inches='tight')
    print(f"Successfully regenerated {out_img} with non-directional conceptual connectors.")

if __name__ == '__main__':
    generate_conceptual_framework_final()
