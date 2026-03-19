#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Group Heatmap Analysis
Creates heatmaps with HTML layout and enhanced color gradients
"""

import csv
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

class EnhancedGroupHeatmapAnalyzer:
    def __init__(self, data_dir="."):
        self.data_dir = data_dir
        self.group1_data = []  # Negative feedback group (101, 102)
        self.group2_data = []  # No negative feedback group (201, 202)
        self.page_dimensions = None
        
    def load_group_data(self):
        """Load gaze data for both groups"""
        print("Loading group data...")
        
        # Group 1: Negative feedback group (101, 102)
        group1_files = ['101_gaze_data.csv', '102_gaze_data.csv']
        for file in group1_files:
            file_path = os.path.join(self.data_dir, file)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            self.group1_data.append({
                                'timestamp': float(row['timestamp']),
                                'sessionTime': int(row['sessionTime']),
                                'x': float(row['x']),
                                'y': float(row['y']),
                                'confidence': int(row['confidence']),
                                'participant': file.split('_')[0]
                            })
                    print(f"✓ Loaded {file}: {len([d for d in self.group1_data if d['participant'] == file.split('_')[0]])} points")
                except Exception as e:
                    print(f"✗ Failed to load {file}: {e}")
        
        # Group 2: No negative feedback group (201, 202)
        group2_files = ['201_gaze_data.csv', '202_gaze_data.csv']
        for file in group2_files:
            file_path = os.path.join(self.data_dir, file)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            self.group2_data.append({
                                'timestamp': float(row['timestamp']),
                                'sessionTime': int(row['sessionTime']),
                                'x': float(row['x']),
                                'y': float(row['y']),
                                'confidence': int(row['confidence']),
                                'participant': file.split('_')[0]
                            })
                    print(f"✓ Loaded {file}: {len([d for d in self.group2_data if d['participant'] == file.split('_')[0]])} points")
                except Exception as e:
                    print(f"✗ Failed to load {file}: {e}")
        
        print(f"✓ Group 1 (Negative feedback): {len(self.group1_data)} total points")
        print(f"✓ Group 2 (No negative feedback): {len(self.group2_data)} total points")
        
        return len(self.group1_data) > 0 and len(self.group2_data) > 0
    
    def analyze_page_dimensions(self):
        """Analyze page dimensions across all data"""
        print("\n=== Page Dimensions Analysis ===")
        
        all_data = self.group1_data + self.group2_data
        if not all_data:
            print("✗ No data available")
            return None
            
        x_coords = [point['x'] for point in all_data]
        y_coords = [point['y'] for point in all_data]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        self.page_dimensions = {
            'width': x_max - x_min,
            'height': y_max - y_min,
            'x_min': x_min,
            'x_max': x_max,
            'y_min': y_min,
            'y_max': y_max
        }
        
        print(f"Overall gaze data range:")
        print(f"  X: {x_min:.2f} - {x_max:.2f}")
        print(f"  Y: {y_min:.2f} - {y_max:.2f}")
        print(f"  Area: {self.page_dimensions['width']:.2f} × {self.page_dimensions['height']:.2f} pixels")
        
        return self.page_dimensions
    
    def create_html_background(self, width=1200, height=800):
        """Create HTML-like background similar to the original heatmap"""
        print("Creating HTML background...")
        
        # Create base image with gradient background
        img = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Create gradient background like HTML body
        for y in range(height):
            intensity = int(255 - (y / height) * 30)
            color = (intensity, intensity, intensity)
            draw.line([(0, y), (width, y)], fill=color)
        
        # Calculate positions based on HTML layout
        body_padding = 20
        container_padding = 20
        container_width = 1000
        
        # Main container (centered)
        container_x = body_padding
        container_y = body_padding
        container_w = container_width
        container_h = height - (body_padding * 2)
        
        # Container with shadow effect (like HTML)
        draw.rectangle([(container_x+3, container_y+3), (container_x + container_w+3, container_y + container_h+3)], 
                      fill=(200, 200, 200))
        draw.rectangle([(container_x, container_y), (container_x + container_w, container_y + container_h)], 
                      fill=(255, 255, 255), outline=(220, 220, 220), width=1)
        
        # Header area
        header_y = container_y + container_padding
        header_h = 80
        
        # Header background
        draw.rectangle([(container_x + container_padding, header_y), 
                       (container_x + container_w - container_padding, header_y + header_h)], 
                      fill=(245, 245, 245), outline=(230, 230, 230), width=1)
        
        # Calibration area (main content area)
        calib_x = container_x + (container_w - 600) // 2
        calib_y = header_y + header_h + container_padding
        calib_w = 600
        calib_h = 400
        
        # Calibration area background (white with border)
        draw.rectangle([(calib_x, calib_y), (calib_x + calib_w, calib_y + calib_h)], 
                      fill=(255, 255, 255), outline=(100, 100, 100), width=2)
        
        # Add calibration area label
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 14)
        except:
            font = ImageFont.load_default()
        
        draw.text((calib_x + 10, calib_y + 10), "Eye-Tracking Calibration Area", fill=(100, 100, 100), font=font)
        
        # Bag detection area (based on HTML percentages)
        bag_x = calib_x + (calib_w * 0.54)
        bag_y = calib_y + (calib_h * 0.55)  # 55% from top
        bag_w = calib_w * 0.31
        bag_h = calib_h * 0.45
        
        # Bag area visualization (semi-transparent green)
        bag_color = (0, 255, 0, 100)  # Semi-transparent green
        bag_overlay = Image.new('RGBA', (int(bag_w), int(bag_h)), bag_color)
        img.paste(bag_overlay, (int(bag_x), int(bag_y)), bag_overlay)
        
        # Bag area border
        draw.rectangle([(int(bag_x), int(bag_y)), (int(bag_x + bag_w), int(bag_y + bag_h))], 
                      outline=(0, 200, 0), width=2)
        
        # Add to cart button area (below calibration area)
        button_x = calib_x + (calib_w - 250) // 2
        button_y = calib_y + calib_h + container_padding
        button_w = 250
        button_h = 50
        
        # Button with gradient (like HTML)
        for i in range(button_h):
            intensity = int(255 - (i / button_h) * 30)
            color = (255, intensity, intensity)
            draw.line([(button_x, button_y + i), (button_x + button_w, button_y + i)], fill=color)
        
        # Button border
        draw.rectangle([(button_x, button_y), (button_x + button_w, button_y + button_h)], 
                      outline=(200, 50, 50), width=2)
        
        # Add button label
        draw.text((button_x + 10, button_y + 15), "Add to Cart", fill=(255, 255, 255), font=font)
        
        return img, {
            'calib_x': calib_x,
            'calib_y': calib_y,
            'calib_w': calib_w,
            'calib_h': calib_h,
            'bag_x': bag_x,
            'bag_y': bag_y,
            'bag_w': bag_w,
            'bag_h': bag_h
        }
    
    def create_heatmap_data(self, gaze_data, layout_info, width=1200, height=800):
        """Create heatmap data from gaze points mapped to HTML layout"""
        if not gaze_data:
            return None
            
        # Get coordinate ranges from original data
        x_coords = [point['x'] for point in gaze_data]
        y_coords = [point['y'] for point in gaze_data]
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        # Initialize heatmap array
        heatmap = np.zeros((height, width))
        
        # Apply enhanced Gaussian kernel to each gaze point
        kernel_radius = 25  # Larger radius for smoother effect
        for point in gaze_data:
            # Map coordinates to HTML layout coordinates
            x = int((point['x'] - x_min) / (x_max - x_min) * (layout_info['calib_w'] - 1) + layout_info['calib_x'])
            y = int((point['y'] - y_min) / (y_max - y_min) * (layout_info['calib_h'] - 1) + layout_info['calib_y'])
            
            # Ensure coordinates are within valid range
            x = max(0, min(x, width - 1))
            y = max(0, min(y, height - 1))
            
            # Apply enhanced Gaussian kernel
            for i in range(max(0, y - kernel_radius), min(height, y + kernel_radius + 1)):
                for j in range(max(0, x - kernel_radius), min(width, x + kernel_radius + 1)):
                    distance = math.sqrt((i - y) ** 2 + (j - x) ** 2)
                    if distance <= kernel_radius:
                        # Enhanced intensity calculation for smoother gradients
                        intensity = math.exp(-distance ** 2 / (kernel_radius / 2.5))
                        heatmap[i, j] += intensity
        
        return heatmap
    
    def enhanced_intensity_to_color(self, intensity, max_intensity):
        """Convert intensity to color using enhanced gradient (blue->purple->green->yellow->orange->red)"""
        if intensity <= 0:
            return (0, 0, 0, 0)  # Transparent
        
        # Normalize intensity
        normalized = intensity / max_intensity if max_intensity > 0 else 0
        
        # Enhanced color scheme: Blue -> Purple -> Green -> Yellow -> Orange -> Red
        if normalized < 0.15:
            # Blue to Purple
            blue = 255
            red = int(100 + 155 * (normalized / 0.15))
            green = 0
            alpha = int(80 + 175 * (normalized / 0.15))
        elif normalized < 0.3:
            # Purple to Green
            blue = int(255 * (1 - (normalized - 0.15) / 0.15))
            red = 255
            green = int(255 * ((normalized - 0.15) / 0.15))
            alpha = int(200 + 55 * ((normalized - 0.15) / 0.15))
        elif normalized < 0.5:
            # Green to Yellow
            blue = 0
            green = 255
            red = 255
            alpha = int(220 + 35 * ((normalized - 0.3) / 0.2))
        elif normalized < 0.7:
            # Yellow to Orange
            blue = 0
            green = int(255 * (1 - (normalized - 0.5) / 0.2))
            red = 255
            alpha = int(230 + 25 * ((normalized - 0.5) / 0.2))
        elif normalized < 0.85:
            # Orange to Red
            blue = 0
            green = 0
            red = 255
            alpha = int(240 + 15 * ((normalized - 0.7) / 0.15))
        else:
            # Bright red
            blue = 0
            green = 0
            red = 255
            alpha = 255
        
        return (red, green, blue, alpha)
    
    def create_enhanced_heatmap(self, gaze_data, title, output_file):
        """Create enhanced heatmap with HTML layout and improved colors"""
        print(f"\nCreating enhanced heatmap: {output_file}")
        
        if not gaze_data:
            print("✗ No gaze data available")
            return False
        
        # Create HTML background
        width, height = 1200, 800
        background, layout_info = self.create_html_background(width, height)
        
        # Create heatmap data
        heatmap_data = self.create_heatmap_data(gaze_data, layout_info, width, height)
        
        if heatmap_data is None:
            print("✗ Failed to create heatmap data")
            return False
        
        # Create heatmap overlay
        heatmap_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        pixels = heatmap_layer.load()
        
        # Find maximum intensity for normalization
        max_intensity = np.max(heatmap_data)
        
        # Apply enhanced colors to heatmap
        for y in range(height):
            for x in range(width):
                intensity = heatmap_data[y, x]
                if intensity > 0:
                    color = self.enhanced_intensity_to_color(intensity, max_intensity)
                    pixels[x, y] = color
        
        # Apply multiple Gaussian blur passes for smoother effect
        heatmap_layer = heatmap_layer.filter(ImageFilter.GaussianBlur(radius=3))
        heatmap_layer = heatmap_layer.filter(ImageFilter.GaussianBlur(radius=2))
        
        # Combine background and heatmap overlay
        result = background.copy()
        result.paste(heatmap_layer, (0, 0), heatmap_layer)
        
        # Add title and annotations
        draw = ImageDraw.Draw(result)
        
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 18)
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 12)
        except:
            title_font = ImageFont.load_default()
            font = ImageFont.load_default()
        
        # Add title
        draw.text((20, 20), title, fill=(0, 0, 0), font=title_font)
        
        # Add enhanced color legend
        legend_y = height - 120
        legend_text = "Gaze Intensity"
        draw.text((20, legend_y), legend_text, fill=(0, 0, 0), font=font)
        
        # Draw enhanced color bar
        for i in range(400):
            x = 20 + i
            y = legend_y + 20
            intensity = i / 400
            color = self.enhanced_intensity_to_color(intensity, 1.0)
            draw.line([(x, y), (x, y + 15)], fill=(color[0], color[1], color[2]), width=1)
        
        # Add legend labels
        draw.text((20, legend_y + 40), "Low", fill=(0, 0, 0), font=font)
        draw.text((380, legend_y + 40), "High", fill=(0, 0, 0), font=font)
        
        # Add statistics
        total_points = len(gaze_data)
        participants = len(set([d['participant'] for d in gaze_data]))
        stats_text = f"Total points: {total_points:,} | Participants: {participants}"
        draw.text((20, legend_y + 60), stats_text, fill=(100, 100, 100), font=font)
        
        # Save the result
        result.save(output_file, "PNG")
        print(f"✓ Enhanced heatmap saved: {output_file}")
        return True
    
    def create_enhanced_comparison(self, output_file="enhanced_group_comparison.png"):
        """Create enhanced side-by-side comparison"""
        print(f"\nCreating enhanced group comparison: {output_file}")
        
        if not self.group1_data or not self.group2_data:
            print("✗ Insufficient data for comparison")
            return False
        
        # Create individual heatmaps
        width, height = 1200, 800
        total_width = width * 2 + 50
        total_height = height + 100
        
        # Create main image
        img = Image.new('RGB', (total_width, total_height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        except:
            title_font = ImageFont.load_default()
            font = ImageFont.load_default()
        
        # Add main title
        draw.text((total_width//2 - 300, 20), "Enhanced Group Heatmap Comparison", fill=(0, 0, 0), font=title_font)
        
        # Create Group 1 heatmap
        background1, layout_info1 = self.create_html_background(width, height)
        heatmap_data1 = self.create_heatmap_data(self.group1_data, layout_info1, width, height)
        
        if heatmap_data1 is not None:
            heatmap_layer1 = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            pixels1 = heatmap_layer1.load()
            max_intensity1 = np.max(heatmap_data1)
            
            for y in range(height):
                for x in range(width):
                    intensity = heatmap_data1[y, x]
                    if intensity > 0:
                        color = self.enhanced_intensity_to_color(intensity, max_intensity1)
                        pixels1[x, y] = color
            
            heatmap_layer1 = heatmap_layer1.filter(ImageFilter.GaussianBlur(radius=3))
            heatmap_layer1 = heatmap_layer1.filter(ImageFilter.GaussianBlur(radius=2))
            background1.paste(heatmap_layer1, (0, 0), heatmap_layer1)
        
        # Create Group 2 heatmap
        background2, layout_info2 = self.create_html_background(width, height)
        heatmap_data2 = self.create_heatmap_data(self.group2_data, layout_info2, width, height)
        
        if heatmap_data2 is not None:
            heatmap_layer2 = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            pixels2 = heatmap_layer2.load()
            max_intensity2 = np.max(heatmap_data2)
            
            for y in range(height):
                for x in range(width):
                    intensity = heatmap_data2[y, x]
                    if intensity > 0:
                        color = self.enhanced_intensity_to_color(intensity, max_intensity2)
                        pixels2[x, y] = color
            
            heatmap_layer2 = heatmap_layer2.filter(ImageFilter.GaussianBlur(radius=3))
            heatmap_layer2 = heatmap_layer2.filter(ImageFilter.GaussianBlur(radius=2))
            background2.paste(heatmap_layer2, (0, 0), heatmap_layer2)
        
        # Paste heatmaps onto main image
        img.paste(background1, (20, 60))
        img.paste(background2, (width + 70, 60))
        
        # Add labels
        draw.text((20, height + 70), "Group 1: Negative Feedback", fill=(0, 0, 0), font=font)
        draw.text((width + 70, height + 70), "Group 2: No Negative Feedback", fill=(0, 0, 0), font=font)
        
        # Add statistics
        stats1 = f"Points: {len(self.group1_data):,}"
        stats2 = f"Points: {len(self.group2_data):,}"
        draw.text((20, height + 90), stats1, fill=(100, 100, 100), font=font)
        draw.text((width + 70, height + 90), stats2, fill=(100, 100, 100), font=font)
        
        # Save the comparison
        img.save(output_file, "PNG")
        print(f"✓ Enhanced group comparison saved: {output_file}")
        return True
    
    def run_enhanced_analysis(self):
        """Run complete enhanced group heatmap analysis"""
        print("=" * 70)
        print("Enhanced Group Heatmap Analysis")
        print("=" * 70)
        
        # Load group data
        if not self.load_group_data():
            print("✗ Data loading failed")
            return False
        
        # Analyze page dimensions
        self.analyze_page_dimensions()
        
        # Create enhanced individual group heatmaps
        print("\nCreating enhanced individual group heatmaps...")
        self.create_enhanced_heatmap(
            self.group1_data,
            "Group 1: Negative Feedback Condition",
            "enhanced_group1_heatmap.png"
        )
        
        self.create_enhanced_heatmap(
            self.group2_data,
            "Group 2: No Negative Feedback Condition",
            "enhanced_group2_heatmap.png"
        )
        
        # Create enhanced comparison heatmap
        self.create_enhanced_comparison()
        
        print("\n" + "=" * 70)
        print("Enhanced Group Analysis Complete!")
        print("Generated files:")
        print("- enhanced_group1_heatmap.png: Group 1 enhanced heatmap")
        print("- enhanced_group2_heatmap.png: Group 2 enhanced heatmap")
        print("- enhanced_group_comparison.png: Enhanced comparison")
        print("=" * 70)
        
        return True

def main():
    analyzer = EnhancedGroupHeatmapAnalyzer()
    analyzer.run_enhanced_analysis()

if __name__ == "__main__":
    main() 