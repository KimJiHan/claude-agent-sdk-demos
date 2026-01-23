"""
Seoul Urban Research Agent - 자동 테스트 스크립트

간단한 테스트 쿼리를 자동으로 실행하여 에이전트 기능을 검증합니다.
"""

import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from seoul_research_agent.agent import load_prompt
from seoul_research_agent.utils.transcript import setup_session, TranscriptWriter
from seoul_research_agent.utils.subagent_tracker import SubagentTracker
from seoul_research_agent.utils.message_handler import process_assistant_message
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition, HookMatcher


async def run_simple_test():
    """간단한 테스트 쿼리 실행"""
    
    # API 키 확인
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\n❌ 오류: ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        print("   .env 파일을 확인해주세요.")
        return False
    
    print("\n" + "=" * 70)
    print("  Seoul Urban Research Agent - 자동 테스트")
    print("=" * 70)
    print("\n✓ API 키 확인 완료")
    
    # 세션 설정
    transcript_file, session_dir = setup_session()
    transcript = TranscriptWriter(transcript_file)
    tracker = SubagentTracker(transcript_writer=transcript, session_dir=session_dir)
    
    # 프롬프트 로드
    print("✓ 프롬프트 로드 중...")
    lead_agent_prompt = load_prompt("lead_agent.txt")
    domestic_researcher_prompt = load_prompt("domestic_researcher.txt")
    international_researcher_prompt = load_prompt("international_researcher.txt")
    statistics_researcher_prompt = load_prompt("statistics_researcher.txt")
    citizen_voice_researcher_prompt = load_prompt("citizen_voice_researcher.txt")
    urban_data_analyst_prompt = load_prompt("urban_data_analyst.txt")
    policy_writer_prompt = load_prompt("policy_writer.txt")
    print("✓ 7개 프롬프트 로드 완료")
    
    # 서브에이전트 정의
    agents = {
        "domestic-researcher": AgentDefinition(
            description="국내 도시 정책 사례 조사",
            tools=["WebSearch", "Write"],
            prompt=domestic_researcher_prompt,
            model="haiku"
        ),
        "international-researcher": AgentDefinition(
            description="해외 도시 정책 사례 조사",
            tools=["WebSearch", "Write"],
            prompt=international_researcher_prompt,
            model="haiku"
        ),
        "statistics-researcher": AgentDefinition(
            description="공공 데이터 및 통계 수집",
            tools=["WebSearch", "Write", "Bash"],
            prompt=statistics_researcher_prompt,
            model="haiku"
        ),
        "citizen-voice-researcher": AgentDefinition(
            description="시민 의견 및 설문조사 데이터 수집",
            tools=["WebSearch", "Write"],
            prompt=citizen_voice_researcher_prompt,
            model="haiku"
        ),
        "urban-data-analyst": AgentDefinition(
            description="도시 데이터 분석 및 시각화",
            tools=["Glob", "Read", "Bash", "Write"],
            prompt=urban_data_analyst_prompt,
            model="haiku"
        ),
        "policy-writer": AgentDefinition(
            description="정책 브리프 PDF 작성",
            tools=["Skill", "Write", "Glob", "Read", "Bash"],
            prompt=policy_writer_prompt,
            model="haiku"
        )
    }
    
    # 훅 설정
    hooks = {
        'PreToolUse': [
            HookMatcher(matcher=None, hooks=[tracker.pre_tool_use_hook])
        ],
        'PostToolUse': [
            HookMatcher(matcher=None, hooks=[tracker.post_tool_use_hook])
        ]
    }
    
    # 에이전트 옵션
    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        setting_sources=["project"],
        system_prompt=lead_agent_prompt,
        allowed_tools=["Task"],
        agents=agents,
        hooks=hooks,
        model="haiku"
    )
    
    # 테스트 쿼리
    test_query = "부산시 자전거 도로 현황을 간단히 조사해주세요"
    
    print(f"\n📝 테스트 쿼리: \"{test_query}\"")
    print("\n⏳ 에이전트 실행 중...\n")
    
    try:
        async with ClaudeSDKClient(options=options) as client:
            # 쿼리 전송
            transcript.write_to_file(f"\n사용자: {test_query}\n")
            await client.query(prompt=test_query)
            
            transcript.write("\n에이전트: ", end="")
            
            # 응답 수신
            async for msg in client.receive_response():
                if type(msg).__name__ == 'AssistantMessage':
                    process_assistant_message(msg, tracker, transcript)
            
            transcript.write("\n")
        
        print("\n" + "=" * 70)
        print("✓ 테스트 완료!")
        print("=" * 70)
        print(f"\n📁 세션 로그: {session_dir}")
        print(f"   - 대화 기록: {transcript_file}")
        print(f"   - 도구 호출: {session_dir / 'tool_calls.jsonl'}")
        
        # 생성된 파일 확인
        files_dir = Path("files")
        if files_dir.exists():
            print(f"\n📂 생성된 파일:")
            for subdir in files_dir.rglob("*"):
                if subdir.is_file():
                    print(f"   - {subdir}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        transcript.close()
        tracker.close()


if __name__ == "__main__":
    print("\n🚀 Seoul Urban Research Agent 테스트 시작\n")
    
    success = asyncio.run(run_simple_test())
    
    if success:
        print("\n✅ 테스트 성공!")
        print("\n다음 단계:")
        print("1. 생성된 연구 노트 확인")
        print("2. 더 복잡한 쿼리로 전체 워크플로우 테스트")
        print("3. 시각화 및 PDF 생성 테스트")
        sys.exit(0)
    else:
        print("\n❌ 테스트 실패")
        print("로그를 확인하여 문제를 진단하세요.")
        sys.exit(1)
