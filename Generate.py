'''
Simple, error-free pathology reports generator
Creates realistic reports without template complexity
'''

import pandas as pd
import random
from datetime import datetime, timedelta

def create_simple_pathology_reports():
    """Generate simple but realistic pathology reports"""
    
    # Sample realistic reports (complete, no templates)
    pathology_reports = [
        # Breast reports
        "The specimen consists of breast tissue measuring 2.3 cm in greatest dimension. Histologic examination reveals invasive ductal carcinoma, grade II/III, with moderate nuclear pleomorphism and increased mitotic activity (8 mitoses per 10 HPF). The tumor shows minimal lymphocytic infiltrate and focal areas of necrosis. Lymphovascular invasion is present. Perineural invasion is not identified. The surgical margins are clear with the closest margin measuring 0.8 cm. Three of seven lymph nodes contain metastatic carcinoma with extracapsular extension. Immunohistochemistry: ER positive (85%), PR positive (70%), HER2 negative (1+), Ki-67 35%.",
        
        "Sections of breast tissue show ductal carcinoma in situ (DCIS), high grade, involving approximately 60% of the specimen. The DCIS shows cribriform pattern with associated calcifications. No evidence of invasive carcinoma is identified. The basement membrane appears intact with no stromal invasion. Surrounding breast tissue shows fibrocystic changes. Surgical margins are clear of DCIS.",
        
        "The specimen shows benign breast tissue with fibrocystic changes. There is usual ductal hyperplasia of the ductal epithelium with no atypia. Chronic inflammation is noted with minimal fibrosis. No evidence of malignancy is identified. The tissue architecture is preserved. Microcalcifications are present.",
        
        "Histologic examination reveals invasive lobular carcinoma, grade I/III, with mild nuclear pleomorphism and low mitotic activity (3 mitoses per 10 HPF). The tumor shows extensive lymphocytic infiltrate and no necrosis. No lymphovascular invasion identified. No perineural invasion is present. The surgical margins are close with the closest margin measuring 0.2 cm. One of twelve lymph nodes contains metastatic carcinoma without extracapsular extension. Immunohistochemistry: ER positive (95%), PR positive (80%), HER2 negative (0), Ki-67 15%.",
        
        # Lung reports
        "Sections reveal adenocarcinoma with moderate differentiation. The tumor measures 3.8 cm and shows acinar growth pattern. Focal pleural invasion is present. Extensive vascular invasion and minimal lymphatic invasion are noted. The bronchial margin is clear and the vascular margin is clear. Regional lymph nodes (8 examined): 2 show metastatic carcinoma. Immunostains: TTF-1 positive, CK7 positive, p40 negative.",
        
        "The lung biopsy shows chronic bronchitis with severe chronic inflammation. Non-necrotizing granulomatous inflammation is present. No evidence of malignancy is identified. The alveolar architecture shows minimal changes and moderate fibrotic changes. Special stains for organisms are negative.",
        
        "Histologic sections show squamous cell carcinoma, poorly differentiated, measuring 4.2 cm. The tumor demonstrates solid growth pattern with extensive necrosis. Pleural invasion is present. Lymphovascular invasion is identified. The bronchial margin is involved. Regional lymph nodes (12 examined): 5 positive for metastatic carcinoma. Immunostains: p40 positive, CK7 negative, TTF-1 negative.",
        
        # Colon reports
        "Colonic mucosa shows tubulovillous adenoma with high-grade dysplasia. The polyp measures 1.8 cm and extends to within 2 mm of the resection margin. No invasion into the submucosa is present. The background mucosa shows unremarkable changes with minimal inflammation. No lymph nodes examined.",
        
        "Sections of colon show invasive adenocarcinoma, moderately differentiated, arising in association with a tubular adenoma. The carcinoma invades through the muscularis propria and measures 3.5 cm. Focal vessel invasion is present. Margins: proximal 5.2 cm, distal 3.8 cm, radial clear. Regional lymph nodes: 18 examined, 3 with metastatic carcinoma.",
        
        "The colonic biopsy demonstrates tubular adenoma with low-grade dysplasia. The polyp measures 0.8 cm and the resection margin is clear. No submucosal invasion is identified. The background mucosa shows inflammatory changes with moderate inflammation. Two lymph nodes examined, both negative for metastatic carcinoma.",
        
        # Cervical reports
        "Cervical biopsy shows squamous intraepithelial lesion with CIN II. The squamous epithelium demonstrates moderate nuclear changes and minimal cytoplasmic changes. Scattered koilocytic changes are present. The basement membrane is intact with no stromal invasion. Mild inflammation is noted in the underlying stroma.",
        
        "Endocervical curettage shows benign endocervical glands with reactive glandular changes. Minimal glandular atypia is present. No evidence of invasive adenocarcinoma is identified. The endocervical glands show normal architecture.",
        
        "Cervical cone biopsy reveals cervical intraepithelial neoplasia, CIN III, involving the transformation zone. The squamous epithelium shows severe nuclear changes and moderate cytoplasmic changes. Numerous koilocytic changes are present. The basement membrane is focally disrupted with focal stromal invasion. Moderate inflammation is noted in the underlying stroma.",
        
        # Additional complex cases
        "The specimen shows infiltrating squamous cell carcinoma extending beyond the basement membrane. Tumor cells form irregular nests and sheets with marked nuclear pleomorphism. Perineural invasion is noted. Lymphovascular spread is not identified. The tumor demonstrates poor differentiation with extensive necrosis. Mitotic activity is high with 18 mitoses per 10 HPF.",
        
        "Sections reveal moderate nuclear atypia and occasional mitotic figures. No malignancy or carcinoma is detected. Architecture remains preserved with minimal inflammatory changes. Low-grade dysplasia cannot be excluded. The tissue shows regenerative changes with focal hyperplasia.",
        
        "Severe pleomorphism and marked nuclear enlargement are evident. Numerous mitotic figures are seen (22 mitoses per 10 HPF). Tissue shows loss of normal architecture with extensive cellular crowding. Stromal invasion is suspected but not confirmed. Atypical mitoses are present.",
        
        "Histologic sections show benign fibrous tissue with scattered areas of chronic inflammation. However, mitotic activity is elevated (12 mitoses per 10 HPF). There is no evidence of cellular atypia or necrosis. Grade I pattern observed with well-preserved tissue architecture.",
        
        "The biopsy demonstrates epithelial hyperplasia with areas of atypical hyperplasia. No definite carcinoma is identified. Basement membrane remains intact with no evidence of invasion. Few mitotic figures are seen (4 mitoses per 10 HPF). The surrounding tissue shows reactive changes.",
        
        "Pathologic examination reveals high-grade serous carcinoma involving the ovarian surface. The tumor shows extensive papillary architecture with prominent nucleoli and high mitotic rate. Lymphovascular invasion is present. No capsular invasion is identified. The fallopian tube shows unremarkable changes.",
        
        "Prostate needle biopsy shows adenocarcinoma, Gleason score 7 (3+4), involving approximately 40% of the core length. The tumor demonstrates moderate nuclear pleomorphism with prominent nucleoli. Perineural invasion is present. No lymphovascular invasion is identified.",
        
        "Skin excision shows malignant melanoma, superficial spreading type, with a Breslow depth of 1.2 mm. The tumor demonstrates moderate pleomorphism with mitotic activity of 3 mitoses per mm². No ulceration is present. The deep and peripheral margins are clear of melanoma."
    ]
    
    # Patient demographics
    first_names = ['Sarah', 'Maria', 'Jennifer', 'Lisa', 'Michelle', 'David', 'Michael', 'John', 'James', 'Robert']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    # Specimen types matching the reports
    specimen_types = [
        'Breast biopsy', 'Breast biopsy', 'Breast biopsy', 'Breast lumpectomy',  # 4 breast
        'Lung biopsy', 'Lung biopsy', 'Lung resection',  # 3 lung
        'Colonic polyp', 'Colon resection', 'Colonic polyp',  # 3 colon
        'Cervical biopsy', 'Cervical curettage', 'Cervical cone biopsy',  # 3 cervical
        'Tissue biopsy', 'Tissue biopsy', 'Tissue biopsy', 'Tissue biopsy', 'Tissue biopsy',  # 5 general
        'Ovarian biopsy', 'Prostate biopsy', 'Skin excision'  # 3 other
    ]
    
    # Diagnosis categories matching the reports
    diagnosis_categories = [
        'Malignant', 'Pre-malignant', 'Benign', 'Malignant',  # breast
        'Malignant', 'Benign', 'Malignant',  # lung
        'Pre-malignant', 'Malignant', 'Pre-malignant',  # colon
        'Pre-malignant', 'Benign', 'Pre-malignant',  # cervical
        'Malignant', 'Pre-malignant', 'Malignant', 'Benign', 'Pre-malignant',  # general
        'Malignant', 'Malignant', 'Malignant'  # other
    ]
    
    reports_data = []
    
    # Generate 100 reports by cycling through the base reports
    for i in range(100):
        # Cycle through available reports
        report_idx = i % len(pathology_reports)
        
        # Patient info
        patient_id = f"PT{str(i+1).zfill(4)}"
        patient_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        age = random.randint(25, 85)
        gender = random.choice(['Female', 'Male'])
        
        # Date info
        report_date = datetime.now() - timedelta(days=random.randint(1, 365))
        
        # Get corresponding specimen type and diagnosis
        specimen_type = specimen_types[report_idx]
        diagnosis_category = diagnosis_categories[report_idx]
        
        # Get the pathology report
        pathology_report = pathology_reports[report_idx]
        
        # Clinical info
        clinical_history = random.choice([
            'Palpable mass noted on physical examination',
            'Abnormal imaging findings',
            'Screening examination',
            'Abnormal laboratory results',
            'Family history of cancer',
            'Follow-up for previous findings',
            'Routine screening',
            'Symptomatic presentation'
        ])
        
        # Pathologist
        pathologists = ['Dr. Smith', 'Dr. Johnson', 'Dr. Williams', 'Dr. Brown', 'Dr. Davis']
        pathologist = random.choice(pathologists)
        
        # Priority
        priority = random.choice(['Routine', 'Urgent', 'STAT'])
        
        reports_data.append({
            'Patient_ID': patient_id,
            'Patient_Name': patient_name,
            'Age': age,
            'Gender': gender,
            'Report_Date': report_date.strftime('%Y-%m-%d'),
            'Specimen_Type': specimen_type,
            'Clinical_History': clinical_history,
            'Pathology_Report': pathology_report,
            'Diagnosis_Category': diagnosis_category,
            'Pathologist': pathologist,
            'Priority': priority,
            'Report_Status': random.choice(['Final', 'Preliminary'])
        })
    
    return pd.DataFrame(reports_data)

