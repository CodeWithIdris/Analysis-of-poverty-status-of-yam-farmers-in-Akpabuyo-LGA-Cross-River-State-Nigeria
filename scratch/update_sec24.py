with open('scratch/build_final_thesis_doc.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_sec24 = '''    add_heading_styled(doc, "2.4 Conceptual Framework", level=2)
    add_body_p(doc, "The conceptual framework of this study, illustrated in Figure 2.1, synthesizes the structural relationships connecting household socioeconomic characteristics (age, sex, marital status, education, household size, farming experience, secondary income), farm asset endowments (total farm size, yam cultivated area, modern tools, improved varieties, fertilizer use), and institutional factors (access to agricultural credit, agricultural extension contact, cooperative membership) to household welfare measures (monthly household expenditure, per-capita monthly household expenditure, and expenditure allocation), poverty status outcomes (relative poverty line, poor/non-poor classification, headcount P₀, poverty gap P₁, and poverty severity P₂), and production/institutional constraints (Objective IV) in Akpabuyo Local Government Area.")
    add_image_with_caption(doc, "scratch/Figure_2_1_Conceptual_Framework_Final.png", "Figure 2.1: Conceptual Framework Showing the Relationship between Socio-Economic, Farm-Related and Institutional Factors and Poverty Status")'''

new_sec24 = '''    add_heading_styled(doc, "2.4 Conceptual Framework", level=2)
    add_body_p(doc, "The conceptual framework of this study, depicted in Figure 2.1, illustrates the structural and conceptual relationships among smallholder farming characteristics, household welfare measures, and poverty status outcomes in Akpabuyo Local Government Area. The framework conceptualizes the household economy as an integrated system structured into distinct analytical components:")
    add_body_p(doc, "1. Socio-Economic Characteristics: Comprising demographic and human capital endowments such as farmer age, sex, marital status, educational attainment, household size, farming experience, and secondary income engagement, which influence labour supply, decision-making, and resource allocation.")
    add_body_p(doc, "2. Farm Asset and Production Factors: Encompassing physical and natural capital assets including total farm size (ha), yam cultivated area (ha), modern farm tools ownership, use of improved yam varieties, and application of chemical fertilizers or organic manure.")
    add_body_p(doc, "3. Institutional Support Factors: Encompassing access to formal and informal agricultural credit, agricultural extension contact, and active membership in agricultural cooperative societies, which provide financial liquidity, technical information, and collective bargaining advantages.")
    add_body_p(doc, "4. HOUSEHOLD WELFARE MEASURE: Representing the empirical standard of living of yam-farming households, operationalized through gross monthly household expenditure, expenditure budget allocation across food and non-food necessities, and Per-Capita Monthly Household Expenditure (PCHE).")
    add_body_p(doc, "5. POVERTY STATUS: Constituting the terminal welfare outcome of the study, determined through the relative poverty line (z = two-thirds mean PCHE) and evaluated via Foster-Greer-Thorbecke (FGT) indices (poverty incidence P₀, poverty depth P₁, and poverty severity P₂) and poor/non-poor binary classification.")
    add_body_p(doc, "6. Challenges Faced by Yam Farmers: Representing exogenous and systemic constraints (labour scarcity, escalating input prices, storage losses, climate variability, credit constraints, extension gaps, and pest/disease infestations) that restrict productivity and welfare attainment (Objective IV).")
    add_body_p(doc, "Methodological and Conceptual Note on Connectors: In strict accordance with the cross-sectional observational design of this research, all connecting lines between framework constructs denote logical conceptual associations and empirical relationships rather than verified causal mediation pathways. Objective II provides a descriptive comparative profile across poverty groups, Objective III evaluates statistical associations using bivariate inferential tests and multivariable logistic regression, and Objective IV evaluates constraint severity using the Mean Severity Index (MSI).")
    add_image_with_caption(doc, "scratch/Figure_2_1_Conceptual_Framework_Final.png", "Figure 2.1: Conceptual Framework Showing the Relationship between Socio-Economic, Farm-Related and Institutional Factors and Poverty Status")'''

if old_sec24 in text:
    text = text.replace(old_sec24, new_sec24)
    with open('scratch/build_final_thesis_doc.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Section 2.4 updated successfully!")
else:
    print("old_sec24 not found!")

