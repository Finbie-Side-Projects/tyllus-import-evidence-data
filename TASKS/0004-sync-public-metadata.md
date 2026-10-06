[DONE]

# Synchronize public metadata

Requested as part of the 6 October 2026 end-of-run maintenance instruction. The underlying 149-record JSON and CSV are unchanged. The public DCAT and CSVW documents have newer modification timestamps, so this task refreshes those exact public files and their manifest checksums without changing the data or generated notice pages. It also removes a stale fixed count from `Architecture.md`.

Verification: `python3 scripts/verify.py`, `git diff --check`, successful Pages deployment and live manifest check.
