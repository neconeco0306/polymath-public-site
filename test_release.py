import base64
import hashlib
import tempfile
import unittest
from pathlib import Path
from prepare_release import build, _public_base

ROOT = Path(__file__).resolve().parent

class ReleaseTests(unittest.TestCase):
    def test_rejects_bad_or_private_urls(self):
        for u in ('http://polymath.ai', 'https://localhost', 'https://example.com',
                  'https://192.168.0.1', 'https://foo.test', 'https://user:pass@polymath.ai',
                  'https://polymath.ai/site/', 'https://polymath.ai/?token=1',
                  'https://polymath.ai/#link', 'https://polymath.ai:8443'):
            with self.subTest(u=u), self.assertRaises(ValueError):
                _public_base(u)
    def test_https_base_normalization(self):
        self.assertEqual(_public_base('https://research.polymath.invalid-site.net'),
                         'https://research.polymath.invalid-site.net/')
    def test_build_from_png_and_metadata(self):
        with tempfile.TemporaryDirectory() as t:
            out = Path(t) / 'dist'
            data = build('https://research.polymath.invalid-site.net/', out)
            html = (out/'index.html').read_text()
            card_hash = hashlib.sha256((out/'social-card.png').read_bytes()).hexdigest()[:16]
            self.assertIn(f'content="https://research.polymath.invalid-site.net/social-card.png?v={card_hash}"',html)
            self.assertIn('rel="canonical"',html)
            self.assertEqual(data['canonical_url'],'https://research.polymath.invalid-site.net/')
            self.assertFalse(data['published'])
            for name,digest in data['files'].items():
                self.assertEqual(hashlib.sha256((out/name).read_bytes()).hexdigest(),digest)
    def test_build_from_base64_fallback(self):
        with tempfile.TemporaryDirectory() as t:
            src=Path(t)/'src';src.mkdir()
            (src/'index.html').write_bytes((ROOT/'index.html').read_bytes())
            for page in ('en.html', 'archive.html'):
                (src/page).write_bytes((ROOT/page).read_bytes())
            (src/'experiments').mkdir()
            (src/'experiments/kepler-227.html').write_bytes((ROOT/'experiments/kepler-227.html').read_bytes())
            (src/'experiments/period-search.html').write_bytes((ROOT/'experiments/period-search.html').read_bytes())
            (src/'social-card.png.b64').write_text(base64.b64encode((ROOT/'social-card.png').read_bytes()).decode())
            out=Path(t)/'dist';build('https://research.polymath.invalid-site.net/',out,src)
            self.assertEqual((out/'social-card.png').read_bytes(),(ROOT/'social-card.png').read_bytes())
    def test_rejects_private_tokens(self):
        with tempfile.TemporaryDirectory() as t:
            src=Path(t)/'src';src.mkdir()
            (src/'index.html').write_text((ROOT/'index.html').read_text()+'github.com/private',encoding='utf-8')
            for page in ('en.html', 'archive.html'):
                (src/page).write_bytes((ROOT/page).read_bytes())
            (src/'experiments').mkdir()
            (src/'experiments/kepler-227.html').write_bytes((ROOT/'experiments/kepler-227.html').read_bytes())
            (src/'experiments/period-search.html').write_bytes((ROOT/'experiments/period-search.html').read_bytes())
            (src/'social-card.png').write_bytes((ROOT/'social-card.png').read_bytes())
            with self.assertRaisesRegex(ValueError,'excluded token'):
                build('https://research.polymath.invalid-site.net/',Path(t)/'dist',src)
    def test_no_overwrite_source(self):
        with self.assertRaises(ValueError):build('https://research.polymath.invalid-site.net/',ROOT)

if __name__ == '__main__':unittest.main(verbosity=2)
