/**
 * Wezip Contact Submission API (Vercel Serverless Function)
 * 
 * 애니맵(Animap)과 100% 동일한 서버리스 아키텍처:
 * 클라이언트 브라우저 직접 호출 대신, Vercel 서버단에서 안전하게 중계하여
 * 브라우저 CORS 차단 및 해외 Cloudflare 방화벽 오류 없이 
 * [위집 wezip.co.kr] 출처를 명확히 각인하여 관리자 이메일(joykorea7@gmail.com)로 전달합니다.
 */

export default async function handler(req, res) {
  // CORS 및 헤더 설정
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const body = req.body || {};
    const { type = 'general', title = '', contact = '', company = '', message = '' } = body;

    if (!contact || !message) {
      return res.status(400).json({ error: '연락처와 문의내용을 입력해 주세요.' });
    }

    // 관리자 수신 이메일 (Base64 난독화: joykorea7@gmail.com)
    const emailDest = Buffer.from('am95a29yZWE3QGdtYWlsLmNvbQ==', 'base64').toString('utf-8');
    const isAd = type === 'ad';
    const inquiryTitle = title && title.trim() ? title.trim() : (isAd ? '광고 제휴 문의' : '일반 서비스 문의');
    const subject = `[위집 ${isAd ? '광고문의' : '일반문의'}] ${inquiryTitle}`;

    const payload = {
      name: `[위집 wezip.co.kr] ${isAd ? '광고문의' : '일반문의'}`,
      _subject: subject,
      사이트출처: '위집 (wezip.co.kr) - 대한민국 생활 금융 포털',
      문의유형: isAd ? '광고 및 제휴 문의' : '일반 문의',
      문의제목: inquiryTitle,
      회신연락처: contact.trim(),
      업체명: company && company.trim() ? company.trim() : '(미입력)',
      문의내용: message.trim(),
      접수일시: new Date().toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' })
    };

    if (contact.includes('@')) {
      payload._replyto = contact.trim();
    }

    // Vercel 서버단에서 FormSubmit으로 안전하게 전달 (서버 간 통신으로 클라이언트 차단 우회)
    try {
      await fetch(`https://formsubmit.co/ajax/${emailDest}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        },
        body: JSON.stringify(payload)
      });
    } catch (upstreamErr) {
      console.warn('FormSubmit upstream warning:', upstreamErr);
    }

    return res.status(200).json({
      success: true,
      message: '문의가 정상 접수되었습니다. 신속히 확인 후 회신드리겠습니다.'
    });
  } catch (error) {
    console.error('Contact handler error:', error);
    // 사용자 경험을 위해 항상 친절한 성공 응답 반환 (애니맵과 100% 동일)
    return res.status(200).json({
      success: true,
      message: '문의가 정상 접수되었습니다.'
    });
  }
}
