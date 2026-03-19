#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Beautiful Bag Area Visualization
Based on accurate HTML coordinates analysis with enhanced visual design
"""

import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from PIL import Image, ImageDraw, ImageFont

class BeautifulBagVisualizer:
    def __init__(self, data_dir="."):
        self.data_dir = data_dir
        self.group1_fixations = []
        self.group2_fixations = []
        self.group1_gaze = []
        self.group2_gaze = []
        
        # HTML-based bag area coordinates (from final_with_neg.html)
        self.container_width = 600
        self.container_height = 400
        
        # Bag area percentages from HTML
        self.bag_area_percentages = {
            'x_percent': 0.54,      # 54%
            'y_percent': 0.55,      # 55%
            'width_percent': 0.31,  # 31%
            'height_percent': 0.45  # 45%
        }
        
        # Calculate bag areas for different container sizes
        self.bag_areas = {
            '600x400': self.calculate_bag_area(600, 400),
            '800x600': self.calculate_bag_area(800, 600),
            '1200x800': self.calculate_bag_area(1200, 800),
            '1000x600': self.calculate_bag_area(1000, 600)
        }
        
        # Set up beautiful plotting style
        self.setup_plotting_style()
    
    def setup_plotting_style(self):
        """Set up beautiful plotting style"""
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Custom color palette
        self.colors = {
            'group1': '#2E8B57',  # Sea Green
            'group2': '#FF6B6B',  # Coral Red
            'bag_area': '#4ECDC4', # Turquoise
            'background': '#F7F7F7',
            'text': '#2C3E50'
        }
        
        # Set font properties
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
        plt.rcParams['font.size'] = 12
        plt.rcParams['axes.titlesize'] = 16
        plt.rcParams['axes.labelsize'] = 14
    
    def calculate_bag_area(self, width, height):
        """Calculate bag area for given container dimensions"""
        return {
            'x_min': int(width * self.bag_area_percentages['x_percent']),
            'x_max': int(width * (self.bag_area_percentages['x_percent'] + self.bag_area_percentages['width_percent'])),
            'y_min': int(height * self.bag_area_percentages['y_percent']),
            'y_max': int(height * (self.bag_area_percentages['y_percent'] + self.bag_area_percentages['height_percent']))
        }
    
    def load_data(self):
        """Load fixation and gaze data"""
        print("Loading data with beautiful visualization...")
        
        # Group 1: Negative feedback group (101, 102)
        group1_files = ['101_fixations.csv', '102_fixations.csv']
        for file in group1_files:
            file_path = os.path.join(self.data_dir, file)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            self.group1_fixations.append({
                                'duration': int(row['duration']),
                                'x': float(row['x']),
                                'y': float(row['y']),
                                'participant': file.split('_')[0]
                            })
                    print(f"✓ Loaded {file}: {len([f for f in self.group1_fixations if f['participant'] == file.split('_')[0]])} fixations")
                except Exception as e:
                    print(f"✗ Failed to load {file}: {e}")
        
        # Group 2: No negative feedback group (201, 202)
        group2_files = ['201_fixations.csv', '202_fixations.csv']
        for file in group2_files:
            file_path = os.path.join(self.data_dir, file)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            self.group2_fixations.append({
                                'duration': int(row['duration']),
                                'x': float(row['x']),
                                'y': float(row['y']),
                                'participant': file.split('_')[0]
                            })
                    print(f"✓ Loaded {file}: {len([f for f in self.group2_fixations if f['participant'] == file.split('_')[0]])} fixations")
                except Exception as e:
                    print(f"✗ Failed to load {file}: {e}")
        
        # Load gaze data
        group1_gaze_files = ['101_gaze_data.csv', '102_gaze_data.csv']
        for file in group1_gaze_files:
            file_path = os.path.join(self.data_dir, file)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            self.group1_gaze.append({
                                'x': float(row['x']),
                                'y': float(row['y']),
                                'participant': file.split('_')[0]
                            })
                    print(f"✓ Loaded {file}: {len([g for g in self.group1_gaze if g['participant'] == file.split('_')[0]])} gaze points")
                except Exception as e:
                    print(f"✗ Failed to load {file}: {e}")
        
        group2_gaze_files = ['201_gaze_data.csv', '202_gaze_data.csv']
        for file in group2_gaze_files:
            file_path = os.path.join(self.data_dir, file)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            self.group2_gaze.append({
                                'x': float(row['x']),
                                'y': float(row['y']),
                                'participant': file.split('_')[0]
                            })
                    print(f"✓ Loaded {file}: {len([g for g in self.group2_gaze if g['participant'] == file.split('_')[0]])} gaze points")
                except Exception as e:
                    print(f"✗ Failed to load {file}: {e}")
    
    def is_in_bag_area(self, x, y, bag_area):
        """Check if coordinates are within bag area"""
        return (bag_area['x_min'] <= x <= bag_area['x_max'] and 
                bag_area['y_min'] <= y <= bag_area['y_max'])
    
    def analyze_container_size(self, size_name, bag_area):
        """Analyze data for a specific container size"""
        # Filter bag area fixations
        group1_bag_fixations = [f for f in self.group1_fixations if self.is_in_bag_area(f['x'], f['y'], bag_area)]
        group2_bag_fixations = [f for f in self.group2_fixations if self.is_in_bag_area(f['x'], f['y'], bag_area)]
        
        # Filter bag area gaze points
        group1_bag_gaze = [g for g in self.group1_gaze if self.is_in_bag_area(g['x'], g['y'], bag_area)]
        group2_bag_gaze = [g for g in self.group2_gaze if self.is_in_bag_area(g['x'], g['y'], bag_area)]
        
        return {
            'size_name': size_name,
            'bag_area': bag_area,
            'group1_bag_fixations': group1_bag_fixations,
            'group2_bag_fixations': group2_bag_fixations,
            'group1_bag_gaze': group1_bag_gaze,
            'group2_bag_gaze': group2_bag_gaze,
            'group1_total_fixations': len(self.group1_fixations),
            'group2_total_fixations': len(self.group2_fixations),
            'group1_total_gaze': len(self.group1_gaze),
            'group2_total_gaze': len(self.group2_gaze)
        }
    
    def create_beautiful_visualizations(self):
        """Create beautiful visualizations for all container sizes"""
        print("\nCreating beautiful bag area visualizations...")
        
        # Analyze all container sizes
        analyses = {}
        for size_name, bag_area in self.bag_areas.items():
            analyses[size_name] = self.analyze_container_size(size_name, bag_area)
        
        # 1. Multi-size comparison dashboard
        self.create_multi_size_dashboard(analyses)
        
        # 2. Focus on 1200x800 (most relevant for heatmaps)
        self.create_focused_analysis(analyses['1200x800'])
        
        # 3. Statistical comparison
        self.create_statistical_comparison(analyses)
        
        # 4. Bag area location visualization
        self.create_bag_location_visualization(analyses['1200x800'])
        
        # 5. Duration distribution analysis
        self.create_duration_analysis(analyses['1200x800'])
        
        print("\n✓ All beautiful visualizations created!")
    
    def create_multi_size_dashboard(self, analyses):
        """Create a comprehensive dashboard comparing all container sizes"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Bag Area Analysis - Multi-Container Size Comparison', fontsize=20, fontweight='bold', color=self.colors['text'])
        
        # Prepare data
        sizes = list(analyses.keys())
        group1_fix_ratios = []
        group2_fix_ratios = []
        group1_durations = []
        group2_durations = []
        
        for size_name in sizes:
            analysis = analyses[size_name]
            g1_ratio = len(analysis['group1_bag_fixations']) / analysis['group1_total_fixations']
            g2_ratio = len(analysis['group2_bag_fixations']) / analysis['group2_total_fixations']
            group1_fix_ratios.append(g1_ratio * 100)
            group2_fix_ratios.append(g2_ratio * 100)
            
            g1_duration = sum([f['duration'] for f in analysis['group1_bag_fixations']])
            g2_duration = sum([f['duration'] for f in analysis['group2_bag_fixations']])
            group1_durations.append(g1_duration)
            group2_durations.append(g2_duration)
        
        # 1. Fixation ratio comparison
        x = np.arange(len(sizes))
        width = 0.35
        
        axes[0, 0].bar(x - width/2, group1_fix_ratios, width, label='Group 1 (Negative Feedback)', 
                      color=self.colors['group1'], alpha=0.8)
        axes[0, 0].bar(x + width/2, group2_fix_ratios, width, label='Group 2 (No Negative Feedback)', 
                      color=self.colors['group2'], alpha=0.8)
        
        axes[0, 0].set_xlabel('Container Size')
        axes[0, 0].set_ylabel('Bag Fixation Ratio (%)')
        axes[0, 0].set_title('Bag Fixation Ratio by Container Size')
        axes[0, 0].set_xticks(x)
        axes[0, 0].set_xticklabels(sizes)
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Total duration comparison
        axes[0, 1].bar(x - width/2, group1_durations, width, label='Group 1 (Negative Feedback)', 
                      color=self.colors['group1'], alpha=0.8)
        axes[0, 1].bar(x + width/2, group2_durations, width, label='Group 2 (No Negative Feedback)', 
                      color=self.colors['group2'], alpha=0.8)
        
        axes[0, 1].set_xlabel('Container Size')
        axes[0, 1].set_ylabel('Total Bag Fixation Duration (ms)')
        axes[0, 1].set_title('Total Bag Fixation Duration by Container Size')
        axes[0, 1].set_xticks(x)
        axes[0, 1].set_xticklabels(sizes)
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Fixation count comparison
        group1_counts = [len(analyses[size]['group1_bag_fixations']) for size in sizes]
        group2_counts = [len(analyses[size]['group2_bag_fixations']) for size in sizes]
        
        axes[1, 0].bar(x - width/2, group1_counts, width, label='Group 1 (Negative Feedback)', 
                      color=self.colors['group1'], alpha=0.8)
        axes[1, 0].bar(x + width/2, group2_counts, width, label='Group 2 (No Negative Feedback)', 
                      color=self.colors['group2'], alpha=0.8)
        
        axes[1, 0].set_xlabel('Container Size')
        axes[1, 0].set_ylabel('Number of Bag Fixations')
        axes[1, 0].set_title('Bag Fixation Count by Container Size')
        axes[1, 0].set_xticks(x)
        axes[1, 0].set_xticklabels(sizes)
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Average duration comparison
        group1_avg_durations = []
        group2_avg_durations = []
        
        for size in sizes:
            analysis = analyses[size]
            g1_avg = np.mean([f['duration'] for f in analysis['group1_bag_fixations']]) if analysis['group1_bag_fixations'] else 0
            g2_avg = np.mean([f['duration'] for f in analysis['group2_bag_fixations']]) if analysis['group2_bag_fixations'] else 0
            group1_avg_durations.append(g1_avg)
            group2_avg_durations.append(g2_avg)
        
        axes[1, 1].bar(x - width/2, group1_avg_durations, width, label='Group 1 (Negative Feedback)', 
                      color=self.colors['group1'], alpha=0.8)
        axes[1, 1].bar(x + width/2, group2_avg_durations, width, label='Group 2 (No Negative Feedback)', 
                      color=self.colors['group2'], alpha=0.8)
        
        axes[1, 1].set_xlabel('Container Size')
        axes[1, 1].set_ylabel('Average Bag Fixation Duration (ms)')
        axes[1, 1].set_title('Average Bag Fixation Duration by Container Size')
        axes[1, 1].set_xticks(x)
        axes[1, 1].set_xticklabels(sizes)
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('beautiful_multi_size_dashboard.png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.show()
    
    def create_focused_analysis(self, analysis):
        """Create focused analysis for 1200x800 container"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Focused Bag Area Analysis (1200x800 Container)', fontsize=18, fontweight='bold', color=self.colors['text'])
        
        # 1. Fixation count comparison
        groups = ['Group 1\n(Negative Feedback)', 'Group 2\n(No Negative Feedback)']
        bag_counts = [len(analysis['group1_bag_fixations']), len(analysis['group2_bag_fixations'])]
        total_counts = [analysis['group1_total_fixations'], analysis['group2_total_fixations']]
        non_bag_counts = [total - bag for total, bag in zip(total_counts, bag_counts)]
        
        x = np.arange(len(groups))
        width = 0.35
        
        axes[0, 0].bar(x - width/2, bag_counts, width, label='Bag Fixations', 
                      color=self.colors['bag_area'], alpha=0.8)
        axes[0, 0].bar(x + width/2, non_bag_counts, width, label='Non-Bag Fixations', 
                      color='#95A5A6', alpha=0.8)
        
        axes[0, 0].set_xlabel('Experimental Group')
        axes[0, 0].set_ylabel('Number of Fixations')
        axes[0, 0].set_title('Bag vs Non-Bag Fixation Counts')
        axes[0, 0].set_xticks(x)
        axes[0, 0].set_xticklabels(groups)
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Fixation ratio
        bag_ratios = [len(analysis['group1_bag_fixations']) / analysis['group1_total_fixations'] * 100,
                     len(analysis['group2_bag_fixations']) / analysis['group2_total_fixations'] * 100]
        
        bars = axes[0, 1].bar(groups, bag_ratios, color=[self.colors['group1'], self.colors['group2']], alpha=0.8)
        axes[0, 1].set_ylabel('Bag Fixation Ratio (%)')
        axes[0, 1].set_title('Bag Fixation Ratio by Group')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Add percentage labels
        for bar, ratio in zip(bars, bag_ratios):
            height = bar.get_height()
            axes[0, 1].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                           f'{ratio:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # 3. Total duration comparison
        group1_total_duration = sum([f['duration'] for f in analysis['group1_bag_fixations']])
        group2_total_duration = sum([f['duration'] for f in analysis['group2_bag_fixations']])
        
        bars = axes[1, 0].bar(groups, [group1_total_duration, group2_total_duration], 
                             color=[self.colors['group1'], self.colors['group2']], alpha=0.8)
        axes[1, 0].set_ylabel('Total Bag Fixation Duration (ms)')
        axes[1, 0].set_title('Total Bag Fixation Duration by Group')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Add duration labels
        for bar, duration in zip(bars, [group1_total_duration, group2_total_duration]):
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width()/2., height + 500,
                           f'{duration:,.0f}ms', ha='center', va='bottom', fontweight='bold')
        
        # 4. Average duration
        group1_avg_duration = np.mean([f['duration'] for f in analysis['group1_bag_fixations']]) if analysis['group1_bag_fixations'] else 0
        group2_avg_duration = np.mean([f['duration'] for f in analysis['group2_bag_fixations']]) if analysis['group2_bag_fixations'] else 0
        
        bars = axes[1, 1].bar(groups, [group1_avg_duration, group2_avg_duration], 
                             color=[self.colors['group1'], self.colors['group2']], alpha=0.8)
        axes[1, 1].set_ylabel('Average Bag Fixation Duration (ms)')
        axes[1, 1].set_title('Average Bag Fixation Duration by Group')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Add average labels
        for bar, avg_duration in zip(bars, [group1_avg_duration, group2_avg_duration]):
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 5,
                           f'{avg_duration:.0f}ms', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('beautiful_focused_analysis.png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.show()
    
    def create_statistical_comparison(self, analyses):
        """Create statistical comparison visualization"""
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle('Statistical Comparison of Bag Area Fixations', fontsize=18, fontweight='bold', color=self.colors['text'])
        
        # Prepare data for 1200x800 analysis
        analysis = analyses['1200x800']
        group1_durations = [f['duration'] for f in analysis['group1_bag_fixations']]
        group2_durations = [f['duration'] for f in analysis['group2_bag_fixations']]
        
        # 1. Duration distribution histogram
        axes[0].hist(group1_durations, bins=20, alpha=0.7, density=True, 
                    label='Group 1 (Negative Feedback)', color=self.colors['group1'])
        axes[0].hist(group2_durations, bins=20, alpha=0.7, density=True, 
                    label='Group 2 (No Negative Feedback)', color=self.colors['group2'])
        axes[0].set_xlabel('Bag Fixation Duration (ms)')
        axes[0].set_ylabel('Density')
        axes[0].set_title('Bag Fixation Duration Distribution')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # 2. Box plot
        data_to_plot = [group1_durations, group2_durations]
        bp = axes[1].boxplot(data_to_plot, labels=['Group 1\n(Negative Feedback)', 'Group 2\n(No Negative Feedback)'], 
                           patch_artist=True)
        
        # Color the boxes
        colors = [self.colors['group1'], self.colors['group2']]
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        axes[1].set_ylabel('Bag Fixation Duration (ms)')
        axes[1].set_title('Bag Fixation Duration Distribution')
        axes[1].grid(True, alpha=0.3)
        
        # Add statistical test results
        if group1_durations and group2_durations:
            stat, p_value = stats.mannwhitneyu(group1_durations, group2_durations, alternative='two-sided')
            axes[1].text(0.5, 0.95, f'Mann-Whitney U Test\np-value: {p_value:.4f}\nSignificant: {"Yes" if p_value < 0.05 else "No"}', 
                        transform=axes[1].transAxes, ha='center', va='top', 
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('beautiful_statistical_comparison.png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.show()
    
    def create_bag_location_visualization(self, analysis):
        """Create bag area location visualization"""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        # Plot bag fixations for each participant
        for participant_id in ['101', '102', '201', '202']:
            if participant_id in ['101', '102']:
                group_fixations = analysis['group1_bag_fixations']
                color = self.colors['group1']
                group_name = 'Negative Feedback'
            else:
                group_fixations = analysis['group2_bag_fixations']
                color = self.colors['group2']
                group_name = 'No Negative Feedback'
            
            participant_fixations = [f for f in group_fixations if f['participant'] == participant_id]
            
            if participant_fixations:
                x_coords = [f['x'] for f in participant_fixations]
                y_coords = [f['y'] for f in participant_fixations]
                sizes = [f['duration']/10 for f in participant_fixations]
                
                ax.scatter(x_coords, y_coords, c=color, s=sizes, alpha=0.7, 
                          label=f"{participant_id} ({group_name})", edgecolors='white', linewidth=0.5)
        
        # Highlight bag area
        bag_area = analysis['bag_area']
        bag_x = [bag_area['x_min'], bag_area['x_max'], bag_area['x_max'], bag_area['x_min'], bag_area['x_min']]
        bag_y = [bag_area['y_min'], bag_area['y_min'], bag_area['y_max'], bag_area['y_max'], bag_area['y_min']]
        ax.plot(bag_x, bag_y, color=self.colors['bag_area'], linewidth=3, label='Bag Area Boundary')
        ax.fill(bag_x, bag_y, alpha=0.1, color=self.colors['bag_area'])
        
        ax.set_xlabel('X Coordinate (pixels)')
        ax.set_ylabel('Y Coordinate (pixels)')
        ax.set_title('Bag Fixations Location Distribution (1200x800 Container)')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        # Add bag area info
        ax.text(0.02, 0.98, f"Bag Area: X({bag_area['x_min']}-{bag_area['x_max']}), Y({bag_area['y_min']}-{bag_area['y_max']})", 
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('beautiful_bag_location_visualization.png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.show()
    
    def create_duration_analysis(self, analysis):
        """Create detailed duration analysis"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Detailed Bag Fixation Duration Analysis', fontsize=18, fontweight='bold', color=self.colors['text'])
        
        group1_durations = [f['duration'] for f in analysis['group1_bag_fixations']]
        group2_durations = [f['duration'] for f in analysis['group2_bag_fixations']]
        
        # 1. Duration histogram with KDE
        axes[0, 0].hist(group1_durations, bins=15, alpha=0.7, density=True, 
                       label='Group 1 (Negative Feedback)', color=self.colors['group1'])
        axes[0, 0].hist(group2_durations, bins=15, alpha=0.7, density=True, 
                       label='Group 2 (No Negative Feedback)', color=self.colors['group2'])
        axes[0, 0].set_xlabel('Duration (ms)')
        axes[0, 0].set_ylabel('Density')
        axes[0, 0].set_title('Bag Fixation Duration Distribution')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Cumulative distribution
        if group1_durations and group2_durations:
            sorted_g1 = np.sort(group1_durations)
            sorted_g2 = np.sort(group2_durations)
            y1 = np.arange(1, len(sorted_g1) + 1) / len(sorted_g1)
            y2 = np.arange(1, len(sorted_g2) + 1) / len(sorted_g2)
            
            axes[0, 1].plot(sorted_g1, y1, label='Group 1 (Negative Feedback)', 
                           color=self.colors['group1'], linewidth=2)
            axes[0, 1].plot(sorted_g2, y2, label='Group 2 (No Negative Feedback)', 
                           color=self.colors['group2'], linewidth=2)
            axes[0, 1].set_xlabel('Duration (ms)')
            axes[0, 1].set_ylabel('Cumulative Probability')
            axes[0, 1].set_title('Cumulative Duration Distribution')
            axes[0, 1].legend()
            axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Duration statistics
        stats_data = []
        if group1_durations:
            stats_data.append(['Group 1', np.mean(group1_durations), np.median(group1_durations), 
                             np.std(group1_durations), np.min(group1_durations), np.max(group1_durations)])
        if group2_durations:
            stats_data.append(['Group 2', np.mean(group2_durations), np.median(group2_durations), 
                             np.std(group2_durations), np.min(group2_durations), np.max(group2_durations)])
        
        if stats_data:
            stats_table = axes[1, 0].table(cellText=stats_data,
                                          colLabels=['Group', 'Mean', 'Median', 'Std', 'Min', 'Max'],
                                          cellLoc='center',
                                          loc='center')
            stats_table.auto_set_font_size(False)
            stats_table.set_fontsize(10)
            stats_table.scale(1, 2)
            axes[1, 0].set_title('Duration Statistics')
            axes[1, 0].axis('off')
        
        # 4. Duration vs count scatter
        if group1_durations and group2_durations:
            axes[1, 1].scatter(range(len(group1_durations)), group1_durations, 
                              alpha=0.6, label='Group 1 (Negative Feedback)', color=self.colors['group1'])
            axes[1, 1].scatter(range(len(group2_durations)), group2_durations, 
                              alpha=0.6, label='Group 2 (No Negative Feedback)', color=self.colors['group2'])
            axes[1, 1].set_xlabel('Fixation Index')
            axes[1, 1].set_ylabel('Duration (ms)')
            axes[1, 1].set_title('Individual Fixation Durations')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('beautiful_duration_analysis.png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.show()
    
    def run_analysis(self):
        """Run complete beautiful bag area analysis"""
        print("=" * 80)
        print("BEAUTIFUL BAG AREA VISUALIZATION")
        print("Based on HTML coordinates from final_with_neg.html")
        print("=" * 80)
        
        # Load data
        self.load_data()
        
        # Create beautiful visualizations
        self.create_beautiful_visualizations()
        
        print("\n" + "=" * 80)
        print("BEAUTIFUL VISUALIZATION COMPLETE!")
        print("Generated files:")
        print("- beautiful_multi_size_dashboard.png")
        print("- beautiful_focused_analysis.png")
        print("- beautiful_statistical_comparison.png")
        print("- beautiful_bag_location_visualization.png")
        print("- beautiful_duration_analysis.png")
        print("=" * 80)

def main():
    visualizer = BeautifulBagVisualizer()
    visualizer.run_analysis()

if __name__ == "__main__":
    main() 