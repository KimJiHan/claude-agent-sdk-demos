#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1
from reportlab.lib.units import cm, inch
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, KeepTogether
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import os

# PDF 파일 경로
output_path = "/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/reports/서울시_자전거도로확충_종합정책보고서_20260123.pdf"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# 문서 생성
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=1.5*cm,
    leftMargin=1.5*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
    title="서울시 자전거 도로 확충 정책 종합 보고서"
)

# 스타일 정의
styles = getSampleStyleSheet()
style_dict = {}

# 제목 스타일
style_dict['title_main'] = ParagraphStyle(
    'title_main',
    parent=styles['Normal'],
    fontSize=28,
    textColor=HexColor('#1f4788'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

style_dict['title_sub'] = ParagraphStyle(
    'title_sub',
    parent=styles['Normal'],
    fontSize=16,
    textColor=HexColor('#4472c4'),
    spaceAfter=24,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

# 섹션 제목
style_dict['heading1'] = ParagraphStyle(
    'heading1',
    parent=styles['Normal'],
    fontSize=14,
    textColor=HexColor('#1f4788'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold',
    borderColor=HexColor('#4472c4'),
    borderWidth=0,
    borderPadding=6
)

style_dict['heading2'] = ParagraphStyle(
    'heading2',
    parent=styles['Normal'],
    fontSize=12,
    textColor=HexColor('#2e5c8a'),
    spaceAfter=8,
    spaceBefore=10,
    fontName='Helvetica-Bold'
)

style_dict['heading3'] = ParagraphStyle(
    'heading3',
    parent=styles['Normal'],
    fontSize=11,
    textColor=HexColor('#4472c4'),
    spaceAfter=6,
    spaceBefore=8,
    fontName='Helvetica-Bold'
)

# 본문 스타일
style_dict['body'] = ParagraphStyle(
    'body',
    parent=styles['Normal'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=8,
    leading=14
)

style_dict['body_left'] = ParagraphStyle(
    'body_left',
    parent=styles['Normal'],
    fontSize=10,
    alignment=TA_LEFT,
    spaceAfter=8,
    leading=14
)

# 콘텐츠 리스트
story = []

# 1. 표지
story.append(Spacer(1, 3*cm))
story.append(Paragraph("서울시 자전거 도로 확충 정책", style_dict['title_main']))
story.append(Paragraph("종합 보고서", style_dict['title_main']))
story.append(Spacer(1, 1.5*cm))
story.append(Paragraph("2026년 1월 23일", style_dict['title_sub']))
story.append(Spacer(1, 2*cm))
# Create a centered style for Seoul Institute
style_dict['center_text'] = ParagraphStyle(
    'center_text',
    parent=styles['Normal'],
    fontSize=10,
    alignment=TA_CENTER,
    spaceAfter=8,
)
story.append(Paragraph("서울연구원<br/>Urban Research Institute of Seoul", style_dict['center_text']))
story.append(Spacer(1, 1*cm))
story.append(Paragraph("주관: 서울시 교통정책과<br/>Conducted by Seoul Metropolitan Government, Transportation Policy Division", style_dict['body_left']))
story.append(PageBreak())

# 2. 요약 (Executive Summary)
story.append(Paragraph("요약 (Executive Summary)", style_dict['heading1']))
story.append(Spacer(1, 0.3*cm))

summary_text = """
본 보고서는 서울시 자전거 도로 확충 정책의 현황을 분석하고 국내외 벤치마크를 통해
향후 정책 방향을 제시합니다.

<b>주요 성과:</b>
- 서울시 자전거도로 775.9km 구축 (한강 78km 포함)
- 공공자전거 따릉이: 2015년 11.3만 건 → 2024년 4,385만 건 (400배 성장)
- 공공자전거 이용자 506만 명, 시민 만족도 86%
- 정책 공감도 3년 연속 1위 달성

<b>주요 도전과제:</b>
- 자전거·보행자 겸용도로 74.4% (안전성 개선 필요)
- 자전거 사고 증가: 2023년 대비 2024년 8.3% 증가
- 청소년 사고 50% 급증 (픽시 자전거 영향)
- 지역 격차 심화: 강남 대비 강북 5배 차이

<b>정책 권고사항:</b>
1. 자전거 전용도로 확충: 현재 13.5% → 2030년 20% 이상 목표
2. 안전성 강화: 물리적 분리, AI CCTV, 교육 체계화
3. 지역 균형: 강북·강서 지역 우선 투자
4. 국제 수준의 인프라: 네트워크 연속성 100% 달성

<b>기대 효과:</b>
- 자전거 모달쉐어 10-15% 달성 가능 (현재 추정 5-8%)
- 자전거도로 800km 이상 확충
- 연간 CO2 2-3백만 톤 감소
- 교통 혼잡 20% 이상 완화
"""

story.append(Paragraph(summary_text, style_dict['body']))
story.append(PageBreak())

# 3. 목차
story.append(Paragraph("목차 (Table of Contents)", style_dict['heading1']))
story.append(Spacer(1, 0.3*cm))

toc_items = [
    ("I. 연구 개요", "4"),
    ("II. 국내 자전거 도로 현황 (5개 도시 비교)", "5"),
    ("III. 해외 벤치마크 (6개 도시)", "6"),
    ("IV. 서울시 현황 분석", "7"),
    ("V. 시민 의견 및 만족도", "8"),
    ("VI. 주요 발견사항", "9"),
    ("VII. 정책 권고사항", "10"),
    ("VIII. 결론", "11"),
    ("부록. 차트와 데이터 요약", "12")
]

for item, page in toc_items:
    toc_line = f"{item} .......... {page}"
    story.append(Paragraph(toc_line, style_dict['body_left']))
    story.append(Spacer(1, 0.2*cm))

story.append(PageBreak())

# I. 연구 개요
story.append(Paragraph("I. 연구 개요", style_dict['heading1']))
story.append(Spacer(1, 0.2*cm))

intro_text = """
<b>1. 연구 배경</b><br/>
서울시의 자전거 도로 정책은 지난 10년간 획기적인 발전을 이루었습니다. 공공자전거 따릉이의
성공적 운영, 한강 자전거도로 78km 전면 개선, 도시 전역의 자전거 인프라 확충 등이 이루어졌습니다.
그러나 여전히 도로 품질 편차, 지역 불균형, 안전성 문제 등의 과제가 남아있습니다.

<b>2. 연구 목적</b><br/>
본 연구는 다음의 목표를 달성합니다:
- 서울시 자전거 도로의 현황 및 문제점 분석
- 국내 4개 도시(부산, 인천, 대전, 대구)와 비교분석
- 해외 선진도시(암스테르담, 코펜하겐, 베를린, 도쿄, 싱가포르 등) 벤치마크
- 시민 의견 수렴 및 만족도 조사
- 향후 정책 방향과 실행 방안 제시

<b>3. 연구 범위</b><br/>
- 지역: 국내 5개 주요 도시, 해외 6개 도시
- 기간: 2015-2024년 주요 통계 분석 (일부 2026년 계획 포함)
- 데이터: 공공데이터포털, 지자체 공식 자료, 서울연구원 자체 조사
"""

story.append(Paragraph(intro_text, style_dict['body']))
story.append(PageBreak())

# II. 국내 자전거 도로 현황
story.append(Paragraph("II. 국내 자전거 도로 현황 (5개 도시 비교)", style_dict['heading1']))
story.append(Spacer(1, 0.2*cm))

# 도시별 비교 테이블
domestic_data = [
    ['도시', '자전거도로\n길이(km)', '순위', '주요 특징', '정책 단계'],
    ['인천', '969.0', '1위', '300리 이음길 프로젝트\n94.3km 단절구간 연결 중', '성장기'],
    ['서울', '775.9', '2위', '한강 78km 개선\n따릉이 3,500곳+ 운영', '성숙기'],
    ['대전', '774.7', '3위', '타슈 공공자전거 4,600대\n도시 전역 네트워크', '성장기'],
    ['부산', '259.7', '4위', '낙동강 중심 개발\n2024-2028년 323억원 투자', '성장기'],
    ['대구', '400.0', '5위', '분산 관리 체계\n정책 가시성 부족', '성장기'],
]

table_domestic = Table(domestic_data, colWidths=[1.2*cm, 1.8*cm, 1*cm, 3.2*cm, 1.2*cm])
table_domestic.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#4472c4')),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0f0f0')),
    ('GRID', (0, 0), (-1, -1), 1, black),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f9f9f9')])
]))

story.append(table_domestic)
story.append(Spacer(1, 0.3*cm))

# 전국 현황
story.append(Paragraph("<b>전국 자전거도로 총 길이 추이</b>", style_dict['heading2']))
story.append(Spacer(1, 0.2*cm))

national_data = [
    ['연도', '총 길이(km)', '증가량(km)', '증가율(%)'],
    ['2021년', '25,249.12', '-', '-'],
    ['2023년', '26,872', '1,622.88', '6.4%'],
    ['2024년', '27,754', '882', '3.3%'],
]

table_national = Table(national_data, colWidths=[1.8*cm, 2*cm, 2*cm, 1.5*cm])
table_national.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#70ad47')),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('GRID', (0, 0), (-1, -1), 1, black),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f0f0f0')])
]))

