# -*- coding: utf-8 -*-
from pathlib import Path
import re

txt = Path("gov-finder.html").read_text(encoding="utf-8")

# Let's inspect occurrences of 'staticSubsidyCatalog'
indices = [m.start() for m in re.finditer(r'<section id="staticSubsidyCatalog"', txt)]
print("Indices:", indices)
for i, idx in enumerate(indices):
    print(f"\n--- Section #{i+1} at char {idx} ---")
    print(txt[idx:idx+400])
