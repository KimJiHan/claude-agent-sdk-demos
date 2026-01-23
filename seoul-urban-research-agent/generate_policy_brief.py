#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import sys

# 한글 폰트 등록
font_paths = [
    '/System/Library/Fonts/Supplemental/AppleGothic.ttf',
    '/Library/Fonts/NanumGothic.ttf',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
]

font_name = 'Helvetica'
for path in font_paths:
    if os.path.exists(path):
        try:
            pdfmetrics.registerFont(TTFont('KoreanFont', path))
            font_name = 'KoreanFont'
            break
        except:
            pass

# 출력 디렉토리 확인
os.makedirs('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/reports', exist_ok=True)

# 문서 생성
doc = SimpleDocTemplate(
    "/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/reports/seoul_bicycle_infrastructure_policy_brief_20260123.pdf",
    pagesize=A4,
    rightMargin=1.5*cm, leftMargin=1.5*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm
)

# 스타일 정의
styles = getSampleStyleSheet()

# 제목 스타일
styles.add(ParagraphStyle(
    name='KoreanTitle',
    fontName=font_name,
    fontSize=20,
    alignment=TA_CENTER,
    spaceAfter=6,
    textColor=colors.HexColor('#1a1a1a'),
    leading=24,
    fontWeight='bold'
))

# 부제목 스타일
styles.add(ParagraphStyle(
    name='KoreanSubtitle',
    fontName=font_name,
    fontSize=11,
    alignment=TA_CENTER,
    spaceAfter=12,
    textColor=colors.HexColor('#555555'),
    leading=14
))

# 섹션 제목 스타일
styles.add(ParagraphStyle(
    name='KoreanHeading1',
    fontName=font_name,
    fontSize=13,
    spaceAfter=10,
    textColor=colors.HexColor('#1a4d99'),
    leading=16,
    fontWeight='bold',
    borderColor=colors.HexColor('#1a4d99'),
    borderWidth=0,
    borderPadding=3
))

# 하위 제목 스타일
styles.add(ParagraphStyle(
    name='KoreanHeading2',
    fontName=font_name,
    fontSize=11,
    spaceAfter=8,
    textColor=colors.HexColor('#2c3e50'),
    leading=14,
    fontWeight='bold',
    leftIndent=12
))

# 본문 스타일
styles.add(ParagraphStyle(
    name='KoreanBody',
    fontName=font_name,
    fontSize=9,
    alignment=TA_JUSTIFY,
    leading=13,
    spaceAfter=6
))

# 본문(작은) 스타일
styles.add(ParagraphStyle(
    name='KoreanBodySmall',
    fontName=font_name,
    fontSize=8.5,
    alignment=TA_JUSTIFY,
    leading=12,
    spaceAfter=4
))

# 강조 스타일
styles.add(ParagraphStyle(
    name='KoreanEmphasis',
    fontName=font_name,
    fontSize=9,
    alignment=TA_LEFT,
    leading=13,
    spaceAfter=6,
    textColor=colors.HexColor('#c7254e')
))

# 항목 스타일
styles.add(ParagraphStyle(
    name='KoreanBullet',
    fontName=font_name,
    fontSize=9,
    alignment=TA_LEFT,
    leading=12,
    spaceAfter=4,
    leftIndent=18,
    bulletIndent=12
))

story = []

# ===== 표지 페이지 =====
story.append(Spacer(1, 2*cm))
story.append(Paragraph(
    "서울시 자전거 인프라 정책 브리프",
    styles['KoreanTitle']
))
story.append(Paragraph(
    "자전거 도로 확충 및 안전 강화 정책 방향",
    styles['KoreanSubtitle']
))
story.append(Spacer(1, 1*cm))
story.append(Paragraph(
    f"발행일: {datetime.now().strftime('%Y년 %m월 %d일')}",
    styles['KoreanBody']
))
story.append(Paragraph(
    "발행 기관: 서울연구원",
    styles['KoreanBody']
))
story.append(Spacer(1, 3*cm))

