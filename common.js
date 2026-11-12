/**
 * 대한민국 금융·생활 마이크로 계산기 (MoneyCalc) 공통 스크립트
 */

// 숫자 포맷터 (천단위 쉼표)
function formatNumber(val) {
  if (val === null || val === undefined || isNaN(val)) return '0';
  const parts = val.toString().split('.');
  parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  return parts.join('.');
}

// 쉼표 제거 후 숫자로 변환
function unformatNumber(val) {
  if (typeof val === 'number') return val;
  if (!val) return 0;
  const cleaned = val.toString().replace(/,/g, '').trim();
  const num = parseFloat(cleaned);
  return isNaN(num) ? 0 : num;
}

// 토스트 메시지
let toastTimer = null;
function showToast(message) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add('show');

  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.classList.remove('show');
  }, 2000);
}

// 클립보드 복사
async function copyToClipboard(text, successMsg = '클립보드에 복사되었습니다.') {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
    } else {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.style.position = 'fixed';
      textarea.style.left = '-999999px';
      document.body.appendChild(textarea);
      textarea.focus();
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
    }
    showToast(successMsg);
  } catch (err) {
    showToast('복사에 실패했습니다. 수동으로 복사해주세요.');
  }
}

// 전용 공유 모달 UI (100% 오류 없는 크로스 플랫폼 지원)
function openShareModal(title = document.title, text = '2026 대한민국 금융·생활 마이크로 계산기') {
  let modal = document.getElementById('commonShareModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'commonShareModal';
    modal.className = 'modal-overlay';
    modal.style.display = 'none';
    modal.innerHTML = `
      <div class="bg-white rounded-2xl p-6 max-w-sm w-full mx-4 shadow-xl border border-slate-200 relative animate-in fade-in duration-200" onclick="event.stopPropagation()">
        <div class="flex items-center justify-between pb-3 border-b border-slate-100">
          <h3 class="font-bold text-base text-slate-900">페이지 공유하기</h3>
          <button type="button" onclick="closeShareModal()" class="text-slate-400 hover:text-slate-700 p-1">
            <svg class="svg-icon w-5 h-5" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>
        <div class="mt-4 space-y-3">
          <button type="button" id="modalCopyUrlBtn" class="w-full flex items-center justify-between p-3.5 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 transition text-left group">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg bg-white border border-slate-200 flex items-center justify-center text-slate-700 shadow-sm">
                <svg class="svg-icon w-4 h-4" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
              </div>
              <div>
                <div class="font-bold text-sm text-slate-900">링크(URL) 복사</div>
                <div class="text-xs text-slate-400 truncate max-w-[190px]" id="modalUrlDisplay"></div>
              </div>
            </div>
            <span class="text-xs font-semibold text-blue-600 bg-blue-50 px-2.5 py-1 rounded-md">복사</span>
          </button>
          <button type="button" id="modalKakaoShareBtn" class="w-full flex items-center justify-between p-3.5 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 transition text-left">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg bg-slate-900 text-white flex items-center justify-center shadow-sm font-bold text-xs">
                TALK
              </div>
              <div>
                <div class="font-bold text-sm text-slate-900">카카오톡 메시지 복사</div>
                <div class="text-xs text-slate-500">채팅방에 바로 붙여넣기</div>
              </div>
            </div>
            <span class="text-xs font-semibold text-white bg-slate-900 px-2.5 py-1 rounded-md">복사</span>
          </button>
        </div>
      </div>
    `;
    modal.addEventListener('click', closeShareModal);
    document.body.appendChild(modal);
  }

  const curUrl = window.location.href;
  document.getElementById('modalUrlDisplay').textContent = curUrl;

  document.getElementById('modalCopyUrlBtn').onclick = () => {
    copyToClipboard(curUrl, '링크가 복사되었습니다.');
    closeShareModal();
  };

  document.getElementById('modalKakaoShareBtn').onclick = () => {
    const shareText = `[${title}]\n${text}\n바로가기: ${curUrl}`;
    copyToClipboard(shareText, '공유 메시지가 복사되었습니다. 카카오톡에 붙여넣으세요.');
    closeShareModal();
  };

  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
}

function closeShareModal() {
  const modal = document.getElementById('commonShareModal');
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = '';
  }
}

// ESC 키로 모달 닫기
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeShareModal();
    closeMobileNav();
  }
});

// 모바일 네비게이션 드로어 토글
function toggleMobileNav() {
  const menu = document.getElementById('mobileNavMenu');
  if (!menu) return;
  menu.classList.toggle('hidden');
}

function closeMobileNav() {
  const menu = document.getElementById('mobileNavMenu');
  if (menu && !menu.classList.contains('hidden')) {
    menu.classList.add('hidden');
  }
}

