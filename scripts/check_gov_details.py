# -*- coding: utf-8 -*-
from pathlib import Path
import re

txt = Path("gov-finder.html").read_text(encoding="utf-8")
print("Occurrences of id='staticSubsidyCatalog':", txt.count('id="staticSubsidyCatalog"'))

# Check actual POLICIES count
m = re.search(r'const\s+POLICIES\s*=\s*\[(.*?)\n\s*\];', txt, re.S)
if m:
    ids = re.findall(r"id:\s*'([^']+)'", m.group(1))
    cats = re.findall(r"category:\s*'([^']+)'", m.group(1))
    print(f"POLICIES array has {len(ids)} items: {set(cats)}")
    from collections import Counter
    print("Category breakdown:", Counter(cats))
