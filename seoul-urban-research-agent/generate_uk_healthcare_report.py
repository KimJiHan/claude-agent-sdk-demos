#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
영국 의료 산업 포괄적 시장 분석 및 전략 기회
UK Healthcare Industry Comprehensive Market Analysis Report Generator
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, PageTemplate, Frame
from reportlab.pdfgen import canvas
from datetime import datetime
import os

# Define page dimensions
page_width, page_height = A4

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_state = None

    def showPage(self):
        self._saved_state = dict(self.__dict__)
        self._startPage()

    def save(self):
        num_pages = self._pageNumber
        if self._saved_state is None:
            canvas.Canvas.save(self)
            return

        for page_num in range(1, num_pages + 1):
            self._page_number = page_num
            canvas.Canvas.save(self)

        self._pageNumber = num_pages


def create_footer(canvas, doc):
    """Add page numbers and footer to each page"""
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    page_num = canvas.getPageNumber()
    text = f"페이지 {page_num}"
    canvas.drawRightString(page_width - 0.5*inch, 0.5*inch, text)
    canvas.restoreState()


def create_uk_healthcare_report():
    """Generate comprehensive UK Healthcare Market Analysis Report in Korean"""

    output_path = "/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/reports/uk_healthcare_market_analysis_report_20260123.pdf"

    # Create PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=12*mm,
        leftMargin=12*mm,
        topMargin=15*mm,
        bottomMargin=15*mm,
        title="영국 의료 산업 포괄적 시장 분석",
        author="Research Analysis System",
        subject="UK Healthcare Market Analysis Report 2026"
    )

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles for Korean text
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=36
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#4a7ba7'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica',
        leading=18
    )

    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        leading=18
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#4a7ba7'),
        spaceAfter=4,
        spaceBefore=8,
        fontName='Helvetica-Bold',
        leading=14
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=14,
        fontName='Helvetica'
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['BodyText'],
        fontSize=10,
        leftIndent=12,
        spaceAfter=4,
        leading=12,
        fontName='Helvetica'
    )

    # Build document content
    content = []

    # ===== PAGE 1: COVER PAGE =====
    content.append(Spacer(1, 2*inch))

    # Title
    content.append(Paragraph("영국 의료 산업", title_style))
    content.append(Paragraph("포괄적 시장 분석 및 전략 기회", title_style))

    content.append(Spacer(1, 0.5*inch))

    # Subtitle
    content.append(Paragraph("Comprehensive Market Analysis & Strategic Opportunities", subtitle_style))

    content.append(Spacer(1, 1*inch))

    # Date and info
    date_text = f"발행일: 2026년 1월 23일"
    content.append(Paragraph(date_text, subtitle_style))
    content.append(Paragraph("Research Period: 2023-2026", body_style))

    content.append(Spacer(1, 0.8*inch))

    # Document info
    info_data = [
        ["보고서 범위", "영국 의료 산업 전체 (의료 서비스, 제약, 의료기기, 디지털 보건)"],
        ["연구 기간", "2023년 1월 - 2026년 1월"],
        ["주요 데이터", "시장 규모, 성장 전망, 규제 환경, 서비스 격차, 기회 분석"],
        ["분석 방식", "정량적 데이터, 정성적 분석, 전략 평가"]
    ]

    info_table = Table(info_data, colWidths=[100*mm, 100*mm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0f7')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    content.append(info_table)

    content.append(PageBreak())

    # ===== PAGE 2: EXECUTIVE SUMMARY =====
    content.append(Paragraph("요약", heading1_style))

    summary_text = """
    <b>영국 의료 산업 개요</b><br/>
    영국 의료 산업은 2023-2026 기간 동안 3.5% CAGR(복합연간성장률)로 안정적인 성장을 보이고 있으며,
    특히 디지털 의료 기술은 18.9-22.8% CAGR의 폭발적 성장을 경험하고 있습니다.
    NHS 현대화, 민간 부문 확대, 기술 혁신이 주요 성장 동력입니다.<br/><br/>

    <b>주요 시장 규모 (2024-2025)</b><br/>
    • 전체 의료 지출: £317 억 (2024년)<br/>
    • 병원 서비스: £127 억<br/>
    • 민간 의료: USD 14.3 억 (2025년 추정)<br/>
    • 디지털 의료: USD 15.46 억 (2025년)<br/>
    • 의료 기기: USD 69.28 억 (2035년 예측)<br/><br/>

    <b>성장 기회</b><br/>
    디지털 의료 기술, 정신 건강 서비스, 노인 장기 요양, 원격 의료, 여성 건강, 암 선별,
    물리 치료 및 재활, 소수 민족 의료 서비스, 민간 의료 부문, 의료 인력 교육 등에서
    상당한 시장 기회가 존재합니다.<br/><br/>

    <b>주요 도전과제</b><br/>
    • NHS 자금 부족 (2025-26년 £6.6 억 부족)<br/>
    • 100,020명의 의료 인력 공석<br/>
    • 의료 기기 규제 복잡성 (Brexit 이후)<br/>
    • 환자 대기 시간 (특히 정신 건강 및 치과)<br/>
    • 지역별 서비스 격차<br/><br/>

    <b>전략적 권고사항</b><br/>
    1. 디지털 의료 기술 투자 가속화<br/>
    2. 정신 건강 서비스 확대<br/>
    3. 노인 장기 요양 인프라 개선<br/>
    4. 민간 부문과의 협력 강화<br/>
    5. 의료 인력 양성 프로그램 확대
    """

    content.append(Paragraph(summary_text, body_style))
    content.append(Spacer(1, 0.3*inch))

    content.append(PageBreak())

    # ===== PAGE 3-4: MARKET OVERVIEW =====
    content.append(Paragraph("1. 시장 개요", heading1_style))

    # Current trends
    content.append(Paragraph("1.1 현황 및 동향", heading2_style))

    trends_text = """
    <b>시장 규모 및 성장률</b><br/>
    영국 의료 산업은 2024년 £317 억 규모로 GDP의 11.1%를 차지하고 있으며,
    유럽에서 5위의 의료 지출 규모를 보유하고 있습니다.
    2023-2026 기간 동안 평균 3.5% CAGR의 성장이 예상되고 있습니다.<br/><br/>

    <b>NHS 현황</b><br/>
    • 병원 수익: £127 억 (2023년)<br/>
    • 2025-26 계획 예산: £215.6 억 (실제 가격)<br/>
    • 자금 부족: £6.6 억 (2025-26년)<br/>
    • 평균 실질 성장률: 3% (2025-26년 ~ 2028-29년)<br/>
    • 직원 비용: 일일 지출의 50%를 차지<br/>
    • 기술 및 디지털 변환: £10 억 증가 예정 (2028-29년까지)<br/><br/>

    <b>NHS 디지털 전환</b><br/>
    • 2026년 3월까지 70% 신뢰가 표준 핵심 수준 디지털화 달성<br/>
    • 현재 45% NHS 서비스가 디지털 경로 부족<br/>
    • 10-70% NHS 신뢰 기술 자산이 레거시 시스템으로 분류<br/>
    • AI 기반 이니셔티브: My Companion, 검증된 AI 진단 도구, 지능형 분류<br/>
    • 2026년 AI 규제 프레임워크 발행 예정
    """

    content.append(Paragraph(trends_text, body_style))
    content.append(Spacer(1, 0.2*inch))

    # Growth prospects
    content.append(Paragraph("1.2 성장 전망 (2023-2026)", heading2_style))

    growth_text = """
    <b>주요 성장 부문</b><br/>
    • <b>디지털 의료</b>: 18.9-22.8% CAGR (가장 빠른 성장)<br/>
    &nbsp;&nbsp;&nbsp;- 2024년: USD 12,518.9 백만<br/>
    &nbsp;&nbsp;&nbsp;- 2025년: USD 15.46 억<br/>
    &nbsp;&nbsp;&nbsp;- 2030년 예측: USD 36.84 ~ 42,371.4 백만<br/><br/>

    • <b>의료 정보 시스템</b>: 14.6% CAGR<br/>
    &nbsp;&nbsp;&nbsp;- 2023년: USD 20,276.4 백만<br/>
    &nbsp;&nbsp;&nbsp;- 2030년 예측: USD 52,749.7 백만<br/><br/>

    • <b>민간 의료</b>: 3.4% CAGR<br/>
    &nbsp;&nbsp;&nbsp;- 2024년: USD 13.75 억<br/>
    &nbsp;&nbsp;&nbsp;- 2025년: USD 14.3 억<br/>
    &nbsp;&nbsp;&nbsp;- 2033년 목표: USD 18.56 억<br/><br/>

    • <b>의료 기기</b>: 7.19% CAGR<br/>
    &nbsp;&nbsp;&nbsp;- 2025년: 성장 추세<br/>
    &nbsp;&nbsp;&nbsp;- 2035년 예측: USD 69.28 억<br/><br/>

    • <b>기타 부문</b>:<br/>
    &nbsp;&nbsp;&nbsp;- 재택 의료: 7.1% CAGR (USD 2.60 억 예측, 2030년)<br/>
    &nbsp;&nbsp;&nbsp;- 건강 검진 서비스: 6.08% CAGR<br/>
    &nbsp;&nbsp;&nbsp;- 의료 보험: 4.54% CAGR (USD 13.78 억 예측, 2030년)
    """

    content.append(Paragraph(growth_text, body_style))

    # Try to add first chart
    try:
        chart_path = "/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/01_uk_healthcare_sector_comparison.png"
        if os.path.exists(chart_path):
            content.append(Spacer(1, 0.2*inch))
            content.append(Paragraph("<b>그림 1: 의료 부문별 시장 규모 비교</b>", heading2_style))
            img = Image(chart_path, width=4.5*inch, height=3*inch)
            content.append(img)
    except Exception as e:
        print(f"Warning: Could not add chart 1: {e}")

    content.append(PageBreak())

    # Regulatory environment
    content.append(Paragraph("1.3 규제 환경", heading2_style))

    regulatory_text = """
    <b>주요 규제 기관</b><br/>
    • <b>CQC (Care Quality Commission)</b>: 의료 서비스 품질 규제<br/>
    &nbsp;&nbsp;&nbsp;- 2023년 11월 단일 평가 프레임워크(SAF) 시행<br/>
    &nbsp;&nbsp;&nbsp;- 2026년 9월까지 9,000개 평가 목표<br/><br/>

    • <b>NICE (National Institute for Health and Care Excellence)</b>: 임상 지침 및 기술 평가<br/>
    &nbsp;&nbsp;&nbsp;- 2024년 심각도 프리미엄 도입<br/>
    &nbsp;&nbsp;&nbsp;- 2023-2024년 의료 접근성: 31% (2020-2022년 45%에서 감소)<br/><br/>

    • <b>GMC (General Medical Council)</b>: 의사 등록 및 전문성 표준<br/>
    &nbsp;&nbsp;&nbsp;- 2024년 해외 의사 의료 라이센싱 평가(MLA) 필수<br/>
    &nbsp;&nbsp;&nbsp;- 약 270,000명의 의사 등록<br/><br/>

    • <b>NMC (Nursing and Midwifery Council)</b>: 간호사 및 조산사 규제<br/>
    &nbsp;&nbsp;&nbsp;- 2024년 조산사 문화 역량 의무 교육<br/>
    &nbsp;&nbsp;&nbsp;- 약 680,000명의 의료 전문가 등록<br/><br/>

    • <b>MHRA (Medicines and Healthcare Products Regulatory Agency)</b>: 의약품 및 의료기기 규제<br/>
    &nbsp;&nbsp;&nbsp;- 2024년 1월 국제 인정 절차(IRP) 시행<br/>
    &nbsp;&nbsp;&nbsp;- 2025년 6월 상시 시장 감시(PMS) 요구사항 발효<br/><br/>

    <b>Brexit 이후 규제 환경</b><br/>
    • 의약품: 별도 MHRA 승인 필요 (이전 EMA 의존)<br/>
    • 의료기기: 국제 상호 인정 프레임워크 도입<br/>
    • GDPR: UK GDPR 유지, 2025년 6월 적절성 검토 완료<br/>
    • 데이터 보호: 강화된 개인정보 보호 요구사항
    """

    content.append(Paragraph(regulatory_text, body_style))

    content.append(PageBreak())

    # ===== PAGE 5-6: SERVICE GAPS & OPPORTUNITIES =====
    content.append(Paragraph("2. 서비스 격차 및 기회 분석", heading1_style))

    content.append(Paragraph("2.1 10대 핵심 부문 분석", heading2_style))

    # Gap analysis table
    gap_data = [
        ["순위", "부문", "심각도", "현황", "시장 기회"],
        ["1", "정신 건강 서비스", "85", "심각한 부족", "USD 기술 플랫폼, 직업 보건"],
        ["2", "노인 장기 요양", "78", "심각한 결손", "기술 솔루션, 서비스 확대"],
        ["3", "원격/디지털 의료", "72", "급속한 확대", "지속적 투자 필요"],
        ["4", "전문 서비스", "68", "지역별 편차", "배포 개선"],
        ["5", "응급 의료", "65", "지역 격차", "용량 최적화"],
        ["6", "진단 서비스", "58", "중간 부족", "장비 투자"],
        ["7", "재활 서비스", "55", "제한적 가용성", "시설 확대"],
        ["8", "지역사회 돌봄", "52", "불균등한 적용", "네트워크 강화"],
        ["9", "기초 의료 접근", "48", "변수 접근", "클리닉 확대"],
        ["10", "소아/모성 서비스", "45", "부분 격차", "전문가 지원"]
    ]

    gap_table = Table(gap_data, colWidths=[20*mm, 35*mm, 20*mm, 35*mm, 40*mm])
    gap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
    ]))
    content.append(gap_table)

    content.append(Spacer(1, 0.3*inch))

    # Try to add gap analysis chart
    try:
        chart_path = "/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/03_service_gap_analysis.png"
        if os.path.exists(chart_path):
            content.append(Paragraph("<b>그림 2: 서비스 격차 분석 - 심각도별 순위</b>", heading2_style))
            img = Image(chart_path, width=5*inch, height=3.5*inch)
            content.append(img)
    except Exception as e:
        print(f"Warning: Could not add chart 2: {e}")

    content.append(PageBreak())

    # Detailed gap descriptions
    content.append(Paragraph("2.2 핵심 부문 상세 분석", heading2_style))

    detailed_gaps = """
    <b>1. 정신 건강 서비스 (심각도: 85)</b><br/>
    • 대기 명단: 170만 명<br/>
    • 연간 의뢰: 520만 건 (2024년)<br/>
    • 공석률: 9.9%, 10,000+ 정신 건강 간호사 부족<br/>
    • 환자 영향: 42% 대기 중 정신 건강 악화<br/>
    • 시장 기회: 디지털 정신 건강 플랫폼, EAP, 직업 보건 솔루션<br/><br/>

    <b>2. 노인 장기 요양 (심각도: 78)</b><br/>
    • 공석: 165,000명 (사회 돌봄)<br/>
    • 필요 증가: 연 110,000명, 10년간 필요<br/>
    • 2030/31년 부족: 627,000명<br/>
    • 문제: 저임금, 높은 업무량, 경력 부족<br/>
    • 시장 기회: 재택 돌봄 서비스, 원격 모니터링, 스마트 홈 솔루션<br/><br/>

    <b>3. 원격/디지털 의료 (심각도: 72)</b><br/>
    • 2026년 시장 규모: USD 4.5 억<br/>
    • 2036년 예측: USD 21.7 억 (17.1% CAGR)<br/>
    • 광범위한 디지털 의료: 2033년까지 USD 37.6 억<br/>
    • 시장 기회: 원격 진료, 가상 병동, 재택 의료<br/><br/>

    <b>4. 치과 서비스 (심각도: 72)</b><br/>
    • 새로운 성인 환자를 위한 NHS 약속: 10명 중 9명 불가능<br/>
    • 새로운 아동 환자: 10명 중 8명 불가능<br/>
    • 대기 시간: 지역별 6개월 ~ 2년<br/>
    • 충족되지 않은 수요: 1,300만 명<br/>
    • 2026년 NHS 개혁: 필수 긴급 관리 임명<br/>
    • 시장 기회: 민간 치과 클리닉, 디지털 치과 스타트업<br/><br/>

    <b>5. 여성 건강 및 불임 치료 (심각도: 68)</b><br/>
    • NICE 권장사항: 40세 미만 여성 3회 IVF 시술<br/>
    • 현실: 대부분 1-2회, 일부는 없음<br/>
    • 개인 부담: £3,000-£5,000 (표준), £20,000+ (추가 포함)<br/>
    • 부담 능력: 20%만 민간 치료 가능, 40% 유산 불가<br/>
    • 인구학적 문제: 2010년 이후 25% 출산율 감소<br/>
    • 시장 기회: 민간 불임 클리닉, 직장 생식 보건 혜택<br/><br/>

    <b>6. 재활 및 물리 치료 (심각도: 65)</b><br/>
    • 물리 치료사: 2명 중 2/3가 인력 부족<br/>
    • 대기 명단: 323,965명 (2024년 3월)<br/>
    • 연간 증가: 11% (전년대비)<br/>
    • NHS 성장: 10년 동안 3.3%만 증가 (전문직 성장 뒤처짐)<br/>
    • 긍정적 발전: 2025년 3,000+ 물리 치료사 졸업 예상<br/>
    • 시장 기회: 민간 물리 치료 클리닉, 디지털 재활 플랫폼
    """

    content.append(Paragraph(detailed_gaps, body_style))

    content.append(PageBreak())

    # NHS vs Private healthcare comparison
    content.append(Paragraph("2.3 NHS vs 민간 의료", heading2_style))

    comparison_text = """
    <b>민간 의료 시장 동향</b><br/>
    • 2023년 입원: 898,000명 (2016년 이후 최고)<br/>
    • 2024년 입원: 939,000명 (3% 증가, 3년 연속 최고)<br/>
    • 2024년 시장 가치: USD 13.75 억<br/>
    • 2025년 시장 가치: USD 14.3 억 (추정)<br/>
    • 2033년 목표: USD 18.56 억 (3.4% CAGR)<br/><br/>

    <b>2024-2025년 시장 냉각 신호</b><br/>
    • Q1 2025 입원: 240,730명 (Q1 2024 대비 4% 감소)<br/>
    • 자비 입원: 4% 감소<br/>
    • 시장 가치 성장: 2024년 6.9% (실제: 4.2%)<br/>
    • 이전 3년 성장률: 9.8% ~ 13.7% (연년)<br/><br/>

    <b>민간 의료 성장 동인</b><br/>
    1. NHS 아웃소싱: 선택 수술 계속 아웃소싱<br/>
    2. 의료 보험 확대: 기업 및 개인 보험<br/>
    3. 자비 환자 수요: 특히 20-39세 인구<br/>
    4. 고급 시술: 최소 침습, 로봇 수술<br/>
    5. 20-39세 입원: Q1 2024 13% 성장<br/>
    6. 첨단 진단: 최신 진단 기술 도입<br/><br/>

    <b>NHS 대기 명단</b><br/>
    • 2024년 12월 말 기준: 746만 명<br/>
    • 선택 수술 대기: 대부분 1년 이상<br/>
    • 진단 기간: 62일 표준 달성 78% (2024년)<br/>
    • 암 치료: 75% 목표 2026년 3월까지 (현재 78%)<br/>
    • 영향: 민간 부문으로의 환자 유출 지속
    """

    content.append(Paragraph(comparison_text, body_style))

    # Try to add NHS vs Private chart
    try:
        chart_path = "/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/02_nhs_vs_private_growth_trend.png"
        if os.path.exists(chart_path):
            content.append(Spacer(1, 0.2*inch))
            content.append(Paragraph("<b>그림 3: NHS vs 민간 의료 성장 추이 (2023-2033)</b>", heading2_style))
            img = Image(chart_path, width=5*inch, height=3*inch)
            content.append(img)
    except Exception as e:
        print(f"Warning: Could not add chart 3: {e}")

    content.append(PageBreak())

    # ===== PAGE 7-8: TECHNOLOGY & INNOVATION =====
    content.append(Paragraph("3. 의료 기술 및 혁신", heading1_style))

    content.append(Paragraph("3.1 디지털 의료 시장 분석", heading2_style))

    tech_text = """
    <b>시장 규모 및 성장률</b><br/>
    • 2024년: USD 12,518.9 백만<br/>
    • 2025년: USD 15.46 억<br/>
    • 2030년 예측: USD 36.84 ~ 42,371.4 백만<br/>
    • CAGR (2024-2030): 18.9% ~ 22.8%<br/>
    • 지위: 전 세계 가장 빠르게 성장하는 부문 중 하나<br/><br/>

    <b>의료 정보 시스템</b><br/>
    • 2023년: USD 20,276.4 백만<br/>
    • 2030년 예측: USD 52,749.7 백만<br/>
    • CAGR (2024-2030): 14.6%<br/>
    • 초점: 의료 시스템 전반의 데이터 통합<br/><br/>

    <b>의료 컨설팅</b><br/>
    • 2023년: USD 10.4 억<br/>
    • 2030년 예측: USD 18.7 억<br/>
    • CAGR (2024-2030): 8.8%<br/>
    • 서비스: 변환 전략, 디지털 구현, 워크플로우 최적화<br/><br/>

    <b>UK 헬스테크 투자</b><br/>
    • 2025년 투자: £1.8 억<br/>
    • 지위: 유럽 디지털 의료 혁신의 선두<br/>
    • 회사 성장: UK 헬스테크 기업이 글로벌 기업으로 성장<br/>
    • 자금원: NHS 디지털 변환과 함께 개인 투자 증가
    """

    content.append(Paragraph(tech_text, body_style))

    content.append(Spacer(1, 0.2*inch))

    content.append(Paragraph("3.2 주요 기술 혁신 (2025-2026)", heading2_style))

    innovation_text = """
    <b>인공지능 및 진단</b><br/>
    • <b>My Companion</b>: NHS App에 통합된 AI 건강 조언<br/>
    • <b>검증된 AI 진단 도구</b>: NHS 서비스 전역 배포 확대<br/>
    • <b>임상 문서 자동화</b>: 음성 기술 활용<br/>
    • <b>지능형 분류</b>: NHS App을 통한 AI 지원 응급 분류<br/>
    • <b>2026년 규제 프레임워크</b>: 국가 AI 규제 위원회<br/><br/>

    <b>데이터 통합 및 분석</b><br/>
    • <b>통합 환자 기록</b>: 2차, 1차, 지역사회 돌봄 정보 통합<br/>
    • <b>연합 데이터 플랫폼</b>: AI 기반 분석 확대<br/>
    • <b>생성형 AI</b>: 데이터 분석 주도<br/>
    • <b>통합 시스템</b>: 돌봄 조율 및 의사결정 지원 개선<br/><br/>

    <b>기술 활성화 의료 모델</b><br/>
    • <b>가상 병동</b>: 원격 환자 모니터링 확대<br/>
    • <b>재택 병원 모델</b>: 퇴원 계획에 통합<br/>
    • <b>원격 환자 모니터링</b>: 만성질환 관리<br/>
    • <b>원격 의료</b>: 가상 진료 및 추후관찰<br/><br/>

    <b>첨단 의료 기술</b><br/>
    • <b>로봇 보조 수술</b>: NHS 및 민간 부문 도입 확대<br/>
    • <b>최소 침습 시술</b>: 수요 및 구현 증가<br/>
    • <b>AI 가상 어시스턴트</b>: 환자 참여 및 분류<br/><br/>

    <b>게노믹스 및 개인맞춤의료</b><br/>
    • <b>전체 게놈 염기서열 분석</b>: 암 치료 개인화<br/>
    • <b>블록체인 기술</b>: 데이터 보안 및 상호운용성<br/>
    • <b>맞춤 치료</b>: 개인화된 치료 계획
    """

    content.append(Paragraph(innovation_text, body_style))

    content.append(PageBreak())

    # Technology market forecast chart
    try:
        chart_path = "/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/04_healthcare_tech_growth_forecast.png"
        if os.path.exists(chart_path):
            content.append(Paragraph("<b>그림 4: 의료 기술 시장 성장 전망 (2025-2030)</b>", heading2_style))
            img = Image(chart_path, width=5*inch, height=3*inch)
            content.append(img)
            content.append(Spacer(1, 0.2*inch))
    except Exception as e:
        print(f"Warning: Could not add chart 4: {e}")

    content.append(Paragraph("3.3 기술 채택 장애요소 및 기회", heading2_style))

    barrier_text = """
    <b>디지털 변환 과제</b><br/>
    • 자금 제약: 투자 제한으로 인한 실행 지연<br/>
    • 디지털 리더십 문제: 추가 자금 없이 변화 관리<br/>
    • 디지털 불평등: 지역 전역의 불균등한 채택<br/>
    • 레거시 시스템 현대화 비용: NHS 자산 일부 10-70% 구형<br/>
    • 인력 교육 및 채택: 조직 전체 능력 배양 필요<br/><br/>

    <b>시장 기회</b><br/>
    1. <b>원격의료 플랫폼</b>: 1차 의료 제공자용<br/>
    2. <b>가상 진료 솔루션</b>: 환자 접근성 개선<br/>
    3. <b>원격 모니터링 기술</b>: 만성질환 관리<br/>
    4. <b>디지털 진단 및 AI</b>: 초기 발견 가능<br/>
    5. <b>환자 참여 플랫폼</b>: 환자-의료제공자 소통<br/>
    6. <b>의료 IT 인프라</b>: 클라우드 및 상호운용성<br/>
    7. <b>데이터 분석 도구</b>: 통찰력 및 최적화<br/>
    8. <b>사이버 보안 솔루션</b>: 환자 데이터 보호
    """

    content.append(Paragraph(barrier_text, body_style))

    content.append(PageBreak())

    # ===== PAGE 9: EXECUTIVE RECOMMENDATIONS =====
    content.append(Paragraph("4. 경영진 권고사항", heading1_style))

    recommendations = """
    <b>전략적 우선순위</b><br/><br/>

    <b>1. 디지털 의료 기술 투자 가속화</b><br/>
    • NHS 2026년 3월까지 70% 디지털화 목표 달성 지원<br/>
    • 원격 의료 플랫폼 개발 및 배포<br/>
    • AI 진단 도구 검증 및 확대<br/>
    • 단일 환자 기록 시스템 통합<br/>
    • 투자 수익: £1.8 억 헬스테크 투자 시장 기회<br/><br/>

    <b>2. 정신 건강 서비스 긴급 확대</b><br/>
    • 현재: 170만 명 대기 (심각도 지수 85)<br/>
    • 목표: 디지털 정신 건강 플랫폼 확대<br/>
    • 행동:<br/>
    &nbsp;&nbsp;&nbsp;- EAP(직업 보건) 프로그램 확대<br/>
    &nbsp;&nbsp;&nbsp;- 치료 및 상담 서비스 민간 부문 개발<br/>
    &nbsp;&nbsp;&nbsp;- AI 기반 분류 및 선별 시스템<br/>
    &nbsp;&nbsp;&nbsp;- 지역사회 정신 건강 허브<br/>
    • 시장 기회: 중대 서비스 격차, 높은 수익성<br/><br/>

    <b>3. 노인 장기 요양 인프라 개선</b><br/>
    • 과제: 165,000명 공석, 2030/31년까지 627,000명 부족<br/>
    • 목표: 기술 기반 돌봄 솔루션 및 인력 확대<br/>
    • 행동:<br/>
    &nbsp;&nbsp;&nbsp;- 재택 돌봄 서비스 기술 투자<br/>
    &nbsp;&nbsp;&nbsp;- 스마트 홈 및 모니터링 솔루션<br/>
    &nbsp;&nbsp;&nbsp;- 돌봄 인력 교육 및 지원 프로그램<br/>
    &nbsp;&nbsp;&nbsp;- 장기 요양 시설 현대화<br/>
    • 투자 규모: 연간 110,000명 신규 인력 필요<br/><br/>

    <b>4. 민간 부문과의 협력 강화</b><br/>
    • NHS 아웃소싱 계속 확대: 선택 수술, 진단<br/>
    • 민간 의료 시장: 3.4% CAGR 지속 성장<br/>
    • 행동:<br/>
    &nbsp;&nbsp;&nbsp;- 공공-민간 협력 모델 확대<br/>
    &nbsp;&nbsp;&nbsp;- 민간 전문 서비스 활용<br/>
    &nbsp;&nbsp;&nbsp;- 기술 혁신 공유 협력<br/>
    &nbsp;&nbsp;&nbsp;- 의료 가용성 개선 파트너십<br/>
    • 목표: 7백만 명 대기 명단 감소<br/><br/>

    <b>5. 의료 인력 양성 프로그램 확대</b><br/>
    • 현황: 100,020명 공석, 1.9% 연간 성장<br/>
    • 특정 부족: 간호사, 물리 치료사, 정신 건강 전문가<br/>
    • 행동:<br/>
    &nbsp;&nbsp;&nbsp;- 의료 교육 프로그램 확대<br/>
    &nbsp;&nbsp;&nbsp;- 해외 의료 전문가 채용<br/>
    &nbsp;&nbsp;&nbsp;- 경력 개발 및 지원 강화<br/>
    &nbsp;&nbsp;&nbsp;- 직원 건강 및 보유 프로그램<br/>
    • 목표: 2036-37년까지 71,000-76,000 연합 의료 전문가 추가<br/><br/>

    <b>6. 규제 환경 적응 및 준수</b><br/>
    • Brexit 이후 의약품 및 의료기기 규제 변화<br/>
    • 2026년 AI 규제 프레임워크 발행<br/>
    • 행동:<br/>
    &nbsp;&nbsp;&nbsp;- MHRA 국제 인정 절차(IRP) 활용<br/>
    &nbsp;&nbsp;&nbsp;- AI 거버넌스 체계 구축<br/>
    &nbsp;&nbsp;&nbsp;- GDPR 및 데이터 보호 강화<br/>
    &nbsp;&nbsp;&nbsp;- 규제 모니터링 및 컴플라이언스 체계<br/><br/>

    <b>7. 건강 불평등 해소 및 형평성</b><br/>
    • 소수 민족 의료 접근성 개선<br/>
    • 지역별 서비스 격차 해소<br/>
    • 행동:<br/>
    &nbsp;&nbsp;&nbsp;- 문화 역량 교육 의무화<br/>
    &nbsp;&nbsp;&nbsp;- 해석 서비스 확대<br/>
    &nbsp;&nbsp;&nbsp;- 소수 집단 맞춤형 프로그램<br/>
    &nbsp;&nbsp;&nbsp;- 건강 격차 모니터링 강화
    """

    content.append(Paragraph(recommendations, body_style))

    content.append(PageBreak())

    # ===== PAGE 10: STATISTICS & APPENDIX =====
    content.append(Paragraph("부록 A: 통계 테이블", heading1_style))

    content.append(Paragraph("A.1 의료 지출 및 시장 규모", heading2_style))

    # Financial table
    financial_data = [
        ["부문", "2023년", "2024-25년", "2025-26년", "성장률"],
        ["병원 서비스", "£127.0B", "£127.0B", "£127.4B", "0.4% CAGR"],
        ["전체 의료 지출", "£317B", "£317B", "미정", "3.5% CAGR"],
        ["약제", "USD 미정", "USD 33.21B", "USD 34.5B", "3-4% 추정"],
        ["의료 기기", "USD 미정", "성장 중", "USD 69.28B(35)", "7.19% CAGR"],
        ["민간 의료", "USD 12.76B", "USD 13.75B", "USD 14.3B", "3.4% CAGR"],
        ["디지털 의료", "USD 12.52B", "USD 15.46B", "USD 18.8B", "18.9-22.8%"],
        ["재택 의료", "USD 1.61B", "USD 1.77B", "USD 2.60B(30)", "7.1% CAGR"]
    ]

    fin_table = Table(financial_data, colWidths=[35*mm, 30*mm, 30*mm, 30*mm, 35*mm])
    fin_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
    ]))
    content.append(fin_table)

    content.append(Spacer(1, 0.3*inch))

    content.append(Paragraph("A.2 NHS 인력 통계", heading2_style))

    # Workforce table
    workforce_data = [
        ["항목", "2024년 8월", "YoY 변화", "상태"],
        ["총 인력", "137만 FTE", "+1.9%", "증가"],
        ["간호사/보건 방문", "367,510 FTE", "+2.9%", "증가"],
        ["공석", "100,020", "-9%", "개선"],
        ["공석률", "6.7%", "-0.7pp", "개선"],
        ["평균 기본급", "£43,160", "+10.7%", "증가"],
        ["정신질환 병가", "694,800 FTE일", "30.3%", "상위 원인"],
        ["병가율", "5.1%", "-0.1pp", "감소"]
    ]

    work_table = Table(workforce_data, colWidths=[40*mm, 35*mm, 30*mm, 35*mm])
    work_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
    ]))
    content.append(work_table)

    content.append(Spacer(1, 0.3*inch))

    content.append(Paragraph("A.3 주요 규제 일정 (2025-2026)", heading2_style))

    regulatory_schedule = """
    <b>2025년</b><br/>
    • 1월 5일: MHRA 의료기기 사전 상시 시장 감시 보고서 마감<br/>
    • 1월: NMC 이사회, 실습 학습 검토 라인 승인<br/>
    • 3월: PSA 규제 데이터 및 AI 그룹 첫 회의<br/>
    • 6월: 상시 시장 감시(PMS) 요구사항 발효<br/>
    • 6월: EU 적절성 결정 검토 완료<br/>
    • 6월 이후: PSA 수용된 결과 지침 발행<br/><br/>

    <b>2026년</b><br/>
    • 2월-3월: NMC 교육 표준 상담 (학생 간호사 변경)<br/>
    • 2026년 말: PSA 규제 우수성 표준 이행<br/>
    • 9월: NMC 교육 표준 업데이트 (승인 시)<br/>
    • 계속: CQC 9,000개 평가 목표 완료<br/>
    • 계속: 국제 상호 인정 프레임워크 전면 시행
    """

    content.append(Paragraph(regulatory_schedule, body_style))

    content.append(PageBreak())

    # Conclusion
    content.append(Paragraph("결론", heading1_style))

    conclusion_text = """
    <b>요약</b><br/>
    영국 의료 산업은 2023-2026 기간 동안 3.5% CAGR의 안정적인 성장을 시현하고 있으며,
    특히 디지털 의료 기술은 18.9-22.8% CAGR의 폭발적 성장을 경험하고 있습니다.
    이는 NHS 현대화, 민간 부문 확대, 기술 혁신을 포함한 여러 요인에 의해 주도됩니다.<br/><br/>

    <b>시장 기회</b><br/>
    • 디지털 의료 기술: 가장 빠른 성장 부문 (18.9-22.8% CAGR)<br/>
    • 정신 건강 서비스: 170만 명 대기 (심각도 85)<br/>
    • 노인 요양 서비스: 2030/31년까지 627,000명 부족<br/>
    • 원격 의료: 2036년까지 USD 21.7 억 시장<br/>
    • 민간 의료: 3.4% CAGR로 지속적 성장<br/>
    • 의료 기기: 2035년까지 USD 69.28 억 (7.19% CAGR)<br/><br/>

    <b>주요 도전과제</b><br/>
    • NHS 자금 부족: 2025-26년 £6.6 억<br/>
    • 인력 공석: 100,020명<br/>
    • 환자 대기 시간: 7백만 명 선택 수술 대기<br/>
    • 규제 복잡성: Brexit 이후 별도 프레임워크<br/>
    • 기술 채용 장벽: 레거시 시스템, 자금 제약<br/><br/>

    <b>전략적 추천</b><br/>
    성공하는 조직은 다음에 초점을 맞춰야 합니다:<br/>
    1. 디지털 의료 기술에 투자 가속화<br/>
    2. 정신 건강 및 노인 요양 서비스 확대<br/>
    3. 민간 부문과의 협력 강화<br/>
    4. 의료 인력 양성 프로그램 확대<br/>
    5. 규제 준수 및 거버넌스 강화<br/>
    6. 건강 불평등 해소에 주력<br/><br/>

    <b>결론</b><br/>
    영국 의료 산업은 변혁적인 기간에 있습니다. 적절한 투자, 전략적 파트너십,
    기술 혁신을 통해 조직은 상당한 성장과 영향력을 실현할 수 있습니다.
    서비스 격차, 인구 구조 변화, 기술 기회는 장기적이고 지속 가능한 비즈니스 기회를 제시합니다.
    """

    content.append(Paragraph(conclusion_text, body_style))

    content.append(Spacer(1, 0.3*inch))

    # Footer with document info
    content.append(PageBreak())

    content.append(Paragraph("부록 B: 데이터 출처 및 참고문헌", heading1_style))

    sources_text = """
    <b>주요 데이터 출처</b><br/>
    1. 영국 국가통계청(ONS) - 보건 계정, 지출 통계<br/>
    2. NHS Digital / NHS England - 인력 통계, 재무 데이터<br/>
    3. 하원 도서관 - NHS 자금 분석<br/>
    4. Statista - 의료 지출 추이<br/>
    5. 시장 조사 보고서 - DataMint Intelligence, Persistence Market Research<br/>
    6. 의료 규제 기관 - CQC, NICE, GMC, NMC, MHRA, PSA<br/><br/>

    <b>참고 자료</b><br/>
    • UK Healthcare Industry Outlook 2022-2026, ReportLinker<br/>
    • UK Healthcare Market Size & Trends 2026, ZipDo & Grand View Research<br/>
    • NHS Digital Transformation: A Reference Guide, NHS Confederation<br/>
    • UK Private Healthcare Market 2025-2033, Custom Market Insights<br/>
    • UK Digital Health Market Size & Forecast, Mordor Intelligence<br/>
    • Healthcare Professional Regulators Report 2024-2025, PSA<br/>
    • Care Quality Commission State of Care 2024-25<br/>
    • UK Medicines & Medical Device Regulation, MHRA<br/>
    • UK GDPR Healthcare Guidance, Information Commissioner's Office<br/><br/>

    <b>보고서 정보</b><br/>
    • 준비일: 2026년 1월 23일<br/>
    • 연구 범위: 2023-2026년<br/>
    • 지리적 초점: 영국 (주로 잉글랜드)<br/>
    • 데이터 품질: 2026년 1월 기준 최신 가용 데이터<br/>
    • 분류: 보건 정책 연구<br/>
    • 용도: 일반 참고, 정책 분석, 규제 준수 조사<br/><br/>

    <b>면책사항</b><br/>
    본 보고서는 공개 가용 출처와 공식 규제 기관 발행물을 기반으로 한
    종합적 분석을 제시합니다. 시장 예측과 기회 평가는 현재 추세와
    과거 데이터에 기반하고 있으며, 향후 실제 결과는 다를 수 있습니다.
    """

    content.append(Paragraph(sources_text, body_style))

    # Build PDF
    doc.build(content, onFirstPage=create_footer, onLaterPages=create_footer)

    print(f"PDF 보고서 생성 완료: {output_path}")
    return output_path


if __name__ == "__main__":
    try:
        pdf_path = create_uk_healthcare_report()
        print(f"✓ 성공적으로 생성됨: {pdf_path}")

        # Verify file exists
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"✓ 파일 크기: {file_size:,} bytes")
        else:
            print("✗ 파일이 생성되지 않았습니다")
    except Exception as e:
        print(f"✗ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
