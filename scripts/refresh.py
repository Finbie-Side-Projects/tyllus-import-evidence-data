#!/usr/bin/env python3
"""Refresh the public Tyllus Radar files and write a checksum manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SOURCES = {
    "us-import-evidence-change-radar.json": "https://www.tyllus.com/data/us-import-evidence-change-radar.json",
    "us-import-evidence-change-radar.csv": "https://www.tyllus.com/data/us-import-evidence-change-radar.csv",
    "us-import-evidence-change-radar.dcat.json": "https://www.tyllus.com/data/us-import-evidence-change-radar.dcat.json",
    "us-import-evidence-change-radar.csv-metadata.json": "https://www.tyllus.com/data/us-import-evidence-change-radar.csv-metadata.json",
}


def fetch(url: str) -> tuple[bytes, dict[str, str | int | None]]:
    request = Request(url, headers={"User-Agent": "Tyllus-open-data-refresh/1.0"})
    with urlopen(request, timeout=30) as response:
        body = response.read()
        if response.status != 200 or not body:
            raise RuntimeError(f"Unexpected response for {url}: {response.status}")
        return body, {
            "status": response.status,
            "content_type": response.headers.get("content-type"),
            "etag": response.headers.get("etag"),
            "last_modified": response.headers.get("last-modified"),
        }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    files = []
    for filename, source_url in SOURCES.items():
        body, headers = fetch(source_url)
        (DATA_DIR / filename).write_bytes(body)
        files.append(
            {
                "file": f"data/{filename}",
                "source_url": source_url,
                **headers,
                "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
            }
        )

    payload = json.loads((DATA_DIR / "us-import-evidence-change-radar.json").read_text())
    manifest = {
        "captured_at": payload.get("generatedAt"),
        "dataset_generated_at": payload.get("generatedAt"),
        "record_count": len(payload.get("notices", [])),
        "schema_version": payload.get("schemaVersion"),
        "taxonomy_version": payload.get("taxonomyVersion"),
        "landing_page": "https://www.tyllus.com/en/resources/us-import-evidence-change-radar",
        "files": files,
    }
    (DATA_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
