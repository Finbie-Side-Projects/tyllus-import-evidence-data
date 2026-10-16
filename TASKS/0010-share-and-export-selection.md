[DONE]

# Share and export source selections

Existing publisher contexts concern specific CBP/USTR topics and individual product notices; requiring readers to download all records makes those selections hard to reuse. Add restorable filter links and current-result CSV/JSON exports to the existing explorer in all four languages. This is an inferred reader need, not a publisher request or an earned backlink.

Keep export selection independent of pagination. Preserve original JSON records and source snapshot provenance; protect spreadsheet CSV cells from formula execution. Validate incoming filter values, preserve context when switching language, keep every notice readable without JavaScript, and make no new network calls. Do not change the underlying source snapshot in this implementation step.

Verify local behavior, official source agreement, publication and live filtered exports before completion.

Local verification passed: five focused selection/export tests plus all repository checks. Actual Chrome downloads verified16exact CBP records in oldest-first order, agreement of CSV and JSON, a one-record original JSON export, and all16records when downloading from page2without resetting the current page. Empty results disable both exports; EN/TR/IT/ES retain filter context and show localized controls. Published as bb448baaefb4900d6a62d09f22690f93bd14ab12 with successful Pages build https://github.com/Finbie-Side-Projects/tyllus-import-evidence-data/actions/runs/38959653331. The live single-record link restores the selected notice and its actual browser JSON download agrees with the source. Full four-locale, metadata and feed verification is recorded in the run log.
