---
id: "01-udg-taxonomy-discovery"
title: "Unstructured Data Taxonomy & Dark Data Discovery: Entropy Profiling and Ingestion Gates"
track: "05-unstructured-data-governance"
difficulty: "L300 (Intermediate)"
estimated_minutes: 45
tags:
  - "data-governance"
  - "dark-data"
  - "shannon-entropy"
  - "unstructured-data"
  - "opa"
  - "rego"
  - "pydantic"
---

# Unstructured Data Taxonomy & Dark Data Discovery: Entropy Profiling and Ingestion Gates

> **Executive Summary:** Up to 80% of enterprise cloud storage consists of unclassified "dark data"—scanned images, audio recordings, corrupted binaries, and obsolete drafts. When fed indiscriminately into semantic vector pipelines, dark data causes catastrophic storage cost explosions, vector fragmentation, and severe query hallucinations. By combining lightweight MIME sniffing and character-level Shannon entropy profiling ($3.0 \le H(X) \le 5.8$) with declarative Open Policy Agent (OPA) gatekeepers, platform engineers intercept corrupt artifacts at ingress before tokenization and embedding generation.

---

# 1. Interactive Concept Breakdown

## 1.1 The Production Crucible (The Why Before The How)

In late 2025, a global logistics enterprise initiated an automated knowledge retrieval pipeline over its 15-year-old corporate Amazon S3 data lake comprising 12 million unstructured files. The goal was to provide customer support engineers with an intelligent RAG assistant capable of surfacing historic troubleshooting notes and machinery manuals.

The ingestion workers were configured with a naive recursive file-watcher that passed every discovered object key directly into a distributed text-chunker and embedding inference service.

```
TIME-SERIES POST-MORTEM (DARK DATA INGESTION MELTDOWN)
Day 01 ── [Crawler Starts] ── 12M Objects Queued ── Baseline Vector DB Heap: 32 GB
Day 03 ── [Corrupted Scans Ingested] ── 4.2M Zero-Entropy OCR Docs Ingested
Day 05 ── [Audio/CAD Files Ingested] ── Worker Nodes Experience Continuous OOM Failures
Day 07 ── [Index Corruption] ── Top-K Search Precision Plummets from 91% to 14%
Day 10 ── [Financial Audit] ── Monthly Vector GPU Compute Projected at $180,000/month
```

### The Root-Cause Chain
1. **Unchecked Binary Ingestion:** Over 400,000 binary CAD drawings and corrupted scanned PDFs with inverted contrast were processed. The OCR parsers emitted hundreds of gigabytes of empty strings or repetitive non-ASCII character noise.
2. **High-Entropy Token Space Pollution:** The embedding models converted random character noise into dense vector representations. These noise vectors clustered densely near the center of the vector index manifold, polluting the cosine distance calculation.
3. **Context Window Contamination:** When support staff queried standard technical terms (e.g., *"Hydraulic pump gasket torque spec"*), the vector store retrieved noise chunks containing broken OCR tokens, forcing the LLM into severe hallucinations or outputting garbled characters.
4. **Economic Collapse:** The company expended over **$180,000** in GPU inference hours embedding files that contained zero actionable semantic information.

To prevent dark data pollution, enterprise ingestion pipelines must enforce a **Stateless Ingestion Gatekeeper**: every unstructured artifact must undergo MIME sniffing and mathematical entropy profiling prior to invoking expensive downstream chunkers.

---

## 1.2 First-Principles Mental Model: Shannon Entropy of Text Manifolds

How can an ingestion service reliably distinguish high-value natural language from encrypted binaries or corrupted OCR noise without running an expensive foundation model? The theoretical foundation is **Normalized Character Shannon Entropy**:

$$H(X) = - \sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$

Where:
- $X$ is the byte stream or character sequence of the incoming document.
- $P(x_i)$ is the empirical probability of character $x_i$ occurring in the payload.
- $H(X)$ measures the average information density in bits per byte.

