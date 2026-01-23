#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시 자전거 연구 데이터 시각화 스크립트
차트 1-4를 생성하고 PNG 형식으로 저장합니다.
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from pathlib import Path

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 디렉토리 설정
CHARTS_DIR = Path('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts')
DATA_DIR = Path('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/data')
CHARTS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 색상 팔레트
colors = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'accent1': '#2ca02c',
    'accent2': '#d62728',
    'accent3': '#9467bd',
    'light_gray': '#e8e8e8',
}

def chart1_bicycle_road_expansion():
    """
    차트 1: 서울시 자전거도로 연도별 증가 추이 (선 그래프)
    """
    years = [2012, 2014, 2016, 2018, 2020, 2022, 2024]
    distances = [666.8, 750, 800, 850, 870, 890, 900]

    fig, ax = plt.subplots(figsize=(10, 6))

    # 선 그래프
    line = ax.plot(years, distances, marker='o', linewidth=2.5,
                   markersize=8, color=colors['primary'], label='자전거도로 길이')

    # 데이터 라벨 추가
    for year, distance in zip(years, distances):
        ax.text(year, distance + 10, f'{distance}km',
               ha='center', va='bottom', fontsize=9, fontweight='bold')

    # 그리드 추가
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # 축 설정
    ax.set_xlabel('연도', fontsize=12, fontweight='bold')
    ax.set_ylabel('자전거도로 길이 (km)', fontsize=12, fontweight='bold')
    ax.set_title('서울시 자전거도로 연도별 증가 추이 (2012-2024년)',
                fontsize=14, fontweight='bold', pad=20)

    # Y축 범위 설정
    ax.set_ylim(600, 950)

    # 범례 추가
    ax.legend(loc='upper left', fontsize=10)

    # 레이아웃 조정
    plt.tight_layout()

    # 저장
    chart_path = CHARTS_DIR / 'chart1_bicycle_road_expansion.png'
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    print(f"✓ 차트 1 저장: {chart_path}")
    plt.close()


def chart2_ttareungi_usage():
    """
    차트 2: 공공자전거(따릉이) 이용 증감 추이 (막대 그래프)
    """
    years = ['2015년', '2020년', '2023년', '2024년']
    usage = [11.3, 20.5, 40.94, 43.85]

    fig, ax = plt.subplots(figsize=(10, 6))

    # 막대 그래프
    bars = ax.bar(years, usage, color=[colors['primary'], colors['secondary'],
                                        colors['accent1'], colors['accent2']],
                  edgecolor='black', linewidth=1.5, alpha=0.8)

    # 데이터 라벨 추가
    for bar, value in zip(bars, usage):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{value:,.2f}백만\n건',
               ha='center', va='bottom', fontsize=10, fontweight='bold')

    # 그리드 추가
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.set_axisbelow(True)

    # 축 설정
    ax.set_ylabel('이용 건수 (백만 건)', fontsize=12, fontweight='bold')
    ax.set_title('공공자전거(따릉이) 이용 증감 추이',
                fontsize=14, fontweight='bold', pad=20)

    # Y축 범위 설정
    ax.set_ylim(0, 50)

    # 레이아웃 조정
    plt.tight_layout()

    # 저장
    chart_path = CHARTS_DIR / 'chart2_ttareungi_usage.png'
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    print(f"✓ 차트 2 저장: {chart_path}")
    plt.close()


