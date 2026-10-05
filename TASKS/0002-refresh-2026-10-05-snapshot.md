[DONE]

# Refresh the public notice explorer

Requested in the Tyllus DR growth full run on 6 October 2026: perform a useful publication in addition to measuring DR.

The upstream Tyllus public dataset was generated on 5 October at 18:00 UTC and contains 149 notices, while the public explorer still showed the 4 October snapshot with 141. Refresh the committed dataset, regenerate every locale, and publish the new version without inventing or editing the original notices.

## Verification

- The new snapshot includes 15 notice IDs absent from the prior snapshot and removes seven outside the rolling window, for a net gain of eight.
- All 15 newly included Federal Register `officialUrl` links returned HTTP 200.
- `python3 scripts/verify.py` passed for 149 records in all four locales and the root fallback, including data checksums and CSV/JSON consistency.
- Verify the live GitHub Pages deployment and a newly included notice after push.