# 개요 박스
overview_data = [
    ['주요 통계', '현황', '목표(2030년)'],
    ['자전거도로 길이', '1,230.5km', '1,330km'],
    ['수송 분담률', '7% (추정)', '15%'],
    ['따릉이 이용', '4,385만 건/년', '-'],
    ['안전사고', '5,571건(2024)', '감소 추세'],
]

overview_table = Table(overview_data, colWidths=[2.5*cm, 2.5*cm, 2.5*cm])
overview_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a4d99')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), font_name),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('FONTWEIGHT', (0, 0), (-1, 0), 'bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('FONTNAME', (0, 1), (-1, -1), font_name),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
]))
story.append(overview_table)
story.append(PageBreak())

# ===== 목차 =====
story.append(Paragraph("목차", styles['KoreanTitle']))
story.append(Spacer(1, 0.3*cm))

toc_items = [
    "1. 요약 (Executive Summary)",
    "2. 연구 배경 및 목표",
    "3. 서울시 현황 분석",
    "4. 국내외 비교 분석",
    "5. 주요 문제점 및 과제",
    "6. 정책 개선 권장사항",
    "7. 향후 추진 계획",
    "8. 결론 및 기대효과",
    "9. 출처"
]

for item in toc_items:
    story.append(Paragraph(item, styles['KoreanBody']))
    story.append(Spacer(1, 0.15*cm))

story.append(PageBreak())

# ===== 1. 요약 =====
story.append(Paragraph("1. 요약 (Executive Summary)", styles['KoreanHeading1']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "서울시는 자전거 인프라 확충을 통해 '자전거 1시간 생활권' 구현을 목표로 하고 있습니다. "
    "2024년 기준 1,230.5km의 자전거도로를 보유하고 있으며, 일평균 120,000건의 따릉이 이용으로 "
    "전국 공영자전거의 약 2.3배 규모를 차지하고 있습니다. 그러나 한강 자전거도로의 사고가 4년간 80% 증가하고, "
    "자전거 통근 비율이 7%로 선진국(암스테르담 68%, 코펜하겐 62%)의 1/10 수준인 점은 개선이 필요합니다.",
    styles['KoreanBody']
))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph(
    "본 정책 브리프는 서울시 자전거 인프라의 현황을 분석하고, "
    "국제 도시의 벤치마킹을 통해 2030년까지 자전거 수송 분담률 15% 달성을 위한 "
    "5-7개의 구체적 정책 권장사항과 로드맵을 제시합니다.",
    styles['KoreanBody']
))
story.append(PageBreak())

# ===== 2. 연구 배경 및 목표 =====
story.append(Paragraph("2. 연구 배경 및 목표", styles['KoreanHeading1']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("2.1 배경", styles['KoreanHeading2']))
story.append(Paragraph(
    "세계 주요 도시들(암스테르담, 코펜하겐, 파리)은 자전거를 핵심 교통 수단으로 인정하고, "
    "대규모 인프라 투자를 통해 높은 자전거 이용률을 달성했습니다. "
    "서울시도 탄소중립 목표와 시민의 건강 증진을 위해 자전거 인프라 확충을 추진 중입니다. "
    "다만 단순 도로 확충을 넘어 안전성, 연계성, 시민 문화 측면의 통합적 개선이 필요합니다.",
    styles['KoreanBody']
))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("2.2 목표", styles['KoreanHeading2']))
story.append(Paragraph("• 2030년까지 자전거도로 1,330km 완성", styles['KoreanBullet']))
story.append(Paragraph("• 자전거 수송 분담률 15% 달성 (현재 7%)", styles['KoreanBullet']))
story.append(Paragraph("• 자전거 교통사고 50% 감소", styles['KoreanBullet']))
story.append(Paragraph("• 자전거 도로 분리율 80% 달성 (선진국 수준)", styles['KoreanBullet']))
story.append(PageBreak())

