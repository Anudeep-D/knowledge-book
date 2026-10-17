# Spec Delta: ai-models-curriculum

## Purpose

Defines curriculum requirements, pedagogical contracts, companion artifacts, and learning benchmarks for Track 02 (AI Models & Embeddings Layer).

## ADDED Requirements

### Requirement: Model Taxonomy and Selection Module
The curriculum SHALL provide a dedicated module `01-model-taxonomy-selection` evaluating trade-offs between fast inference (3B-8B), reasoning (test-time search), vision-language (VLM), and domain-specialized models.

#### Scenario: Verify Model Taxonomy module structure
- **WHEN** `tracks/02-ai-models-inference/01-model-taxonomy-selection/index.md` is inspected
- **THEN** it contains a production crucible on routing costs, mathematical model of inference compute FLOPs, plain ASCII control-vs-data plane diagrams, and a Pydantic dynamic model router.

### Requirement: Embedding Models and Vector Geometry Module
The curriculum SHALL provide a dedicated module `02-embeddings-vector-space` analyzing metric vector space mechanics, dimensionality trade-offs, Matryoshka Representation Learning (MRL), and scalar quantization (SQ8).

#### Scenario: Verify Vector Space module artifacts
- **WHEN** `tracks/02-ai-models-inference/02-embeddings-vector-space/` is inspected
- **THEN** it contains runnable Python implementations of Matryoshka prefix truncation with L2 re-normalization, 8-bit scalar quantization, and vector index JSON configuration.

### Requirement: Context Windows and Chunking Strategies Module
The curriculum SHALL provide a dedicated module `03-context-windows-chunking` exploring token boundaries, semantic boundary rupture, recursive AST chunking, and hierarchical Parent-Child context retention.

#### Scenario: Verify Context Window and Chunking module
- **WHEN** `tracks/02-ai-models-inference/03-context-windows-chunking/` is inspected
- **THEN** it contains an insurance indemnity boundary failure case study, hierarchical parent-child chunking implementation with metadata breadcrumb headers, and chunking strategy decision tables.

### Requirement: Multimodal Data Ingestion Module
The curriculum SHALL provide a dedicated module `04-multimodal-data-pipelines` covering mixed-input ingestion pipelines, table/chart preservation, Text-First VLM extraction, and ColPali visual late-interaction.

#### Scenario: Verify Multimodal Ingestion pipeline module
- **WHEN** `tracks/02-ai-models-inference/04-multimodal-data-pipelines/` is inspected
- **THEN** it details financial table flattening failures, provides a runnable multimodal document packager preserving table headers, and compares ColPali against text-first decomposition.