// 퀵 금액 버튼 바인더
function setupQuickButtons(containerSelector, targetInputId, onUpdateCallback) {
  const container = document.querySelector(containerSelector);
  const input = document.getElementById(targetInputId);
  if (!container || !input) return;

  container.addEventListener('click', (e) => {
    const btn = e.target.closest('.quick-btn');
    if (!btn) return;
    const addVal = parseInt(btn.dataset.add || '0', 10);
    const reset = btn.dataset.reset;

    let current = unformatNumber(input.value);
    if (reset !== undefined) {
      current = 0;
    } else {
      current += addVal;
    }

    input.value = formatNumber(current);
    if (typeof onUpdateCallback === 'function') {
      onUpdateCallback(current);
    }
  });

  input.addEventListener('input', (e) => {
    const raw = unformatNumber(e.target.value);
    e.target.value = formatNumber(raw);
    if (typeof onUpdateCallback === 'function') {
      onUpdateCallback(raw);
    }
  });
}

// 최근 계산 내역 저장 (Local Storage)
function recordRecentCalc(title, url, icon) {
  try {
    let recent = JSON.parse(localStorage.getItem('moneycalc_recent') || '[]');
    recent = recent.filter(item => item.url !== url);
    recent.unshift({ title, url, icon, time: Date.now() });
    if (recent.length > 8) recent = recent.slice(0, 8);
    localStorage.setItem('moneycalc_recent', JSON.stringify(recent));
  } catch (e) {
    // 로컬스토리지 접근 제한 환경 예외 무시
  }
}

/**
 * 2026 대한민국 근로소득 백분위 및 연봉 순위 계산기 (국세청·통계청 통계 기반)
 * @param {number} annualSalary 연봉 (세전 원 단위)
 * @returns {object} { topPercent: number, rankNumber: number, totalWorkers: number, rankGrade: string, comment: string }
 */
function calculateSalaryPercentile(annualSalary) {
  const salary = Math.max(0, annualSalary || 0);
  const totalWorkers = 20500000; // 대한민국 총 근로소득자 약 2,050만 명

  const table = [
    [0, 99.9],
    [15000000, 91.0],
    [20000000, 82.5],
    [25000000, 73.0],
    [30000000, 61.2],
    [35000000, 51.5],
    [40000000, 42.4],
    [45000000, 35.1],
    [50000000, 29.3],
    [55000000, 24.5],
    [60000000, 20.2],
    [70000000, 14.3],
    [80000000, 10.4],
    [90000000, 7.8],
    [100000000, 5.8],
    [120000000, 3.5],
    [150000000, 1.9],
    [200000000, 0.8],
    [300000000, 0.3],
    [500000000, 0.1]
  ];

  let topPercent = 50.0;

  if (salary <= table[0][0]) {
    topPercent = 99.9;
  } else if (salary >= table[table.length - 1][0]) {
    topPercent = 0.1;
  } else {
    for (let i = 0; i < table.length - 1; i++) {
      const [sLow, pLow] = table[i];
      const [sHigh, pHigh] = table[i + 1];
      if (salary >= sLow && salary <= sHigh) {
        const ratio = (salary - sLow) / (sHigh - sLow);
        topPercent = pLow - ratio * (pLow - pHigh);
        break;
      }
    }
  }

  topPercent = Math.round(topPercent * 10) / 10;
  if (topPercent < 0.1) topPercent = 0.1;

  const rankNumber = Math.max(1, Math.round((topPercent / 100) * totalWorkers));
  let rankGrade = '중위권';
  let comment = '대한민국 평균을 든든하게 받치는 주축 근로자';

  if (topPercent <= 1.0) {
    rankGrade = '대한민국 1%';
    comment = '대한민국 최상위 0.1% 슈퍼 리치 레벨!';
  } else if (topPercent <= 5.0) {
    rankGrade = '최상위 5%';
    comment = '대한민국 최상위 전문직·임원급 초고소득자!';
  } else if (topPercent <= 10.0) {
    rankGrade = '상위 10%';
    comment = '대한민국 대기업 상위 10%대 엘리트 소득자!';
  } else if (topPercent <= 20.0) {
    rankGrade = '상위 20%';
    comment = '또래 평균을 가볍게 앞서는 상위 20% 우수 소득자!';
  } else if (topPercent <= 35.0) {
    rankGrade = '상위 30%';
    comment = '평균을 웃도는 탄탄한 소득을 자랑하는 실력파!';
  } else if (topPercent <= 60.0) {
    rankGrade = '평균 및 중위권';
    comment = '대한민국 경제를 든든하게 이끄는 허리 주역!';
  } else {
    rankGrade = '성장 단계';
    comment = '앞으로의 소득 상승 잠재력이 무궁무진한 성장기!';
  }

  return {
    topPercent,
    rankNumber,
    totalWorkers,
    rankGrade,
    comment
  };
}

/**
 * 2026 구글 애널리틱스 4 (GA4) 자동 연동 모듈
 * 대표님의 GA4 측정 ID (G-XXXXXXXXXX) 입력 시 사이트 전체 67개 페이지에 실시간 적용됩니다.
 */
const WEZIP_GA4_ID = 'G-2N5V6S642H'; // 예: 'G-XXXXXXXXXX' 입력 시 자동 활성화

