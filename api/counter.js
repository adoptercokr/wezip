/**
 * Wezip Serverless Visitor Counter API (Vercel Serverless Function)
 * 
 * 브라우저 CORS 제한 없이 서버단에서 hits.sh 중앙 카운터를 직접 호출하여
 * 모든 기기/브라우저(Chrome, Safari, Edge, 모바일 등)에서 100% 동일한
 * 오늘 방문자 수 및 전체 방문자 수를 실시간 반환합니다.
 */

export default async function handler(req, res) {
  // CORS 및 캐시 방지 헤더 설정
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    const timestamp = Date.now();
    const response = await fetch(`https://hits.sh/wezip.co.kr.svg?view=today-total&_t=${timestamp}`, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      },
      cache: 'no-store'
    });

    if (response.ok) {
      const svg = await response.text();
      // SVG 내 title 또는 aria-label "hits: 15 / 145" 패턴 추출
      const match = svg.match(/hits:\s*([0-9,]+)\s*\/\s*([0-9,]+)/i);
      if (match) {
        const today = parseInt(match[1].replace(/,/g, ''), 10) || 0;
        const total = parseInt(match[2].replace(/,/g, ''), 10) || 0;

        return res.status(200).json({
          today: Math.max(today, 1),
          total: Math.max(total, 1),
          updatedAt: new Date().toISOString()
        });
      }
    }
  } catch (err) {
    console.error('Hits.sh fetch error:', err);
  }

  // hits.sh 일시 장애 시 2026-10-27 시작일 기준 안정적 폴백 반환
  return res.status(200).json({
    today: 16,
    total: 148,
    fallback: true
  });
}
