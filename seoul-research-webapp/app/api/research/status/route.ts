import { NextRequest } from 'next/server';
import path from 'path';
import fs from 'fs/promises';

export async function GET(request: NextRequest) {
    const searchParams = request.nextUrl.searchParams;
    const sessionId = searchParams.get('sessionId');

    if (!sessionId) {
        return new Response('Session ID required', { status: 400 });
    }

    // SSE 헤더 설정
    const encoder = new TextEncoder();
    const stream = new ReadableStream({
        async start(controller) {
            try {
                // 시작 이벤트
                const startMessage = `event: started\ndata: ${JSON.stringify({
                    message: '연구 시작'
                })}\n\n`;
                controller.enqueue(encoder.encode(startMessage));

                // Python 에이전트 경로
                const agentPath = path.join(
                    process.cwd(),
                    '..',
                    'seoul-urban-research-agent'
                );

                const logsPath = path.join(agentPath, 'logs');

                // 에이전트 진행 상황 모니터링
                // 실제 구현에서는 로그 파일을 tail하거나 프로세스 출력을 파싱해야 함
                // 여기서는 간단한 시뮬레이션

                const agents = [
                    { name: 'Lead Agent', task: '연구 계획 수립', delay: 2000 },
                    { name: 'Domestic Researcher', task: '국내 사례 조사', delay: 3000 },
                    { name: 'International Researcher', task: '해외 사례 조사', delay: 3000 },
                    { name: 'Statistics Researcher', task: '통계 데이터 수집', delay: 3000 },
                    { name: 'Citizen Voice Researcher', task: '시민 의견 수집', delay: 3000 },
                    { name: 'Urban Data Analyst', task: '데이터 분석 및 시각화', delay: 4000 },
                    { name: 'Policy Writer', task: 'PDF 보고서 작성', delay: 4000 },
                ];

                for (const agent of agents) {
                    // 에이전트 시작
                    const startMsg = `event: agent_started\ndata: ${JSON.stringify({
                        agent: agent.name,
                        task: agent.task
                    })}\n\n`;
                    controller.enqueue(encoder.encode(startMsg));

                    // 잠시 대기
                    await new Promise(resolve => setTimeout(resolve, agent.delay));

                    // 에이전트 완료
                    const completeMsg = `event: agent_completed\ndata: ${JSON.stringify({
                        agent: agent.name
                    })}\n\n`;
                    controller.enqueue(encoder.encode(completeMsg));
                }

                // 세션 디렉토리 찾기
                let sessionDir: string | null = null;
                let filesCreated: string[] = [];

                try {
                    const logDirs = await fs.readdir(logsPath);
                    const sortedDirs = logDirs
                        .filter(dir => dir.startsWith('session_'))
                        .sort()
                        .reverse();

                    if (sortedDirs.length > 0) {
                        sessionDir = path.join(logsPath, sortedDirs[0]);

                        // 생성된 파일 찾기
                        const filesPath = path.join(agentPath, 'files');

                        // 연구 노트
                        try {
                            const researchNotes = await fs.readdir(path.join(filesPath, 'research_notes'));
                            filesCreated.push(...researchNotes.map(f => `research_notes/${f}`));
                        } catch { }

                        // 차트
                        try {
                            const charts = await fs.readdir(path.join(filesPath, 'charts'));
                            filesCreated.push(...charts.map(f => `charts/${f}`));
                        } catch { }

                        // 보고서
                        try {
                            const reports = await fs.readdir(path.join(filesPath, 'reports'));
                            filesCreated.push(...reports.filter(f => f.endsWith('.pdf')).map(f => `reports/${f}`));
                        } catch { }
                    }
                } catch (error) {
                    console.error('Error reading logs:', error);
                }

                // 파일 생성 이벤트
                for (const file of filesCreated) {
                    const fileMsg = `event: file_created\ndata: ${JSON.stringify({
                        file
                    })}\n\n`;
                    controller.enqueue(encoder.encode(fileMsg));
                }

                // 완료 이벤트
                const completeMessage = `event: completed\ndata: ${JSON.stringify({
                    sessionDir,
                    filesCreated,
                    message: '연구 완료'
                })}\n\n`;
                controller.enqueue(encoder.encode(completeMessage));

            } catch (error) {
                const errorMessage = `event: error\ndata: ${JSON.stringify({
                    error: String(error)
                })}\n\n`;
                controller.enqueue(encoder.encode(errorMessage));
            } finally {
                controller.close();
            }
        }
    });

    return new Response(stream, {
        headers: {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
        },
    });
}
