# POLYMATH Open Lab — Safe 100-item index addition (2026-10-19)

## Result and scope

This is a **non-destructive static-site update** to the user's existing POLYMATH Open Lab at <https://polymath-open-lab.vercel.app/>. It adds a small section near the beginning of the existing content, linking to the three working prototypes and the separate 100-item development directory at `/creator-suite/`.

The original research page is preserved **byte-for-byte apart from the scoped section and its CSS**. Do not replace it with a newly invented landing page or overwrite research artifacts. The 100 services are *references and candidates*, **not 100 built products**. Three prototypes have public demos, 97 items are not started, and **zero products have certified paid-tier superiority**.

## Links

- MORPH: <https://nilo-morph-lab.onrender.com/>
- PLOTCRAFT: <https://nilo-plotcraft-lab.onrender.com/>
- LINKLOOM: <https://nilo-linkloom-lab.onrender.com/>
- Directory: <https://polymath-open-lab.vercel.app/creator-suite/>

## Source of truth and reproduction

The underlying original Open Lab site is *not* hosted in this repository; the earlier Vercel build was a direct HTML upload. We deliberately use the immutable last-known-good deployment `dpl_Az8FhJNeJ8FBFHKfryLEZqwaUdJX` (URL in `build.mjs`) as the first-choice build-time source, with the public production alias as a fail-closed fallback. This avoids recursively copying the previously broken insertions and allows preserving the complete original HTML without rewriting it from a truncated connector response. **The baseline URL must remain accessible or builds must fail; this is a transitional solution, not a permanent source-control substitute.** Long-term, place the *original full HTML source* into Git, review its exact contents, and remove remote-fetch build dependency.

- `build.mjs`: fetch/validate the intact source, inject only the scoped launch section, copy the directory and JSON source, write a build audit; rejects malformed/short/double-patched HTML.
- `reference_100.json`: original reference list of 100 services, with explicit stage metadata.
- `create_catalog.py`: reproducible catalog builder (run from this folder); uses `reference_100.json`, produces `creator_suite_index.html` and `catalog.json`. Copy `creator_suite_index.html` to `catalog.html` after regeneration.
- `catalog.html`: responsive interactive directory; 100 entries across 10 categories, search, filter by three prototype references vs remaining 97.
- `test_site.py`: local Chromium browser acceptance (search, filtering, responsive widths, no JS exceptions) on a fixture homepage.
- `release_validation.py`: structural, provenance and link assertions.
- `mock-original.html`: clearly artificial test fixture for CI; never deploy it as the real site.

## Deployment and evidence

- Previous broken live deployment: `dpl_2Ta4Hd3nCTwPZF2N6pY6KmD9uYC5`. It was rolled back to stable `dpl_Az8FhJNeJ8FBFHKfryLEZqwaUdJX` before this fix.
- First guarded preview failed its build (`dpl_CnF8p35qN32ytFvvsYm6aXD8sPTo`) and was **not** released. Hardened source-fetch/pinned-baseline preview `dpl_GKAcfV6KyjgDMNpMBATxAv9m9gNe` reached READY.
- Production deployment `dpl_3UX64rEi96S9sBDypX1pbbAQ4DYR` reached READY, with alias `polymath-open-lab.vercel.app` assigned and independently read back from Vercel.
- Local isolated tests: PASS, 100 entries, 3 reference demos, 97 backlog, four responsive widths 320/390/768/1440, search and filters. Build audit asserts the exact original markup is recovered when removing only the new section and CSS.
- **Not verified:** A real external HTTP/browser screenshot and navigation on the production alias. Due to outbound-network limitations in this environment, provider READY and local browser fixtures must not be misrepresented as an end-user rendering certification.

## Emergency rollback

Use the authorized Vercel connector `request_rollback` for project `prj_A37kD0t0VIKUZWcoCgASq9Pqimip` to deployment `dpl_Az8FhJNeJ8FBFHKfryLEZqwaUdJX`, then read the exact alias binding with `get_alias`. Verify the site visually in an independent browser before announcing success.

## Production caveat

The public 3 demos are hosted on Render and independently deployed. Their pricing/feature comparisons remain incomplete. The directory advertises only their concrete functions; it must never claim that all 100 candidates are completed or any product outperforms a paid competitor without a fair benchmark.
