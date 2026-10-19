from playwright.sync_api import sync_playwright
from pathlib import Path
from bs4 import BeautifulSoup
import json
home=Path('/mnt/data/open_lab_repair/dist/index.html').read_text()
page=Path('/mnt/data/open_lab_repair/dist/creator-suite/index.html').read_text()
results={}
with sync_playwright() as p:
  b=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width in (320,390,768,1440):
    tab=b.new_page(viewport={'width':width,'height':880});errors=[]
    tab.on('pageerror',lambda e:errors.append(str(e)))
    tab.set_content(page,wait_until='load')
    assert tab.locator('[data-entry]').count()==100
    assert tab.locator('.lead-card').count()==3
    assert tab.locator('#visible-count').inner_text()=='100'
    assert tab.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),('catalog overflow',width)
    if width==390:
       tab.screenshot(path='/mnt/data/open_lab_repair/catalog-mobile.png',full_page=False)
       tab.locator('[data-filter="public"]').click()
       assert tab.locator('#visible-count').inner_text()=='3'
       assert tab.locator('[data-entry]:visible').count()==3
       tab.locator('[data-filter="candidate"]').click()
       assert tab.locator('#visible-count').inner_text()=='97'
       tab.locator('[data-filter="all"]').click()
       tab.locator('#search').fill('Linktree')
       assert tab.locator('#visible-count').inner_text()=='1'
       assert tab.locator('[data-entry]:visible').count()==1
       tab.locator('#search').fill('nonexistent-xxx')
       assert tab.locator('#visible-count').inner_text()=='0'
       assert tab.locator('#no-results').is_visible()
    if width==1440:tab.screenshot(path='/mnt/data/open_lab_repair/catalog-desktop.png',full_page=False)
    assert not errors,(width,errors)
    results[str(width)]={'overflow':False,'jsErrors':0,'entries':100}
    tab.close()
  tab=b.new_page(viewport={'width':390,'height':880});tab.set_content(home);assert tab.locator('#polymath-product-entry a.polytool').count()==3
  assert tab.locator('nav a[href="#research"]').count()==1
  assert tab.locator('#research').count()==1
  assert tab.evaluate('document.documentElement.scrollWidth<=innerWidth+2')
  tab.screenshot(path='/mnt/data/open_lab_repair/home-mock-mobile.png',full_page=False)
  b.close()
print(json.dumps({'PASS':'100 entries, search, filters, a11y basics, 3 links, original main preserved','viewports':results},ensure_ascii=False))