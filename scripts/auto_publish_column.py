# -*- coding: utf-8 -*-
"""
Wezip Automated SEO Column Publisher (v2: High-Retention Blog + Live News + 3x/Week)
Designed for GitHub Actions and Local CRON Execution.

1. Fetches live South Korean financial/welfare/tax policy headlines from the last 7 days.
2. Uses optional GEMINI_API_KEY (if configured in environment/GitHub Secrets) to craft a fresh
   policy-linked column, OR selects the best seasonal/news-matched column from topics_catalog.py.
3. Renders the 3-stage WE ZIP blog style (Hooking numbers/words -> Easy Story -> Table & 1-won Sim -> 4 Traps & FAQs).
4. Updates blog.html, sitemap.xml, and rss.xml safely and passes strict structural verification.
"""

import argparse
import datetime
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

BASE_DIR = os.path.dirname(SCRIPT_DIR)
HTML_DIR = BASE_DIR
KST = datetime.timezone(datetime.timedelta(hours=9))

from site_header import build_unified_header
from topics_catalog import TOPIC_CATALOG

ALLOWED_CALCULATORS = [
    ("salary.html", "2026 연봉 실수령액·연말정산 계산기"),
    ("savings.html", "예·적금 & 절세 만기 비교 계산기"),
    ("gov-finder.html", "나에게 맞는 2026 정부지원금 찾기"),
    ("gov-rent.html", "청년월세 지원 및 공제 조회기"),
    ("gov-parent.html", "부모급여 & 아동수당 계산기"),
    ("gov-subsidy.html", "2026 근로·자녀장려금 즉시 계산기"),
    ("real-estate.html", "부동산 취득세·중개보수 계산기"),
    ("severance.html", "퇴직금·실업급여 간편 계산기"),
    ("unemployment.html", "2026 실업급여 모의 계산기"),
    ("hourly-wage.html", "최저시급·주휴수당 알바 급여 계산기"),
    ("youth-leap.html", "청년도약계좌 만기 수령액 계산기"),
    ("tax-housing-subscription-points.html", "청약 가점제 84점 만점 계산기"),
    ("subsidy-freelancer-3-3-refund.html", "프리랜서 3.3% 세금 환급 조회기"),
    ("subsidy-national-pension-calc.html", "국민연금 예상 수령액 계산기"),
    ("subsidy-health-skin-dependent.html", "건강보험 피부양자 자격 조회기"),
    ("subsidy-deposit-tax-isa.html", "ISA 만기 비과세·절세 비교 계산기"),
    ("subsidy-overseas-stock-tax.html", "해외주식 양도소득세 계산기"),
    ("subsidy-k-pass-transport-2026.html", "K-패스 대중교통 환급액 계산기"),
    ("subsidy-energy-voucher-2026.html", "에너지바우처 지원금액 조회기"),
    ("subsidy-gift-tax-deduction.html", "증여세 면제 한도 및 세율 계산기"),
    ("tax-jeonse-protection-3law.html", "전세보증금 안전 진단·임대차 계산기"),
]

# Highlight rules (Cool Blue for money/rates, Rose for risk/urgency; zero amber/yellow)
_HIGHLIGHT_PATTERN = re.compile(
    r"(?P<danger>(?<![가-힣])(?:즉시\s*탈락|전액\s*불가|세금\s*폭탄|건보료\s*폭탄|추징\s*폭탄|즉시\s*박탈|이중\s*과세|1원도|토해[내는낼내]|0원|세금\s*면제|전액\s*비과세|전액\s*공제))|"
    r"(?P<metric>(?<![가-힣0-9a-zA-Z])(?:(?:최대\s*|최소\s*|연\s*|월\s*)?(?:\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+)\s*(?:억(?:\s*\d{1,4}\s*만)?|만(?:\s*\d{1,4})?)\s*원|(?:최대\s*|월\s*|연\s*)?\d{1,3}(?:,\d{3})+\s*원|\d{1,2}\s*원|\d{1,3}(?:\.\d+)?%|\d+(?:\.\d+)?배))"
)


def strip_emojis(text):
    """Remove colored emojis/pictographs to comply with crisp monochrome editorial rules."""
    if not text:
        return ""
    return re.sub(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]", "", str(text)).strip()


def sanitize_text(text):
    """Sanitize forbidden color tokens (amber / #FEE500) and colored emojis."""
    cleaned = strip_emojis(text)
    cleaned = re.sub(r"amber", "포인트", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"#fee500", "#EFF6FF", cleaned, flags=re.IGNORECASE)
    return cleaned


def highlight_inline(text, variant="body"):
    """Highlight key numeric figures and urgency phrases cleanly inside visible HTML text nodes."""
    text = sanitize_text(text)
    parts = re.split(r"(<[^>]+>)", text)

    def _replace_match(m):
        if m.group("danger"):
            tok = m.group("danger")
            if variant == "h1":
                return f'<span class="text-rose-600">{tok}</span>'
            return f'<span class="px-1 py-0.5 rounded bg-rose-50 text-rose-700 font-extrabold">{tok}</span>'
        tok = m.group("metric")
        if variant == "h1":
            return f'<span class="text-blue-600 underline decoration-blue-200 decoration-4 underline-offset-4">{tok}</span>'
        return f'<span class="px-1 py-0.5 rounded bg-blue-50 text-blue-700 font-extrabold">{tok}</span>'

    in_anchor = False
    out = []
    for part in parts:
        if not part:
            continue
        if part.startswith("<"):
            lower = part.lower()
            if lower.startswith("<a "):
                in_anchor = True
            elif lower.startswith("</a"):
                in_anchor = False
            out.append(part)
        else:
            if in_anchor:
                out.append(part)
            else:
                out.append(_HIGHLIGHT_PATTERN.sub(_replace_match, part))
    return "".join(out)


def get_week_label(kst_date):
    """Return Korean month-week label like '2026년 11월 2주차'."""
    week_num = (kst_date.day - 1) // 7 + 1
    return f"{kst_date.year}년 {kst_date.month}월 {week_num}주차"


