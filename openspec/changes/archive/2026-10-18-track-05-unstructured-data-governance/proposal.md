# Proposal: Track 05 Unstructured Data Governance, Quality, & Compliance Curriculum

## Why

As enterprise organizations scale generative AI, RAG pipelines, and high-dimensional semantic search, unstructured data ingestion is where production systems most critically fail. Ingesting unclassified "dark data" leads to catastrophic storage cost spikes, near-duplicate and low-density boilerplate chunks hijack Top-$K$ retrieval context windows, and unsanitized PII/PHI or indirect prompt-injection payloads expose organizations to severe regulatory liability and security exploits. Furthermore, standard vector indices (such as HNSW graphs) lack native support for GDPR/CCPA "Right to be Forgotten" deletion requests, risking regulatory non-compliance through persistent "zombie" embeddings.

This change introduces Track 05's comprehensive curriculum structure across four foundational pillars:
1. **Unstructured Data Taxonomy & Dark Data Discovery:** MIME sniffing, Shannon entropy gates, media classification, and automated gatekeeper policy-as-code enforcement.
2. **Data Quality & Hygiene for AI Pipelines:** Syntactic deduplication (MinHash LSH), semantic deduplication (SemDeDup), multimodal OCR quality scoring, and drift monitoring.
3. **Privacy, Redaction, & Adversarial Ingestion Defense:** Presidio NER masking, cryptographic format-preserving encryption (FPE) vaults, and indirect prompt injection sanitization.
4. **Compliance, Lineage, & Vector Unlearning:** OpenLineage provenance tracking, tamper-evident audit ledgers, and two-tier HNSW tombstoning for GDPR/CCPA Article 17 erasure.

## What Changes

- **Update Curriculum Taxonomy**: Expand the repository's recognized curriculum tracks to include `tracks/05-unstructured-data-governance` across taxonomy specifications and validation scripts (`shared/scripts/validate-module.py`).
- **Establish Track Syllabus**: Create `tracks/05-unstructured-data-governance/README.md` establishing the 4-module pedagogical roadmap, prerequisites, and artifact registries.
- **Module 01 (`01-unstructured-taxonomy-dark-data-discovery`)**: Establish an Educative.io module covering Shannon entropy filtering, MIME classification, and OPA/Rego ingestion policies.
- **Module 02 (`02-data-quality-hygiene-curation-pipelines`)**: Establish an Educative.io module covering MinHash LSH, SemDeDup vector pruning, table layout preservation, and OCR quality gates.
- **Module 03 (`03-privacy-redaction-pii-phi-masking`)**: Establish an Educative.io module covering Presidio PII/PHI masking, cryptographic vault pseudonymization, and indirect prompt-injection sanitization.
- **Module 04 (`04-compliance-lineage-gdpr-vector-unlearning`)**: Establish an Educative.io module covering OpenLineage DAGs, HNSW graph deletion mechanics, soft tombstoning, and partition compaction.
- **Companion Artifacts & Schemas**: Provide production-grade, typed Python implementations, JSON schemas, and OPA policies for each module.

## Capabilities

### New Capabilities
- `unstructured-data-governance-curriculum`: Defines curriculum standards, syllabus structure, pedagogical invariants, and companion code benchmarks for Track 05 (Unstructured Data Governance, Quality, & Compliance).

### Modified Capabilities
- `curriculum-taxonomy`: Updates the repository taxonomy and module directory layout requirements to include Track 05 (`tracks/05-unstructured-data-governance`) and updates the automated module contract linter (`shared/scripts/validate-module.py`) to recognize Track 05 in `VALID_TRACKS`.

## Impact

- **Curriculum Architecture**: Adds `tracks/05-unstructured-data-governance` with modules 01, 02, 03, and 04.
- **Tooling & Dependencies**: Python 3.12+, `pydantic>=2.7.0`, `presidio-analyzer>=2.2.0`, `presidio-anonymizer>=2.2.0`, `numpy>=1.26.0`, `openlineage-python>=1.0.0`.
- **Validation**: Updates `shared/scripts/validate-module.py` `VALID_TRACKS` to allow `05-unstructured-data-governance` and ensures all modules pass the automated module contract linter.
