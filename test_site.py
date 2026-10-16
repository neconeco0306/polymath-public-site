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

class SiteTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.html=(ROOT/'index.html').read_text(encoding='utf-8')
  cls.doc=CheckHTML();cls.doc.feed(cls.html)
 def test_links_are_local_and_resolve(self):
  for href in self.doc.hrefs:
   self.assertTrue(href.startswith('#'),href)
   self.assertIn(href[1:],self.doc.ids,href)
 def test_unique_ids(self):self.assertEqual(len(self.doc.ids),len(set(self.doc.ids)))
 def test_no_secret_or_private_link(self):
  for token in ['neconeco0306','notion.com','github.com/','api_key','sk-proj','password','@gmail.com','https://docs.google.com/']:
   self.assertNotIn(token,self.html.lower(),token)
 def test_non_official_warning(self):self.assertIn('大学、研究機関、学会の公式発表ではありません',self.html)
 def test_static_snapshot(self):self.assertIn('2026年10月16日',self.html);self.assertIn('自動更新ではありません',self.html)
 def test_scientific_claim_boundary(self):
  for phrase in ['合成デモ','実世界での実証','第三者による再現']:
   self.assertIn(phrase,self.html)
 def test_social_metadata(self):
  for attr in ['og:title','og:description','twitter:card','twitter:title']:
   self.assertTrue(any(m.get('property')==attr or m.get('name')==attr for m in self.doc.meta),attr)
 def test_buttons_and_js(self):
  for key in ['naive-btn','root-btn','declared-count','count-bar','exp-explain']:
   self.assertIn(key,self.doc.ids)

if __name__=='__main__':unittest.main(verbosity=2)