# ===== 3. 서울시 현황 분석 =====
story.append(Paragraph("3. 서울시 현황 분석", styles['KoreanHeading1']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("3.1 자전거도로 인프라 현황", styles['KoreanHeading2']))

# 표 1: 자전거도로 현황
table1_data = [
    ['항목', '2016년', '2024년', '변화'],
    ['총 도로 길이', '868.7km', '1,230.5km', '+41.6%'],
    ['한강 자전거도로', '-', '78km', '신설'],
    ['전국 대비 비중', '-', '4.4%', '-'],
]

table1 = Table(table1_data, colWidths=[2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
table1.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a4d99')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), font_name),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('FONTWEIGHT', (0, 0), (-1, 0), 'bold'),
    ('FONTNAME', (0, 1), (-1, -1), font_name),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
]))
story.append(table1)
story.append(Spacer(1, 0.3*cm))

# 차트 1: 서울시 따릉이 이용 추이
if os.path.exists('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/01_seoul_usage_trend.png'):
    img1 = Image('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/01_seoul_usage_trend.png', width=15*cm, height=8*cm)
    story.append(img1)
    story.append(Paragraph("그림 1. 서울시 따릉이 연도별 이용 추이 (2010-2024년)", styles['KoreanBodySmall']))
    story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "서울시 따릉이는 2010년 41만 건에서 2024년 4,385만 건으로 약 400배 증가했습니다. "
    "일평균 약 120,000건의 이용으로 시민 중심의 교통수단으로 정착했으며, "
    "정기권 이용자 비율이 74.8%(2020년)에서 80.3%(2022년)로 증가하여 수익성도 개선되었습니다.",
    styles['KoreanBody']
))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("3.2 따릉이 이용 시간대별 패턴", styles['KoreanHeading2']))

# 차트 4: 시간대별 이용 패턴
if os.path.exists('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/04_hourly_usage_pattern.png'):
    img4 = Image('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/04_hourly_usage_pattern.png', width=15*cm, height=8*cm)
    story.append(img4)
    story.append(Paragraph("그림 2. 평일/주말 시간대별 이용 패턴 (2024년)", styles['KoreanBodySmall']))
    story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "평일 출퇴근 시간대(07-09시, 17-19시)에 44.3% 이용으로 주요 교통 수단 역할을 하며, "
    "주말 오후(13-18시)에 41.9% 이용으로 여가 활동도 증가하는 추세입니다. "
    "계절별로는 동절기 이용이 2019년 334만 건에서 2023년 1,177만 건으로 3.5배 증가해 "
    "연중 안정적 수송 수단으로 자리 잡았습니다.",
    styles['KoreanBody']
))
story.append(PageBreak())

story.append(Paragraph("3.3 안전 현황", styles['KoreanHeading2']))

# 표 2: 자전거 사고 추이
table2_data = [
    ['연도', '발생 건수', '사망자', '변화율'],
    ['2022년', '5,393건', '91명', '-'],
    ['2023년', '5,146건', '64명', '-4.6%'],
    ['2024년', '5,571건', '75명', '+8.3%'],
]

table2 = Table(table2_data, colWidths=[2*cm, 2.5*cm, 2*cm, 2*cm])
table2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#c7254e')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), font_name),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('FONTWEIGHT', (0, 0), (-1, 0), 'bold'),
    ('FONTNAME', (0, 1), (-1, -1), font_name),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
]))
story.append(table2)
story.append(Spacer(1, 0.3*cm))

# 차트 5: 교통사고 추이
if os.path.exists('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/05_accident_trend.png'):
    img5 = Image('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/05_accident_trend.png', width=15*cm, height=8*cm)
    story.append(img5)
    story.append(Paragraph("그림 3. 한강 자전거도로 사고 발생 추이 (2019-2023년)", styles['KoreanBodySmall']))
    story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "한강 자전거도로의 사고는 2019년 65건에서 2023년 117건으로 4년간 80% 증가했습니다. "
    "전체 사고 중 과속 관련이 약 50%(자전거 간 추월 36.9%, 보행자 충돌 11.3%)를 차지하며, "
    "전기자전거 과속, 킥보드 불법 이용 민원이 지속적으로 증가하고 있습니다. "
    "2024년 전국 자전거 사고는 5,571건으로 2023년 대비 8.3% 증가, 사망자도 17% 증가했습니다.",
    styles['KoreanBody']
))
story.append(PageBreak())

