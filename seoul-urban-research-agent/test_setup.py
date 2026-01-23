"""
Seoul Urban Research Agent - 간단한 테스트 스크립트

이 스크립트는 에이전트의 기본 기능을 테스트합니다.
실제 API 호출 없이 구조만 검증합니다.
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from seoul_research_agent.agent import load_prompt

def test_prompts():
    """모든 프롬프트 파일이 올바르게 로드되는지 테스트"""
    print("=" * 60)
    print("Seoul Urban Research Agent - 프롬프트 테스트")
    print("=" * 60)
    
    prompts = [
        "lead_agent.txt",
        "domestic_researcher.txt",
        "international_researcher.txt",
        "statistics_researcher.txt",
        "citizen_voice_researcher.txt",
        "urban_data_analyst.txt",
        "policy_writer.txt"
    ]
    
    results = []
    for prompt_file in prompts:
        try:
            content = load_prompt(prompt_file)
            status = "✓"
            size = len(content)
            preview = content[:100].replace('\n', ' ')
            results.append((prompt_file, status, size, preview))
            print(f"\n{status} {prompt_file}")
            print(f"  크기: {size:,} bytes")
            print(f"  미리보기: {preview}...")
        except Exception as e:
            status = "✗"
            results.append((prompt_file, status, 0, str(e)))
            print(f"\n{status} {prompt_file}")
            print(f"  오류: {e}")
    
    print("\n" + "=" * 60)
    print("테스트 요약")
    print("=" * 60)
    
    success_count = sum(1 for _, status, _, _ in results if status == "✓")
    total_count = len(results)
    
    print(f"\n성공: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("\n✓ 모든 프롬프트 파일이 정상적으로 로드되었습니다!")
        return True
    else:
        print("\n✗ 일부 프롬프트 파일 로드에 실패했습니다.")
        return False

def test_directory_structure():
    """필요한 디렉토리 구조 확인"""
    print("\n" + "=" * 60)
    print("디렉토리 구조 확인")
    print("=" * 60)
    
    required_dirs = [
        "seoul_research_agent",
        "seoul_research_agent/prompts",
        "seoul_research_agent/utils"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        exists = full_path.exists()
        status = "✓" if exists else "✗"
        print(f"\n{status} {dir_path}")
        if exists:
            items = list(full_path.iterdir())
            print(f"  파일 수: {len(items)}")
        else:
            all_exist = False
    
    return all_exist

def test_dependencies():
    """필요한 패키지가 설치되어 있는지 확인"""
    print("\n" + "=" * 60)
    print("의존성 확인")
    print("=" * 60)
    
    packages = [
        ("claude_agent_sdk", "Claude Agent SDK"),
        ("reportlab", "ReportLab (PDF 생성)"),
        ("matplotlib", "Matplotlib (차트 생성)"),
        ("folium", "Folium (지도 시각화)")
    ]
    
    all_installed = True
    for package_name, display_name in packages:
        try:
            __import__(package_name)
            print(f"\n✓ {display_name}")
        except ImportError:
            print(f"\n✗ {display_name} - 설치 필요")
            all_installed = False
    
    return all_installed

if __name__ == "__main__":
    print("\n")
    
    # 테스트 실행
    dir_ok = test_directory_structure()
    deps_ok = test_dependencies()
    prompts_ok = test_prompts()
    
    # 최종 결과
    print("\n" + "=" * 60)
    print("최종 결과")
    print("=" * 60)
    
    if dir_ok and deps_ok and prompts_ok:
        print("\n✓ 모든 테스트 통과!")
        print("\n다음 단계:")
        print("1. .env 파일에 ANTHROPIC_API_KEY 설정")
        print("2. uv run python seoul_research_agent/agent.py 실행")
        print("3. 테스트 쿼리: '서울시 자전거 도로 확충 정책을 연구해주세요'")
        sys.exit(0)
    else:
        print("\n✗ 일부 테스트 실패")
        if not dir_ok:
            print("  - 디렉토리 구조 확인 필요")
        if not deps_ok:
            print("  - 의존성 설치 필요: uv sync")
        if not prompts_ok:
            print("  - 프롬프트 파일 확인 필요")
        sys.exit(1)
