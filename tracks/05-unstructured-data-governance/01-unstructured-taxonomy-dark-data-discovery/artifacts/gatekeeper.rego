package enterprise.data.ingestion

import future.keywords.in

default allow = false

# Gatekeeper Policy: Ingest documents only if entropy, classification, and metadata meet invariants
allow {
    input.classification != "restricted"
    valid_entropy_bounds
    valid_media_kind
    has_mandatory_metadata
}

valid_entropy_bounds {
    input.shannon_entropy >= 2.8
    input.shannon_entropy <= 6.0
}

valid_media_kind {
    allowed_kinds := ["text/clean", "image/scanned", "audio/voice", "text/code", "application/sheet"]
    input.media_kind in allowed_kinds
}

has_mandatory_metadata {
    input.metadata.data_owner != ""
    input.metadata.retention_period_days > 0
    count(input.metadata.data_owner) >= 3
}
