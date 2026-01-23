"""Test Korean PDF generation with reportlab"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 한글 폰트 등록 시도 (macOS)
font_name = 'Helvetica'  # 기본값
try:
    # macOS 시스템 폰트 경로
    font_paths = [
        '/System/Library/Fonts/Supplemental/AppleGothic.ttf',
        '/Library/Fonts/AppleGothic.ttf',
        '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont('KoreanFont', path))
            font_name = 'KoreanFont'
            print(f"✓ 한글 폰트 등록 성공: {path}")
            break
    else:
        print("⚠ 한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
except Exception as e:
    print(f"⚠ 폰트 등록 중 오류: {e}")

# 출력 디렉토리 생성
os.makedirs('test_output', exist_ok=True)

# PDF 문서 생성
pdf_path = f"test_output/korean_pdf_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm
)

# 스타일 정의
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name='KoreanTitle',
    fontName=font_name,
    fontSize=18,
    alignment=TA_CENTER,
    spaceAfter=12,
    textColor=colors.HexColor('#1a1a1a')
))
styles.add(ParagraphStyle(
    name='KoreanHeading',
    fontName=font_name,
    fontSize=14,
    spaceAfter=10,
    textColor=colors.HexColor('#2c3e50')
))
styles.add(ParagraphStyle(
    name='KoreanBody',
    fontName=font_name,
    fontSize=10,
    alignment=TA_JUSTIFY,
    leading=14,
    spaceAfter=8
))

# 문서 내용 구성
story = []

# 제목
story.append(Paragraph("서울시 자전거 도로 확충 정책 브리프", styles['KoreanTitle']))
story.append(Paragraph(f"발행일: {datetime.now().strftime('%Y년 %m월 %d일')}", styles['KoreanBody']))
story.append(Spacer(1, 0.5*cm))

# 요약
story.append(Paragraph("요약", styles['KoreanHeading']))
story.append(Paragraph(
    "서울시 자전거 도로 확충 정책에 대한 연구 결과를 요약합니다. "
    "국내외 사례 분석, 통계 데이터, 시민 의견을 종합하여 정책 제안을 도출하였습니다.",
    styles['KoreanBody']
))
story.append(Spacer(1, 0.3*cm))

# 주요 발견
story.append(Paragraph("주요 발견", styles['KoreanHeading']))
story.append(Paragraph("• 서울시 자전거 도로 총 길이: 1,230.5km (2024년)", styles['KoreanBody']))
story.append(Paragraph("• 일평균 이용 건수: 421,350건 (2024년)", styles['KoreanBody']))
story.append(Paragraph("• 시민 찬성 비율: 68.5%", styles['KoreanBody']))
story.append(Spacer(1, 0.3*cm))

# 정책 제안
story.append(Paragraph("정책 제안", styles['KoreanHeading']))
story.append(Paragraph(
    "1. 안전성 강화: 분리형 자전거 도로 확대 (2027년까지 300km 추가)",
    styles['KoreanBody']
))
story.append(Paragraph(
    "2. 대중교통 연계: 지하철역 주변 자전거 주차장 확충",
    styles['KoreanBody']
))
story.append(Paragraph(
    "3. 시민 참여: 자전거 이용자 의견 수렴 정기화",
    styles['KoreanBody']
))
story.append(Spacer(1, 0.3*cm))

# 기대 효과
story.append(Paragraph("기대 효과", styles['KoreanHeading']))
story.append(Paragraph(
    "• 탄소 배출 감소: 연간 135,000톤 CO2 감축 예상",
    styles['KoreanBody']
))
story.append(Paragraph(
    "• 교통 혼잡 완화: 자전거 이용률 20% 증가 목표",
    styles['KoreanBody']
))

# PDF 생성
try:
    doc.build(story)
    print(f"\n✓ PDF 생성 성공!")
    print(f"  파일 위치: {os.path.abspath(pdf_path)}")
    print(f"  파일 크기: {os.path.getsize(pdf_path):,} bytes")
    print("\n한글 PDF 생성 테스트 완료!")
except Exception as e:
    print(f"\n✗ PDF 생성 실패: {e}")
    raise
