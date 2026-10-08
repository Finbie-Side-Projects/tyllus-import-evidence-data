[DONE]

# RSS distribution and the 8 October evening snapshot

Refresh the changed public dataset and provide reusable RSS feeds for readers who track customs and USTR developments. Generate both feeds from committed public records during the normal site build; retain original English source text, official links, dates and stable document identifiers. Do not invent publication times or imply exhaustive regulatory coverage. Link the feeds from all four localized interfaces.

Compare the current public snapshot with the previous 156-record version. The 18:00 UTC source contains 163 records: 18 newly included, 11 absent from the rolling selection, and no changes to retained records. Absence from this selection does not establish withdrawal or changed legal effect.

Verify the new official PDFs, data checksums, generated pages, feed XML/source agreement, live search and published feed responses. Keep the archived Zenodo DOI separate from this newer snapshot.

Completed 8 October 2026. All 18 new GovInfo PDFs returned successful PDF responses. Local verification passed for 163 records, four localized pages and the root fallback, RSS XML/source consistency, stable unique GUIDs, file checksums, CSV/JSON agreement, JavaScript syntax and publication-boundary checks.

Published implementation: `835a19784fe9006dd91ad6dac788e9589aefa708`; [Pages build succeeded](https://github.com/Finbie-Side-Projects/tyllus-import-evidence-data/actions/runs/37826985819). The live four locale pages, four dataset files, manifest and both RSS feeds exactly matched the local files. The general feed has 50 records and the USTR feed has 8. Searching `2026-20650` returned one matching proposed-rule record; reset restored all 163. The [dated evening release](https://github.com/Finbie-Side-Projects/tyllus-import-evidence-data/releases/tag/data-2026-10-08-1800) preserves eight public attachments without replacing the earlier same-day snapshot.
