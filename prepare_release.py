"""Build a separate public-only, static website. Does not publish or contact the network."""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import ipaddress
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent


def _public_base(value: str) -> str:
    url = urlsplit(value)
    host = (url.hostname or '').lower()
    if url.scheme != 'https' or not host or url.username or url.password:
        raise ValueError('public URL must be anonymous HTTPS')
    if url.query or url.fragment or url.path not in ('', '/'):
        raise ValueError('use a root homepage URL without query, fragment or path')
    if host in ('localhost', 'example.com', 'example.org', 'example.net') or host.endswith(('.localhost', '.local', '.test', '.invalid')):
        raise ValueError('placeholder or local domain is not publishable')
    try:
        ipaddress.ip_address(host)
    except ValueError:
        if '.' not in host or '..' in host or len(host) > 253:
            raise ValueError('invalid public hostname')
    else:
        raise ValueError('IP literals are not public website domains')
    if url.port not in (None, 443):
        raise ValueError('non-standard port is not suitable for public links')
    return value.rstrip('/') + '/'


def build(base_url: str, output: Path, source: Path = ROOT) -> dict:
    base = _public_base(base_url)
    if output.resolve() == source.resolve():
        raise ValueError('output must be distinct from source directory')
    website = (source / 'index.html').read_text(encoding='utf-8')
    if website.count('</head>') != 1 or '<meta name="twitter:card" content="summary_large_image">' not in website:
        raise ValueError('source site does not match reviewed template')
    if 'name="twitter:image"' in website or 'property="og:image"' in website:
        raise ValueError('source already contains deployed card URL; review before rebuilding')
    # One explicitly reviewed public repository may be linked from a normal href.
    # Mask only this exact href; every other github.com path remains excluded.
    approved_github_href = 'href="https://github.com/neconeco0306/polymath-public-site"'
    inspected_website = website.replace(approved_github_href, 'href="PUBLIC_REVIEWED_SOURCE_REPO"')
    for token in ('notion.com', 'github.com/', 'polymath-lab1', 'polymath-lab2',
                  'sk-proj', 'api_key', 'password', '@gmail.com'):
        if token.lower() in inspected_website.lower():
            raise ValueError('site unexpectedly includes an internal/excluded token')
    card_path = source / 'social-card.png'
    if card_path.exists():
        card = card_path.read_bytes()
    else:
        encoded = (source / 'social-card.png.b64').read_text(encoding='ascii')
        card = base64.b64decode(''.join(encoded.split()), validate=True)
    if not card.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('invalid social card PNG')
    # Content-versioned OG URL prevents stale images in social share caches.
    card_url = base + 'social-card.png?v=' + hashlib.sha256(card).hexdigest()[:16]
    tags = '\n'.join([
        '<link rel="canonical" href="' + html.escape(base, quote=True) + '">',
        '<meta property="og:url" content="' + html.escape(base, quote=True) + '">',
        '<meta property="og:image" content="' + html.escape(card_url, quote=True) + '">',
        '<meta name="twitter:image" content="' + html.escape(card_url, quote=True) + '">',
    ])
    website = website.replace('</head>', tags + '\n</head>')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'index.html').write_text(website, encoding='utf-8')
    (output / 'social-card.png').write_bytes(card)
    # Only the separately reviewed, source-attributed experiment is publishable.
    experiment = source / 'experiments' / 'kepler-227.html'
    if not experiment.is_file():
        raise ValueError('public experiment is missing; failing closed')
    exhibit = experiment.read_text(encoding='utf-8')
    for token in ('<title>見えない惑星の影を読む', 'NASA Exoplanet Archive', '64,814', 'f7185dd055fc7993469bb788816be6f592751a38'):
        if token not in exhibit:
            raise ValueError('experiment failed provenance/identity check')
    for token in ('sk-proj', 'api_key', 'password', '@gmail.com', 'neconeco0306/'):
        if token in exhibit.lower():
            raise ValueError('experiment accidentally contains a private token')
    (output / 'experiments').mkdir(parents=True, exist_ok=True)
    (output / 'experiments' / 'kepler-227.html').write_text(exhibit, encoding='utf-8')
    second = source / 'experiments' / 'period-search.html'
    second_html = second.read_text(encoding='utf-8')
    for token in ('FIELD EXPERIMENT 002', 'f7185dd055fc7993469bb788816be6f592751a38',
                  '9.4874', '厳格な盲検ではありません', '新しい惑星を発見した'):
        if token not in second_html:
            raise ValueError('second public experiment provenance or qualification missing')
    for token in ('sk-proj', 'api_key', 'password', '@gmail.com', 'neconeco0306/'):
        if token in second_html.lower():
            raise ValueError('second experiment contains a private token')
    (output / 'experiments' / 'period-search.html').write_text(second_html, encoding='utf-8')
    # The bilingual landing pages are separately reviewed public-only summaries.
    # Keep legacy pages available rather than silently dropping older research context.
    for name, expected_lang, marker_text in (
        ('en.html', 'en', 'Six findings, explained simply.'),
        ('archive.html', 'ja', 'id="research-index"'),
    ):
        file_path = source / name
        if not file_path.is_file():
            raise ValueError('missing reviewed public page: ' + name)
        content = file_path.read_text(encoding='utf-8')
        if 'lang="' + expected_lang + '"' not in content or marker_text not in content:
            raise ValueError('public page identity check failed: ' + name)
        if content.count('</html>') != 1 or content.count('</head>') != 1:
            raise ValueError('invalid HTML document structure: ' + name)
        inspected = content.replace(approved_github_href, 'href="PUBLIC_REVIEWED_SOURCE_REPO"')
        for token in ('notion.com', 'github.com/', 'polymath-lab1',
                      'polymath-lab2', 'sk-proj', 'api_key', 'password', '@gmail.com'):
            if token.lower() in inspected.lower():
                raise ValueError('public page contains excluded text: ' + name)
        (output / name).write_text(content, encoding='utf-8')
    data = {
        'schema': 'polymath-public-site-release-v1',
        'canonical_url': base,
        'release_type': 'public-static-review-only',
        'published': False,
        'files': {p: hashlib.sha256((output / p).read_bytes()).hexdigest() for p in ('index.html', 'en.html', 'archive.html', 'social-card.png', 'experiments/kepler-227.html', 'experiments/period-search.html')},
        'claims': 'synthetic demos and local software testing only; no independent scientific verification',
    }
    (output / 'release-manifest.json').write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True, help='Confirmed public HTTPS root URL')
    parser.add_argument('--out', required=True, type=Path, help='Isolated output directory')
    args = parser.parse_args()
    result = build(args.url, args.out)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
