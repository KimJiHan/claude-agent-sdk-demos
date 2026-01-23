import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs/promises';

// 활성 세션 저장
const activeSessions = new Map<string, {
    query: string;
    status: 'running' | 'completed' | 'error';
    process?: any;
    sessionDir?: string;
    startTime: number;
    endTime?: number;
}>();

export async function POST(request: NextRequest) {
    try {
        const { query } = await request.json();

        if (!query) {
            return NextResponse.json(
                { error: 'Query is required' },
                { status: 400 }
            );
        }

        // 세션 ID 생성
        const sessionId = `session_${Date.now()}`;

        // Python 에이전트 경로
        const agentPath = path.join(
            process.cwd(),
            '..',
            'seoul-urban-research-agent'
        );

        console.log('Starting research:', { sessionId, query, agentPath });

        // 세션 정보 초기화
        activeSessions.set(sessionId, {
            query,
            status: 'running',
            startTime: Date.now()
        });

        // Python 프로세스 시작 (백그라운드)
        // 실제 에이전트 실행
        const pythonProcess = spawn('uv', [
            'run',
            'python',
            'seoul_research_agent/agent.py'
        ], {
            cwd: agentPath,
            stdio: ['pipe', 'pipe', 'pipe']
        });

        // 세션 정보에 프로세스 저장
        const session = activeSessions.get(sessionId);
        if (session) {
            session.process = pythonProcess;
        }

        // 쿼리를 stdin으로 전달
        pythonProcess.stdin?.write(query + '\n');
        pythonProcess.stdin?.end();

        // 출력 캡처
        pythonProcess.stdout?.on('data', (data) => {
            const output = data.toString();
            console.log('[Agent Output]:', output);
        });

        pythonProcess.stderr?.on('data', (data) => {
            console.error('[Agent Error]:', data.toString());
        });

        pythonProcess.on('close', async (code) => {
            console.log('Python process closed:', code);
            const session = activeSessions.get(sessionId);
            if (session) {
                session.status = code === 0 ? 'completed' : 'error';
                session.endTime = Date.now();

                // 세션 디렉토리 찾기
                try {
                    const logsPath = path.join(agentPath, 'logs');
                    const logDirs = await fs.readdir(logsPath);
                    const sortedDirs = logDirs
                        .filter(dir => dir.startsWith('session_'))
                        .sort()
                        .reverse();

                    if (sortedDirs.length > 0) {
                        session.sessionDir = path.join(logsPath, sortedDirs[0]);
                    }
                } catch (error) {
                    console.error('Error finding session directory:', error);
                }
            }
        });

        return NextResponse.json({
            sessionId,
            status: 'started',
            query,
            message: 'Research started successfully'
        });
    } catch (error) {
        console.error('Error starting research:', error);
        return NextResponse.json(
            { error: 'Failed to start research', details: String(error) },
            { status: 500 }
        );
    }
}

// 세션 상태 조회를 위한 GET 엔드포인트
export async function GET(request: NextRequest) {
    const searchParams = request.nextUrl.searchParams;
    const sessionId = searchParams.get('sessionId');

    if (!sessionId) {
        return NextResponse.json({ error: 'Session ID required' }, { status: 400 });
    }

    const session = activeSessions.get(sessionId);
    if (!session) {
        return NextResponse.json({ error: 'Session not found' }, { status: 404 });
    }

    // 프로세스 정보 제외하고 반환
    const { process, ...sessionInfo } = session;
    return NextResponse.json(sessionInfo);
}
