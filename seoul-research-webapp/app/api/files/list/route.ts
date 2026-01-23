import { NextRequest, NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs/promises';

export async function GET(request: NextRequest) {
    try {
        const searchParams = request.nextUrl.searchParams;
        const sessionId = searchParams.get('sessionId');

        // Python 에이전트 경로
        const agentPath = path.join(
            process.cwd(),
            '..',
            'seoul-urban-research-agent'
        );

        const filesPath = path.join(agentPath, 'files');

        const files: {
            researchNotes: Array<{ name: string; file: string }>;
            charts: Array<{ name: string; file: string }>;
            maps: Array<{ name: string; file: string }>;
            reports: Array<{ name: string; file: string; size?: number }>;
        } = {
            researchNotes: [],
            charts: [],
            maps: [],
            reports: [],
        };

        // 연구 노트 찾기
        try {
            const researchNotesPath = path.join(filesPath, 'research_notes');
            const noteFiles = await fs.readdir(researchNotesPath);

            for (const file of noteFiles) {
                if (file.endsWith('.md')) {
                    const stats = await fs.stat(path.join(researchNotesPath, file));
                    files.researchNotes.push({
                        name: file.replace('.md', '').replace(/_/g, ' '),
                        file: `research_notes/${file}`,
                    });
                }
            }

            // 하위 디렉토리도 확인
            const subdirs = ['domestic_cases', 'international_cases', 'statistics', 'citizen_voice'];
            for (const subdir of subdirs) {
                try {
                    const subdirPath = path.join(researchNotesPath, subdir);
                    const subdirFiles = await fs.readdir(subdirPath);
                    for (const file of subdirFiles) {
                        if (file.endsWith('.md')) {
                            files.researchNotes.push({
                                name: `${subdir}/${file}`.replace('.md', '').replace(/_/g, ' '),
                                file: `research_notes/${subdir}/${file}`,
                            });
                        }
                    }
                } catch { }
            }
        } catch (error) {
            console.error('Error reading research notes:', error);
        }

        // 차트 찾기
        try {
            const chartsPath = path.join(filesPath, 'charts');
            const chartFiles = await fs.readdir(chartsPath);

            for (const file of chartFiles) {
                if (file.endsWith('.png')) {
                    files.charts.push({
                        name: file.replace('.png', '').replace(/_/g, ' '),
                        file: `charts/${file}`,
                    });
                }
            }
        } catch (error) {
            console.error('Error reading charts:', error);
        }

        // 지도 찾기
        try {
            const geodataPath = path.join(filesPath, 'geodata');
            const mapFiles = await fs.readdir(geodataPath);

            for (const file of mapFiles) {
                if (file.endsWith('.html')) {
                    files.maps.push({
                        name: file.replace('.html', '').replace(/_/g, ' '),
                        file: `geodata/${file}`,
                    });
                }
            }
        } catch (error) {
            console.error('Error reading maps:', error);
        }

        // PDF 보고서 찾기
        try {
            const reportsPath = path.join(filesPath, 'reports');
            const reportFiles = await fs.readdir(reportsPath);

            for (const file of reportFiles) {
                if (file.endsWith('.pdf')) {
                    const stats = await fs.stat(path.join(reportsPath, file));
                    files.reports.push({
                        name: file.replace('.pdf', '').replace(/_/g, ' '),
                        file: `reports/${file}`,
                        size: stats.size,
                    });
                }
            }
        } catch (error) {
            console.error('Error reading reports:', error);
        }

        return NextResponse.json(files);
    } catch (error) {
        console.error('Error listing files:', error);
        return NextResponse.json(
            { error: 'Failed to list files', details: String(error) },
            { status: 500 }
        );
    }
}