# ===== 4. 국내외 비교 분석 =====
story.append(Paragraph("4. 국내외 비교 분석", styles['KoreanHeading1']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("4.1 국제 도시 자전거 인프라 비교", styles['KoreanHeading2']))

# 차트 2: 국제 도시 비교
if os.path.exists('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/02_seoul_vs_international_cities.png'):
    img2 = Image('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/02_seoul_vs_international_cities.png', width=15*cm, height=8*cm)
    story.append(img2)
    story.append(Paragraph("그림 4. 서울 vs 국제 도시 자전거도로 길이 비교 (2024년)", styles['KoreanBodySmall']))
    story.append(Spacer(1, 0.3*cm))

# 표 3: 도시별 비교
table3_data = [
    ['도시', '도로 길이', '통근 비율', '1인당 투자'],
    ['암스테르담', '1,242.5km', '68%', '€143/년'],
    ['코펜하겐', '397km', '62%', '€38/년'],
    ['파리', '1,300km+', '11.2%', '€7.8/년'],
    ['서울', '1,230.5km', '7%', '추정 €3/년'],
]

table3 = Table(table3_data, colWidths=[2*cm, 2.5*cm, 2.5*cm, 2.5*cm])
table3.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a4d99')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), font_name),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('FONTWEIGHT', (0, 0), (-1, 0), 'bold'),
    ('FONTNAME', (0, 1), (-1, -1), font_name),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
]))
story.append(table3)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "서울의 자전거도로 길이는 국제 도시(암스테르담, 파리)와 비슷하나, "
    "통근 비율은 7%로 선진국의 1/9 수준입니다. 암스테르담은 완전 분리 도로 858.1km(전체의 69%)를 갖추고, "
    "코펜하겐은 연간 1인당 €38을 투자하는 등 질적 수준이 높습니다. "
    "서울은 인프라 길이는 충분하나 안전성, 연계성, 투자 규모에서 개선이 필요합니다.",
    styles['KoreanBody']
))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("4.2 자전거 통근 비율 비교", styles['KoreanHeading2']))

# 차트 6: 통근 비율 비교
if os.path.exists('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/06_commute_rate_comparison.png'):
    img6 = Image('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/06_commute_rate_comparison.png', width=15*cm, height=8*cm)
    story.append(img6)
    story.append(Paragraph("그림 5. 주요 도시 자전거 통근 비율 비교", styles['KoreanBodySmall']))
    story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "암스테르담(68%), 코펜하겐(62%)은 자전거가 주요 교통수단이나, "
    "서울(7%)은 여전히 낮습니다. 도쿄(12.89%), 파리(11.2%)도 서울을 초과하고 있으며, "
    "서울의 2030년 목표(15%)도 선진국의 절반 수준입니다. "
    "인프라 확충뿐 아니라 자전거 문화 정착, 안전 강화, 대중교통 연계가 병행되어야 합니다.",
    styles['KoreanBody']
))
story.append(PageBreak())

story.append(Paragraph("4.3 국내 도시별 비교", styles['KoreanHeading2']))

# 표 4: 국내 도시 비교
table4_data = [
    ['항목', '서울', '부산', '인천', '대전'],
    ['도로 길이', '1,230.5km', '미공개', '미공개', '774.7km'],
    ['공영자전거', '4,385만 건', '미공개', '미공개', '2,500→7,500대'],
    ['투자 규모', '미공개', '323억원', '336.5억원', '798억원'],
]

table4 = Table(table4_data, colWidths=[2*cm, 2.5*cm, 2.5*cm, 2.5*cm])
table4.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a4d99')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), font_name),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('FONTWEIGHT', (0, 0), (-1, 0), 'bold'),
    ('FONTNAME', (0, 1), (-1, -1), font_name),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
]))
story.append(table4)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    "부산은 259.7km 추가 도로 확충(323억원), 인천은 300리 자전거 이음길(336.5억원, 130km)을 추진 중입니다. "
    "대전은 798억원 규모로 공공자전거를 2,500대에서 7,500대로 확대하고, 자전거 학교 설립을 계획하고 있습니다. "
    "서울은 따릉이 이용률이 전국 대비 2.3배로 가장 높으나, 투자 규모 공개 부족과 안전성 개선 필요가 과제입니다.",
    styles['KoreanBody']
))
story.append(PageBreak())

