# POLYMATH — Public Field Notes

This repository is **public-only**. The private POLYMATH LAB1/LAB2 source repositories are separate; do not copy their documents or credentials here.

## Public site

- Canonical homepage: https://polymath-research-jp.onrender.com/
- Field 001: `experiments/kepler-227.html` (known orbital periods, illustrative reprocessing)
- Field 002: `experiments/period-search.html` (post-hoc exploratory period search, NOT a blinded discovery)
- Simplified six-finding summaries and seven qualified October 18–19 research updates (Japanese): `index.html`; corresponding English digest: `en.html`
- Previous Japanese 17-topic research directory: `archive.html` (preserved; not a new scientific finding)
- The two existing interactive astronomy exhibits retain Japanese labels; English findings and cautions are fully translated on `en.html`
- Public source link: `https://github.com/neconeco0306/polymath-public-site` (this repository only, **not** private LAB1/LAB2 code)
- Public work link: `https://neconeco0306.github.io/fracture-visual-evidence/` (an engineering artifact, not an independently verified scientific result)
- Render: static site; branch `main`, `sh render-build.sh`, publish directory `dist`, autoDeploy disabled.
- Files served: `index.html`, `en.html`, `archive.html`, `social-card.png`, `release-manifest.json`, `experiments/kepler-227.html`, `experiments/period-search.html` only.
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

## Research-finding publication boundaries (updated 2026-10-19)

The six numerical stories on the Japanese and English homepage are pre-existing exploratory observations, not an independently validated original discovery. These public-only descriptions intentionally exclude private research paths, artifacts, contributor accounts and unpublished data. The 81.79% initial/noise figure and 0.63% holdout figure come from **separate** Gaussian simulation runs (not paired real-world measurement). The Kepler period was chosen through a post-hoc harmonic check, not strict blind discovery. The simple-rule circuit result uses synthetic classical problems. The source-lineage matcher tied a simple baseline (7/8). The budget-allocation floor's task value is unknown.

Translation parity is regression-tested for all six findings. The existing Japanese-only interactive experiment pages are retained unmodified; an English reader can understand their conclusions on the English homepage, though the interactive controls are not yet translated. Render autoDeploy remains off; merging a PR by itself is not a verified live deployment.

The newer seven-card digest separates exact mathematical/software checks from protocols, exploratory market signals, and an untested mobile-sensor prototype. It contains no private LAB source links. Scores from synthetic or narrowly scoped experiments are not claimed to establish independent scientific discoveries, real-world model performance or revenue. The Render service has `autoDeploy` disabled; merged code is not proof that the public URL was redeployed.
