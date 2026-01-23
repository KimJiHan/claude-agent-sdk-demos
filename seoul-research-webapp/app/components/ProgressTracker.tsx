'use client';

import { useEffect, useState } from 'react';

interface ProgressTrackerProps {
    sessionId: string;
    query: string;
    onComplete: () => void;
}

interface AgentStatus {
    name: string;
    status: 'pending' | 'running' | 'completed';
    description?: string;
}

export default function ProgressTracker({ sessionId, query, onComplete }: ProgressTrackerProps) {
    const [agents, setAgents] = useState<AgentStatus[]>([
        { name: 'Lead Agent', status: 'pending' },
        { name: 'Domestic Researcher', status: 'pending' },
        { name: 'International Researcher', status: 'pending' },
        { name: 'Statistics Researcher', status: 'pending' },
        { name: 'Citizen Voice Researcher', status: 'pending' },
        { name: 'Urban Data Analyst', status: 'pending' },
        { name: 'Policy Writer', status: 'pending' },
    ]);

    const [filesCreated, setFilesCreated] = useState<string[]>([]);
    const [currentEvent, setCurrentEvent] = useState<string>('연구 시작 중...');

    useEffect(() => {
        // SSE 연결
        const eventSource = new EventSource(`/api/research/status?sessionId=${sessionId}`);

        eventSource.addEventListener('started', (e) => {
            const data = JSON.parse(e.data);
            setCurrentEvent(data.message);
        });

        eventSource.addEventListener('agent_started', (e) => {
            const data = JSON.parse(e.data);
            setCurrentEvent(`${data.agent}: ${data.task}`);

            // 에이전트 상태 업데이트
            setAgents(prev => prev.map(agent =>
                agent.name === data.agent
                    ? { ...agent, status: 'running' as const, description: data.task }
                    : agent
            ));
        });

        eventSource.addEventListener('agent_completed', (e) => {
            const data = JSON.parse(e.data);

            // 에이전트 상태 업데이트
            setAgents(prev => prev.map(agent =>
                agent.name === data.agent
                    ? { ...agent, status: 'completed' as const }
                    : agent
            ));
        });

        eventSource.addEventListener('file_created', (e) => {
            const data = JSON.parse(e.data);
            setFilesCreated(prev => [...prev, data.file]);
        });

        eventSource.addEventListener('completed', (e) => {
            setCurrentEvent('연구 완료!');
            setTimeout(() => {
                eventSource.close();
                onComplete();
            }, 1000);
        });

        eventSource.addEventListener('error', (e) => {
            // SSE 연결이 정상적으로 종료될 때도 error 이벤트가 발생하므로
            // readyState를 확인하여 실제 오류인지 판단
            if (eventSource.readyState === EventSource.CLOSED) {
                // 정상 종료 - 로그 출력 안 함
                eventSource.close();
            } else {
                // 실제 오류
                console.error('SSE Error:', e);
                setCurrentEvent('연결 오류 발생');
                eventSource.close();
            }
        });

        return () => {
            eventSource.close();
        };
    }, [sessionId, onComplete]);

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'completed': return '✅';
            case 'running': return '⏳';
            default: return '⏸️';
        }
    };

    const completedCount = agents.filter(a => a.status === 'completed').length;
    const progress = (completedCount / agents.length) * 100;

    return (
        <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
                <div className="mb-6">
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">
                        ⏳ 연구 진행 중...
                    </h2>
                    <p className="text-gray-600">{query}</p>
                    <p className="text-sm text-blue-600 mt-2">{currentEvent}</p>
                </div>

                {/* Progress Bar */}
                <div className="mb-8">
                    <div className="flex justify-between text-sm text-gray-600 mb-2">
                        <span>{completedCount}/{agents.length} 완료</span>
                        <span>{Math.round(progress)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                            className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                            style={{ width: `${progress}%` }}
                        />
                    </div>
                </div>

                {/* Agent Status */}
                <div className="space-y-3 mb-8">
                    {agents.map((agent, index) => (
                        <div
                            key={index}
                            className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg"
                        >
                            <span className="text-2xl">{getStatusIcon(agent.status)}</span>
                            <div className="flex-1">
                                <div className="font-medium text-gray-900">{agent.name}</div>
                                {agent.description && (
                                    <div className="text-sm text-gray-600">{agent.description}</div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>

                {/* Files Created */}
                {filesCreated.length > 0 && (
                    <div>
                        <h3 className="font-medium text-gray-900 mb-3">
                            📊 생성된 파일 ({filesCreated.length}개)
                        </h3>
                        <div className="space-y-2">
                            {filesCreated.map((file, index) => (
                                <div
                                    key={index}
                                    className="px-4 py-2 bg-green-50 border border-green-200 rounded-lg text-sm text-green-800"
                                >
                                    📄 {file}
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
