# Tasks

## 1. Taxonomy & Linter Setup

- [x] 1.1 Update `shared/scripts/validate-module.py` to register `05-unstructured-data-governance` in `VALID_TRACKS` and verify script execution succeeds.
- [x] 1.2 Create `tracks/05-unstructured-data-governance/README.md` syllabus overview and verify all 4 foundational modules and prerequisites are indexed.

## 2. Module 01: Unstructured Data Taxonomy & Dark Data Discovery

- [x] 2.1 Scaffold `tracks/05-unstructured-data-governance/01-unstructured-taxonomy-dark-data-discovery/` and author `index.md` following the strict 4-part module contract.
- [x] 2.2 Author companion artifacts `artifacts/taxonomy_router.py` (Pydantic Shannon entropy model) and `artifacts/gatekeeper.rego` (OPA ingestion policy) and verify runnable execution.
- [x] 2.3 Run `python3 shared/scripts/validate-module.py --path tracks/05-unstructured-data-governance/01-unstructured-taxonomy-dark-data-discovery` and verify exit code 0.

## 3. Module 02: Data Quality & Hygiene for AI

- [x] 3.1 Scaffold `tracks/05-unstructured-data-governance/02-data-quality-hygiene-curation-pipelines/` and author `index.md` following the strict 4-part module contract.
- [x] 3.2 Author companion artifacts `artifacts/deduplication_engine.py` (MinHash LSH + SemDeDup), `artifacts/multimodal_quality_gate.py` (Laplacian variance and table preservation), and `artifacts/chunk-hygiene-rules.json`.
- [x] 3.3 Run `python3 shared/scripts/validate-module.py --path tracks/05-unstructured-data-governance/02-data-quality-hygiene-curation-pipelines` and verify exit code 0.

## 4. Module 03: Privacy, Redaction, & Adversarial Ingestion Defense

- [x] 4.1 Scaffold `tracks/05-unstructured-data-governance/03-privacy-redaction-pii-phi-masking/` and author `index.md` following the strict 4-part module contract.
- [x] 4.2 Author companion artifacts `artifacts/pii_sanitizer.py` (Presidio analyzer/anonymizer), `artifacts/prompt_injection_guard.py` (adversarial injection & zero-width stripper), and `artifacts/pii_policy.rego`.
- [x] 4.3 Run `python3 shared/scripts/validate-module.py --path tracks/05-unstructured-data-governance/03-privacy-redaction-pii-phi-masking` and verify exit code 0.

## 5. Module 04: Compliance, Lineage, & Vector Unlearning (GDPR/CCPA)

- [x] 5.1 Scaffold `tracks/05-unstructured-data-governance/04-compliance-lineage-gdpr-vector-unlearning/` and author `index.md` following the strict 4-part module contract.
- [x] 5.2 Author companion artifacts `artifacts/lineage_gdpr_manager.py` (OpenLineage provenance tracking and two-tier soft tombstoning) and `artifacts/query_enforcement.py` (query-time exclusion filter).
- [x] 5.3 Run `python3 shared/scripts/validate-module.py --path tracks/05-unstructured-data-governance/04-compliance-lineage-gdpr-vector-unlearning` and verify exit code 0.

## 6. Track 05 Verification & Linter Audit

- [x] 6.1 Execute `python3 shared/scripts/validate-module.py` across all four modules in `tracks/05-unstructured-data-governance/` and verify 100% compliance with zero errors.
