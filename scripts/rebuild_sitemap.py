import os
import datetime

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_url = 'https://wezip.co.kr'
today = datetime.datetime.now().strftime('%Y-%m-%d')

html_files = sorted([f for f in os.listdir(base_dir) if f.endswith('.html')])
print(f'Total HTML files found: {len(html_files)}')

# 127 Doorway files with noindex (isolated from sitemap for AdSense compliance)
salary_doorway = [f for f in html_files if f.startswith('salary-')]
subsidy_doorway = [f for f in html_files if f.startswith('subsidy-')]
tax_doorway = [
    f for f in html_files 
    if f.startswith('tax-') and f not in ['tax-brokerage-fee-calc.html', 'tax-jeonse-to-monthly-calc.html']
]
doorway_files = set(salary_doorway + subsidy_doorway + tax_doorway)
print(f'Doorway files (excluded from sitemap): {len(doorway_files)}')

urls = []
for f in html_files:
    if f in doorway_files or f == '404.html':
        continue
    
    if f == 'index.html':
        loc = f'{base_url}/'
        priority = '1.0'
        freq = 'daily'
    elif f in [
        'blog.html', 'gov-finder.html', 'salary.html', 'hourly-wage.html',
        'unemployment.html', 'severance.html', 'annual-leave.html',
        'real-transfer-tax.html', 'real-loan.html', 'hug-guarantee.html', 'real-estate.html',
        'gov-rent.html', 'gov-parent.html', 'gov-subsidy.html',
        'gov-median.html', 'loan-dsr.html', 'savings.html',
        'youth-leap.html', 'dutch-pay.html'
    ]:
        loc = f'{base_url}/{f}'
        priority = '0.9'
        freq = 'daily'
    elif f.startswith('blog-'):
        loc = f'{base_url}/{f}'
        priority = '0.8'
        freq = 'weekly'
    else:
        loc = f'{base_url}/{f}'
        priority = '0.5'
        freq = 'monthly'
    
    urls.append((loc, today, freq, priority))

xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

for loc, lastmod, freq, priority in urls:
    xml_lines.append('  <url>')
    xml_lines.append(f'    <loc>{loc}</loc>')
    xml_lines.append(f'    <lastmod>{lastmod}</lastmod>')
    xml_lines.append(f'    <changefreq>{freq}</changefreq>')
    xml_lines.append(f'    <priority>{priority}</priority>')
    xml_lines.append('  </url>')

xml_lines.append('</urlset>')

sitemap_path = os.path.join(base_dir, 'sitemap.xml')
with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_lines) + '\n')

print(f'Successfully generated {len(urls)} elite URLs in sitemap.xml!')
