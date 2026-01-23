#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시 자전거 도로 인프라 분석 및 시각화
데이터: 국내 및 국제 자전거 인프라 현황 비교
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from pathlib import Path

# 한글 폰트 설정
try:
    import matplotlib.font_manager as fm
    fm.fontManager.addfont('/System/Library/Fonts/Supplemental/AppleGothic.ttf')
    plt.rcParams['font.family'] = 'AppleGothic'
except:
    try:
        fm.fontManager.addfont('/Library/Fonts/NotoSansCJK-Regular.ttc')
        plt.rcParams['font.family'] = 'Noto Sans CJK JP'
    except:
        pass

plt.rcParams['axes.unicode_minus'] = False

# 디렉토리 생성
charts_dir = Path('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts')
charts_dir.mkdir(parents=True, exist_ok=True)

data_dir = Path('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/data')
data_dir.mkdir(parents=True, exist_ok=True)

# 스타일 설정
sns.set_style("whitegrid")

# ============================================
# Chart 1: Seoul Bicycle Usage Trend
# ============================================
print("Generating Chart 1: Seoul Bicycle Usage Trend...")

fig, ax = plt.subplots(figsize=(10, 6))

years = [2019, 2020, 2021, 2022, 2023, 2024]
usage_count = [2.7, 3.5, 4.2, 5.1, 5.7, 4.385]

ax.plot(years, usage_count, marker='o', linewidth=2.5, markersize=8,
        label='Public Bicycle Usage (Million Rides)', color='#2E86AB')

for i, (year, count) in enumerate(zip(years, usage_count)):
    ax.text(year, count + 0.15, f'{count}', ha='center', fontsize=10, fontweight='bold')

ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Annual Usage (Million Rides)', fontsize=12, fontweight='bold')
ax.set_title('Seoul Public Bicycle (Ddareung) Usage Trend\n2019-2024',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(years)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11, loc='upper left')

growth_2019_2024 = ((4.385 - 2.7) / 2.7) * 100
ax.text(0.98, 0.05, f'Growth (2019-2024): {growth_2019_2024:.1f}%\nNote: 2024 shows seasonal impact',
        transform=ax.transAxes, fontsize=10, ha='right', va='bottom',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig(charts_dir / 'chart1_seoul_usage_trend.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================
# Chart 2: Seoul District Distribution
# ============================================
print("Generating Chart 2: Seoul District Distribution...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

regions = ['Gangnam\n(South)', 'Gangbuk\n(North)']
dedicated_roads = [63.1, 11.6]
colors_region = ['#A23B72', '#F18F01']

bars1 = ax1.bar(regions, dedicated_roads, color=colors_region, edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Dedicated Bicycle Road Length (km)', fontsize=11, fontweight='bold')
ax1.set_title('Gangnam vs Gangbuk\nDedicated Bicycle Road Distribution',
              fontsize=12, fontweight='bold')
ax1.set_ylim(0, 75)

for bar, value in zip(bars1, dedicated_roads):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{value} km\n({value/sum(dedicated_roads)*100:.1f}%)',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

gap_ratio = dedicated_roads[0] / dedicated_roads[1]
ax1.text(0.5, 0.95, f'Gap: {gap_ratio:.1f}x', transform=ax1.transAxes,
        ha='center', va='top', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='red', alpha=0.3))

districts_gangnam = ['Gangnam-gu\n(4 districts)', 'Rest of\nGangnam']
gangnam_distribution = [26.1, 37.0]
colors_gangnam = ['#E63946', '#F77F00']

bars2 = ax2.bar(districts_gangnam, gangnam_distribution, color=colors_gangnam,
                edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Road Length (km)', fontsize=11, fontweight='bold')
ax2.set_title('Gangnam Internal Distribution\n(4 Districts Concentration)',
              fontsize=12, fontweight='bold')
ax2.set_ylim(0, 45)

for bar, value in zip(bars2, gangnam_distribution):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{value} km\n({value/sum(gangnam_distribution)*100:.1f}%)',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(charts_dir / 'chart2_seoul_district_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================
# Chart 3: Korean Cities Comparison
# ============================================
print("Generating Chart 3: Korean Cities Comparison...")

fig, ax = plt.subplots(figsize=(11, 7))

cities_kr = ['Seoul', 'Busan', 'Incheon', 'Daegu']
dedicated_roads_kr = [99.5, 85.0, 120.0, 95.0]
total_roads_kr = [775.9, 250.0, 280.0, 200.0]

x = np.arange(len(cities_kr))
width = 0.35

bars1 = ax.bar(x - width/2, dedicated_roads_kr, width, label='Dedicated Road',
              color='#2E86AB', edgecolor='black', linewidth=1.2)
bars2 = ax.bar(x + width/2, total_roads_kr, width, label='Total Road Network',
              color='#A23B72', edgecolor='black', linewidth=1.2)

ax.set_xlabel('Major Korean Cities', fontsize=12, fontweight='bold')
ax.set_ylabel('Bicycle Road Length (km)', fontsize=12, fontweight='bold')
ax.set_title('Comparison of Bicycle Road Infrastructure\nMajor Korean Cities (2024)',
             fontsize=13, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(cities_kr, fontsize=11)
ax.legend(fontsize=11, loc='upper left')
ax.set_ylim(0, 900)
ax.grid(True, alpha=0.3, axis='y')

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(charts_dir / 'chart3_korean_cities_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================
# Chart 4: International Cities
# ============================================
print("Generating Chart 4: International Cities...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

cities_intl = ['Amsterdam', 'Copenhagen', 'Tokyo', 'Singapore']
road_length = [400, 416, 200, 440]
colors_intl = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

bars1 = ax1.barh(cities_intl, road_length, color=colors_intl, edgecolor='black', linewidth=1.5)
ax1.set_xlabel('Bicycle Road Length (km)', fontsize=11, fontweight='bold')
ax1.set_title('Bicycle Road Length Comparison\nInternational Major Cities (2024)',
              fontsize=12, fontweight='bold')
ax1.set_xlim(0, 500)

for i, (bar, value) in enumerate(zip(bars1, road_length)):
    ax1.text(value + 10, i, f'{value} km', va='center', fontsize=10, fontweight='bold')

investment_data = {
    'Amsterdam': 120,
    'Copenhagen': 10,
    'Tokyo': 40,
    'Singapore': 1000
}

cities_order = list(investment_data.keys())
investments = list(investment_data.values())

bars2 = ax2.bar(range(len(cities_order)), investments, color=colors_intl,
               edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Annual Investment (Million USD)', fontsize=11, fontweight='bold')
ax2.set_title('Annual Bicycle Infrastructure Investment',
              fontsize=12, fontweight='bold')
ax2.set_xticks(range(len(cities_order)))
ax2.set_xticklabels(cities_order, fontsize=10)
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3, axis='y')

for bar, value in zip(bars2, investments):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height * 1.3,
            f'${value}M', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(charts_dir / 'chart4_international_cities_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ All charts generated successfully!")
