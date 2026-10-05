# Architecture

The source is the versioned Federal Register compilation in `data/`. `scripts/build_site.py` loads that snapshot and interface dictionaries, then uses the shared `site/page.html` template and `scripts/site_render.py` record renderer to write each locale page. The root provides the English content and forwards to `/en/`.

`assets/styles.css` handles responsive light/dark presentation. `assets/app.js` only reads the pre-rendered DOM to filter, sort and paginate records. It makes no network requests and injects no dataset HTML. All 141 current notices remain available if JavaScript fails or is disabled.

GitHub Pages serves static files from the `main` branch. `scripts/refresh.py` refreshes public data; the refresh workflow rebuilds and verifies the website before committing matching HTML and data. The manifest checksums describe the data files and are preserved when only the website changes.

Verification checks generated-page consistency, every notice/source link and localized interface, internal file links, JSON/CSV record agreement, manifest checksums, JavaScript syntax, and tracked secret patterns. There is no Firebase access, server secret, user upload or authenticated product panel in this project.
