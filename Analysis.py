'''
Fixed Enhanced Pathology Content Analyzer
Resolves all matplotlib and type errors

Author: Zain Rasool (Fixed)
Date: 30/6/25
Version: 1.2
'''

import re
from collections import defaultdict, Counter
from rich.console import Console
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

console = Console()

class EnhancedPathologyContentAnalyzer:
    def __init__(self):
        # Load sentence transformer for embeddings
        print("Loading SentenceTransformer model...")
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Enhanced corpus (just more terms, same structure)
        self.diagnostic_terms = {
            'malignant': [
                'carcinoma', 'adenocarcinoma', 'sarcoma', 'lymphoma', 'melanoma',
                'invasive carcinoma', 'ductal carcinoma', 'lobular carcinoma', 
                'squamous cell carcinoma', 'invasive ductal carcinoma', 
                'invasive lobular carcinoma', 'tumor', 'cancer', 'malignancy',
                'neoplasm', 'metastasis', 'poorly differentiated', 'undifferentiated'
            ],
            'pre_malignant': [
                'dysplasia', 'carcinoma in situ', 'atypical hyperplasia',
                'ductal carcinoma in situ', 'lobular carcinoma in situ',
                'high grade dysplasia', 'severe dysplasia', 'moderate dysplasia',
                'mild dysplasia', 'atypical ductal hyperplasia', 'atypical lobular hyperplasia'
            ],
            'benign': [
                'hyperplasia', 'metaplasia', 'inflammation', 'fibrosis',
                'chronic inflammation', 'acute inflammation', 'reactive hyperplasia',
                'lymphocytic infiltrate', 'fibroadenoma', 'adenoma', 'benign'
            ],
            'morphology': [
                'pleomorphism', 'mitotic activity', 'nuclear atypia', 'differentiation',
                'nuclear pleomorphism', 'cellular pleomorphism', 'mitotic figures',
                'nuclear enlargement', 'prominent nucleoli', 'hyperchromatic nuclei',
                'architectural distortion', 'loss of architecture', 'cellular crowding'
            ]
        }

        self.severity_modifiers = {
            'high': [
                'severe', 'marked', 'prominent', 'high-grade', 'extensive',
                'elevated', 'numerous', 'profound', 'markedly increased', 
                'pronounced', 'intense', 'grade iii', 'grade iv', 'grade 3', 'grade 4',
                'poorly differentiated', 'aggressive', 'widespread'
            ],
            'moderate': [
                'moderate', 'intermediate', 'moderately',
                'borderline', 'average', 'notable', 'moderately increased',
                'grade ii', 'grade 2', 'moderately differentiated'
            ],
            'low': [
                'mild', 'minimal', 'low-grade', 'slight', 'focal',
                'few', 'scant', 'occasional', 'limited', 'low-density', 'sparse',
                'grade i', 'grade 1', 'well differentiated'
            ]
        }

        self.negation_terms = ['no', 'negative', 'absent', 'not', 'without', 'lacks']

        self.quantity_patterns = {
            'mitotic_count': r'(\d+)\s*mitoses?\s*per\s*(\d+)\s*hpf',
            'grade': r'grade\s*([IVX\d]+)',
            'percentage': r'(\d+)%', 
            'size': r'(\d+\.?\d*)\s*(mm|cm)'
        }
        
        # Pre-compute embeddings for faster similarity matching
        print("Pre-computing term embeddings...")
        self._precompute_embeddings()
        print("Ready!")

    def _precompute_embeddings(self):
        """Pre-compute embeddings for all diagnostic terms"""
        self.term_embeddings = {}
        
        for category, terms in self.diagnostic_terms.items():
            self.term_embeddings[category] = {}
            for term in terms:
                embedding = self.sentence_model.encode(term)
                self.term_embeddings[category][term] = embedding

    def _find_terms_with_embeddings(self, sentence, similarity_threshold=0.7):
        """Find terms using both exact matching and embedding similarity"""
        sentence_lower = sentence.lower()
        sentence_embedding = self.sentence_model.encode(sentence_lower)
        found_terms = []
        
        for category, term_embeddings in self.term_embeddings.items():
            for term, term_embedding in term_embeddings.items():
                # Check exact match first (faster)
                if term in sentence_lower:
                    found_terms.append({
                        'term': term, 
                        'category': category,
                        'method': 'exact',
                        'similarity': 1.0
                    })
                else:
                    # Check semantic similarity
                    similarity = cosine_similarity(
                        sentence_embedding.reshape(1, -1), 
                        term_embedding.reshape(1, -1)
                    )[0][0]
                    
                    if similarity > similarity_threshold:
                        found_terms.append({
                            'term': term, 
                            'category': category,
                            'method': 'semantic',
                            'similarity': float(similarity)
                        })
        
        return found_terms

    def _analyze_sentence(self, sentence):
        """Enhanced sentence analysis with embeddings"""
        sentence_lower = sentence.lower()
        features = {
            'text': sentence,
            'diagnostic_terms': [],
            'severity': None,
            'is_negative': False,
            'quantitative': {}
        }

        # Negation detection (same as original)
        features['is_negative'] = any(re.search(rf'\b{re.escape(neg)}\b', sentence_lower) for neg in self.negation_terms)

        # Enhanced term detection using embeddings
        found_terms = self._find_terms_with_embeddings(sentence)
        for term_info in found_terms:
            features['diagnostic_terms'].append(term_info)

        # Severity detection (same as original)
        for severity, modifiers in self.severity_modifiers.items():
            if any(mod in sentence_lower for mod in modifiers):
                features['severity'] = severity
                break

        # Quantitative patterns (same as original)
        for data_type, pattern in self.quantity_patterns.items():
            matches = re.findall(pattern, sentence_lower)
            if matches:
                features['quantitative'][data_type] = matches

        return features

    def extract_structured_features(self, text):
        """Same as original but with enhanced sentence analysis"""
        features = {
            'diagnostic_categories': {},
            'severity_indicators': {},
            'negation_context': [],
            'quantitative_data': {},
            'co_occurrences': [],
            'sentence_analysis': []
        }

        sentences = re.split(r'[.!?]+', text)

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            analysis = self._analyze_sentence(sentence)
            features['sentence_analysis'].append(analysis)

        features = self._aggregate_features(features)
        return features

    def _aggregate_features(self, features):
        """Same as original aggregation"""
        all_diagnostic_terms = []
        all_severity = []

        for sentence_analysis in features['sentence_analysis']:
            for term_info in sentence_analysis['diagnostic_terms']:
                category = term_info['category']
                if category not in features['diagnostic_categories']:
                    features['diagnostic_categories'][category] = []

                features['diagnostic_categories'][category].append({
                    'term': term_info['term'],
                    'context': sentence_analysis['text'],
                    'is_negative': sentence_analysis['is_negative'],
                    'severity': sentence_analysis['severity'],
                    'detection_method': term_info.get('method', 'exact'),
                    'similarity': term_info.get('similarity', 1.0)
                })

                all_diagnostic_terms.append(term_info['term'])

            if sentence_analysis['is_negative']:
                features['negation_context'].append(sentence_analysis['text'])

            if sentence_analysis['severity']:
                all_severity.append(sentence_analysis['severity'])

            for data_type, values in sentence_analysis['quantitative'].items():
                if data_type not in features['quantitative_data']:
                    features['quantitative_data'][data_type] = []
                features['quantitative_data'][data_type].extend(values)

        features['severity_indicators'] = dict(Counter(all_severity))
        features['co_occurrences'] = dict(self._find_cooccurrences(features['sentence_analysis']))
        return features

    def _find_cooccurrences(self, sentence_analyses):
        """Same as original co-occurrence detection"""
        co_occurrences = []

        for sentence_analysis in sentence_analyses:
            terms = []
            for term_info in sentence_analysis['diagnostic_terms']:
                terms.append(term_info['term'])

            if len(terms) > 1:
                for i in range(len(terms)):
                    for j in range(i + 1, len(terms)):
                        co_occurrence = f"{terms[i]} + {terms[j]}"
                        co_occurrences.append(co_occurrence)

        return Counter(co_occurrences)

    def generate_final_diagnosis(self, results):
        """Generate final diagnostic decision based on analysis"""
        
        # Calculate weighted scores for each category
        category_scores = {}
        diagnostic_weights = {
            'malignant': 4.0,      # Highest priority
            'pre_malignant': 3.0,  # High priority
            'morphology': 2.0,     # Supportive evidence
            'benign': 1.0          # Lowest priority
        }
        
        for category, entries in results['diagnostic_categories'].items():
            # Count non-negated terms only
            non_negated = [entry for entry in entries if not entry['is_negative']]
            if non_negated:
                # Weight by category importance and similarity scores
                weight = diagnostic_weights.get(category, 1.0)
                avg_similarity = np.mean([entry.get('similarity', 1.0) for entry in non_negated])
                category_scores[category] = len(non_negated) * weight * avg_similarity
        
        # Determine primary diagnosis
        if not category_scores:
            primary_diagnosis = "No significant pathology identified"
            confidence = "Low"
        else:
            primary_category = max(category_scores.items(), key=lambda x: x[1])[0]
            primary_score = category_scores[primary_category]
            
            # Get most confident term from primary category
            primary_entries = [e for e in results['diagnostic_categories'][primary_category] 
                             if not e['is_negative']]
            if primary_entries:
                best_term = max(primary_entries, key=lambda x: x.get('similarity', 1.0))
                primary_diagnosis = best_term['term']
                
                # Determine confidence based on score and detection method
                if primary_score > 8 and best_term.get('similarity', 1.0) > 0.8:
                    confidence = "High"
                elif primary_score > 4:
                    confidence = "Moderate" 
                else:
                    confidence = "Low"
            else:
                primary_diagnosis = "Indeterminate"
                confidence = "Low"
        
        # Add severity modifier if available
        severity_modifier = ""
        if results['severity_indicators']:
            dominant_severity = max(results['severity_indicators'].items(), key=lambda x: x[1])[0]
            if dominant_severity in ['high', 'severe']:
                severity_modifier = "high-grade "
            elif dominant_severity in ['moderate']:
                severity_modifier = "moderate-grade "
            elif dominant_severity in ['low', 'mild']:
                severity_modifier = "low-grade "
        
        final_diagnosis = f"{severity_modifier}{primary_diagnosis}".strip()
        
        return {
            'final_diagnosis': final_diagnosis,
            'confidence': confidence,
            'category_scores': category_scores,
            'supporting_evidence': {
                'quantitative_findings': results.get('quantitative_data', {}),
                'negated_findings': [entry['term'] for category in results['diagnostic_categories'].values() 
                                   for entry in category if entry['is_negative']],
                'severity_indicators': results.get('severity_indicators', {})
            }
        }

    def plot_comprehensive_analysis(self, results, diagnosis_info):
        """Create comprehensive visualization of the analysis"""
        
        fig = plt.figure(figsize=(16, 12))
        
        # 1. Category Distribution (Top Left)
        plt.subplot(2, 3, 1)
        categories = list(results['diagnostic_categories'].keys())
        if categories:
            category_counts = [len(results['diagnostic_categories'][cat]) for cat in categories]
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'][:len(categories)]
            bars = plt.bar(categories, category_counts, color=colors, alpha=0.7)
            plt.title('Diagnostic Terms by Category', fontweight='bold')
            plt.ylabel('Number of Terms')
            plt.xticks(rotation=45)
            
            # Add value labels on bars
            for bar, count in zip(bars, category_counts):
                if count > 0:
                    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                            str(count), ha='center', va='bottom', fontweight='bold')
        else:
            plt.text(0.5, 0.5, 'No Categories\nFound', ha='center', va='center', 
                    transform=plt.gca().transAxes, fontsize=12)
            plt.title('Diagnostic Terms by Category', fontweight='bold')
        
        # 2. Detection Methods (Top Center)
        plt.subplot(2, 3, 2)
        methods = []
        for category in results['diagnostic_categories'].values():
            for entry in category:
                methods.append(entry.get('detection_method', 'exact'))
        
        if methods:
            method_counts = Counter(methods)
            colors = ['#ff9999', '#66b3ff', '#99ff99']
            plt.pie(list(method_counts.values()), 
                   labels=list(method_counts.keys()), 
                   autopct='%1.1f%%',
                   colors=colors[:len(method_counts)])
            plt.title('Detection Methods Used', fontweight='bold')
        else:
            plt.text(0.5, 0.5, 'No Methods\nFound', ha='center', va='center', 
                    transform=plt.gca().transAxes, fontsize=12)
            plt.title('Detection Methods Used', fontweight='bold')
        
        # 3. Confidence Distribution (Top Right)
        plt.subplot(2, 3, 3)
        similarities = []
        for category, entries in results['diagnostic_categories'].items():
            for entry in entries:
                if not entry['is_negative']:  # Only non-negated terms
                    similarities.append(entry.get('similarity', 1.0))
        
        if similarities:
            plt.scatter(range(len(similarities)), similarities, alpha=0.7, s=60, c='blue')
            plt.axhline(y=0.7, color='red', linestyle='--', alpha=0.5, label='Similarity Threshold')
            plt.title('Term Confidence Scores', fontweight='bold')
            plt.ylabel('Similarity Score')
            plt.xlabel('Term Index')
            plt.ylim(0, 1)
            plt.legend()
        else:
            plt.text(0.5, 0.5, 'No Confidence\nScores Available', ha='center', va='center', 
                    transform=plt.gca().transAxes, fontsize=12)
            plt.title('Term Confidence Scores', fontweight='bold')
        
        # 4. Severity Analysis (Bottom Left)
        plt.subplot(2, 3, 4)
        if results['severity_indicators']:
            severities = list(results['severity_indicators'].keys())
            severity_counts = list(results['severity_indicators'].values())
            colors_map = {'high': '#ff6b6b', 'moderate': '#ffd93d', 'low': '#6bcf7f'}
            bar_colors = [colors_map.get(sev, 'gray') for sev in severities]
            
            bars = plt.bar(severities, severity_counts, color=bar_colors, alpha=0.8)
            plt.title('Severity Distribution', fontweight='bold')
            plt.ylabel('Frequency')
            
            # Add value labels
            for bar, count in zip(bars, severity_counts):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
                        str(count), ha='center', va='bottom', fontweight='bold')
        else:
            plt.text(0.5, 0.5, 'No Severity\nIndicators Found', 
                    ha='center', va='center', fontsize=12, 
                    transform=plt.gca().transAxes)
            plt.title('Severity Distribution', fontweight='bold')
        
        # 5. Quantitative Findings (Bottom Center)
        plt.subplot(2, 3, 5)
        quant_data = results.get('quantitative_data', {})
        if quant_data:
            quant_types = list(quant_data.keys())
            quant_counts = [len(quant_data[qt]) for qt in quant_types]
            
            bars = plt.bar(quant_types, quant_counts, color='lightcoral', alpha=0.7)
            plt.title('Quantitative Measurements', fontweight='bold')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
            
            # Add value labels
            for bar, count in zip(bars, quant_counts):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
                        str(count), ha='center', va='bottom', fontweight='bold')
        else:
            plt.text(0.5, 0.5, 'No Quantitative\nData Found', 
                    ha='center', va='center', fontsize=12,
                    transform=plt.gca().transAxes)
            plt.title('Quantitative Measurements', fontweight='bold')
        
        # 6. Final Diagnosis Summary (Bottom Right)
        plt.subplot(2, 3, 6)
        plt.axis('off')
        
        # Create diagnosis summary text
        diagnosis_text = f"""FINAL DIAGNOSIS
{'='*20}

Primary Finding:
{diagnosis_info['final_diagnosis']}

Confidence: {diagnosis_info['confidence']}

Key Evidence:"""
        
        # Add top diagnostic terms
        top_terms = []
        for category, entries in results['diagnostic_categories'].items():
            for entry in entries:
                if not entry['is_negative']:
                    top_terms.append((entry['term'], entry.get('similarity', 1.0)))
        
        # Sort by similarity and take top 3
        top_terms.sort(key=lambda x: x[1], reverse=True)
        for i, (term, sim) in enumerate(top_terms[:3]):
            diagnosis_text += f"\n• {term} ({sim:.2f})"
        
        # Add negated findings if any
        negated = diagnosis_info['supporting_evidence']['negated_findings']
        if negated:
            diagnosis_text += f"\n\nRuled Out:\n• " + "\n• ".join(negated[:3])
        
        plt.text(0.05, 0.95, diagnosis_text, transform=plt.gca().transAxes, 
                fontsize=10, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
        
        plt.suptitle('Comprehensive Pathology Analysis Report', fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        plt.subplots_adjust(top=0.93)
        plt.show()

    def compare_with_original(self, text):
        """Compare enhanced vs original analyzer performance"""
        # Enhanced analysis
        enhanced_results = self.extract_structured_features(text)
        
        # Generate final diagnosis
        diagnosis_info = self.generate_final_diagnosis(enhanced_results)
        
        # Simulate original analyzer with basic corpus
        original_terms = {
            'malignant': ['carcinoma', 'adenocarcinoma', 'sarcoma', 'lymphoma', 'melanoma'],
            'pre_malignant': ['dysplasia', 'carcinoma in situ', 'atypical hyperplasia'],
            'benign': ['hyperplasia', 'metaplasia', 'inflammation', 'fibrosis'],
            'morphology': ['pleomorphism', 'mitotic activity', 'nuclear atypia', 'differentiation']
        }
        
        # Count terms found
        enhanced_count = sum(len(terms) for terms in enhanced_results['diagnostic_categories'].values())
        
        # Simulate original count
        original_count = 0
        text_lower = text.lower()
        for category, terms in original_terms.items():
            for term in terms:
                if term in text_lower:
                    original_count += 1
        
        print(f"\n{'='*60}")
        print(f"ANALYSIS COMPARISON & FINAL DIAGNOSIS")
        print(f"{'='*60}")
        print(f"Enhanced analyzer found: {enhanced_count} terms")
        print(f"Original analyzer would find: {original_count} terms")
        print(f"Improvement: {enhanced_count/original_count if original_count > 0 else 'N/A'}x")
        print(f"\nFINAL DIAGNOSIS: {diagnosis_info['final_diagnosis']}")
        print(f"Confidence Level: {diagnosis_info['confidence']}")
        print(f"{'='*60}")
        
        return enhanced_results, diagnosis_info

    # Keep all original plotting methods exactly the same but simplified
    def plot_diagnostic_terms(self, results):
        """Simplified diagnostic terms plot"""
        rows = []
        for category, entries in results['diagnostic_categories'].items():
            for items in entries:
                rows.append({
                    'Term': items['term'],
                    'Category': category,
                    'is_negative': items['is_negative'],
                    'Method': items.get('detection_method', 'exact')
                })
        
        if not rows:
            print("No diagnostic terms found for plotting")
            return
            
        df = pd.DataFrame(rows)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Original style plot
        category_counts = df['Category'].value_counts()
        ax1.bar(category_counts.index, category_counts.values, alpha=0.7)
        ax1.set_title('Diagnostic Terms by Category')
        ax1.set_ylabel('Count')
        ax1.tick_params(axis='x', rotation=45)
        
        # Detection methods
        method_counts = df['Method'].value_counts()
        ax2.pie(method_counts.values, labels=method_counts.index, autopct='%1.1f%%')
        ax2.set_title('Detection Methods')
        
        plt.tight_layout()
        plt.show()

    def plot_negation_pie(self, results):
        """Same as original but with error handling"""
        negated = 0
        affirmed = 0
        
        for category, entries in results['diagnostic_categories'].items():
            for item in entries:
                if item['is_negative']:
                    negated += 1
                else:
                    affirmed += 1
        
        if negated == 0 and affirmed == 0:
            print("No terms found for negation analysis")
            return
        
        labels = ['Affirmed', 'Negated']
        sizes = [affirmed, negated]
        colors = ['#66b3ff', '#ff9999']
        
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title('Negation Context of Diagnostic Terms')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def plot_cooccurrence_heatmap(self, results):
        """Simplified co-occurrence plot"""
        term_list = []
        for sent in results['sentence_analysis']:
            sent_terms = [t['term'] for t in sent['diagnostic_terms']]
            if len(sent_terms) > 1:
                term_list.extend(sent_terms)
        
        if len(set(term_list)) < 2:
            print("Insufficient terms for co-occurrence analysis")
            return
        
        # Simple co-occurrence count
        term_counts = Counter(term_list)
        most_common = term_counts.most_common(10)  # Top 10
        
        plt.figure(figsize=(10, 6))
        terms, counts = zip(*most_common)
        plt.bar(terms, counts, alpha=0.7)
        plt.title('Most Frequent Terms')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()


# ──────────────────────────────
# Driver code - same structure as original
if __name__ == "__main__":

    analyzer = EnhancedPathologyContentAnalyzer()
    
    print("\n" + "="*60)
    print("TESTING WITH EXCEL DATA")
    print("="*60)
    
    try:
        from Generate import test_analyzer_with_excel
        
        results_summary = test_analyzer_with_excel('pathology_reports_dataset.xlsx', analyzer, num_samples=100)
        
        print("\n🎉 Excel pipeline test completed!")
        print("📊 Results saved to 'analyzer_test_results.xlsx'")
        
    except ImportError:
        print("Excel test function not found - skipping Excel test")
    except FileNotFoundError:
        print("Excel file not found - run data generator first")
    except Exception as e:
        print(f"Excel test error: {e}")