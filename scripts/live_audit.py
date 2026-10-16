"""Verify the deployed public website against the local, allowlisted release output.

Only this project's known public HTTPS host is queried. No secrets, accounts or internal APIs.
"""
from __future__ import annotations
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://polymath-research-jp.onrender.com"
DIST = Path("dist")
PAGES = ("index.html", "experiments/kepler-227.html", "experiments/period-search.html", "social-card.png", "release-manifest.json")
PRIVATE = ("research/REPORT.md", "research/observations.json", "prepare_release.py", ".github/workflows/public-site-checks.yml")


def fetch(path: str, attempts: int = 5) -> tuple[int, bytes, dict]:
    assert path and ".." not in path and not path.startswith("/"), path
    url = BASE + "/" + path + "?public-ci=1"
    for i in range(attempts):
        req = urllib.request.Request(url, headers={
            "User-Agent": "POLYMATH-public-release-verifier/1.0",
            "Cache-Control": "no-cache",
            "Accept-Encoding": "identity",
        })
        try:
            with urllib.request.urlopen(req, timeout=24) as response:
                return response.status, response.read(), dict(response.headers)
        except urllib.error.HTTPError as error:
            if error.code in (403, 404, 410):
                return error.code, error.read(), dict(error.headers)
            exc = error
        except (urllib.error.URLError, TimeoutError) as error:
            exc = error
        if i + 1 < attempts:
            time.sleep(3)
        else:
            raise AssertionError(f"public GET did not succeed for {path}: {exc}") from exc
    raise AssertionError("unreachable")


def main() -> None:
    expected = set(PAGES)
    actual = {str(p.relative_to(DIST)) for p in DIST.rglob("*") if p.is_file()}
    assert actual == expected, f"public asset allowlist drift: {sorted(actual ^ expected)}"
    index = (DIST / "index.html").read_text(encoding="utf-8")
    assert 'id="research-index"' in index
    assert 'href="https://github.com/neconeco0306/polymath-public-site"' in index
    manifest = json.loads((DIST / "release-manifest.json").read_text())
    assert set(manifest["files"]) == expected - {"release-manifest.json"}
    for path in PAGES:
        status, data, headers = fetch(path)
        assert status == 200, (path, status)
        digest = hashlib.sha256(data).hexdigest()
        local_digest = hashlib.sha256((DIST / path).read_bytes()).hexdigest()
        assert digest == local_digest, (path, digest, local_digest)
        if path in manifest["files"]:
            assert digest == manifest["files"][path], path
        if path.endswith(".html"):
            assert "html" in headers.get("Content-Type", "").lower(), (path, headers)
        print(f"PASS GET {path} HTTP {status} bytes={len(data)} SHA256={digest[:16]}")

    for path in PRIVATE:
        status, data, _ = fetch(path)
        assert status in (403, 404, 410), (path, status, len(data))
        print(f"PASS BLOCKED {path} HTTP {status}")

    for marker in ("polymath-lab1", "polymath-lab2", "sk-proj", "@gmail.com"):
        assert marker not in index.lower(), marker
    print("PASS public host verified, 5 identical files, 4 blocked internal paths")


if __name__ == "__main__":
    main()
