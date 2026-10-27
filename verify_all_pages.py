import os
import glob
import re

html_files = sorted(glob.glob('*.html'))
print(f"Verifying {len(html_files)} HTML files...")

errors = 0
warnings = 0

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as fp:
        full_text = fp.read()

    # 1. Check title, canonical, viewport
    if "<title>" not in full_text:
        print(f"[ERROR] {fpath}: Missing <title>")
        errors += 1
    if 'rel="canonical"' not in full_text:
        print(f"[ERROR] {fpath}: Missing canonical link")
        errors += 1
    if 'common.js' not in full_text and fpath not in ['privacy.html', 'terms.html', 'about.html']:
        print(f"[WARNING] {fpath}: Missing common.js")
        warnings += 1

    # 2. Check policy links in footer
    if 'about.html' not in full_text or 'terms.html' not in full_text or 'privacy.html' not in full_text:
        print(f"[ERROR] {fpath}: Missing policy links in footer")
        errors += 1

    # 3. Check Cool Blue logo presence
    if 'w-10 h-10 rounded-xl bg-blue-600' not in full_text:
        print(f"[ERROR] {fpath}: Missing cool blue logo")
        errors += 1

    # 4. Check for unwanted yellow/amber traces
    if 'amber' in full_text or '#FEE500' in full_text:
        print(f"[ERROR] {fpath}: Unwanted yellow/amber found")
        errors += 1

    # 5. Check div and section balance
    open_d = len(re.findall(r'<div\b', full_text))
    close_d = len(re.findall(r'</div>', full_text))
    open_s = len(re.findall(r'<section\b', full_text))
    close_s = len(re.findall(r'</section>', full_text))
    if open_d != close_d:
        print(f"[ERROR] {fpath}: Div count mismatch ({open_d} open vs {close_d} close)")
        errors += 1
    if open_s != close_s:
        print(f"[ERROR] {fpath}: Section count mismatch ({open_s} open vs {close_s} close)")
        errors += 1

    # 6. Check for broken internal links (only relative .html)
    raw_links = re.findall(r'href="([^":#]+\.html)"', full_text)
    for link in raw_links:
        target = link.split('?')[0].split('#')[0]
        if target and not os.path.exists(target):
            print(f"[ERROR] {fpath}: Broken relative link to {target}")
            errors += 1

print(f"\nVerification Results: Errors = {errors}, Warnings = {warnings}")
if errors == 0 and warnings == 0:
    print(">>> ALL CHECKS PASSED PERFECTLY! 100% HEALTHY & SLEEK FINTECH DESIGN <<<")
