#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# 디렉토리 생성
charts_dir = Path('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts')
charts_dir.mkdir(parents=True, exist_ok=True)

data_dir = Path('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/data')
data_dir.mkdir(parents=True, exist_ok=True)

# 한글 폰트 설정
plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# Chart 1: Seoul Usage Trend
print("Creating Chart 1: Seoul Bicycle Usage Trend...")
fig, ax = plt.subplots(figsize=(10, 6))
years = [2019, 2020, 2021, 2022, 2023, 2024]
usage = [2.7, 3.5, 4.2, 5.1, 5.7, 4.385]

ax.plot(years, usage, marker='o', linewidth=2.5, markersize=8, color='#2E86AB')
for year, count in zip(years, usage):
    ax.text(year, count + 0.15, f'{count}', ha='center', fontsize=10, fontweight='bold')

ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Usage (Million Rides)', fontsize=12, fontweight='bold')
ax.set_title('Seoul Public Bicycle Usage Trend 2019-2024', fontsize=14, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 7)
plt.tight_layout()
plt.savefig(charts_dir / 'chart1_seoul_usage_trend.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 2: District Distribution
print("Creating Chart 2: Seoul District Distribution...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left: Gangnam vs Gangbuk
regions = ['Gangnam\n(South)', 'Gangbuk\n(North)']
roads = [63.1, 11.6]
colors = ['#A23B72', '#F18F01']

bars = ax1.bar(regions, roads, color=colors, edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Dedicated Road Length (km)', fontsize=11, fontweight='bold')
ax1.set_title('Gangnam vs Gangbuk Distribution', fontsize=12, fontweight='bold')
ax1.set_ylim(0, 75)

for bar, val in zip(bars, roads):
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
            f'{val} km', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Right: Gangnam detail
districts = ['4 Districts', 'Rest']
dist_roads = [26.1, 37.0]
colors2 = ['#E63946', '#F77F00']

bars = ax2.bar(districts, dist_roads, color=colors2, edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Road Length (km)', fontsize=11, fontweight='bold')
ax2.set_title('Gangnam Distribution Detail', fontsize=12, fontweight='bold')
ax2.set_ylim(0, 45)

for bar, val in zip(bars, dist_roads):
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
            f'{val} km', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(charts_dir / 'chart2_seoul_district_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 3: Korean Cities
print("Creating Chart 3: Korean Cities Comparison...")
fig, ax = plt.subplots(figsize=(11, 7))

cities = ['Seoul', 'Busan', 'Incheon', 'Daegu']
dedicated = [99.5, 85.0, 120.0, 95.0]
total = [775.9, 250.0, 280.0, 200.0]

x = np.arange(len(cities))
width = 0.35

bars1 = ax.bar(x - width/2, dedicated, width, label='Dedicated Road', color='#2E86AB', edgecolor='black')
bars2 = ax.bar(x + width/2, total, width, label='Total Network', color='#A23B72', edgecolor='black')

ax.set_xlabel('Cities', fontsize=12, fontweight='bold')
ax.set_ylabel('Road Length (km)', fontsize=12, fontweight='bold')
ax.set_title('Korean Cities Bicycle Road Comparison', fontsize=13, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(cities)
ax.legend(fontsize=11)
ax.set_ylim(0, 900)
ax.grid(True, alpha=0.3, axis='y')

for bars in [bars1, bars2]:
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(charts_dir / 'chart3_korean_cities_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# Chart 4: International Cities
print("Creating Chart 4: International Cities...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

cities_intl = ['Amsterdam', 'Copenhagen', 'Tokyo', 'Singapore']
length = [400, 416, 200, 440]
colors_intl = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

bars = ax1.barh(cities_intl, length, color=colors_intl, edgecolor='black', linewidth=1.5)
ax1.set_xlabel('Road Length (km)', fontsize=11, fontweight='bold')
ax1.set_title('International Cities Road Length', fontsize=12, fontweight='bold')
ax1.set_xlim(0, 500)

for i, (bar, val) in enumerate(zip(bars, length)):
    ax1.text(val + 10, i, f'{val} km', va='center', fontsize=10, fontweight='bold')

# Investment
cities_inv = ['Amsterdam', 'Copenhagen', 'Tokyo', 'Singapore']
investments = [120, 10, 40, 1000]

bars = ax2.bar(range(len(cities_inv)), investments, color=colors_intl, edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Investment (Million USD)', fontsize=11, fontweight='bold')
ax2.set_title('Annual Bicycle Infrastructure Investment', fontsize=12, fontweight='bold')
ax2.set_xticks(range(len(cities_inv)))
ax2.set_xticklabels(cities_inv, fontsize=10)
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3, axis='y')

for bar, val in zip(bars, investments):
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() * 1.3,
            f'${val}M', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(charts_dir / 'chart4_international_cities_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ All charts created successfully!")
print(f"Charts saved to: {charts_dir}")
