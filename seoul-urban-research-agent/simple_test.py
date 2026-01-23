"""
Seoul Urban Research Agent - Simplified Web API

웹 앱에서 직접 호출할 수 있는 간단한 스크립트
"""

import sys
import json
from pathlib import Path

# 간단한 테스트 출력
if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "테스트 쿼리"
    
    print(json.dumps({
        "status": "started",
        "query": query,
        "message": "연구를 시작합니다..."
    }, ensure_ascii=False))
    
    # 실제 에이전트는 시간이 오래 걸리므로
    # 웹 앱에서는 간단한 응답만 반환
    print(json.dumps({
        "status": "info",
        "message": f"쿼리: {query}"
    }, ensure_ascii=False))
