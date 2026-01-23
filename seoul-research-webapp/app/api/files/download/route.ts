import { NextRequest, NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs/promises';

export async function GET(request: NextRequest) {
    try {
        const searchParams = request.nextUrl.searchParams;
        const filePath = searchParams.get('path');

        if (!filePath) {
            return NextResponse.json({ error: 'File path required' }, { status: 400 });
        }

        // Python 에이전트 경로
        const agentPath = path.join(
            process.cwd(),
            '..',
            'seoul-urban-research-agent'
        );

        const fullPath = path.join(agentPath, 'files', filePath);

        // 파일 존재 확인
        try {
            await fs.access(fullPath);
        } catch {
            return NextResponse.json({ error: 'File not found' }, { status: 404 });
        }

        // 파일 읽기
        const fileBuffer = await fs.readFile(fullPath);
        const fileName = path.basename(fullPath);

        // MIME 타입 결정
        let contentType = 'application/octet-stream';
        if (fileName.endsWith('.pdf')) {
            contentType = 'application/pdf';
        } else if (fileName.endsWith('.png')) {
            contentType = 'image/png';
        } else if (fileName.endsWith('.html')) {
            contentType = 'text/html';
        } else if (fileName.endsWith('.md')) {
            contentType = 'text/markdown';
        }

        // 파일 반환
        return new NextResponse(fileBuffer, {
            headers: {
                'Content-Type': contentType,
                'Content-Disposition': `attachment; filename="${encodeURIComponent(fileName)}"`,
            },
        });
    } catch (error) {
        console.error('Error downloading file:', error);
        return NextResponse.json(
            { error: 'Failed to download file', details: String(error) },
            { status: 500 }
        );
    }
}
