# Sacred Atlas for Educators — Git-managed preview v0.7.1

This directory contains a static, non-transactional educational service inquiry site and lesson sample. Intended for Render Static Sites.

## Deployment
- Publish directory: `sacred-atlas-educators` (dedicated folder on the isolated Git branch)
- Build command: `echo "Sacred Atlas static assets ready"`
- Branch: `sacred-atlas/educators-v07`
- No backend, analytics, checkout, customer database, or sensitive religious-data collection.
- The only inquiry entry point opens the visitor's email app via `mailto:`; sending is always the visitor's action.
- No order or payment is collected. The 19,800 JPY figure is a tentative service quote for a future pilot, subject to scope, review, legal and tax readiness.

## Release cautions
- Content is a prototype, not endorsed by any religious institution. An independent subject expert review is not complete.
- Japanese online-sales disclosures and identity / privacy information require review before taking binding orders. Do not expose unconfirmed home address in source.
- The sales site is separate from the free educational PWA at `https://sacred-atlas-ten.vercel.app/`.
- The public email address was explicitly approved by the owner for the inquiry page.

## Source of truth
Google Drive `/Sacred Atlas/release-v0.7` and the GitHub branch named above. Source branch uses isolated namespace and files under the `sacred-atlas-educators/` folder to avoid changing `main` or unrelated projects.
