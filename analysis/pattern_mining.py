"""
Pattern mining module for analyzing communication patterns in the game.
"""
from collections import defaultdict
import numpy as np
from typing import Dict, List, Tuple

class PatternAnalyzer:
    def __init__(self):
        self.patterns = defaultdict(list)
        self.response_metrics = defaultdict(list)
        
    def analyze_response(self, player: str, response: str) -> Dict:
        """Analyze a single response for various metrics."""
        metrics = {
            'length': len(response),
            'words': len(response.split()),
            'sentences': len(response.split('.')),
            'avg_word_length': np.mean([len(word) for word in response.split()]),
            'punctuation_count': sum(1 for char in response if char in '.,!?;'),
            'capitalization_ratio': sum(1 for char in response if char.isupper()) / len(response) if response else 0,
            'has_emoji': any(char for char in response if char in '😊🤔😂👍🎭🎯'),
        }
        
        self.response_metrics[player].append(metrics)
        return metrics

    def extract_frequent_patterns(self) -> Dict[str, Dict]:
        """Extract frequent patterns from all responses."""
        all_patterns = {}
        
        for player, metrics_list in self.response_metrics.items():
            if not metrics_list:
                continue
                
            avg_metrics = {
                'avg_response_length': np.mean([m['length'] for m in metrics_list]),
                'avg_words_per_response': np.mean([m['words'] for m in metrics_list]),
                'avg_sentences': np.mean([m['sentences'] for m in metrics_list]),
                'avg_word_length': np.mean([m['avg_word_length'] for m in metrics_list]),
                'punctuation_density': np.mean([m['punctuation_count'] for m in metrics_list]),
                'capitalization_consistency': np.std([m['capitalization_ratio'] for m in metrics_list]),
                'emoji_usage': np.mean([m['has_emoji'] for m in metrics_list]),
            }
            
            # Identify key behavioral patterns
            patterns = {
                'verbosity': 'high' if avg_metrics['avg_words_per_response'] > 30 else 'low',
                'formality': 'high' if avg_metrics['punctuation_density'] > 0.1 else 'low',
                'consistency': 'high' if avg_metrics['capitalization_consistency'] < 0.1 else 'low',
                'expressiveness': 'high' if avg_metrics['emoji_usage'] > 0.3 else 'low'
            }
            
            all_patterns[player] = {
                'metrics': avg_metrics,
                'patterns': patterns
            }
            
        return all_patterns

    def generate_summary(self) -> str:
        """Generate a summary of the communication patterns."""
        patterns = self.extract_frequent_patterns()
        
        summary = "Communication Patterns Observed.\n\n"
        
        for player, data in patterns.items():
            metrics = data['metrics']
            behavior = data['patterns']
            
            summary += f"Player: {player}\n"
            summary += "=" * (len(player) + 8) + "\n"
            summary += f"Response Style:\n"
            summary += f"- Average response length: {metrics['avg_response_length']:.1f} characters\n"
            summary += f"- Words per response: {metrics['avg_words_per_response']:.1f}\n"
            summary += f"- Sentence complexity: {metrics['avg_sentences']:.1f} sentences/response\n\n"
            
            summary += "Behavioral Patterns:\n"
            summary += f"- Verbosity: {behavior['verbosity']}\n"
            summary += f"- Formality: {behavior['formality']}\n"
            summary += f"- Consistency: {behavior['consistency']}\n"
            summary += f"- Expressiveness: {behavior['expressiveness']}\n\n"
            
        return summary

    def clear(self):
        """Clear all stored patterns and metrics."""
        self.patterns.clear()
        self.response_metrics.clear()
