#!/bin/sh
# Build only reviewed public assets. Never publish parent repository contents.
set -eu
: "${RENDER_EXTERNAL_URL:?RENDER_EXTERNAL_URL must come from Render's service environment}"
# The audited GitHub connector carries the PNG as text; reconstruct it deterministically.
python3 - <<'PYIMG'
from pathlib import Path
import base64, hashlib, struct
encoded=Path('social-card.png.b64').read_text(encoding='ascii')
image=base64.b64decode(''.join(encoded.split()),validate=True)
if image[:8]!=b'\x89PNG\r\n\x1a\n' or struct.unpack('>II',image[16:24])!=(1200,630):
    raise SystemExit('bad public OG image; refusing to build')
p=Path('social-card.png')
if p.exists() and p.read_bytes()!=image:
    raise SystemExit('OG image drift; refusing to build')
p.write_bytes(image)
print('OG image SHA256:',hashlib.sha256(image).hexdigest())
PYIMG
python3 prepare_release.py --url "$RENDER_EXTERNAL_URL" --out dist
python3 -m unittest -q test_site test_release
python3 - <<'PY'
from pathlib import Path
import json
p=Path('dist')
manifest=json.loads((p/'release-manifest.json').read_text(encoding='utf-8'))
assert sorted(p.name for p in p.iterdir()) == ['experiments','index.html','release-manifest.json','social-card.png']
assert manifest['canonical_url'].startswith('https://')
assert sorted(x.name for x in (p/'experiments').iterdir())==['kepler-227.html']
print('PUBLIC ASSETS ONLY:', ', '.join(sorted(x.name for x in p.iterdir())))
PY
