'''
Pathology Results Visualization Pipeline
Comprehensive analysis and visualization of AI pathology results

Save as: visualization_pipeline.py
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
import re
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class PathologyResultsVisualizer:
    def __init__(self, results_file='analyzer_test_results.xlsx'):
        """Initialize with results file"""
        self.results_file = results_file
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load and prepare data"""
        try:
            self.df = pd.read_excel(self.results_file)
            print(f"✅ Loaded {len(self.df)} results from {self.results_file}")
            print(f"📋 Columns found: {list(self.df.columns)}")
            self.prepare_data()
        except FileNotFoundError:
            print(f"❌ File {self.results_file} not found!")
            print("💡 Make sure you've run the complete analysis first")
    
    def prepare_data(self):
        """Clean and prepare data for analysis"""
        if self.df is None:
            return
        
        # Handle missing Severity_Detected column gracefully
        if 'Severity_Detected' not in self.df.columns:
            self.df['Severity_Detected'] = ''
        
        # Extract severity and diagnosis from AI_Diagnosis
        self.df['AI_Severity'] = self.df['AI_Diagnosis'].str.extract(r'^(high-grade|moderate-grade|low-grade)')
        self.df['AI_Primary_Term'] = self.df['AI_Diagnosis'].str.replace(r'^(high-grade|moderate-grade|low-grade)\s*', '', regex=True)
        
        # Create accuracy column
        self.df['Category_Match'] = self.df.apply(self._check_category_match, axis=1)
        
        # Parse severity detected - handle NaN values
        self.df['Has_Severity'] = self.df['Severity_Detected'].fillna('').str.len() > 0
        
        print(f"📊 Data prepared: {len(self.df)} records with {self.df['Category_Match'].sum()} category matches")
        print(f"🎯 Overall accuracy: {self.df['Category_Match'].mean()*100:.1f}%")
    
    def _check_category_match(self, row):
        """Check if AI diagnosis category matches expected"""
        expected = row['Expected_Category'].lower()
        ai_diagnosis = row['AI_Diagnosis'].lower()
        
        # Define category keywords
        malignant_keywords = ['carcinoma', 'sarcoma', 'lymphoma', 'melanoma', 'cancer', 'malignancy']
        premalignant_keywords = ['dysplasia', 'in situ', 'atypical', 'cin', 'hyperplasia']
        benign_keywords = ['benign', 'inflammation', 'hyperplasia', 'fibrosis', 'reactive']
        
        if expected == 'malignant':
            return any(keyword in ai_diagnosis for keyword in malignant_keywords)
        elif expected == 'pre-malignant':
            return any(keyword in ai_diagnosis for keyword in premalignant_keywords)
        elif expected == 'benign':
            return any(keyword in ai_diagnosis for keyword in benign_keywords)
        return False
    
    def create_overview_dashboard(self):
        """Create comprehensive overview dashboard"""
        if self.df is None:
            return
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # 1. Category Accuracy
        ax1 = axes[0, 0]
        accuracy_data = self.df.groupby('Expected_Category')['Category_Match'].agg(['sum', 'count'])
        accuracy_data['accuracy'] = accuracy_data['sum'] / accuracy_data['count'] * 100
        
        bars = ax1.bar(accuracy_data.index, accuracy_data['accuracy'], 
                      color=['#ff7f7f', '#7f7fff', '#7fff7f'], alpha=0.8)
        ax1.set_title('Category Prediction Accuracy', fontweight='bold', fontsize=12)
        ax1.set_ylabel('Accuracy (%)')
        ax1.set_ylim(0, 100)
        
        # Add percentage labels
        for bar, pct in zip(bars, accuracy_data['accuracy']):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{pct:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # 2. Confidence Distribution
        ax2 = axes[0, 1]
        confidence_counts = self.df['AI_Confidence'].value_counts()
        colors = {'High': '#4CAF50', 'Moderate': '#FF9800', 'Low': '#F44336'}
        wedges, texts, autotexts = ax2.pie(confidence_counts.values, 
                                          labels=confidence_counts.index,
                                          autopct='%1.1f%%',
                                          colors=[colors.get(x, 'gray') for x in confidence_counts.index])
        ax2.set_title('AI Confidence Distribution', fontweight='bold', fontsize=12)
        
        # 3. Terms Found Distribution
        ax3 = axes[0, 2]
        terms_bins = [0, 5, 10, 15, 20, 25, 30, 50]
        ax3.hist(self.df['Terms_Found'], bins=terms_bins, alpha=0.7, color='skyblue', edgecolor='black')
        ax3.set_title('Terms Found per Report', fontweight='bold', fontsize=12)
        ax3.set_xlabel('Number of Terms')
        ax3.set_ylabel('Frequency')
        ax3.axvline(self.df['Terms_Found'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {self.df["Terms_Found"].mean():.1f}')
        ax3.legend()
        
        # 4. Severity Analysis
        ax4 = axes[1, 0]
        severity_counts = self.df['AI_Severity'].value_counts().dropna()
        if not severity_counts.empty:
            severity_colors = {'high-grade': '#d32f2f', 'moderate-grade': '#f57c00', 'low-grade': '#388e3c'}
            bars = ax4.bar(severity_counts.index, severity_counts.values,
                          color=[severity_colors.get(x, 'gray') for x in severity_counts.index])
            ax4.set_title('Severity Grade Distribution', fontweight='bold', fontsize=12)
            ax4.set_ylabel('Count')
            plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)
        else:
            ax4.text(0.5, 0.5, 'No Severity Data', ha='center', va='center', 
                    transform=ax4.transAxes, fontsize=12)
            ax4.set_title('Severity Grade Distribution', fontweight='bold', fontsize=12)
        
        # 5. Specimen Type Analysis
        ax5 = axes[1, 1]
        specimen_counts = self.df['Specimen_Type'].value_counts()
        ax5.barh(specimen_counts.index, specimen_counts.values, alpha=0.7)
        ax5.set_title('Specimen Types Analyzed', fontweight='bold', fontsize=12)
        ax5.set_xlabel('Count')
        
        # 6. Accuracy by Specimen Type
        ax6 = axes[1, 2]
        specimen_accuracy = self.df.groupby('Specimen_Type')['Category_Match'].mean() * 100
        bars = ax6.bar(range(len(specimen_accuracy)), specimen_accuracy.values, alpha=0.7)
        ax6.set_title('Accuracy by Specimen Type', fontweight='bold', fontsize=12)
        ax6.set_ylabel('Accuracy (%)')
        ax6.set_xticks(range(len(specimen_accuracy)))
        ax6.set_xticklabels(specimen_accuracy.index, rotation=45, ha='right')
        ax6.set_ylim(0, 100)
        
        plt.tight_layout()
        plt.suptitle('Pathology AI Analysis - Overview Dashboard', fontsize=16, fontweight='bold', y=0.98)
        plt.show()
    
    def create_diagnostic_term_analysis(self):
        """Analyze the most common diagnostic terms"""
        if self.df is None:
            return
        
        # Extract all diagnostic terms from AI_Primary_Term
        all_terms = []
        for diagnosis in self.df['AI_Primary_Term'].dropna():
            # Split on common separators and clean
            terms = re.split(r'[,\s]+', diagnosis.lower())
            all_terms.extend([term.strip() for term in terms if len(term.strip()) > 2])
        
        # Also get full AI_Diagnosis terms
        all_diagnoses = self.df['AI_Diagnosis'].dropna().str.lower().tolist()
        
        # Count individual terms
        term_counts = Counter(all_terms)
        top_terms = dict(term_counts.most_common(15))
        
        # Count full diagnoses
        diagnosis_counts = Counter(all_diagnoses)
        top_diagnoses = dict(diagnosis_counts.most_common(10))
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 12))
        
        # 1. Top diagnostic terms bar chart
        if top_terms:
            terms = list(top_terms.keys())
            counts = list(top_terms.values())
            
            bars = ax1.barh(terms, counts, alpha=0.8, color='skyblue')
            ax1.set_title('Most Common Diagnostic Terms', fontweight='bold', fontsize=14)
            ax1.set_xlabel('Frequency')
            ax1.invert_yaxis()
            
            # Add count labels
            for bar, count in zip(bars, counts):
                ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                        str(count), va='center', fontweight='bold')
        
        # 2. Full diagnoses
        if top_diagnoses:
            diag_names = [d[:25] + '...' if len(d) > 25 else d for d in top_diagnoses.keys()]
            diag_counts = list(top_diagnoses.values())
            
            bars = ax2.barh(diag_names, diag_counts, alpha=0.8, color='lightcoral')
            ax2.set_title('Most Common Full Diagnoses', fontweight='bold', fontsize=14)
            ax2.set_xlabel('Frequency')
            ax2.invert_yaxis()
            
            for bar, count in zip(bars, diag_counts):
                ax2.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                        str(count), va='center', fontweight='bold')
        
        # 3. Word cloud
        if len(all_terms) > 10:
            try:
                wordcloud = WordCloud(width=600, height=400, 
                                     background_color='white',
                                     colormap='viridis').generate(' '.join(all_terms))
                ax3.imshow(wordcloud, interpolation='bilinear')
                ax3.axis('off')
                ax3.set_title('Diagnostic Terms Word Cloud', fontweight='bold', fontsize=14)
            except:
                ax3.text(0.5, 0.5, 'Word Cloud\nUnavailable', ha='center', va='center', 
                        transform=ax3.transAxes, fontsize=12)
                ax3.set_title('Diagnostic Terms Word Cloud', fontweight='bold', fontsize=14)
        else:
            ax3.text(0.5, 0.5, 'Insufficient\nTerms for\nWord Cloud', ha='center', va='center', 
                    transform=ax3.transAxes, fontsize=12)
            ax3.set_title('Diagnostic Terms Word Cloud', fontweight='bold', fontsize=14)
        
        # 4. Terms found distribution by category
        terms_by_category = self.df.groupby('Expected_Category')['Terms_Found'].agg(['mean', 'std', 'count'])
        
        categories = terms_by_category.index
        means = terms_by_category['mean']
        stds = terms_by_category['std'].fillna(0)
        
        bars = ax4.bar(categories, means, yerr=stds, capsize=5, alpha=0.8, 
                      color=['#ff7f7f', '#7f7fff', '#7fff7f'])
        ax4.set_title('Average Terms Found by Category', fontweight='bold', fontsize=14)
        ax4.set_ylabel('Average Terms Found')
        ax4.set_xlabel('Expected Category')
        
        # Add count labels
        for bar, mean, count in zip(bars, means, terms_by_category['count']):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + bar.get_height()*0.05, 
                    f'{mean:.1f}\n(n={count})', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def create_performance_heatmap(self):
        """Create performance heatmap by category and specimen type"""
        if self.df is None:
            return
        
        # Create cross-tabulation
        performance_matrix = pd.crosstab(self.df['Specimen_Type'], 
                                       self.df['Expected_Category'], 
                                       self.df['Category_Match'], 
                                       aggfunc='mean') * 100
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(performance_matrix, annot=True, fmt='.1f', cmap='RdYlGn', 
                   cbar_kws={'label': 'Accuracy (%)'}, vmin=0, vmax=100)
        plt.title('AI Accuracy Heatmap: Specimen Type vs Expected Category', 
                 fontweight='bold', fontsize=14)
        plt.ylabel('Specimen Type')
        plt.xlabel('Expected Category')
        plt.tight_layout()
        plt.show()
    
    def create_confidence_accuracy_analysis(self):
        """Analyze relationship between confidence and accuracy"""
        if self.df is None:
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Confidence vs Accuracy
        conf_accuracy = self.df.groupby('AI_Confidence').agg({
            'Category_Match': ['mean', 'count'],
            'Terms_Found': 'mean'
        }).round(3)
        
        conf_accuracy.columns = ['Accuracy', 'Count', 'Avg_Terms']
        conf_accuracy['Accuracy'] *= 100
        
        # Bar plot
        bars = ax1.bar(conf_accuracy.index, conf_accuracy['Accuracy'], 
                      alpha=0.8, color=['#4CAF50', '#FF9800', '#F44336'])
        ax1.set_title('Accuracy by Confidence Level', fontweight='bold')
        ax1.set_ylabel('Accuracy (%)')
        ax1.set_ylim(0, 100)
        
        # Add labels
        for bar, acc, count in zip(bars, conf_accuracy['Accuracy'], conf_accuracy['Count']):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{acc:.1f}%\n(n={count})', ha='center', va='bottom', fontweight='bold')
        
        # Terms found vs Confidence
        confidence_order = ['Low', 'Moderate', 'High']
        conf_data = [self.df[self.df['AI_Confidence'] == conf]['Terms_Found'].values 
                    for conf in confidence_order if conf in self.df['AI_Confidence'].values]
        conf_labels = [conf for conf in confidence_order if conf in self.df['AI_Confidence'].values]
        
        ax2.boxplot(conf_data, labels=conf_labels)
        ax2.set_title('Terms Found by Confidence Level', fontweight='bold')
        ax2.set_ylabel('Number of Terms Found')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def create_interactive_dashboard(self):
        """Create interactive dashboard using Plotly"""
        if self.df is None:
            return
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Category Accuracy', 'Confidence vs Terms Found', 
                          'Specimen Type Distribution', 'Severity Timeline'],
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "pie"}, {"type": "bar"}]]
        )
        
        # 1. Category Accuracy
        accuracy_data = self.df.groupby('Expected_Category')['Category_Match'].mean() * 100
        fig.add_trace(
            go.Bar(x=accuracy_data.index, y=accuracy_data.values, 
                   name="Accuracy", marker_color=['#ff7f7f', '#7f7fff', '#7fff7f']),
            row=1, col=1
        )
        
        # 2. Confidence vs Terms Found scatter
        colors = {'High': '#4CAF50', 'Moderate': '#FF9800', 'Low': '#F44336'}
        for conf in self.df['AI_Confidence'].unique():
            conf_data = self.df[self.df['AI_Confidence'] == conf]
            fig.add_trace(
                go.Scatter(x=conf_data['Terms_Found'], y=conf_data['Category_Match'].astype(int),
                          mode='markers', name=f'{conf} Confidence',
                          marker=dict(color=colors.get(conf, 'gray'), size=8)),
                row=1, col=2
            )
        
        # 3. Specimen Type Distribution
        specimen_counts = self.df['Specimen_Type'].value_counts()
        fig.add_trace(
            go.Pie(labels=specimen_counts.index, values=specimen_counts.values, name="Specimens"),
            row=2, col=1
        )
        
        # 4. Severity Distribution
        severity_counts = self.df['AI_Severity'].value_counts().dropna()
        if not severity_counts.empty:
            fig.add_trace(
                go.Bar(x=severity_counts.index, y=severity_counts.values, 
                       name="Severity", marker_color=['#d32f2f', '#f57c00', '#388e3c']),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title_text="Interactive Pathology Analysis Dashboard",
            title_x=0.5,
            height=800,
            showlegend=True
        )
        
        fig.show()
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        if self.df is None:
            return
        
        total_reports = len(self.df)
        overall_accuracy = self.df['Category_Match'].mean() * 100
        avg_terms = self.df['Terms_Found'].mean()
        high_confidence_pct = (self.df['AI_Confidence'] == 'High').mean() * 100
        
        # Category-specific accuracy
        category_accuracy = self.df.groupby('Expected_Category')['Category_Match'].mean() * 100
        
        # Confidence vs accuracy
        conf_accuracy = self.df.groupby('AI_Confidence')['Category_Match'].mean() * 100
        
        report = f"""
PATHOLOGY AI ANALYSIS SUMMARY REPORT
{'='*50}

OVERALL PERFORMANCE:
   • Total Reports Analyzed: {total_reports}
   • Overall Accuracy: {overall_accuracy:.1f}%
   • Average Terms Found: {avg_terms:.1f}
   • High Confidence Predictions: {high_confidence_pct:.1f}%

ACCURACY BY CATEGORY:
"""
        for category, accuracy in category_accuracy.items():
            report += f"   • {category}: {accuracy:.1f}%\n"
        
        report += f"""
CONFIDENCE vs ACCURACY:
"""
        for conf, accuracy in conf_accuracy.items():
            count = (self.df['AI_Confidence'] == conf).sum()
            report += f"   • {conf}: {accuracy:.1f}% (n={count})\n"
        
        # Top diagnostic terms
        all_terms = []
        for diagnosis in self.df['AI_Primary_Term'].dropna():
            terms = re.split(r'[,\s]+', diagnosis.lower())
            all_terms.extend([term.strip() for term in terms if len(term.strip()) > 2])
        
        top_terms = Counter(all_terms).most_common(5)
        
        report += f"""
TOP DIAGNOSTIC TERMS:
"""
        for term, count in top_terms:
            report += f"   • {term}: {count} times\n"
        
        report += f"""
KEY INSIGHTS:
   • Best performing category: {category_accuracy.idxmax()} ({category_accuracy.max():.1f}%)
   • Most reliable confidence level: {conf_accuracy.idxmax()} ({conf_accuracy.max():.1f}%)
   • Average terms per report suggests good detection coverage
   • {'High accuracy indicates strong model performance' if overall_accuracy > 80 else 'Moderate accuracy suggests room for improvement'}

Detailed results saved in: {self.results_file}
        """
        
        print(report)
        
        # Save report to file with UTF-8 encoding
        with open('pathology_analysis_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report
    
    def run_complete_analysis(self):
        """Run all visualization analyses"""
        if self.df is None:
            print("❌ No data loaded. Cannot run analysis.")
            return
        
        print("🎨 Starting Complete Visualization Pipeline...")
        print("="*50)
        
        # Generate all visualizations
        print("📊 1. Creating Overview Dashboard...")
        self.create_overview_dashboard()
        
        print("🔍 2. Analyzing Diagnostic Terms...")
        self.create_diagnostic_term_analysis()
        
        print("🌡️ 3. Creating Performance Heatmap...")
        self.create_performance_heatmap()
        
        print("🎯 4. Analyzing Confidence vs Accuracy...")
        self.create_confidence_accuracy_analysis()
        
        print("📱 5. Creating Interactive Dashboard...")
        try:
            self.create_interactive_dashboard()
        except ImportError:
            print("⚠️  Plotly not available - skipping interactive dashboard")
        
        print("📄 6. Generating Summary Report...")
        self.generate_summary_report()
        
        print("\n🎉 Complete visualization pipeline finished!")
        print("📁 Check 'pathology_analysis_report.txt' for detailed summary")

# Main execution
if __name__ == "__main__":
    # Initialize visualizer
    visualizer = PathologyResultsVisualizer()
    
    # Run complete analysis
    visualizer.run_complete_analysis()
    
    print(f"""
🚀 VISUALIZATION PIPELINE COMPLETE!

Generated:
✅ Overview Dashboard (6 panels)
✅ Diagnostic Terms Analysis
✅ Performance Heatmap  
✅ Confidence Analysis
✅ Interactive Dashboard (if Plotly available)
✅ Summary Report (pathology_analysis_report.txt)

💡 Next steps:
   - Review the summary report for key insights
   - Check accuracy by category and specimen type
   - Analyze confidence vs performance relationship
   - Use insights to improve the AI model
    """)