def fetch_weekly_policy_news(limit=20):
    """Fetch recent 7-day Korean finance/policy/welfare headlines via Google News RSS."""
    queries = [
        "정부지원금 OR 복지정책 OR 연말정산 OR 세금개편 when:7d",
        "국민연금 OR 건강보험료 OR 청약 OR 전월세 OR 실업급여 when:7d",
        "최저임금 OR 근로장려금 OR 적금 OR 금리 OR 개인투자 when:7d",
    ]
    blocked_terms = ("야구", "축구", "연예", "드라마", "아이돌", "결별", "열애", "음주운전")
    seen_keys = set()
    collected = []

    for q in queries:
        encoded_q = urllib.parse.quote(q)
        url = f"https://news.google.com/rss/search?q={encoded_q}&hl=ko&gl=KR&ceid=KR:ko"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                xml_bytes = resp.read()
            root = ET.fromstring(xml_bytes)
            for item in root.findall("./channel/item")[:10]:
                raw_title = (item.findtext("title") or "").strip()
                if not raw_title:
                    continue
                if " - " in raw_title:
                    title_part, source_part = raw_title.rsplit(" - ", 1)
                else:
                    title_part, source_part = raw_title, "정책·경제 뉴스"
                title_part = sanitize_text(title_part)
                source_part = sanitize_text(source_part)
                if len(title_part) < 10 or any(b in title_part for b in blocked_terms):
                    continue
                norm_key = re.sub(r"[^가-힣a-zA-Z0-9]", "", title_part)[:18]
                if norm_key in seen_keys:
                    continue
                seen_keys.add(norm_key)
                collected.append({
                    "title": title_part,
                    "source": source_part,
                    "pubDate": (item.findtext("pubDate") or "").strip(),
                })
                if len(collected) >= limit:
                    return collected
        except Exception as exc:
            print(f"[Info] Weekly RSS fetch skipped for query ({exc})")
            continue
    return collected


def ensure_valid_calc_link(calc_link):
    """Guarantee calc_link points to an existing calculator page inside HTML_DIR."""
    valid_set = {fname for fname, _ in ALLOWED_CALCULATORS if os.path.exists(os.path.join(HTML_DIR, fname))}
    if calc_link in valid_set:
        return calc_link
    if calc_link and os.path.exists(os.path.join(HTML_DIR, calc_link)):
        return calc_link
    return "gov-finder.html"


def validate_topic_dict(topic):
    """Verify a topic dictionary matches the full 3-stage WE ZIP blog schema."""
    if not isinstance(topic, dict):
        return False, "topic is not a dict"
    required_str = ("slug", "title", "desc", "cat", "catName", "badge", "readTime", "calcLink", "calcName",
                    "hook_title", "hook_p1", "hook_p2", "editor_tip")
    for key in required_str:
        val = topic.get(key)
        if not isinstance(val, str) or not val.strip():
            return False, f"missing or empty field: {key}"
    if not re.match(r"^blog-[a-z0-9-]+$", topic["slug"]):
        return False, f"invalid slug format: {topic['slug']}"
    if not isinstance(topic.get("part1_easy"), list) or len(topic["part1_easy"]) < 2:
        return False, "part1_easy must have at least 2 sections"
    table = topic.get("table")
    if not isinstance(table, dict) or not table.get("headers") or len(table.get("rows", [])) < 2:
        return False, "table must have headers and at least 2 rows"
    sim = topic.get("simulation")
    if not isinstance(sim, dict) or not sim.get("title") or not sim.get("body"):
        return False, "simulation missing title or body"
    if not isinstance(topic.get("traps"), list) or len(topic["traps"]) < 3:
        return False, "traps must have at least 3 entries"
    if not isinstance(topic.get("faqs"), list) or len(topic["faqs"]) < 2:
        return False, "faqs must have at least 2 entries"
    return True, "ok"


def get_existing_article_titles():
    """Read existing titles from blog.html ARTICLES array so generated posts never duplicate topics."""
    blog_path = os.path.join(HTML_DIR, "blog.html")
    if not os.path.exists(blog_path):
        return []
    with open(blog_path, "r", encoding="utf-8") as f:
        content = f.read()
    return re.findall(r'title:\s*"([^"]+)"', content)


def already_published_today(today_kst):
    """Return True if blog.html already contains an article published on today_kst (YYYY.MM.DD)."""
    blog_path = os.path.join(HTML_DIR, "blog.html")
    if not os.path.exists(blog_path):
        return False
    today_dot = today_kst.strftime("%Y.%m.%d")
    with open(blog_path, "r", encoding="utf-8") as f:
        content = f.read()
    return bool(re.search(rf'date:\s*"{re.escape(today_dot)}"', content))