# ===== 5. 주요 문제점 및 과제 =====
story.append(Paragraph("5. 주요 문제점 및 과제", styles['KoreanHeading1']))
story.append(Spacer(1, 0.3*cm))

# 차트 3: 구별 이용량 비교
if os.path.exists('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/03_district_usage_comparison.png'):
    img3 = Image('/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/03_district_usage_comparison.png', width=15*cm, height=8*cm)
    story.append(img3)
    story.append(Paragraph("그림 6. 자치구별 따릉이 이용량 비교 (2023년)", styles['KoreanBodySmall']))
    story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("5.1 지역 불균형", styles['KoreanHeading2']))
story.append(Paragraph(
    "강서구(524만 건), 송파구(401만 건), 영등포구(370만 건)이 전체 이용의 상당 부분을 차지하고 있어, "
    "도시 중심부와 한강변 접근성이 높은 지역 편중이 심합니다. "
    "외곽 지역의 자전거도로 및 편의시설 확충이 필요합니다.",
    styles['KoreanBody']
))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("5.2 안전성 악화", styles['KoreanHeading2']))
story.append(Paragraph(
    "한강 자전거도로 사고가 4년간 80% 증가했고, 과속 관련 사고가 50%를 차지합니다. "
    "전기자전거 과속, 킥보드 불법 이용, 음주 탑승 민원이 지속되며, "
    "보행자와 자전거 충돌도 증가하고 있습니다. "
    "AI 기반 CCTV 확대, 보도와 자전거도로 완전 분리, 과속 방지 시설 강화가 시급합니다.",
    styles['KoreanBody']
))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("5.3 통근 비율 저조", styles['KoreanHeading2']))
story.append(Paragraph(
    "자전거 통근 비율 7%는 선진국의 1/10 수준입니다. "
    "날씨, 거리, 안전 우려 등이 주요 장애 요인이며, "
    "자전거 문화 확산 및 인식 개선이 필요합니다. "
    "직장 자전거 보관소, 직장인 대상 교육 확대 등 맞춤형 정책이 필요합니다.",
    styles['KoreanBody']
))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("5.4 도로 시인성 및 혼란", styles['KoreanHeading2']))
story.append(Paragraph(
    "자전거도로 노면 표시 탈색이 많고, 전용도로와 겸용도로 구분이 불명확합니다. "
    "시민 민원 우선순위 1위가 '도로 시인성 개선'이며, "
    "도로 유형별 명확한 표시 및 이용 교육이 필요합니다.",
    styles['KoreanBody']
))
story.append(PageBreak())

# ===== 6. 정책 개선 권장사항 =====
story.append(Paragraph("6. 정책 개선 권장사항 (5-7개)", styles['KoreanHeading1']))
story.append(Spacer(1, 0.3*cm))

