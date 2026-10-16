[TODO]

# Keep source metadata and derived feeds in the same publication

Refresh the October16 18:00UTC public snapshot metadata. All167 source records are unchanged. Preserve original record text, previous dated releases and stable RSS item identities.

The existing manual refresh workflow rebuilds and verifies RSS but omits the feeds directory from its publication commit. Include that generated directory in the same commit as data and localized pages so a workflow run cannot publish newer metadata with older feeds. Do not add or resume a recurring schedule. Verify the complete repository and live publication before completion.
