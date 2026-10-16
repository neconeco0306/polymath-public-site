"""Offline Render-specific build contract and negative checks. No network."""
from pathlib import Path
import os, subprocess, tempfile, json, unittest

ROOT = Path(__file__).resolve().parent

class RenderBuildTests(unittest.TestCase):
    def run_build(self, url=None):
        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            for fn in ('index.html','social-card.png.b64','prepare_release.py','test_site.py','test_release.py','render-build.sh'):
                (t/fn).write_bytes((ROOT/fn).read_bytes())
            env=dict(os.environ)
            env.pop('RENDER_EXTERNAL_URL',None)
            if url is not None:
                env['RENDER_EXTERNAL_URL']=url
            p=subprocess.run(['sh','render-build.sh'],cwd=t,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            manifest=None; html=None; valid_asset=False
            if (t/'dist/release-manifest.json').exists():
                manifest=json.loads((t/'dist/release-manifest.json').read_text())
                html=(t/'dist/index.html').read_text()
                valid_asset=(t/'dist/social-card.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
            return p,manifest,html,valid_asset

    def test_auto_inject_render_url(self):
        p,m,html,png=self.run_build('https://polymath-lab.onrender.com')
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(m['canonical_url'],'https://polymath-lab.onrender.com/')
        self.assertIn('content="https://polymath-lab.onrender.com/social-card.png"',html)
        self.assertIn('rel="canonical" href="https://polymath-lab.onrender.com/"',html)
        self.assertTrue(png)
        self.assertTrue('PUBLIC ASSETS ONLY:' in p.stdout)

    def test_missing_render_url_fails_closed(self):
        p,m,_,_=self.run_build()
        self.assertNotEqual(p.returncode,0)
        self.assertIsNone(m)

    def test_http_url_fails_closed(self):
        p,m,_,_=self.run_build('http://insecure.onrender.com')
        self.assertNotEqual(p.returncode,0)
        self.assertIsNone(m)

    def test_placeholder_host_fails_closed(self):
        p,m,_,_=self.run_build('https://example.com')
        self.assertNotEqual(p.returncode,0)
        self.assertIsNone(m)

if __name__=='__main__':unittest.main()