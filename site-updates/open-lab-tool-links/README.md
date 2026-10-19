# Open Lab navigation: creator tools (2026-10-19)

Target: https://polymath-open-lab.vercel.app/

## Change
Add a keyboard-accessible, mobile-responsive “公開ツールを使ってみる” section near the opening table of contents with outbound links to:
- https://nilo-morph-lab.onrender.com/
- https://nilo-plotcraft-lab.onrender.com/
- https://nilo-linkloom-lab.onrender.com/

## Why the build-time fetch?
The Open Lab is currently a direct-upload Vercel static site, not a GitHub Git integration. The Vercel source-inspection connector returns an incomplete base64 excerpt for the 80KB+ HTML. Reconstructing a replacement file from it would lose the research archive. The reviewed build script fetches the exact published live HTML *once at build time*, checks expected structure, inserts a scoped card section, and writes static output. It never calls the origin at visitor runtime.

## Guardrails
- Fail closed on broken HTTP response, short/unrecognized source, missing placement, or duplicate insertion.
- All existing research content retained verbatim except the new links and CSS; robots.txt retained where available.
- Links use real deployed URLs, noreferrer/noopener, focus-visible styling, mobile single-column layout.
- Source script lives at `site-updates/open-lab-tool-links/build.mjs`; record is a reproducible one-time patch. Running it against the already-updated production page intentionally fails instead of adding duplicates. For subsequent updates, use a pinned original baseline or a proper source-controlled original.
- The production page's previous Vercel deployment was `dpl_Az8FhJNeJ8FBFHKfryLEZqwaUdJX`; current is `dpl_2Ta4Hd3nCTwPZF2N6pY6KmD9uYC5`.

## Observed evidence
- Preview deployment `dpl_HuKaFFrC9SYtszAgeHGvkEYvvC7v`: READY.
- Production deployment `dpl_2Ta4Hd3nCTwPZF2N6pY6KmD9uYC5`: READY, alias `polymath-open-lab.vercel.app` assigned; no alias error.
- 3 local structural tests passed (toc, no-nav fallback, duplicate fail-closed).
- Independent public-browser screenshot/HTTP body readback is blocked in this environment; claim only provider-ready + deterministic build checks, not verified rendering.

## Work stream separation
MORPH, PLOTCRAFT and LINKLOOM are product/creative-tool demos, not research evidence. Their own quality gates remain separate from POLYMATH experiments.