def maybe_generate_topic_with_gemini(news_items, today_kst):
    """If GEMINI_API_KEY is set, generate a brand-new timely article based on this week's live news."""
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key or not news_items:
        return None, []

    existing_titles = get_existing_article_titles()[:40]
    headlines_str = "\n".join(f"- {n['title']} ({n['source']})" for n in news_items[:8])
    calc_choices_str = "\n".join(f"- {fname}: {cname}" for fname, cname in ALLOWED_CALCULATORS)
    existing_str = "\n".join(f"- {t}" for t in existing_titles[:25])

    prompt = f"""당신은 대한민국 생활금융 포털 '위집(WE ZIP)'의 수석 경제·정책 블로거입니다.
오늘은 {today_kst.isoformat()} ({get_week_label(today_kst)})입니다.

[이번 주 실시간 주요 정책·경제 뉴스]
{headlines_str}

[이미 발행된 최신 칼럼 제목 목록 (절대 중복 금지)]
{existing_str}

[연동 가능한 위집 계산기 목록]
{calc_choices_str}

[작성 절대 수칙]
1. 위 실시간 뉴스 중 독자의 지갑(월급, 세금, 지원금, 부동산, 연금, 생활비)에 가장 직결되는 핫한 주제 1건을 선정해 새로운 장문 블로그 칼럼을 작성하세요.
2. AI 티를 완전히 배제하고 이모지를 절대 쓰지 마세요. (amber/노란색 단어 사용 금지)
3. 제목(title)은 보도자료식 딱딱한 문체 대신, 쉬운 일상어와 자극적인 구체적 숫자·금액, 궁금증을 유발하는 후킹 제목으로 작성하세요.
4. 1부(part1_easy)는 어려운 법률·세무 용어를 싹 빼고 중학생도 이해할 수 있는 쉬운 블로그형 말투로 작성하세요.
5. 2부(table + simulation)는 한눈에 들어오는 비교 표와 가상 인물의 1원 단위 구체적 금액 계산 예시를 담으세요.
6. 3부(traps + faqs)는 현장에서 90%가 놓치는 실수 함정 4가지와 실전 질문·답변 3가지를 작성하세요.
7. 반드시 아래 순수 JSON 객체 하나만 반환하세요(마크다운 코드블록 없이 JSON만):
{{
  "slug": "blog-영문소문자-하이픈-슬러그-2026",
  "title": "후킹 제목",
  "desc": "120자 내외 메타 설명",
  "cat": "salary 또는 realestate 또는 welfare 또는 finance 중 1개",
  "catName": "급여·세무 또는 부동산·주거 또는 복지·지원금 또는 금융·저축 중 1개",
  "badge": "4~6글자 뱃지 (예: 11월속보, 절세필독)",
  "readTime": "약 7분",
  "calcLink": "연동 계산기 파일명",
  "calcName": "연동 계산기 이름",
  "keywords": ["핵심키워드1", "핵심키워드2", "핵심키워드3"],
  "hook_title": "도입부 박스 소제목",
  "hook_p1": "공감 스토리 첫 문단 (3~4문장)",
  "hook_p2": "궁금증 해소 및 핵심 요약 두 번째 문단 (3~4문장)",
  "editor_tip": "편집국 실전 핵심 조언 1~2문장",
  "part1_easy": [["1. 쉬운 질문형 소제목", "친근한 해설"], ["2. 두 번째 소제목", "친근한 해설"]],
  "table": {{"title": "표 제목", "headers": ["구분", "대상/기준", "핵심 혜택/금액"], "rows": [["행1", "값", "값"], ["행2", "값", "값"], ["행3", "값", "값"]]}},
  "simulation": {{"title": "실전 계산: 구체적 가상 인물 사례", "body": "• 상황: ...\\n• 비교: ...\\n• 결과: ..."}},
  "traps": [["1. 함정1 제목", "설명"], ["2. 함정2 제목", "설명"], ["3. 함정3 제목", "설명"], ["4. 함정4 제목", "설명"]],
  "faqs": [["Q. 질문1?", "답변1"], ["Q. 질문2?", "답변2"], ["Q. 질문3?", "답변3"]]
}}"""

    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.6, "responseMimeType": "application/json"},
    }).encode("utf-8")

    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
    )
    try:
        with urllib.request.urlopen(req, timeout=35) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text_out = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        text_out = re.sub(r"^```json\s*|\s*```$", "", text_out).strip()
        topic = json.loads(text_out)
        topic["calcLink"] = ensure_valid_calc_link(topic.get("calcLink", "gov-finder.html"))
        if os.path.exists(os.path.join(HTML_DIR, f"{topic.get('slug', '')}.html")):
            topic["slug"] = f"{topic['slug']}-{today_kst.strftime('%m%d')}"
        ok, reason = validate_topic_dict(topic)
        if not ok:
            print(f"[Warn] Gemini output skipped ({reason}), using curated news-matched catalog.")
            return None, []
        matched = [n for n in news_items if any(kw in n["title"] for kw in topic.get("keywords", []))]
        return topic, (matched[:3] if matched else news_items[:3])
    except Exception as exc:
        print(f"[Info] Gemini dynamic generation unavailable ({exc}), falling back to catalog.")
        return None, []


def select_best_catalog_topic(news_items, today_kst):
    """Pick unpublished catalog topic with strongest score from live weekly news + current month."""
    unpublished = [
        t for t in TOPIC_CATALOG
        if not os.path.exists(os.path.join(HTML_DIR, f"{t['slug']}.html"))
    ]
    if not unpublished:
        return None, []

    best_topic = None
    best_score = -1
    best_matched = []
    cur_month = today_kst.month

    for idx, topic in enumerate(unpublished):
        keywords = topic.get("keywords", [])
        matched = [
            n for n in news_items
            if any(kw.replace(" ", "") in n["title"].replace(" ", "") for kw in keywords)
        ]
        score = len(matched) * 5
        if cur_month in topic.get("best_months", []):
            score += 4
        if f"{cur_month}월" in topic.get("badge", "") or f"{cur_month}월" in topic.get("title", ""):
            score += 3
        # Slight tie-breaker favoring catalog priority order
        total_rank = (score, -idx)
        if best_topic is None or total_rank > best_score:
            best_topic = topic
            best_score = total_rank
            best_matched = matched

    display_news = best_matched[:3] if best_matched else news_items[:3]
    return best_topic, display_news


def render_table_html(table_data):
    """Render clean responsive comparison table with highlighted final outcome column."""
    headers = table_data.get("headers", [])
    rows = table_data.get("rows", [])
    th_parts = []
    for idx, h_text in enumerate(headers):
        cls = "p-3 font-bold text-blue-600" if idx == len(headers) - 1 else "p-3"
        th_parts.append(f'<th class="{cls}">{html.escape(sanitize_text(h_text))}</th>')
    headers_html = "".join(th_parts)

    rows_parts = []
    for row in rows:
        cells = []
        for idx, cell in enumerate(row):
            safe_cell = highlight_inline(sanitize_text(str(cell)))
            if idx == 0:
                cells.append(f'<td class="p-3 font-bold text-slate-900">{safe_cell}</td>')
            elif idx == len(row) - 1:
                cells.append(f'<td class="p-3 font-extrabold text-blue-600">{safe_cell}</td>')
            else:
                cells.append(f'<td class="p-3 text-slate-700">{safe_cell}</td>')
        rows_parts.append(f'<tr class="hover:bg-slate-50 transition">{"".join(cells)}</tr>')

    return headers_html, "\n".join(rows_parts)


