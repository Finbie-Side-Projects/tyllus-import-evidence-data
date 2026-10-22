# CBP consultation response worksheet

This optional Tyllus worksheet retains all 64 numbered questions in the official
2 September 2026 advance notice, *Heightened Import Disclosures for Supply Chain
Visibility*, document 2026-17926, docket USCBP-2026-1058, 91 FR 56408–56414.

Official source: https://www.govinfo.gov/content/pkg/FR-2026-09-02/html/2026-17926.htm

The original notice states a 1 December 2026 comment deadline. Check the current
official docket for subsequent changes before submitting a response. This
worksheet neither establishes a requirement nor submits comments to an agency.

Download `response-worksheet.csv`, retain the source columns, and fill the blank
columns locally. Assign a response owner and record actual evidence, measurement
period, sample size, time/cost units and assumptions. Distinguish measured values
from estimates; do not treat a blank field as zero or a missing answer as proof of
noncompliance. No example company facts, answers or savings are supplied.

`official-source.html` is the retained public government source. `questions.json`
records its SHA-256 and the normalized question text. Only line wrapping and
pagination markers are removed; wrapped hyphenated words are joined. Government
ASCII typography is retained. Official section names and question wording stay in
English; the four site interfaces explain that boundary. Per-question PDF links
open the page where the question starts; Q22 and Q61 continue onto the next page.

The eleven blank response columns are Tyllus worksheet additions, not government
fields. There is no login, upload, tracking of responses, or automatic submission.
Do not put confidential shipment or personal information into a public comment
without reviewing the agency's publication notice and obtaining appropriate advice.
This is a preparation aid, not legal advice or an official CBP product.

Rebuild with `python3 scripts/build_site.py`; verify with
`python3 scripts/verify.py`. Source status and terms are explained in
[`DATA-USAGE.md`](../../DATA-USAGE.md). No new license over government text is claimed.

## Team workbook

`response-workbook.xlsx` is an optional English Excel version. The Questions tab
retains the same 64 official questions and page URLs. The Responses tab has 11
blank local input fields per question, filtered tables, review/measurement
dropdowns, and formula-based next preparation steps and counts. No measured
company values or example answers are supplied. Blank numeric inputs remain
blank, and costs are not summed across currencies. Review counts describe
preparation only, not legal compliance or a submitted comment.

Assign an owner, draft a response and add an evidence reference or explain why
evidence is unavailable. Mark the draft Reviewed only after your own review.
Not answering is an explicit scope decision, separate from a reviewed response.
The next-step formula continues to show missing owner/draft/evidence even if
Reviewed was selected early. Source URLs are plain text and may be copied into
a browser; the workbook does not use hyperlink formulas or macros.

The public workbook is blank. Fill it locally and keep your completed copy
private. It does not upload responses, file comments, or change official dates.
Its numeric calculations were checked with representative edits and restored
to blank inputs before publication. Native Excel behavior was not separately
tested. The normal site verifier checks the exported source rows, blank input
fields, formula presence and categorical validations. Regenerate and review
the workbook whenever the retained source questions change.
