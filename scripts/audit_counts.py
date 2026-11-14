# -*- coding: utf-8 -*-
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 1. Check blog.html
blog_text = (ROOT / "blog.html").read_text(encoding="utf-8")
cat_matches = re.findall(r'cat:\s*"([^"]+)"', blog_text)
cat_counts = Counter(cat_matches)
print("[1] blog.html ARTICLES array:")
print("  Total items:", len(cat_matches), "Sum of cats:", sum(cat_counts.values()), dict(cat_counts))
for span_id in ["countAll", "filteredTotal", "countSalary", "countRealestate", "countWelfare", "countFinance"]:
    m = re.search(rf'id="{span_id}"[^>]*>(\d+)<', blog_text)
    print(f"  #{span_id}: {m.group(1) if m else 'MISSING'}")

# 2. Check gov-finder.html
gov_text = (ROOT / "gov-finder.html").read_text(encoding="utf-8")
# Extract POLICIES JS block
m_pol = re.search(r"const\s+POLICIES\s*=\s*\[(.*?)\n\s*\];", gov_text, flags=re.S)
pol_block = m_pol.group(1) if m_pol else ""
pol_cats = re.findall(r"category:\s*'(business|personal)'", pol_block)
pol_counts = Counter(pol_cats)
print("\n[2] gov-finder.html POLICIES array:")
print("  Total items:", len(pol_cats), dict(pol_counts))
for idx, line in enumerate(gov_text.splitlines(), 1):
    if re.search(r"\b(?:22|25|30|35|40|45|52|55|60|100)\s*(?:개|건|종|대)", line):
        if not any(k in line for k in ["amountText", "summary:", "req:", "description", "<td", "title:"]):
            print(f"  L{idx}: {line.strip()[:120]}")

# 3. Check all main menu HTML files and JS files for any hardcoded DB/article/calculator counts
print("\n[3] Scanning all core HTML & JS files for count phrases (N개/N건/N종/N대/N편):")
core_files = [
    "index.html", "blog.html", "gov-finder.html", "salary.html", "hourly-wage.html",
    "unemployment.html", "severance.html", "annual-leave.html", "real-transfer-tax.html",
    "real-loan.html", "real-estate.html", "gov-rent.html", "gov-parent.html",
    "gov-subsidy.html", "gov-median.html", "loan-dsr.html", "savings.html",
    "youth-leap.html", "dutch-pay.html", "about.html", "common.js"
]
for fname in core_files:
    fpath = ROOT / fname
    if not fpath.exists():
        continue
    txt = fpath.read_text(encoding="utf-8")
    for idx, line in enumerate(txt.splitlines(), 1):
        if re.search(r"(?:지원금|정책|칼럼|계산기|문서|DB|총람)[^<\n]{0,30}?\b\d+\s*(?:개|건|종|대|편)|\b\d+\s*(?:개|건|종|대|편)\s*(?:핵심|정부|지원금|정책|칼럼|계산기|복지|소상공인)", line):
            print(f"  {fname} L{idx}: {line.strip()[:130]}")