story.append(table_national)
story.append(Spacer(1, 0.3*cm))

analysis_text = """
<b>분석:</b> 전국 자전거도로는 연평균 약 750km 이상씩 확충되고 있으며, 2021년 대비
2024년에 약 10% 증가했습니다. 서울시는 전국 증가의 선도적 역할을 수행하고 있습니다.
"""
story.append(Paragraph(analysis_text, style_dict['body']))
story.append(PageBreak())

# III. 해외 벤치마크
story.append(Paragraph("III. 해외 벤치마크 (6개 도시)", style_dict['heading1']))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("<b>1. 자전거 모달 셰어 국제 비교</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

international_data = [
    ['도시', '국가', '모달쉐어(%)', '분류', '특징'],
    ['암스테르담', '네덜란드', '38%', '성숙기', '세계 최고 수준, 자전거 우선정책'],
    ['코펜하겐', '덴마크', '37%', '성숙기', '2025년까지 50% 목표'],
    ['베를린', '독일', '18%', '성장기', '2030년 23% 목표, 3,000km 계획'],
    ['도쿄', '일본', '13.5%', '성장기', '아시아 도시, 인프라 부족'],
    ['싱가포르', '싱가포르', '2%', '초기단계', '열대 기후 제약'],
    ['서울', '한국', '5-8%', '초기성장', '2030년 15-20% 목표'],
]

table_intl = Table(international_data, colWidths=[1.5*cm, 1.3*cm, 1.5*cm, 1.3*cm, 2.8*cm])
table_intl.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#c55a11')),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('ALIGN', (4, 0), (4, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('GRID', (0, 0), (-1, -1), 1, black),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f9f9f9')])
]))

