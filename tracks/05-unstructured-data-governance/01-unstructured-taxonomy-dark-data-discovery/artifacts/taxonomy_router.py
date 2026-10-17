#!/usr/bin/env python3
"""
Unstructured Data Taxonomy & Ingestion Router
Evaluates MIME profiles and character-level Shannon entropy to filter dark data
and corrupted binaries before compute-heavy chunking and vector embedding.
"""

from collections import Counter
from datetime import datetime, timezone
from enum import StrEnum
import math
import mimetypes
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, computed_field


class DataClassification(StrEnum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class MediaKind(StrEnum):
    TEXT_CLEAN = "text/clean"
    SCANNED_IMAGE = "image/scanned"
    AUDIO_RECORDING = "audio/voice"
    STRUCTURED_SPREADSHEET = "application/sheet"
    CODE_DOCUMENT = "text/code"
    UNKNOWN_DARK_DATA = "application/unknown"


class IngestionMetadata(BaseModel):
    data_owner: str = Field(..., min_length=3)
    retention_period_days: int = Field(default=365, ge=1)
    business_unit: str = Field(default="engineering")
    is_customer_facing: bool = False


class IngestionDocument(BaseModel):
    document_id: str
    source_uri: str
    raw_payload: bytes
    declared_mime: Optional[str] = None
    metadata: IngestionMetadata
    classification: DataClassification = DataClassification.INTERNAL
    discovered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @computed_field
    @property
    def detected_mime(self) -> str:
        """Sniff MIME type from URI filename heuristics."""
        mime, _ = mimetypes.guess_type(self.source_uri)
        return mime or self.declared_mime or "application/octet-stream"

    @computed_field
    @property
    def shannon_entropy(self) -> float:
        """
        Calculates normalized character Shannon entropy in bits per byte.
        Formula: H(X) = - sum( P(x) * log2(P(x)) )
        Natural language typically exhibits 3.0 <= H(X) <= 5.8.
        Encrypted/compressed binaries exhibit H(X) > 6.5.
        Repetitive noise or blank scans exhibit H(X) < 2.5.
        """
        if not self.raw_payload:
            return 0.0
        length = len(self.raw_payload)
        counts = Counter(self.raw_payload)
        return -sum(
            (count / length) * math.log2(count / length)
            for count in counts.values()
        )

    @computed_field
    @property
    def media_kind(self) -> MediaKind:
        """Classifies media based on MIME sniffing and entropy."""
        mime = self.detected_mime.lower()
        if mime.startswith("text/") or mime in ("application/pdf", "application/msword"):
            # Check for binary camouflage
            if self.shannon_entropy > 6.5:
                return MediaKind.UNKNOWN_DARK_DATA
            if "python" in mime or "json" in mime or "yaml" in mime or self.source_uri.endswith((".py", ".json", ".yaml")):
                return MediaKind.CODE_DOCUMENT
            return MediaKind.TEXT_CLEAN
        elif mime.startswith("image/"):
            return MediaKind.SCANNED_IMAGE
        elif mime.startswith("audio/"):
            return MediaKind.AUDIO_RECORDING
        elif "excel" in mime or "spreadsheet" in mime or self.source_uri.endswith((".xlsx", ".csv")):
            return MediaKind.STRUCTURED_SPREADSHEET
        return MediaKind.UNKNOWN_DARK_DATA

    def evaluate_ingestion_eligibility(self) -> tuple[bool, str]:
        """
        Enforces gatekeeper invariant:
        Rejects restricted data, unclassified dark data, and corrupted entropy profiles.
        """
        if self.classification == DataClassification.RESTRICTED:
            return False, "GATEKEEPER_REJECT: Restricted data classification prohibited in standard vector index"
        
        if self.media_kind == MediaKind.UNKNOWN_DARK_DATA:
            return False, "GATEKEEPER_REJECT: Dark data cannot be parsed without dedicated deep decoder"

        # Entropy safety bounds for natural text and code
        if self.media_kind in (MediaKind.TEXT_CLEAN, MediaKind.CODE_DOCUMENT):
            if self.shannon_entropy < 2.8:
                return False, f"GATEKEEPER_REJECT: Low-entropy boilerplate or empty OCR scan (H={self.shannon_entropy:.2f})"
            if self.shannon_entropy > 6.0:
                return False, f"GATEKEEPER_REJECT: High-entropy binary payload detected (H={self.shannon_entropy:.2f})"

        return True, "GATEKEEPER_ACCEPT"


if __name__ == "__main__":
    # Self-test demonstration
    valid_text = (
        "Enterprise data governance ensures high data quality, compliance with regulations "
        "such as GDPR and HIPAA, and lineage tracking throughout the AI data lifecycle."
    ).encode("utf-8")
    
    doc = IngestionDocument(
        document_id="doc-test-101",
        source_uri="s3://enterprise-lake/docs/compliance_policy.txt",
        raw_payload=valid_text,
        metadata=IngestionMetadata(data_owner="sec-ops-team", retention_period_days=730)
    )
    
    is_valid, reason = doc.evaluate_ingestion_eligibility()
    print(f"Document: {doc.document_id}")
    print(f"MIME: {doc.detected_mime} | Entropy: {doc.shannon_entropy:.3f} bits/byte | Media: {doc.media_kind}")
    print(f"Status: {is_valid} ({reason})")
    assert is_valid, "Valid document must pass ingestion gate"
