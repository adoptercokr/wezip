with open(r'01-Nova-Web-Studio\money-calc\gov-finder.html', 'r', encoding='utf-8') as f:
    c = f.read()
import re

first_sec = c.find('<!-- 섹션 3-2:')
last_sec = c.rfind('<!-- 섹션 3-2:')
faq_idx = c.find('<!-- 섹션 4: FAQ -->')

print(f"first_sec: {first_sec}, last_sec: {last_sec}, faq_idx: {faq_idx}")
print(f"Distance between last section end and FAQ: {faq_idx - last_sec}")