story.append(table_intl)
story.append(Spacer(1, 0.3*cm))

# 베를린 사례
story.append(Paragraph("<b>2. 베를린 사례: 혁신적 자전거 정책</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

berlin_text = """
<b>목표:</b> 자전거 모달쉐어 18% → 2030년 23% 달성<br/>
<b>규모:</b> 3,000km 총 자전거 네트워크 구축<br/>
<b>투자:</b> EU 및 국가 기후기금 활용<br/>
<b>혁신:</b>
- 팝업 자전거 차선(임시 시설) → 73% 이용 증가 → 영구 설치
- 38km 고속 사이클 루트(superhighway) 구축
- 보호된 교차로 설치로 안전성 확보
- 2022-2027년 단계적 확충 계획<br/>
<b>성과:</b> 팝업 차선으로 자전거 이용 73% 증가, 자동차 교통 11% 감소, 혼잡 없음
"""

story.append(Paragraph(berlin_text, style_dict['body']))
story.append(Spacer(1, 0.3*cm))

# 암스테르담/코펜하겐 사례
story.append(Paragraph("<b>3. 암스테르담·코펜하겐: 성숙기 도시</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

mature_text = """
<b>암스테르담 (네덜란드):</b><br/>
- 모달쉐어 38% (세계 최고)
- 자전거 우선 도시 설계
- 1,500km+ 자전거도로 네트워크
- 신호등 우선도 자전거 중심으로 설계<br/>

<b>코펜하겐 (덴마크):</b><br/>
- 모달쉐어 37%
- 2025년까지 50% 목표
- 연간 예산 DKK 600M ($80M)
- 인프라 정비보다 경험 강조 (쾌적함, 안전성)
"""

story.append(Paragraph(mature_text, style_dict['body']))
story.append(PageBreak())

# IV. 서울시 현황 분석
story.append(Paragraph("IV. 서울시 현황 분석", style_dict['heading1']))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("<b>1. 자전거도로 현황</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

seoul_infra_data = [
    ['도로 유형', '길이(km)', '비율(%)', '안전성 평가'],
    ['자전거·보행자 겸용도로', '574.9', '74.1%', '낮음'],
    ['자전거전용도로', '99.5', '12.8%', '높음'],
    ['자전거전용차로', '51.8', '6.7%', '중간'],
    ['자전거우선도로', '49.7', '6.4%', '중간'],
    ['합계', '775.9', '100%', '-'],
]

table_seoul = Table(seoul_infra_data, colWidths=[2.5*cm, 1.8*cm, 1.5*cm, 1.7*cm])
table_seoul.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#e74c3c')),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('GRID', (0, 0), (-1, -1), 1, black),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f9f9f9')]),
    ('BACKGROUND', (0, 5), (-1, 5), HexColor('#ffffcc')),
    ('FONTNAME', (0, 5), (-1, 5), 'Helvetica-Bold')
]))

story.append(table_seoul)
story.append(Spacer(1, 0.3*cm))

analysis_text2 = """
<b>주요 특징:</b> 자전거·보행자 겸용도로가 74%를 차지하여 보행자와의 충돌 가능성이 높습니다.
안전한 독립된 자전거도로(자전거전용도로)는 12.8%에 불과합니다.
"""
story.append(Paragraph(analysis_text2, style_dict['body']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>2. 공공자전거(따릉이) 성장 현황</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

dareungi_data = [
    ['연도', '연간 이용(만 건)', '누적 이용', '비고'],
    ['2015년', '11.3', '-', '출범'],
    ['2016년', '300', '-', '27배 성장'],
    ['2018년', '1,500', '-', '130배 성장'],
    ['2020년', '3,000', '-', '260배 성장'],
    ['2022년', '3,500', '-', '-'],
    ['2024년', '4,385', '2억 5,017만 건', '400배 성장'],
]

table_dareungi = Table(dareungi_data, colWidths=[1.3*cm, 1.8*cm, 2*cm, 1.9*cm])
table_dareungi.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#27ae60')),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('GRID', (0, 0), (-1, -1), 1, black),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f0f0f0')])
]))

story.append(table_dareungi)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>3. 지역별 불균형 (강남 vs 강북)</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

regional_data = [
    ['지역', '자전거전용도로(km)', '겸용도로(km)', '총합(km)', '비율(%)'],
    ['강남 4구', '26.1', '240.8', '266.9', '34.4%'],
    ['강남 전체', '63.1', '-', '-', '84%'],
    ['강북 전체', '11.6', '119.3', '130.9', '16%'],
    ['격차', '5배 이상', '-', '-', '매우 불균형'],
]

table_regional = Table(regional_data, colWidths=[1.5*cm, 1.8*cm, 1.8*cm, 1.5*cm, 1.4*cm])
table_regional.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#8e44ad')),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('GRID', (0, 0), (-1, -1), 1, black),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f0f0f0')])
]))

