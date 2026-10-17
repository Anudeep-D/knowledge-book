# Track 05: Unstructured Data Governance, Quality, & Compliance

## Overview

Welcome to **Track 05: Unstructured Data Governance, Quality, & Compliance**. This track establishes the core data governance and platform engineering discipline required to discover dark data across enterprise object storage, prune duplicate and low-signal noise, sanitize PII/PHI and adversarial prompt-injection payloads, and enforce regulatory compliance (GDPR/CCPA "Right to be Forgotten") across high-dimensional vector spaces.

As generative AI and retrieval-augmented generation (RAG) scale from prototype to enterprise production, unstructured data pipelines are the primary source of operational failure, cost overruns, context window contamination, and regulatory exposure.

---

## Pedagogical Philosophy

1. **Information Entropy & Discovery Mechanics:** Measuring character-level Shannon entropy ($H(X)$) and MIME profiles to filter unclassified dark data, corrupt scans, and binary debris before compute-heavy chunking.
2. **Two-Tier Hygiene & Multimodal Layout Preservation:** Combining syntactic MinHash LSH with dense embedding SemDeDup to eliminate Top-$K$ retrieval redundancy while preserving 2D table layout topologies.
3. **Defense-in-Depth Privacy & Prompt Sanitization:** Applying contextual entity-class masking (`<PERSON_N>`), format-preserving encryption (FPE) vaults, and adversarial injection filtering against zero-width character attacks.
4. **Vector Lineage & Deterministic Unlearning:** Maintaining OpenLineage provenance graphs from source lakes to vector indices, coupled with query-time soft tombstoning and maintenance compaction for compliant GDPR erasure.

---

## Curriculum Roadmap

```
+---------------------------------------------------------------------------------------------------+
|               TRACK 05: UNSTRUCTURED DATA GOVERNANCE, QUALITY, & COMPLIANCE                       |
+---------------------------------------------------------------------------------------------------+
|  TIER A: INGESTION DISCOVERY & DATA HYGIENE                                                        |
|                                                                                                   |
|  01. Unstructured Data Taxonomy & Dark Data Discovery                                            |
|      (MIME Sniffing, Normalized Shannon Entropy H(X), Gatekeeper Policy-as-Code)                  |
|                                                                                                   |
|  02. Data Quality & Hygiene: Deduplication, Chunk Quality, & Semantic Drift                      |
|      (MinHash LSH Jaccard, SemDeDup Cosine Centroids, Table Flattening Defense, OCR Blur)         |
|                                                                                                   |
|  TIER B: PRIVACY, AUDITING, & REGULATORY COMPLIANCE                                               |
|                                                                                                   |
|  03. Privacy, Redaction, & Adversarial Ingestion Defense                                         |
|      (Presidio NER Masking, Format-Preserving Encryption Vault, Prompt Injection Sanitizer)       |
|                                                                                                   |
|  04. Compliance, Lineage, & Vector Unlearning (GDPR Right to Be Forgotten)                        |
|      (OpenLineage Source-to-Vector DAGs, HNSW Graph Edge Rewiring vs Soft Tombstone Compaction)   |
+---------------------------------------------------------------------------------------------------+
```

---

## Module Registry

| Module Slug | Status | Focus Areas | Key Artifacts |
| :--- | :--- | :--- | :--- |
| **[`01-unstructured-taxonomy-dark-data-discovery`](./01-unstructured-taxonomy-dark-data-discovery/)** | **Planned** | MIME sniffing, Shannon entropy gates, OPA gatekeeper | `taxonomy_router.py`, `gatekeeper.rego` |
| **[`02-data-quality-hygiene-curation-pipelines`](./02-data-quality-hygiene-curation-pipelines/)** | **Planned** | MinHash LSH, SemDeDup vector pruning, table layout preservation | `deduplication_engine.py`, `multimodal_quality_gate.py`, `chunk-hygiene-rules.json` |
| **[`03-privacy-redaction-pii-phi-masking`](./03-privacy-redaction-pii-phi-masking/)** | **Planned** | Presidio PII/PHI masking, FPE vaults, indirect prompt injection defense | `pii_sanitizer.py`, `prompt_injection_guard.py`, `pii_policy.rego` |
| **[`04-compliance-lineage-gdpr-vector-unlearning`](./04-compliance-lineage-gdpr-vector-unlearning/)** | **Planned** | OpenLineage tracking, HNSW graph deletion, soft tombstoning | `lineage_gdpr_manager.py`, `query_enforcement.py` |

---

## Prerequisites & Tooling

- Understanding of tokenization, chunking, and embedding geometry (Track 02).
- Familiarity with vector database indexing (HNSW, IVF-PQ) and lakehouse table layouts (Track 03).
- Tooling: Python 3.12+, Pydantic v2, Microsoft Presidio, Open Policy Agent (OPA/Rego), OpenLineage.
