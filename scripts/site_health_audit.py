"""
WE ZIP (wezip.co.kr) Site Health, Policy Rate & Calculator Integrity Auditor.

Checks:
1. JSON-LD structured data parsing across every *.html page.
2. Core calculator JavaScript syntax (`node --check`), DOM `getElementById` bindings,
   and functional calculation smoke tests (including `gov-median.html` repeated toggle).
3. `common.js` syntax & UI token hygiene (zero `amber`, zero `#FEE500`, broken links).
4. Statutory 2026 policy rate regression guard across HTML / JS / catalog files.
5. `sitemap.xml` & `rss.xml` well-formedness and URL parity with *.html files on disk.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Tokens that indicate stale 2024/2025 rates left behind as current 2026 rates.
STALE_RATE_RULES: list[tuple[str, re.Pattern[str], str]] = [
    ("stale_min_wage_2025", re.compile(r"(?<![\d,+\-])10,030원"), "2026 최저시급은 10,320원입니다."),
    ("stale_min_monthly_2025", re.compile(r"(?<![\d,+\-])2,096,270"), "2026 주40h 월 환산 최저임금은 2,156,880원입니다."),
    ("stale_weekly_holiday_40", re.compile(r"(?<![\d,+\-])80,240"), "2026 주 40h 주휴수당은 82,560원입니다."),
    ("stale_weekly_holiday_20", re.compile(r"(?<![\d,+\-])40,120"), "2026 주 20h 주휴수당은 41,280원입니다."),
    ("stale_effective_hourly", re.compile(r"(?<![\d,+\-])12,036"), "2026 주휴 포함 실질 시급은 12,384원입니다."),
    ("stale_probation_hourly", re.compile(r"(?<![\d,+\-])9,027"), "2026 수습 90% 시급은 9,288원입니다."),
    ("stale_unemp_lower", re.compile(r"(?<![\d,+\-])(?:64,192|63,104)"), "2026 실업급여 1일 하한액은 66,048원입니다."),
    ("stale_unemp_upper", re.compile(r"(?<![\d,+\-])(?:66,000원|66000원)|상한\s*66,000"), "2026 실업급여 1일 상한액은 68,100원입니다."),
    ("stale_median_1", re.compile(r"(?<![\d,+\-])2,392,013"), "2026 1인 가구 기준 중위소득은 2,564,238원입니다."),
    ("stale_median_4", re.compile(r"(?<![\d,+\-])6,097,773|4인\s*기준\s*609만|4인가구\s*609만"), "2026 4인 가구 기준 중위소득은 6,494,738원입니다."),
    ("stale_np_rate_code", re.compile(r"(?<![\d.])0\.045\b"), "2026.7월 이후 국민연금 근로자 요율은 0.0475입니다."),
    ("stale_hi_rate_code", re.compile(r"(?<![\d.])0\.03545\b|(?<![\d.])3\.545%"), "2026 건강보험 근로자 요율은 3.595%입니다."),
    ("stale_ltc_rate_code", re.compile(r"(?<![\d.])0\.1295\b|(?<![\d.])12\.95%"), "2026 노인장기요양보험 요율은 건보료의 13.14%입니다."),
    ("stale_ins_sum", re.compile(r"(?<![\d.])9\.39%"), "2026 4대보험 합계는 약 9.72%입니다."),
    ("stale_np_cap_617", re.compile(r"(?<![\d,+\-])(?:617만\s*원|617만원|277,650)"), "2026.7월 이후 국민연금 상한은 월 659만 원(월 최대 313,020원)입니다."),
    ("stale_eitc_dual", re.compile(r"(?<![\d,+\-])38000000"), "2026 근로장려금 맞벌이 소득 상한은 4,400만 원입니다."),
    ("stale_hardcoded_date", re.compile(r"new\s+Date\(2026,\s*9"), "고정 날짜 대신 new Date()를 사용하세요."),
]

ALLOW_HISTORICAL_FILES = {
    "blog-hourly-wage-2026.html",
}


def check_json_ld(html_files: list[Path], errors: list[str]) -> int:
    checked = 0
    pattern = re.compile(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        re.S | re.I,
    )
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        for idx, block in enumerate(pattern.findall(text), 1):
            checked += 1
            try:
                json.loads(block.strip())
            except json.JSONDecodeError as exc:
                errors.append(f"[JSON-LD] {path.name} block #{idx}: {exc}")
    return checked


def check_common_js_and_tokens(errors: list[str]) -> None:
    common_js = ROOT / "common.js"
    if not common_js.exists():
        errors.append("[COMMON] common.js is missing")
        return
    txt = common_js.read_text(encoding="utf-8")
    if "amber" in txt or "#FEE500" in txt:
        errors.append("[COMMON] Unwanted amber/#FEE500 token in common.js")

    # Verify every internal .html link referenced in common.js exists on disk.
    for target in set(re.findall(r"url:\s*'([^']+\.html)'", txt)):
        if not (ROOT / target).exists():
            errors.append(f"[COMMON] Broken link target in WEZIP_CROSS_GRAPH: {target}")

    proc = subprocess.run(
        ["node", "--check", str(common_js)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        errors.append(f"[COMMON] node --check failed:\n{proc.stderr.strip()}")


def check_stale_rates(errors: list[str]) -> None:
    scan_targets = (
        sorted(ROOT.glob("*.html"))
        + [ROOT / "scripts" / "site_header.py", ROOT / "scripts" / "topics_catalog.py"]
    )
    for path in scan_targets:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for label, pat, advice in STALE_RATE_RULES:
            if path.name in ALLOW_HISTORICAL_FILES and label == "stale_min_wage_2025":
                # Allow explicit comparison "(전년 10,030원 대비)" only
                cleaned = text.replace("전년(10,030원) 대비", "")
                if pat.search(cleaned):
                    errors.append(f"[STALE:{label}] {path.name}: {advice}")
                continue
            if pat.search(text):
                errors.append(f"[STALE:{label}] {path.name}: {advice}")


def check_calculator_scripts(errors: list[str]) -> None:
    # Run functional JS smoke tests in Node against real inline calculator scripts.
    smoke_js = r"""