```
THE SHANNON ENTROPY INFORMATION DENSITY SPECTRUM
Bits/Byte
^
|   8.0 +-------------------------------------------------------------------+
|       | Encrypted Files, Compressed Binaries (.zip, .tar.gz, .exe, CAD)   | (H > 6.2) -> REJECT
|   6.0 +-------------------------------------------------------------------+
|       | Structured Source Code & Dense Technical Docs (.py, .json, .yaml) | (5.2 - 6.0) -> ROUTE CODE
|   4.5 +-------------------------------------------------------------------+
|       | Standard Natural Language (English Prose, Contracts, Memos)       | (3.0 - 5.2) -> PASS CHUNKER
|   2.5 +-------------------------------------------------------------------+
|       | Repetitive OCR Noise, Null-Byte Spacers, Corrupted Blank Scans    | (H < 2.8) -> REJECT
|   0.0 +-------------------------------------------------------------------+
+-----------------------------------------------------------------------------> Byte Distribution
```

### The Core Invariants
1. **Natural Language Bounds:** Natural language text adheres to Zipf's Law distribution, naturally bounding its Shannon entropy between **3.0 and 5.8 bits/byte**.
2. **High-Entropy Binary Defense ($H > 6.2$):** Compressed archives and encrypted binaries have nearly uniform byte distributions ($H \approx 8.0$), allowing instant CPU-level rejection in $O(N)$ time.
3. **Low-Entropy Boilerplate Defense ($H < 2.8$):** Empty documents, repetitive null characters, or failed OCR scans collapse toward minimal entropy, allowing immediate filtering before vector storage.

---

# 2. Visual Architecture

## 2.1 Control Plane vs. Data Plane Ingestion Gatekeeper

```
+---------------------------------------------------------------------------------------------------+
|                           CONTROL PLANE: POLICY & CATALOG ORCHESTRATION                           |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [ Data Lake Catalog ] -----> [ Ingestion Gatekeeper (OPA) ] <---- [ CISO Security Policies ]     |
|  (S3 / Azure Blob / GCS)      - Validates: Classification != Restricted                           |
|                               - Validates: Retention & Owner Metadata                             |
|                               - Validates: Entropy Bounds [3.0, 5.8]                              |
|                                            |                                                      |
+--------------------------------------------|------------------------------------------------------+
                                             | Emits Ingestion Approval Ticket
                                             v
+---------------------------------------------------------------------------------------------------+
|                             DATA PLANE: CONTENT ROUTING & PARSING                                 |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|                     +----------------------------------+                                          |
|                     | S3 Event Notification Ingress    |                                          |
|                     +-----------------+----------------+                                          |
|                                       |                                                           |
|                                       v                                                           |
|                     +----------------------------------+                                          |
|                     | Fast Stream Profiler (Worker)    |                                          |
|                     | - Sniff MIME Type from Magic/URI |                                          |
|                     | - Compute Shannon Entropy H(X)   |                                          |
|                     +-----------------+----------------+                                          |
|                                       |                                                           |
|                   +-------------------+-------------------+                                       |
|                   | (Passed Gate)                         | (Violated Invariant)                  |
|                   v                                       v                                       |
|        [ Media Router Dispatcher ]              [ Quarantine Dead-Letter S3 ]                     |
|                   |                             - Emit Alert to Data Stewards                     |
|         +---------+---------+                   - Retain Telemetry Audit Record                   |
|         |                   |                                                                     |
|         v (Clean Text)      v (Images/Scans)                                                      |
|   [ Chunking Engine ]  [ Tesseract / VLM ]                                                        |
|         |                   |                                                                     |
|         +---------+---------+                                                                     |
|                   |                                                                               |
|                   v                                                                               |
|       [ Semantic Embedding Bus ] ===> [ Production Vector DB ]                                    |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

---

# 3. Real-World Code & Configuration

The complete reference implementation consists of a typed Pydantic v2 metadata model evaluating character entropy, paired with an Open Policy Agent (OPA) Rego policy rule.

### 3.1 Pydantic V2 Ingestion Router (`artifacts/taxonomy_router.py`)

```python
from collections import Counter
from datetime import datetime, timezone
from enum import StrEnum
import math
import mimetypes
from typing import Optional
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
        mime, _ = mimetypes.guess_type(self.source_uri)
        return mime or self.declared_mime or "application/octet-stream"

    @computed_field
    @property
    def shannon_entropy(self) -> float:
        """H(X) = - sum( P(x) * log2(P(x)) )"""
        if not self.raw_payload:
            return 0.0
        length = len(self.raw_payload)
        counts = Counter(self.raw_payload)
        return -sum((count / length) * math.log2(count / length) for count in counts.values())

    @computed_field
    @property
    def media_kind(self) -> MediaKind:
        mime = self.detected_mime.lower()
        if mime.startswith("text/") or mime in ("application/pdf", "application/msword"):
            if self.shannon_entropy > 6.5:
                return MediaKind.UNKNOWN_DARK_DATA
            if "python" in mime or "json" in mime or self.source_uri.endswith((".py", ".json")):
                return MediaKind.CODE_DOCUMENT
            return MediaKind.TEXT_CLEAN
        elif mime.startswith("image/"):
            return MediaKind.SCANNED_IMAGE
        return MediaKind.UNKNOWN_DARK_DATA

    def evaluate_ingestion_eligibility(self) -> tuple[bool, str]:
        if self.classification == DataClassification.RESTRICTED:
            return False, "GATEKEEPER_REJECT: Restricted data classification prohibited"
        if self.media_kind == MediaKind.UNKNOWN_DARK_DATA:
            return False, "GATEKEEPER_REJECT: Dark data cannot be parsed without dedicated decoder"
        if self.media_kind == MediaKind.TEXT_CLEAN:
            if self.shannon_entropy < 2.8:
                return False, f"GATEKEEPER_REJECT: Low-entropy boilerplate (H={self.shannon_entropy:.2f})"
            if self.shannon_entropy > 6.0:
                return False, f"GATEKEEPER_REJECT: High-entropy binary payload (H={self.shannon_entropy:.2f})"
        return True, "GATEKEEPER_ACCEPT"
