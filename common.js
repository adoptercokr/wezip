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
    initWezipSearchIntentRouter();
  });
} else {
  initGA4();
  initVisitorCounter();
  initWezipRetentionAndLinks();
    initWezipSearchIntentRouter();
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

function renderWezipPolicyRadar(footerEl, fileName, todayDot) {
  const skipPages = new Set(['index.html', '', 'about.html', 'contact.html', 'privacy.html', 'terms.html']);
  if (skipPages.has(fileName) || document.getElementById('wezipPolicyRadar')) return;

  const cat = getWezipCategoryForPage(fileName);
  const radarData = {
    salary: {
      title: '2026 급여·세무·사업주 인건비 핵심 기준 및 숨은 지원금',
      items: [
        { badge: '법정시급·주휴', name: '2026 법정 최저시급 10,320원 & 주휴수당', desc: '주 15시간 이상 근무 시 주휴수당 의무 발생 (주 40시간 월 환산 2,156,880원 / 미지급 시 임금체불)', url: 'hourly-wage.html' },
        { badge: '4대보험 개편', name: '국민연금 4.75% · 건강보험 3.595% · 장기요양 13.14%', desc: '2026.7월 연금개혁 근로자 부담분 4.75% 및 비과세 식대 월 20만 원 한도 비과세 공제 적용', url: 'salary.html' },
        { badge: '사업주·근로자', name: '두루누리 사회보험료 80% 지원 & 청년일자리도약장려금', desc: '10인 미만 사업장 연금·고용보험 80% 국비 지원 / 청년 정규직 채용 시 사업주 연 최대 720만 원 지급', url: 'gov-finder.html' },
        { badge: '구직·퇴직보호', name: '실업급여 1일 상한 68,100원 / 하한 66,048원', desc: '퇴직 전 18개월 중 피보험단위기간 180일 이상 충족 시 연령·가입기간별 120~270일 비과세 지급', url: 'unemployment.html' }
      ]
    },
    gov: {
      title: '2026 개인·가구 복지 & 소상공인·사업자 핵심 지원금 브리핑',
      items: [
        { badge: '소상공인 특화', name: '소상공인 정책자금 5,000만 · 스마트상점 1,500만 · 철거비 400만', desc: '저금리 대환·경영안정자금, 키오스크·서빙로봇 70% 보조, 희망리턴패키지 폐업철거비·재창업 2,000만 원', url: 'gov-finder.html' },
        { badge: '출산·양육 확대', name: '부모급여(월 100/50만) + 아동수당 만 9세 미만 확대', desc: '첫만남이용권 200~300만 원, 만 0세 월 100만·1세 50만 원, 만 9세(107개월) 미만 아동수당 월 10만 원+', url: 'gov-parent.html' },
        { badge: '근로·자녀장려금', name: '근로장려금 최대 330만 원 & 맞벌이 상한 4,400만 원', desc: '맞벌이 가구 소득 상한 4,400만 원 확대, 자녀장려금 부부합산 7,000만 원 미만 자녀당 최대 100만 원', url: 'gov-subsidy.html' },
        { badge: '중위소득 역대최대', name: '2026 기준 중위소득 4인 6,494,738원 (1인 2,564,238원)', desc: '생계급여(32%·4인 최대 207.8만), 의료급여(40%), 주거급여(48%), 교육급여(50%) 수급 커트라인 상향', url: 'gov-median.html' }
      ]
    },
    real: {
      title: '2026 부동산 세제·전월세 지원·정책 모기지 최신 기준',
      items: [
        { badge: '양도세 비과세', name: '1세대 1주택 고가주택 기준 12억 원 & 장기보유특별공제 MAX 80%', desc: '실거래가 12억 이하 비과세(2년 보유·조정지역 2년 거주) 및 10년 보유·거주 시 최대 80% 공제', url: 'real-transfer-tax.html' },
        { badge: '취득세 감면', name: '생애최초 주택구입 취득세 최대 200만 원 면제·감면', desc: '소득 제한 없이 실거래가 12억 원 이하 생애최초 주택 취득 시 산출 취득세에서 최대 200만 원 감면', url: 'real-estate.html' },
        { badge: '전세안전·대출', name: '신생아 특례(최저 1.6%) · 청년 버팀목 · HUG 반환보증료 30만 환급', desc: '출산 가구 최대 5억 저리 대출, 무주택 청년 전세대출 2억 및 보증보험료 최대 30만 원 현금 환급', url: 'real-loan.html' },
        { badge: '주거비 현금지원', name: '청년월세 특별지원 상시 전환 (월 20만 원 × 24개월 = 480만 원)', desc: '만 19~34세 무주택 청년(중위 60% 이하)에게 최대 480만 원 현금 지급 및 월세 세액공제 15~17%', url: 'gov-rent.html' }
      ]
    },
    loan: {
      title: '2026 대출 한도 규제(DSR 3단계) · 정책 금융 · 절세 적금 기준',
      items: [
        { badge: 'DSR 3단계 시행', name: '스트레스 DSR 3단계 수도권 +1.50%p / 지방 +0.75%p 가산', desc: '전 금융권 주담대·신용대출 한도 산정 시 스트레스 가산금리 의무 반영 (주기형·혼합형 우대 적용)', url: 'loan-dsr.html' },
        { badge: '청년 목돈마련', name: '청년도약계좌 기여금 매칭 확대 & 2026 청년미래적금(3년)', desc: '전 구간 월 70만 원 매칭 한도 확대(월 최대 3.3만 원 기여금) + 이자소득세 15.4% 전액 비과세', url: 'youth-leap.html' },
        { badge: '소상공인 금융', name: '소상공인 저금리 대환대출(7%→4.5%) & 지자체 이차보전(2~3.5%p)', desc: '고금리 사업자대출 대환, 지역신보 특례보증, 새출발기금 부실차주 원금 60~80% 감면 지원', url: 'gov-finder.html' },
        { badge: '이자소득 절세', name: '일반과세(15.4%) vs 세금우대·비과세 예적금 만기 실수령 비교', desc: '단리·복리 이자 산출 및 비과세 종합저축·상호금융 출자금 활용 시 세후 순이자 수익 비교', url: 'savings.html' }
      ]
    }
  };

  const data = radarData[cat] || radarData.gov;
  const sec = document.createElement('section');
  sec.id = 'wezipPolicyRadar';
  sec.className = 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8';
  sec.innerHTML = `
    <div class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-xs space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-blue-600"></span>
          <h2 class="text-base sm:text-lg font-black text-slate-900">${escapeWezipHtml(data.title)}</h2>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-[11px] font-bold text-slate-500 bg-slate-100 px-2.5 py-1 rounded-full border border-slate-200">기준 업데이트 <strong class="text-slate-800">${escapeWezipHtml(todayDot)}</strong></span>
          <a href="gov-finder.html" class="text-xs font-bold text-blue-600 hover:underline">전체 지원금 찾기 &rarr;</a>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
        ${data.items.map(item => `
          <a href="${escapeWezipHtml(item.url)}" class="p-4 rounded-xl bg-slate-50/80 hover:bg-blue-50/50 border border-slate-200/90 hover:border-blue-400 transition block group space-y-1.5">
            <div class="flex items-center justify-between gap-2">
              <span class="text-[11px] font-extrabold text-blue-700 bg-blue-50 border border-blue-200 px-2 py-0.5 rounded">${escapeWezipHtml(item.badge)}</span>
              <span class="text-[11px] font-bold text-slate-400 group-hover:text-blue-600">계산·조회 &rarr;</span>
            </div>
            <div class="text-sm font-extrabold text-slate-900 group-hover:text-blue-700">${escapeWezipHtml(item.name)}</div>
            <p class="text-xs text-slate-600 leading-relaxed">${escapeWezipHtml(item.desc)}</p>
          </a>
        `).join('')}
      </div>
    </div>
  `;
  footerEl.parentNode.insertBefore(sec, footerEl);
}

function syncWezipUpdatedDateBadges() {
  const kstNow = new Date(Date.now() + 9 * 60 * 60 * 1000);
  const todayDot = kstNow.toISOString().slice(0, 10).replace(/-/g, '.');
  document.querySelectorAll('[data-wezip-updated]').forEach(el => {
    const cur = (el.textContent || '').trim();
    if (!cur || cur < todayDot) {
      el.textContent = todayDot;
    }
  });
  return todayDot;
}

function initWezipRetentionAndLinks() {
  const todayDot = syncWezipUpdatedDateBadges();
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
    renderWezipPolicyRadar(footerEl, fileName, todayDot);
    renderWezipCrossLinks(footerEl, fileName);
  }
}