def render_article_html(topic, today_str, matched_news=None, week_label=""):
    """Render a full 3-stage WE ZIP article HTML page passing all structural checks."""
    title = sanitize_text(topic["title"])
    desc = sanitize_text(topic["desc"])
    cat_name = sanitize_text(topic["catName"])
    badge = sanitize_text(topic.get("badge", "필독"))
    read_time = sanitize_text(topic["readTime"])
    filename = f"{topic['slug']}.html"
    calc_link = ensure_valid_calc_link(topic["calcLink"])
    calc_name = sanitize_text(topic["calcName"])

    meta_title = html.escape(title, quote=True)
    meta_desc = html.escape(desc, quote=True)
    json_title = json.dumps(title, ensure_ascii=False)
    json_desc = json.dumps(desc, ensure_ascii=False)

    # Weekly policy briefing box (live RSS context)
    weekly_news_html = ""
    if matched_news:
        news_li = []
        for item in matched_news[:3]:
            n_title = html.escape(sanitize_text(item["title"]))
            n_src = html.escape(sanitize_text(item.get("source", "경제·정책 보도")))
            news_li.append(
                f'<li class="flex items-start gap-2">'
                f'<span class="text-blue-600 font-black shrink-0">&bull;</span>'
                f'<span><strong class="text-slate-900">{n_title}</strong> '
                f'<span class="text-slate-400 text-xs">({n_src})</span></span>'
                f'</li>'
            )
        news_ul = "\n                        ".join(news_li)
        w_label = html.escape(week_label or f"{today_str[:7]} 주요 정책 브리핑")
        weekly_news_html = f"""
                <!-- [이번 주 실시간 정책·뉴스 연동 브리핑] -->
                <section class="bg-slate-50 border border-slate-200 rounded-2xl p-4 sm:p-6 space-y-3" aria-label="금주 정책 및 뉴스 브리핑">
                    <div class="flex items-center justify-between gap-2 flex-wrap">
                        <div class="flex flex-wrap items-center gap-2">
                            <span class="px-2.5 py-0.5 rounded bg-blue-600 text-white text-xs font-bold">금주 이슈 연동</span>
                            <span class="text-base sm:text-lg font-extrabold text-slate-900">{w_label} 최신 정책·금융 브리핑</span>
                        </div>
                        <span class="text-xs sm:text-sm text-slate-500 font-medium">{today_str} 최신 보도 반영</span>
                    </div>
                    <ul class="space-y-2 text-sm sm:text-base text-slate-700 leading-relaxed">
                        {news_ul}
                    </ul>
                </section>"""

    # Part 1: Easy storytelling explanations
    part1_cards = []
    for p_heading, p_body in topic["part1_easy"]:
        part1_cards.append(
            f'<div class="p-4 sm:p-5 bg-slate-50 border border-slate-200 rounded-xl space-y-2.5">'
            f'<h3 class="text-lg sm:text-xl font-bold text-slate-900">{highlight_inline(p_heading)}</h3>'
            f'<p class="text-base sm:text-lg text-slate-700 leading-relaxed">{highlight_inline(p_body)}</p>'
            f'</div>'
        )
    part1_html = "\n                        ".join(part1_cards)

    # Part 2: Comparison table & simulation
    headers_html, table_rows_html = render_table_html(topic["table"])
    sim = topic["simulation"]
    sim_lines = [line.strip() for line in sanitize_text(sim["body"]).splitlines() if line.strip()]
    sim_paras = []
    for idx, line in enumerate(sim_lines):
        if idx == len(sim_lines) - 1:
            sim_paras.append(
                f'<p class="pt-3 border-t border-slate-200 text-blue-900 font-extrabold text-base sm:text-lg">{highlight_inline(line)}</p>'
            )
        else:
            sim_paras.append(f'<p>{highlight_inline(line)}</p>')
    sim_body_html = "\n                        ".join(sim_paras)

    # Part 3: 4 Traps
    trap_cards = []
    for t_title, t_body in topic["traps"]:
        trap_cards.append(
            f'<div class="p-4 sm:p-5 bg-slate-50 border border-slate-200 rounded-xl space-y-2">'
            f'<div class="flex flex-wrap items-center gap-2">'
            f'<span class="px-2 py-0.5 rounded bg-rose-50 text-rose-700 border border-rose-200 text-xs font-bold shrink-0">주의</span>'
            f'<span class="font-bold text-slate-900 text-base sm:text-lg">{highlight_inline(t_title)}</span>'
            f'</div>'
            f'<p class="text-sm sm:text-base text-slate-700 leading-relaxed">{highlight_inline(t_body)}</p>'
            f'</div>'
        )
    traps_html = "\n                        ".join(trap_cards)

    # FAQs + FAQPage JSON-LD
    faq_blocks = []
    faq_schema_items = []
    for q, a in topic["faqs"]:
        q_clean = sanitize_text(q)
        a_clean = sanitize_text(a)
        faq_blocks.append(
            f'<div class="p-4 sm:p-5 bg-slate-50 border border-slate-200 rounded-xl">'
            f'<div class="font-bold text-slate-900 text-base sm:text-lg">{html.escape(q_clean)}</div>'
            f'<div class="text-sm sm:text-base text-slate-700 mt-2 leading-relaxed">{highlight_inline(a_clean)}</div>'
            f'</div>'
        )
        faq_schema_items.append(
            f'{{\n          "@type": "Question",\n          "name": {json.dumps(q_clean, ensure_ascii=False)},\n'
            f'          "acceptedAnswer": {{\n            "@type": "Answer",\n            "text": {json.dumps(a_clean, ensure_ascii=False)}\n          }}\n        }}'
        )
    faq_html = "\n                        ".join(faq_blocks)
    faq_schema_str = ",\n        ".join(faq_schema_items)

    unified_header = build_unified_header(filename)

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-2N5V6S642H"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', 'G-2N5V6S642H');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>{meta_title} | 위집 (wezip)</title>
    <meta name="description" content="{meta_desc}">
    <link rel="canonical" href="https://wezip.co.kr/{filename}">

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{meta_title} | 위집">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:url" content="https://wezip.co.kr/{filename}">
    <meta property="og:site_name" content="위집 (wezip)">
    <meta property="og:locale" content="ko_KR">
    <meta property="og:image" content="https://wezip.co.kr/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="WE ZIP - 대한민국 생활 금융 포털">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="https://wezip.co.kr/og-image.png">

    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="manifest" href="site.webmanifest">

    <!-- Google AdSense -->
    <meta name="google-adsense-account" content="ca-pub-5717882145510454">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5717882145510454" crossorigin="anonymous"></script>

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="common.css">

    <!-- Schema.org JSON-LD -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "headline": {json_title},
      "description": {json_desc},
      "author": {{
        "@type": "Organization",
        "name": "위집 금융편집국",
        "url": "https://wezip.co.kr/about.html"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "위집",
        "url": "https://wezip.co.kr"
      }},
      "datePublished": "{today_str}",
      "dateModified": "{today_str}",
      "mainEntityOfPage": "https://wezip.co.kr/{filename}"
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {faq_schema_str}
      ]
    }}
    </script>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen flex flex-col font-sans">