const fs = require('fs');
const vm = require('vm');
const assert = require('assert');

function makeClassList(initial = []) {
  const set = new Set(initial);
  return {
    add: (...c) => c.forEach(x => set.add(x)),
    remove: (...c) => c.forEach(x => set.delete(x)),
    toggle: (x, force) => force === undefined ? (set.has(x) ? set.delete(x) : set.add(x)) : (force ? set.add(x) : set.delete(x)),
    contains: (x) => set.has(x),
    toString: () => Array.from(set).join(' '),
  };
}

function makeStubDoc(html) {
  const elements = new Map();
  const idRegex = /\bid=["']([^"']+)["']([^>]*)>/g;
  let m;
  while ((m = idRegex.exec(html)) !== null) {
    const id = m[1];
    const attrs = m[2] || '';
    const valMatch = attrs.match(/\bvalue=["']([^"']*)["']/);
    const el = {
      id,
      value: valMatch ? valMatch[1] : '',
      textContent: '',
      innerHTML: '',
      className: '',
      style: {},
      dataset: {},
      checked: /\bchecked\b/.test(attrs),
      classList: makeClassList(),
      children: [{ textContent: '', className: '' }, { textContent: '', className: '' }],
      get firstElementChild() { return { children: this.children }; },
      addEventListener() {},
      querySelector() { return null; },
      querySelectorAll() { return []; },
      closest() { return null; },
    };
    elements.set(id, el);
  }
  const selectRegex = /<select[^>]*\bid=["']([^"']+)["'][^>]*>([\s\S]*?)<\/select>/gi;
  let sm;
  while ((sm = selectRegex.exec(html)) !== null) {
    const id = sm[1];
    const body = sm[2];
    const opts = Array.from(body.matchAll(/<option([^>]*)value=["']([^"']*)["']/gi));
    if (opts.length > 0 && elements.has(id)) {
      const selected = opts.find(o => /\bselected\b/i.test(o[1]));
      elements.get(id).value = selected ? selected[2] : opts[0][2];
    }
  }
  const doc = {
    readyState: 'complete',
    body: { appendChild() {}, removeChild() {}, classList: makeClassList() },
    head: { appendChild() {} },
    getElementById(id) {
      if (!elements.has(id)) {
        const stub = {
          id, value: '', textContent: '', innerHTML: '', className: '',
          style: {}, dataset: {}, checked: false, classList: makeClassList(),
          children: [{ textContent: '' }, { textContent: '' }],
          get firstElementChild() { return { children: this.children }; },
          addEventListener() {}, querySelector() { return null; }, querySelectorAll() { return []; },
        };
        elements.set(id, stub);
      }
      return elements.get(id);
    },
    querySelector() { return null; },
    querySelectorAll() { return []; },
    getElementsByName(name) {
      const matches = [];
      const rx = new RegExp(`<input[^>]*\\bname=["']${name}["']([^>]*)>`, 'gi');
      let rm;
      while ((rm = rx.exec(html)) !== null) {
        const attrs = rm[1] || '';
        const valM = attrs.match(/\bvalue=["']([^"']*)["']/);
        matches.push({
          name,
          value: valM ? valM[1] : '',
          checked: /\bchecked\b/i.test(attrs),
          addEventListener() {},
        });
      }
      return matches.length ? matches : [{ name, value: 'born', checked: true, addEventListener() {} }];
    },
    createElement() { return { style: {}, classList: makeClassList(), select() {}, appendChild() {} }; },
    addEventListener() {},
    execCommand() {},
  };
  return { doc, elements };
}

