"""
Seoul Urban Research Agent - Web API Wrapper

Next.js 웹 앱에서 호출할 수 있는 간단한 Python API 래퍼
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from seoul_research_agent.agent import load_prompt
from seoul_research_agent.utils.transcript import setup_session, TranscriptWriter
from seoul_research_agent.utils.subagent_tracker import SubagentTracker
from seoul_research_agent.utils.message_handler import process_assistant_message
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition, HookMatcher


class ResearchAgentAPI:
    """웹 앱용 Research Agent API"""
    
    def __init__(self):
        self.sessions = {}
    
    async def start_research(self, query: str, session_id: str = None):
        """연구 시작"""
        if not session_id:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 세션 디렉토리 설정
        transcript_file, session_dir = setup_session()
        transcript = TranscriptWriter(transcript_file)
        tracker = SubagentTracker(transcript_writer=transcript, session_dir=session_dir)
        
        # 프롬프트 로드
        lead_agent_prompt = load_prompt("lead_agent.txt")
        domestic_researcher_prompt = load_prompt("domestic_researcher.txt")
        international_researcher_prompt = load_prompt("international_researcher.txt")
        statistics_researcher_prompt = load_prompt("statistics_researcher.txt")
        citizen_voice_researcher_prompt = load_prompt("citizen_voice_researcher.txt")
        urban_data_analyst_prompt = load_prompt("urban_data_analyst.txt")
        policy_writer_prompt = load_prompt("policy_writer.txt")
        
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
        
        # 세션 정보 저장
        self.sessions[session_id] = {
            'query': query,
            'session_dir': session_dir,
            'transcript_file': transcript_file,
            'status': 'running',
            'events': []
        }
        
        try:
            async with ClaudeSDKClient(options=options) as client:
                # 쿼리 전송
                transcript.write_to_file(f"\n사용자: {query}\n")
                await client.query(prompt=query)
                
                transcript.write("\n에이전트: ", end="")
                
                # 응답 수신
                async for msg in client.receive_response():
                    if type(msg).__name__ == 'AssistantMessage':
                        process_assistant_message(msg, tracker, transcript)
                        
                        # 이벤트 기록
                        event = {
                            'type': 'message',
                            'content': str(msg),
                            'timestamp': datetime.now().isoformat()
                        }
                        self.sessions[session_id]['events'].append(event)
                
                transcript.write("\n")
            
            # 완료 상태 업데이트
            self.sessions[session_id]['status'] = 'completed'
            
            return {
                'session_id': session_id,
                'status': 'completed',
                'session_dir': str(session_dir),
                'transcript_file': str(transcript_file)
            }
            
        except Exception as e:
            self.sessions[session_id]['status'] = 'error'
            self.sessions[session_id]['error'] = str(e)
            raise
        finally:
            transcript.close()
            tracker.close()
    
    def get_session_status(self, session_id: str):
        """세션 상태 조회"""
        if session_id not in self.sessions:
            return {'error': 'Session not found'}
        
        return self.sessions[session_id]


# CLI 인터페이스
async def main():
    """CLI로 실행"""
    if len(sys.argv) < 2:
        print("Usage: python web_api.py <query>")
        sys.exit(1)
    
    query = sys.argv[1]
    
    api = ResearchAgentAPI()
    result = await api.start_research(query)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