// ==============================================================================
// 2026 실시간 검색어 인텐트 라우터 (Search Intent & Direct Landing Engine)
// 네이버·구글 실제 검색량 기반 160대 고빈도 검색어 매핑
// ==============================================================================
const WEZIP_SEARCH_INTENT_MAP = [
  {
    targetUrl: 'salary.html',
    title: '2026 연봉·급여 실수령액 계산기',
    badge: '급여·연봉 1위',
    keywords: [
      '급여계산', '급여계산기', '연봉계산', '연봉계산기', '월급계산', '월급계산기', '실수령액', '실수령액계산기',
      '월급실수령액', '연봉실수령액', '2026연봉', '2026월급', '4대보험계산', '4대보험계산기', '국민연금계산',
      '건강보험료계산', '소득세계산', '근로소득세계산', '간이세액표', '식대비과세', '연봉세후', '월급세후', '세전세후',
      '연봉표', '월급표', '실수령액표', '실수령', '월급명세서', '급여명세서', '세후월급'
    ]
  },
  {
    targetUrl: 'tax-brokerage-fee-calc.html',
    title: '2026 부동산 복비·중개수수료 계산기',
    badge: '부동산 1위',
    keywords: [
      '복비', '복비계산', '복비계산기', '부동산복비', '부동산복비계산기', '중개수수료', '중개수수료계산기',
      '부동산중개수수료', '중개보수', '중개보수계산기', '아파트복비', '전세복비', '월세복비', '매매복비',
      '오피스텔복비', '상가복비', '공인중개사수수료', '복비요율', '중개수수료요율', '복비부가세',
      '부동산수수료', '집계약수수료', '부동산중개비', '부동산중개료'
    ]
  },
  {
    targetUrl: 'severance.html',
    title: '2026 퇴직금 및 퇴직소득세 계산기',
    badge: '퇴직금 1위',
    keywords: [
      '퇴직금', '퇴직금계산', '퇴직금계산기', '퇴직소득세', '퇴직소득세계산기', '퇴직금세금', '퇴직금계산법',
      '퇴직금지급기준', '퇴직금실수령액', '1년퇴직금', '알바퇴직금', '평균임금', '통상임금퇴직금', 'IRP퇴직금',
      '퇴직연금계산', '퇴직금조건', '퇴직금세율'
    ]
  },
  {
    targetUrl: 'unemployment.html',
    title: '2026 실업급여 모의계산기',
    badge: '실업급여 1위',
    keywords: [
      '실업급여', '실업급여계산', '실업급여계산기', '실업급여모의계산', '구직급여', '구직급여계산',
      '실업급여수급자격', '자진퇴사실업급여', '실업급여금액', '실업급여상한액', '조기재취업수당', '실업급여180일',
      '실업급여신청', '실업급여모의', '구직급여상한액'
    ]
  },
  {
    targetUrl: 'hourly-wage.html',
    title: '2026 시급·알바비·주휴수당 계산기',
    badge: '알바·시급 1위',
    keywords: [
      '시급', '시급계산', '시급계산기', '알바비', '알바비계산', '알바비계산기', '최저시급', '최저임금',
      '2026최저시급', '주휴수당', '주휴수당계산', '주휴수당계산기', '야간수당', '연장수당', '알바실수령액', '주15시간',
      '최저시급계산', '시급실수령액', '알바월급'
    ]
  },
  {
    targetUrl: 'gov-rent.html',
    title: '2026 청년월세 특별지원 대상조회기 (월 20만원)',
    badge: '청년주거 1위',
    keywords: [
      '청년월세', '청년월세지원', '청년월세특별지원', '월세지원', '청년월세20만원', '청년월세조건',
      '청년월세신청', '청년월세자격', '복지로청년월세', '청년월세소득기준', '월세480만원', '청년주거지원',
      '월세지원금', '청년월세계산'
    ]
  },
  {
    targetUrl: 'gov-parent.html',
    title: '2026 부모급여·아동수당 통합 계산기',
    badge: '출산복지 1위',
    keywords: [
      '부모급여', '부모급여계산', '부모급여신청', '부모급여100만원', '아동수당', '아동수당신청', '아동수당10만원',
      '첫만남이용권', '출산지원금', '출산축하금', '육아수당', '어린이집부모급여', '부모급여차액', '양육수당',
      '출산바우처', '아동수당나이'
    ]
  },
  {
    targetUrl: 'youth-leap.html',
    title: '2026 청년도약계좌 만기 모의 계산기',
    badge: '청년금융 1위',
    keywords: [
      '청년도약계좌', '청년도약', '도약계좌', '청년도약계좌계산기', '청년도약계좌조건', '청년도약계좌신청',
      '청년도약계좌기여금', '청년도약계좌만기', '청년미래적금', '도약계좌5000', '청년적금', '도약계좌금리'
    ]
  },
  {
    targetUrl: 'gov-subsidy.html',
    title: '2026 국세청 근로장려금·자녀장려금 계산기',
    badge: '국세청 환급 1위',
    keywords: [
      '근로장려금', '근로장려금계산', '근로장려금계산기', '근로장려금신청', '근로장려금자격', '근로장려금지급일',
      '근로장려금소득기준', '자녀장려금', '자녀장려금계산', '자녀장려금신청', '홈택스장려금', '장려금신청자격',
      '근로장려금재산'
    ]
  },
  {
    targetUrl: 'gov-median.html',
    title: '2026 가구원수별 기준 중위소득 판정기',
    badge: '복지기준 1위',
    keywords: [
      '기준중위소득', '중위소득', '중위소득계산', '중위소득100', '중위소득60', '중위소득50', '중위소득150',
      '생계급여기준', '의료급여기준', '주거급여기준', '소득인정액', '4인가구중위소득', '1인가구중위소득', '중위소득기준표'
    ]
  },
  {
    targetUrl: 'gov-finder.html?category=business',
    title: '2026 소상공인·자영업자 45대 특화 지원금 총람',
    badge: '사업자 특화 1위',
    keywords: [
      '소상공인정책자금', '소상공인지원금', '자영업자지원금', '개인사업자지원금', '사업자지원금',
      '소상공인대출', '소상공인저금리', '소상공인대환대출', '소상공인대환', '희망리턴패키지',
      '점포철거비', '점포철거비지원', '스마트상점', '스마트상점기술보급', '키오스크지원',
      '테이블오더지원', '소상공인전기요금', '전기요금특별지원', '노란우산공제', '소상공인부채경감',
      '새출발기금', '신용보증재단대출', '중소기업정책자금', '소상공인창업자금', '소진공대출'
    ]
  },
  {
    targetUrl: 'gov-finder.html',
    title: '2026 대한민국 100대 정부지원금 실시간 매칭',
    badge: '정부지원금 1위',
    keywords: [
      '정부지원금', '정부지원금찾기', '지원금찾기', '지원금조회', '보조금', '보조금24', '숨은정부지원금',
      '소상공인지원금', '소상공인정책자금', '점포철거비', '소상공인전기요금', '희망리턴패키지', '스마트상점',
      '국가지원금', '지원금모의계산'
    ]
  },
  {
    targetUrl: 'loan-dsr.html',
    title: '2026 스트레스 DSR 대출한도 계산기',
    badge: '대출한도 1위',
    keywords: [
      'dsr', 'dsr계산', 'dsr계산기', '스트레스dsr', '대출한도', '대출한도계산', '대출한도계산기',
      '주담대한도', '신용대출dsr', 'dti계산기', '원리금균등상환', '주택담보대출한도'
    ]
  },
  {
    targetUrl: 'tax-jeonse-to-monthly-calc.html',
    title: '2026 전월세 전환율 및 월세 계산기',
    badge: '임대차 1위',
    keywords: [
      '전월세전환', '전월세전환율', '전세월세전환', '전월세계산기', '보증금증액', '월세전환',
      '계약갱신청구권5', '임대차3법', '전세월세계산'
    ]
  },
  {
    targetUrl: 'real-transfer-tax.html',
    title: '2026 부동산 취득세·양도소득세 계산기',
    badge: '부동산세금 1위',
    keywords: [
      '취득세', '취득세계산', '취득세계산기', '부동산취득세', '아파트취득세', '생애최초취득세',
      '양도세', '양도소득세', '양도소득세계산기', '1가구1주택비과세', '다주택자중과', '부동산세금'
    ]
  },
  {
    targetUrl: 'annual-leave.html',
    title: '2026 미사용 연차수당 및 연차 계산기',
    badge: '근로기준법 1위',
    keywords: [
      '연차', '연차계산', '연차계산기', '연차수당', '연차수당계산', '연차수당계산기', '미사용연차수당',
      '1년미만연차', '연차발생기준', '통상임금연차', '연차정산'
    ]
  },
  {
    targetUrl: 'savings.html',
    title: '2026 예적금 이자 및 복리 계산기',
    badge: '예적금 1위',
    keywords: [
      '적금이자계산', '적금이자계산기', '예금이자계산', '예금이자계산기', '복리계산', '복리계산기',
      '이자소득세', '적금이자', '예금이자', '예적금계산기'
    ]
  }
];

