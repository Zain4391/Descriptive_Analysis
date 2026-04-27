# Descriptive Analysis of Pathology Reports

A Python-based NLP pipeline for descriptive analysis and classification of pathology reports. The project generates synthetic pathology datasets, analyzes report content using semantic similarity and keyword extraction, and produces comprehensive visualizations of diagnostic outcomes.

## Features

- **Synthetic data generation** – Creates realistic pathology reports covering breast, lung, colon, cervical, and other specimen types
- **Content analysis** – Classifies reports as Malignant, Pre-malignant, or Benign using rule-based term matching and sentence transformer embeddings
- **Severity scoring** – Detects high/moderate/low-grade indicators and morphological features
- **Visualization pipeline** – Generates charts, word clouds, and interactive Plotly dashboards from analysis results

## Project Structure

```
Descriptive_Analysis/
├── Analysis.py                    # Core pathology content analyzer (EnhancedPathologyContentAnalyzer)
├── Generate.py                    # Synthetic pathology report dataset generator
├── Visuals.py                     # Results visualization pipeline
├── Techniques.docx                # Documentation of analysis techniques
├── pathology_reports_dataset.xlsx # Generated dataset (100 reports)
├── analyzer_test_results.xlsx     # Output of analyzer test run
└── pathology_analysis_report.txt  # Text summary of analysis results
```

## Requirements

Install the dependencies before running:

```bash
pip install pandas openpyxl rich matplotlib numpy scikit-learn sentence-transformers seaborn wordcloud plotly
```

## Usage

### 1. Generate the dataset

```bash
python Generate.py
```

This creates `pathology_reports_dataset.xlsx` with 100 synthetic pathology reports and a summary sheet.

### 2. Run the analyzer

```python
from Analysis import EnhancedPathologyContentAnalyzer

analyzer = EnhancedPathologyContentAnalyzer()

report_text = "Sections reveal invasive ductal carcinoma, grade II/III..."
results, diagnosis_info = analyzer.compare_with_original(report_text)

print(diagnosis_info['final_diagnosis'])
print(diagnosis_info['confidence'])
```

### 3. Visualize results

```bash
python Visuals.py
```

This reads `analyzer_test_results.xlsx` and produces charts and dashboards for the analysis output.

## Diagnosis Categories

| Category | Description |
|---|---|
| **Malignant** | Confirmed invasive carcinoma, sarcoma, melanoma, or other cancer |
| **Pre-malignant** | Dysplasia, carcinoma in situ, atypical hyperplasia |
| **Benign** | Reactive changes, chronic inflammation, benign neoplasms |

## Author

**Zain Rasool**  
Version: 1.2 — 30/6/25

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
