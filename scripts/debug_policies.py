# -*- coding: utf-8 -*-
from pathlib import Path
import re

txt = Path("gov-finder.html").read_text(encoding="utf-8")
m = re.search(r'const\s+POLICIES\s*=\s*\[(.*?)\n\s*\];', txt, re.S)
if m:
    # Find each policy object
    pol_texts = m.group(1).split("{\n                id:")
    print("Blocks found:", len(pol_texts))
    for i, p in enumerate(pol_texts[1:], 1):
        m_id = re.search(r"^\s*'([^']+)'", p)
        m_cat = re.search(r"category:\s*'([^']+)'", p)
        pid = m_id.group(1) if m_id else "unknown"
        pcat = m_cat.group(1) if m_cat else "NO_CAT"
        if pcat not in ['business', 'personal']:
            print(f"Policy #{i} {pid}: INVALID CAT '{pcat}'")
    
    # Check all category occurrences
    all_cats = re.findall(r"category:\s*'([^']+)'", m.group(1))
    from collections import Counter
    print("All categories in POLICIES:", Counter(all_cats))
    
    # Look for items without category or different syntax
    for i, p in enumerate(pol_texts[1:], 1):
        m_id = re.search(r"^\s*'([^']+)'", p)
        pid = m_id.group(1) if m_id else f"item_{i}"
        if "category:" not in p:
            print(f"Policy #{i} {pid} has NO category field!")
