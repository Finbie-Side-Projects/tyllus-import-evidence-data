# Tyllus U.S. Import Evidence Change Radar data

This repository is the public, versioned distribution mirror for the [Tyllus U.S. Import Evidence Change Radar](https://www.tyllus.com/en/resources/us-import-evidence-change-radar). It makes the source-linked dataset easy to cite, download, inspect and reuse in research workflows.

The current snapshot contains **141 notices** from the U.S. Federal Register and was generated on **2026-10-04**. Tyllus maps each notice to operational evidence domains with a deterministic keyword taxonomy. Every record keeps its official notice URL.

## Download

| Format | Purpose |
| --- | --- |
| [JSON](data/us-import-evidence-change-radar.json) | Complete records and methodology metadata |
| [CSV](data/us-import-evidence-change-radar.csv) | Analysis in spreadsheets and data tools |
| [DCAT 3](data/us-import-evidence-change-radar.dcat.json) | Dataset catalogue harvesting |
| [CSVW](data/us-import-evidence-change-radar.csv-metadata.json) | CSV field definitions and machine-readable schema |
| [Manifest](data/manifest.json) | Capture time, record count, source URLs and SHA-256 checksums |

The [live Radar](https://www.tyllus.com/en/resources/us-import-evidence-change-radar) remains the human-readable source. The repository refreshes from Tyllus's public endpoints every day and commits only when the published files change.

## Provenance

The records come from the [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1) for U.S. Customs and Border Protection, the Federal Maritime Commission, the International Trade Administration, the International Trade Commission and the Office of the United States Trade Representative.

Tyllus adds a transparent evidence-domain classification. These matches are discovery aids. They are not legal advice, compliance decisions, risk scores or statements that a proposal is in force. Always review the linked official notice, its scope and effective date.

## Citation

Use the repository's [`CITATION.cff`](CITATION.cff) or cite the live dataset:

> Tyllus. *U.S. Import Evidence Change Radar*. https://www.tyllus.com/en/resources/us-import-evidence-change-radar

## Updates and corrections

The scheduled refresh script downloads only the four public dataset files, verifies that each response is successful and writes a checksum manifest. Open an issue for a reproducible data or classification problem and include the Federal Register document number.

## Terms

The refresh code and landing page are available under the MIT License. Dataset use is governed separately; see [`DATA-USAGE.md`](DATA-USAGE.md) and the [Tyllus Terms of Use](https://www.tyllus.com/en/terms-of-use).
