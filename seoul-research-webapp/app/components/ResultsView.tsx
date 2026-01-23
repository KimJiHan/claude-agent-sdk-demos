'use client';

import { useEffect, useState } from 'react';

interface ResultsViewProps {
    sessionId: string;
    query: string;
    onNewResearch: () => void;
}

interface FileItem {
    name: string;
    file: string;
    size?: number;
}

interface Files {
    researchNotes: FileItem[];
    charts: FileItem[];
    maps: FileItem[];
    reports: FileItem[];
}

export default function ResultsView({ sessionId, query, onNewResearch }: ResultsViewProps) {
    const [files, setFiles] = useState<Files>({
        researchNotes: [],
        charts: [],
        maps: [],
        reports: [],
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // 파일 목록 가져오기
        const fetchFiles = async () => {
            try {
                const response = await fetch(`/api/files/list?sessionId=${sessionId}`);
                const data = await response.json();
                setFiles(data);
            } catch (error) {
                console.error('Error fetching files:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchFiles();
    }, [sessionId]);

    const handleDownload = (filePath: string) => {
        window.open(`/api/files/download?path=${encodeURIComponent(filePath)}`, '_blank');
    };

    const formatFileSize = (bytes?: number) => {
        if (!bytes) return '';
        const kb = bytes / 1024;
        if (kb < 1024) return `${kb.toFixed(1)} KB`;
        return `${(kb / 1024).toFixed(1)} MB`;
    };

    if (loading) {
        return (
            <div className="max-w-6xl mx-auto">
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
                    <div className="text-center">
                        <div className="text-2xl mb-4">⏳</div>
                        <p className="text-gray-600">파일 목록을 불러오는 중...</p>
                    </div>
                </div>
            </div>
        );
    }

    const totalFiles = files.researchNotes.length + files.charts.length + files.maps.length + files.reports.length;

    return (
        <div className="max-w-6xl mx-auto">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
                <div className="mb-8">
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">
                        ✅ 연구 완료!
                    </h2>
                    <p className="text-gray-600">{query}</p>
                    <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                        <p className="text-sm text-green-800">
                            <strong>✓ 생성 완료</strong>: 총 {totalFiles}개 파일이 생성되었습니다.
                        </p>
                    </div>
                </div>

                {/* Research Notes */}
                {files.researchNotes.length > 0 && (
                    <div className="mb-8">
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">
                            📄 연구 노트 ({files.researchNotes.length})
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {files.researchNotes.map((note, index) => (
                                <div
                                    key={index}
                                    onClick={() => handleDownload(note.file)}
                                    className="p-4 bg-blue-50 border border-blue-200 rounded-lg hover:bg-blue-100 cursor-pointer transition-colors"
                                >
                                    <div className="font-medium text-blue-900">{note.name}</div>
                                    <div className="text-sm text-blue-600 mt-1">{note.file}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Charts */}
                {files.charts.length > 0 && (
                    <div className="mb-8">
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">
                            📈 차트 ({files.charts.length})
                        </h3>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            {files.charts.map((chart, index) => (
                                <div
                                    key={index}
                                    onClick={() => handleDownload(chart.file)}
                                    className="p-4 bg-green-50 border border-green-200 rounded-lg hover:bg-green-100 cursor-pointer transition-colors"
                                >
                                    <div className="text-4xl mb-2">📊</div>
                                    <div className="font-medium text-green-900 text-sm">{chart.name}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Maps */}
                {files.maps.length > 0 && (
                    <div className="mb-8">
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">
                            🗺️ 지도 ({files.maps.length})
                        </h3>
                        <div className="grid grid-cols-1 gap-4">
                            {files.maps.map((map, index) => (
                                <div
                                    key={index}
                                    onClick={() => handleDownload(map.file)}
                                    className="p-4 bg-purple-50 border border-purple-200 rounded-lg hover:bg-purple-100 cursor-pointer transition-colors"
                                >
                                    <div className="font-medium text-purple-900">{map.name}</div>
                                    <div className="text-sm text-purple-600 mt-1">{map.file}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* PDF Report */}
                {files.reports.length > 0 && (
                    <div className="mb-8">
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">
                            📑 정책 브리프
                        </h3>
                        {files.reports.map((report, index) => (
                            <div key={index} className="p-6 bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg mb-4">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <div className="text-lg font-semibold text-gray-900">
                                            {report.name}
                                        </div>
                                        <div className="text-sm text-gray-600 mt-1">
                                            한글 PDF 보고서 · 차트 포함 {report.size && `· ${formatFileSize(report.size)}`}
                                        </div>
                                    </div>
                                    <button
                                        onClick={() => handleDownload(report.file)}
                                        className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
                                    >
                                        📥 다운로드
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {/* No files message */}
                {totalFiles === 0 && (
                    <div className="mb-8 p-6 bg-yellow-50 border border-yellow-200 rounded-lg">
                        <p className="text-yellow-800">
                            ⚠️ 생성된 파일이 없습니다. 연구가 완료되지 않았거나 오류가 발생했을 수 있습니다.
                        </p>
                    </div>
                )}

                {/* Actions */}
                <div className="flex space-x-4">
                    <button
                        onClick={onNewResearch}
                        className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
                    >
                        🔄 새 연구 시작
                    </button>
                </div>
            </div>
        </div>
    );
}
