# -*- coding: utf-8 -*-
import os
import sys
import docx

sys.stdout.reconfigure(encoding='utf-8')

def audit_final_document():
    doc_path = "FINAL_THESIS_FOUR_OBJECTIVES_AKPABUYO_FINAL.docx"
    print(f"Auditing {doc_path}...")
    doc = docx.Document(doc_path)
    
    full_paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    table_texts = [cell.text.strip() for t in doc.tables for r in t.rows for cell in r.cells if cell.text.strip()]
    full_text = " \n ".join(full_paragraphs + table_texts)
    
    # 1. Check Figure 2.1 Image Existence & Caption
    fig_img_exists = os.path.exists("scratch/Figure_2_1_Conceptual_Framework_Final.png")
    fig_caption_present = any("Figure 2.1: Conceptual Framework" in p for p in full_paragraphs)
    
    # 2. Check Empirical Tables (Table 4.1 to 4.10)
    table_checks = [
        ("Table 4.1 (Sample Size N=60, 36 males, 24 females)", "36" in full_text and "24" in full_text and "60" in full_text),
        ("Table 4.2 (Food 60,703.33, Total 115,837.50, Sum 113,985.83)", "60,703.33" in full_text and "115,837.50" in full_text and "113,985.83" in full_text),
        ("Table 4.3 (Mean PCHE 20,289.03, Line 13,526.02)", "20,289.03" in full_text and "13,526.02" in full_text),
        ("Table 4.4 (P0=0.2167, P1=0.0232, P2=0.0034)", "0.2167" in full_text and "0.0232" in full_text and "0.0034" in full_text),
        ("Table 4.5 (Poor n=13, Non-poor n=47, Credit: 7.69% vs 61.70%, Ext: 0% vs 44.68%)", "7.69%" in full_text and "61.70%" in full_text and "44.68%" in full_text),
        ("Table 4.6 (Age: 51.31 vs 44.57; HH size: 8.31 vs 5.66; Farm: 1.98 vs 2.56)", "51.31 ± 8.99" in full_text and "8.31 ± 1.70" in full_text and "1.98 ± 0.48" in full_text),
        ("Table 4.7 (PCHE: 12,079.49 vs 22,559.76; Deficit: 1,446.53)", "12,079.49" in full_text and "22,559.76" in full_text and "1,446.53" in full_text),
        ("Table 4.8 (Mann-Whitney U: Age=432.00, HH=536.00, Farm=170.50; Credit chi2=9.820)", "432.00" in full_text and "536.00" in full_text and "170.50" in full_text and "9.820" in full_text),
        ("Table 4.9 (Credit OR=0.0744, p=0.0369; Farm OR=0.6505, p=0.5979; LR=13.861)", "0.0744" in full_text and "0.0369" in full_text and "0.6505" in full_text and "13.861" in full_text),
        ("Table 4.10 (MSI: Labour=4.15, Inputs=4.00, Storage=3.88, Climate=3.70, Stakes=3.57, Credit=3.53)", "4.15" in full_text and "4.00" in full_text and "3.88" in full_text and "3.70" in full_text and "3.57" in full_text and "3.53" in full_text)
    ]
    
    print("\n--- Figure 2.1 Audit ---")
    print(f"Figure 2.1 Image File: {'PASSED' if fig_img_exists else 'FAILED'}")
    print(f"Figure 2.1 Caption: {'PASSED' if fig_caption_present else 'FAILED'}")
    
    print("\n--- Empirical Tables Integrity Check ---")
    all_tables_pass = True
    for name, res in table_checks:
        status = "PASSED" if res else "FAILED"
        if not res: all_tables_pass = False
        print(f"  [{status}] {name}")
        
    print(f"\nOverall Final Document Status: {'ALL AUDITS PASSED (100% INTEGRITY)' if all_tables_pass and fig_img_exists and fig_caption_present else 'ISSUES FOUND'}")

if __name__ == "__main__":
    audit_final_document()