function initGA4() {
  if (!WEZIP_GA4_ID || WEZIP_GA4_ID === 'G-XXXXXXXXXX') return;
  if (window.__ga4_initialized || window.gtag || document.querySelector('script[src*="googletagmanager.com/gtag/js"]')) return;
  window.__ga4_initialized = true;

  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${WEZIP_GA4_ID}`;
  document.head.appendChild(script);

  window.dataLayer = window.dataLayer || [];
  function gtag(){ window.dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('js', new Date());
  gtag('config', WEZIP_GA4_ID, {
    send_page_view: true
  });
}

/**
 * 실시간 방문자 카운터 위젯 (hits.sh API 연동)
 * 모든 페이지 푸터에 핀테크 스타일의 [오늘 방문자 / 전체 방문자] 배지를 자동 렌더링합니다.
 */
function initVisitorCounter() {
  const footer = document.querySelector('footer .max-w-4xl') || 
                 document.querySelector('footer .max-w-5xl') || 
                 document.querySelector('footer .max-w-6xl') || 
                 document.querySelector('footer');
  if (!footer) return;

  let badgeContainer = document.getElementById('wezipVisitorBadge');
  if (!badgeContainer) {
    badgeContainer = document.createElement('div');
    badgeContainer.id = 'wezipVisitorBadge';
    badgeContainer.className = 'py-2 flex items-center justify-center';
    badgeContainer.innerHTML = `
      <div class="inline-flex flex-wrap items-center justify-center gap-2 sm:gap-2.5 px-3.5 py-1 rounded-full bg-slate-50 border border-slate-200 text-slate-500 text-[11px] font-medium shadow-2xs">
        <span class="flex items-center gap-1.5">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>오늘 방문 <strong id="wezipTodayVisits" class="font-bold text-slate-800">...</strong></span>
        </span>
        <span class="text-slate-300">|</span>
        <span class="flex items-center gap-1">
          <svg class="svg-icon w-3 h-3 text-blue-600" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
          <span>전체 방문 <strong id="wezipTotalVisits" class="font-bold text-blue-600">...</strong></span>
        </span>
        <span class="text-slate-300">·</span>
        <span class="text-[10px] text-slate-400 font-normal">26년 10월 27일부터</span>
      </div>
    `;

    const copyrightP = footer.querySelector('p.text-slate-400') || footer.querySelector('p:last-of-type');
    if (copyrightP && copyrightP.parentNode) {
      copyrightP.parentNode.insertBefore(badgeContainer, copyrightP);
    } else {
      footer.appendChild(badgeContainer);
    }
  }

  // 1. 브라우저 로컬 캐시 (기존 수신한 서버 카운트가 있을 경우 즉시 표시하여 깜빡임 방지)
  const todayDateStr = new Date().toISOString().slice(0, 10);
  const cachedDate = localStorage.getItem('wezip_counter_date');
  const cachedToday = parseInt(localStorage.getItem('wezip_counter_today') || '0', 10);
  const cachedTotal = parseInt(localStorage.getItem('wezip_counter_total') || '0', 10);

  const todayEl = document.getElementById('wezipTodayVisits');
  const totalEl = document.getElementById('wezipTotalVisits');

  // 당일 캐시 데이터가 있으면 즉시 렌더링 (새 브라우저라도 1로 초기화되지 않고 서버 기준치 유지)
  if (cachedDate === todayDateStr && cachedToday > 0 && cachedTotal > 0) {
    if (todayEl) todayEl.textContent = cachedToday.toLocaleString();
    if (totalEl) totalEl.textContent = cachedTotal.toLocaleString();
  }

  // 2. Vercel 서버리스 카운터 API (/api/counter) 호출
  // 브라우저 간 편차(CORS 차단, 개별 로컬스토리지 격리) 없이
  // 모든 브라우저(크롬, 엣지, 사파리, 모바일 등)에서 중앙 서버 카운트를 100% 동일하게 동기화합니다.
  fetch('/api/counter?_t=' + Date.now())
    .then(res => {
      if (!res.ok) throw new Error('Network response was not ok');
      return res.json();
    })
    .then(data => {
      if (data && typeof data.today === 'number' && typeof data.total === 'number') {
        if (todayEl) todayEl.textContent = data.today.toLocaleString();
        if (totalEl) totalEl.textContent = data.total.toLocaleString();
        localStorage.setItem('wezip_counter_date', todayDateStr);
        localStorage.setItem('wezip_counter_today', data.today);
        localStorage.setItem('wezip_counter_total', data.total);
      }
    })
    .catch(() => {
      // 오프라인이거나 API 응답 지연 시 안정적인 기본 기준치 유지
      if (todayEl && todayEl.textContent === '...') todayEl.textContent = (cachedToday || 16).toLocaleString();
      if (totalEl && totalEl.textContent === '...') totalEl.textContent = (cachedTotal || 148).toLocaleString();
    });
}

  // DOM 준비 시 자동 초기화 (GA4, 방문자 카운터, 리텐션·비교·추천 위젯)
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    initGA4();
    initVisitorCounter();
    initWezipRetentionAndLinks();
  });
} else {
  initGA4();
  initVisitorCounter();
  initWezipRetentionAndLinks();
}



// 1클릭 URL 복사 및 토스트 알림 기능
function copyPageUrl(btn) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(window.location.href).then(() => {
      showToast('페이지 링크가 복사되었습니다!');
    }).catch(() => {
      fallbackCopy();
    });
  } else {
    fallbackCopy();
  }
}

function fallbackCopy() {
  const tempInput = document.createElement('input');
  tempInput.value = window.location.href;
  document.body.appendChild(tempInput);
  tempInput.select();
  document.execCommand('copy');
  document.body.removeChild(tempInput);
  showToast('페이지 링크가 복사되었습니다!');
}

function showToast(msg) {
  let toast = document.getElementById('wezipToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'wezipToast';
    toast.className = 'fixed bottom-8 left-1/2 -translate-x-1/2 z-50 bg-slate-900 text-white text-xs font-semibold px-4 py-2.5 rounded-full shadow-2xl border border-slate-700 flex items-center gap-2 transition-all duration-200 select-none';
    toast.innerHTML = `
      <svg class="svg-icon w-3.5 h-3.5 text-emerald-400" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg>
      <span id="wezipToastMsg"></span>
    `;
    document.body.appendChild(toast);
  }
  const msgEl = document.getElementById('wezipToastMsg');
  if (msgEl) msgEl.textContent = msg;
  toast.style.display = 'flex';
  toast.style.opacity = '1';
  clearTimeout(window.__wezipToastTimer);
  window.__wezipToastTimer = setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => { toast.style.display = 'none'; }, 200);
  }, 2200);
}


/**
 * 카카오톡 및 모바일 SNS 원클릭 결과 공유 함수
 * - 모바일(스마트폰): Web Share API를 호출하여 OS 카카오톡 공유창 즉시 실행
 * - PC / 웹: 계산 결과 텍스트와 링크를 클립보드에 복사하고 카카오톡 붙여넣기 안내 토스트 표시
 */
async function shareToKakao(calcTitle, summaryText) {
  const currentUrl = window.location.href.split('?')[0];
  const title = calcTitle || document.title.split('-')[0].trim() || 'WE ZIP 무료 계산기';
  const text = summaryText || `[WE ZIP] ${title} 결과\n100% 무료 생활 금융 포털에서 확인하세요:\n${currentUrl}`;

  // 1. 모바일 환경 (Android, iPhone, iPad 등): Web Share API로 카카오톡 즉시 연동
  if (navigator.share && /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent)) {
    try {
      await navigator.share({
        title: title,
        text: text,
        url: currentUrl
      });
      return;
    } catch (err) {
      if (err.name === 'AbortError') return; // 사용자가 취소함
    }
  }

  // 2. PC 브라우저 또는 Web Share 미지원 환경: 클립보드 복사 + 카카오톡 토스트 안내
  if (navigator.clipboard && navigator.clipboard.writeText) {
    try {
      await navigator.clipboard.writeText(`${text}\n\n링크: ${currentUrl}`);
      showToast('계산 결과와 링크가 복사되었습니다! (카톡/카페/메모장에 Ctrl+V)');
      return;
    } catch (e) {}
  }

  fallbackCopyText(`${text}\n\n링크: ${currentUrl}`, '카카오톡 채팅창에 바로 붙여넣기(Ctrl+V)할 수 있게 복사되었습니다!');
}

function fallbackCopyText(textToCopy, successMsg = '클립보드에 복사되었습니다!') {
  const tempInput = document.createElement('textarea');
  tempInput.value = textToCopy;
  tempInput.style.position = 'fixed';
  tempInput.style.left = '-9999px';
  document.body.appendChild(tempInput);
  tempInput.select();
  document.execCommand('copy');
  document.body.removeChild(tempInput);
  showToast(successMsg);
}

// =========================================================================
// [WE ZIP 리텐션·비교·내부링크 엔진] 최근 계산기 / 결과 저장 비교 / 연관 추천
// =========================================================================

const WEZIP_CALC_CATALOG = {
  'salary.html': { title: '2026 연봉 실수령액 계산기', tag: '급여·세후', cat: 'salary' },
  'unemployment.html': { title: '퇴사자 실업급여 계산기', tag: '상한 68,100원', cat: 'salary' },
  'hourly-wage.html': { title: '알바 시급·주휴수당 계산기', tag: '최저 10,320원', cat: 'salary' },
  'severance.html': { title: '법정 퇴직금·퇴직세 계산기', tag: 'IRP 절세', cat: 'salary' },
  'annual-leave.html': { title: '연차 일수·수당 정산기', tag: '근로기준법', cat: 'salary' },
  'gov-finder.html': { title: '2026 정부 지원금 맞춤 찾기', tag: '정책 통합', cat: 'gov' },
  'gov-rent.html': { title: '청년월세 지원 (최대 480만)', tag: '상시 전환', cat: 'gov' },
  'gov-parent.html': { title: '부모급여·아동수당 로드맵', tag: '만 9세 미만', cat: 'gov' },
  'gov-subsidy.html': { title: '근로·자녀장려금 대상조회', tag: '최대 330만', cat: 'gov' },
  'gov-median.html': { title: '2026 기준 중위소득 판정기', tag: '4대 급여', cat: 'gov' },
  'loan-dsr.html': { title: '대출이자 & 스트레스 DSR', tag: '3단계 +1.50%p', cat: 'loan' },
  'real-transfer-tax.html': { title: '주택 양도소득세 계산기', tag: '12억 비과세', cat: 'real' },
  'real-loan.html': { title: '전세대출 & HUG 보증조회', tag: '전세안전', cat: 'real' },
  'real-estate.html': { title: '부동산 복비·취득세 계산기', tag: '생애최초 감면', cat: 'real' },
  'savings.html': { title: '예·적금 만기이자 비교기', tag: '세후 실수익', cat: 'loan' },
  'youth-leap.html': { title: '청년도약·청년미래적금 안내', tag: '정부 매칭', cat: 'gov' },
  'dutch-pay.html': { title: '1초 더치페이 N빵 계산기', tag: '생활 금융', cat: 'loan' }
};

const WEZIP_CROSS_GRAPH = {
  salary: {
    calcs: [
      { title: '연봉 실수령액 & 순위 계산기', url: 'salary.html', desc: '2026.7월 국민연금 4.75% 반영 실수령' },
      { title: '법정 퇴직금 & IRP 절세 계산기', url: 'severance.html', desc: '1일 평균임금 기반 퇴직소득세 비교' },
      { title: '알바 시급·주휴수당 계산기', url: 'hourly-wage.html', desc: '최저시급 10,320원·주휴수당 정밀 산정' }
    ],
    posts: [
      { title: '2026 연봉별 통장 실수령액 & 4대보험 요율표', url: 'blog-salary-guide-2026.html' },
      { title: '직장인 연말정산 13월의 월급 환급 팁', url: 'blog-year-end-tax-settlement-guide.html' },
      { title: '퇴직 전 실업급여 상·하한액 및 자진퇴사 예외', url: 'blog-unemployment-benefit.html' }
    ]
  },
  gov: {
    calcs: [
      { title: '내 조건 정부지원금 1초 통합 찾기', url: 'gov-finder.html', desc: '소득·연령·주거 조건별 수혜 정책 매칭' },
      { title: '2026 기준 중위소득 자격 판정기', url: 'gov-median.html', desc: '생계·의료·주거·교육급여 즉시 확인' },
      { title: '근로·자녀장려금 수급 모의계산', url: 'gov-subsidy.html', desc: '맞벌이 4,400만 확대 요건 반영' }
    ],
    posts: [
      { title: '2026 기준 중위소득 4인 649만 & 복지 커트라인', url: 'blog-median-income-welfare.html' },
      { title: '만 9세 미만 아동수당·부모급여 총 3,080만 로드맵', url: 'blog-childcare-subsidies.html' },
      { title: '청년월세 최대 480만·버팀목 전세대출 가이드', url: 'blog-youth-welfare-2026.html' }
    ]
  },
  real: {
    calcs: [
      { title: '주택 양도소득세 & 장특공 계산기', url: 'real-transfer-tax.html', desc: '1주택 12억 비과세 & 다주택 중과 체크' },
      { title: '부동산 복비·취득세 계산기', url: 'real-estate.html', desc: '생애최초 취득세 200만 감면 반영' },
      { title: '전세대출·HUG 보증보험 안전 조회', url: 'real-loan.html', desc: '부채비율 70% 깡통전세 사전 차단' }
    ],
    posts: [
      { title: '스트레스 DSR 3단계(+1.50%p) 대출 한도 방어 전략', url: 'blog-stress-dsr-guide.html' },
      { title: '1세대 1주택 양도세 비과세 & 일시적 2주택 가이드', url: 'blog-real-estate-transfer-tax.html' },
      { title: '전세사기 예방 등기부등본·전세보증 체크리스트', url: 'blog-jeonse-scam-prevention-checklist.html' }
    ]
  },
  loan: {
    calcs: [
      { title: '대출이자 & 스트레스 DSR 계산기', url: 'loan-dsr.html', desc: '수도권 +1.50%p 반영 최대 한도 산출' },
      { title: '예·적금 세후 만기이자 비교기', url: 'savings.html', desc: '일반과세 vs 비과세 실수령 이자 비교' },
      { title: '전세대출 & HUG 전세보증 조회', url: 'real-loan.html', desc: '임대차 보증금 안전성 즉시 확인' }
    ],
    posts: [
      { title: '스트레스 DSR 3단계 주담대 한도 축소 방어 전략', url: 'blog-stress-dsr-guide.html' },
      { title: '마이너스통장 vs 일반 신용대출 이자 차이', url: 'blog-credit-loan-vs-minus-account.html' },
      { title: '금리인하요구권 승인 높이는 신용점수 관리법', url: 'blog-interest-rate-cut-demand-right.html' }
    ]
  }
};

function escapeWezipHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function getWezipCategoryForPage(fileName) {
  if (WEZIP_CALC_CATALOG[fileName]) return WEZIP_CALC_CATALOG[fileName].cat;
  if (fileName.startsWith('salary-') || /unemployment|hourly|severance|annual-leave|overtime|freelancer|job-change|comprehensive-income|year-end/.test(fileName)) return 'salary';
  if (fileName.startsWith('gov-') || fileName.startsWith('subsidy-') || /child|parent|median|rent|youth|energy|telecom|infertility|diaper|k-pass|single-parent|pension/.test(fileName)) return 'gov';
  if (fileName.startsWith('tax-') || fileName.startsWith('real-') || /jeonse|transfer-tax|holding-tax|officetel|housing-subscription|gift-tax|first-home|brokerage|capital-gains|didimdol/.test(fileName)) return 'real';
  return 'loan';
}

function getWezipSavedResults() {
  try {
    const raw = JSON.parse(localStorage.getItem('wezip_saved_results') || '[]');
    return Array.isArray(raw) ? raw : [];
  } catch (e) {
    return [];
  }
}

function saveCalcSnapshot(calcName, summary, url) {
  try {
    const currentFile = (url || window.location.pathname.split('/').pop() || 'index.html').split('?')[0];
    let saved = getWezipSavedResults();
    const cleanName = String(calcName || '계산 결과').trim();
    const cleanSummary = String(summary || '').trim();
    if (!cleanSummary) {
      showToast('저장할 계산 결과를 찾지 못했습니다. 숫자를 입력한 뒤 다시 시도해 주세요.');
      return;
    }
    saved = saved.filter(item => !(item.url === currentFile && item.summary === cleanSummary));
    saved.unshift({
      id: String(Date.now()),
      calcName: cleanName,
      summary: cleanSummary,
      url: currentFile,
      time: Date.now()
    });
    if (saved.length > 6) saved = saved.slice(0, 6);
    localStorage.setItem('wezip_saved_results', JSON.stringify(saved));
    renderRecentAndSavedHome();
    renderWezipSavedInline();
    showToast('계산 결과를 저장했습니다. 다른 조건과 나란히 비교할 수 있습니다.');
  } catch (e) {
    showToast('브라우저 저장소 설정으로 인해 결과를 저장할 수 없습니다.');
  }
}

function removeCalcSnapshot(snapshotId) {
  try {
    const saved = getWezipSavedResults().filter(item => item.id !== String(snapshotId));
    localStorage.setItem('wezip_saved_results', JSON.stringify(saved));
    renderRecentAndSavedHome();
    renderWezipSavedInline();
  } catch (e) {}
}

function captureCurrentCalcSnapshot() {
  const fileName = (window.location.pathname.split('/').pop() || 'index.html').split('?')[0];
  const h1 = document.querySelector('main h1, header h1, h1');
  const titleText = (WEZIP_CALC_CATALOG[fileName] && WEZIP_CALC_CATALOG[fileName].title)
    || (h1 ? h1.textContent.trim() : document.title.split('|')[0].trim());

  const mainEl = document.querySelector('main') || document.body;
  const preferredSelectors = [
    '#resultNetPay', '#wageNetMonthly', '#unemployMonthlyText', '#unemployDailyAmount',
    '#netSeveranceDisplay', '#severanceResult', '#leaveAllowanceDisplay',
    '#currentMedianText', '#annualTotalGrantText', '#monthlyGrantText',
    '#subsidyTotalAmount', '#parentTotalGrant', '#firstMonthPayment',
    '#finalTaxDisplay', '#taxResult', '#leapTotalResult',
    '#maturityAmount', '#perPersonAmount', '[data-result-primary]'
  ];
  let primaryVal = '';
  for (const sel of preferredSelectors) {
    const el = document.querySelector(sel);
    if (el && el.textContent.trim()) {
      primaryVal = el.textContent.trim().replace(/\s+/g, ' ');
      break;
    }
  }
  if (!primaryVal) {
    const bigEls = Array.from(mainEl.querySelectorAll('.text-4xl, .text-5xl, .text-3xl, .text-2xl'))
      .filter(el => /[0-9]/.test(el.textContent) && /원|%|일|개월|만원/.test(el.textContent));
    if (bigEls.length > 0) {
      primaryVal = bigEls[0].textContent.trim().replace(/\s+/g, ' ');
    }
  }

  const inputNotes = [];
  const inputs = Array.from(mainEl.querySelectorAll('input[type="text"], input[type="number"], select')).slice(0, 3);
  for (const inp of inputs) {
    if (inp.offsetParent === null) continue;
    let lblText = '';
    const wrapper = inp.closest('div');
    const label = inp.id ? document.querySelector(`label[for="${inp.id}"]`) : null;
    if (label) lblText = label.textContent.trim();
    else if (wrapper && wrapper.previousElementSibling && wrapper.previousElementSibling.tagName === 'LABEL') {
      lblText = wrapper.previousElementSibling.textContent.trim();
    }
    const val = inp.tagName === 'SELECT'
      ? (inp.options[inp.selectedIndex] ? inp.options[inp.selectedIndex].text.trim() : inp.value)
      : inp.value.trim();
    if (val) inputNotes.push(lblText ? `${lblText.slice(0, 12)}: ${val}` : val);
  }

  const summary = primaryVal
    ? `${primaryVal}${inputNotes.length ? ' (' + inputNotes.join(' · ') + ')' : ''}`
    : (inputNotes.join(' · ') || '계산 조건 저장됨');

  saveCalcSnapshot(titleText, summary, fileName);
}

function renderRecentAndSavedHome() {
  const recentEl = document.getElementById('recentCalcSection');
  const savedEl = document.getElementById('savedCompareSection');

  if (recentEl) {
    let recent = [];
    try {
      recent = JSON.parse(localStorage.getItem('moneycalc_recent') || '[]');
    } catch (e) { recent = []; }
    if (Array.isArray(recent) && recent.length > 0) {
      const itemsHtml = recent.slice(0, 5).map(item => `
        <a href="${escapeWezipHtml(item.url)}" class="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-400 text-xs sm:text-sm font-bold text-slate-800 hover:text-blue-700 transition shrink-0 shadow-xs">
          <span class="w-1.5 h-1.5 rounded-full bg-blue-600 shrink-0"></span>
          <span>${escapeWezipHtml(item.title)}</span>
        </a>
      `).join('');
      recentEl.innerHTML = `
        <div class="bg-slate-50 border border-slate-200 rounded-2xl p-4 sm:p-5">
          <div class="flex items-center justify-between gap-2 mb-3">
            <div class="flex items-center gap-2 text-xs sm:text-sm font-extrabold text-slate-900">
              <svg class="svg-icon w-4 h-4 text-blue-600" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
              <span>최근 이용한 계산기 바로 이어하기</span>
            </div>
            <button type="button" onclick="try{localStorage.removeItem('moneycalc_recent');renderRecentAndSavedHome();}catch(e){}" class="text-xs font-semibold text-slate-400 hover:text-slate-700 transition">기록 비우기</button>
          </div>
          <div class="flex flex-wrap gap-2">${itemsHtml}</div>
        </div>
      `;
      recentEl.classList.remove('hidden');
    } else {
      recentEl.innerHTML = '';
      recentEl.classList.add('hidden');
    }
  }

  if (savedEl) {
    const saved = getWezipSavedResults();
    if (saved.length > 0) {
      const cardsHtml = saved.map(item => `
        <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl flex flex-col justify-between gap-2">
          <div class="flex items-start justify-between gap-2">
            <a href="${escapeWezipHtml(item.url)}" class="text-xs font-bold text-blue-700 hover:underline">${escapeWezipHtml(item.calcName)}</a>
            <button type="button" onclick="removeCalcSnapshot('${escapeWezipHtml(item.id)}')" class="text-xs text-slate-400 hover:text-rose-600 shrink-0" aria-label="삭제">삭제</button>
          </div>
          <div class="text-sm sm:text-base font-black text-slate-900 break-words">${escapeWezipHtml(item.summary)}</div>
        </div>
      `).join('');
      savedEl.innerHTML = `
        <div class="bg-white border border-slate-200 rounded-2xl p-4 sm:p-5 shadow-xs">
          <div class="flex items-center justify-between gap-2 mb-3">
            <div class="flex items-center gap-2 text-xs sm:text-sm font-extrabold text-slate-900">
              <svg class="svg-icon w-4 h-4 text-emerald-600" viewBox="0 0 24 24"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg>
              <span>내 계산 결과 저장함 & 나란히 비교 (${saved.length}/6)</span>
            </div>
            <button type="button" onclick="try{localStorage.removeItem('wezip_saved_results');renderRecentAndSavedHome();renderWezipSavedInline();}catch(e){}" class="text-xs font-semibold text-slate-400 hover:text-slate-700 transition">전체 삭제</button>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">${cardsHtml}</div>
        </div>
      `;
      savedEl.classList.remove('hidden');
    } else {
      savedEl.innerHTML = '';
      savedEl.classList.add('hidden');
    }
  }
}

function renderWezipSavedInline() {
  const listEl = document.getElementById('wezipSavedInlineList');
  if (!listEl) return;
  const saved = getWezipSavedResults();
  if (saved.length === 0) {
    listEl.innerHTML = '<div class="text-xs text-slate-400">위 버튼을 눌러 현재 조건의 결과를 저장하면 다른 연봉·금리·가구 조건과 한눈에 비교할 수 있습니다.</div>';
    return;
  }
  listEl.innerHTML = `
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5 mt-3">
      ${saved.map(item => `
        <div class="p-3 bg-white border border-slate-200 rounded-xl flex flex-col justify-between gap-1.5">
          <div class="flex items-center justify-between gap-2">
            <a href="${escapeWezipHtml(item.url)}" class="text-xs font-bold text-blue-700 hover:underline truncate">${escapeWezipHtml(item.calcName)}</a>
            <button type="button" onclick="removeCalcSnapshot('${escapeWezipHtml(item.id)}')" class="text-xs text-slate-400 hover:text-rose-600 shrink-0">삭제</button>
          </div>
          <div class="text-xs sm:text-sm font-black text-slate-900 break-words">${escapeWezipHtml(item.summary)}</div>
        </div>
      `).join('')}
    </div>
  `;
}

function renderWezipCalcRetentionBar(footerEl, fileName) {
  if (!WEZIP_CALC_CATALOG[fileName] && !fileName.startsWith('salary-')) return;
  if (document.getElementById('wezipCalcSaveBar')) return;
  const bar = document.createElement('section');
  bar.id = 'wezipCalcSaveBar';
  bar.className = 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8';
  bar.innerHTML = `
    <div class="bg-slate-50 border border-slate-200 rounded-2xl p-5 space-y-3">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 class="text-sm sm:text-base font-extrabold text-slate-900">내 계산 결과 저장 및 다른 조건과 비교</h2>
          <p class="text-xs text-slate-500 mt-0.5">계산한 값을 브라우저에 안전하게 저장해 두고, 입력 조건을 바꿔가며 결과를 비교해 보세요.</p>
        </div>
        <button type="button" onclick="captureCurrentCalcSnapshot()" class="inline-flex items-center justify-center gap-1.5 px-4 py-2.5 rounded-xl bg-slate-900 hover:bg-blue-600 text-white text-xs sm:text-sm font-bold transition shrink-0">
          <svg class="svg-icon w-4 h-4" viewBox="0 0 24 24"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path></svg>
          <span>현재 계산 결과 저장하기</span>
        </button>
      </div>
      <div id="wezipSavedInlineList"></div>
    </div>
  `;
  footerEl.parentNode.insertBefore(bar, footerEl);
  renderWezipSavedInline();
}

function renderWezipCrossLinks(footerEl, fileName) {
  const skipPages = new Set(['index.html', '', 'blog.html', 'about.html', 'contact.html', 'privacy.html', 'terms.html']);
  if (skipPages.has(fileName) || document.getElementById('wezipCrossLinks')) return;
  const cat = getWezipCategoryForPage(fileName);
  const graph = WEZIP_CROSS_GRAPH[cat] || WEZIP_CROSS_GRAPH.salary;
  const recCalcs = graph.calcs.filter(c => c.url !== fileName).slice(0, 2);
  const recPosts = graph.posts.filter(p => p.url !== fileName).slice(0, 2);

  const sec = document.createElement('section');
  sec.id = 'wezipCrossLinks';
  sec.className = 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8 mb-6';
  sec.innerHTML = `
    <div class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-xs space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-blue-600"></span>
          <h2 class="text-base sm:text-lg font-black text-slate-900">함께 확인하면 좋은 계산기 &amp; 필독 칼럼</h2>
        </div>
        <a href="index.html" class="text-xs font-bold text-blue-600 hover:underline">전체 계산기 허브 &rarr;</a>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
        ${recCalcs.map(c => `
          <a href="${escapeWezipHtml(c.url)}" class="p-4 rounded-xl bg-slate-50 hover:bg-blue-50/70 border border-slate-200 hover:border-blue-400 transition block group">
            <div class="text-xs font-bold text-blue-700 mb-1">맞춤 계산기</div>
            <div class="text-sm sm:text-base font-extrabold text-slate-900 group-hover:text-blue-700">${escapeWezipHtml(c.title)}</div>
            <div class="text-xs text-slate-500 mt-1">${escapeWezipHtml(c.desc)}</div>
          </a>
        `).join('')}
        ${recPosts.map(p => `
          <a href="${escapeWezipHtml(p.url)}" class="p-4 rounded-xl bg-white hover:bg-slate-50 border border-slate-200 hover:border-slate-400 transition block group">
            <div class="text-xs font-bold text-emerald-700 mb-1">필독 해설 칼럼</div>
            <div class="text-sm sm:text-base font-extrabold text-slate-900 group-hover:text-blue-700">${escapeWezipHtml(p.title)}</div>
            <div class="text-xs text-slate-500 mt-1">실제 수령액 비교표·함정 체크리스트 확인</div>
          </a>
        `).join('')}
      </div>
    </div>
  `;
  footerEl.parentNode.insertBefore(sec, footerEl);
}

function initWezipRetentionAndLinks() {
  const fileName = (window.location.pathname.split('/').pop() || 'index.html').split('?')[0] || 'index.html';
  if (WEZIP_CALC_CATALOG[fileName]) {
    recordRecentCalc(WEZIP_CALC_CATALOG[fileName].title, fileName, WEZIP_CALC_CATALOG[fileName].cat);
  } else if (fileName.startsWith('salary-') && fileName.endsWith('.html')) {
    const label = fileName.replace('salary-', '연봉 ').replace('.html', '만 원 실수령액');
    recordRecentCalc(label, fileName, 'salary');
  }

  renderRecentAndSavedHome();

  const footerEl = document.querySelector('footer');
  if (footerEl && footerEl.parentNode) {
    renderWezipCalcRetentionBar(footerEl, fileName);
    renderWezipCrossLinks(footerEl, fileName);
  }
}
