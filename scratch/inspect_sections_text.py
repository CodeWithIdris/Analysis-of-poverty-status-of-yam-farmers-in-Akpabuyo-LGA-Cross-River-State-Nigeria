# -*- coding: utf-8 -*-
import docx, sys
sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document('../chapter 1-5.docx')

print("=== ABSTRACT ===")
for i in range(54, 60):
    print(f"P{i:03d}: {doc.paragraphs[i].text}")

print("\n=== CHAPTER 1 (P078 - P100) ===")
for i in range(78, 100):
    print(f"P{i:03d}: {doc.paragraphs[i].text}")

print("\n=== CHAPTER 3 (P240 - P330) ===")
for i in range(240, 331):
    txt = doc.paragraphs[i].text.strip()
    if txt:
        print(f"P{i:03d}: {txt}")

print("\n=== CHAPTER 5 (P467 - P500) ===")
for i in range(467, 500):
    print(f"P{i:03d}: {doc.paragraphs[i].text}")

