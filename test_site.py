import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parent
FINDINGS=('missing','noise','kepler','simple','lineage','floor')
LOCAL=('index.html','en.html','archive.html','experiments/kepler-227.html','experiments/period-search.html')
EXTERNAL=('https://github.com/neconeco0306/polymath-public-site','https://neconeco0306.github.io/fracture-visual-evidence/')

class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[];self.links=[];self.meta=[];self.languages=[];self.hreflangs=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.append(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='meta':self.meta.append(a)
        if tag=='html':self.languages.append(a.get('lang'))
        if tag=='link' and a.get('hreflang'):self.hreflangs.append(a['hreflang'])

class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages={}
        for name in ('index.html','en.html'):
            content=(ROOT/name).read_text(encoding='utf-8')
            parser=Scan();parser.feed(content)
            cls.pages[name]=(content,parser)
    def test_complete_bilingual_homepage(self):
        for page,lang in (('index.html','ja'),('en.html','en')):
            content,doc=self.pages[page]
            with self.subTest(page=page):
                self.assertEqual(doc.languages,[lang])
                self.assertEqual(len(doc.ids),len(set(doc.ids)))
                self.assertEqual({'ja','en','x-default'},set(doc.hreflangs))
                for item in FINDINGS:self.assertIn('id="'+item+'"',content)
                self.assertEqual(content.count('class="finding" id='),6)
                self.assertIn('href="archive.html"',content)
                self.assertIn('href="en.html"',content)
                self.assertIn('href="index.html"',content)
    def test_language_and_claim_boundaries(self):
        ja=self.pages['index.html'][0];en=self.pages['en.html'][0]
        for term in ('81.79%', '0.63%', '9.4874', '65.54%', '62.41%', '17 / 300'):
            self.assertIn(term,ja);self.assertIn(term,en)
        self.assertIn('独立した新しい科学的発見として認定',ja)
        self.assertIn('independently replicated new scientific discovery',en)
        self.assertIn('完全な盲検ではない',ja)
        self.assertIn('not a blind discovery',en)
        self.assertIn('大学・研究機関・学会の公式発表ではありません',ja)
        self.assertIn('not an official statement',en)
    def test_local_links_and_whitelist(self):
        for name,(content,doc) in self.pages.items():
            for link in doc.links:
                if link.startswith('#'):
                    self.assertIn(link[1:],doc.ids,(name,link))
                elif link.startswith('https://'):
                    self.assertIn(link,EXTERNAL,(name,link))
                else:
                    self.assertIn(link,LOCAL,(name,link))
                    self.assertTrue((ROOT/link).is_file(),(name,link))
    def test_og_and_mobile(self):
        for name,(content,doc) in self.pages.items():
            attrs={m.get('property') or m.get('name') for m in doc.meta}
            for value in ('og:title','og:description','twitter:card','twitter:title'):
                self.assertIn(value,attrs)
            self.assertIn('@media(max-width:620px)',content)
            self.assertIn('prefers-reduced-motion',content)
    def test_no_private_data_or_scripts(self):
        for name,(content,doc) in self.pages.items():
            lower=content.lower()
            for token in ('polymath-lab1','polymath-lab2','notion.com','api_key','sk-proj','password','@gmail.com','https://docs.google.com/'):
                self.assertNotIn(token,lower,(name,token))
            self.assertNotIn('<script',lower,(name,'unexpected runtime dependency'))
    def test_existing_interactive_experiments_link_back_to_english(self):
        for name in ('kepler-227.html','period-search.html'):
            html=(ROOT/'experiments'/name).read_text(encoding='utf-8')
            self.assertIn('href="../en.html#kepler"',html)
            self.assertIn('Read this experiment in English',html)
            self.assertIn('Interactive chart controls remain in Japanese.',html)
    def test_archive_preserved(self):
        old=(ROOT/'archive.html').read_text(encoding='utf-8')
        for token in ('id="research-index"','HPA-001','PAA-001','MAINT-001','ZCAI-001','FRACTURE','Graph固有の性能優位は示せませんでした'):
            self.assertIn(token,old)

if __name__=='__main__':unittest.main(verbosity=2)
