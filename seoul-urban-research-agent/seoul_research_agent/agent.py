"""Entry point for research agent using AgentDefinition for subagents."""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition, HookMatcher

from seoul_research_agent.utils.subagent_tracker import SubagentTracker
from seoul_research_agent.utils.transcript import setup_session, TranscriptWriter
from seoul_research_agent.utils.message_handler import process_assistant_message

# Load environment variables
load_dotenv()

# Paths to prompt files
PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(filename: str) -> str:
    """Load a prompt from the prompts directory."""
    prompt_path = PROMPTS_DIR / filename
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


async def chat():
    """Start interactive chat with the research agent."""

    # Check API key first, before creating any files
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\nError: ANTHROPIC_API_KEY not found.")
        print("Set it in a .env file or export it in your shell.")
        print("Get your key at: https://console.anthropic.com/settings/keys\n")
        return

    # Setup session directory and transcript
    transcript_file, session_dir = setup_session()

    # Create transcript writer
    transcript = TranscriptWriter(transcript_file)

    # Load prompts
    lead_agent_prompt = load_prompt("lead_agent.txt")
    domestic_researcher_prompt = load_prompt("domestic_researcher.txt")
    international_researcher_prompt = load_prompt("international_researcher.txt")
    statistics_researcher_prompt = load_prompt("statistics_researcher.txt")
    citizen_voice_researcher_prompt = load_prompt("citizen_voice_researcher.txt")
    urban_data_analyst_prompt = load_prompt("urban_data_analyst.txt")
    policy_writer_prompt = load_prompt("policy_writer.txt")

    # Initialize subagent tracker with transcript writer and session directory
    tracker = SubagentTracker(transcript_writer=transcript, session_dir=session_dir)

    # Define specialized subagents for Seoul Urban Research
    agents = {
        "domestic-researcher": AgentDefinition(
            description=(
                "국내 도시 정책 사례를 조사하는 전문 연구원입니다. "
                "서울, 부산, 인천 등 국내 주요 도시의 정책 사례, 통계, 성공/실패 사례를 조사합니다. "
                "지자체 보도자료, 정책 문서, 연구 보고서를 검색하여 국내 맥락에 맞는 데이터를 수집합니다. "
                "결과를 files/research_notes/domestic_cases/에 저장합니다."
            ),
            tools=["WebSearch", "Write"],
            prompt=domestic_researcher_prompt,
            model="haiku"
        ),
        "international-researcher": AgentDefinition(
            description=(
                "해외 도시 정책 사례를 조사하는 전문 연구원입니다. "
                "뉴욕, 런던, 도쿄, 싱가포르 등 글로벌 주요 도시의 정책 사례를 조사합니다. "
                "OECD, UN-Habitat, 세계은행 등 국제기구 보고서와 해외 도시 정부 자료를 검색하여 "
                "벤치마킹 가능한 사례를 수집합니다. 결과를 files/research_notes/international_cases/에 저장합니다."
            ),
            tools=["WebSearch", "Write"],
            prompt=international_researcher_prompt,
            model="haiku"
        ),
        "statistics-researcher": AgentDefinition(
            description=(
                "공공 데이터 및 통계를 수집하는 전문 연구원입니다. "
                "통계청, 서울시 빅데이터 캠퍼스, 공공데이터포털 등에서 정량적 통계 데이터를 수집합니다. "
                "인구, 교통, 환경, 경제 등 도시 지표 데이터를 우선적으로 검색합니다. "
                "결과를 files/research_notes/statistics/에 저장합니다."
            ),
            tools=["WebSearch", "Write", "Bash"],
            prompt=statistics_researcher_prompt,
            model="haiku"
        ),
        "citizen-voice-researcher": AgentDefinition(
            description=(
                "시민 의견 및 설문조사 데이터를 수집하는 전문 연구원입니다. "
                "시민 설문조사, 공청회 자료, SNS 여론, 민원 데이터 등 시민의 목소리를 수집합니다. "
                "서울시 민주주의 서울, 시민참여예산 등의 플랫폼 데이터를 조사합니다. "
                "결과를 files/research_notes/citizen_voice/에 저장합니다."
            ),
            tools=["WebSearch", "Write"],
            prompt=citizen_voice_researcher_prompt,
            model="haiku"
        ),
        "urban-data-analyst": AgentDefinition(
            description=(
                "도시 연구 데이터를 분석하고 시각화하는 전문 데이터 분석가입니다. "
                "연구 노트에서 데이터를 추출하고 Python(matplotlib/folium)으로 차트 및 지도 시각화를 생성합니다. "
                "차트는 files/charts/에, 지도는 files/geodata/에, 데이터 요약은 files/data/에 저장합니다. "
                "모든 researcher가 완료된 후에 사용하세요."
            ),
            tools=["Glob", "Read", "Bash", "Write"],
            prompt=urban_data_analyst_prompt,
            model="haiku"
        ),
        "policy-writer": AgentDefinition(
            description=(
                "정책 브리프 PDF 보고서를 작성하는 전문 작성자입니다. "
                "연구 결과를 정책 브리프 형식의 한글 PDF 보고서로 작성합니다. "
                "연구 노트, 데이터 분석, 차트를 종합하여 files/reports/에 전문적인 PDF를 생성합니다. "
                "정책 제안, 기대 효과, 추진 방안을 포함한 구조화된 문서를 생성합니다. "
                "urban-data-analyst 완료 후에 사용하세요."
            ),
            tools=["Skill", "Write", "Glob", "Read", "Bash"],
            prompt=policy_writer_prompt,
            model="haiku"
        )
    }

    # Set up hooks for tracking
    hooks = {
        'PreToolUse': [
            HookMatcher(
                matcher=None,  # Match all tools
                hooks=[tracker.pre_tool_use_hook]
            )
        ],
        'PostToolUse': [
            HookMatcher(
                matcher=None,  # Match all tools
                hooks=[tracker.post_tool_use_hook]
            )
        ]
    }

    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        setting_sources=["project"],  # Load skills from project .claude directory
        system_prompt=lead_agent_prompt,
        allowed_tools=["Task"],
        agents=agents,
        hooks=hooks,
        model="haiku"
    )

    print("\n" + "=" * 60)
    print("  Seoul Urban Research Agent (서울연구원 AI 연구 에이전트)")
    print("=" * 60)
    print("\n도시 정책 연구를 수행하고 정책 브리프 PDF를 생성합니다.")
    print("예시: '서울시 자전거 도로 확충 정책을 연구해주세요'")
    print("\n종료하려면 'exit'를 입력하세요.\n")

    try:
        async with ClaudeSDKClient(options=options) as client:
            while True:
                # Get input
                try:
                    user_input = input("\nYou: ").strip()
                except (EOFError, KeyboardInterrupt):
                    break

                if not user_input or user_input.lower() in ["exit", "quit", "q"]:
                    break

                # Write user input to transcript (file only, not console)
                transcript.write_to_file(f"\nYou: {user_input}\n")

                # Send to agent
                await client.query(prompt=user_input)

                transcript.write("\nAgent: ", end="")

                # Stream and process response
                async for msg in client.receive_response():
                    if type(msg).__name__ == 'AssistantMessage':
                        process_assistant_message(msg, tracker, transcript)

                transcript.write("\n")
    finally:
        transcript.write("\n\nGoodbye!\n")
        transcript.close()
        tracker.close()
        print(f"\nSession logs saved to: {session_dir}")
        print(f"  - Transcript: {transcript_file}")
        print(f"  - Tool calls: {session_dir / 'tool_calls.jsonl'}")


if __name__ == "__main__":
    asyncio.run(chat())
