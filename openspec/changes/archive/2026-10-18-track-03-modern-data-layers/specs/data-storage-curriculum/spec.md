# Spec Delta: data-storage-curriculum

## Purpose

Defines curriculum requirements, pedagogical contracts, companion artifacts, and technical benchmarks for Track 03 (Modern Data Layers & Storage Systems).

## ADDED Requirements

### Requirement: Vector Databases and ANN Search Module
The curriculum SHALL provide a dedicated module `01-vector-databases-ann-search` evaluating metric geometry, approximate nearest neighbor search algorithms, vector quantization, and distributed cluster partitioning.

#### Scenario: Verify Vector Databases module artifacts
- **WHEN** `tracks/03-modern-data-layers/01-vector-databases-ann-search/` is inspected
- **THEN** it contains a production crucible on vector memory cliffs, plain ASCII control-vs-data plane diagrams, runnable Python implementations of symmetric scalar quantization, and production pgvector HNSW DDL configuration.

### Requirement: Modern Lakehouse Architectures Module
The curriculum SHALL provide a dedicated module `02-lakehouse-iceberg-delta-lake` analyzing unified storage layer mechanics for structured tables and multimodal AI training artifacts, ACID transactions on object storage, metadata trees, and deterministic time travel.

#### Scenario: Verify Lakehouse Architecture module artifacts
- **WHEN** `tracks/03-modern-data-layers/02-lakehouse-iceberg-delta-lake/` is inspected
- **THEN** it contains an S3 write concurrency incident case study, Delta log vs Iceberg metadata tree diagrams, production Apache Iceberg table DDL with Merge-on-Read (MoR), and PySpark deterministic time-travel scripts.

### Requirement: Agent State Persistence and Memory Hierarchies Module
The curriculum SHALL provide a dedicated module `03-agent-state-persistence-memory` exploring four-tier memory architectures, temporal decay scoring, distributed session synchronization, and semantic caching for autonomous AI agents.

#### Scenario: Verify Agent State Persistence module artifacts
- **WHEN** `tracks/03-modern-data-layers/03-agent-state-persistence-memory/` is inspected
- **THEN** it details context window exhaustion and agent amnesia failures, contains a four-tier memory topology diagram, production PostgreSQL pgvector schema with temporal decay stored procedures, and an async Python multi-tier memory manager with Redis session locking.