// 검색어 인텐트 매칭 유틸리티
function findMatchingIntent(query) {
  if (!query) return null;
  const cleanQ = query.toString().trim().toLowerCase().replace(/\s+/g, '');
  if (cleanQ.length < 2) return null;

  for (const item of WEZIP_SEARCH_INTENT_MAP) {
    for (const kw of item.keywords) {
      const cleanKw = kw.toLowerCase().replace(/\s+/g, '');
      if (cleanQ.includes(cleanKw) || cleanKw.includes(cleanQ)) {
        return item;
      }
    }
  }
  return null;
}

// URL 쿼리 파라미터(?q=... 또는 ?search=...) 기반 스마트 유입 라우터
function initWezipUrlQueryRouter() {
  const params = new URLSearchParams(window.location.search);
  const q = params.get('q') || params.get('query') || params.get('search') || params.get('keyword');
  if (!q) return;

  const currentFile = (window.location.pathname.split('/').pop() || 'index.html').split('?')[0] || 'index.html';
  const match = findMatchingIntent(q);

  const targetPath = match ? match.targetUrl.split('?')[0] : '';
  const currentSearch = window.location.search;
  const isExactCurrent = match && (match.targetUrl === currentFile || (targetPath === currentFile && (!match.targetUrl.includes('?') || currentSearch.includes('category=business'))));

  if (match && !isExactCurrent) {
    // 세련된 토스 스타일의 다이렉트 이동 안내 배너 팝업
    const banner = document.createElement('div');
    banner.id = 'wezipIntentBanner';
    banner.className = 'fixed top-16 sm:top-20 left-1/2 -translate-x-1/2 z-50 bg-slate-900/95 text-white border border-blue-500/50 shadow-2xl rounded-2xl p-4 sm:p-5 flex items-center justify-between gap-3 sm:gap-4 max-w-md w-[92%] backdrop-blur-md transition-all duration-300';
    banner.innerHTML = `
      <div class="flex items-center gap-3 min-w-0">
        <div class="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center shrink-0 text-white shadow-sm">
          <svg class="svg-icon w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        </div>
        <div class="min-w-0">
          <div class="text-[11px] text-blue-300 font-bold">'${decodeURIComponent(q)}' 검색 추천</div>
          <div class="text-xs sm:text-sm font-extrabold truncate text-white">${match.title}</div>
        </div>
      </div>
      <div class="flex items-center gap-1.5 shrink-0">
        <a href="${match.targetUrl}" class="px-3.5 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-black shadow-sm transition">
          바로가기 &rarr;
        </a>
        <button type="button" onclick="this.closest('#wezipIntentBanner').remove()" class="p-1.5 text-slate-400 hover:text-white transition text-xs" aria-label="닫기">
          ✕
        </button>
      </div>
    `;
    document.body.appendChild(banner);
  }
}

