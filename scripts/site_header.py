# -*- coding: utf-8 -*-
"""
Shared canonical WE ZIP site header builder and repository-wide synchronizer.
Single source of truth for the global navigation bar across all HTML pages
and automated column publisher scripts.
"""

import glob
import os
import re


def get_active_section(filename):
    """Map an HTML filename to its top navigation section key."""
    base = os.path.basename(filename or "").lower()
    if base == "gov-finder.html":
        return "gov_finder"
    if base == "blog.html" or base.startswith("blog-"):
        return "blog"
    if (
        base in ("salary.html", "hourly-wage.html", "unemployment.html", "severance.html", "annual-leave.html")
        or base.startswith("salary-")
    ):
        return "salary"
    if base.startswith("real-") or base.startswith("tax-"):
        return "realestate"
    if base in ("gov-rent.html", "gov-parent.html", "gov-subsidy.html", "gov-median.html") or base.startswith("subsidy-"):
        return "welfare"
    if base in ("loan-dsr.html", "savings.html", "youth-leap.html", "dutch-pay.html"):
        return "finance"
    return "home"


def build_unified_header(filename="index.html", indent="    "):
    """Return the unified WE ZIP global header HTML with active section state."""
    sec = get_active_section(filename)

    gov_desktop_cls = (
        "bg-emerald-600 text-white border-emerald-400 shadow-xs"
        if sec == "gov_finder"
        else "text-emerald-300 hover:text-white hover:bg-slate-800 border-emerald-500/30"
    )
    gov_mobile_cls = (
        "bg-emerald-600 text-white border-emerald-400 shadow-xs"
        if sec == "gov_finder"
        else "bg-emerald-950/80 border-emerald-500/40 text-emerald-300 hover:text-white"
    )
    blog_cls = (
        "text-white bg-slate-800 font-bold"
        if sec == "blog"
        else "text-slate-200 hover:text-white hover:bg-slate-800"
    )
    sal_cls = (
        "text-white bg-slate-800"
        if sec == "salary"
        else "text-slate-200 hover:text-white hover:bg-slate-800"
    )
    re_cls = (
        "text-white bg-slate-800"
        if sec == "realestate"
        else "text-slate-200 hover:text-white hover:bg-slate-800"
    )
    wel_cls = (
        "text-white bg-slate-800"
        if sec == "welfare"
        else "text-slate-200 hover:text-white hover:bg-slate-800"
    )
    fin_cls = (
        "text-white bg-slate-800"
        if sec == "finance"
        else "text-slate-200 hover:text-white hover:bg-slate-800"
    )

    raw = f"""<!-- 포털 최상단 슬림 바: 로고, 로고 우측 주메뉴(PC), 지원금 찾기(모바일 상시), 모바일 메뉴 토글 -->
<header class="bg-[#1E293B] text-white sticky top-0 z-50 shadow-md select-none">
    <div class="max-w-6xl mx-auto px-3 sm:px-4 h-16 flex items-center justify-between gap-2">
        <!-- 좌측: 로고 + 주메뉴 (PC에서는 한 줄로 로고 바로 오른쪽에 배치) -->
        <div class="flex items-center gap-4 lg:gap-8 h-full">
            <a href="index.html" class="flex items-center gap-2 sm:gap-2.5 shrink-0 group" aria-label="WE ZIP 홈으로 이동">
                <div class="w-10 h-10 rounded-xl bg-blue-600 group-hover:bg-blue-500 flex items-center justify-center text-white shadow-sm transition">
                    <svg class="svg-icon w-5 h-5 text-white stroke-[2.2]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M3 9.5L12 3l9 6.5v10a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 19.5v-10z"></path>
                        <polyline points="9 21 9 12 15 12 15 21"></polyline>
                    </svg>
                </div>
                <div class="flex items-center gap-1.5">
                    <span class="font-black text-lg sm:text-xl tracking-tight text-white notranslate whitespace-nowrap" translate="no">WE <span class="text-blue-400">ZIP</span></span>
                    <span class="text-[11px] font-black text-emerald-300 px-1.5 sm:px-2 py-0.5 bg-emerald-950/70 rounded-full border border-emerald-500 shadow-sm whitespace-nowrap">100% 무료</span>
                </div>
            </a>

            <!-- PC 주메뉴 (로고 바로 오른쪽에 배치, 단일 가로행 유지 & whitespace-nowrap) -->
            <nav class="hidden md:flex items-center gap-0.5 lg:gap-1 xl:gap-2 h-full text-xs lg:text-sm font-bold whitespace-nowrap">
                <a href="gov-finder.html" class="whitespace-nowrap shrink-0 px-2 lg:px-2.5 py-1.5 rounded-lg {gov_desktop_cls} transition flex items-center gap-1 font-extrabold border">
                    <svg class="svg-icon w-3.5 h-3.5 text-emerald-400" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                    <span>지원금 찾기</span>
                </a>
                <a href="blog.html" class="whitespace-nowrap shrink-0 px-2 lg:px-2.5 py-1.5 rounded-lg {blog_cls} transition">금융 칼럼</a>

                <!-- 1. 급여·소득 -->
                <div class="relative group h-full flex items-center">
                    <button type="button" class="whitespace-nowrap shrink-0 px-2 lg:px-2.5 py-1.5 rounded-lg {sal_cls} transition flex items-center gap-1">
                        <span>급여·소득</span>
                        <svg class="svg-icon w-3 h-3 text-slate-400 group-hover:rotate-180 transition-transform" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
                    </button>
                    <div class="absolute left-0 top-full pt-1 hidden group-hover:block z-50 w-64 animate-in fade-in">
                        <div class="bg-white rounded-xl shadow-xl border border-slate-200 py-2 text-slate-800 text-sm font-medium">
                            <a href="salary.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span class="font-bold">연봉 계산기</span>
                                <span class="text-[11px] text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded font-bold">실수령액</span>
                            </a>
                            <a href="hourly-wage.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span>알바·최저시급 계산기</span>
                                <span class="text-[11px] text-slate-400">10,320원</span>
                            </a>
                            <a href="unemployment.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span class="font-bold">퇴사자 실업급여 계산기</span>
                                <span class="text-[11px] text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded font-bold">1일 68,100</span>
                            </a>
                            <a href="severance.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span>퇴직금 계산기</span>
                                <span class="text-[11px] text-slate-400">실수령액</span>
                            </a>
                            <a href="annual-leave.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span>연차 일수·수당 계산기</span>
                                <span class="text-[11px] text-slate-400">미사용 수당</span>
                            </a>
                        </div>
                    </div>
                </div>

                <!-- 2. 부동산 -->
                <div class="relative group h-full flex items-center">
                    <button type="button" class="whitespace-nowrap shrink-0 px-2 lg:px-2.5 py-1.5 rounded-lg {re_cls} transition flex items-center gap-1">
                        <span>부동산</span>
                        <svg class="svg-icon w-3 h-3 text-slate-400 group-hover:rotate-180 transition-transform" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
                    </button>
                    <div class="absolute left-0 top-full pt-1 hidden group-hover:block z-50 w-64 animate-in fade-in">
                        <div class="bg-white rounded-xl shadow-xl border border-slate-200 py-2 text-slate-800 text-sm font-medium">
                            <a href="real-transfer-tax.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span class="font-bold">내 집 양도세 계산기</span>
                                <span class="text-[11px] text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded font-semibold">12억 비과세</span>
                            </a>
                            <a href="real-loan.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span>버팀목 전세대출·HUG 조회</span>
                                <span class="text-[11px] text-slate-400">연 1.8%</span>
                            </a>
                            <a href="real-estate.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span>부동산 복비·취득세 계산기</span>
                                <span class="text-[11px] text-slate-400">국토부 상한</span>
                            </a>
                        </div>
                    </div>
                </div>

                <!-- 3. 복지·지원 -->
                <div class="relative group h-full flex items-center">
                    <button type="button" class="whitespace-nowrap shrink-0 px-2 lg:px-2.5 py-1.5 rounded-lg {wel_cls} transition flex items-center gap-1">
                        <span>복지·지원</span>
                        <svg class="svg-icon w-3 h-3 text-slate-400 group-hover:rotate-180 transition-transform" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
                    </button>
                    <div class="absolute left-0 top-full pt-1 hidden group-hover:block z-50 w-64 animate-in fade-in">
                        <div class="bg-white rounded-xl shadow-xl border border-slate-200 py-2 text-slate-800 text-sm font-medium">
                            <a href="gov-finder.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span class="font-bold text-emerald-600">맞춤 지원금 & 정책 찾기</span>
                                <span class="text-[11px] text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded font-bold">32대 정책</span>
                            </a>
                            <a href="gov-rent.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span class="font-bold">청년 지원 대상조회</span>
                                <span class="text-[11px] text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded font-bold">월 20만·24개월</span>
                            </a>
                            <a href="gov-parent.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span>부모급여·아동수당 대상조회</span>
                                <span class="text-[11px] text-slate-400">만 9세 확대</span>
                            </a>
                            <a href="gov-subsidy.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span>근로장려금 수급 대상조회</span>
                                <span class="text-[11px] text-slate-400">최대 330만</span>
                            </a>
                            <a href="gov-median.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span>2026 복지 지원금 자격조회</span>
                                <span class="text-[11px] text-slate-400">중위소득</span>
                            </a>
                        </div>
                    </div>
                </div>

                <!-- 4. 대출·금융 -->
                <div class="relative group h-full flex items-center">
                    <button type="button" class="whitespace-nowrap shrink-0 px-2 lg:px-2.5 py-1.5 rounded-lg {fin_cls} transition flex items-center gap-1">
                        <span>대출·금융</span>
                        <svg class="svg-icon w-3 h-3 text-slate-400 group-hover:rotate-180 transition-transform" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
                    </button>
                    <div class="absolute left-0 top-full pt-1 hidden group-hover:block z-50 w-64 animate-in fade-in">
                        <div class="bg-white rounded-xl shadow-xl border border-slate-200 py-2 text-slate-800 text-sm font-medium">
                            <a href="loan-dsr.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span class="font-bold">대출이자 & DSR 계산기</span>
                                <span class="text-[11px] text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded font-semibold">+1.50%p</span>
                            </a>
                            <a href="savings.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span>예·적금 만기이자 계산기</span>
                                <span class="text-[11px] text-slate-400">비과세 비교</span>
                            </a>
                            <a href="youth-leap.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span>청년도약계좌 만기금 조회</span>
                                <span class="text-[11px] text-slate-400">기여금 매칭</span>
                            </a>
                            <a href="dutch-pay.html" class="flex items-center justify-between px-4 py-2.5 hover:bg-slate-50 hover:text-blue-600 transition">
                                <span>더치페이 N빵 계산기</span>
                                <span class="text-[11px] text-slate-400">카톡 1초</span>
                            </a>
                        </div>
                    </div>
                </div>
            </nav>
        </div>

        <!-- 우측: 모바일 상단 '지원금 찾기' 상시 노출 + 햄버거 메뉴 버튼 -->
        <div class="flex items-center gap-1.5 md:hidden shrink-0">
            <a href="gov-finder.html" class="whitespace-nowrap shrink-0 px-2.5 py-1.5 rounded-lg {gov_mobile_cls} transition flex items-center gap-1 font-extrabold text-xs border">
                <svg class="svg-icon w-3.5 h-3.5 text-emerald-400" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                <span>지원금 찾기</span>
            </a>
            <button type="button" id="mobileMenuBtn" onclick="toggleMobileNav()" class="p-2 rounded-xl bg-slate-800 text-slate-200 hover:text-white border border-slate-700 transition" aria-label="메뉴 열기">
                <svg class="svg-icon w-5 h-5" viewBox="0 0 24 24">
                    <line x1="3" y1="12" x2="21" y2="12"></line>
                    <line x1="3" y1="6" x2="21" y2="6"></line>
                    <line x1="3" y1="18" x2="21" y2="18"></line>
                </svg>
            </button>
        </div>
    </div>

    <!-- 모바일 전용 반응형 드롭다운 메뉴 -->
    <div id="mobileNavMenu" class="hidden md:hidden bg-[#0F172A] border-t border-slate-800 px-4 py-4 space-y-4 max-h-[80vh] overflow-y-auto animate-in slide-in-from-top duration-200">
        <!-- 핵심 빠른 링크 -->
        <div class="grid grid-cols-2 gap-2 pb-3 border-b border-slate-800">
            <a href="gov-finder.html" class="p-2.5 rounded-lg bg-emerald-950/80 border border-emerald-500/40 text-emerald-300 hover:text-white font-bold text-xs flex items-center justify-center gap-1.5">
                <svg class="svg-icon w-3.5 h-3.5 text-emerald-400" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                <span>지원금 찾기</span>
            </a>
            <a href="blog.html" class="p-2.5 rounded-lg bg-blue-950/80 border border-blue-500/40 text-blue-300 hover:text-white font-bold text-xs flex items-center justify-center gap-1.5">
                <svg class="svg-icon w-3.5 h-3.5 text-blue-400" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                <span>금융 칼럼</span>
            </a>
        </div>

        <!-- 급여·소득 -->
        <div>
            <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">급여·소득</div>
            <div class="grid grid-cols-2 gap-2 text-xs">
                <a href="salary.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-bold transition">연봉 계산기</a>
                <a href="hourly-wage.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-medium transition">알바·시급</a>
                <a href="unemployment.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-bold transition">퇴사자 실업급여</a>
                <a href="severance.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-medium transition">퇴직금 계산기</a>
                <a href="annual-leave.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-medium transition col-span-2">연차 일수·수당</a>
            </div>
        </div>

        <!-- 부동산·주거 -->
        <div>
            <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">부동산·주거</div>
            <div class="grid grid-cols-2 gap-2 text-xs">
                <a href="real-transfer-tax.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-bold transition">내 집 양도세</a>
                <a href="real-loan.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-medium transition">버팀목 전세대출</a>
                <a href="real-estate.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-medium transition col-span-2">부동산 복비·취득세</a>
            </div>
        </div>

        <!-- 정부지원·복지 -->
        <div>
            <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">정부지원·복지</div>
            <div class="grid grid-cols-2 gap-2 text-xs">
                <a href="gov-rent.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-bold transition">청년 지원 대상조회</a>
                <a href="gov-parent.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-medium transition">부모급여·아동수당</a>
                <a href="gov-subsidy.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-medium transition">근로장려금 조회</a>
                <a href="gov-median.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-medium transition">복지 지원금 자격</a>
            </div>
        </div>

        <!-- 대출·금융 -->
        <div>
            <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">대출·금융</div>
            <div class="grid grid-cols-2 gap-2 text-xs">
                <a href="loan-dsr.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-bold transition">대출이자 & DSR</a>
                <a href="savings.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-medium transition">예·적금 만기이자</a>
                <a href="youth-leap.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-medium transition">청년도약계좌</a>
                <a href="dutch-pay.html" class="p-2.5 rounded-lg bg-slate-800/80 hover:bg-blue-600 hover:text-white font-medium transition">더치페이 N빵</a>
            </div>
        </div>
    </div>
</header>"""

    return "\n".join((indent + line if line else "") for line in raw.splitlines())