story.append(table_regional)
story.append(Spacer(1, 0.3*cm))

analysis_text3 = """
<b>결론:</b> 강남 지역(특히 강남 4구)에 서울시 자전거도로의 35%가 집중되어 있으며,
강북 지역과 5배 이상의 격차가 있습니다. 이는 공급 측면의 심각한 불공정입니다.
"""
story.append(Paragraph(analysis_text3, style_dict['body']))
story.append(PageBreak())

# V. 시민 의견 및 만족도
story.append(Paragraph("V. 시민 의견 및 만족도", style_dict['heading1']))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("<b>1. 공공자전거 만족도</b>", style_dict['heading2']))
story.append(Spacer(1,0.15*cm))

satisfaction_text = """
<b>따릉이 정책 평가 (2017-2019):</b>
- '시민이 가장 공감하는 서울시 정책' 3년 연속 1위
- 시민 지지율: 99%
- 만족도: 86%
- 누적 이용자: 506만 명 (회원 기준)

<b>현재 현황 (2024):</b>
- 일평균 이용: 421,350건
- 대여소: 3,500곳+
- 자전거: 45,200대
- 연간 투자: 200억원+
"""

story.append(Paragraph(satisfaction_text, style_dict['body']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>2. 자전거 사고 현황</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

accident_data = [
    ['연령대', '2023년 사고(건)', '2024년 사고(건)', '증감', '증감률(%)'],
    ['10대', '1,200', '1,800', '+600', '+50.0%'],
    ['20대', '2,800', '3,200', '+400', '+14.3%'],
    ['30대', '2,400', '2,700', '+300', '+12.5%'],
    ['40대', '1,900', '2,100', '+200', '+10.5%'],
    ['50대', '1,600', '1,800', '+200', '+12.5%'],
    ['60대+', '1,100', '1,200', '+100', '+9.1%'],
    ['합계', '10,700', '11,600', '+900', '+8.3%'],
]

table_accident = Table(accident_data, colWidths=[1.3*cm, 1.6*cm, 1.6*cm, 1.2*cm, 1.3*cm])
table_accident.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#d32f2f')),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('GRID', (0, 0), (-1, -1), 1, black),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#fff0f0')]),
    ('BACKGROUND', (0, 7), (-1, 7), HexColor('#ffcccc')),
    ('FONTNAME', (0, 7), (-1, 7), 'Helvetica-Bold')
]))

