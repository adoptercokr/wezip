with open(r'01-Nova-Web-Studio\money-calc\gov-finder.html', 'r', encoding='utf-8') as f:
    c = f.read()
import re
print('Occurrences of id="staticSubsidyCatalog":', len(re.findall(r'id="staticSubsidyCatalog"', c)))
print('Occurrences of <!-- 섹션 3-2:', len(re.findall(r'<!-- 섹션 3-2:', c)))
