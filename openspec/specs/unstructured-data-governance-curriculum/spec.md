# unstructured-data-governance-curriculum Specification

## Purpose

Defines curriculum standards, syllabus structure, pedagogical invariants, and companion code benchmarks for Track 05 (Unstructured Data Governance, Quality, & Compliance).

## Requirements

### Requirement: Track 05 Syllabus and Module Hierarchy
The Track 05 curriculum SHALL organize modules covering unstructured data taxonomy, data quality and deduplication, privacy redaction and adversarial prompt-injection defense, and compliance lineage with GDPR vector unlearning.

#### Scenario: Track syllabus overview validation
- **WHEN** an engineer or automated linter inspects `tracks/05-unstructured-data-governance/README.md`
- **THEN** it indexes the 4 foundational modules with clear prerequisites, pedagogical learning goals, and companion artifact tables.

### Requirement: Shannon Entropy Gate and Ingestion Policy Enforcement
Module 01 SHALL establish ingestion gatekeeper rules evaluating normalized Shannon character entropy ($3.0 \le H(X) \le 5.8$) and MIME sniffing to quarantine dark data and corrupt binaries prior to chunking.

#### Scenario: Dark data entropy gating
- **WHEN** a document with Shannon entropy outside the valid text threshold ($H < 3.0$ or $H > 5.8$) is ingested
- **THEN** the ingestion pipeline rejects the document and logs an OPA gatekeeper rejection.

### Requirement: Two-Tier Syntactic and Semantic Deduplication
Module 02 SHALL provide a hybrid deduplication pipeline implementing MinHash LSH for syntactic duplicate rejection and embedding-based cosine distance clustering for semantic boilerplate pruning.

#### Scenario: Deduplication pipeline execution
- **WHEN** near-duplicate or repeated boilerplate chunks pass through the hygiene pipeline
- **THEN** syntactic duplicates with Jaccard similarity $\ge 0.85$ and semantic duplicates with cosine similarity $\ge 0.92$ are pruned before vector persistence.

### Requirement: Multimodal Layout and OCR Quality Scoring
Module 02 SHALL implement multimodal chunk validation that detects image blurriness via Laplacian variance, enforces minimum OCR confidence scores, and prevents 2D table flattening.

#### Scenario: Degraded scanned document rejection
- **WHEN** a scanned document with Laplacian variance $< 100.0$ or mean OCR confidence $< 0.82$ is processed
- **THEN** the chunk is flagged as low quality and diverted to a high-resolution visual refinement queue.

### Requirement: Privacy Redaction, PII Masking, and Prompt Injection Defense
Module 03 SHALL implement automated PII/PHI detection using Presidio entity-class masking, cryptographic format-preserving tokenization, and indirect prompt injection filtering against zero-width characters and jailbreak directives.

#### Scenario: PII detection and masking
- **WHEN** unstructured text containing social security numbers, emails, or medical data is submitted
- **THEN** raw entities are masked or replaced with typed tokens preserving syntactic structure without leaking raw identifiers.

#### Scenario: Indirect prompt injection quarantine
- **WHEN** an ingested document contains zero-width unicode characters or directive hijacking strings
- **THEN** the document is sanitized or quarantined and prevented from entering the vector database.

### Requirement: Vector Lineage Tracking and GDPR Tombstone Unlearning
Module 04 SHALL track data provenance from raw source files to vector store chunk IDs via OpenLineage and provide a two-tier vector unlearning controller that executes soft tombstone filtering and scheduled graph partition compaction for GDPR Article 17 requests.

#### Scenario: GDPR right to be forgotten execution
- **WHEN** a data subject erasure request is received for a specified user identifier
- **THEN** the controller resolves all associated chunk IDs via the lineage catalog, scrubs text payloads in vector storage, marks tombstone bits to exclude them from query-time search, and logs a cryptographic audit receipt.