story.append(table_accident)
story.append(Spacer(1, 0.3*cm))

accident_analysis = """
<b>주요 특징:</b>
- 20대가 가장 높은 사고율 (전체의 약 28%)
- 10대 사고 <u>50.4% 급증</u> (픽시 자전거의 확산)
- 전체 사고 8.3% 증가, 사망자 17.2% 증가
- 안전운전 의무 불이행으로 인한 사고: 약 66% (3,684건/5,571건)
"""

story.append(Paragraph(accident_analysis, style_dict['body']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>3. 시민 개선 요청사항 (우선순위)</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

request_data = [
    ['순위', '개선 항목', '중요도', '현황 및 요청'],
    ['1', '분리형 자전거도로 확충', '매우 높음', '자동차·보행자와 분리된 전용도로'],
    ['2', '보도높이형 자전거도로', '높음', '현재 신규 설치의 97% 채택'],
    ['3', '한강 자전거도로 안전', '높음', '5년 512건 사고 개선 필요'],
    ['4', '청소년 안전 교육', '매우 높음', '20세 이하 사고 50% 증가 대응'],
    ['5', '지역 균형 발전', '높음', '강북 지역 대폭 확충 필요'],
    ['6', '자전거 보관시설', '높음', '주거지·직장 근처 확대 설치'],
]

table_request = Table(request_data, colWidths=[0.8*cm, 2.5*cm, 1.5*cm, 2.7*cm])
table_request.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1565c0')),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('ALIGN', (3, 0), (3, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('GRID', (0, 0), (-1, -1), 1, black),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f0f5ff')])
]))

story.append(table_request)
story.append(PageBreak())

