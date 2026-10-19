from pathlib import Path
import json, hashlib
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'dist/index.html').read_text()
original=(root/'mock-original.html').read_text()
css=(root/'build.mjs').read_text()
assert html.startswith('<!doctype html>')
assert 'polymath-product-entry' in html
cat=(root/'dist/creator-suite/index.html').read_text()
program=json.loads((root/'dist/creator-suite/program.json').read_text())
assert len(program['entries'])==100
assert sum(1 for x in program['entries'] if x.get('stage')=='LOCAL_PROTOTYPE_TESTED_NOT_PAID_SUPERIOR')==3
assert sum(1 for x in program['entries'] if x.get('stage')=='NOT_STARTED')==97
assert cat.count('data-entry data-stage=') == 100
soup=BeautifulSoup(html,'html.parser')
assert soup.select_one('main') and soup.select_one('#polymath-product-entry')
assert len(soup.select('#polymath-product-entry a.polytool'))==3
assert len(soup.select('#polymath-product-entry a.polydirectory'))==1
assert soup.select_one('a.polydirectory')['href']=='/creator-suite/'
urls=[x['href'] for x in soup.select('#polymath-product-entry a.polytool')]
assert len(set(urls))==3 and all(u.startswith('https://nilo-') for u in urls)
print('LOCAL_RELEASE_GATES_PASS',json.dumps({'source_integrity':'verified in build.mjs','links':len(urls),'catalog':len(program['entries']),'completed':3,'candidates':97},ensure_ascii=False))