recommendations = [
    ("1. 안전성 강화 및 스마트시스템 도입",
     "• AI 기반 CCTV 확대: 한강 40개에서 시내 주요 거점 100개로 확대, 과속 탐지 및 안내방송\n"
     "• 보행자-자전거 완전 분리: 보도높이형 도로 비율 97%에서 100% 목표\n"
     "• 교차로 신호 체계 개선: 코펜하겐식 자전거 사전신호(pre-greens) 도입"),

    ("2. 도로 시인성 및 혼란 해소",
     "• 노면 표시 강화: 탈색 방지 재료 사용, 5년 주기 재정비\n"
     "• 도로 유형별 색상 표준화: 전용도로(빨강), 겸용도로(파랑) 등 명확한 구분\n"
     "• 도로 안내판 정비: 자전거도로 현황지도 앱 및 실시간 안내"),

    ("3. 자전거 주차 인프라 혁신",
     "• 지하 주차장 개발: 서울역, 용산역, 강남역 등 3곳에 총 30,000개 규모 (암스테르담 사례)\n"
     "• 지상 거치대 확충: 아파트, 학교, 직장 중심 5,000개 추가\n"
     "• 스마트 시스템: 주차 공간 실시간 예약 및 결제 시스템 도입"),

    ("4. 자동차 공간 재배치",
     "• 주차 공간 재편성: 연간 1,000개 자동차 주차 제거 → 자전거 주차, 녹지, 보행환경 개선\n"
     "• 도로 재설계: 강남, 강북 주요 도심 간선도로의 20-30% 자동차 공간 축소\n"
     "• 20년 로드맵: 2045년까지 누적 20,000개 자동차 주차 감소"),

    ("5. 지역 불균형 해소",
     "• 외곽 지역 집중 투자: 강동, 강북, 노원 지역 자전거도로 150km 확충 (2025-2027)\n"
     "• 지선망 연계: 한강 도로와 주거지, 역, 학교를 연결하는 순환형 지선 구축\n"
     "• 대중교통 연계: 지하철역 자전거 보관소 확대, 자전거-지하철 통합 정기권 도입"),

    ("6. 자전거 문화 정착 및 교육",
     "• 직장인 교육 강화: 출근 안전 교육, 자전거 보험 지원 (직장별 조직)\n"
     "• 어린이-청소년 프로그램: 학교 안전 교육, 자전거 타기 대회 연간 확대\n"
     "• 공공캠페인: 자전거 통근의 건강/환경 편익 홍보 (연간 30% 확대)"),

    ("7. 투자 규모 확대 및 다년 계획",
     "• 예산 증액: 현재 대비 50-100% 증액 (코펜하겐 방식: 1인당 €38/년 = 서울 380억원/년 필요)\n"
     "• 다년 계획 수립: 2025-2030년 5개년 계획에 예산 배정\n"
     "• 재정 다원화: 탄소세, 혼잡통행료 일부를 자전거 인프라에 할당")
]

for title, content in recommendations:
    story.append(Paragraph(title, styles['KoreanHeading2']))
    for line in content.split('\n'):
        if line.strip():
            story.append(Paragraph(line, styles['KoreanBullet']))
    story.append(Spacer(1, 0.2*cm))

story.append(PageBreak())

# ===== 7. 향후 추진 계획 (로드맵) =====
story.append(Paragraph("7. 향후 추진 계획 (2030년까지 로드맵)", styles['KoreanHeading1']))
story.append(Spacer(1, 0.3*cm))

# 로드맵 표
roadmap_data = [
    ['시점', '주요 과제', '예상 결과'],
    ['2025년\n(1단계)',
     '• 한강 CCTV 40개 완성\n• 자전거도로 노면 표시 강화(20%)\n• 주차소 5,000개 추가',
     '• 한강 사고 15% 감소\n• 도로 시인성 개선\n'],
    ['2026-2027년\n(2단계)',
     '• 자동차 공간 2,000개 재배치\n• 지하 주차장 1개 완공(10,000개)\n• 외곽 지역 도로 150km 확충',
     '• 자전거 주차 공간 50% 증\n• 외곽 이용률 30% 증가\n'],
    ['2028-2029년\n(3단계)',
     '• 지하 주차장 추가 2개(20,000개)\n• 자동차 공간 추가 2,000개 재배치\n• 도로 분리율 80% 달성',
     '• 주차 공간 부족 해소\n• 안전성 대폭 개선\n'],
    ['2030년\n(완성)',
     '• 자전거도로 1,330km 완성\n• 통근 비율 15% 달성\n• 사고 50% 감소',
     '• 자전거 1시간 생활권 구현\n• 선진국 수준의 인프라\n'],
]

roadmap_table = Table(roadmap_data, colWidths=[2*cm, 4.5*cm, 3.5*cm])
roadmap_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a4d99')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('FONTNAME', (0, 0), (-1, 0), font_name),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('FONTWEIGHT', (0, 0), (-1, 0), 'bold'),
    ('FONTNAME', (0, 1), (-1, -1), font_name),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(roadmap_table)
