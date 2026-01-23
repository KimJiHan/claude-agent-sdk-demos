#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
서울시 의료 인프라 분포 지도 생성
Seoul Healthcare Infrastructure Distribution Map
"""

try:
    import folium
    from folium import plugins
except ImportError:
    print("folium 모듈을 설치하세요: pip install folium")
    exit(1)

from pathlib import Path

OUTPUT_DIR = Path("/Users/jihan/project/claude-agent-sdk-demos/seoul-urban-research-agent/files/charts")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_seoul_healthcare_map():
    """서울 의료 인프라 분포 지도 생성"""
    print("생성 중: Seoul Healthcare Infrastructure Map")

    # 서울 중심 좌표
    seoul_center = [37.5665, 126.9780]

    # 지도 생성
    m = folium.Map(
        location=seoul_center,
        zoom_start=12,
        tiles='OpenStreetMap'
    )

    # 서울 주요 병원 데이터 (이름, 위도, 경도, 유형)
    hospitals_data = [
        # 서울아산병원
        {"name": "Seoul Asan Medical Center", "lat": 37.2761, "lng": 127.0060, "type": "General Hospital", "level": "국제 수준"},
        # 삼성서울병원
        {"name": "Samsung Medical Center", "lat": 37.4847, "lng": 127.0953, "type": "General Hospital", "level": "국제 수준"},
        # 서울대병원
        {"name": "Seoul National University Hospital", "lat": 37.4582, "lng": 127.0036, "type": "General Hospital", "level": "국제 수준"},
        # 세브란스병원
        {"name": "Severance Hospital", "lat": 37.5639, "lng": 126.9663, "type": "General Hospital", "level": "국제 수준"},
        # 권역응급의료센터들
        {"name": "Seoul Metropolitan Emergency Care Center", "lat": 37.5, "lng": 127.0, "type": "Emergency Center", "level": "권역"},
        # 지역별 주요 병원들 (샘플)
        {"name": "강남성심병원", "lat": 37.4979, "lng": 127.0276, "type": "Hospital", "level": "지역"},
        {"name": "고려대학교 안암병원", "lat": 37.5906, "lng": 127.0269, "type": "Hospital", "level": "지역"},
        {"name": "을지대학교 서울병원", "lat": 37.5398, "lng": 127.0857, "type": "Hospital", "level": "지역"},
        {"name": "경희대학교 서울동대문병원", "lat": 37.5707, "lng": 127.0108, "type": "Hospital", "level": "지역"},
        {"name": "국립중앙의료원", "lat": 37.5733, "lng": 127.0100, "type": "Public Hospital", "level": "공공"},
        {"name": "서울의료원", "lat": 37.5577, "lng": 127.0240, "type": "Public Hospital", "level": "공공"},
    ]

    # 마커 색상 지정
    color_map = {
        "General Hospital": "red",
        "Emergency Center": "darkred",
        "Hospital": "blue",
        "Public Hospital": "green"
    }

    icon_map = {
        "General Hospital": "hospital",
        "Emergency Center": "ambulance",
        "Hospital": "hospital",
        "Public Hospital": "hospital"
    }

    # 마커 추가
    for hospital in hospitals_data:
        folium.Marker(
            location=[hospital["lat"], hospital["lng"]],
            popup=f"""
            <b>{hospital['name']}</b><br>
            Type: {hospital['type']}<br>
            Level: {hospital['level']}
            """,
            tooltip=hospital['name'],
            icon=folium.Icon(color=color_map[hospital['type']], icon='hospital')
        ).add_to(m)

    # 범례 추가
    legend_html = '''
    <div style="position: fixed;
     bottom: 50px; left: 50px; width: 220px; height: auto; background-color: white;
     border:2px solid grey; z-index:9999; font-size:14px; padding: 10px">
     <p style="margin-top:0"><b>Healthcare Infrastructure Legend</b></p>
     <p><i class="fa fa-map-marker fa-2x" style="color:red"></i> General Hospital (International Level)</p>
     <p><i class="fa fa-map-marker fa-2x" style="color:darkred"></i> Emergency Center</p>
     <p><i class="fa fa-map-marker fa-2x" style="color:blue"></i> Hospital (Regional)</p>
     <p><i class="fa fa-map-marker fa-2x" style="color:green"></i> Public Hospital</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # 지도 저장
    output_path = OUTPUT_DIR / 'seoul_healthcare_infrastructure_map.html'
    m.save(str(output_path))
    print(f"✓ seoul_healthcare_infrastructure_map.html 저장됨 ({output_path})")
    return str(output_path)


def create_district_healthcare_heatmap():
    """자치구별 의료 인프라 밀도 히트맵"""
    print("생성 중: District Healthcare Density Heatmap")

    seoul_center = [37.5665, 126.9780]

    # 지도 생성
    m = folium.Map(
        location=seoul_center,
        zoom_start=11,
        tiles='CartoDB positron'
    )

    # 자치구별 의료기관 밀도 데이터 (추정치)
    # 좌표: 자치구 중심, 값: 의료기관 밀도 (병원+의원+약국 수의 상대적 비율)
    district_data = [
        {"name": "강남구", "lat": 37.4979, "lng": 127.0276, "density": 450, "institutions": 980},
        {"name": "서초구", "lat": 37.4830, "lng": 127.0323, "density": 380, "institutions": 850},
        {"name": "강동구", "lat": 37.5303, "lng": 127.1233, "density": 280, "institutions": 620},
        {"name": "강북구", "lat": 37.6398, "lng": 127.0056, "density": 200, "institutions": 440},
        {"name": "강서구", "lat": 37.5510, "lng": 126.8312, "density": 220, "institutions": 480},
        {"name": "관악구", "lat": 37.4816, "lng": 126.9535, "density": 240, "institutions": 530},
        {"name": "광진구", "lat": 37.5383, "lng": 127.0879, "density": 250, "institutions": 550},
        {"name": "구로구", "lat": 37.4954, "lng": 126.8865, "density": 180, "institutions": 400},
        {"name": "금천구", "lat": 37.4571, "lng": 126.8956, "density": 160, "institutions": 350},
        {"name": "노원구", "lat": 37.6540, "lng": 127.0569, "density": 210, "institutions": 460},
        {"name": "도봉구", "lat": 37.6687, "lng": 127.0305, "density": 170, "institutions": 370},
        {"name": "동대문구", "lat": 37.5707, "lng": 127.0108, "density": 220, "institutions": 480},
        {"name": "동작구", "lat": 37.5126, "lng": 126.9398, "density": 280, "institutions": 610},
        {"name": "마포구", "lat": 37.5639, "lng": 126.9070, "density": 290, "institutions": 640},
        {"name": "서대문구", "lat": 37.5795, "lng": 126.9369, "density": 310, "institutions": 680},
        {"name": "서초구", "lat": 37.4830, "lng": 127.0323, "density": 380, "institutions": 850},
        {"name": "성동구", "lat": 37.5454, "lng": 127.0370, "density": 240, "institutions": 530},
        {"name": "성북구", "lat": 37.5894, "lng": 127.0176, "density": 260, "institutions": 570},
        {"name": "송파구", "lat": 37.5145, "lng": 127.1069, "density": 350, "institutions": 770},
        {"name": "양천구", "lat": 37.5170, "lng": 126.8658, "density": 200, "institutions": 440},
        {"name": "영등포구", "lat": 37.5272, "lng": 126.8968, "density": 230, "institutions": 500},
        {"name": "용산구", "lat": 37.5326, "lng": 126.9941, "density": 270, "institutions": 590},
        {"name": "은평구", "lat": 37.6190, "lng": 126.9238, "density": 190, "institutions": 420},
        {"name": "종로구", "lat": 37.5725, "lng": 126.9895, "density": 340, "institutions": 750},
        {"name": "중구", "lat": 37.5640, "lng": 126.9972, "density": 330, "institutions": 720},
    ]

    # 히트맵 데이터 준비
    heat_data = [[d["lat"], d["lng"], d["density"]] for d in district_data]

    # 히트맵 레이어 추가
    plugins.HeatMap(heat_data, radius=30, blur=25, max_zoom=13).add_to(m)

    # 각 자치구에 원형 마커 추가 (밀도 표시)
    for district in district_data:
        # 밀도에 따라 색상 결정
        if district["density"] > 350:
            color = "#FF0000"  # 빨강 (높음)
        elif district["density"] > 250:
            color = "#FF7F00"  # 주황 (중상)
        elif district["density"] > 150:
            color = "#FFFF00"  # 노랑 (중하)
        else:
            color = "#90EE90"  # 연두 (낮음)

        folium.CircleMarker(
            location=[district["lat"], district["lng"]],
            radius=8,
            popup=f"""
            <b>{district['name']}</b><br>
            Healthcare Institutions: {district['institutions']}<br>
            Density Index: {district['density']}
            """,
            tooltip=f"{district['name']} (Density: {district['density']})",
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.7,
            weight=2
        ).add_to(m)

    # 범례 추가
    legend_html = '''
    <div style="position: fixed;
     bottom: 50px; left: 50px; width: 250px; height: auto; background-color: white;
     border:2px solid grey; z-index:9999; font-size:12px; padding: 10px">
     <p style="margin-top:0"><b>Healthcare Density by District</b></p>
     <p><i class="fa fa-circle" style="color:#FF0000"></i> High (>350)</p>
     <p><i class="fa fa-circle" style="color:#FF7F00"></i> Medium-High (251-350)</p>
     <p><i class="fa fa-circle" style="color:#FFFF00"></i> Medium-Low (151-250)</p>
     <p><i class="fa fa-circle" style="color:#90EE90"></i> Low (≤150)</p>
     <hr>
     <p><i>Heat map shows density distribution</i></p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    output_path = OUTPUT_DIR / 'seoul_healthcare_density_by_district.html'
    m.save(str(output_path))
    print(f"✓ seoul_healthcare_density_by_district.html 저장됨")
    return str(output_path)


def main():
    """메인 실행 함수"""
    print("=" * 70)
    print("서울시 의료 인프라 지도 생성")
    print("Seoul Healthcare Infrastructure Map Generator")
    print("=" * 70)

    try:
        create_seoul_healthcare_map()
        create_district_healthcare_heatmap()

        print("\n" + "=" * 70)
        print("✓ 모든 지도 생성 완료!")
        print("=" * 70)
        print(f"\n지도 저장 위치: {OUTPUT_DIR}")
        print("\n생성된 지도:")
        print("  - seoul_healthcare_infrastructure_map.html")
        print("  - seoul_healthcare_density_by_district.html")

    except Exception as e:
        print(f"\n✗ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
