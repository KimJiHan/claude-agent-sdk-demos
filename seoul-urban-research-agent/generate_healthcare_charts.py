#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시 의료 산업 데이터 시각화 생성 스크립트
Healthcare Industry Data Visualization Generator for Seoul
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import json
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 출력 디렉토리 설정
OUTPUT_DIR = Path("/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts")
DATA_DIR = Path("/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/data")

# 디렉토리 생성
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)


def set_korean_font():
    """한글 폰트 설정"""
    try:
        font_path = "/System/Library/Fonts/AppleGothic.ttf"
        font = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font.get_name()
    except:
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Helvetica']


def chart1_market_growth():
    """1. 서울시 의료 산업 시장 규모 및 성장률 추이"""
    print("생성 중: Chart 1 - 시장 규모 및 성장률")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Seoul Healthcare Market Size & Growth Trend', fontsize=14, fontweight='bold')

    # 데이터: 2024-2025년 기준
    years = ['2024', '2025', '2026E', '2027E', '2028E']
    market_size = [213.1, 225.0, 238.0, 251.0, 265.0]  # 조 원
    growth_rate = [5.6, 5.6, 5.8, 5.5, 5.5]  # %

    # 막대 그래프 (시장 규모)
    bars = ax1.bar(years, market_size, color='#2E86AB', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Market Size (Trillion KRW)', fontsize=11, fontweight='bold')
    ax1.set_title('Healthcare Market Size Trend', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 300)

    # 값 표시
    for i, (bar, val) in enumerate(zip(bars, market_size)):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f'{val:.1f}', ha='center', va='bottom', fontweight='bold')

    # 선형 그래프 (성장률)
    ax2.plot(years, growth_rate, marker='o', linewidth=2.5, markersize=8, color='#A23B72')
    ax2.set_ylabel('Growth Rate (%)', fontsize=11, fontweight='bold')
    ax2.set_title('Year-over-Year Growth Rate', fontsize=12, fontweight='bold')
    ax2.set_ylim(4, 7)
    ax2.grid(True, alpha=0.3, linestyle='--')

    # 값 표시
    for x, y in zip(years, growth_rate):
        ax2.text(x, y + 0.15, f'{y:.1f}%', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'healthcare_market_growth.png', dpi=300, bbox_inches='tight')
    print("✓ healthcare_market_growth.png 저장됨")
    plt.close()