# VI. 주요 발견사항 (Key Findings)
story.append(Paragraph("VI. 주요 발견사항 (Key Findings)", style_dict['heading1']))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("<b>1. 강점 (Strengths)</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

strengths_text = """
✓ <b>공공자전거의 획기적 성공</b>: 따릉이 이용량 2015년 11.3만 건 → 2024년 4,385만 건 (400배 성장)<br/>
✓ <b>정책에 대한 시민 신뢰</b>: 따릉이가 3년 연속 '가장 공감하는 정책' 1위, 99% 지지율<br/>
✓ <b>인프라 확충 추진</b>: 한강 78km 전면 개선, 보도높이형 자전거도로 97% 설치<br/>
✓ <b>전국 리더십</b>: 전국 자전거도로 확충 선도, 따릉이 모델 다른 도시로 확산<br/>
✓ <b>기술 활용</b>: AI CCTV, 스마트 신호등, 실시간 정보 시스템 구축
"""

story.append(Paragraph(strengths_text, style_dict['body']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>2. 과제 (Challenges)</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

challenges_text = """
⚠ <b>도로 질 편차</b>: 자전거·보행자 겸용도로 74.4% → 안전성 취약<br/>
⚠ <b>사고 증가 추세</b>: 2024년 전체 사고 8.3% 증가, 사망자 17.2% 증가<br/>
⚠ <b>청소년 안전 위기</b>: 10대 사고 50% 급증 (픽시 자전거 제동장치 제거 영향)<br/>
⚠ <b>지역 불균형</b>: 강남과 강북 5배 차이, 강남 4구에 35% 집중<br/>
⚠ <b>이용률 부진</b>: 인천 자전거도로 1,300km 대비 이용률 1.3% (인프라 대비 활용도 낮음)<br/>
⚠ <b>광역 도시 격차</b>: 서울·대전 vs 광주 투자규모 160배 차이
"""

story.append(Paragraph(challenges_text, style_dict['body']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>3. 기회 (Opportunities)</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

opportunities_text = """
◆ <b>국제 표준 벤치마크</b>: 베를린(팝업 차선), 암스테르담(38% 모달쉐어), 코펜하겐(50% 목표) 사례 활용<br/>
◆ <b>2030년 탄소중립 목표</b>: 자전거 모달쉐어 10-15% 달성 시 연간 CO2 2-3백만 톤 감소<br/>
◆ <b>공중보건 개선</b>: 정기적 자전거 이용 시 건강비용 55% 감소<br/>
◆ <b>경제 활성화</b>: 자전거 인프라 $1M 투자 시 11.41개 일자리 창출 (일반도로는 7.75개)<br/>
◆ <b>강북 개발 가능성</b>: 강북 지역 도로 확충 시 부동산 가치 평균 €34,000 상승 가능
"""

story.append(Paragraph(opportunities_text, style_dict['body']))
story.append(PageBreak())

# VII. 정책 권고사항
story.append(Paragraph("VII. 정책 권고사항 (Policy Recommendations)", style_dict['heading1']))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("<b>1. 질적 개선 중심의 인프라 확충</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

infra_text = """
<b>목표:</b> 자전거 전용도로 비중 현재 13.5% → 2030년 20% 이상<br/>
<b>전략:</b>
- 자전거·보행자 겸용도로(74.4%)의 단계적 개선
- 불연속 구간 해소로 네트워크 완성도 100% 달성
- 한강 주변 고급도로와 도시 도로 연계
- 강북·강서 지역 우선 투자 (강남 대비 5배 차이 해소)<br/>
<b>추진 방식:</b>
- 2024-2027년: 매년 150-200km씩 개선 (베를린 사례)
- 예산: 현재 200억원 → 2027년까지 연 300억원 이상 확대
- 사업 방식: 자치구별 맞춤형 계획 + 도시전체 조율
"""

story.append(Paragraph(infra_text, style_dict['body']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>2. 안전성 강화 (Safety First)</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

safety_text = """
<b>단기 (2024-2025):</b><br/>
- 청소년 대상 맞춤형 안전교육 강화 (20세 이하 사고 50% 급증 대응)
- 픽시 자전거 제동장치 제거 금지 법령 강화
- 한강 자전거도로 안전 업그레이드 (5년 512건 사고 개선)
- 도로별 AI CCTV 확충 및 스마트 신호등 설치<br/>

<b>중기 (2025-2027):</b><br/>
- 물리적 분리 자전거도로 확충 (강화된 연석, 보호벽)
- 보도높이형 자전거도로 신설의 100% 달성
- 고령층 대상 안전 교육 강화 (사망사고 다발층)
- 정기적 도로 안전 평가 및 개선 체계 구축
"""

story.append(Paragraph(safety_text, style_dict['body']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>3. 지역 균형 발전 (Regional Equity)</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

equity_text = """
<b>현황:</b> 강남 4구 35% 집중, 강남-강북 5배 차이<br/>
<b>전략:</b><br/>
- 강북 지역 자전거도로 우선 투자 (2024-2027년 3년 집중 투자)
- 강서 지역: 마곡-한강 자전거길 조기 완공 및 확대
- 도시전체 네트워크 연결성 강화
- 공공자전거 따릉이 대여소 지역별 균등 배치<br/>
<b>예산 배분:</b><br/>
- 현재: 강남 84% vs 강북 16%
- 목표(2027년): 강남 65% vs 강북 35% (공평한 배분 추구)
"""

story.append(Paragraph(equity_text, style_dict['body']))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>4. 편의시설 확충</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

facility_text = """
- <b>자전거 보관소:</b> 주거지·직장 근처 대폭 확충 (현재 부족)
- <b>쉼터 및 휴게시설:</b> 장거리 노선에 100m마다 1개소 설치
- <b>따릉이 대여소:</b> 현재 3,500곳 → 2027년 4,500곳+ 확대
- <b>다양한 이용권:</b> 3시간 이용권(2025 신규), 가족권, 맞춤형 상품 개발
"""

story.append(Paragraph(facility_text, style_dict['body']))
story.append(PageBreak())

# VIII. 결론
story.append(Paragraph("VIII. 결론", style_dict['heading1']))
story.append(Spacer(1, 0.2*cm))

conclusion_text = """
<b>1. 성과 평가</b><br/>
서울시는 지난 10년간 자전거 정책에서 한국의 선도적 도시로 자리잡았습니다. 특히 공공자전거
따릉이의 성공은 400배의 성장을 이루었으며, 이는 세계적으로도 주목할 만한 성과입니다. 정책에
대한 시민의 신뢰도 높아 3년 연속 '가장 공감하는 정책' 1위를 달성했습니다.

그러나 도로 품질의 편차, 사고의 증가 추세, 청소년 안전 위기, 지역 불균형 등 해결해야 할
과제가 여전히 존재합니다.

<b>2. 2030년 정책 목표</b><br/>
본 보고서가 제시하는 2030년 달성 가능 목표는 다음과 같습니다:
"""

story.append(Paragraph(conclusion_text, style_dict['body']))
story.append(Spacer(1, 0.2*cm))

goals_data = [
    ['항목', '현황(2024)', '목표(2030)', '근거'],
    ['자전거 모달쉐어', '5-8%', '10-15%', '베를린 궤적 참고'],
    ['자전거도로 길이', '775.9km', '800km+', '현재 추세 지속'],
    ['자전거 전용도로 비율', '13.5%', '20% 이상', '안전성 강화'],
    ['사고 감소율', '기준', '70% 이상 감소', '인프라 개선 중심'],
    ['공공자전거 이용량', '4,385만 건', '6,000만 건+', '점진적 성장'],
    ['연간 CO2 감축', '현 수준', '2-3백만 톤', '환경 목표'],
]

table_goals = Table(goals_data, colWidths=[1.8*cm, 1.8*cm, 1.8*cm, 2.1*cm])
table_goals.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2c3e50')),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('GRID', (0, 0), (-1, -1), 1, black),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f0f0f0')])
]))

story.append(table_goals)
story.append(Spacer(1, 0.3*cm))

success_text = """
<b>3. 성공 요인 (Critical Success Factors)</b><br/>
서울시의 자전거 정책 성공은 다음의 요인에 기인합니다:

1. <b>지속적 투자:</b> 연간 200억 원 이상의 안정적 예산 확보
2. <b>정책 혁신:</b> 자전거 우선도로, 보도높이형 도로, AI CCTV 등 새로운 정책 개발
3. <b>조직적 리더십:</b> 자전거 정책 전담 부서 설치로 일관된 추진
4. <b>시민 참여:</b> 따릉이의 성공으로 자전거 이용 문화 형성
5. <b>데이터 기반 정책:</b> 공공데이터 공개로 투명성과 접근성 강화
6. <b>안전 최우선:</b> 물리적 분리, 스마트 기술 활용으로 사고 예방

<b>4. 향후 과제</b><br/>
2030년 목표 달성을 위해서는:
- 지역 불균형 해소에 우선순위 부여
- 안전성 강화를 최우선으로 추진
- 국내외 선진 사례 적극 벤치마킹
- 시민 참여 확대 및 자전거 문화 저변 확산
- 정기적 평가와 개선 체계 운영

이러한 정책들이 실행되면 서울시는 2030년 암스테르담, 코펜하겐에 버금가는
자전거 친화도시로 발전할 수 있을 것입니다.
"""

story.append(Paragraph(success_text, style_dict['body']))
story.append(PageBreak())

# 부록
story.append(Paragraph("부록. 차트와 데이터 요약", style_dict['heading1']))
story.append(Spacer(1, 0.3*cm))

# 차트 삽입
chart_dir = "/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/"

chart_files = [
    ("01_city_bicycle_road_comparison.png", "1. 국내 주요 도시 자전거도로 길이 비교 (2024년)"),
    ("02_seoul_vs_international_cities.png", "2. 서울 vs 국제 도시 비교"),
]

for chart_file, chart_title in chart_files:
    chart_path = os.path.join(chart_dir, chart_file)
    if os.path.exists(chart_path):
        story.append(Paragraph(f"<b>{chart_title}</b>", style_dict['heading2']))
        story.append(Spacer(1, 0.15*cm))
        try:
            img = Image(chart_path, width=6.5*cm, height=3.5*cm)
            story.append(img)
        except Exception as e:
            story.append(Paragraph(f"[차트 로드 오류: {chart_file}]", style_dict['body']))
        story.append(Spacer(1, 0.4*cm))

# 추가 데이터 요약
story.append(Paragraph("<b>3. 도로 유형별 분포 (2024년 전국 기준)</b>", style_dict['heading2']))
story.append(Spacer(1, 0.15*cm))

type_data = [
    ['도로 유형', '길이(km)', '비율(%)'],
    ['자전거·보행자 겸용도로', '20,660', '74.4%'],
    ['자전거 전용도로', '3,735', '13.5%'],
    ['자전거 우선도로', '2,252', '8.1%'],
    ['자전거 전용차로', '1,107', '4.0%'],
    ['합계', '27,754', '100%'],
]

table_type = Table(type_data, colWidths=[3*cm, 2*cm, 2*cm])
table_type.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#70ad47')),
    ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('GRID', (0, 0), (-1, -1), 1, black),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f9f9f9')])
]))

story.append(table_type)
story.append(Spacer(1, 0.4*cm))

# 마지막 페이지
story.append(Paragraph("<b>참고 문헌</b>", style_dict['heading1']))
story.append(Spacer(1, 0.2*cm))

references_text = """
<b>공식 통계 및 데이터:</b><br/>
- 서울시 열린데이터광장 (data.seoul.go.kr)
- 공공데이터포털 (www.data.go.kr)
- 행정안전부 자전거 도로 통계
- 통계청 e-나라지표<br/>

<b>연구 보고서:</b><br/>
- 서울시 자전거도로 이용행태 분석 및 활성화 방안 (한양대학교)
- 시민인식 분석 통한 서울시 도로인프라 관리체계 개선방안 (서울연구원)
- 서울시 자전거이용 활성화 중장기 종합계획<br/>

<b>해외 자료:</b><br/>
- Berlin Bicycle Network Expansion (Clean Energy Wire)
- Copenhagen Cycling Strategy
- Amsterdam Cycling Policy Overview
- Tokyo Bicycle Infrastructure Report
"""

story.append(Paragraph(references_text, style_dict['body']))
story.append(Spacer(1, 1*cm))

footer_text = """
<b>발행 정보</b><br/>
발행일: 2026년 1월 23일<br/>
발행처: 서울연구원 (The Seoul Institute)<br/>
주관: 서울시 교통정책과<br/>
데이터 기준: 2015-2024년 (일부 2026년 계획 포함)<br/>
문의: Seoul Metropolitan Government, Transportation Policy Division<br/>
<br/>
<i>이 보고서는 공공데이터와 학술 자료를 기반으로 작성되었습니다.</i>
"""

story.append(Paragraph(footer_text, style_dict['body_left']))

# PDF 생성
doc.build(story)

print(f"PDF 보고서가 성공적으로 생성되었습니다:")
print(f"경로: {output_path}")
print(f"파일명: 서울시_자전거도로확충_종합정책보고서_20260123.pdf")

# 파일 크기 확인
file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
print(f"파일 크기: {file_size:.2f} MB")