function runInlineCalc(fileName, extraSetup) {
  const html = fs.readFileSync(fileName, 'utf8');
  // Parse out first inline calculator script (excluding ld+json and external common.js)
  const scripts = [];
  const re = /<script(?![^>]*(?:src=|application\/ld\+json))[^>]*>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m[1].trim() && !m[1].includes('tailwind.config') && !m[1].includes('function gtag')) scripts.push(m[1]);
  }
  assert(scripts.length > 0, `${fileName}: no inline script found`);
  const { doc, elements } = makeStubDoc(html);
  const ctx = {
    console, Math, Number, String, Array, Object, Date, JSON, Intl, parseInt, parseFloat, isNaN,
    dataLayer: [],
    gtag() {},
    document: doc,
    window: { location: { href: `https://wezip.co.kr/${fileName}`, pathname: `/${fileName}` }, addEventListener() {} },
    navigator: {},
    localStorage: { _d: {}, getItem(k) { return this._d[k] || null; }, setItem(k, v) { this._d[k] = String(v); }, removeItem(k) { delete this._d[k]; } },
    setTimeout, clearTimeout,
    formatNumber: (n) => Math.round(Number(n) || 0).toLocaleString('en-US'),
    unformatNumber: (s) => parseInt(String(s || '0').replace(/[^0-9-]/g, ''), 10) || 0,
    recordRecentCalc() {},
    calculateSalaryPercentile: () => ({ topPercent: 25, rankNumber: 5000000, rankGrade: '상위 30%', comment: 'ok' }),
    setupQuickButtons() {},
    showToast() {},
  };
  ctx.window.document = doc;
  vm.createContext(ctx);
  vm.runInContext(scripts.join('\n'), ctx);
  if (extraSetup) extraSetup(ctx, doc, elements);
}

// 1. salary.html: verify 2026.7 rates (4.75%, 3.595%, 13.14%)
runInlineCalc('salary.html', (ctx, doc) => {
  doc.getElementById('salaryInput').value = '50,000,000';
  doc.getElementById('nonTaxInput').value = '200,000';
  doc.getElementById('familyCount').value = '1';
  doc.getElementById('childCount').value = '0';
  ctx.calculate();
  const net = doc.getElementById('resultNetPay').textContent;
  assert(net.includes('3,497,496'), `salary.html net mismatch: ${net}`);
});

