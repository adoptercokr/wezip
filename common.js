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
          <button type="button" id="modalKakaoShareBtn" class="w-full flex items-center justify-between p-3.5 rounded-xl bg-[#FEE500]/15 hover:bg-[#FEE500]/30 border border-[#FEE500]/40 transition text-left">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-lg bg-[#FEE500] text-slate-900 flex items-center justify-center shadow-sm font-bold text-xs">
                TALK
              </div>
              <div>
                <div class="font-bold text-sm text-slate-900">카카오톡 메시지 복사</div>
                <div class="text-xs text-slate-500">채팅방에 바로 붙여넣기</div>
              </div>
            </div>
            <span class="text-xs font-semibold text-amber-900 bg-[#FEE500] px-2.5 py-1 rounded-md">복사</span>
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
const WEZIP_GA4_ID = ''; // 예: 'G-XXXXXXXXXX' 입력 시 자동 활성화

function initGA4() {
  if (!WEZIP_GA4_ID || WEZIP_GA4_ID === 'G-XXXXXXXXXX') return;
  if (window.__ga4_initialized) return;
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

// DOM 준비 시 자동 초기화
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    initGA4();
    initVisitorCounter();
  });
} else {
  initGA4();
  initVisitorCounter();
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
