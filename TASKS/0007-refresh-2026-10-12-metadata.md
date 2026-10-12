[DONE]

# Synchronize the 12 October public snapshot metadata

The current public source is generated at 06:00 UTC on 12 October 2026. It retains the same 163 records as the 8 October evening snapshot: no added, absent or changed notice records. Synchronize the public distribution metadata, manifest, derived feeds and localized pages without implying that unchanged notices were newly published.

Preserve stable source document GUIDs in RSS. Keep the 4 October Zenodo archive and 8 October dated releases tied to their original versions. Verify generated pages, source/data consistency, live file responses and search before closing the task.

Completed 12 October 2026. The original 163 notice records and CSV rows are unchanged; JSON/DCAT/CSVW snapshot metadata, the manifest, generated locale pages and feed build dates now match the 06:00 UTC public source. RSS item GUIDs and ordering remained identical, so unchanged records were not assigned new identities.

Local verification passed. Implementation commit `d3ce300a797c78b497b5fd654635e958ddac16d6` was published with [successful Pages build](https://github.com/Finbie-Side-Projects/tyllus-import-evidence-data/actions/runs/38238688447). All four live language pages, four data files, manifest and both feeds matched the local files. Live search for `2026-20650` returned exactly one source record; reset restored all 163. No new dated release or catalogue PR was necessary for unchanged notice contents.