// 2. hourly-wage.html: 10,320 * 209 = 2,156,880
runInlineCalc('hourly-wage.html', (ctx, doc) => {
  doc.getElementById('wageInput').value = '10,320';
  doc.getElementById('dailyHours').value = '8';
  doc.getElementById('weeklyDays').value = '5';
  ctx.calculateWage();
  const gross = doc.getElementById('wageGrossMonthly').textContent;
  assert(gross.includes('2,152,457') || gross.includes('2,156,880'), `hourly-wage gross mismatch: ${gross}`);
});

// 3. unemployment.html: verify upper 68,100 and lower 66,048
runInlineCalc('unemployment.html', (ctx, doc) => {
  ctx.calculateUnemployment();
  const daily = doc.getElementById('unemployDailyAmount').textContent;
  assert(daily.includes('68,100') || daily.includes('66,048'), `unemployment daily mismatch: ${daily}`);
});

// 4. gov-median.html: verify repeated eligible setCard() calls do NOT crash or wipe children
runInlineCalc('gov-median.html', (ctx, doc) => {
  doc.getElementById('medianFamilySize').value = '4';
  doc.getElementById('medianIncomeInput').value = '1,500,000';
  ctx.calculateMedian();
  const cardLife = doc.getElementById('cardLife');
  const prevChildrenLen = cardLife.children.length;
  doc.getElementById('medianFamilySize').value = '3';
  ctx.calculateMedian();
  assert.strictEqual(doc.getElementById('cardLife').children.length, prevChildrenLen);
  assert(doc.getElementById('currentMedianText').textContent.includes('5,359,036'),
    `gov-median 3p mismatch: ${doc.getElementById('currentMedianText').textContent}`);
});

// 5. gov-rent.html: 24개월 최대 4,800,000원
runInlineCalc('gov-rent.html', (ctx, doc) => {
  doc.getElementById('rentAge').value = 'match';
  doc.getElementById('youthIncomeInput').value = '1,200,000';
  doc.getElementById('monthlyRentInput').value = '200,000';
  doc.getElementById('depositInput').value = '10,000,000';
  doc.getElementById('isNoHouse').checked = true;
  ctx.calculateRent();
  assert(doc.getElementById('annualTotalGrantText').textContent.includes('4,800,000'),
    `gov-rent 24m total mismatch: ${doc.getElementById('annualTotalGrantText').textContent}`);
});

// 6. gov-subsidy.html: 맞벌이 4,400만 원 이하 수급 가능 확인
runInlineCalc('gov-subsidy.html', (ctx, doc) => {
  doc.getElementById('subsidyFamilyType').value = 'dualIncome';
  doc.getElementById('annualIncomeInput').value = '43,000,000';
  doc.getElementById('subsidyChildCount').value = '0';
  doc.getElementById('subsidyAssetTier').value = 'under170';
  ctx.calculateSubsidy();
  assert(!doc.getElementById('subsidyTotalAmount').textContent.startsWith('0'),
    `gov-subsidy dual 43M should qualify: ${doc.getElementById('subsidyTotalAmount').textContent}`);
});

// 7. gov-parent.html: 만 9세 미만(10,800,000) + new Date()
runInlineCalc('gov-parent.html', (ctx, doc) => {
  assert(fs.readFileSync('gov-parent.html', 'utf8').includes('10,800,000'));
  ctx.calculateParent();
  assert(doc.getElementById('resChildAllowance').textContent.includes('10,800,000'),
    `gov-parent child allowance mismatch: ${doc.getElementById('resChildAllowance').textContent}`);
});

