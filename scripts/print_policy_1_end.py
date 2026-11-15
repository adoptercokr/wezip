with open(r'01-Nova-Web-Studio\money-calc\gov-finder.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find("id: 'rent_subsidy'")
idx2 = c.find("id: 'youth_leap'")
print(repr(c[idx:idx2]))
