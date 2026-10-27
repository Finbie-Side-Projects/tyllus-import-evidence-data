# Architecture

The source is the versioned Federal Register compilation in `data/`. `scripts/build_site.py` loads that snapshot and interface dictionaries, then uses the shared `site/page.html` template and `scripts/site_render.py` record renderer to write each locale page. The root provides the English content and forwards to `/en/`.

`assets/styles.css` handles responsive light/dark presentation. `assets/app.js` only reads the pre-rendered DOM to filter, sort and paginate records. It makes no network requests and injects no dataset HTML. All notices in the committed snapshot remain available if JavaScript fails or is disabled.

GitHub Pages serves static files from the `main` branch. `scripts/refresh.py` refreshes public data; the refresh workflow rebuilds and verifies the website before committing matching HTML and data. The manifest checksums describe the data files and are preserved when only the website changes.

Verification checks generated-page consistency, every notice/source link and localized interface, internal file links, JSON/CSV record agreement, manifest checksums, JavaScript syntax, and tracked secret patterns. There is no Firebase access, server secret, user upload or authenticated product panel in this project.

`scripts/feeds.py` generates three RSS 2.0 distributions during the normal site build: up to 50 latest selected notices, up to 50 USTR-only notices, and up to 50 CBP-only notices. All use only committed public records, preserve original source text, and keep stable Federal Register document GUIDs. Locale pages expose the same English feeds with localized labels and autodiscovery links. Verification parses the feeds and checks source agreement and uniqueness.

Filtered selections are restored from validated URL parameters. The page embeds the same public dataset for local JSON/CSV export; no additional request is made. Pagination changes visibility only; exports include every matching record in the chosen sort order. JSON includes source snapshot and selection provenance. CSV uses the bulk distribution columns with spreadsheet-safe text handling. Language changes retain the selection and notice fragment.

`worksheets/2026-17926/` retains a public official notice and its 64 numbered
questions. `scripts/consultation.py` checks the source hash and normalized wording,
generates an entirely blank response CSV and renders all questions under native
details elements in each locale. It does not change the notice dataset or send
responses anywhere. This supplementary worksheet has its own source notes.

The optional `response-workbook.xlsx` uses the same retained questions with a
separate blank response tab, categorical validation and preparation formulas.
It has no macros, external data connections or response uploads. The verifier
checks source rows, initial input blanks, filter tables and formula presence.
Regeneration is required if retained source questions change.

`data/previously-included-notices.json` retains records that leave the current
source selection. Each entry identifies its prior public source commit, snapshot
date and checksums. Refresh accepts historical entries only from the previously
committed snapshot. They are rendered separately and never added to current
counts, exports or feeds. An exact historical-ID search with no current record
offers the retained Tyllus and official links. Unknown IDs do not create guessed
links, and a record returning to the current selection uses its current result.