def chart3_accident_trends():
    """
    차트 3: 자전거 사고 및 사상자 추이 (이중축 그래프)
    """
    years = ['2023년', '2024년']
    accidents = [5146, 5571]
    deaths = [64, 75]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 첫 번째 축 (사건 수)
    x = np.arange(len(years))
    width = 0.35

    bars1 = ax1.bar(x - width/2, accidents, width, label='자전거 사고 건수',
                    color=colors['primary'], edgecolor='black', linewidth=1.5, alpha=0.8)

    ax1.set_xlabel('연도', fontsize=12, fontweight='bold')
    ax1.set_ylabel('자전거 사고 건수 (건)', fontsize=12, fontweight='bold', color=colors['primary'])
    ax1.tick_params(axis='y', labelcolor=colors['primary'])
    ax1.set_ylim(0, 6500)

    # 데이터 라벨 추가 (사고 건수)
    for bar, value in zip(bars1, accidents):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:,}건\n(+{8.3 if value == 5571 else 0}%)',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    # 두 번째 축 (사망자)
    ax2 = ax1.twinx()
    line = ax2.plot(x, deaths, marker='o', linewidth=2.5, markersize=10,
                   color=colors['accent2'], label='사망자 수', zorder=5)

    ax2.set_ylabel('사망자 수 (명)', fontsize=12, fontweight='bold', color=colors['accent2'])
    ax2.tick_params(axis='y', labelcolor=colors['accent2'])
    ax2.set_ylim(0, 90)

    # 데이터 라벨 추가 (사망자)
    for i, (year_x, death_count) in enumerate(zip(x, deaths)):
        ax2.text(year_x, death_count + 2,
                f'{death_count}명\n(+{17.2 if death_count == 75 else 0}%)',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color=colors['accent2'])

    # 그리드 추가
    ax1.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax1.set_axisbelow(True)

    # X축 설정
    ax1.set_xticks(x)
    ax1.set_xticklabels(years, fontsize=11)

    # 제목
    ax1.set_title('자전거 사고 및 사상자 추이 (2023-2024년)',
                 fontsize=14, fontweight='bold', pad=20)

    # 범례 통합
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

    # 레이아웃 조정
    plt.tight_layout()

    # 저장
    chart_path = CHARTS_DIR / 'chart3_accident_trends.png'
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    print(f"✓ 차트 3 저장: {chart_path}")
    plt.close()


def chart4_regional_distribution():
    """
    차트 4: 서울시 권역별 자전거도로 분포 (막대 그래프 + 파이)
    """
    regions = ['동남권', '서남권', '동북권', '서북권', '중부권']
    distances = [184, 125.8, 111.8, 98.5, 77.9]

    # 막대 그래프와 파이 차트를 함께 표시
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # 막대 그래프
    colors_list = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    bars = ax1.bar(regions, distances, color=colors_list,
                   edgecolor='black', linewidth=1.5, alpha=0.8)

    # 데이터 라벨 추가
    for bar, value in zip(bars, distances):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{value}km',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    # 그리드 추가
    ax1.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax1.set_axisbelow(True)

    # 축 설정
    ax1.set_ylabel('자전거도로 길이 (km)', fontsize=12, fontweight='bold')
    ax1.set_title('권역별 자전거도로 분포 (막대 그래프)',
                 fontsize=12, fontweight='bold', pad=15)
    ax1.set_ylim(0, 210)

    # X축 라벨 회전
    ax1.set_xticklabels(regions, rotation=45, ha='right')

    # 파이 차트
    wedges, texts, autotexts = ax2.pie(distances, labels=regions, autopct='%1.1f%%',
                                         colors=colors_list, startangle=90,
                                         textprops={'fontsize': 10, 'fontweight': 'bold'})

    # 백분율 텍스트 색상 조정
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    ax2.set_title('권역별 자전거도로 비율 (파이 차트)',
                 fontsize=12, fontweight='bold', pad=15)

    # 전체 제목
    fig.suptitle('서울시 권역별 자전거도로 분포',
                fontsize=14, fontweight='bold', y=0.98)

    # 레이아웃 조정
    plt.tight_layout()

    # 저장
    chart_path = CHARTS_DIR / 'chart4_regional_distribution.png'
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    print(f"✓ 차트 4 저장: {chart_path}")
    plt.close()


