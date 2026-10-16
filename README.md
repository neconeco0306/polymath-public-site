# POLYMATH — Public Field Notes

This repository is **public-only**. The private POLYMATH LAB1/LAB2 source repositories are separate; do not copy their documents or credentials here.

## Public site

- Canonical homepage: https://polymath-research-jp.onrender.com/
- Field 001: `experiments/kepler-227.html` (known orbital periods, illustrative reprocessing)
- Field 002: `experiments/period-search.html` (post-hoc exploratory period search, NOT a blinded discovery)
- Render: static site; branch `main`, `sh render-build.sh`, publish directory `dist`, autoDeploy disabled.
- Files served: `index.html`, `social-card.png`, `release-manifest.json`, `experiments/kepler-227.html`, `experiments/period-search.html` only.
- `research/` contains optional offline reproduction code and qualified observations; **never serve source or internal evidence** through Render.

## Reproduce

In a clean Python 3.11+ environment, download the two **third-party** Kepler CSVs named in `research/observations.json` from their cited GitHub repository. The scripts refuse input if their Git blob SHA-1 is not exactly the recorded version.

```sh
python3 -m unittest discover -s research -p 'test_*.py' -v
python3 research/period_search.py /path/to/10797460.csv > period_output.json
python3 research/control_scan.py /path/to/10419211.csv > control_output.json
python3 -m unittest discover -p 'test_*.py' -v
RENDER_EXTERNAL_URL=https://polymath-research-jp.onrender.com sh render-build.sh
```

Data conclusions are limited. The analysis is **not** a new exoplanet discovery, independently blinded experiment, official astronomical classifier, or demonstrated real-world scientific novelty. The search range for the half-period was tuned after examining data. The other CSV is labelled `false_positive` only by its third-party folder path, **not** by a verified NASA disposition. SHA-1 identifies exact Git blob bytes but does not authenticate the producer. See `research/REPORT.md`, `research/COUNTEREXAMPLE.md` and `research/observations.json`.

## Update policy

New research artifacts require source/provenance checks, scientific-claim boundaries, unit tests, responsive/browser checks and explicit review before deployment. This stable homepage is intentionally manually updated. Never publish private research code, contacts, account credentials or API keys.