story.append(PageBreak())

# ===== 8. 결론 및 기대효과 =====
story.append(Paragraph("8. 결론 및 기대효과", styles['KoreanHeading1']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("8.1 핵심 메시지", styles['KoreanHeading2']))
story.append(Paragraph(
    "서울의 자전거 인프라는 길이 면에서는 국제 도시 수준이나, "
    "안전성, 투자, 통근 비율 측면에서는 개선이 필요합니다. "
    "단순 도로 확충을 넘어 스마트시스템, 문화 정착, 대중교통 연계를 통한 "
    "통합적 개선이 필수입니다.",
    styles['KoreanBody']
))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("8.2 기대효과", styles['KoreanHeading2']))

effects = [
    ("환경 편익",
     "자동차 이동의 27% 전환 시 교통 부문 CO2 15-19% 감축(파리 사례)\n"
     "연간 약 260만 톤의 CO2 감축 기대"),

    ("보건 편익",
     "자전거 통근자의 심혈관질환 발생 위험 30-40% 감소\n"
     "만성질환 예방 및 정신건강 개선"),

    ("경제 효과",
     "자전거 인프라 투자 1억원당 25개 일자리 창출\n"
     "소매 판매 증가(뉴욕 9th Ave: 보호 도로 설치 후 49% 증가)\n"
     "부동산 가치 상승(자전거도로 근처 10-15%)"),

    ("교통 효과",
     "한강 교통량 해소로 자동차 통행 시간 5-10% 단축\n"
     "지하철 혼잡 완화(따릉이로 지하철 승객 10% 대체 가능)"),

    ("안전 효과",
     "보호 자전거 도로로 사고 40-50% 감소(뉴욕 사례)\n"
     "사망자 50% 감소를 통한 사회적 손실 경감"),
]

for title, content in effects:
    story.append(Paragraph(f"• {title}", styles['KoreanHeading2']))
    story.append(Paragraph(content, styles['KoreanBody']))
    story.append(Spacer(1, 0.15*cm))

story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("8.3 향후 과제", styles['KoreanHeading2']))
story.append(Paragraph(
    "본 정책 권장사항의 성공을 위해서는 \n"
    "(1) 시장과 자치구의 적극적 리더십, \n"
    "(2) 예산의 지속적 확대, \n"
    "(3) 시민 참여 및 공감대 형성이 필수입니다. "
    "특히 안전성 강화와 문화 정착에 5-10년의 중기적 관점이 필요합니다.",
    styles['KoreanBody']
))
story.append(PageBreak())

# ===== 9. 출처 =====
story.append(Paragraph("9. 출처", styles['KoreanHeading1']))
story.append(Spacer(1, 0.3*cm))

sources = [
    "서울시 열린데이터광장 - 자전거 이용 통계 (2024년)",
    "서울시 자전거도로 현황 통계 (2024년)",
    "행정안전부 자전거 이용 현황 통계 (2024년)",
    "도로교통공단 TAAS 교통사고분석시스템",
    "Amsterdam Cycling Infrastructure Data (2024)",
    "Copenhagen Cycling Account (2024)",
    "NYC Department of Transportation Bike Lane Statistics (2024)",
    "Paris Bicycle Infrastructure Program (2024)",
    "Tokyo Cycling Statistics (2024)",
    "뉴욕시 자전거도로 안전 효과 보고서",
    "코펜하겐 자전거 안전 통계",
    "서울시 한강자전거도로 안전 개선 종합 대책",
    "서울시민 자전거 이용 만족도 조사 (서울서베이)",
    "부산시 자전거도로 정책 현황",
    "인천시 '300리 자전거 이음길' 사업 자료",
    "대전시 자전거 도로 정책 현황",
]

for i, source in enumerate(sources, 1):
    story.append(Paragraph(f"{i}. {source}", styles['KoreanBodySmall']))
    story.append(Spacer(1, 0.1*cm))

# PDF 생성
doc.build(story)
print("PDF 생성 완료: /Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/reports/seoul_bicycle_infrastructure_policy_brief_20260123.pdf")
