[TODO]

# Rebuild the public evidence explorer

Requested on 5 October 2026: repair the GitHub Pages website, remove “Human-readable source” and show substantive readable content directly.

## Acceptance

- Display all real dataset records with dates, agencies, original summaries, topic classifications and official source/PDF links.
- Provide working search, filters, sort and pagination, with accessible empty states.
- Keep downloads, methodology, checksum provenance and the archived citation.
- Support localized interfaces and responsive light/dark presentation.
- Preserve the dataset and regenerate pages whenever public data refreshes.
- Pass repository verification, publish the change, and verify the live page visually and functionally.

## Verification

- `python3 scripts/verify.py`: passed for 141 records in all four locales and the root fallback, internal links, localized UI, unchanged dataset checksums, CSV/JSON counts, JavaScript syntax and secret scan.
- `python3 -m py_compile`: all four Python scripts passed.
- Prettier formatting check and `git diff --check`: passed.
- Browser: multiword aluminum/China search returned 2 records; Türkiye also matched Turkey and returned 9; CBP filter returned 17; CBP + Rule returned 1; topic shortcut returned 2; no-match/reset states passed.
- Browser: page 2 showed records 13–24; oldest-first sort and featured-notice expansion passed; all four locale transitions passed; no console warnings/errors.
- Responsive: at 375 × 812, document width remained 375 and the first readable update started at 585 px, with its summary visible on the first screen.
- Live publication verification pending.
