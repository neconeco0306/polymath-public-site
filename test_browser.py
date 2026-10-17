"""Read-only headless browser smoke test for the reviewed public landing pages."""
from __future__ import annotations
import html
import json
import re
import shutil
import struct
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class BrowserLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = next((shutil.which(n) for n in ('google-chrome','chromium','chromium-browser') if shutil.which(n)), None)
        cls.build = ROOT/'dist'
        if cls.browser is None:
            raise unittest.SkipTest('No headless Chrome executable; browser QA not claimed')
        if not (cls.build/'index.html').exists():
            raise unittest.SkipTest('Run public release build before browser QA')

    def test_ja_en_layout_and_screenshots(self):
        js = """
        <script>
        (function(){
          const run=()=>{
            const ids=['findings','observations','method','archive'];
            const nav=Array.from(document.querySelectorAll('header a')).map(e=>{
              const r=e.getBoundingClientRect();
              return {left:r.left,right:r.right,width:r.width};
            });
            document.body.setAttribute('data-qa',JSON.stringify({
              width:window.innerWidth,
              documentWidth:document.documentElement.scrollWidth,
              bodyWidth:document.body.scrollWidth,
              lang:document.documentElement.lang,
              cards:document.querySelectorAll('.finding').length,
              anchors:ids.every(i=>!!document.getElementById(i)),
              controls:nav
            }));
          };
          if (document.readyState==='loading') document.addEventListener('DOMContentLoaded',run);
          else run();
        })()
        </script>
        """
        with tempfile.TemporaryDirectory() as t:
            folder=Path(t)
            for name,language in (('index.html','ja'),('en.html','en')):
                data=(self.build/name).read_text(encoding='utf-8')
                staged=folder/name
                staged.write_text(data.replace('</body>',js+'</body>'),encoding='utf-8')
                for width in (390,1440):
                    with self.subTest(page=name,width=width):
                        screenshot=folder/f"{language}-{width}.png"
                        args=[self.browser,'--headless=new','--no-sandbox','--disable-gpu',
                              '--disable-dev-shm-usage','--hide-scrollbars',
                              '--force-device-scale-factor=1',f'--window-size={width},900',
                              '--run-all-compositor-stages-before-draw','--virtual-time-budget=1500',
                              f'--screenshot={screenshot}','--dump-dom',staged.as_uri()]
                        output=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=35)
                        self.assertEqual(output.returncode,0,output.stderr[-1600:])
                        m=re.search(r'data-qa="([^"]+)"',output.stdout)
                        self.assertIsNotNone(m,output.stdout[-300:])
                        stats=json.loads(html.unescape(m.group(1)))
                        self.assertEqual(stats['lang'],language)
                        self.assertEqual(stats['cards'],6)
                        self.assertTrue(stats['anchors'])
                        self.assertLessEqual(stats['documentWidth'],stats['width']+2,stats)
                        self.assertLessEqual(stats['bodyWidth'],stats['width']+2,stats)
                        self.assertTrue(all(v['width']>0 for v in stats['controls']))
                        self.assertTrue(screenshot.exists())
                        pic=screenshot.read_bytes()
                        self.assertGreater(len(pic),2500)
                        self.assertEqual(pic[:8],b'\\x89PNG\\r\\n\\x1a\\n')
                        image_width,image_height=struct.unpack('>II',pic[16:24])
                        self.assertGreaterEqual(image_width,390 if width==390 else 1200)
                        self.assertGreater(image_height,400)
                        print(f"BrowserQA {language} requested={width} viewport={stats['width']} "
                              f"document={stats['documentWidth']} screenshot={image_width}x{image_height}")

if __name__=='__main__':
    unittest.main(verbosity=2)
