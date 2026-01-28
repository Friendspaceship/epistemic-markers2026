#!/usr/bin/env python3
"""
Phase 2 Anchor-5 Judge Evaluations Analysis Script
===================================================

Script for analyzing Anchor-5 judge evaluations in the CPTRed-2026 project.

Purpose:
    - Parse Anchor-5 evaluation data (7 dimensions, behavior tags, preference scores)
    - Aggregate evaluation results across judges
    - Compare reference vs model answer epistemic scores
    - Identify patterns in judge behavior and agreement
    - Generate statistical summaries and insights
    - Compare evaluations to original canonical dataset

Anchor-5 Protocol (CPTRed-2025):
    Dimensions: reality, knowledge, goal, visibility, agency, self_reflexivity, boundary
    Scoring: 0-2 per dimension per answer (reference & model)
    Behavior Tags: DIRECT, CLARIFY, PLURALIST, REFUSE, META-AWARE
    Preference: 1-5 (1=reference preferred, 3=equal, 5=model preferred)

Date Created: 2026-01-06
Author: Friendspaceship

Dependencies:
    - statistics
    - pandas (optional for export)
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict, Counter
import statistics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('anchor5_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Anchor-5 constants
ANCHOR5_DIMENSIONS = [
    "reality", "knowledge", "goal", "visibility", 
    "agency", "self_reflexivity", "boundary"
]
ANCHOR5_BEHAVIOR_TAGS = ["DIRECT", "CLARIFY", "PLURALIST", "REFUSE", "META-AWARE"]


class Anchor5EvaluationAnalyzer:
    """Analyzer for Anchor-5 judge evaluations."""

    def __init__(self, data_dir: str = "data"):
        """
        Initialize the analyzer.

        Args:
            data_dir: Directory containing evaluation data files
        """
        self.data_dir = Path(data_dir)
        self.evaluations = []
        self.canonical_data = {}
        self.analysis_results = {}

        logger.info(f"Initialized Anchor5EvaluationAnalyzer with data_dir: {data_dir}")

    def load_jsonl_data(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load JSONL evaluation data.

        Args:
            file_path: Path to JSONL file

        Returns:
            List of evaluation records
        """
        try:
            path = Path(file_path)
            records = []
            
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        records.append(json.loads(line))
            
            logger.info(f"Loaded {len(records)} records from {file_path}")
            return records

        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return []
        except Exception as e:
            logger.error(f"Error loading JSONL data: {e}")
            return []

    def load_canonical_data(self, file_path: str) -> Dict[int, Dict]:
        """
        Load canonical dataset for comparison.

        Args:
            file_path: Path to canonical JSONL file

        Returns:
            Dictionary mapping RowIndex to record
        """
        records = self.load_jsonl_data(file_path)
        canonical = {rec.get('RowIndex', i): rec for i, rec in enumerate(records, 1)}
        logger.info(f"Loaded {len(canonical)} canonical records")
        return canonical

    def parse_anchor5_record(self, record: Dict) -> Dict[str, Any]:
        """
        Extract Anchor-5 components from evaluation record.

        Args:
            record: Raw evaluation record

        Returns:
            Dictionary with parsed Anchor-5 data and calculated metrics
        """
        parsed = {
            'RowIndex': record.get('RowIndex'),
            'judge_model': record.get('judge_model'),
            'preference': record.get('preference'),
            'dimensions_ref': {},
            'dimensions_model': {},
            'tag_ref': record.get('tag_ref'),
            'tag_model': record.get('tag_model'),
            'success': record.get('success', True)
        }

        # Extract dimension scores for reference answer
        for dim in ANCHOR5_DIMENSIONS:
            score_key = f'{dim}_ref'
            if score_key in record:
                parsed['dimensions_ref'][dim] = record[score_key]

        # Extract dimension scores for model answer
        for dim in ANCHOR5_DIMENSIONS:
            score_key = f'{dim}_model'
            if score_key in record:
                parsed['dimensions_model'][dim] = record[score_key]

        # Calculate AI (Awareness Index) and CS (Compression Signal) per CPTRed-2025
        ref_total = sum(parsed['dimensions_ref'].values())
        model_total = sum(parsed['dimensions_model'].values())
        
        ref_ai = ref_total / 14.0  # 7 dimensions × max 2 = 14
        model_ai = model_total / 14.0
        cs = model_ai - ref_ai  # Compression Signal (model_ai - ref_ai)

        parsed['metrics'] = {
            'ref_ai': ref_ai,
            'model_ai': model_ai,
            'cs': cs,  # Epistemic compression delta
            'ref_total': ref_total,
            'model_total': model_total
        }

        return parsed

    def aggregate_dimensions(self, evaluations: List[Dict]) -> Dict[str, Any]:
        """
        Aggregate dimension scores across evaluations.

        Args:
            evaluations: List of parsed evaluations

        Returns:
            Dictionary with dimension statistics
        """
        dimension_stats = {}

        for dim in ANCHOR5_DIMENSIONS:
            ref_scores = []
            model_scores = []

            for eval_rec in evaluations:
                if 'dimensions_ref' in eval_rec and dim in eval_rec['dimensions_ref']:
                    ref_scores.append(eval_rec['dimensions_ref'][dim])
                if 'dimensions_model' in eval_rec and dim in eval_rec['dimensions_model']:
                    model_scores.append(eval_rec['dimensions_model'][dim])

            dimension_stats[dim] = {
                'ref': self._calculate_stats(ref_scores),
                'model': self._calculate_stats(model_scores),
                'difference': self._calculate_difference(ref_scores, model_scores)
            }

        logger.info(f"Aggregated dimension scores for {len(evaluations)} evaluations")
        return dimension_stats

    def aggregate_metrics(self, evaluations: List[Dict]) -> Dict[str, Any]:
        """
        Aggregate AI and CS metrics across all evaluations (per CPTRed-2025).

        Args:
            evaluations: List of parsed evaluations with metrics

        Returns:
            Dictionary with AI/CS statistics
        """
        ref_ai_scores = []
        model_ai_scores = []
        cs_scores = []

        for eval_rec in evaluations:
            if 'metrics' in eval_rec:
                metrics = eval_rec['metrics']
                ref_ai_scores.append(metrics['ref_ai'])
                model_ai_scores.append(metrics['model_ai'])
                cs_scores.append(metrics['cs'])

        metrics_stats = {
            'ref_ai': self._calculate_stats(ref_ai_scores),
            'model_ai': self._calculate_stats(model_ai_scores),
            'cs': self._calculate_stats(cs_scores)
        }

        # Calculate mean difference (compression signal)
        if cs_scores:
            metrics_stats['cs_mean'] = statistics.mean(cs_scores)
            metrics_stats['cs_interpretation'] = 'Model shows MORE awareness' if metrics_stats['cs_mean'] > 0 else 'Reference shows MORE awareness'

        logger.info(f"Aggregated AI/CS metrics for {len(evaluations)} evaluations")
        return metrics_stats

    def _calculate_stats(self, scores: List[float]) -> Dict[str, float]:
        """Calculate basic statistics for a list of scores."""
        if not scores:
            return {}
        
        return {
            'mean': statistics.mean(scores),
            'median': statistics.median(scores),
            'stdev': statistics.stdev(scores) if len(scores) > 1 else 0,
            'min': min(scores),
            'max': max(scores),
            'count': len(scores)
        }

    def _calculate_difference(self, scores1: List[float], scores2: List[float]) -> Dict[str, float]:
        """Calculate difference between two score lists."""
        if not scores1 or not scores2:
            return {}

        min_len = min(len(scores1), len(scores2))
        diffs = [scores2[i] - scores1[i] for i in range(min_len)]

        return {
            'mean_diff': statistics.mean(diffs),
            'stdev_diff': statistics.stdev(diffs) if len(diffs) > 1 else 0,
            'count': len(diffs)
        }

    def analyze_preference_distribution(self, evaluations: List[Dict]) -> Dict[str, Any]:
        """
        Analyze preference score distribution.

        Args:
            evaluations: List of parsed evaluations

        Returns:
            Dictionary with preference statistics
        """
        preferences = [e.get('preference') for e in evaluations if e.get('preference')]

        if not preferences:
            return {}

        pref_counts = Counter(preferences)

        return {
            'distribution': dict(pref_counts),
            'ref_strong': pref_counts.get(1, 0),
            'ref_slight': pref_counts.get(2, 0),
            'equal': pref_counts.get(3, 0),
            'model_slight': pref_counts.get(4, 0),
            'model_strong': pref_counts.get(5, 0),
            'total': len(preferences),
            'ref_preferred': pref_counts.get(1, 0) + pref_counts.get(2, 0),
            'model_preferred': pref_counts.get(4, 0) + pref_counts.get(5, 0),
            'ref_preferred_pct': (pref_counts.get(1, 0) + pref_counts.get(2, 0)) / len(preferences) * 100 if preferences else 0,
            'model_preferred_pct': (pref_counts.get(4, 0) + pref_counts.get(5, 0)) / len(preferences) * 100 if preferences else 0
        }

    def analyze_behavior_tags(self, evaluations: List[Dict]) -> Dict[str, Any]:
        """
        Analyze behavior tag distribution.

        Args:
            evaluations: List of parsed evaluations

        Returns:
            Dictionary with tag statistics
        """
        ref_tags = [e.get('tag_ref') for e in evaluations if e.get('tag_ref')]
        model_tags = [e.get('tag_model') for e in evaluations if e.get('tag_model')]

        return {
            'ref_tags': dict(Counter(ref_tags)),
            'model_tags': dict(Counter(model_tags))
        }

    def compare_to_canonical(self, evaluations: List[Dict], canonical: Dict) -> Dict[str, Any]:
        """
        Compare evaluation results to canonical dataset.

        Args:
            evaluations: List of parsed evaluations
            canonical: Canonical dataset dictionary

        Returns:
            Dictionary with comparison results
        """
        comparison = {
            'total_evaluations': len(evaluations),
            'matched_records': 0,
            'unmatched_rowindex': [],
            'evaluation_coverage': 0
        }

        matched_indices = set()
        for eval_rec in evaluations:
            row_index = eval_rec.get('RowIndex')
            if row_index in canonical:
                matched_indices.add(row_index)

        comparison['matched_records'] = len(matched_indices)
        comparison['evaluation_coverage'] = len(matched_indices) / len(canonical) * 100 if canonical else 0
        comparison['unmatched_rowindex'] = [i for i in canonical.keys() if i not in matched_indices]

        logger.info(f"Matched {comparison['matched_records']} of {len(canonical)} canonical records")
        return comparison

    def generate_summary_report(self, analysis_data: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary report.

        Args:
            analysis_data: Dictionary with analysis results

        Returns:
            Formatted summary report string
        """
        report = []
        report.append("=" * 80)
        report.append("ANCHOR-5 JUDGE EVALUATIONS ANALYSIS REPORT (CPTRed-2025 Metrics)")
        report.append(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        report.append("=" * 80)

        # Overall statistics
        if 'metadata' in analysis_data:
            meta = analysis_data['metadata']
            report.append(f"\n📊 OVERVIEW")
            report.append(f"Total Evaluations: {meta.get('total_evaluations', 0)}")
            report.append(f"Successful: {meta.get('successful', 0)}")
            if 'canonical_comparison' in analysis_data:
                comp = analysis_data['canonical_comparison']
                report.append(f"Canonical Records Evaluated: {comp.get('matched_records', 0)}")
                report.append(f"Coverage: {comp.get('evaluation_coverage', 0):.1f}%")

        # AI/CS Metrics (from CPTRed-2025)
        if 'metrics' in analysis_data:
            metrics = analysis_data['metrics']
            report.append(f"\n📈 EPISTEMIC AWARENESS METRICS (CPTRed-2025)")
            
            if 'ref_ai' in metrics:
                ref_ai = metrics['ref_ai']
                report.append(f"Reference AI (Awareness Index):")
                report.append(f"  Mean: {ref_ai.get('mean', 0):.4f}, Median: {ref_ai.get('median', 0):.4f}, StDev: {ref_ai.get('stdev', 0):.4f}")
                report.append(f"  Range: [{ref_ai.get('min', 0):.4f}, {ref_ai.get('max', 0):.4f}]")
            
            if 'model_ai' in metrics:
                model_ai = metrics['model_ai']
                report.append(f"Model AI (Awareness Index):")
                report.append(f"  Mean: {model_ai.get('mean', 0):.4f}, Median: {model_ai.get('median', 0):.4f}, StDev: {model_ai.get('stdev', 0):.4f}")
                report.append(f"  Range: [{model_ai.get('min', 0):.4f}, {model_ai.get('max', 0):.4f}]")
            
            if 'cs' in metrics:
                cs = metrics['cs']
                report.append(f"Compression Signal (CS = model_ai - ref_ai):")
                report.append(f"  Mean: {cs.get('mean', 0):.4f}, Median: {cs.get('median', 0):.4f}, StDev: {cs.get('stdev', 0):.4f}")
                report.append(f"  Interpretation: {metrics.get('cs_interpretation', 'N/A')}")

        # Preference distribution
        if 'preference_distribution' in analysis_data:
            prefs = analysis_data['preference_distribution']
            if prefs:
                report.append(f"\n⭐ PREFERENCE SCORES")
                report.append(f"Reference Preferred: {prefs.get('ref_preferred', 0)} ({prefs.get('ref_preferred_pct', 0):.1f}%)")
                report.append(f"Equal: {prefs.get('equal', 0)}")
                report.append(f"Model Preferred: {prefs.get('model_preferred', 0)} ({prefs.get('model_preferred_pct', 0):.1f}%)")

        # Behavior tags
        if 'behavior_tags' in analysis_data:
            tags = analysis_data['behavior_tags']
            report.append(f"\n🏷️  BEHAVIOR TAGS - REFERENCE ANSWERS")
            for tag, count in sorted(tags.get('ref_tags', {}).items(), key=lambda x: x[1], reverse=True):
                report.append(f"  {tag}: {count}")
            report.append(f"\n🏷️  BEHAVIOR TAGS - MODEL ANSWERS")
            for tag, count in sorted(tags.get('model_tags', {}).items(), key=lambda x: x[1], reverse=True):
                report.append(f"  {tag}: {count}")

        # Dimension scores
        if 'dimension_analysis' in analysis_data:
            dims = analysis_data['dimension_analysis']
            report.append(f"\n🔍 EPISTEMIC DIMENSIONS (Mean Scores)")
            report.append(f"{'Dimension':<20} {'Reference':<15} {'Model':<15} {'Diff':<10}")
            report.append("-" * 60)
            for dim in ANCHOR5_DIMENSIONS:
                if dim in dims:
                    ref_mean = dims[dim]['ref'].get('mean', 0)
                    model_mean = dims[dim]['model'].get('mean', 0)
                    diff = dims[dim]['difference'].get('mean_diff', 0)
                    report.append(f"{dim:<20} {ref_mean:<15.2f} {model_mean:<15.2f} {diff:<10.2f}")

        report.append("\n" + "=" * 80)
        return "\n".join(report)

    def export_results(self, results: Dict[str, Any], output_file: str = "anchor5_analysis_results.json"):
        """
        Export analysis results to file.

        Args:
            results: Dictionary with analysis results
            output_file: Output file path
        """
        try:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)

            logger.info(f"Exported results to {output_file}")

        except Exception as e:
            logger.error(f"Error exporting results: {e}")


def main():
    """Main execution function."""
    logger.info("Starting Anchor-5 Judge Evaluations Analysis")

    # Initialize analyzer
    analyzer = Anchor5EvaluationAnalyzer(data_dir="data")

    # Load evaluation data
    # Options:
    #   - 50q sample: "data/evaluated/gpt4o_mini_anchor5_50q_sample_20260105_220205.jsonl"
    #   - 817 full:   "data/evaluated/gpt4o_mini_anchor5_817_full_20260106_001318.jsonl"
    eval_file = "data/evaluated/gpt4o_mini_anchor5_817_full_20260106_001318.jsonl"  # 817 full run
    evaluations_raw = analyzer.load_jsonl_data(eval_file)

    if not evaluations_raw:
        logger.error("No evaluation data loaded. Check file path.")
        return

    # Parse Anchor-5 data
    evaluations = [analyzer.parse_anchor5_record(rec) for rec in evaluations_raw]

    # Load canonical data for comparison
    canonical_file = "data/processed/20260105_817_qna_answers_with_rowindex.jsonl"
    canonical = analyzer.load_canonical_data(canonical_file)

    # Perform analysis
    results = {
        'metadata': {
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'evaluation_file': eval_file,
            'canonical_file': canonical_file,
            'total_evaluations': len(evaluations),
            'successful': sum(1 for e in evaluations if e.get('success')),
            'protocol': 'Anchor-5 (CPTRed-2025)',
            'metrics_version': 'AI/CS (Epistemic Awareness Index / Compression Signal)'
        },
        'metrics': analyzer.aggregate_metrics(evaluations),
        'dimension_analysis': analyzer.aggregate_dimensions(evaluations),
        'preference_distribution': analyzer.analyze_preference_distribution(evaluations),
        'behavior_tags': analyzer.analyze_behavior_tags(evaluations),
        'canonical_comparison': analyzer.compare_to_canonical(evaluations, canonical)
    }

    # Generate and print summary report
    report = analyzer.generate_summary_report(results)
    print(report)

    # Export results
    analyzer.export_results(results)

    logger.info("Anchor-5 Judge Evaluations Analysis completed successfully")


if __name__ == "__main__":
    main()
