'use client';

import { useState } from 'react';

interface ResearchInputProps {
    onStartResearch: (query: string) => void;
}

const quickStartTemplates = [
    '서울시 자전거 도로 확충 정책을 연구해주세요',
    '서울시 대중교통 개선 방안을 분석해주세요',
    '서울시 녹지 공간 확대 정책을 조사해주세요',
    '서울시 스마트시티 구축 전략을 연구해주세요',
];

export default function ResearchInput({ onStartResearch }: ResearchInputProps) {
    const [query, setQuery] = useState('');

    const handleSubmit = () => {
        if (query.trim()) {
            onStartResearch(query);
        }
    };

    return (
        <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                    🔍 연구 주제 입력
                </h2>

                <textarea
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="연구하고 싶은 도시 정책 주제를 입력하세요..."
                    className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                />

                <div className="mt-4">
                    <p className="text-sm text-gray-600 mb-2">빠른 시작 템플릿:</p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                        {quickStartTemplates.map((template, index) => (
                            <button
                                key={index}
                                onClick={() => setQuery(template)}
                                className="px-4 py-2 text-sm text-left bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-lg transition-colors"
                            >
                                {template}
                            </button>
                        ))}
                    </div>
                </div>

                <button
                    onClick={handleSubmit}
                    disabled={!query.trim()}
                    className="mt-6 w-full px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                    🚀 연구 시작
                </button>

                <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                    <p className="text-sm text-blue-800">
                        <strong>💡 참고</strong>: 연구는 약 5-10분 정도 소요됩니다.
                        6개의 전문 에이전트가 순차적으로 데이터를 수집하고 분석하여
                        한글 PDF 정책 브리프를 생성합니다.
                    </p>
                </div>
            </div>
        </div>
    );
}
