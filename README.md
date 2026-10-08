# Tyllus U.S. Import Evidence Change Radar data

This repository is the public, versioned distribution mirror for the [Tyllus U.S. Import Evidence Change Radar](https://www.tyllus.com/en/resources/us-import-evidence-change-radar). The [public website](https://finbie-side-projects.github.io/tyllus-import-evidence-data/en/) lets readers search by product or country, browse topics, and read the notices directly. It includes plain summaries of selected customs updates, full original notice text, dates and links. Review the dataset terms before reuse.

The [current manifest](data/manifest.json) gives the latest snapshot date, record count and checksums. Tyllus maps each notice to operational evidence domains with a deterministic keyword taxonomy. Every record keeps its official notice URL.

## Download

| Format                                                         | Purpose                                                       |
| -------------------------------------------------------------- | ------------------------------------------------------------- |
| [JSON](data/us-import-evidence-change-radar.json)              | Complete records and methodology metadata                     |
| [CSV](data/us-import-evidence-change-radar.csv)                | Analysis in spreadsheets and data tools                       |
| [DCAT 3](data/us-import-evidence-change-radar.dcat.json)       | Dataset catalogue harvesting                                  |
| [CSVW](data/us-import-evidence-change-radar.csv-metadata.json) | CSV field definitions and machine-readable schema             |
| [Manifest](data/manifest.json)                                 | Capture time, record count, source URLs and SHA-256 checksums |
| [RSS — selected notices](feeds/notices.xml)                   | Up to 50 recent notices in the current selection, for feed readers |
| [RSS — USTR](feeds/ustr.xml)                                  | The same format, limited to USTR notices in the selection |

The RSS feeds retain original English titles and abstracts, document IDs, publication dates, official notice/PDF links and the corresponding Tyllus Radar record. Stable document identifiers let readers recognize notices already seen. A feed is refreshed with each dataset build and is not a comprehensive regulatory alert service. Source publication dates have no exact time, so item timestamps are omitted rather than invented.

All notices are rendered directly on this website. JavaScript adds search, agency/topic/type filters, sorting and pagination; complete records remain readable without it. The English interface is the default, with Turkish, Italian and Spanish interfaces. The root forwards to `/en/`.

An on-demand workflow refreshes the repository from Tyllus's public endpoints, rebuilds each locale page, verifies data and pages, and commits only when the published files change.

## Provenance

The records come from the [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1) for U.S. Customs and Border Protection, the Federal Maritime Commission, the International Trade Administration, the International Trade Commission and the Office of the United States Trade Representative.

Tyllus adds a transparent evidence-domain classification. These matches are discovery aids. They are not legal advice, compliance decisions, risk scores or statements that a proposal is in force. Always review the linked official notice, its scope and effective date.

## Citation

The snapshot is archived as [Zenodo record 23147873](https://zenodo.org/records/23147873), with version DOI [10.5281/zenodo.23147873](https://doi.org/10.5281/zenodo.23147873). Use the repository's [`CITATION.cff`](CITATION.cff) or cite the live dataset:

> Tyllus. _U.S. Import Evidence Change Radar_. https://www.tyllus.com/en/resources/us-import-evidence-change-radar

## Updates and corrections

The refresh script downloads only the four public dataset files, verifies that each response is successful and writes a checksum manifest. Open an issue for a reproducible data or classification problem and include the Federal Register document number.

## Terms

The refresh code and landing page are available under the MIT License. Dataset use is governed separately; see [`DATA-USAGE.md`](DATA-USAGE.md) and the [Tyllus Terms of Use](https://www.tyllus.com/en/terms-of-use).

## Website development

Edit `site/page.html`, `assets/`, `locales/` and the render/build scripts. Generated HTML is committed for GitHub Pages. Never edit the generated locale pages by hand.

```sh
python3 scripts/build_site.py
python3 scripts/verify.py
python3 -m http.server 8766 --bind 127.0.0.1
```

Open `http://127.0.0.1:8766/en/`. The build and verification require Python 3.9+ and Node.js. Verification checks all real records, localized interfaces, internal links, public source URLs, the immutable data checksums, CSV counts, JavaScript syntax and secret patterns.

Selected customs-update summaries live in the locale dictionaries and are tied to exact notice IDs. If an updated snapshot omits a featured ID, that card is omitted. The DOI always refers to the archived 4 October 2026 snapshot, not a claim that every future website update is archived under that DOI.