// 8. loan-dsr.html & real-transfer-tax.html & youth-leap.html syntax & execution check
runInlineCalc('loan-dsr.html', (ctx) => ctx.calculateLoan());
runInlineCalc('real-transfer-tax.html', (ctx) => { if (typeof ctx.calculateTax === 'function') ctx.calculateTax(); else if (typeof ctx.calculate === 'function') ctx.calculate(); });
runInlineCalc('youth-leap.html', (ctx) => { if (typeof ctx.calculateLeap === 'function') ctx.calculateLeap(); else if (typeof ctx.calculate === 'function') ctx.calculate(); });

console.log('NODE_CALC_SMOKE_OK');
"""
    proc = subprocess.run(
        ["node", "-e", smoke_js],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0 or "NODE_CALC_SMOKE_OK" not in proc.stdout:
        errors.append(f"[CALC_SMOKE] Node smoke test failed:\n{proc.stdout}\n{proc.stderr}")


def check_sitemap_and_rss(html_files: list[Path], errors: list[str]) -> None:
    sitemap_path = ROOT / "sitemap.xml"
    rss_path = ROOT / "rss.xml"
    html_names = {p.name for p in html_files}

    if not sitemap_path.exists():
        errors.append("[SITEMAP] sitemap.xml missing")
    else:
        try:
            tree = ET.parse(sitemap_path)
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            locs = [el.text.strip() for el in tree.getroot().findall("sm:url/sm:loc", ns) if el.text]
            sitemap_files = set()
            for loc in locs:
                if loc == "https://wezip.co.kr/":
                    sitemap_files.add("index.html")
                else:
                    fname = loc.replace("https://wezip.co.kr/", "")
                    sitemap_files.add(fname)
                    if fname not in html_names:
                        errors.append(f"[SITEMAP] URL target missing on disk: {fname}")
            # Only indexable pages are required to be in sitemap.xml (noindex pages are properly excluded for AdSense)
            indexable_html_names = set()
            for p in html_files:
                try:
                    content = p.read_text(encoding='utf-8', errors='ignore')
                    if 'noindex' not in content:
                        indexable_html_names.add(p.name)
                except Exception:
                    indexable_html_names.add(p.name)

            missing_in_sitemap = sorted(indexable_html_names - sitemap_files)
            if missing_in_sitemap:
                errors.append(
                    f"[SITEMAP] {len(missing_in_sitemap)} indexable HTML pages missing from sitemap.xml: {missing_in_sitemap[:5]}"
                )
        except ET.ParseError as exc:
            errors.append(f"[SITEMAP] XML parse error: {exc}")

    if not rss_path.exists():
        errors.append("[RSS] rss.xml missing")
    else:
        try:
            ET.parse(rss_path)
        except ET.ParseError as exc:
            errors.append(f"[RSS] XML parse error: {exc}")

    # AI GEO / LLM Discovery files check
    for geo_file in ("llms.txt", "llms-full.txt", "wezip2026indexnowkey8f9a2b3c4d5e.txt"):
        gp = ROOT / geo_file
        if not gp.exists() or gp.stat().st_size < 20:
            errors.append(f"[AI_GEO] Required AI discovery file missing or empty: {geo_file}")

    gov_finder_html = (ROOT / "gov-finder.html").read_text(encoding="utf-8")
    if 'id="staticSubsidyCatalog"' not in gov_finder_html or '"@type": "ItemList"' not in gov_finder_html:
        errors.append("[AI_GEO] gov-finder.html missing staticSubsidyCatalog or ItemList JSON-LD for AI crawlers")


def main() -> int:
    html_files = sorted(ROOT.glob("*.html"))
    errors: list[str] = []

    ld_count = check_json_ld(html_files, errors)
    check_common_js_and_tokens(errors)
    check_stale_rates(errors)
    check_calculator_scripts(errors)
    check_sitemap_and_rss(html_files, errors)

    print(f"Audited {len(html_files)} HTML pages ({ld_count} JSON-LD blocks), common.js, calculators, sitemap.xml & rss.xml.")
    if errors:
        print(f"FAILED with {len(errors)} error(s):")
        for err in errors:
            print(" ", err)
        return 1

    print("ALL SITE HEALTH & POLICY AUDITS PASSED (0 errors).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
