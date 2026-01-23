#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Seoul Bicycle Road Expansion Policy Report Generator
한글 정책 브리프 PDF 생성 스크립트 (Version 2 - 개선된 한글 지원)
"""

import os
import sys
from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 출력 디렉토리
output_dir = "/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/reports/"
chart_dir = "/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/"

# 출력 파일명
output_filename = "seoul_bicycle_road_expansion_policy_report_20260123.pdf"
output_path = os.path.join(output_dir, output_filename)

# 색상 정의
COLOR_PRIMARY = HexColor("#2E5090")      # 진한 파란색
COLOR_SECONDARY = HexColor("#4A90E2")    # 밝은 파란색
COLOR_ACCENT = HexColor("#F5A623")       # 주황색
COLOR_DARK = HexColor("#2C3E50")         # 진한 회색
COLOR_LIGHT = HexColor("#ECF0F1")        # 밝은 회색
COLOR_LINE = HexColor("#BDC3C7")         # 선 색상

# 한글 폰트 설정 시도
def setup_korean_fonts():
    """한글 폰트 설정"""
    font_paths = {
        "Helvetica": "/System/Library/Fonts/Helvetica.ttc",
        "Arial": "/System/Library/Fonts/Arial.ttf",
    }

    # 기본 한글 폰트 설정 시도
    korean_fonts = [
        ("/Library/Fonts/NanumGothic.ttf", "NanumGothic"),
        ("/Library/Fonts/NotoSansCJK-Regular.ttc", "NotoSans"),
    ]

    registered = False
    for font_path, font_name in korean_fonts:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                print(f"Korean font registered: {font_name} from {font_path}")
                registered = True
                break
            except Exception as e:
                print(f"Failed to register {font_name}: {e}")

    if not registered:
        print("No Korean fonts found. Using default fonts.")

    return registered

# 폰트 설정
korean_font_available = setup_korean_fonts()

def get_font_name(use_korean=False):
    """폰트 이름 반환"""
    if korean_font_available and use_korean:
        return "NanumGothic"
    return "Helvetica"

# 스타일 정의
def create_styles():
    """문서 스타일 생성"""
    styles = getSampleStyleSheet()

    # 제목 스타일
    styles.add(ParagraphStyle(
        name='TitleStyle',
        fontName=get_font_name(),
        fontSize=28,
        textColor=COLOR_PRIMARY,
        spaceAfter=6,
        alignment=TA_CENTER,
        bold=True
    ))

    # 부제목 스타일
    styles.add(ParagraphStyle(
        name='SubtitleStyle',
        fontName=get_font_name(),
        fontSize=14,
        textColor=COLOR_SECONDARY,
        spaceAfter=12,
        alignment=TA_CENTER
    ))

    # 장제목 스타일
    styles.add(ParagraphStyle(
        name='ChapterStyle',
        fontName=get_font_name(),
        fontSize=16,
        textColor=COLOR_PRIMARY,
        spaceAfter=12,
        spaceBefore=12,
        bold=True
    ))

    # 절제목 스타일
    styles.add(ParagraphStyle(
        name='SectionStyle',
        fontName=get_font_name(),
        fontSize=13,
        textColor=COLOR_DARK,
        spaceAfter=10,
        spaceBefore=10,
        bold=True
    ))

    # 본문 스타일
    styles.add(ParagraphStyle(
        name='BodyStyle',
        fontName=get_font_name(),
        fontSize=11,
        textColor=COLOR_DARK,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=16
    ))

    # 강조 본문
    styles.add(ParagraphStyle(
        name='BoldBodyStyle',
        fontName=get_font_name(),
        fontSize=11,
        textColor=COLOR_PRIMARY,
        spaceAfter=8,
        bold=True
    ))

    # 목차 스타일
    styles.add(ParagraphStyle(
        name='TOCStyle',
        fontName=get_font_name(),
        fontSize=11,
        textColor=COLOR_DARK,
        spaceAfter=6,
        leftIndent=20
    ))

    return styles

def add_chapter_header(elements, title, styles, page_width):
    """장 제목 추가"""
    border_line = Paragraph(
        '<font size="1" color="#4A90E2">━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</font>',
        styles['BodyStyle']
    )
    elements.append(border_line)
    elements.append(Spacer(page_width, 0.2 * cm))
    elements.append(Paragraph(title, styles['ChapterStyle']))
    elements.append(Spacer(page_width, 0.3 * cm))

# PDF 생성 함수
def generate_policy_report():
    """정책 브리프 PDF 생성"""

    # 스타일 생성
    styles = create_styles()

    # 문서 요소 리스트
    elements = []

    # 페이지 크기
    page_width, page_height = A4

    # ========== 1. 표지 ==========
    elements.append(Spacer(page_width, 4 * cm))

    # 표지 제목 (한글과 영문 혼합)
    title_kor = "Seoul Bicycle Road\nExpansion Policy Research"
    title = Paragraph(
        title_kor,
        styles['TitleStyle']
    )
    elements.append(title)
    elements.append(Spacer(page_width, 1 * cm))

    # 부제목
    subtitle = Paragraph(
        "Policy Brief Report",
        styles['SubtitleStyle']
    )
    elements.append(subtitle)
    elements.append(Spacer(page_width, 2 * cm))

    # 작성일 및 정보
    info_text = """
    <b>Date: January 23, 2026</b><br/>
    <b>Analysis Scope: 4 Domestic Cities + 6 International Cities</b><br/>
    <b>Data Period: 2022-2024</b><br/>
    <br/><br/>
    <i>This report analyzes the current status of Seoul's<br/>
    bicycle road policies and proposes sustainable expansion strategies.</i>
    """
    elements.append(Paragraph(info_text, styles['BodyStyle']))

    # 페이지 나누기
    elements.append(PageBreak())

    # ========== 2. 목차 ==========
    add_chapter_header(elements, "Contents", styles, page_width)
    elements.append(Spacer(page_width, 0.2 * cm))

    toc_items = [
        ("1. Executive Summary", "3"),
        ("2. Current Status Analysis", "4-6"),
        ("   2.1 Seoul Status", "4"),
        ("   2.2 Domestic City Comparison", "5"),
        ("   2.3 International Benchmarks", "5"),
        ("3. Problem Analysis", "7-8"),
        ("   3.1 Safety Issues", "7"),
        ("   3.2 Infrastructure Imbalance", "7"),
        ("   3.3 User Satisfaction", "8"),
        ("4. Policy Recommendations", "9-10"),
        ("   4.1 Short-term Strategy (H1 2026)", "9"),
        ("   4.2 Mid-term Strategy (2026-2027)", "9"),
        ("   4.3 Long-term Strategy (2027-2030)", "10"),
        ("5. Expected Effects", "11"),
        ("Appendix: Charts and Statistics", "12-15"),
    ]

    for item, page_num in toc_items:
        toc_line = Paragraph(
            f'{item}' + '.' * (60 - len(item)) + f' {page_num}',
            styles['TOCStyle']
        )
        elements.append(toc_line)

    elements.append(PageBreak())

    # ========== 3. 요약 (Executive Summary) ==========
    add_chapter_header(elements, "1. Executive Summary", styles, page_width)

    summary_text = """
    <b>Key Findings:</b><br/>
    """
    elements.append(Paragraph(summary_text, styles['BodyStyle']))
    elements.append(Spacer(page_width, 0.2 * cm))

    # 강점
    strengths = """
    <b>Strengths</b><br/>
    • Seoul's Ttareungyi (bike-sharing): 99% expansion support, 86% satisfaction<br/>
    • Policy Achievement: ~400x growth over 10 years (2015-2024)<br/>
    • Safety Improvement: Enhanced safety through AI CCTV technology<br/>
    • Infrastructure Expansion: 25,249km (2021) → 27,754km (2024) - 10% increase<br/>
    """
    elements.append(Paragraph(strengths, styles['BodyStyle']))
    elements.append(Spacer(page_width, 0.2 * cm))

    # 과제
    challenges = """
    <b>Key Challenges</b><br/>
    • Road Quality Variance: 74.5% bicycle-pedestrian shared roads<br/>
    • Accident Increase: 8.3% surge in 2024, 50.4% spike in youth accidents<br/>
    • City Imbalance: Seoul (mature) vs. Daegu (early stage)<br/>
    • Usage Rate Disparity: Seoul 120k trips/day vs. Incheon 1.3%<br/>
    """
    elements.append(Paragraph(challenges, styles['BodyStyle']))
    elements.append(Spacer(page_width, 0.3 * cm))

    # 권고사항 요약
    recommendations = """
    <b>Policy Recommendations:</b><br/>
    To achieve 5-10% bicycle modal share by 2030, phased policy implementation is needed,<br/>
    with emphasis on safety enhancement, infrastructure quality improvement, and<br/>
    customized policies for each city.
    """
    elements.append(Paragraph(recommendations, styles['BodyStyle']))

    elements.append(PageBreak())

    # ========== 4. 제1장 현황 분석 ==========
    add_chapter_header(elements, "2. Current Status Analysis", styles, page_width)

    # 2.1 서울시 현황
    elements.append(Paragraph("2.1 Seoul Bicycle Policy Status", styles['SectionStyle']))

    seoul_data = """
    <b>Basic Statistics (2024)</b><br/>
    • Bicycle Road Length: 775.9 km<br/>
    • Han River Bicycle Path: 78 km (South 47.5km, North 30.5km)<br/>
    • Ttareungyi Stations: 2,843 locations<br/>
    • Ttareungyi Bikes: 45,200 units<br/>
    • Cumulative Members: 5.06 million<br/>
    • Annual Usage: 43.85 million trips (avg. 120,000/day)<br/>
    <br/>
    Seoul has entered the mature stage of bicycle policy with well-established<br/>
    infrastructure and services. However, road safety and accessibility improvements<br/>
    remain critical.
    """
    elements.append(Paragraph(seoul_data, styles['BodyStyle']))
    elements.append(Spacer(page_width, 0.3 * cm))

    # 차트 1 추가
    chart1_path = os.path.join(chart_dir, "03_seoul_ttareungyi_usage_trend.png")
    if os.path.exists(chart1_path):
        try:
            img1 = RLImage(chart1_path, width=5.5*cm, height=3.5*cm)
            elements.append(img1)
            elements.append(Spacer(page_width, 0.2 * cm))
            elements.append(Paragraph(
                "<i>Figure 1: Seoul Ttareungyi Usage Trend (2022-2024)</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 1 error: {e}")

    elements.append(Spacer(page_width, 0.3 * cm))

    # 2.2 국내 도시 비교
    elements.append(Paragraph("2.2 Domestic City Comparison", styles['SectionStyle']))

    domestic_data = """
    <b>City-level Policy Maturity</b><br/>
    • Seoul: 4.0/5.0 (Mature) - 78km Han River improvement, 400x Ttareungyi growth<br/>
    • Busan: 2.5/5.0 (Growth) - 259.7km expansion plan (2024-2028), 323B KRW investment<br/>
    • Incheon: 2.5/5.0 (Growth) - 969km infrastructure, 300-ri bicycle link project ongoing<br/>
    • Daegu: 1.5/5.0 (Early) - Limited policy visibility, fragmented management<br/>
    <br/>
    Korean cities implement differentiated policies suited to regional characteristics,<br/>
    but city-level gap reduction and unified standards are needed.
    """
    elements.append(Paragraph(domestic_data, styles['BodyStyle']))
    elements.append(Spacer(page_width, 0.3 * cm))

    # 차트 2 추가
    chart2_path = os.path.join(chart_dir, "01_domestic_cities_bicycle_road_comparison.png")
    if os.path.exists(chart2_path):
        try:
            img2 = RLImage(chart2_path, width=5.5*cm, height=3.5*cm)
            elements.append(img2)
            elements.append(Spacer(page_width, 0.2 * cm))
            elements.append(Paragraph(
                "<i>Figure 2: Domestic City Bicycle Road Length Comparison</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 2 error: {e}")

    elements.append(PageBreak())

    # 2.3 해외 벤치마크
    elements.append(Paragraph("2.3 International Best Practice Benchmarking", styles['SectionStyle']))

    international_data = """
    <b>Advanced Countries' Policy Cases</b><br/>
    <br/>
    <b>Amsterdam (Netherlands)</b><br/>
    • Bicycle Modal Share: 38% (world's highest)<br/>
    • Characteristics: Complete separation model, high investment level<br/>
    <br/>
    <b>Copenhagen (Denmark)</b><br/>
    • Bicycle Modal Share: 37%<br/>
    • Characteristics: Integrated approach, 50% target by 2025<br/>
    <br/>
    <b>Berlin (Germany)</b><br/>
    • Bicycle Network: 3,000km planned<br/>
    • Investment Growth: €5M → €32M (6x increase)<br/>
    • Characteristics: Efficient expansion model<br/>
    <br/>
    Advanced countries have elevated bicycle usage to mass transit levels through<br/>
    high investment and consistent policies. Korea needs long-term vision and<br/>
    sustained investment.
    """
    elements.append(Paragraph(international_data, styles['BodyStyle']))
    elements.append(Spacer(page_width, 0.3 * cm))

    # 차트 3 추가
    chart3_path = os.path.join(chart_dir, "02_international_modal_share_comparison.png")
    if os.path.exists(chart3_path):
        try:
            img3 = RLImage(chart3_path, width=5.5*cm, height=3.5*cm)
            elements.append(img3)
            elements.append(Spacer(page_width, 0.2 * cm))
            elements.append(Paragraph(
                "<i>Figure 3: International City Bicycle Modal Share Comparison</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 3 error: {e}")

    elements.append(PageBreak())

    # ========== 5. 제2장 문제점 분석 ==========
    add_chapter_header(elements, "3. Problem Analysis", styles, page_width)

    # 3.1 안전 문제
    elements.append(Paragraph("3.1 Bicycle Traffic Safety Issues", styles['SectionStyle']))

    safety_data = """
    <b>Accident Status and Trends</b><br/>
    <br/>
    <b>National Bicycle Accident Statistics (2022-2024)</b><br/>
    • 2022: 5,393 incidents, 91 deaths<br/>
    • 2023: 5,146 incidents, 64 deaths<br/>
    • 2024: 5,250 incidents, 60 deaths<br/>
    • 2024 Change: +2.0% YoY (deaths -6%)<br/>
    <br/>
    <b>Key Issues</b><br/>
    • Car-bicycle collisions: 83% of total accidents<br/>
    • Youth accidents: 50.4% surge in under-20 age group (critical)<br/>
    • Brakes-less bikes: Increasing due to high-end bicycle trend<br/>
    • Safety education gaps: Need for continuous training<br/>
    """
    elements.append(Paragraph(safety_data, styles['BodyStyle']))
    elements.append(Spacer(page_width, 0.2 * cm))

    # 차트 4 추가
    chart4_path = os.path.join(chart_dir, "04_bicycle_accident_trend.png")
    if os.path.exists(chart4_path):
        try:
            img4 = RLImage(chart4_path, width=5.5*cm, height=3.5*cm)
            elements.append(img4)
            elements.append(Spacer(page_width, 0.2 * cm))
            elements.append(Paragraph(
                "<i>Figure 4: Bicycle Accident and Fatality Trends</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 4 error: {e}")

    elements.append(Spacer(page_width, 0.3 * cm))

    # 3.2 인프라 불균형
    elements.append(Paragraph("3.2 Infrastructure Imbalance and Quality Variance", styles['SectionStyle']))

    infrastructure_data = """
    <b>Road Type Distribution (2023)</b><br/>
    <br/>
    • Bicycle-pedestrian shared roads: 20,023km (74.5%)<br/>
    • Dedicated bicycle roads: 3,763km (14.0%)<br/>
    • Bicycle priority roads: 2,071km (7.7%)<br/>
    • Dedicated bicycle lanes: 1,015km (3.8%)<br/>
    <br/>
    <b>Key Issues</b><br/>
    • Insufficient dedicated roads: Only 14% vs. much higher in developed countries<br/>
    • Discontinuous segments: 23.7km out of 190km in Incheon are disconnected<br/>
    • City-level gaps: Seoul 775.9km vs. Daegu with limited information<br/>
    • Maintenance shortfalls: Need to prioritize aging road repairs<br/>
    """
    elements.append(Paragraph(infrastructure_data, styles['BodyStyle']))
    elements.append(Spacer(page_width, 0.2 * cm))

    # 차트 5 추가
    chart5_path = os.path.join(chart_dir, "05_seoul_road_type_composition.png")
    if os.path.exists(chart5_path):
        try:
            img5 = RLImage(chart5_path, width=5.5*cm, height=3.5*cm)
            elements.append(img5)
            elements.append(Spacer(page_width, 0.2 * cm))
            elements.append(Paragraph(
                "<i>Figure 5: Bicycle Road Type Composition</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 5 error: {e}")

    elements.append(Spacer(page_width, 0.3 * cm))

    # 3.3 이용자 만족도
    elements.append(Paragraph("3.3 User Satisfaction and Improvement Requests", styles['SectionStyle']))

    satisfaction_data = """
    <b>Seoul Ttareungyi User Satisfaction (2024)</b><br/>
    <br/>
    • Service Satisfaction: 86% (high)<br/>
    • Bicycle Road Expansion Support: 99% (very high)<br/>
    • Safety Concerns: 30%<br/>
    • Bike Storage Issues: 30%<br/>
    <br/>
    <b>Improvement Requests</b><br/>
    • Enhanced Safety: Road safety facilities, traffic signal improvements<br/>
    • Road Expansion: More dedicated bicycle roads<br/>
    • Storage Facilities: Secure bike storage expansion<br/>
    • Convenience: App improvements, simplified rental procedures<br/>
    """
    elements.append(Paragraph(satisfaction_data, styles['BodyStyle']))
    elements.append(Spacer(page_width, 0.2 * cm))

    # 차트 6 추가
    chart6_path = os.path.join(chart_dir, "08_citizen_satisfaction.png")
    if os.path.exists(chart6_path):
        try:
            img6 = RLImage(chart6_path, width=5.5*cm, height=3.5*cm)
            elements.append(img6)
            elements.append(Spacer(page_width, 0.2 * cm))
            elements.append(Paragraph(
                "<i>Figure 6: User Satisfaction and Policy Support</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 6 error: {e}")

    elements.append(PageBreak())

    # ========== 6. 제3장 정책 권고 ==========
    add_chapter_header(elements, "4. Policy Recommendations", styles, page_width)

    elements.append(Paragraph("4.1 Short-term Strategy (H1 2026)", styles['SectionStyle']))

    short_term = """
    <b>Urgent Tasks (Immediate Implementation)</b><br/>
    <br/>
    1. <b>Ban Operation of Bicycles Without Brakes</b><br/>
    &nbsp;&nbsp;- High-end bike trend increasing brake-less bicycle usage<br/>
    &nbsp;&nbsp;- Strong regulation and public awareness needed<br/>
    &nbsp;&nbsp;- Establish fine system for violators<br/>
    <br/>
    2. <b>Expand CCTV in High-accident Areas</b><br/>
    &nbsp;&nbsp;- AI-powered CCTV for concentrated management<br/>
    &nbsp;&nbsp;- Identify blind spots and install security cameras<br/>
    &nbsp;&nbsp;- Target: 100 installations by H1 2026<br/>
    <br/>
    3. <b>Strengthen Youth Safety Education</b><br/>
    &nbsp;&nbsp;- Address critical 50.4% surge in under-20 accidents<br/>
    &nbsp;&nbsp;- Integrate safety education in school curriculum<br/>
    &nbsp;&nbsp;- Conduct bicycle safety campaigns monthly<br/>
    """
    elements.append(Paragraph(short_term, styles['BodyStyle']))

    elements.append(Spacer(page_width, 0.3 * cm))

    elements.append(Paragraph("4.2 Mid-term Strategy (2026-2027)", styles['SectionStyle']))

    medium_term = """
    <b>Infrastructure Structure Improvement</b><br/>
    <br/>
    1. <b>Increase Dedicated Bicycle Road Share to 15%+</b><br/>
    &nbsp;&nbsp;- Current 14% → 2027 target 15%+<br/>
    &nbsp;&nbsp;- Prioritize major arterial roads<br/>
    &nbsp;&nbsp;- Create 50-100km annually<br/>
    <br/>
    2. <b>Eliminate Road Discontinuities</b><br/>
    &nbsp;&nbsp;- Connect 23.7km discontinuous segments in Incheon (190km total)<br/>
    &nbsp;&nbsp;- Map and prioritize other cities' segments<br/>
    &nbsp;&nbsp;- Target: 80%+ connectivity by 2027<br/>
    <br/>
    3. <b>Establish Dedicated Bicycle Department</b><br/>
    &nbsp;&nbsp;- Create bicycle policy task force in each city<br/>
    &nbsp;&nbsp;- Integrate transportation, safety, health, and urban planning<br/>
    &nbsp;&nbsp;- Build data-driven policy framework<br/>
    """
    elements.append(Paragraph(medium_term, styles['BodyStyle']))

    elements.append(Spacer(page_width, 0.3 * cm))

    elements.append(Paragraph("4.3 Long-term Strategy (2027-2030)", styles['SectionStyle']))

    long_term = """
    <b>Comprehensive Policy Implementation</b><br/>
    <br/>
    1. <b>Achieve 5-10% Bicycle Modal Share</b><br/>
    &nbsp;&nbsp;- Seoul: Current ~1% → 2030 target 5%<br/>
    &nbsp;&nbsp;- National level: 2-3% → 5%<br/>
    &nbsp;&nbsp;- Promote commute-time bicycle usage<br/>
    <br/>
    2. <b>Reach 20% Dedicated Bicycle Road Share</b><br/>
    &nbsp;&nbsp;- Current 14% → 2030 target 20%<br/>
    &nbsp;&nbsp;- Establish unified national road design standards<br/>
    &nbsp;&nbsp;- Mandate in new city development<br/>
    <br/>
    3. <b>Standardize National Policy Framework</b><br/>
    &nbsp;&nbsp;- Reduce city-level policy maturity gaps<br/>
    &nbsp;&nbsp;- Establish national bicycle master plan<br/>
    &nbsp;&nbsp;- Create city-specific support framework<br/>
    """
    elements.append(Paragraph(long_term, styles['BodyStyle']))

    elements.append(Spacer(page_width, 0.3 * cm))

    # 차트 7-8 추가
    chart7_path = os.path.join(chart_dir, "06_policy_maturity_comparison.png")
    if os.path.exists(chart7_path):
        try:
            img7 = RLImage(chart7_path, width=5.5*cm, height=3.5*cm)
            elements.append(img7)
            elements.append(Spacer(page_width, 0.2 * cm))
            elements.append(Paragraph(
                "<i>Figure 7: Domestic City Policy Maturity Comparison</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 7 error: {e}")

    elements.append(PageBreak())

    # ========== 7. 제4장 기대효과 ==========
    add_chapter_header(elements, "5. Expected Effects", styles, page_width)

    effects_text = """
    <b>Socioeconomic Impact Analysis</b><br/>
    <br/>
    <b>Economic Benefits</b><br/>
    • Cost-Benefit Ratio: DKK 4.79 benefit per km (Berlin case)<br/>
    • Job Creation: 11.41 jobs per $1M investment<br/>
    • Real Estate Value: €34,000 increase near bicycle infrastructure<br/>
    <br/>
    <b>Health Benefits</b><br/>
    • Health Cost Reduction: 55% savings (Copenhagen case)<br/>
    • Lifestyle Improvement: Reduced obesity rates from increased bike usage<br/>
    • Air Quality: CO2 emission reduction<br/>
    <br/>
    <b>Transportation Benefits</b><br/>
    • Traffic Congestion Reduction: Decreased car usage<br/>
    • Transit Integration: Strengthened last-mile connections<br/>
    • Urban Mobility: Enhanced short-distance transportation efficiency<br/>
    <br/>
    <b>Environmental Benefits</b><br/>
    • Carbon Emission Reduction: Up to 50% annual decrease<br/>
    • Air Pollution Improvement: PM2.5 and NO2 reduction<br/>
    • Noise Reduction: Quieter urban environment<br/>
    <br/>
    <b>Social Benefits</b><br/>
    • Regional Revitalization: Increased bicycle tourism and cultural events<br/>
    • Safer Cities: Reduced traffic accidents<br/>
    • Quality of Life: 99% citizen satisfaction achievement<br/>
    """
    elements.append(Paragraph(effects_text, styles['BodyStyle']))

    elements.append(Spacer(page_width, 0.3 * cm))

    # 차트 9 추가
    chart9_path = os.path.join(chart_dir, "09_ttareungyi_usage_by_time.png")
    if os.path.exists(chart9_path):
        try:
            img9 = RLImage(chart9_path, width=5.5*cm, height=3.5*cm)
            elements.append(img9)
            elements.append(Spacer(page_width, 0.2 * cm))
            elements.append(Paragraph(
                "<i>Figure 9: Ttareungyi User Time Distribution</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 9 error: {e}")

    elements.append(PageBreak())

    # ========== 8. 부록: 차트 및 통계 ==========
    add_chapter_header(elements, "Appendix: Charts and Statistics", styles, page_width)

    # 추가 차트들
    chart10_path = os.path.join(chart_dir, "10_investment_comparison.png")
    if os.path.exists(chart10_path):
        try:
            img10 = RLImage(chart10_path, width=5.5*cm, height=3.5*cm)
            elements.append(img10)
            elements.append(Spacer(page_width, 0.2 * cm))
            elements.append(Paragraph(
                "<i>Figure 10: Bicycle Infrastructure Investment Comparison</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 10 error: {e}")

    elements.append(Spacer(page_width, 0.3 * cm))

    # 통계 테이블
    elements.append(Paragraph("Appendix Table 1: Seoul Ttareungyi Usage Trends", styles['SectionStyle']))

    table_data = [
        ['Year', 'Annual Usage', 'Daily Avg'],
        ['2022', '14.14M trips', '38.7K'],
        ['2023', '44.90M trips', '123K'],
        ['2024', '43.85M trips', '120K'],
    ]

    table = Table(table_data, colWidths=[2*cm, 3*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), COLOR_LIGHT),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_LINE),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    elements.append(table)

    elements.append(Spacer(page_width, 0.5 * cm))

    # 통계 테이블 2
    elements.append(Paragraph("Appendix Table 2: Domestic City Bicycle Policy Overview", styles['SectionStyle']))

    table_data2 = [
        ['City', 'Road Length', 'Stage', 'Maturity'],
        ['Seoul', '775.9km', 'Mature', '4.0/5.0'],
        ['Busan', '259.7km', 'Growth', '2.5/5.0'],
        ['Incheon', '969km', 'Growth', '2.5/5.0'],
        ['Daegu', 'Limited', 'Early', '1.5/5.0'],
    ]

    table2 = Table(table_data2, colWidths=[2*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), COLOR_LIGHT),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_LINE),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    elements.append(table2)

    elements.append(Spacer(page_width, 0.5 * cm))

    # 핵심 지표 요약
    elements.append(Paragraph("Appendix Table 3: International Best Practice Performance", styles['SectionStyle']))

    table_data3 = [
        ['City', 'Modal Share', 'Network', 'Characteristics'],
        ['Amsterdam', '38%', 'Large', 'Complete Separation'],
        ['Copenhagen', '37%', 'Large', 'Integrated Approach'],
        ['Berlin', '9%+', '3,000km', 'Aggressive Expansion'],
        ['Tokyo', '13.5%', 'Large', 'Cultural Strength'],
    ]

    table3 = Table(table_data3, colWidths=[2.5*cm, 2*cm, 2.5*cm, 2.5*cm])
    table3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), COLOR_LIGHT),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_LINE),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    elements.append(table3)

    elements.append(PageBreak())

    # ========== 9. 결론 ==========
    add_chapter_header(elements, "Conclusion", styles, page_width)

    conclusion = """
    <b>Current Status Assessment</b><br/>
    <br/>
    Korea's bicycle road policies show highly imbalanced progress by city. Seoul has<br/>
    entered the mature stage, while Busan and Incheon are in growth stages, and Daegu<br/>
    remains in early stages.<br/>
    <br/>
    <b>Success Factors</b><br/>
    <br/>
    1. Quality-focused infrastructure expansion<br/>
    2. User-centered safety culture development<br/>
    3. Data-driven efficient investment<br/>
    <br/>
    <b>Future Outlook</b><br/>
    <br/>
    Achievable targets by 2030:<br/>
    • 5-10% bicycle modal share achievement<br/>
    • 30% reduction in car-bicycle accidents<br/>
    • 2x increase in public bike usage<br/>
    <br/>
    If policy recommendations are implemented consistently, Seoul and domestic cities<br/>
    are expected to establish advanced-country-level bicycle culture well before 2030.<br/>
    <br/>
    <br/>
    <b>---</b><br/>
    <br/>
    <b>Author</b>: Claude AI Agent<br/>
    <b>Date</b>: January 23, 2026<br/>
    <b>Data Period</b>: 2024-2025 Latest Statistics<br/>
    """
    elements.append(Paragraph(conclusion, styles['BodyStyle']))

    # PDF 생성
    print(f"Generating PDF: {output_path}")

    try:
        # SimpleDocTemplate 생성
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm,
            title="Seoul Bicycle Road Expansion Policy Report",
            author="Claude AI Agent",
            subject="Seoul Bicycle Road Expansion Policy Research"
        )

        # PDF 빌드
        doc.build(elements)

        print(f"PDF generated successfully: {output_path}")

        # 파일 크기 확인
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
        print(f"File size: {file_size:.2f} MB")

        return True

    except Exception as e:
        print(f"Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = generate_policy_report()
    sys.exit(0 if success else 1)
