with open(r'01-Nova-Web-Studio\money-calc\scripts\generate_llms_txt.py', 'r', encoding='utf-8') as f:
    code = f.read()

import re
match = re.search(r'def build_static_subsidy_catalog_section[\s\S]*?(?=\ndef [a-zA-Z_]|\Z)', code)
if match:
    print(match.group(0))