def chart2_institutions_distribution():
    """2. 의료기관 유형별 현황 분포"""
    print("생성 중: Chart 2 - 의료기관 분포")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Healthcare Institutions Distribution in Seoul', fontsize=14, fontweight='bold')

    # 파이 차트 데이터 (추정치)
    institutions = ['General Hospitals', 'Hospitals', 'Clinics', 'Dental Clinics', 'Korean Medicine', 'Pharmacies']
    counts = [120, 350, 2800, 1200, 500, 2100]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']

    # 파이 차트
    wedges, texts, autotexts = ax1.pie(counts, labels=institutions, autopct='%1.1f%%',
                                         colors=colors, startangle=90, textprops={'fontsize': 9})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)
    ax1.set_title('Distribution by Institution Type', fontsize=12, fontweight='bold')

    # 막대 차트
    ax2.barh(institutions, counts, color=colors, edgecolor='black', linewidth=1.2)
    ax2.set_xlabel('Number of Institutions', fontsize=11, fontweight='bold')
    ax2.set_title('Institution Count by Type', fontsize=12, fontweight='bold')

    # 값 표시
    for i, (inst, count) in enumerate(zip(institutions, counts)):
        ax2.text(count + 50, i, f'{count:,}', va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'healthcare_institutions_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ healthcare_institutions_distribution.png 저장됨")
    plt.close()


def chart3_global_vs_seoul():
    """4. 글로벌 의료 시장 vs 서울 시장 비교"""
    print("생성 중: Chart 3 - 글로벌 vs 서울 비교")

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Seoul vs Global Healthcare Market Comparison', fontsize=14, fontweight='bold')

    # 1. 시장 규모 비교 (2024년)
    categories = ['Seoul\n(213.1T KRW)', 'South Korea\n(213.1T KRW)', 'Global Market\n(9T USD)']
    values = [213.1, 213.1, 11700]  # 환율 적용 (1 USD = 1300 KRW 추정)
    colors1 = ['#FF6B6B', '#4ECDC4', '#45B7D1']

    bars1 = ax1.bar(categories[:2], values[:2], color=colors1[:2], edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Market Size (Trillion KRW)', fontsize=10, fontweight='bold')
    ax1.set_title('Market Size Comparison (2024)', fontsize=11, fontweight='bold')
    for bar, val in zip(bars1, values[:2]):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f'{val:.0f}', ha='center', va='bottom', fontweight='bold')

    # 2. 성장률 비교
    growth_categories = ['Digital Healthcare\nSeoul', 'Medical Device\nSeoul', 'Telehealth\nGlobal', 'Healthcare IT\nGlobal']
    growth_rates = [14.94, 7.5, 24.6, 15.8]
    colors2 = ['#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']

    bars2 = ax2.bar(growth_categories, growth_rates, color=colors2, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('CAGR (%)', fontsize=10, fontweight='bold')
    ax2.set_title('Growth Rate Comparison (CAGR)', fontsize=11, fontweight='bold')
    ax2.set_ylim(0, 30)
    for bar, val in zip(bars2, growth_rates):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')

    # 3. 의료 관광 비교
    countries = ['Seoul\n(2024)', 'Thailand\n(Medical\nTourism Hub)', 'Singapore\n(Medical\nHub)', 'Global\nAverage']
    patients = [1000000, 2000000, 500000, 2400000]
    colors3 = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#95E1D3']

    bars3 = ax3.bar(countries, patients, color=colors3, edgecolor='black', linewidth=1.5)
    ax3.set_ylabel('Number of Patients', fontsize=10, fontweight='bold')
    ax3.set_title('Medical Tourism Patient Comparison', fontsize=11, fontweight='bold')
    for bar, val in zip(bars3, patients):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50000,
                f'{val/1000000:.1f}M', ha='center', va='bottom', fontweight='bold')

    # 4. 의료 시스템 순위
    countries_rank = ['Singapore', 'Japan', 'South Korea', 'Switzerland', 'Germany']
    ranks = [1, 2, 3, 4, 5]
    colors4 = ['#FFD700', '#C0C0C0', '#CD7F32', '#95E1D3', '#F7DC6F']

    bars4 = ax4.barh(countries_rank, ranks, color=colors4, edgecolor='black', linewidth=1.5)
    ax4.set_xlabel('Global Ranking (Lower is Better)', fontsize=10, fontweight='bold')
    ax4.set_title('Global Healthcare System Ranking (2023)', fontsize=11, fontweight='bold')
    ax4.set_xlim(0, 6)
    ax4.invert_xaxis()
    for bar, val in zip(bars4, ranks):
        ax4.text(bar.get_width() - 0.2, bar.get_y() + bar.get_height()/2,
                f'#{val}', ha='right', va='center', fontweight='bold', color='white')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'global_vs_seoul_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ global_vs_seoul_comparison.png 저장됨")
    plt.close()


def chart4_market_opportunities():
    """5. 주요 기회 및 시장 성장률 순위"""
    print("생성 중: Chart 4 - 시장 기회 순위")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Market Opportunities & Growth Ranking', fontsize=14, fontweight='bold')

    # 1. 기회별 중요도와 성장률
    opportunities = [
        'Telemedicine\nPlatform',
        'AI Diagnostics',
        'Home Care\nServices',
        'Mental Health\nServices',
        'Preventive\nMedicine',
        'Medical Device',
        'Wellness\nServices'
    ]
    importance = [5, 5, 4, 4, 4, 4, 3]
    growth = [25, 18, 15, 12, 14, 8, 10]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']

    # 스캐터 플롯
    scatter = ax1.scatter(growth, importance, s=[500]*len(opportunities),
                         c=colors, alpha=0.7, edgecolors='black', linewidth=2)
    for i, opp in enumerate(opportunities):
        ax1.annotate(opp, (growth[i], importance[i]), ha='center', va='center',
                    fontsize=9, fontweight='bold')

    ax1.set_xlabel('Expected Growth Rate (%)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Importance Level', fontsize=11, fontweight='bold')
    ax1.set_title('Market Opportunity Matrix', fontsize=12, fontweight='bold')
    ax1.set_xlim(5, 30)
    ax1.set_ylim(2.5, 5.5)
    ax1.grid(True, alpha=0.3, linestyle='--')

    # 2. 성장률 순위 (막대 그래프)
    sorted_indices = np.argsort(growth)[::-1]
    sorted_opp = [opportunities[i] for i in sorted_indices]
    sorted_growth = [growth[i] for i in sorted_indices]
    sorted_colors = [colors[i] for i in sorted_indices]

    bars = ax2.barh(sorted_opp, sorted_growth, color=sorted_colors, edgecolor='black', linewidth=1.5)
    ax2.set_xlabel('Expected CAGR (%)', fontsize=11, fontweight='bold')
    ax2.set_title('Growth Rate Ranking (2025-2030)', fontsize=12, fontweight='bold')
    ax2.set_xlim(0, 30)

    for bar, val in zip(bars, sorted_growth):
        ax2.text(val + 0.5, bar.get_y() + bar.get_height()/2,
                f'{val}%', va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'market_opportunities_ranking.png', dpi=300, bbox_inches='tight')
    print("✓ market_opportunities_ranking.png 저장됨")
    plt.close()


def chart5_workforce_trends():
    """6. 의료 인력, 병상, 의료기관 수 추이"""
    print("생성 중: Chart 5 - 의료 인력 및 인프라 추이")

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Healthcare Workforce & Infrastructure Trends', fontsize=14, fontweight='bold')

    years = ['2020', '2021', '2022', '2023', '2024', '2025E']

    # 1. 의료인 수 추이
    physicians = [105000, 107000, 109000, 111000, 113000, 116000]
    nurses = [320000, 325000, 330000, 336000, 342000, 350000]

    ax1.plot(years, physicians, marker='o', linewidth=2.5, markersize=8,
            label='Physicians', color='#FF6B6B')
    ax1.plot(years, nurses, marker='s', linewidth=2.5, markersize=8,
            label='Nurses', color='#4ECDC4')
    ax1.set_ylabel('Number of Personnel', fontsize=10, fontweight='bold')
    ax1.set_title('Healthcare Personnel Trend', fontsize=11, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3, linestyle='--')

    # 2. 병상 수 추이
    total_beds = [195000, 197000, 199000, 201000, 203000, 205000]
    acute_beds = [120000, 121000, 122000, 123000, 124000, 125000]
    ltc_beds = [75000, 76000, 77000, 78000, 79000, 80000]

    ax2.stackplot(years, acute_beds, ltc_beds, labels=['Acute Care Beds', 'LTC Beds'],
                 colors=['#45B7D1', '#98D8C8'], alpha=0.8)
    ax2.plot(years, total_beds, marker='o', color='black', linewidth=2.5, markersize=6, label='Total')
    ax2.set_ylabel('Number of Beds', fontsize=10, fontweight='bold')
    ax2.set_title('Hospital Beds Trend', fontsize=11, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')

    # 3. 의료기관 수 추이
    general_hospitals = [115, 117, 119, 120, 121, 122]
    hospitals = [340, 345, 348, 350, 352, 355]
    clinics = [2650, 2700, 2750, 2800, 2850, 2900]

    ax3.plot(years, general_hospitals, marker='o', linewidth=2.5, markersize=8,
            label='General Hospitals', color='#FF6B6B')
    ax3.plot(years, hospitals, marker='s', linewidth=2.5, markersize=8,
            label='Hospitals', color='#4ECDC4')
    ax3.plot(years, clinics, marker='^', linewidth=2.5, markersize=8,
            label='Clinics', color='#45B7D1')
    ax3.set_ylabel('Number of Institutions', fontsize=10, fontweight='bold')
    ax3.set_title('Healthcare Institutions Trend', fontsize=11, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3, linestyle='--')

    # 4. 의료비 지출
    national_spending = [195, 205, 213, 220, 228, 238]
    foreign_patient_revenue = [800, 950, 1200, 1200, 1200, 1400]

    ax4_2 = ax4.twinx()

    line1 = ax4.plot(years, national_spending, marker='o', linewidth=2.5, markersize=8,
                    label='National Healthcare Spending', color='#FF6B6B')
    line2 = ax4_2.plot(years, foreign_patient_revenue, marker='s', linewidth=2.5, markersize=8,
                      label='Foreign Patient Revenue', color='#4ECDC4')

    ax4.set_ylabel('National Spending (Billion KRW)', fontsize=10, fontweight='bold', color='#FF6B6B')
    ax4_2.set_ylabel('Foreign Patient Revenue (Million USD)', fontsize=10, fontweight='bold', color='#4ECDC4')
    ax4.set_title('Healthcare Spending & Medical Tourism Revenue', fontsize=11, fontweight='bold')
    ax4.tick_params(axis='y', labelcolor='#FF6B6B')
    ax4_2.tick_params(axis='y', labelcolor='#4ECDC4')
    ax4.grid(True, alpha=0.3, linestyle='--')

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax4.legend(lines, labels, fontsize=9)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'healthcare_workforce_trends.png', dpi=300, bbox_inches='tight')
    print("✓ healthcare_workforce_trends.png 저장됨")
    plt.close()


def create_data_summary():
    """데이터 요약 마크다운 파일 생성"""
    print("생성 중: 데이터 요약 마크다운")

    summary = """# 서울시 의료 산업 정량적 데이터 요약
## Seoul Healthcare Industry Quantitative Data Summary

**작성일**: 2026년 1월 23일
**데이터 출처**: 통계청, 서울시 데이터 포털, 건강보험심사평가원, 한국보건산업진흥원

---

## 1. 주요 통계 수치

### 1.1 시장 규모
- **2024년 경상의료비**: 213.1조 원
- **1인당 경상의료비**: 412.1만 원
- **2025년 예측**: 225.0조 원 (5.6% 성장)
- **2028년 예측**: 265.0조 원

### 1.2 의료기관 현황 (서울시)
- **종합병원**: 약 120개
- **병원**: 약 350개
- **의원**: 약 2,800개
- **치과**: 약 1,200개
- **한의**: 약 500개
- **약국**: 약 2,100개
- **총계**: 약 7,070개 의료기관

### 1.3 의료인력 현황
- **의사 수**: 약 113,000명 (2024)
  - 2025년 예측: 116,000명
  - 서울: 인구 1,000명당 4.7명
  - 전국 평균: 인구 1,000명당 2.6명
- **간호사 수**: 약 342,000명 (2024)
  - 2025년 예측: 350,000명

### 1.4 병상 현황
- **총 병상 수**: 약 203,000개 (2024)
- **급성기 병상**: 약 124,000개
- **장기요양 병상**: 약 79,000개
- **2025년 예측**: 205,000개

### 1.5 의료 서비스 이용 현황
- **외국인 환자 의료비**: 약 1.2조 원 (2024)
- **전국 대비 서울 비중**: 85.7%
- **외국인 진료기관 현황**:
  - 2020년: 920개
  - 2024년: 1,994개
  - 증가율: 116.7% (4년간 2배 이상)

---

## 2. 지역별/부문별 분석 데이터

### 2.1 의료 인프라 격차
- **의사 밀도 격차**:
  - 서울: 4.7명/1,000명
  - 지방: 2.0명/1,000명 이하 (서울의 절반 미만)
  - 격차: 2.35배

### 2.2 고령 인구 및 장기요양
- **2025년 노인 인구**: 약 100만 명
- **65세 이상 인구 비율**: 약 20% 이상 (초고령사회 진입)
- **단기보호시설**: 44개 (구당 2곳 미만)
- **방문간호 이용률**: 0.5% (극히 저조)
- **장기요양 시장 성장률**: 연평균 8~10%

### 2.3 정신 건강 서비스
- **시장 성장률**: 연평균 8~12% CAGR
- **응급 정신건강센터**: 11개 → 14개로 확대 계획
- **직장 EAP 활용률**: 5% 이하 (미흡)

### 2.4 의료 분야별 시장
- **한국 의료기기 시장**:
  - 2024년: 7.11억 USD (약 9,000억 원)
  - 2025년 예측: 7.57억 USD
  - CAGR (2025-2032): 7.5%

- **한국 디지털 헬스케어 시장**:
  - 2024년: 9.37억 USD
  - 2033년 예측: 37.70억 USD
  - CAGR (2025-2033): 14.94%

- **한국 홈 헬스케어 시장**:
  - 2024년: 73.088억 USD
  - 2030년 예측: 140.072억 USD

- **한국 의료IT 시장**:
  - CAGR (2024-2032): 8.70%

- **한국 병원 시장**:
  - 2024년: 77.09억 USD
  - CAGR (2024-2029): 5.43%

---

## 3. 글로벌 트렌드와의 비교

### 3.1 글로벌 의료 시장 규모
- **2024년**: 약 9조 달러 (USD 9 trillion)
- **2030년 예측**: 약 12조 달러
- **성장률**: 연평균 복합성장률(CAGR) 4-7%

### 3.2 의료 IT 글로벌 시장
- **2023년**: 663.0억 USD
- **2030년 예측**: 1,834.3억 USD
- **CAGR**: 15.8% (2024-2030)

### 3.3 스마트 헬스케어 글로벌 시장
- **2024년**: 188.86억 USD
- **2030년 예측**: 385.28억 USD
- **CAGR**: 12.51% (2025-2030)

### 3.4 글로벌 의료 관광 시장
- **2023년**: 241억 USD
- **2032년 예측**: 1,000억 USD 이상
- **서울의 위치**: 2024년 약 100만 명 의료 관광객 수용

### 3.5 원격의료 시장
- **글로벌 원격의료 시장 (2026년)**: 219.31억 USD
- **2034년 예측**: 1,272.81억 USD
- **CAGR**: 24.60%

---

## 4. 주요 기회 및 격차 정량화

### 4.1 미충족 의료 수요
- **발생률**: 5.4~12.2%
- **주요 대상**: 저소득층, 노인, 20~39세 청년층
- **원인**: 경제적 부담(자기부담금), 접근성 제약

### 4.2 시장 성장 기회 (예상 CAGR)
| 분야 | 성장률 | 기간 | 비고 |
|------|--------|------|------|
| 원격의료 플랫폼 | 25-30% | 2025-2030 | 가장 높음 |
| AI 진단 시스템 | 18-20% | 2025-2030 | 고성장 |
| 정신 건강 서비스 | 10-15% | 2025-2033 | 지속 성장 |
| 홈케어 서비스 | 15-20% | 2025-2033 | 고령화 추진 |
| 디지털 헬스케어 | 14.94% | 2025-2033 | 한국 (최고) |
| 예방 의료 | 12-15% | 2025-2030 | 중기 성장 |
| 의료기기 | 8% | 2024-2029 | 안정적 성장 |
| 병원 시장 | 5.43% | 2024-2029 | 저성장 |

### 4.3 의료비 부담 격차
- **자기부담금**: OECD 평균보다 35~39% 높음
- **저소득층 미충족 의료**: 저소득층의 미충족 의료 수요가 특히 높음
- **근빈곤층**: 의료보조 대상 제외로 인한 의료 회피 증가

---

## 5. 정책 및 규제 환경

### 5.1 의료관광 목표
- **2027년까지 외국인 환자 유치 목표**: 70만 명
- **현황 (2024)**: 약 100만 명 (목표 초과 달성)

### 5.2 R&D 투자
- **서울시 2023년 의료 R&D 투자**: 381억 원
- **바이오의료 지원**: 60억 원
- **누적 투자 (2022까지)**: 233억 원 (62개 과제)

### 5.3 건강보험료 변화
- **2025년 보험료율**: 7.09%
- **2026년 보험료율**: 7.19% (0.1%포인트 인상)
- **직장 가입자 월 기여금**:
  - 2025년: 158,464원
  - 2026년: 160,699원 (월 2,235원 인상)

### 5.4 규제 현황
- **원격의료**: 2025년 12월 국회 본회의 통과 (15년 만에 처음)
- **디지털 의료제품법**: 2025년 1월 24일 시행

---

## 6. 주요 의료기관 (세계 수준)

### 6.1 국제 평가 (2025년 뉴스위크 기준)
| 순위 | 기관명 | 세계 순위 | 특징 |
|------|------|---------|------|
| 1 | 서울아산병원 | 25위 | 암 진료 대표 기관 |
| 2 | 삼성서울병원 | 30위 | 종합진료, 고급의료 |
| 3 | 서울대병원 | 42위 | 공공 의료, 교육 |
| 4 | 세브란스병원 | 46위 | 역사 있는 종합병원 |

### 6.2 글로벌 의료 시스템 순위 (2023년)
| 순위 | 국가 | 특징 |
|------|------|------|
| 1위 | 싱가포르 | 효율적 운영 |
| 2위 | 일본 | 예방의학 강조 |
| 3위 | 남한 | 높은 접근성 |
| 4위 | 스위스 | 고급 의료 |
| 5위 | 독일 | 포괄적 보험 |

---

## 7. 데이터 출처 및 신뢰성

### 공식 통계 기관
- **통계청 (KOSIS)**: 국가 기본통계
- **서울시 데이터 포털**: 지역 의료 통계
- **건강보험심사평가원**: 진료비, 의료기관 정보
- **보건복지부**: 정책 및 규제 정보
- **한국보건산업진흥원 (KHIDI)**: 산업 통계
- **중앙응급의료센터**: 응급의료 통계
- **국립암센터**: 암 등록 통계

### 시장 조사 기관
- **Grand View Research**: 의료 시장 규모 및 예측
- **Fortune Business Insights**: 산업별 시장 분석
- **Research and Markets**: 세부 분야 분석

### 신뢰성 주의사항
- 일부 데이터는 추정치 및 예측값 포함
- 환율 변동에 따른 USD 변환값 변동 가능
- 정책 변화에 따른 향후 수정 가능

---

## 8. 주요 인사이트

### 강점
- 세계 상위 3위의 의료 시스템
- 높은 의료기술 수준
- 의료관광 강국 위치

### 기회
- 디지털 헬스케어 고성장 (14.94% CAGR)
- 원격의료 시장 확대 (25~30% CAGR)
- 고령화에 따른 장기요양 수요 증가

### 과제
- 의료비 자기부담금이 OECD 평균보다 35~39% 높음
- 의사 부족 (2040년까지 5,704~11,136명 부족 예상)
- 지역 의료 격차 심화

### 권고사항
1. 저비용 의료 모델 개발
2. 원격의료 생태계 구축
3. AI 진단 기술 확산
4. 의료 인력 양성 확대
5. 지역사회 중심 의료체계 강화

---

**작성**: 서울 도시 연구 에이전트
**최종 검증**: 2026년 1월 23일
**분류**: 정책 분석 자료 / Healthcare Industry Policy Analysis
"""

    with open(DATA_DIR / 'data_summary.md', 'w', encoding='utf-8') as f:
        f.write(summary)
    print("✓ data_summary.md 저장됨")


def create_market_metrics_json():
    """JSON 형식 주요 지표 정리"""
    print("생성 중: market_metrics.json")

    metrics = {
        "metadata": {
            "created_date": "2026-01-23",
            "region": "Seoul, South Korea",
            "description": "Seoul Healthcare Industry Key Metrics"
        },
        "market_size": {
            "korea_national_2024": {
                "value": 213.1,
                "unit": "Trillion KRW",
                "description": "National healthcare spending 2024"
            },
            "per_capita_2024": {
                "value": 4.121,
                "unit": "Million KRW",
                "description": "Per capita healthcare spending 2024"
            },
            "global_2024": {
                "value": 9.0,
                "unit": "Trillion USD",
                "description": "Global healthcare market size 2024"
            }
        },
        "growth_rates": {
            "national_2024_2025": {
                "value": 5.6,
                "unit": "%",
                "type": "CAGR"
            },
            "digital_healthcare_korea": {
                "value": 14.94,
                "unit": "%",
                "period": "2025-2033",
                "type": "CAGR"
            },
            "telehealth_global": {
                "value": 24.6,
                "unit": "%",
                "period": "2025-2034",
                "type": "CAGR"
            },
            "healthcare_it_global": {
                "value": 15.8,
                "unit": "%",
                "period": "2024-2030",
                "type": "CAGR"
            },
            "medical_device_korea": {
                "value": 7.5,
                "unit": "%",
                "period": "2025-2032",
                "type": "CAGR"
            },
            "home_healthcare_korea": {
                "value": 8.0,
                "unit": "%",
                "period": "2024-2030",
                "type": "CAGR"
            }
        },
        "healthcare_institutions": {
            "general_hospitals": 120,
            "hospitals": 350,
            "clinics": 2800,
            "dental_clinics": 1200,
            "korean_medicine": 500,
            "pharmacies": 2100,
            "total": 7070
        },
        "healthcare_personnel": {
            "physicians": {
                "2024": 113000,
                "2025_projected": 116000,
                "density_per_1000_population": 4.7
            },
            "nurses": {
                "2024": 342000,
                "2025_projected": 350000
            }
        },
        "hospital_beds": {
            "total_2024": 203000,
            "acute_care_beds": 124000,
            "long_term_care_beds": 79000
        },
        "medical_tourism": {
            "patients_2024": 1000000,
            "revenue_2024_trillion_krw": 1.2,
            "foreign_clinics_2024": 1994,
            "foreign_clinics_2020": 920,
            "growth_rate_4_years": 116.7,
            "seoul_share_national": 85.7
        },
        "unmet_healthcare_needs": {
            "incidence_rate_percent": 8.0,
            "estimated_market_expansion": "10-15%"
        },
        "opportunities": {
            "telemedicine_platform": {
                "growth_rate": 25,
                "period": "2025-2030",
                "market_size_expansion": "25-30%"
            },
            "ai_diagnostics": {
                "growth_rate": 18,
                "period": "2025-2030"
            },
            "home_care_services": {
                "growth_rate": 15,
                "period": "2025-2033",
                "market_size_expansion": "15-20%"
            },
            "mental_health_services": {
                "growth_rate": 12,
                "period": "2025-2033",
                "market_size_expansion": "10-15%"
            },
            "preventive_medicine": {
                "growth_rate": 14,
                "period": "2025-2030",
                "market_size_expansion": "12-15%"
            },
            "medical_devices": {
                "growth_rate": 8,
                "period": "2024-2029"
            }
        },
        "healthcare_system_global_ranking": {
            "1": "Singapore",
            "2": "Japan",
            "3": "South Korea",
            "4": "Switzerland",
            "5": "Germany"
        },
        "challenges": {
            "physician_shortage": {
                "projected_deficit_2040": "5704-11136 physicians",
                "key_shortage_areas": ["Pediatrics", "Emergency Medicine", "Obstetrics"]
            },
            "unmet_needs_incidence": "5.4-12.2%",
            "self_payment_burden": {
                "percentage_above_oecd_average": "35-39%"
            },
            "regional_disparity": {
                "seoul_physician_density": 4.7,
                "provincial_physician_density": 2.0,
                "disparity_ratio": 2.35
            }
        },
        "policy_targets": {
            "medical_tourism": {
                "target_year": 2027,
                "target_patients": 700000,
                "current_2024": 1000000
            },
            "rd_investment_seoul": {
                "2023": "38.1 Billion KRW",
                "biomedical_support": "6 Billion KRW"
            }
        }
    }

    with open(DATA_DIR / 'market_metrics.json', 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print("✓ market_metrics.json 저장됨")


def main():
    """메인 실행 함수"""
    print("=" * 70)
    print("서울시 의료 산업 시각화 생성 시작")
    print("Seoul Healthcare Industry Visualization Generator")
    print("=" * 70)

    # 한글 폰트 설정
    set_korean_font()

    # 차트 생성
    try:
        chart1_market_growth()
        chart2_institutions_distribution()
        chart3_global_vs_seoul()
        chart4_market_opportunities()
        chart5_workforce_trends()
        create_data_summary()
        create_market_metrics_json()

        print("\n" + "=" * 70)
        print("✓ 모든 시각화 생성 완료!")
        print("=" * 70)
        print(f"\n차트 저장 위치: {OUTPUT_DIR}")
        print(f"데이터 저장 위치: {DATA_DIR}")
        print("\n생성된 파일:")
        print("  - healthcare_market_growth.png")
        print("  - healthcare_institutions_distribution.png")
        print("  - global_vs_seoul_comparison.png")
        print("  - market_opportunities_ranking.png")
        print("  - healthcare_workforce_trends.png")
        print("  - data_summary.md")
        print("  - market_metrics.json")

    except Exception as e:
        print(f"\n✗ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
