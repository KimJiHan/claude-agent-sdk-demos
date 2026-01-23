#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
자전거 도로 및 이용 현황 차트 생성 스크립트
Bicycle Infrastructure and Usage Analysis Charts Generation Script
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 출력 디렉토리 설정
output_dir = '/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts'
os.makedirs(output_dir, exist_ok=True)

# ============================================================================
# 1. 도시별 자전거 도로 길이 비교 (막대 차트)
# ============================================================================
def create_city_comparison_chart():
    """
    국내 5개 도시 자전거 도로 길이 비교
    """
    cities = ['서울', '부산', '인천', '대구', '대전']
    road_lengths = [775.9, 259.7, 969, 400, 774.7]  # km
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']

    fig, ax = plt.subplots(figsize=(12, 7))

    bars = ax.bar(cities, road_lengths, color=colors, edgecolor='black', linewidth=1.5)

    # 막대 위에 수치 표시
    for i, (bar, value) in enumerate(zip(bars, road_lengths)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.1f}km',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_ylabel('자전거 도로 길이 (km)', fontsize=12, fontweight='bold')
    ax.set_title('국내 주요 도시별 자전거 도로 길이 비교 (2024년 기준)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 1050)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/01_city_bicycle_road_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 1 saved: 01_city_bicycle_road_comparison.png")
    plt.close()

# ============================================================================
# 2. 따릉이 이용량 추이 (선 그래프)
# ============================================================================
def create_dareungi_trend_chart():
    """
    2015-2024년 따릉이 이용량 추이
    """
    years = [2015, 2016, 2018, 2020, 2022, 2024]
    usage = [0.113, 0.3, 1.5, 30, 35, 43.85]  # million trips (백만 건)

    fig, ax = plt.subplots(figsize=(12, 7))

    # 라인 그래프
    line = ax.plot(years, usage, marker='o', linewidth=2.5, markersize=8,
                   color='#FF6B6B', markerfacecolor='#FF6B6B', markeredgewidth=2,
                   markeredgecolor='white')

    # 데이터 포인트 레이블
    for year, value in zip(years, usage):
        ax.annotate(f'{value:.2f}M', xy=(year, value),
                   xytext=(0, 10), textcoords='offset points',
                   ha='center', fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))

    ax.set_xlabel('연도', fontsize=12, fontweight='bold')
    ax.set_ylabel('이용량 (백만 건)', fontsize=12, fontweight='bold')
    ax.set_title('따릉이(서울 공공자전거) 이용량 추이 (2015-2024년)\n2015년 대비 약 400배 성장',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(years)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.set_ylim(0, 50)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/02_dareungi_usage_trend.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 2 saved: 02_dareungi_usage_trend.png")
    plt.close()

# ============================================================================
# 3. 연령대별 자전거 사고 현황 (그룹 막대 차트)
# ============================================================================
def create_age_group_accident_chart():
    """
    2023-2024년 연령대별 자전거 사고 현황
    """
    age_groups = ['10대', '20대', '30대', '40대', '50대', '60대+']
    accidents_2023 = [1200, 2800, 2400, 1900, 1600, 1100]  # 2023년 사고 건수
    accidents_2024 = [1800, 3200, 2700, 2100, 1800, 1200]  # 2024년 사고 건수

    x = np.arange(len(age_groups))
    width = 0.35

    fig, ax = plt.subplots(figsize=(13, 7))

    bars1 = ax.bar(x - width/2, accidents_2023, width, label='2023년',
                   color='#4ECDC4', edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x + width/2, accidents_2024, width, label='2024년',
                   color='#FF6B6B', edgecolor='black', linewidth=1.5)

    # 막대 위에 수치 표시
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_xlabel('연령대', fontsize=12, fontweight='bold')
    ax.set_ylabel('자전거 사고 건수', fontsize=12, fontweight='bold')
    ax.set_title('연령대별 자전거 사고 현황 (2023-2024년)\n20대가 가장 높은 사고율 보유',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(age_groups)
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.set_ylim(0, 3800)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/03_age_group_accidents.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 3 saved: 03_age_group_accidents.png")
    plt.close()

# ============================================================================
# 4. 서울시 지역별 자전거 도로 분포 (파이 차트)
# ============================================================================
def create_seoul_regional_distribution():
    """
    서울시 지역별 자전거 도로 길이 분포 (강남/강북 비교)
    """
    regions = ['강남\n4구', '강북\n지역', '도심권', '서남권', '동남권', '서북권', '동북권']
    lengths = [266.9, 131.4, 43.5, 125.8, 184, 56.1, 111.8]  # km
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']

    fig, ax = plt.subplots(figsize=(12, 8))

    wedges, texts, autotexts = ax.pie(lengths, labels=regions, autopct='%1.1f%%',
                                        colors=colors, startangle=90,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'},
                                        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})

    # 퍼센트 텍스트 포매팅
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')

    ax.set_title('서울시 지역별 자전거 도로 길이 분포\n강남 지역이 강북 지역의 약 2배 규모',
                 fontsize=14, fontweight='bold', pad=20)

    # 범례 추가
    legend_labels = [f'{region.replace(chr(10), " ")}: {length:.1f}km'
                     for region, length in zip(regions, lengths)]
    ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/04_seoul_regional_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 4 saved: 04_seoul_regional_distribution.png")
    plt.close()

# ============================================================================
# 5. 국내 vs 해외 도시 자전거 모달쉐어 비교 (가로 막대 차트)
# ============================================================================
def create_modal_share_comparison():
    """
    국내 vs 해외 도시 자전거 모달 셰어 비교
    """
    cities = ['암스테르담', '코펜하겐', '베를린', '서울\n(목표)', '도쿄', '런던', '싱가포르']
    modal_shares = [38, 37, 18, 15, 13.5, 5, 2]  # percentage
    colors = ['#4ECDC4', '#4ECDC4', '#45B7D1', '#FF6B6B', '#FFA07A', '#98D8C8', '#F7DC6F']

    fig, ax = plt.subplots(figsize=(12, 7))

    bars = ax.barh(cities, modal_shares, color=colors, edgecolor='black', linewidth=1.5)

    # 막대 오른쪽에 수치 표시
    for i, (bar, value) in enumerate(zip(bars, modal_shares)):
        width = bar.get_width()
        ax.text(width + 0.5, bar.get_y() + bar.get_height()/2.,
                f'{value}%',
                ha='left', va='center', fontsize=11, fontweight='bold')

    ax.set_xlabel('자전거 모달 셰어 (%)', fontsize=12, fontweight='bold')
    ax.set_title('국내·해외 도시 자전거 모달 셰어 비교\n유럽 도시는 30% 이상, 아시아 도시는 20% 이하',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 45)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/05_modal_share_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 5 saved: 05_modal_share_comparison.png")
    plt.close()

# ============================================================================
# 6. 자전거도로 유형별 분포 (서울시)
# ============================================================================
def create_road_type_distribution():
    """
    서울시 자전거도로 유형별 분포
    """
    road_types = ['자전거·보행자\n겸용도로', '자전거\n전용도로', '자전거\n전용차로', '자전거\n우선도로']
    lengths = [574.9, 99.5, 51.8, 49.7]  # km
    percentages = [74.1, 12.8, 6.7, 6.4]  # percent
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # 막대 차트
    bars = ax1.bar(road_types, lengths, color=colors, edgecolor='black', linewidth=1.5)

    for bar, value in zip(bars, lengths):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.1f}km',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax1.set_ylabel('길이 (km)', fontsize=12, fontweight='bold')
    ax1.set_title('서울시 자전거도로 유형별 길이', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_axisbelow(True)
    ax1.set_ylim(0, 650)

    # 파이 차트
    wedges, texts, autotexts = ax2.pie(percentages, labels=road_types, autopct='%1.1f%%',
                                         colors=colors, startangle=90,
                                         textprops={'fontsize': 10, 'fontweight': 'bold'},
                                         wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')

    ax2.set_title('서울시 자전거도로 유형별 비중', fontsize=12, fontweight='bold')

    fig.suptitle('서울시 자전거도로 유형별 분포 현황 (2015년 기준)\n겸용도로 74.1%로 대부분을 차지',
                 fontsize=14, fontweight='bold', y=1.02)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/06_road_type_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 6 saved: 06_road_type_distribution.png")
    plt.close()

# ============================================================================
# 7. 전국 자전거도로 연장 추이
# ============================================================================
def create_national_trend():
    """
    전국 자전거도로 총 길이 연장 추이
    """
    years = [2021, 2023, 2024]
    lengths = [25249.12, 26872, 27754]  # km

    fig, ax = plt.subplots(figsize=(12, 7))

    line = ax.plot(years, lengths, marker='o', linewidth=2.5, markersize=10,
                   color='#4ECDC4', markerfacecolor='#4ECDC4', markeredgewidth=2,
                   markeredgecolor='white')

    # 데이터 포인트 레이블
    for year, value in zip(years, lengths):
        ax.annotate(f'{value:,.0f}km', xy=(year, value),
                   xytext=(0, 15), textcoords='offset points',
                   ha='center', fontsize=11, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='lightblue', alpha=0.7))

    ax.set_xlabel('연도', fontsize=12, fontweight='bold')
    ax.set_ylabel('자전거도로 총 길이 (km)', fontsize=12, fontweight='bold')
    ax.set_title('전국 자전거도로 총 길이 연장 추이\n2021년 대비 2024년 약 10% 증가',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(years)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.set_ylim(24500, 28500)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/07_national_road_trend.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 7 saved: 07_national_road_trend.png")
    plt.close()

# ============================================================================
# 메인 실행
# ============================================================================
def main():
    print("=" * 60)
    print("자전거 도로 및 이용 현황 분석 차트 생성 시작")
    print("=" * 60)
    print()

    create_city_comparison_chart()
    create_dareungi_trend_chart()
    create_age_group_accident_chart()
    create_seoul_regional_distribution()
    create_modal_share_comparison()
    create_road_type_distribution()
    create_national_trend()

    print()
    print("=" * 60)
    print("모든 차트가 성공적으로 생성되었습니다!")
    print(f"저장 위치: {output_dir}")
    print("=" * 60)

if __name__ == '__main__':
    main()