```

### 3.2 Declarative Gatekeeper Policy (`artifacts/gatekeeper.rego`)

```rego
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
```

---

# 4. Edge Cases, Failure Modes & Trade-offs

## 4.1 Comparative Architectural Decision Matrix

| Strategy | When to Use | When It Breaks Down | Triage Runbook Indicator |
| :--- | :--- | :--- | :--- |
| **Heuristic MIME Sniffing** | High-throughput ingress (>10k docs/sec), minimal CPU overhead | Fails on polyglot files (e.g., zip files disguised as PDFs) | Downstream parser `CorruptedFileException` spikes |
| **Shannon Character Entropy** | Universal pre-filtering of dark data, encrypted files, and OCR noise | Flags legitimate minified JavaScript or dense Base64 strings as binaries | High rejection rate on `.json` or `.min.js` configuration objects |
| **VLM-Assisted Media Classification** | Mixed scanned reports with embedded charts and handwriting | Cost-prohibitive (>500ms/page, $0.02/call) for multi-million file lakes | Ingestion queue lag and GPU worker OOM events |

## 4.2 Operational Triage Runbook

```
+---------------------------------------------------------------------------------------------------+
|                        OPERATIONAL TRIAGE RUNBOOK: INGESTION GATEKEEPER                           |
+---------------------------------------------------------------------------------------------------+
| SYMPTOM: Ingestion queue depth growing exponentially; worker pods saturated                      |
|                                                                                                   |
| STEP 1: Inspect Quarantine Dead-Letter Metrics                                                    |
|   aws s3 ls s3://enterprise-lake/quarantine/ --summarize                                          |
|                                                                                                   |
| STEP 2: Check Entropy Rejection Distribution                                                      |
|   If rejection reason is "Low-entropy boilerplate":                                               |
|     - Verify whether a batch of blank scanned PDFs was ingested by automated scanner              |
|     - Tune minimum threshold from 2.8 to 2.5 if documents contain large tabular whitespace        |
|                                                                                                   |
| STEP 3: Handle False-Positive Rejections on Source Code                                           |
|   If legitimate JSON/YAML files are rejected (H > 6.0):                                           |
|     - Ensure MIME sniff rules prioritize file extension over raw byte entropy for code types      |
|     - Verify OPA rule `text/code` bypass is active                                                |
|                                                                                                   |
| STEP 4: Review CISO Restricted Classification Alerts                                              |
|   If sensitive docs are detected:                                                                 |
|     - Trigger automated security audit log to HashiCorp Vault / SIEM                              |
+---------------------------------------------------------------------------------------------------+
```
