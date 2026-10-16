[DONE]

# Keep source metadata and derived feeds in the same publication

Refresh the October16 18:00UTC public snapshot metadata. All167 source records are unchanged. Preserve original record text, previous dated releases and stable RSS item identities.

The existing manual refresh workflow rebuilds and verifies RSS but omits the feeds directory from its publication commit. Include that generated directory in the same commit as data and localized pages so a workflow run cannot publish newer metadata with older feeds. Do not add or resume a recurring schedule. Verify the complete repository and live publication before completion.

Completed16October2026. Source snapshot generated18:00UTC retains167identical notice records; JSON/DCAT/CSVW metadata, manifest and RSS build dates were synchronized. All three feeds retain the exact same items, GUIDs, source targets and descriptions. The workflow now stages feeds with generated pages and data. Commit000b1080a440f47d685f2994fbc8dae037bfe642 passed Pages build https://github.com/Finbie-Side-Projects/tyllus-import-evidence-data/actions/runs/38960138210. All15live locale/data/feed/runtime files match the generated files. Prior archives and DOI remain unchanged; no redundant record release was created.