def sync_all_html_headers(html_dir):
    """Replace the top site navigation <header> across every HTML file consistently."""
    files = sorted(glob.glob(os.path.join(html_dir, "*.html")))
    top_header_re = re.compile(
        r"(?:\s*<!--[^\n]*-->\s*)?<header\b[^>]*>.*?</header>",
        flags=re.S,
    )
    updated = 0
    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        body_m = re.search(r"<body\b[^>]*>", content)
        if not body_m:
            raise RuntimeError(f"Missing <body> in {path}")
        body_end = body_m.end()
        tail = content[body_end:]
        hdr_m = top_header_re.search(tail)
        if not hdr_m or hdr_m.start() > 500:
            raise RuntimeError(f"Missing top navigation <header> near <body> in {path}")
        matched_hdr = hdr_m.group(0)
        if "WE <span" not in matched_hdr and "WE ZIP" not in matched_hdr:
            raise RuntimeError(f"Unexpected first <header> content in {path}")

        replacement = "\n\n" + build_unified_header(os.path.basename(path))
        new_tail = tail[: hdr_m.start()] + replacement + tail[hdr_m.end() :]
        new_content = content[:body_end] + new_tail
        if new_content != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            updated += 1
    return len(files), updated


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    total, count = sync_all_html_headers(base)
    print(f"Synced unified header across {total} HTML files ({count} modified).")
