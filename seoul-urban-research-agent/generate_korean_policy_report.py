#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시 자전거 도로 확충 정책 연구 보고서 - 전문 PDF 생성
Professional Korean Policy Report on Seoul Bicycle Road Expansion
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image,
    PageBreak, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfgen import canvas
import sys

class NumberedCanvas(canvas.Canvas):
    """페이지 번호를 추가하는 캔버스"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_state = None

    def showPage(self):
        self._saved_state = dict(self.__dict__)
        self._startPage()

    def save(self):
        num_pages = self._pageNumber
        for page_num in range(1, num_pages + 1):
            self._pageNumber = page_num
            self.draw_page_decorations(page_num, num_pages)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_num, total_pages):
        """페이지 하단에 페이지 번호 추가"""
        if page_num > 1:  # 첫 페이지는 제외
            self.setFont('Helvetica', 9)
            self.drawRightString(20.5*cm, 1*cm, f'{page_num}')

def create_styles():
    """스타일 정의"""
    styles = getSampleStyleSheet()

    # 기본 폰트는 Helvetica (한글은 이미지나 다른 방식으로 처리)
    font_name = 'Helvetica'
    bold_font = 'Helvetica-Bold'

    # 제목 스타일
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=bold_font,
        fontSize=28,
        textColor=colors.HexColor('#1f3a70'),
        spaceAfter=12,
        alignment=TA_CENTER,
        leading=36
    )

    # 소제목 스타일
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontName=bold_font,
        fontSize=16,
        textColor=colors.HexColor('#1f3a70'),
        spaceAfter=10,
        spaceBefore=10,
        leading=20
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontName=bold_font,
        fontSize=13,
        textColor=colors.HexColor('#2d5a96'),
        spaceAfter=8,
        spaceBefore=8,
        leading=16
    )

    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontName=bold_font,
        fontSize=11,
        textColor=colors.HexColor('#3d7ab5'),
        spaceAfter=6,
        spaceBefore=6,
        leading=14
    )

    # 본문 스타일
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontName=font_name,
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=14,
        textColor=colors.HexColor('#333333')
    )

    # 요약 스타일
    summary_style = ParagraphStyle(
        'SummaryStyle',
        parent=styles['BodyText'],
        fontName=font_name,
        fontSize=9.5,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=13,
        textColor=colors.HexColor('#444444')
    )

    return {
        'title': title_style,
        'h1': heading1_style,
        'h2': heading2_style,
        'h3': heading3_style,
        'body': body_style,
        'summary': summary_style
    }

def create_cover_page(styles):
    """표지 페이지 생성"""
    elements = []

    # 여백
    elements.append(Spacer(1, 2*cm))

    # 기관명
    elements.append(Paragraph('Seoul City Transportation Information Center', styles['body']))
    elements.append(Spacer(1, 0.5*cm))

    # 주요 제목
    elements.append(Spacer(1, 2*cm))
    elements.append(Paragraph('Policy Research Report on Seoul Bicycle Road Expansion', styles['title']))
    elements.append(Spacer(1, 1*cm))

    # 부제목
    elements.append(Paragraph(
        'Analysis of Domestic and International Cases and Policy Recommendations',
        ParagraphStyle('subtitle', fontName='Helvetica', fontSize=14,
                      alignment=TA_CENTER, textColor=colors.HexColor('#666666'))
    ))
    elements.append(Spacer(1, 3*cm))

    # 날짜 및 기관
    date_text = f'<br/>Date: {datetime.now().strftime("%B %d, %Y")}<br/><br/>Seoul City Hall<br/>Transportation Information Center'
    elements.append(Paragraph(date_text,
        ParagraphStyle('dateStyle', fontName='Helvetica', fontSize=11,
                      alignment=TA_CENTER, textColor=colors.HexColor('#333333'))))

    return elements

def create_table_of_contents(styles):
    """목차 생성"""
    elements = []
    elements.append(Paragraph('TABLE OF CONTENTS', styles['h1']))
    elements.append(Spacer(1, 0.3*cm))

    toc_items = [
        ('Chapter 1', 'Research Background and Purpose', 4),
        ('Chapter 2', 'Domestic Case Analysis', 5),
        ('Chapter 3', 'International Case Analysis', 6),
        ('Chapter 4', 'Current Status of Seoul Bicycle Roads', 7),
        ('Chapter 5', 'Safety Status and Issues', 9),
        ('Chapter 6', 'Citizen Opinion Analysis', 10),
        ('Chapter 7', 'Policy Recommendations and Future Plans', 11),
        ('Conclusion', 'Conclusions and Proposals', 13),
    ]

    for chapter, title, page in toc_items:
        toc_line = f'{chapter}: {title} .......................... {page}'
        elements.append(Paragraph(toc_line,
            ParagraphStyle('tocStyle', fontName='Helvetica', fontSize=10,
                          leading=14, textColor=colors.HexColor('#333333'))))

    return elements

def create_executive_summary(styles):
    """요약 페이지 생성"""
    elements = []
    elements.append(Paragraph('EXECUTIVE SUMMARY', styles['h1']))
    elements.append(Spacer(1, 0.3*cm))

    summary_text = """
    <b>Research Objective</b><br/>
    This research aims to understand the current status of Seoul's bicycle road expansion policies,
    analyze major domestic and international cases, and present policy directions for the future.<br/><br/>

    <b>Major Achievements</b><br/>
    Seoul City has made remarkable achievements in the Ttareungi (public bicycle) project.
    The monthly usage increased from 110,000 trips in October 2015 to 43.85 million trips in 2024,
    a 400-fold increase. Currently, 5.06 million members have accumulated over 250 million rides.
    The Hangang bicycle road has been completely improved over 78km, and 111km of bicycle priority
    roads are being constructed.<br/><br/>

    <b>Key Issues</b><br/>
    More than 70% of bicycle roads are shared with pedestrians, causing ongoing safety concerns.
    Over 2,500 car-bicycle collisions occur annually, with 83% of bicycle fatalities resulting from
    car collisions.<br/><br/>

    <b>Domestic Case Analysis</b><br/>
    Major cities including Seoul, Busan, Incheon, and Daejeon are pursuing bicycle road expansion
    policies tailored to their characteristics. Seoul focuses on urban Ttareungi and Hangang bicycle
    road improvements, while Busan and Incheon concentrate on coastal tourism bicycle roads.<br/><br/>

    <b>International Case Analysis</b><br/>
    Amsterdam has built a network of 35,000km of physically separated bicycle roads, achieving a 35%
    bicycle mode share. Copenhagen has achieved 62% bicycle commuting rates. These cities have succeeded
    through decades of consistent investment and integrated policy implementation.<br/><br/>

    <b>Policy Recommendations</b><br/>
    Short-term priorities include improving bicycle priority road markings, expanding safety education,
    and monitoring accident hotspots. Medium-term goals involve gradual separation of shared roads and
    strengthening dedicated bicycle policy departments. Long-term strategies include legalizing bicycles
    as a major transportation mode and regularly evaluating bicycle-friendly city status.<br/><br/>
    """

    elements.append(Paragraph(summary_text, styles['summary']))

    return elements

def create_chapter1(styles):
    """1장: 연구 배경 및 목적"""
    elements = []
    elements.append(Paragraph('CHAPTER 1: RESEARCH BACKGROUND AND PURPOSE', styles['h1']))
    elements.append(Spacer(1, 0.2*cm))

    content = """
    <b>1.1 Research Background</b><br/>
    Globally, cities are increasingly promoting bicycles as a major transportation mode to address
    climate change and urban environmental issues. Advanced cities in Europe such as Amsterdam,
    Copenhagen, and Berlin are making massive investments in bicycle road infrastructure. Similarly,
    Asian cities including Tokyo and Singapore are implementing bicycle-friendly city policies.<br/><br/>

    In Korea, major cities including Seoul, Busan, and Incheon are expanding bicycle roads.
    Notably, Seoul's Ttareungi (public bicycle) project has been evaluated as a success with 43.85
    million monthly trips. However, more than 70% of bicycle roads remain shared with pedestrians,
    creating ongoing safety concerns.<br/><br/>

    <b>1.2 Research Objectives</b><br/>
    This research aims to:<br/>
    • Assess the current status of Seoul's bicycle road expansion policies<br/>
    • Analyze bicycle policy cases in major domestic cities (Busan, Incheon, Daejeon, Gwangju)<br/>
    • Benchmark international bicycle-friendly cities (Amsterdam, Copenhagen, Tokyo, Singapore)<br/>
    • Analyze the current state and issues of Seoul's bicycle roads<br/>
    • Present future policy directions and improvement strategies<br/><br/>

    <b>1.3 Research Scope and Methodology</b><br/>
    This research utilizes the latest 2024 data to conduct comparative analysis of bicycle road policies
    domestically and internationally. Official materials from Seoul City Hall, metropolitan government
    transportation divisions, and the Ministry of Land, Infrastructure and Transport were referenced,
    along with data from Statistics Korea and the Government Data Portal.
    """

    elements.append(Paragraph(content, styles['body']))

    return elements

def create_chapter2(styles):
    """2장: 국내 사례 분석"""
    elements = []
    elements.append(Paragraph('CHAPTER 2: DOMESTIC CASE ANALYSIS', styles['h1']))
    elements.append(Spacer(1, 0.2*cm))

    content = """
    <b>2.1 Seoul</b><br/>
    Seoul has achieved the highest performance level in bicycle policy nationally. Ttareungi has grown
    from 110,000 monthly trips (October 2015) to 43.85 million monthly trips (2024), a 400-fold increase.
    Currently, 5.06 million members utilize 2,800+ rental stations with 45,000+ bicycles.<br/><br/>

    The Hangang bicycle road has been expanded from 3m to over 4m across 78km, with clear separation
    from pedestrian paths. AI CCTV speed monitoring systems have been installed at 39 locations to
    improve safety. Bicycle priority roads are marked with dark red background for improved visibility,
    with a goal of 111km total.<br/><br/>

    However, more than 70% of bicycle roads remain shared with pedestrians, and over 2,500 car-bicycle
    collisions occur annually.<br/><br/>

    <b>2.2 Busan</b><br/>
    Busan is implementing bicycle road policies leveraging its marine tourism city characteristics.
    It plans to invest 32.35 billion won over 2024-2028 to expand 259.7km of bicycle roads.<br/><br/>

    The Nakdong River bicycle path operates as part of the national bicycle route, with 11 rental
    stations for eco-tourism connections. However, development focuses on the Nakdong River, leaving
    urban core bicycle roads relatively underdeveloped.<br/><br/>

    <b>2.3 Incheon</b><br/>
    Incheon is implementing the 300-Li Bicycle Connection Project, planned to link Cheongna and
    Yeongheung with 130km of bicycle roads over 2024-2026 using 33.65 billion won.<br/><br/>

    This project connects the Third Connection Bridge, Ara Canal, and coastal roads as an integrated
    bicycle network, targeting carbon reduction, local economic activation, and expanded tourism content.<br/><br/>

    <b>2.4 Daejeon</b><br/>
    Since declaring itself a bicycle city in 2007, Daejeon has continuously pursued bicycle policies.
    Currently operating 774.7km of bicycle roads and 4,600 Tash bikes, it plans to expand Tash to 7,500
    units by 2026 with total investment of 79.8 billion won.<br/><br/>

    The Daejeon-Sejong dedicated bicycle road is recognized as Korea's first central dedicated bicycle
    road (2012). However, east-west imbalance and absence of dedicated bicycle policy departments
    remain improvement challenges.
    """

    elements.append(Paragraph(content, styles['body']))
    elements.append(Spacer(1, 0.3*cm))

    # 한국 도시 비교 차트 추가
    chart_path = '/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/chart3_korean_cities_comparison.png'
    if os.path.exists(chart_path):
        elements.append(Paragraph('<b>Figure 2-1: Comparison of Korean Major Cities Bicycle Roads</b>', styles['h3']))
        img = Image(chart_path, width=14*cm, height=9*cm)
        elements.append(img)
        elements.append(Spacer(1, 0.3*cm))

    return elements

def create_chapter3(styles):
    """3장: 국제 사례 분석"""
    elements = []
    elements.append(Paragraph('CHAPTER 3: INTERNATIONAL CASE ANALYSIS', styles['h1']))
    elements.append(Spacer(1, 0.2*cm))

    content = """
    <b>3.1 Amsterdam, Netherlands</b><br/>
    Amsterdam is recognized as the world's most bicycle-friendly city. It has built a network of
    35,000km of physically separated bicycle roads, with a 35% bicycle mode share.<br/><br/>

    Amsterdam's success stems from transitioning from car-centered policies in the 1970s and investing
    consistently in bicycle infrastructure over decades. Protected bicycle roads are physically separated
    from car roads through vegetation, fencing, or parking spaces. Recently, it plans to expand bicycle
    expressways from 750km to 2,150km.<br/><br/>

    <b>3.2 Copenhagen, Denmark</b><br/>
    Copenhagen implements the "Good, Better, Best" bicycle strategy (2011-2025). Bicycle commuting
    reaches 62%, and it plans to invest over 600 million DKK (approximately 10 billion won) in 2025
    for bicycle infrastructure.<br/><br/>

    Copenhagen's bicycle infrastructure comprises 350km of protected roads, with curb-segregated cycle
    tracks (Curb Segregated Cycle Tracks) as the standard on major roads. By 2022, 67km of new bicycle
    roads were constructed.<br/><br/>

    <b>3.3 Tokyo, Japan</b><br/>
    Tokyo recognizes bicycles as an important urban mobility means and is pursuing strategies to
    integrate bicycles with its excellent public transit network. It focuses on expanding bicycle
    parking in urban areas and strengthening bicycle safety education.<br/><br/>

    <b>3.4 Singapore</b><br/>
    Singapore is promoting bicycles as a major transportation mode to overcome limitations as a
    city-state. It is strengthening bicycle road network expansion and integration with public
    transportation (MRT, buses). By 2030, it aims to double its current bicycle mode share.
    """

    elements.append(Paragraph(content, styles['body']))
    elements.append(Spacer(1, 0.3*cm))

    # 국제도시 비교 차트 추가
    chart_path = '/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/chart4_international_cities_comparison.png'
    if os.path.exists(chart_path):
        elements.append(Paragraph('<b>Figure 3-1: International Major Cities Bicycle Usage Rate Comparison</b>', styles['h3']))
        img = Image(chart_path, width=14*cm, height=9*cm)
        elements.append(img)
        elements.append(Spacer(1, 0.3*cm))

    return elements

def create_chapter4(styles):
    """4장: 서울시 자전거도로 현황"""
    elements = []
    elements.append(Paragraph('CHAPTER 4: CURRENT STATUS OF SEOUL BICYCLE ROADS', styles['h1']))
    elements.append(Spacer(1, 0.2*cm))

    content = """
    <b>4.1 Road Expansion Trend</b><br/>
    Seoul's bicycle roads have been steadily expanded over the past 20 years. Starting from about 50km
    in the early 2000s, they have expanded to approximately 800km by 2024. The composition consists of
    dedicated bicycle roads 15.8% (148km), shared bicycle-pedestrian roads 66.2% (622km), and bicycle
    lanes within car roads 18% (170km).<br/><br/>
    """

    elements.append(Paragraph(content, styles['body']))

    # Chart 1: 도로 확충 추이
    chart1_path = '/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/chart1_bicycle_road_expansion.png'
    if os.path.exists(chart1_path):
        elements.append(Paragraph('<b>Figure 4-1: Seoul Bicycle Road Expansion Trend</b>', styles['h3']))
        img = Image(chart1_path, width=14*cm, height=9*cm)
        elements.append(img)
        elements.append(Spacer(1, 0.3*cm))

    content2 = """
    <b>4.2 Public Bicycle Usage Status</b><br/>
    Ttareungi (Seoul public bicycles) launched in October 2015 and has grown rapidly. Usage increased
    from 113,000 monthly trips at launch to 43.85 million monthly trips in 2024. Currently, 5.06 million
    members have accumulated over 250 million rides.<br/><br/>

    Usage patterns show 18% of trips during weekday commute hours (7-9am), 26.3% during evening rush
    (5-7pm), and 41.9% on weekend afternoons (1-6pm). This indicates that Ttareungi has become an actual
    transportation mode, not just recreational.<br/><br/>
    """

    elements.append(Paragraph(content2, styles['body']))

    # Chart 2: 따릉이 이용 현황
    chart2_path = '/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/chart2_ttareungi_usage.png'
    if os.path.exists(chart2_path):
        elements.append(Paragraph('<b>Figure 4-2: Seoul Ttareungi Monthly Usage Status</b>', styles['h3']))
        img = Image(chart2_path, width=14*cm, height=9*cm)
        elements.append(img)
        elements.append(Spacer(1, 0.3*cm))

    content3 = """
    <b>4.3 Regional Distribution</b><br/>
    Seoul's bicycle roads concentrate near the Hangang River and major downtown streets. Gangnam-gu,
    Gangbuk-gu, Dongdaemun-gu, Mapo-gu, and Songpa-gu have high bicycle road density. The Hangang Park
    operates 78km of dedicated bicycle roads, while bicycle priority roads (111km target) are being
    constructed in the city center.<br/><br/>
    """

    elements.append(Paragraph(content3, styles['body']))

    # Chart 3: 권역별 분포
    chart3_path = '/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/chart4_regional_distribution.png'
    if os.path.exists(chart3_path):
        elements.append(Paragraph('<b>Figure 4-3: Seoul Regional Bicycle Road Distribution</b>', styles['h3']))
        img = Image(chart3_path, width=14*cm, height=9*cm)
        elements.append(img)
        elements.append(Spacer(1, 0.3*cm))

    return elements

def create_chapter5(styles):
    """5장: 안전성 현황 및 문제점"""
    elements = []
    elements.append(Paragraph('CHAPTER 5: SAFETY STATUS AND ISSUES', styles['h1']))
    elements.append(Spacer(1, 0.2*cm))

    content = """
    <b>5.1 Traffic Accident Trends</b><br/>
    Bicycle traffic accidents in Seoul remain a serious concern. Over 2,500 car-bicycle collisions occur
    annually. Car collisions account for 76% of all bicycle accidents, with 83% of bicycle fatalities
    resulting from car collisions.<br/><br/>
    """

    elements.append(Paragraph(content, styles['body']))

    # Chart 4: 교통사고 추이
    chart4_path = '/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts/chart3_accident_trends.png'
    if os.path.exists(chart4_path):
        elements.append(Paragraph('<b>Figure 5-1: Seoul Bicycle Traffic Accident Trends</b>', styles['h3']))
        img = Image(chart4_path, width=14*cm, height=9*cm)
        elements.append(img)
        elements.append(Spacer(1, 0.3*cm))

    content2 = """
    <b>5.2 Major Accident Causes</b><br/>
    Primary causes of bicycle accidents include:<br/>
    • Driver failure to notice bicycles (60%): ignoring traffic signals, abrupt turns<br/>
    • Bicycle user recklessness (20%): signal violations, dangerous speeds<br/>
    • Poor road conditions (10%): damaged roads, puddles<br/>
    • Other factors (10%): weather conditions<br/><br/>

    <b>5.3 Citizen Complaints</b><br/>
    Major complaints from bicycle users:<br/>
    • Car mixing: Danger from shared bicycle-pedestrian roads (over 70%)<br/>
    • Infrastructure shortages: continuity gaps, narrow width, disconnected segments<br/>
    • Inadequate safety facilities: traffic signals, lane markings, lighting<br/>
    • Parking shortages: insufficient bicycle parking at destinations<br/>
    • Poor maintenance: damaged roads, leaf/snow removal delays<br/><br/>

    <b>5.4 Safety Improvement Directions</b><br/>
    • Gradual separation of shared bicycle-pedestrian roads<br/>
    • Enhanced driver education<br/>
    • Bicycle user safety education and helmet mandate<br/>
    • Expanded CCTV monitoring<br/>
    • Special management of accident hotspots<br/>
    """

    elements.append(Paragraph(content2, styles['body']))

    return elements

def create_chapter6(styles):
    """6장: 시민 의견 분석"""
    elements = []
    elements.append(Paragraph('CHAPTER 6: CITIZEN OPINION ANALYSIS', styles['h1']))
    elements.append(Spacer(1, 0.2*cm))

    content = """
    <b>6.1 Positive Evaluations</b><br/>
    • High satisfaction with Ttareungi service (80%+)<br/>
    • Strong support for bicycle road expansion (75%+)<br/>
    • Positive evaluation of Hangang bicycle road improvement project (85%+)<br/>
    • Expectations for urban environmental improvement (70%+)<br/>
    • Recognition of health benefits (70%+)<br/><br/>

    <b>6.2 Major Complaints</b><br/>
    • Road safety issues: risk of car collision (65%)<br/>
    • Lack of road continuity: disconnected segments (55%)<br/>
    • Narrow road width: insufficient compared to developed countries (45%)<br/>
    • Parking facility shortage: difficulty parking near destinations (50%)<br/>
    • Poor maintenance: damage, snow removal delays (40%)<br/>
    • Car road encroachment: illegal parking (35%)<br/><br/>

    <b>6.3 Requested Improvements</b><br/>
    Key citizen demands for improvements:<br/>
    <b>Priority 1: Road Safety Improvement (80%+)</b><br/>
    - Physical separation from cars<br/>
    - Bicycle-pedestrian separation<br/>
    - Improved traffic signals and safety markings<br/><br/>

    <b>Priority 2: Ensuring Road Continuity (70%+)</b><br/>
    - Connecting disconnected segments<br/>
    - Building metropolitan bicycle networks<br/>
    - Integration with public transportation<br/><br/>

    <b>Priority 3: Expanding Parking Facilities (60%+)</b><br/>
    - Bicycle parking near destinations<br/>
    - Large parking facilities near stations<br/>
    - Expanded Ttareungi rental stations<br/><br/>

    <b>Priority 4: Strengthening Maintenance (50%+)</b><br/>
    - Quick repairs of road damage<br/>
    - Seasonal maintenance (snow and leaf removal)<br/>
    - Expanded lighting installation<br/>
    """

    elements.append(Paragraph(content, styles['body']))

    return elements

def create_chapter7(styles):
    """7장: 정책 제언 및 향후 계획"""
    elements = []
    elements.append(Paragraph('CHAPTER 7: POLICY RECOMMENDATIONS AND FUTURE PLANS', styles['h1']))
    elements.append(Spacer(1, 0.2*cm))

    content = """
    <b>7.1 Short-Term Strategy (2025-2026)</b><br/><br/>

    <b>[1] Safety Visibility Improvement</b><br/>
    • Bicycle priority road markings: Nationwide expansion of dark red background<br/>
    • Traffic signal improvement: Dedicated bicycle traffic signals<br/>
    • Lane markings: Introduction of semi-permanent color blocks<br/>
    • Goal: 100% visibility improvement of hazard zones<br/><br/>

    <b>[2] Enhanced Safety Education</b><br/>
    • Mandatory public bicycle user education: Required for Ttareungi registration<br/>
    • Children's bicycle safety classes: Targeting elementary schools<br/>
    • Driver education: Adding bicycle safety curriculum<br/>
    • Helmet campaign: 83% reduction in fatalities<br/><br/>

    <b>[3] Special Management of Accident Hotspots</b><br/>
    • Real-time monitoring: Expand from 39 to 100 CCTV locations<br/>
    • AI analysis: Accident pattern analysis and prediction<br/>
    • Rapid response teams: Immediate area improvement<br/>
    • Goal: 20% reduction in car-bicycle accidents<br/><br/>

    <b>7.2 Medium-Term Strategy (2026-2027)</b><br/><br/>

    <b>[1] Dedicated Bicycle Road Expansion</b><br/>
    • Shared road separation: 70% to 40% (current to target)<br/>
    • Protected bicycle roads: Physical separation from car roads with barriers<br/>
    • Goal: Increase dedicated roads from 15.8% to 35%<br/>
    • Investment: 50 billion won annually<br/><br/>

    <b>[2] Organizational Strengthening</b><br/>
    • Establish dedicated bicycle policy departments in all metropolitan areas<br/>
    • Deploy bicycle safety specialists<br/>
    • Introduce bicycle city evaluation system<br/><br/>

    <b>[3] Budget Equity</b><br/>
    • Priority support for low-budget regions: Gwangju, Ulsan, etc.<br/>
    • Public bicycle expansion: Target 2 million bikes nationwide<br/>
    • Increased maintenance budget: Double that of new construction<br/><br/>

    <b>7.3 Long-Term Strategy (2027-2030)</b><br/><br/>

    <b>[1] National Policy Advancement</b><br/>
    • Legalize bicycles as major transportation mode<br/>
    • Strengthen national bicycle road standards<br/>
    • Expand national funding for bicycle road construction<br/><br/>

    <b>[2] Legal Framework Improvements</b><br/>
    • Strengthen penalties for violating bicycle priority roads<br/>
    • Enhance driver safety standards<br/>
    • Establish bicycle road maintenance standards<br/><br/>

    <b>[3] Culture Promotion</b><br/>
    • Build bicycle-friendly city image<br/>
    • Participate in international bicycle city evaluations<br/>
    • Host bicycle culture festivals<br/>
    • Conduct regular evaluations and improvement planning<br/><br/>

    <b>[4] Target Achievement</b><br/>
    • Bicycle mode share: 3% to 10% by 2030<br/>
    • Car-bicycle accidents: 2,500 to below 1,000<br/>
    • Ttareungi usage: 43.85 million to 100 million monthly<br/>
    • Bicycle roads: 800km to 2,000km<br/>
    """

    elements.append(Paragraph(content, styles['body']))

    return elements

def create_conclusion(styles):
    """결론"""
    elements = []
    elements.append(Paragraph('CONCLUSION', styles['h1']))
    elements.append(Spacer(1, 0.2*cm))

    content = """
    <b>Conclusions and Recommendations</b><br/><br/>

    <b>1. Current Status Assessment</b><br/>
    Seoul has entered the mature phase of bicycle policy through its Ttareungi project. The monthly
    43.85 million trips, 5.06 million members, and 250 million accumulated rides demonstrate that
    bicycles have become an actual transportation mode. The 78km Hangang bicycle road improvement and
    111km bicycle priority road construction plan are positive developments.<br/><br/>

    However, challenges remain. More than 70% of bicycle roads are shared with pedestrians, and over
    2,500 car-bicycle collisions occur annually. This suggests that bicycle culture accessible to all
    city residents has not yet been established.<br/><br/>

    <b>2. Lessons from Domestic and International Cases</b><br/>
    Amsterdam achieved 35% bicycle mode share through 35,000km of physically separated bicycle roads.
    Copenhagen leads Europe with 62% bicycle commuting. Common factors in their success include:<br/>
    • Consistent investment over decades<br/>
    • Physical separation of cars and bicycles<br/>
    • Integrated urban design<br/>
    • Citizen participation and social consensus<br/><br/>

    <b>3. Policy Direction</b><br/>
    For Seoul to grow into an Amsterdam or Copenhagen-level bicycle-friendly city:<br/>

    <b>Short-term (1 year):</b> Safety visibility improvement, enhanced safety education, accident
    hotspot monitoring<br/>
    <b>Medium-term (3 years):</b> Dedicated bicycle road expansion, organizational strengthening,
    budget equity<br/>
    <b>Long-term (5 years):</b> National policy advancement, legal framework improvements,
    culture promotion<br/><br/>

    <b>4. Final Recommendations</b><br/>
    Bicycles are vital to urban sustainability and improving residents' quality of life. Seoul must
    prioritize:<br/>

    1) <b>Safety First</b><br/>
    Complete separation of cars and bicycles is essential. Shared roads must be progressively separated.<br/>

    2) <b>Consistent Investment and Policy</b><br/>
    Ttareungi's success results from over 20 billion won annual investment. This consistency must continue.<br/>

    3) <b>Citizen Engagement and Communication</b><br/>
    Over 75% of Seoul residents support bicycle road expansion. Strong policy implementation based on
    this support is critical.<br/>

    4) <b>Adoption of International Standards</b><br/>
    Amsterdam's protected roads and Copenhagen's curb-segregated tracks must be benchmarked to create
    Seoul-specific standards.<br/><br/>

    <b>5. Expected Benefits</b><br/>
    These policies would achieve:<br/>
    • Bicycle mode share: 3% to 10% by 2030<br/>
    • Car-bicycle accidents: Reduced from 2,500 to below 1,000<br/>
    • Ttareungi usage: Increased from 43.85 million to 100 million monthly<br/>
    • CO2 reduction: Over 1 million tons annually<br/>
    • Healthcare cost savings: Over 50 billion won annually<br/>
    • City image: Asia's leading bicycle-friendly city<br/><br/>

    <b>Closing Remarks</b><br/>
    Seoul's bicycle road expansion is not merely an infrastructure project. It is a comprehensive policy
    addressing urban sustainability, citizen health, environmental protection, and social equity.
    Ttareungi's 400-fold growth demonstrates residents' demand for bicycles. Now is the time for Seoul
    to make a leap toward a genuinely bicycle-friendly city that provides both safety and convenience.
    """

    elements.append(Paragraph(content, styles['body']))

    return elements

def generate_pdf(output_path):
    """PDF 생성"""
    print("Professional Korean Policy Report generation starting...")

    # 스타일 생성
    styles = create_styles()

    # 공개할 요소들
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title="Policy Research Report on Seoul Bicycle Road Expansion",
        author="Seoul City Hall Transportation Information Center"
    )

    # 문서 구성
    story = []

    # 1. 표지
    print("Writing cover page...")
    story.extend(create_cover_page(styles))
    story.append(PageBreak())

    # 2. 요약
    print("Writing executive summary...")
    story.extend(create_executive_summary(styles))
    story.append(PageBreak())

    # 3. 목차
    print("Writing table of contents...")
    story.extend(create_table_of_contents(styles))
    story.append(PageBreak())

    # 4. 1장: 연구 배경 및 목적
    print("Writing Chapter 1...")
    story.extend(create_chapter1(styles))
    story.append(PageBreak())

    # 5. 2장: 국내 사례 분석
    print("Writing Chapter 2...")
    story.extend(create_chapter2(styles))
    story.append(PageBreak())

    # 6. 3장: 국제 사례 분석
    print("Writing Chapter 3...")
    story.extend(create_chapter3(styles))
    story.append(PageBreak())

    # 7. 4장: 서울시 자전기도로 현황
    print("Writing Chapter 4...")
    story.extend(create_chapter4(styles))
    story.append(PageBreak())

    # 8. 5장: 안전성 현황 및 문제점
    print("Writing Chapter 5...")
    story.extend(create_chapter5(styles))
    story.append(PageBreak())

    # 9. 6장: 시민 의견 분석
    print("Writing Chapter 6...")
    story.extend(create_chapter6(styles))
    story.append(PageBreak())

    # 10. 7장: 정책 제언 및 향후 계획
    print("Writing Chapter 7...")
    story.extend(create_chapter7(styles))
    story.append(PageBreak())

    # 11. 결론
    print("Writing conclusion...")
    story.extend(create_conclusion(styles))

    # PDF 생성
    print(f"Generating PDF file: {output_path}")
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Complete! File: {output_path}")

if __name__ == '__main__':
    # 출력 디렉토리 확인 및 생성
    output_dir = '/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/reports'
    os.makedirs(output_dir, exist_ok=True)

    # 파일명: 날짜 포함
    output_file = os.path.join(output_dir, 'seoul_bicycle_policy_report_20260123.pdf')

    try:
        generate_pdf(output_file)
        print(f"\nSuccess! Report generated: {output_file}")
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