{unified_header}

    <!-- [와이드 3단 레이아웃: 좌측 배너 + 중앙 컨텐츠 + 우측 배너] -->
    <div class="w-full max-w-[1560px] mx-auto px-2 sm:px-4 py-8 flex items-start justify-center gap-5 flex-grow">
        <!-- [좌측 스폰서 배너 광고 (데스크톱 160x600)] -->
        <aside class="hidden xl:flex flex-col items-center w-[160px] shrink-0 sticky top-20 select-none z-10" aria-label="좌측 스폰서 광고">
            <div class="w-full bg-white border border-dashed border-slate-300 rounded-2xl p-3 text-center shadow-xs min-h-[600px] flex flex-col justify-between hover:border-slate-400 transition">
                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">ADVERTISEMENT</span>
                <div class="my-auto py-8 text-slate-400">
                    <svg class="svg-icon w-6 h-6 mx-auto mb-2 text-slate-400" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
                    <div class="text-xs font-bold text-slate-600">좌측 날개 배너</div>
                    <div class="text-[11px] text-slate-400 mt-1">160 × 600<br>구글 애드센스 및<br>직접 광고 스폰서</div>
                </div>
                <div class="w-full pt-2 border-t border-slate-100">
                    <span class="text-[10px] text-slate-400 font-medium block mb-1">WE ZIP 스폰서</span>
                    <a href="contact.html?type=ad" class="block w-full py-1.5 px-2 bg-blue-50 hover:bg-blue-100 text-blue-700 text-[11px] font-bold rounded-lg border border-blue-200 transition text-center">
                        배너 광고 문의 &rarr;
                    </a>
                </div>
            </div>
        </aside>

        <!-- [중앙 메인 컨텐츠] -->
        <main class="w-full min-w-0 max-w-4xl mx-auto space-y-8">
            <nav class="flex flex-wrap items-center gap-2 text-xs sm:text-sm text-slate-500 font-medium">
                <a href="index.html" class="hover:text-blue-600 transition">홈</a>
                <span>&gt;</span>
                <a href="blog.html" class="hover:text-blue-600 transition">금융 칼럼</a>
                <span>&gt;</span>
                <span class="text-slate-800 font-bold">{html.escape(cat_name)}</span>
            </nav>

            <header class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-8 shadow-xs space-y-4">
                <div class="flex items-center gap-2 flex-wrap">
                    <span class="text-xs sm:text-sm font-bold px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 border border-blue-200">{html.escape(cat_name)} {html.escape(badge)}</span>
                    <span class="text-xs sm:text-sm text-slate-400">읽는 시간 {html.escape(read_time)} · {today_str}</span>
                </div>
                <h1 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight leading-snug">
                    {highlight_inline(title, variant="h1")}
                </h1>
                <p class="text-base sm:text-lg text-slate-600 leading-relaxed">
                    {highlight_inline(desc)}
                </p>

                <!-- 계산기 바로가기 배너 -->
                <div class="p-4 sm:p-5 bg-blue-50/70 border border-blue-200 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-3 mt-4">
                    <div class="flex items-center gap-2 text-sm sm:text-base text-blue-900 font-bold">
                        <svg class="svg-icon w-4 h-4 text-blue-600 shrink-0" viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2"></rect><line x1="8" y1="6" x2="16" y2="6"></line></svg>
                        <span>내 예상 금액과 자격을 지금 1초 만에 직접 계산해 보세요!</span>
                    </div>
                    <a href="{calc_link}" class="px-4 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-sm sm:text-base font-bold transition shadow-sm shrink-0 text-center">
                        {html.escape(calc_name)} &rarr;
                    </a>
                </div>
            </header>

            <article class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-8 shadow-xs space-y-8 text-slate-700 leading-relaxed font-normal">
                <!-- [블로그형 스토리텔링 도입부 & 공감 해설 박스] -->
                <div class="bg-gradient-to-r from-blue-50/70 via-slate-50 to-blue-50/40 border-l-4 border-blue-600 rounded-r-2xl p-4 sm:p-7 space-y-4 text-slate-700 text-base sm:text-lg leading-relaxed">
                    <div class="flex items-center gap-2 font-black text-slate-900 text-lg sm:text-xl">
                        <span class="w-2.5 h-2.5 rounded-full bg-blue-600 shrink-0"></span>
                        <span>{highlight_inline(topic["hook_title"])}</span>
                    </div>
                    <p class="font-medium text-slate-800 leading-relaxed">
                        {highlight_inline(topic["hook_p1"])}
                    </p>
                    <p class="text-base sm:text-lg text-slate-700 leading-relaxed">
                        {highlight_inline(topic["hook_p2"])}
                    </p>
                    <div class="pt-3 border-t border-blue-100/80 flex flex-col sm:flex-row sm:items-center gap-1.5 sm:gap-2 text-sm font-bold text-blue-800">
                        <span class="shrink-0">* 위집 편집국 핵심 조언:</span>
                        <span class="font-normal text-slate-700">{highlight_inline(topic["editor_tip"])}</span>
                    </div>
                </div>
                {weekly_news_html}

                <!-- [1단계: 초반부] 누구나 이해하는 쉬운 블로그식 원리 설명 -->
                <section class="space-y-4">
                    <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900 border-b border-slate-200 pb-2">
                        1. 초보자도 3분 만에 이해하는 핵심 원리
                    </h2>
                    <div class="space-y-3.5">
                        {part1_html}
                    </div>
                </section>

                <!-- [2단계: 중반부] 세부 비교 표 & 실전 1원 단위 시뮬레이션 -->
                <section class="space-y-5 border-t border-slate-100 pt-6">
                    <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900 border-b border-slate-200 pb-2">
                        2. {html.escape(sanitize_text(topic["table"]["title"]))}
                    </h2>
                    <div class="overflow-x-auto">
                        <table class="w-full min-w-[540px] sm:min-w-0 text-sm sm:text-base text-left border border-slate-200 rounded-xl overflow-hidden">
                            <thead class="bg-slate-100 text-slate-800 font-bold border-b border-slate-200">
                                <tr>{headers_html}</tr>
                            </thead>
                            <tbody class="divide-y divide-slate-200 font-medium">
                                {table_rows_html}
                            </tbody>
                        </table>
                    </div>

                    <h3 class="text-lg sm:text-xl font-bold text-slate-900 pt-2">{highlight_inline(sim["title"])}</h3>
                    <div class="p-4 sm:p-6 bg-slate-50 border border-slate-200 rounded-2xl text-base sm:text-lg text-slate-700 leading-relaxed space-y-3.5 font-medium">
                        {sim_body_html}
                    </div>
                </section>

                <!-- [3단계: 후반부] 모르면 손해 보는 치명적 실수 함정 4가지 -->
                <section class="space-y-4 border-t border-slate-100 pt-6">
                    <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900 border-b border-slate-200 pb-2">
                        3. 모르면 손해 보는 치명적 실수 함정
                    </h2>
                    <div class="space-y-3.5">
                        {traps_html}
                    </div>
                </section>

                <!-- 자주 묻는 질문 (FAQ) -->
                <section class="space-y-4 border-t border-slate-100 pt-6">
                    <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900 flex items-center gap-2">
                        <span class="w-2 h-5 bg-blue-600 rounded-full inline-block"></span>
                        <span>자주 묻는 질문 (FAQ)</span>
                    </h2>
                    <div class="space-y-3.5">
                        {faq_html}
                    </div>
                </section>

                <!-- 관련 계산기 하단 추천 배너 -->
                <section class="p-5 sm:p-6 bg-blue-50/70 border border-blue-200 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4">
                    <div class="space-y-1 text-center sm:text-left">
                        <div class="text-xs sm:text-sm font-bold text-blue-600 uppercase tracking-wide">WE ZIP 실시간 계산기 연동</div>
                        <div class="text-base sm:text-lg font-extrabold text-slate-900">내 실제 예상 금액을 1초 만에 확인해 보세요</div>
                        <p class="text-sm sm:text-base text-slate-600">2026년 최신 법정 기준이 100% 반영된 무료 시뮬레이터입니다.</p>
                    </div>
                    <a href="{calc_link}" class="w-full sm:w-auto py-3 px-5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm sm:text-base rounded-xl transition text-center shrink-0 shadow-sm">
                        {html.escape(calc_name)} 바로가기 &rarr;
                    </a>
                </section>
            </article>

            <div class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-xs flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <div class="font-bold text-slate-900 text-base">페이지 내용이 도움이 되셨나요?</div>
                    <div class="text-sm text-slate-500">지인이나 동료에게 링크를 복사하여 유용한 금융·세무 정보를 공유해 보세요.</div>
                </div>
                <button type="button" onclick="copyPageUrl(this)" class="px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm flex items-center gap-1.5 transition shrink-0">
                    <svg class="svg-icon w-4 h-4" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
                    <span>페이지 링크 복사</span>
                </button>
            </div>
        </main>

        <!-- [우측 스폰서 배너 광고 (데스크톱 160x600)] -->
        <aside class="hidden xl:flex flex-col items-center w-[160px] shrink-0 sticky top-20 select-none z-10" aria-label="우측 스폰서 광고">
            <div class="w-full bg-white border border-dashed border-slate-300 rounded-2xl p-3 text-center shadow-xs min-h-[600px] flex flex-col justify-between hover:border-slate-400 transition">
                <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">ADVERTISEMENT</span>
                <div class="my-auto py-8 text-slate-400">
                    <svg class="svg-icon w-6 h-6 mx-auto mb-2 text-slate-400" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
                    <div class="text-xs font-bold text-slate-600">우측 날개 배너</div>
                    <div class="text-[11px] text-slate-400 mt-1">160 × 600<br>구글 애드센스 및<br>직접 광고 스폰서</div>
                </div>
                <div class="w-full pt-2 border-t border-slate-100">
                    <span class="text-[10px] text-slate-400 font-medium block mb-1">WE ZIP 스폰서</span>
                    <a href="contact.html?type=ad" class="block w-full py-1.5 px-2 bg-blue-50 hover:bg-blue-100 text-blue-700 text-[11px] font-bold rounded-lg border border-blue-200 transition text-center">
                        배너 광고 문의 &rarr;
                    </a>
                </div>
            </div>
        </aside>
    </div>

    <footer class="bg-white border-t border-slate-200 mt-20 select-none">
        <div class="max-w-6xl mx-auto px-4 py-8">
            <div class="flex flex-col sm:flex-row items-center justify-between gap-4 border-b border-slate-100 pb-6 text-xs text-slate-500">
                <div class="flex items-center gap-2">
                    <div class="w-6 h-6 rounded-md bg-blue-600 flex items-center justify-center text-white font-bold text-xs">W</div>
                    <span class="font-bold text-slate-700">위집 (wezip)</span>
                    <span class="text-slate-300">|</span>
                    <span>2026 대한민국 생활 금융 포털</span>
                </div>
                <div class="flex items-center gap-4 font-medium">
                    <a href="about.html" class="hover:text-blue-600 transition">서비스 소개</a>
                    <a href="terms.html" class="hover:text-blue-600 transition">이용약관</a>
                    <a href="privacy.html" class="hover:text-blue-600 transition font-bold text-slate-700">개인정보처리방침</a>
                </div>
            </div>
            <div class="pt-6 text-center text-xs text-slate-400 space-y-1">
                <p>본 사이트의 모든 계산 결과는 2026년 관계 법령 및 세법 기준 시뮬레이션이며, 법적 효력을 갖는 공식 증명서가 아닙니다.</p>
                <p>© 2026 wezip.co.kr. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script src="common.js"></script>