// 온페이지 검색창 실시간 스마트 가이드 위젯
function initOnPageSearchIntentGuides() {
  const searchInputs = [
    document.getElementById('calcSearchInput'),
    document.getElementById('boardSearchInput'),
    document.getElementById('policySearchInput')
  ].filter(Boolean);

  searchInputs.forEach(input => {
    // 퀵 점프 뱃지 컨테이너 생성
    const guideBox = document.createElement('div');
    guideBox.className = 'wezip-quick-jump-box hidden mt-2 p-3 bg-blue-50/90 border border-blue-200 rounded-xl flex items-center justify-between gap-2 text-xs transition-all';
    if (input.parentNode) {
      input.parentNode.appendChild(guideBox);
    }

    input.addEventListener('input', (e) => {
      const val = (e.target.value || '').trim();
      if (!val || val.length < 2) {
        guideBox.classList.add('hidden');
        guideBox.innerHTML = '';
        return;
      }

      const match = findMatchingIntent(val);
      const currentFile = (window.location.pathname.split('/').pop() || 'index.html').split('?')[0] || 'index.html';

      const targetPath = match ? match.targetUrl.split('?')[0] : '';
  const currentSearch = window.location.search;
  const isExactCurrent = match && (match.targetUrl === currentFile || (targetPath === currentFile && (!match.targetUrl.includes('?') || currentSearch.includes('category=business'))));

  if (match && !isExactCurrent) {
        guideBox.classList.remove('hidden');
        guideBox.innerHTML = `
          <div class="flex items-center gap-1.5 font-bold text-blue-900 truncate">
            <span class="px-1.5 py-0.5 rounded bg-blue-600 text-white text-[10px] shrink-0">${match.badge}</span>
            <span>전용 계산기:</span>
            <span class="underline underline-offset-2">${match.title}</span>
          </div>
          <a href="${match.targetUrl}" class="px-3 py-1 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs transition shrink-0 whitespace-nowrap shadow-xs">
            바로가기 &rarr;
          </a>
        `;
      } else {
        guideBox.classList.add('hidden');
        guideBox.innerHTML = '';
      }
    });
  });
}

// 통합 초기화 함수
function initWezipSearchIntentRouter() {
  initWezipUrlQueryRouter();
  initOnPageSearchIntentGuides();
}