def create_pathology_excel():
    """Create Excel file with pathology reports"""
    
    print("Generating realistic pathology reports...")
    df = create_simple_pathology_reports()
    
    # Create Excel file
    filename = 'pathology_reports_dataset.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Main reports sheet
        df.to_excel(writer, sheet_name='Pathology_Reports', index=False)
        
        # Summary statistics sheet
        malignant_count = (df['Diagnosis_Category'] == 'Malignant').sum()
        premalignant_count = (df['Diagnosis_Category'] == 'Pre-malignant').sum()
        benign_count = (df['Diagnosis_Category'] == 'Benign').sum()
        breast_count = df['Specimen_Type'].str.contains('Breast', case=False).sum()
        lung_count = df['Specimen_Type'].str.contains('Lung', case=False).sum()
        colon_count = df['Specimen_Type'].str.contains('Colon', case=False).sum()
        cervical_count = df['Specimen_Type'].str.contains('Cervical', case=False).sum()
        avg_age = df['Age'].mean()
        
        summary_data = {
            'Metric': [
                'Total Reports',
                'Malignant Cases',
                'Pre-malignant Cases', 
                'Benign Cases',
                'Breast Specimens',
                'Lung Specimens',
                'Colon Specimens',
                'Cervical Specimens',
                'Average Patient Age'
            ],
            'Value': [
                str(len(df)),
                str(malignant_count),
                str(premalignant_count),
                str(benign_count),
                str(breast_count),
                str(lung_count),
                str(colon_count),
                str(cervical_count),
                f"{avg_age:.1f} years"
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Sample reports for quick testing
        sample_reports = df.head(10)[['Patient_ID', 'Specimen_Type', 'Pathology_Report', 'Diagnosis_Category']]
        sample_reports.to_excel(writer, sheet_name='Sample_Reports', index=False)
    
    print(f"✅ Created {filename} with {len(df)} realistic pathology reports!")
    
    # Calculate counts safely
    malignant_count = (df['Diagnosis_Category'] == 'Malignant').sum()
    premalignant_count = (df['Diagnosis_Category'] == 'Pre-malignant').sum()
    benign_count = (df['Diagnosis_Category'] == 'Benign').sum()
    
    print(f"📊 Distribution:")
    print(f"   - Malignant: {malignant_count}")
    print(f"   - Pre-malignant: {premalignant_count}")
    print(f"   - Benign: {benign_count}")
    
    return filename, df

def test_analyzer_with_excel(excel_file, analyzer, num_samples=5):
    """Test the analyzer with Excel data"""
    
    # Read Excel file
    df = pd.read_excel(excel_file, sheet_name='Pathology_Reports')
    
    print(f"\n{'='*60}")
    print(f"TESTING ANALYZER WITH EXCEL DATA")
    print(f"{'='*60}")
    
    # Test with random samples
    sample_reports = df.sample(n=num_samples)
    
    results_summary = []
    
    for idx, row in sample_reports.iterrows():
        print(f"\n🔬 Testing Report #{row['Patient_ID']} - {row['Specimen_Type']}")
        print(f"Expected Category: {row['Diagnosis_Category']}")
        print("-" * 50)
        
        # Analyze with enhanced analyzer
        results, diagnosis_info = analyzer.compare_with_original(row['Pathology_Report'])
        
        # Store results
        results_summary.append({
            'Patient_ID': row['Patient_ID'],
            'Specimen_Type': row['Specimen_Type'],
            'Expected_Category': row['Diagnosis_Category'],
            'AI_Diagnosis': diagnosis_info['final_diagnosis'],
            'AI_Confidence': diagnosis_info['confidence'],
            'Terms_Found': sum(len(terms) for terms in results['diagnostic_categories'].values()),
            'Severity_Detected': ', '.join(results.get('severity_indicators', {}).keys())
        })
        
        # Show brief summary
        print(f"🎯 AI Diagnosis: {diagnosis_info['final_diagnosis']}")
        print(f"📊 Confidence: {diagnosis_info['confidence']}")
        print(f"🔍 Terms Found: {sum(len(terms) for terms in results['diagnostic_categories'].values())}")
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(results_summary)
    
    # Save results
    summary_df.to_excel('analyzer_test_results.xlsx', index=False)
    print(f"\n✅ Test results saved to 'analyzer_test_results.xlsx'")
    
    return summary_df

if __name__ == "__main__":
    # Create the Excel file
    filename, df = create_pathology_excel()
    
    # Show sample reports
    print(f"\n📋 Sample pathology reports:")
    for i, row in df.head(3).iterrows():
        print(f"\n--- Report {i} ---")
        print(f"Patient: {row['Patient_Name']} ({row['Age']}Y {row['Gender']})")
        print(f"Specimen: {row['Specimen_Type']}")
        print(f"Category: {row['Diagnosis_Category']}")
        print(f"Report: {row['Pathology_Report'][:200]}...")
    
    print(f"\n🎯 Ready to test with your enhanced analyzer!")
    print(f"💡 Use: test_analyzer_with_excel('{filename}', analyzer)")