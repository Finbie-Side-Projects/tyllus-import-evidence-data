[DONE]

# Keep the public snapshot current

Requested 6 October 2026: keep the live Tyllus U.S. Import Evidence Change Radar distribution and its catalogue entry current when the underlying data changes.

This update captures the latest available public snapshot, regenerates the localized explorer, removes the hard-coded old count from the README, verifies the generated output, and checks the published result. The regular end-of-run maintenance instruction is stored in the DR work plan rather than adding an unattended GitHub schedule.

Verification: `python3 scripts/verify.py`, `git diff --check`, successful Pages build and live source checks.
