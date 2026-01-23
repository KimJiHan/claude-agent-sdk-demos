'use client';

import { useState } from 'react';
import ResearchInput from './components/ResearchInput';
import ProgressTracker from './components/ProgressTracker';
import ResultsView from './components/ResultsView';

export default function Home() {
  const [stage, setStage] = useState<'input' | 'progress' | 'results'>('input');
  const [query, setQuery] = useState('');
  const [sessionId, setSessionId] = useState('');

  const handleStartResearch = async (researchQuery: string) => {
    setQuery(researchQuery);
    setStage('progress');

    // API 호출 시뮬레이션
    const response = await fetch('/api/research/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: researchQuery }),
    });

    const data = await response.json();
    setSessionId(data.sessionId);
  };

  const handleResearchComplete = () => {
    setStage('results');
  };

  const handleNewResearch = () => {
    setStage('input');
    setQuery('');
    setSessionId('');
  };

  return (
    <main className="min-h-screen">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center space-x-3">
            <div className="text-4xl">🏙️</div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Seoul Urban Research Agent
              </h1>
              <p className="text-sm text-gray-600">
                서울연구원 맞춤형 AI 연구 에이전트
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {stage === 'input' && (
          <ResearchInput onStartResearch={handleStartResearch} />
        )}

        {stage === 'progress' && (
          <ProgressTracker
            sessionId={sessionId}
            query={query}
            onComplete={handleResearchComplete}
          />
        )}

        {stage === 'results' && (
          <ResultsView
            sessionId={sessionId}
            query={query}
            onNewResearch={handleNewResearch}
          />
        )}
      </div>
    </main>
  );
}
