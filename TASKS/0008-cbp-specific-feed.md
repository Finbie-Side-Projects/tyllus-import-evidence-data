[DONE]

# CBP-specific RSS distribution

Customs readers need to track CBP publications without selecting them from an inter-agency feed. The current dataset supports a CBP-only distribution from the same committed public records. Add that feed to the shared build and all four localized discovery pages; retain original titles, official sources and stable document identifiers.

Do not imply complete customs coverage or turn publication dates into invented exact timestamps. Keep the current dataset, previous feeds and archived releases intact. Verify the CBP-only record selection, source links, successful Pages deployment and live explorer behavior before completion.

Live review also found that the interface described the available original abstract as the full notice text. Clarify the source-language hint in all four interfaces: details contain the complete abstract and supplied dates; the full notice remains at the official source.

Completed 12 October 2026. The CBP feed contains all 15 selected CBP notices with stable identifiers and official sources, including the supply-chain disclosure advance notice and Form 5106 enforcement notice. The previous general and USTR feeds and dataset records remained unchanged. Local verification passed; all four live pages and three feeds matched their generated files. The live CBP filter returned 15 records, searching `2026-17926` returned one record, and clearing filters restored all 163.

Published feed commit: `b3dd6875af454228d237c549dcc83557f0dc2f11`; [Pages build succeeded](https://github.com/Finbie-Side-Projects/tyllus-import-evidence-data/actions/runs/38248301024). The abstract/full-notice clarification was published as `95797d08fa02dc42f189d3059a3367b70afa27e0`; [its build succeeded](https://github.com/Finbie-Side-Projects/tyllus-import-evidence-data/actions/runs/38248598304). The public dataset remained identical at the final source check; no new data archive or catalogue correction was needed.
