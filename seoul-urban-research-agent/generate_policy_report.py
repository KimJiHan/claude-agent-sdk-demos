#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Seoul Bicycle Road Expansion Policy Report Generator
한글 정책 브리프 PDF 생성 스크립트
"""

import os
import sys
from datetime import datetime
from io import BytesIO
from PIL import Image

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1
from reportlab.lib.units import cm, inch
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak, Table, TableStyle
from reportlab.lib import colors

# 한글 폰트 설정
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Mac에서 시스템 폰트 경로
font_paths = [
    "/Library/Fonts/NanumGothic.ttf",
    "/System/Library/Fonts/Supplemental/NanumGothic.ttf",
    "/usr/local/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/Arial.ttf"
]

# 사용 가능한 한글 폰트 찾기
korean_font_path = None
for path in font_paths:
    if os.path.exists(path):
        korean_font_path = path
        print(f"Using font: {path}")
        break

if korean_font_path:
    try:
        pdfmetrics.registerFont(TTFont("NanumGothic", korean_font_path))
        pdfmetrics.registerFont(TTFont("NanumGothicBold", korean_font_path))
    except Exception as e:
        print(f"Font registration error: {e}")
        print("Falling back to default fonts")
else:
    print("Warning: Korean font not found. Using default fonts.")

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

# 글꼴 설정
def get_font(name="NanumGothic", size=11, bold=False):
    """글꼴 설정"""
    if bold and korean_font_path:
        return f"{name}"
    elif korean_font_path:
        return f"{name}"
    else:
        return "Helvetica"

# 스타일 정의
def create_styles():
    """문서 스타일 생성"""
    styles = getSampleStyleSheet()

    # 제목 스타일
    styles.add(ParagraphStyle(
        name='TitleStyle',
        fontName=get_font(),
        fontSize=28,
        textColor=COLOR_PRIMARY,
        spaceAfter=6,
        alignment=TA_CENTER,
        bold=True
    ))

    # 부제목 스타일
    styles.add(ParagraphStyle(
        name='SubtitleStyle',
        fontName=get_font(),
        fontSize=14,
        textColor=COLOR_SECONDARY,
        spaceAfter=12,
        alignment=TA_CENTER
    ))

    # 장제목 스타일
    styles.add(ParagraphStyle(
        name='ChapterStyle',
        fontName=get_font(),
        fontSize=16,
        textColor=COLOR_PRIMARY,
        spaceAfter=12,
        spaceBefore=12,
        bold=True,
        borderColor=COLOR_SECONDARY,
        borderWidth=2,
        borderPadding=8
    ))

    # 절제목 스타일
    styles.add(ParagraphStyle(
        name='SectionStyle',
        fontName=get_font(),
        fontSize=13,
        textColor=COLOR_DARK,
        spaceAfter=10,
        spaceBefore=10,
        bold=True
    ))

    # 본문 스타일
    styles.add(ParagraphStyle(
        name='BodyStyle',
        fontName=get_font(),
        fontSize=11,
        textColor=COLOR_DARK,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=16
    ))

    # 강조 본문
    styles.add(ParagraphStyle(
        name='BoldBodyStyle',
        fontName=get_font(),
        fontSize=11,
        textColor=COLOR_PRIMARY,
        spaceAfter=8,
        bold=True
    ))

    # 목차 스타일
    styles.add(ParagraphStyle(
        name='TOCStyle',
        fontName=get_font(),
        fontSize=11,
        textColor=COLOR_DARK,
        spaceAfter=6,
        leftIndent=20
    ))

    return styles


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

    # 표지 제목
    title = Paragraph(
        "서울시 자전거 도로 확충 정책 연구",
        styles['TitleStyle']
    )
    elements.append(title)
    elements.append(Spacer(page_width, 1 * cm))

    # 부제목
    subtitle = Paragraph(
        "정책 브리프 보고서",
        styles['SubtitleStyle']
    )
    elements.append(subtitle)
    elements.append(Spacer(page_width, 2 * cm))

    # 작성일 및 정보
    info_text = f"""
    <font face="{get_font()}" size="11">
    <b>작성일: 2026년 1월 23일</b><br/>
    <b>분석 범위: 국내 4개 도시 + 해외 6개 도시</b><br/>
    <b>데이터 기준: 2022-2024년</b><br/>
    <br/><br/>
    <i>본 보고서는 서울시 자전거 도로 정책의 현황을 분석하고<br/>
    지속가능한 확충 정책을 제안합니다.</i>
    </font>
    """
    elements.append(Paragraph(info_text, styles['BodyStyle']))

    # 페이지 나누기
    elements.append(PageBreak())

    # ========== 2. 목차 ==========
    elements.append(Paragraph("목차", styles['ChapterStyle']))
    elements.append(Spacer(page_width, 0.5 * cm))

    toc_items = [
        ("1. 요약 (Executive Summary)", "3"),
        ("2. 현황 분석", "4-6"),
        ("   2.1 서울시 현황", "4"),
        ("   2.2 국내 도시 비교", "5"),
        ("   2.3 해외 벤치마크", "5"),
        ("3. 문제점 분석", "7-8"),
        ("   3.1 안전 문제", "7"),
        ("   3.2 인프라 불균형", "7"),
        ("   3.3 이용자 만족도", "8"),
        ("4. 정책 권고", "9-10"),
        ("   4.1 단기 전략 (2026년 상반기)", "9"),
        ("   4.2 중기 전략 (2026-2027년)", "9"),
        ("   4.3 장기 전략 (2027-2030년)", "10"),
        ("5. 기대효과", "11"),
        ("부록: 차트 및 통계", "12-15"),
    ]

    for item, page_num in toc_items:
        toc_line = Paragraph(
            f'<b>{item}</b><font color="{COLOR_PRIMARY}">{"."*(50-len(item))} {page_num}</font>',
            styles['TOCStyle']
        )
        elements.append(toc_line)

    elements.append(PageBreak())

    # ========== 3. 요약 (Executive Summary) ==========
    elements.append(Paragraph("1. 요약 (Executive Summary)", styles['ChapterStyle']))
    elements.append(Spacer(page_width, 0.3 * cm))

    summary_text = """
    <b>주요 발견사항:</b><br/>
    """
    elements.append(Paragraph(summary_text, styles['BodyStyle']))
    elements.append(Spacer(page_width, 0.2 * cm))

    # 강점
    strengths = """
    <b>✓ 강점</b><br/>
    • 서울시 따릉이: 시민 99% 확충 지지도, 86% 만족도 달성<br/>
    • 정책 성과: 10년간 약 400배 성장 (2015-2024년)<br/>
    • 안전 개선: AI CCTV 등 기술 활용으로 안전성 강화<br/>
    • 인프라 확충: 2021년 25,249km → 2024년 27,754km (10% 증가)<br/>
    """
    elements.append(Paragraph(strengths, styles['BodyStyle']))
    elements.append(Spacer(page_width, 0.2 * cm))

    # 과제
    challenges = """
    <b>⚠ 주요 과제</b><br/>
    • 도로 질 편차: 자전거·보행자 겸용도로 74.5%로 높음<br/>
    • 사고 증가: 2024년 자전거 사고 8.3% 증가, 청소년 50.4% 급증<br/>
    • 도시별 불균형: 서울(성숙기) vs 대구(초기 단계)<br/>
    • 이용률 차이: 서울 12만건/일 vs 인천 1.3%<br/>
    """
    elements.append(Paragraph(challenges, styles['BodyStyle']))
    elements.append(Spacer(page_width, 0.3 * cm))

    # 권고사항 요약
    recommendations = """
    <b>정책 권고:</b><br/>
    2030년까지 자전거 모달 셰어 5-10% 달성을 위해 단계적 정책 추진이 필요하며,<br/>
    특히 안전성 강화, 인프라 질적 개선, 도시별 맞춤형 정책이 핵심입니다.
    """
    elements.append(Paragraph(recommendations, styles['BodyStyle']))

    elements.append(PageBreak())

    # ========== 4. 제1장 현황 분석 ==========
    elements.append(Paragraph("2. 현황 분석", styles['ChapterStyle']))
    elements.append(Spacer(page_width, 0.3 * cm))

    # 2.1 서울시 현황
    elements.append(Paragraph("2.1 서울시 자전거 정책 현황", styles['SectionStyle']))

    seoul_data = """
    <b>기본 통계 (2024년)</b><br/>
    • 자전거 도로 길이: 775.9 km<br/>
    • 한강 자전거도로: 78 km (강남 47.5km, 강북 30.5km)<br/>
    • 따릉이 대여소: 2,843개소<br/>
    • 따릉이 자전거: 45,200대<br/>
    • 누적 회원: 506만 명<br/>
    • 연간 이용: 43.85백만 건 (일평균 120,000건)<br/>
    <br/>
    서울시는 자전거 정책이 성숙기에 진입했으며, 공공자전거 서비스와 인프라가<br/>
    높은 수준으로 구축되었습니다. 다만, 도로 안전성과 접근성 개선이 계속 필요합니다.
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
                "<i>그림 1: 서울시 따릉이 이용 추이 (2022-2024)</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 1 error: {e}")

    elements.append(Spacer(page_width, 0.3 * cm))

    # 2.2 국내 도시 비교
    elements.append(Paragraph("2.2 국내 도시별 비교 분석", styles['SectionStyle']))

    domestic_data = """
    <b>도시별 정책 성숙도</b><br/>
    • 서울: 4.0/5.0 (성숙기) - 한강 78km 개선, 따릉이 400배 성장<br/>
    • 부산: 2.5/5.0 (성장기) - 259.7km 확충 계획 (2024-2028), 323억 원 투자<br/>
    • 인천: 2.5/5.0 (성장기) - 969km 인프라, 300리 자전거 이음길 진행 중<br/>
    • 대구: 1.5/5.0 (초기) - 정책 가시성 부족, 분산 관리 체계<br/>
    <br/>
    국내 도시들은 지역 특성에 맞는 차별화된 정책을 추진하고 있으나,<br/>
    도시 간 격차 해소와 통일된 표준화가 필요합니다.
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
                "<i>그림 2: 국내 도시별 자전거 도로 길이 비교</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 2 error: {e}")

    elements.append(PageBreak())

    # 2.3 해외 벤치마크
    elements.append(Paragraph("2.3 해외 선진 정책 벤치마크", styles['SectionStyle']))

    international_data = """
    <b>자전거 선진국의 정책 사례</b><br/>
    <br/>
    <b>암스테르담 (네덜란드)</b><br/>
    • 자전거 모달 셰어: 38% (세계 최고 수준)<br/>
    • 특징: 완전 분리형 모델, 높은 투자 수준<br/>
    <br/>
    <b>코펜하겐 (덴마크)</b><br/>
    • 자전거 모달 셰어: 37%<br/>
    • 특징: 통합적 접근, 2025년 50% 목표<br/>
    <br/>
    <b>베를린 (독일)</b><br/>
    • 자전거 네트워크: 3,000km 계획<br/>
    • 투자 확대: €5M → €32M (6배 증가)<br/>
    • 특징: 효율적 확대 모델<br/>
    <br/>
    해외 선진국들은 높은 투자와 정책 일관성으로 자전거 이용을 대중교통 수준으로<br/>
    향상시켰으며, 한국도 장기적 비전과 지속적 투자가 필요합니다.
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
                "<i>그림 3: 해외 주요 도시의 자전거 모달 셰어 비교</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 3 error: {e}")

    elements.append(PageBreak())

    # ========== 5. 제2장 문제점 분석 ==========
    elements.append(Paragraph("3. 문제점 분석", styles['ChapterStyle']))
    elements.append(Spacer(page_width, 0.3 * cm))

    # 3.1 안전 문제
    elements.append(Paragraph("3.1 자전거 교통사고 안전 문제", styles['SectionStyle']))

    safety_data = """
    <b>사고 현황 및 추이</b><br/>
    <br/>
    <b>전국 자전거 사고 통계 (2022-2024)</b><br/>
    • 2022년: 5,393건, 사망자 91명<br/>
    • 2023년: 5,146건, 사망자 64명<br/>
    • 2024년: 5,250건, 사망자 60명<br/>
    • 2024년 증감: 전년 대비 +2.0% (사망자는 -6% 감소)<br/>
    <br/>
    <b>주요 문제점</b><br/>
    • 자동차 대 자전거 사고: 전체의 83%<br/>
    • 청소년 사고: 20세 이하 50.4% 급증 (매우 심각)<br/>
    • 제동장치 없는 자전거: 고급 자전거의 유행으로 증가<br/>
    • 안전교육 부족: 지속적인 교육 강화 필요<br/>
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
                "<i>그림 4: 자전거 교통사고 및 사망자 추이</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 4 error: {e}")

    elements.append(Spacer(page_width, 0.3 * cm))

    # 3.2 인프라 불균형
    elements.append(Paragraph("3.2 인프라 불균형 및 질적 편차", styles['SectionStyle']))

    infrastructure_data = """
    <b>도로 유형별 분포 현황 (2023년)</b><br/>
    <br/>
    • 자전거·보행자 겸용도로: 20,023km (74.5%)<br/>
    • 자전거 전용도로: 3,763km (14.0%)<br/>
    • 자전거 우선도로: 2,071km (7.7%)<br/>
    • 자전거 전용차로: 1,015km (3.8%)<br/>
    <br/>
    <b>주요 문제점</b><br/>
    • 전용도로 부족: 전용도로는 14% 수준으로 선진국 대비 매우 낮음<br/>
    • 불연속 구간: 인천의 경우 190km 중 23.7km가 불연속<br/>
    • 도시별 격차: 서울 775.9km vs 대구 미흡한 정보 공개<br/>
    • 유지보수 부족: 노후 도로 정비의 우선순위 필요<br/>
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
                "<i>그림 5: 자전거 도로 유형별 구성</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 5 error: {e}")

    elements.append(Spacer(page_width, 0.3 * cm))

    # 3.3 이용자 만족도
    elements.append(Paragraph("3.3 이용자 만족도 및 개선 요구사항", styles['SectionStyle']))

    satisfaction_data = """
    <b>서울시 따릉이 이용자 만족도 (2024년)</b><br/>
    <br/>
    • 서비스 만족도: 86% (높음)<br/>
    • 자전거 도로 확충 지지도: 99% (매우 높음)<br/>
    • 안전성 미흡 지적: 30%<br/>
    • 자전거 보관 문제: 30%<br/>
    <br/>
    <b>개선 요청 사항</b><br/>
    • 안전성 강화: 도로 안전시설, 신호등 개선<br/>
    • 도로 확충: 자전거 전용도로 확대<br/>
    • 보관 시설: 안전한 자전거 보관소 확충<br/>
    • 편의성: 앱 개선, 대여 절차 간편화<br/>
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
                "<i>그림 6: 시민 만족도 및 정책 지지도</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 6 error: {e}")

    elements.append(PageBreak())

    # ========== 6. 제3장 정책 권고 ==========
    elements.append(Paragraph("4. 정책 권고", styles['ChapterStyle']))
    elements.append(Spacer(page_width, 0.3 * cm))

    elements.append(Paragraph("4.1 단기 전략 (2026년 상반기)", styles['SectionStyle']))

    short_term = """
    <b>긴급 과제 (즉시 추진)</b><br/>
    <br/>
    1. <b>제동장치 제거 자전거 운행 금지</b><br/>
    &nbsp;&nbsp;- 고급 자전거 유행으로 제동장치 제거 자전거 증가<br/>
    &nbsp;&nbsp;- 강력한 규제 및 홍보 필요<br/>
    &nbsp;&nbsp;- 위반 시 과태료 부과 시스템 구축<br/>
    <br/>
    2. <b>사고 다발 구간 CCTV 확대</b><br/>
    &nbsp;&nbsp;- AI CCTV를 활용한 위험 구간 집중 관리<br/>
    &nbsp;&nbsp;- 사각지대 파악 및 보안카메라 설치<br/>
    &nbsp;&nbsp;- 2026년 상반기 중 100개소 설치 목표<br/>
    <br/>
    3. <b>청소년 안전 교육 강화</b><br/>
    &nbsp;&nbsp;- 20세 이하 사고 급증 대응<br/>
    &nbsp;&nbsp;- 학교 교육과정 통합 안전교육<br/>
    &nbsp;&nbsp;- 자전거 안전 캠페인 월 1회 이상 실시<br/>
    """
    elements.append(Paragraph(short_term, styles['BodyStyle']))

    elements.append(Spacer(page_width, 0.3 * cm))

    elements.append(Paragraph("4.2 중기 전략 (2026-2027년)", styles['SectionStyle']))

    medium_term = """
    <b>인프라 구조 개선</b><br/>
    <br/>
    1. <b>자전거 전용도로 비중 15% 이상 확대</b><br/>
    &nbsp;&nbsp;- 현재 14% → 2027년 15% 이상<br/>
    &nbsp;&nbsp;- 주요 간선도로 중심으로 우선 시행<br/>
    &nbsp;&nbsp;- 연간 50-100km 신규 조성<br/>
    <br/>
    2. <b>불연속 구간 해소 사업</b><br/>
    &nbsp;&nbsp;- 인천 190km 중 23.7km 불연속 구간 연결<br/>
    &nbsp;&nbsp;- 타 도시 불연속 구간 매핑 및 우선순위 설정<br/>
    &nbsp;&nbsp;- 2027년까지 80% 이상 연결화 목표<br/>
    <br/>
    3. <b>자전거 전담 부서 설치</b><br/>
    &nbsp;&nbsp;- 도시별 자전거 정책 전담 조직 신설<br/>
    &nbsp;&nbsp;- 교통, 안전, 보건, 도시계획 통합 관리<br/>
    &nbsp;&nbsp;- 데이터 기반 정책 수립 체계 구축<br/>
    """
    elements.append(Paragraph(medium_term, styles['BodyStyle']))

    elements.append(Spacer(page_width, 0.3 * cm))

    elements.append(Paragraph("4.3 장기 전략 (2027-2030년)", styles['SectionStyle']))

    long_term = """
    <b>포괄적 정책 추진</b><br/>
    <br/>
    1. <b>자전거 모달 셰어 5-10% 달성</b><br/>
    &nbsp;&nbsp;- 서울시 현재 약 1% → 2030년 5%<br/>
    &nbsp;&nbsp;- 국가 수준으로 2-3% → 5% 상향<br/>
    &nbsp;&nbsp;- 출퇴근 시간대 자전거 이용 증진<br/>
    <br/>
    2. <b>자전거 전용도로 비중 20% 달성</b><br/>
    &nbsp;&nbsp;- 현재 14% → 2030년 20%<br/>
    &nbsp;&nbsp;- 전국 표준화된 도로 설계 기준 수립<br/>
    &nbsp;&nbsp;- 신도시 개발 시 필수 포함<br/>
    <br/>
    3. <b>전국 정책 표준화</b><br/>
    &nbsp;&nbsp;- 도시별 정책 성숙도 격차 해소<br/>
    &nbsp;&nbsp;- 국가 자전거 정책 마스터플랜 수립<br/>
    &nbsp;&nbsp;- 도시별 맞춤형 지원 프레임워크 구축<br/>
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
                "<i>그림 7: 국내 도시 정책 성숙도 비교</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 7 error: {e}")

    elements.append(PageBreak())

    # ========== 7. 제4장 기대효과 ==========
    elements.append(Paragraph("5. 기대효과", styles['ChapterStyle']))
    elements.append(Spacer(page_width, 0.3 * cm))

    effects_text = """
    <b>사회경제적 효과 분석</b><br/>
    <br/>
    <b>경제적 효과</b><br/>
    • 비용편익: 자전거 1km당 DKK 4.79 이득 (베를린 사례)<br/>
    • 일자리 창출: $1M 투자 시 11.41개 일자리<br/>
    • 부동산 가치: 자전거 도로 근처 €34,000 상승<br/>
    <br/>
    <b>보건 효과</b><br/>
    • 건강 비용 절감: 55% 감소 (코펜하겐 사례)<br/>
    • 생활 습관 개선: 자전거 이용 증가로 비만율 감소<br/>
    • 공기질 개선: CO2 배출 감소<br/>
    <br/>
    <b>교통 효과</b><br/>
    • 교통 혼잡 감소: 자전거 전환으로 자동차 이용 감소<br/>
    • 대중교통 연계 강화: 환승 거점 정비<br/>
    • 도시 이동성 향상: 단거리 이동 효율성 증대<br/>
    <br/>
    <b>환경 효과</b><br/>
    • 탄소 배출 감소: 년간 이산화탄소 최대 50% 감소<br/>
    • 대기오염 개선: PM2.5, NO2 농도 감소<br/>
    • 소음 감소: 전기차 추진으로 인한 소음 공해 완화<br/>
    <br/>
    <b>사회 효과</b><br/>
    • 지역 활성화: 자전거 관광, 문화 행사 증대<br/>
    • 안전한 도시: 교통사고 감소로 더 안전한 도시<br/>
    • 삶의 질 향상: 시민 만족도 99% 달성<br/>
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
                "<i>그림 9: 따릉이 이용자 사용 시간대 분포</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 9 error: {e}")

    elements.append(PageBreak())

    # ========== 8. 부록: 차트 및 통계 ==========
    elements.append(Paragraph("부록: 차트 및 통계", styles['ChapterStyle']))
    elements.append(Spacer(page_width, 0.3 * cm))

    # 추가 차트들
    chart10_path = os.path.join(chart_dir, "10_investment_comparison.png")
    if os.path.exists(chart10_path):
        try:
            img10 = RLImage(chart10_path, width=5.5*cm, height=3.5*cm)
            elements.append(img10)
            elements.append(Spacer(page_width, 0.2 * cm))
            elements.append(Paragraph(
                "<i>그림 10: 자전거 도로 투자 규모 비교</i>",
                styles['SectionStyle']
            ))
        except Exception as e:
            print(f"Chart 10 error: {e}")

    elements.append(Spacer(page_width, 0.3 * cm))

    # 통계 테이블
    elements.append(Paragraph("부록 표 1: 서울시 따릉이 이용 추이", styles['SectionStyle']))

    table_data = [
        ['연도', '이용 건수', '일평균'],
        ['2022', '14.14백만 건', '3.87만 건'],
        ['2023', '44.90백만 건', '12.3만 건'],
        ['2024', '43.85백만 건', '12.0만 건'],
    ]

    table = Table(table_data, colWidths=[2*cm, 3*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), get_font()),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), COLOR_LIGHT),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_LINE),
        ('FONTNAME', (0, 1), (-1, -1), get_font()),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    elements.append(table)

    elements.append(Spacer(page_width, 0.5 * cm))

    # 통계 테이블 2
    elements.append(Paragraph("부록 표 2: 국내 도시별 자전거 정책 현황", styles['SectionStyle']))

    table_data2 = [
        ['도시', '도로길이', '정책단계', '성숙도'],
        ['서울', '775.9km', '성숙기', '4.0/5.0'],
        ['부산', '259.7km', '성장기', '2.5/5.0'],
        ['인천', '969km', '성장기', '2.5/5.0'],
        ['대구', '미흡', '초기', '1.5/5.0'],
    ]

    table2 = Table(table_data2, colWidths=[2*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), get_font()),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), COLOR_LIGHT),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_LINE),
        ('FONTNAME', (0, 1), (-1, -1), get_font()),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    elements.append(table2)

    elements.append(Spacer(page_width, 0.5 * cm))

    # 핵심 지표 요약
    elements.append(Paragraph("부록 표 3: 해외 도시 자전거 정책 성과지표", styles['SectionStyle']))

    table_data3 = [
        ['도시', '모달셰어', '네트워크', '특징'],
        ['암스테르담', '38%', '높음', '완전분리형'],
        ['코펜하겐', '37%', '높음', '통합적접근'],
        ['베를린', '9%+', '3,000km', '적극확대'],
        ['도쿄', '13.5%', '높음', '문화강점'],
    ]

    table3 = Table(table_data3, colWidths=[2.5*cm, 2*cm, 2.5*cm, 2.5*cm])
    table3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), get_font()),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), COLOR_LIGHT),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_LINE),
        ('FONTNAME', (0, 1), (-1, -1), get_font()),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    elements.append(table3)

    elements.append(PageBreak())

    # ========== 9. 결론 ==========
    elements.append(Paragraph("결론", styles['ChapterStyle']))
    elements.append(Spacer(page_width, 0.3 * cm))

    conclusion = """
    <b>현황 평가</b><br/>
    <br/>
    한국의 자전거 도로 정책은 도시별로 매우 불균형적인 진행을 보이고 있습니다.<br/>
    서울시는 성숙기에 진입했으나, 부산·인천은 성장기, 대구는 초기 단계에 있습니다.<br/>
    <br/>
    <b>성공의 핵심 요소</b><br/>
    <br/>
    1. 질적 개선 중심의 인프라 확충<br/>
    2. 사용자 중심의 안전 문화 조성<br/>
    3. 데이터 기반의 효율적 투자<br/>
    <br/>
    <b>향후 전망</b><br/>
    <br/>
    2030년까지 달성 가능한 목표:<br/>
    • 자전거 모달 셰어 5-10% 달성<br/>
    • 자동차 대 자전거 사고 30% 감소<br/>
    • 공공자전거 이용 2배 이상 확대<br/>
    <br/>
    정책 권고사항이 차질 없이 추진된다면, 서울시와 국내 도시들은 2030년 전에<br/>
    선진국 수준의 자전거 문화 정착을 이룰 수 있을 것으로 예상됩니다.<br/>
    <br/>
    <br/>
    <b>---</b><br/>
    <br/>
    <b>작성</b>: Claude AI Agent<br/>
    <b>작성일</b>: 2026년 1월 23일<br/>
    <b>데이터 기준</b>: 2024년~2025년 최신 통계<br/>
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
            subject="서울시 자전거 도로 확충 정책 연구"
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