</body>
</html>
"""
    return html_content


def verify_rendered_html(slug, html_content):
    """Run strict integrity assertions on rendered article HTML before saving."""
    if "amber" in html_content.lower() or "#fee500" in html_content.lower():
        raise AssertionError(f"[{slug}] Forbidden amber/#FEE500 token detected in rendered HTML")
    if html_content.count("<div") != html_content.count("</div"):
        raise AssertionError(f"[{slug}] Unbalanced <div> tags")
    if html_content.count("<section") != html_content.count("</section"):
        raise AssertionError(f"[{slug}] Unbalanced <section> tags")
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html_content, flags=re.S):
        json.loads(block.strip())


def update_blog_html(topic, today_str):
    blog_path = os.path.join(HTML_DIR, "blog.html")
    with open(blog_path, "r", encoding="utf-8") as f:
        content = f.read()

    filename = f"{topic['slug']}.html"
    if f'link: "{filename}"' in content:
        print(f"blog.html already contains {filename}; skipping insert.")
        return

    no_matches = [int(m) for m in re.findall(r"no:\s*(\d+)", content)]
    next_no = max(no_matches) + 1 if no_matches else 52
    date_formatted = today_str.replace("-", ".")

    new_article_entry = (
        f"      {{\n"
        f"        no: {next_no},\n"
        f"        title: {json.dumps(sanitize_text(topic['title']), ensure_ascii=False)},\n"
        f"        desc: {json.dumps(sanitize_text(topic['desc']), ensure_ascii=False)},\n"
        f"        cat: {json.dumps(topic['cat'], ensure_ascii=False)},\n"
        f"        catName: {json.dumps(sanitize_text(topic['catName']), ensure_ascii=False)},\n"
        f"        badge: {json.dumps(sanitize_text(topic.get('badge', '필독')), ensure_ascii=False)},\n"
        f"        date: \"{date_formatted}\",\n"
        f"        readTime: {json.dumps(sanitize_text(topic['readTime']), ensure_ascii=False)},\n"
        f"        link: \"{filename}\"\n"
        f"      }},"
    )

    articles_marker = "const ARTICLES = ["
    if articles_marker in content:
        content = content.replace(articles_marker, f"{articles_marker}\n{new_article_entry}", 1)

    # Automatically synchronize total count spans and category count spans
    content = re.sub(r'(<span id="countAll">)\d+(</span>)', rf'\g<1>{next_no}\g<2>', content)
    content = re.sub(r'(<span id="filteredTotal"[^>]*>)\d+(</span>)', rf'\g<1>{next_no}\g<2>', content)

    cat_id_map = {
        "salary": "countSalary",
        "realestate": "countRealestate",
        "welfare": "countWelfare",
        "finance": "countFinance",
    }
    cat_span_id = cat_id_map.get(topic.get("cat"))
    if cat_span_id:
        def inc_cat(m):
            cur = int(m.group(2))
            return f"{m.group(1)}{cur + 1}{m.group(3)}"
        content = re.sub(rf'(<span id="{cat_span_id}">)(\d+)(</span>)', inc_cat, content)

    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated blog.html: Added article #{next_no} ({filename})")


def update_sitemap(filename, today_str):
    sitemap_path = os.path.join(HTML_DIR, "sitemap.xml")
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_url_entry = (
        f"    <url>\n"
        f"        <loc>https://wezip.co.kr/{filename}</loc>\n"
        f"        <lastmod>{today_str}</lastmod>\n"
        f"        <changefreq>weekly</changefreq>\n"
        f"        <priority>0.80</priority>\n"
        f"    </url>"
    )

    if f"<loc>https://wezip.co.kr/{filename}</loc>" not in content:
        content = content.replace("</urlset>", f"{new_url_entry}\n</urlset>")
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated sitemap.xml: Added {filename}")


def update_rss(topic):
    rss_path = os.path.join(HTML_DIR, "rss.xml")
    with open(rss_path, "r", encoding="utf-8") as f:
        content = f.read()

    filename = f"{topic['slug']}.html"
    rfc822_date = datetime.datetime.now(KST).strftime("%a, %d %b %Y %H:%M:%S +0900")
    safe_title = html.escape(sanitize_text(topic["title"]), quote=False)
    safe_desc = html.escape(sanitize_text(topic["desc"]), quote=False)
    safe_cat = html.escape(sanitize_text(topic["catName"]), quote=False)

    new_item = (
        f"    <item>\n"
        f"      <title>{safe_title}</title>\n"
        f"      <link>https://wezip.co.kr/{filename}</link>\n"
        f"      <guid>https://wezip.co.kr/{filename}</guid>\n"
        f"      <description>{safe_desc}</description>\n"
        f"      <pubDate>{rfc822_date}</pubDate>\n"
        f"      <category>{safe_cat}</category>\n"
        f"    </item>"
    )

    if f"<link>https://wezip.co.kr/{filename}</link>" not in content:
        channel_marker = "<channel>"
        if channel_marker in content:
            m = re.search(r"(<lastBuildDate>[^<]+</lastBuildDate>)", content)
            if m:
                content = content.replace(m.group(1), f"{m.group(1)}\n    {new_item}", 1)
            else:
                content = content.replace(channel_marker, f"{channel_marker}\n    {new_item}", 1)
        with open(rss_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated rss.xml: Added {filename}")


def verify_catalog():
    """Dry-run validate every topic in TOPIC_CATALOG for schema, links, tags, and zero amber."""
    today_kst = datetime.datetime.now(KST).date()
    today_str = today_kst.isoformat()
    week_label = get_week_label(today_kst)
    sample_news = [{"title": "2026년 연말정산·정부지원금 핵심 개편안 발표", "source": "정책브리핑"}]

    print(f"Verifying {len(TOPIC_CATALOG)} topics in TOPIC_CATALOG...")
    seen_slugs = set()
    for idx, topic in enumerate(TOPIC_CATALOG, 1):
        ok, msg = validate_topic_dict(topic)
        if not ok:
            raise AssertionError(f"Catalog #{idx} invalid: {msg}")
        slug = topic["slug"]
        if slug in seen_slugs:
            raise AssertionError(f"Duplicate slug in TOPIC_CATALOG: {slug}")
        seen_slugs.add(slug)

        calc_path = os.path.join(HTML_DIR, topic["calcLink"])
        if not os.path.exists(calc_path):
            raise AssertionError(f"Catalog #{idx} ({slug}) calcLink missing on disk: {topic['calcLink']}")

        rendered = render_article_html(topic, today_str, matched_news=sample_news, week_label=week_label)
        verify_rendered_html(slug, rendered)

    print(f"ALL {len(TOPIC_CATALOG)} CATALOG TOPICS VERIFIED: 0 errors, valid links, balanced tags, valid JSON-LD.")


def load_topic_from_json_arg(json_arg, news_items, today_kst):
    """Load an external AI-authored topic JSON file (or '-' for stdin) and pair weekly news."""
    if json_arg == "-":
        raw = sys.stdin.read()
    else:
        with open(json_arg, "r", encoding="utf-8") as f:
            raw = f.read()
    topic = json.loads(raw)
    topic["calcLink"] = ensure_valid_calc_link(topic.get("calcLink", "gov-finder.html"))
    if os.path.exists(os.path.join(HTML_DIR, f"{topic.get('slug', '')}.html")):
        topic["slug"] = f"{topic['slug']}-{today_kst.strftime('%m%d')}"
    keywords = topic.get("keywords", [])
    matched = [n for n in news_items if any(kw in n["title"] for kw in keywords)]
    return topic, (matched[:3] if matched else news_items[:3])


def main():
    parser = argparse.ArgumentParser(description="Wezip Auto Column Publisher")
    parser.add_argument("--verify-catalog", action="store_true", help="Render-check all catalog topics without writing files")
    parser.add_argument("--dry-run", action="store_true", help="Select and verify next post without modifying disk")
    parser.add_argument("--check-today", action="store_true", help="Print PUBLISHED or PENDING for today's KST date and exit")
    parser.add_argument("--force", action="store_true", help="Publish even if an article already exists for today")
    parser.add_argument("--from-json", type=str, default="", help="Publish a custom AI-authored topic JSON file ('-' for stdin)")
    parser.add_argument("--delete-json", action="store_true", help="Remove the --from-json source file after successful publish")
    args = parser.parse_args()

    if args.verify_catalog:
        verify_catalog()
        return

    today_kst = datetime.datetime.now(KST).date()
    if args.check_today:
        print("PUBLISHED" if already_published_today(today_kst) else "PENDING")
        return

    today_str = today_kst.isoformat()
    week_label = get_week_label(today_kst)

    if already_published_today(today_kst) and not args.dry_run and not args.force:
        print(f"[Skip] Today's column ({today_kst.strftime('%Y.%m.%d')}) is already published. Skipping duplicate.")
        return

    print(f"Starting Wezip Auto Column Publisher ({today_str}, {week_label})...")

    news_items = fetch_weekly_policy_news()
    print(f"Fetched {len(news_items)} recent 7-day Korean finance/policy headlines.")

    if args.from_json:
        selected_topic, matched_news = load_topic_from_json_arg(args.from_json, news_items, today_kst)
        source_mode = "Antigravity AI + Live RSS"
    else:
        selected_topic, matched_news = maybe_generate_topic_with_gemini(news_items, today_kst)
        source_mode = "Gemini + Live RSS"
        if not selected_topic:
            selected_topic, matched_news = select_best_catalog_topic(news_items, today_kst)
            source_mode = "Curated Catalog + Live RSS"

    if not selected_topic:
        print("All catalog topics are already published and GEMINI_API_KEY is unset. Queue exhausted.")
        return

    ok, reason = validate_topic_dict(selected_topic)
    if not ok:
        raise RuntimeError(f"Selected topic validation failed: {reason}")

    filename = f"{selected_topic['slug']}.html"
    print(f"[{source_mode}] Selected: {selected_topic['title']} -> {filename}")
    if matched_news:
        print(f"Connected weekly headlines ({len(matched_news)}):")
        for n in matched_news:
            print(f"  - {n['title']} ({n['source']})")

    html_content = render_article_html(selected_topic, today_str, matched_news=matched_news, week_label=week_label)
    verify_rendered_html(selected_topic["slug"], html_content)

    if args.dry_run:
        print("Dry-run completed cleanly. No files were modified.")
        return

    file_path = os.path.join(HTML_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated standalone article file: {file_path}")

    update_blog_html(selected_topic, today_str)
    update_sitemap(filename, today_str)
    update_rss(selected_topic)
    # Refresh unified top headers (with latest KST update date), llms.txt & llms-full.txt, and ping IndexNow
    try:
        from site_header import sync_all_html_headers
        sync_all_html_headers(HTML_DIR)
    except Exception as exc:
        print(f"[Info] Header sync warning: {exc}")
    try:
        import subprocess
        gen_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generate_llms_txt.py")
        if os.path.exists(gen_script):
            subprocess.run([sys.executable, gen_script, "--ping"], cwd=HTML_DIR, timeout=30, check=False)
    except Exception as exc:
        print(f"[Info] LLM context sync warning: {exc}")
    if args.from_json and args.from_json != "-" and args.delete_json and os.path.exists(args.from_json):
        os.remove(args.from_json)
    print(f"Successfully published new column: {selected_topic['title']}")


if __name__ == "__main__":
    main()