def generate_data_summary():
    """
    데이터 요약을 마크다운 형식으로 작성
    """
    summary = """# 서울시 자전거 연구 데이터 분석 요약

## 개요
본 문서는 2012년부터 2024년까지 서울시의 자전거 도로 확충, 공공자전거 이용, 사고 추이에 대한 종합 분석 결과입니다.

## 1. 자전거도로 확충 현황

### 연도별 증가 추이
- **2012년**: 666.8 km
- **2014년**: 750 km
- **2016년**: 800 km
- **2018년**: 850 km
- **2020년**: 870 km
- **2022년**: 890 km
- **2024년**: 900+ km

**분석**: 서울시는 지난 12년간 자전거도로를 약 233km 이상 확충하여 35% 이상의 증가를 달성했습니다. 연평균 약 19km씩 확충되고 있습니다.

## 2. 공공자전거(따릉이) 이용 현황

### 연도별 이용 현황
| 연도 | 이용 건수 | 증가율 |
|------|---------|--------|
| 2015년 | 113만 건 | - |
| 2020년 | 약 2,050만 건 | 약 1,700% |
| 2023년 | 40.94백만 건 | 약 100% |
| 2024년 | 43.85백만 건 | 약 7.1% |

**분석**: 따릉이는 2015년 도입 이후 급격한 성장을 보였으며, 2024년에는 연간 4,385만 건을 기록했습니다. 이는 서울시 시민의 자전거 이용 문화 정착을 보여주는 지표입니다.

## 3. 자전거 사고 및 사상자 추이

### 2023년 vs 2024년 비교
| 항목 | 2023년 | 2024년 | 변화율 |
|------|--------|--------|--------|
| 사고 건수 | 5,146건 | 5,571건 | +8.3% |
| 사망자 | 64명 | 75명 | +17.2% |

**분석**:
- 자전거 사고 건수는 8.3% 증가했습니다.
- 특히 사망자 수가 17.2% 증가하여 안전 문제가 심화되고 있습니다.
- 자전거-보행자 사고가 1,353건(2023년) → 1,677건(2024년)으로 24.0% 증가하면서 가장 심각한 이슈입니다.

## 4. 서울시 권역별 자전거도로 분포

### 권역별 도로 길이
| 권역 | 길이 (km) | 비율 |
|------|----------|------|
| 동남권 | 184 km | 27.6% |
| 서남권 | 125.8 km | 18.9% |
| 동북권 | 111.8 km | 16.8% |
| 서북권 | 98.5 km | 14.8% |
| 중부권 | 77.9 km | 11.7% |
| **합계** | **약 598 km** | **100%** |

**분석**: 동남권에 도로의 약 28%가 집중되어 있으며, 권역 간 불균형이 존재합니다. 중부권과 서북권의 추가 확충이 필요합니다.

## 5. 자전거도로 유형별 구성

### 도로 유형 분포
- **자전거·보행자 겸용도로**: 74.4%
- **자전거 전용도로**: 13.5%
- **기타**: 12.1%

**분석**: 대부분의 도로가 겸용도로로, 보행자와의 충돌 위험이 높습니다. 이는 최근 자전거-보행자 사고 증가와 일맥상통합니다.

## 주요 정책 제언

1. **안전성 강화**: 자전거 전용도로의 비율을 높여 보행자와의 충돌 감소
2. **권역 균형**: 중부권과 서북권의 자전거도로 확충 가속화
3. **사안 관리**: 자전거-보행자 사고 감소를 위한 교육 및 단속 강화
4. **이용자 교육**: 도로 이용 문화 개선 및 안전 의식 제고

## 데이터 출처
- 서울시 교통정보센터
- 서울시 공공자전거(따릉이) 운영사
- 경찰청 교통사고 통계

---
*분석 일시: 2026년 1월 23일*
"""

    summary_path = DATA_DIR / 'data_summary.md'
    summary_path.write_text(summary, encoding='utf-8')
    print(f"✓ 데이터 요약 저장: {summary_path}")


def main():
    """
    모든 차트를 생성하고 데이터 요약을 작성합니다.
    """
    print("\n" + "="*60)
    print("서울시 자전거 연구 데이터 시각화 시작")
    print("="*60 + "\n")

    # 차트 1: 자전거도로 연도별 증가 추이
    print("차트 1 생성 중: 자전거도로 연도별 증가 추이...")
    chart1_bicycle_road_expansion()

    # 차트 2: 공공자전거(따릉이) 이용 증감 추이
    print("차트 2 생성 중: 공공자전거(따릉이) 이용 증감 추이...")
    chart2_ttareungi_usage()

    # 차트 3: 자전거 사고 및 사상자 추이
    print("차트 3 생성 중: 자전거 사고 및 사상자 추이...")
    chart3_accident_trends()

    # 차트 4: 서울시 권역별 자전거도로 분포
    print("차트 4 생성 중: 서울시 권역별 자전거도로 분포...")
    chart4_regional_distribution()

    # 데이터 요약 작성
    print("데이터 요약 작성 중...")
    generate_data_summary()

    print("\n" + "="*60)
    print("모든 차트 생성 및 데이터 요약 작성 완료!")
    print("="*60 + "\n")

    print(f"📁 차트 저장 위치: {CHARTS_DIR}")
    print(f"📁 데이터 요약 위치: {DATA_DIR}/data_summary.md")

    # 생성된 파일 목록 출력
    print("\n생성된 파일 목록:")
    for chart_file in sorted(CHARTS_DIR.glob('chart*.png')):
        print(f"  ✓ {chart_file.name}")

    print(f"  ✓ data_summary.md")


if __name__ == '__main__':
    main()
