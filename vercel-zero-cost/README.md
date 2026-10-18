# POLYMATH — Zero-Cost AI Lab public site source

- Target production project: `polymath-open-lab` (Vercel), not the Render research homepage.
- Public report file: `index.html` in this directory. This folder is **not** included in the Render public-site release allowlist.
- Last editorial update: 2026-10-19. Underlying research records: 2026-10-17.
- Focus: ZCAI-001 v0.7 local-first Web Retrieval prototype and citation/source integrity checks.
- Reported creator-side results: 92/92 development tests; 30/30 synthetic search cases; 15/15 HTML counterexamples; v0.6 nonempty extraction on 50/50 local technical HTML inputs. An optional Markdown adapter recorded 22/22 simulated/development tests. These are **not** independent certification or commercial parity measurements.
- Not verified: live Web retrieval, independently labelled >=50 legitimate real pages and >=30 queries, provider/OSS parity, semantic citation validity, current target OS and production security, demand, total operating costs, LAB2 verification.
- The embedded demonstration performs local substring matching and SHA-256 hashing only. It makes no external request and does not prove a scientific claim.
- Public HTML intentionally omits private LAB1/LAB2 repository content and private Drive downloads.

## Preview QA record

- HTML publication gate: required research claims/disclaimers present; required section IDs and navigation targets complete; section/article/button/textarea/script/style/main/header/footer tags balanced; duplicate IDs absent; external scripts absent; no private repository URLs.
- Vercel preview deployed from exact GitHub-branch HTML bytes; deployment state READY. The browser-level external HTTP/JS verification is not completed because the Vercel URL fetch connector returned a protection-bypass 403.
- Production publish requires explicit target `polymath-open-lab` and postdeploy READY/alias checks. Never claim an independently tested API service is live: the site is only a research report/demo.
