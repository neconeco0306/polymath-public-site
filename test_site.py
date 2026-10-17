from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import re, unittest, json

ROOT=Path(__file__).parent
class CheckHTML(HTMLParser):
 def __init__(self):
  super().__init__();self.ids=[];self.hrefs=[];self.meta=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='a':self.hrefs.append(a.get('href',''))
  if tag=='meta':self.meta.append(a)

class NotebookStructure(HTMLParser):
 def __init__(self):
  super().__init__();self.div_classes=[];self.entries=0;self.times=0;self.errors=[]
 def handle_starttag(self,tag,attrs):
  if tag=='div':
   classes=set((dict(attrs).get('class') or '').split())
   if 'log-entry' in classes and 'notebook' in self.div_classes:
    self.entries+=1
    if 'log-entry' in self.div_classes:self.errors.append('nested log-entry')
    if self.div_classes[-2:]!=['notebook','']:self.errors.append('log-entry is not a direct notebook-row child')
   self.div_classes.append('notebook' if 'notebook' in classes else 'log-entry' if 'log-entry' in classes else '')
  elif tag=='time' and 'notebook' in self.div_classes:
   self.times+=1
   if 'log-entry' not in self.div_classes:self.errors.append('time outside log-entry')
 def handle_endtag(self,tag):
  if tag=='div' and self.div_classes:self.div_classes.pop()

class SiteTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.html=(ROOT/'index.html').read_text(encoding='utf-8')
  cls.doc=CheckHTML();cls.doc.feed(cls.html)
 def test_links_are_local_and_resolve(self):
  for href in self.doc.hrefs:
   if href in ('experiments/kepler-227.html','experiments/period-search.html'):
    self.assertTrue((ROOT/href).exists())
   elif href.startswith('https://'):
    self.assertIn(href,{
     'https://github.com/neconeco0306/polymath-public-site',
     'https://neconeco0306.github.io/fracture-visual-evidence/'},href)
   else:
    self.assertTrue(href.startswith('#'),href)
    self.assertIn(href[1:],self.doc.ids,href)
 def test_unique_ids(self):self.assertEqual(len(self.doc.ids),len(set(self.doc.ids)))
 def test_no_secret_or_private_link(self):
  for token in ['polymath-lab1','polymath-lab2','notion.com','api_key','sk-proj','password','@gmail.com','https://docs.google.com/']:
   self.assertNotIn(token,self.html.lower(),token)
 def test_research_directory_and_public_links(self):
  self.assertIn('id="research-index"',self.html)
  self.assertIn('2026.10.17',self.html)
  for public in ['HPA-001','PAA-001','MAINT-001','AEGL-001','EQS-001','ZCAI-001','RG-LOOP-001','EXPLOSION','AASI-001','FRACTURE','SOLIDCRAFT']:
   self.assertIn(public,self.html)
  self.assertIn('https://github.com/neconeco0306/polymath-public-site',self.html)
  self.assertIn('実AI比較0件',self.html)
  self.assertIn('非公開リポジトリ',self.html)
 def test_non_official_warning(self):self.assertIn('大学、研究機関、学会の公式発表ではありません',self.html)
 def test_static_snapshot(self):self.assertIn('2026年10月17日',self.html);self.assertIn('experiments/kepler-227.html',self.html);self.assertIn('experiments/period-search.html',self.html);self.assertIn('リアルタイム同期ではありません',self.html);self.assertIn('Graph固有の性能優位は示せませんでした',self.html)
 def test_scientific_claim_boundary(self):
  for phrase in ['合成デモ','実世界での実証','第三者による再現']:
   self.assertIn(phrase,self.html)
 def test_social_metadata(self):
  for attr in ['og:title','og:description','twitter:card','twitter:title']:
   self.assertTrue(any(m.get('property')==attr or m.get('name')==attr for m in self.doc.meta),attr)
 def test_buttons_and_js(self):
  for key in ['naive-btn','root-btn','declared-count','count-bar','exp-explain']:
   self.assertIn(key,self.doc.ids)

 def test_notebook_entries_are_siblings(self):
  parsed=NotebookStructure();parsed.feed(self.html)
  self.assertGreaterEqual(parsed.entries,3)
  self.assertEqual(parsed.entries,parsed.times)
  self.assertEqual(parsed.errors,[])
 def test_notebook_guard_rejects_nested_entries(self):
  bad='<div class="notebook"><div><div class="log-entry"><time>1</time><div class="log-entry"><time>2</time></div></div></div></div>'
  parsed=NotebookStructure();parsed.feed(bad)
  self.assertIn('nested log-entry',parsed.errors)

if __name__=='__main__':unittest.main(verbosity=2)
