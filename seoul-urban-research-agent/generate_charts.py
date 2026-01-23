#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
자전거 도로 정책 종합 데이터 분석 및 차트 생성 스크립트
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'

# 차트 출력 경로
CHART_DIR = Path('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts')
DATA_DIR = Path('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/data')

# 경로 생성
CHART_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 1. 국내 도시별 자전거 도로 길이 비교
def create_domestic_cities_comparison():
    cities = ['Seoul', 'Busan', 'Incheon', 'Daegu', 'National\nAverage']
    road_lengths = [775.9, 259.7, 969, 850, 1000]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#CCCCCC']

    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.bar(cities, road_lengths, color=colors, edgecolor='black', linewidth=1.5)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}km',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_ylabel('Bicycle Road Length (km)', fontsize=12, fontweight='bold')
    ax.set_title('Domestic Cities: Bicycle Road Length Comparison',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, max(road_lengths) * 1.15)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(CHART_DIR / '01_domestic_cities_bicycle_road_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

# 2. 해외 주요 도시의 자전거 모달 셰어 비교
def create_international_modal_share_comparison():
    cities = ['Amsterdam', 'Copenhagen', 'Berlin', 'Tokyo', 'Singapore']
    modal_shares = [38, 37, 9, 13.5, 2]
    colors = ['#FF6B6B', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']

    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.bar(cities, modal_shares, color=colors, edgecolor='black', linewidth=1.5)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_ylabel('Bicycle Modal Share (%)', fontsize=12, fontweight='bold')
    ax.set_title('International Cities: Bicycle Modal Share Comparison',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 45)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    ax.axhline(y=7, color='red', linestyle='--', linewidth=2, label='World Average (~7%)')
    ax.legend()

    plt.tight_layout()
    plt.savefig(CHART_DIR / '02_international_modal_share_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

# 3. 서울시 공공자전거 이용 추이
def create_seoul_ttareungyi_trend():
    years = [2022, 2023, 2024]
    usage = [14.14, 44.90, 43.85]
    daily_avg = [38.97, 123.01, 120.14]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    line1 = ax1.plot(years, usage, marker='o', linewidth=2.5, markersize=10,
                     color='#FF6B6B', label='Annual Usage')
    ax1.fill_between(years, usage, alpha=0.3, color='#FF6B6B')

    for i, (x, y) in enumerate(zip(years, usage)):
        ax1.text(x, y + 1.5, f'{y:.2f}M', ha='center', fontsize=10, fontweight='bold')

    ax1.set_ylabel('Annual Usage (Million Rides)', fontsize=11, fontweight='bold')
    ax1.set_title('Seoul TTareungyi: Annual Usage Trend (2022-2024)',
                  fontsize=13, fontweight='bold', pad=15)
    ax1.set_xticks(years)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_ylim(0, 50)

    line2 = ax2.plot(years, daily_avg, marker='s', linewidth=2.5, markersize=10,
                     color='#4ECDC4', label='Daily Average')
    ax2.fill_between(years, daily_avg, alpha=0.3, color='#4ECDC4')

    for i, (x, y) in enumerate(zip(years, daily_avg)):
        ax2.text(x, y + 2, f'{y:.2f}K', ha='center', fontsize=10, fontweight='bold')

    ax2.set_ylabel('Daily Average Usage (10,000 Rides)', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax2.set_title('Seoul TTareungyi: Daily Average Usage Trend (2022-2024)',
                  fontsize=13, fontweight='bold', pad=15)
    ax2.set_xticks(years)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_ylim(0, 150)

    plt.tight_layout()
    plt.savefig(CHART_DIR / '03_seoul_ttareungyi_usage_trend.png', dpi=300, bbox_inches='tight')
    plt.close()

# 4. 자전거 사고 및 사망자 추이
def create_bicycle_accident_trend():
    years = [2022, 2023, 2024]
    accidents = [5393, 5146, 5250]
    deaths = [91, 64, 60]

    fig, ax1 = plt.subplots(figsize=(12, 7))

    ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Accidents (Cases)', fontsize=12, fontweight='bold', color='#FF6B6B')
    line1 = ax1.plot(years, accidents, marker='o', linewidth=2.5, markersize=10,
                     color='#FF6B6B', label='Accidents')
    ax1.fill_between(years, accidents, alpha=0.3, color='#FF6B6B')
    ax1.tick_params(axis='y', labelcolor='#FF6B6B')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_xticks(years)

    for x, y in zip(years, accidents):
        ax1.text(x, y + 100, f'{y}', ha='center', fontsize=10, fontweight='bold', color='#FF6B6B')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Deaths (People)', fontsize=12, fontweight='bold', color='#45B7D1')
    line2 = ax2.plot(years, deaths, marker='s', linewidth=2.5, markersize=10,
                     color='#45B7D1', label='Deaths')
    ax2.fill_between(years, deaths, alpha=0.3, color='#45B7D1')
    ax2.tick_params(axis='y', labelcolor='#45B7D1')

    for x, y in zip(years, deaths):
        ax2.text(x, y + 3, f'{y}', ha='center', fontsize=10, fontweight='bold', color='#45B7D1')

    fig.suptitle('Bicycle Accidents and Deaths Trend (2022-2024)',
                 fontsize=14, fontweight='bold', y=0.98)

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', fontsize=11)

    plt.tight_layout()
    plt.savefig(CHART_DIR / '04_bicycle_accident_trend.png', dpi=300, bbox_inches='tight')
    plt.close()

# 5. 서울시 도로 유형별 구성
def create_seoul_road_type_composition():
    labels = ['Shared\n(74.5%)', 'Dedicated\n(14.0%)', 'Priority\n(7.7%)', 'Exclusive\n(3.8%)']
    sizes = [74.5, 14.0, 7.7, 3.8]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    explode = (0.05, 0.05, 0, 0)

    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                        explode=explode, shadow=True, startangle=90,
                                        textprops={'fontsize': 10, 'weight': 'bold'})

    ax.set_title('Seoul Bicycle Road Type Composition (National Average)',
                 fontsize=13, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(CHART_DIR / '05_seoul_road_type_composition.png', dpi=300, bbox_inches='tight')
    plt.close()

# 6. 국내 도시 정책 성숙도 비교
def create_policy_maturity_comparison():
    cities = ['Seoul', 'Busan', 'Incheon', 'Daegu']
    maturity_levels = [4, 2.5, 2.5, 1.5]

    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.barh(cities, maturity_levels, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
                   edgecolor='black', linewidth=1.5)

    for i, (bar, val) in enumerate(zip(bars, maturity_levels)):
        ax.text(val + 0.1, bar.get_y() + bar.get_height()/2.,
                f'{val}/5.0', ha='left', va='center', fontsize=11, fontweight='bold')

    ax.set_xlabel('Policy Maturity Level (5-point scale)', fontsize=12, fontweight='bold')
    ax.set_title('Domestic Cities: Bicycle Policy Maturity Comparison',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 5)
    ax.grid(axis='x', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(CHART_DIR / '06_policy_maturity_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

# 7. 해외 도시 네트워크 규모 비교
def create_international_network_comparison():
    cities = ['Amsterdam', 'Berlin\n(Plan)', 'Singapore', 'London\n(Plan)', 'Copenhagen', 'Tokyo']
    lengths = [700, 3000, 730, 450, 454, 404]
    colors = ['#FF6B6B', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFD700']

    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.bar(cities, lengths, color=colors, edgecolor='black', linewidth=1.5)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}km',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_ylabel('Network Length (km)', fontsize=12, fontweight='bold')
    ax.set_title('International Cities: Bicycle Network Size Comparison',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 3500)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(CHART_DIR / '07_international_network_size_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

# 8. 시민 만족도 및 정책 지지도
def create_citizen_satisfaction():
    categories = ['Service\nSatisfaction', 'Expansion\nSupport', 'Safety\nConcern', 'Inconvenience\nRate']
    percentages = [86, 99, 30, 14]
    colors = ['#4ECDC4', '#4ECDC4', '#FF6B6B', '#FFB6C1']

    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.bar(categories, percentages, color=colors, edgecolor='black', linewidth=1.5)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}%',
                ha='center', va='bottom', fontsize=12, fontweight='bold')

    ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    ax.set_title('Citizen Opinion on Bicycle Policy: Satisfaction and Support',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 110)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(CHART_DIR / '08_citizen_satisfaction.png', dpi=300, bbox_inches='tight')
    plt.close()

# 9. 따릉이 이용자 사용 시간대 분포
def create_ttareungyi_usage_by_time():
    time_periods = ['Morning\nCommute', 'Evening\nCommute', 'Afternoon\nLeisure']
    weekday = [18, 26.3, 0]
    weekend = [0, 0, 41.9]

    x = np.arange(len(time_periods))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 7))
    bars1 = ax.bar(x - width/2, weekday, width, label='Weekday',
                   color='#4ECDC4', edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x + width/2, weekend, width, label='Weekend',
                   color='#FF6B6B', edgecolor='black', linewidth=1.5)

    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%',
                        ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_ylabel('Usage Percentage (%)', fontsize=12, fontweight='bold')
    ax.set_title('TTareungyi Usage by Time Period and Day Type',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(time_periods)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, 50)

    plt.tight_layout()
    plt.savefig(CHART_DIR / '09_ttareungyi_usage_by_time.png', dpi=300, bbox_inches='tight')
    plt.close()

# 10. 투자 규모 비교
def create_investment_comparison():
    cities = ['Seoul\n(Annual)', 'Berlin\n(2020)', 'Copenhagen\n(2025)', 'London\n(Annual)']
    investments = [20, 32, 80, 100]

    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.bar(cities, investments, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'],
                  edgecolor='black', linewidth=1.5)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.0f}M',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_ylabel('Annual Investment (Million USD)', fontsize=12, fontweight='bold')
    ax.set_title('Bicycle Infrastructure Investment Comparison by City',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 120)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(CHART_DIR / '10_investment_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    print("\n" + "="*80)
    print("Starting Bicycle Road Policy Data Analysis and Chart Generation")
    print("="*80 + "\n")

    create_domestic_cities_comparison()
    print("✓ Chart 01 completed")

    create_international_modal_share_comparison()
    print("✓ Chart 02 completed")

    create_seoul_ttareungyi_trend()
    print("✓ Chart 03 completed")

    create_bicycle_accident_trend()
    print("✓ Chart 04 completed")

    create_seoul_road_type_composition()
    print("✓ Chart 05 completed")

    create_policy_maturity_comparison()
    print("✓ Chart 06 completed")

    create_international_network_comparison()
    print("✓ Chart 07 completed")

    create_citizen_satisfaction()
    print("✓ Chart 08 completed")

    create_ttareungyi_usage_by_time()
    print("✓ Chart 09 completed")

    create_investment_comparison()
    print("✓ Chart 10 completed")

    print("\n" + "="*80)
    print("All charts generated successfully!")
    print("="*80)
    print(f"\nChart location: {CHART_DIR}")
    print("\nGenerated files:")
    for chart_file in sorted(CHART_DIR.glob('*.png')):
        print(f"  - {chart_file.name}")

if __name__ == '__main__':
    main()
