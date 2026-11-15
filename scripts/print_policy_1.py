with open(r'01-Nova-Web-Studio\money-calc\gov-finder.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find("id: 'rent_subsidy'")
print(c[idx-20:idx+200])
