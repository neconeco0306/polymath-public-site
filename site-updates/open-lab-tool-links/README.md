# POLYMATH Open Lab — safe restoration and 100-product directory (2026-10-19)

## Incident and repair
- User reported production homepage broken after earlier creator-suite nav injection.
- Immediately rolled back canonical alias `https://polymath-open-lab.vercel.app/` to pre-change **original deployment `dpl_Az8FhJNeJ8FBFHKfryLEZqwaUdJX`**. Alias change read-back verified.
- Earlier patch `build.mjs` replaced with a **one-shot guarded builder** that fetches original pre-change page at build time, adds one scoped entry inside `<main>`, and checks that removing the new CSS + section restores the **exact original HTML string**.
- Separate searchable page `/creator-suite/` includes **100 existing paid services as reference targets**, grouped into 10 categories; 3 released local tool demos and 97 unstarted candidates. No assertion that 100 sites have been built or that 3 products outperform paid alternatives.

## Links in directory
- https://nilo-morph-lab.onrender.com/
- https://nilo-plotcraft-lab.onrender.com/
- https://nilo-linkloom-lab.onrender.com/

## Build source and verification
- `build.mjs` — fail-closed preservation build (fetches current original alias; rejects unexpectedly short HTML, invalid expected document, already-inserted sections, or any unintended change to original).
- `catalog.html` — accessible, searchable, filtered, responsive standalone directory; 100 references.
- `catalog.json` — complete named reference and status data from earlier 100-product queue.
- `package.json` — dependency-free build via `node build.mjs`.

Local acceptance: mock research HTML preservation + 3 outbound links + 100 candidate items; Chromium responsive layout at 320/390/768/1440px; live 3/candidate 97 filtering, search and no-result state; JS errors 0. Archive: `POLYMATH_OPEN_LAB_REPAIR_20261019.zip` available in conversation.

## Vercel deployed evidence
- Preview `dpl_A9PyEoBXMKrJdkMGKQTXLdWRAsaL` READY (build integrity gate passed).
- Production `dpl_CfWQ7ebvrdFypyk11XLm3hua3CUt` READY.
- `request_promote` applied and canonical alias read-back now points to production `dpl_CfWQ7ebvrdFypyk11XLm3hua3CUt`.
- External HTTP screenshot/body access blocked by current tooling; no independent live-browser visual certification claimed.

## Critical caution
**DO NOT simply rerun this one-shot builder after this deployment:** The canonical live alias now contains the inserted section, and builder intentionally fails against duplicate contents. Migrate or pin the original production HTML as a durable source-controlled asset before future updates; original immutable Vercel deployment ID above is the rollback point. Do not replace research body with guessed markup.

No main branch edit performed in GitHub; branch is review/audit source for separately deployed Vercel project.