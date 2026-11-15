import os
import datetime

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_url = 'https://wezip.co.kr'
today = datetime.datetime.now().strftime('%Y-%m-%d')

html_files = sorted([f for f in os.listdir(base_dir) if f.endswith('.html')])
print(f'Total HTML files found: {len(html_files)}')

urls = []
for f in html_files:
    if f == 'contact.html':
        continue # contact.html has noindex tag
    
    if f == 'index.html':
        loc = f'{base_url}/'
        priority = '1.0'
        freq = 'daily'
    elif f in [
        'blog.html', 'gov-finder.html', 'salary.html', 'hourly-wage.html',
        'unemployment.html', 'severance.html', 'annual-leave.html',
        'real-transfer-tax.html', 'real-loan.html', 'real-estate.html',
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
    elif f.startswith('salary-') or f.startswith('subsidy-') or f.startswith('tax-'):
        loc = f'{base_url}/{f}'
        priority = '0.75'
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

print(f'Successfully generated {len(urls)} URLs in sitemap.xml!')
