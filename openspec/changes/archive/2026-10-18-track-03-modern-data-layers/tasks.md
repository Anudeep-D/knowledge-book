# Tasks

## 1. Track Syllabus & Taxonomy Configuration

- [x] 1.1 Update `tracks/03-modern-data-layers/README.md` to reflect the 3-module curriculum, technical prerequisites, and learning roadmap.

## 2. Module 01: Vector Databases & High-Dimensional ANN Search

- [x] 2.1 Scaffold `tracks/03-modern-data-layers/01-vector-databases-ann-search/` with `diagrams/` and `artifacts/` subdirectories.
- [x] 2.2 Implement companion artifacts `artifacts/vector_quantizer.py` (symmetric 8-bit scalar quantizer, L2 normalizer, SIMD asymmetric dot product) and `artifacts/hnsw_pgvector.sql` (pgvector DDL and HNSW index configuration).
- [x] 2.3 Author `tracks/03-modern-data-layers/01-vector-databases-ann-search/index.md` adhering strictly to the four-part pedagogical contract (Production Crucible, first-principles Voronoi/HNSW mental models, ASCII control/data plane diagrams, and trade-off matrices).
- [x] 2.4 Validate Module 01 against the contract via `python3 shared/scripts/validate-module.py --path tracks/03-modern-data-layers/01-vector-databases-ann-search` and verify exit code 0.

## 3. Module 02: Modern Lakehouse Architectures (Delta Lake & Apache Iceberg)

- [x] 3.1 Scaffold `tracks/03-modern-data-layers/02-lakehouse-iceberg-delta-lake/` with `diagrams/` and `artifacts/` subdirectories.
- [x] 3.2 Implement companion artifacts `artifacts/iceberg_schema.sql` (Merge-on-Read, hidden daily partitioning, Parquet zstd compression) and `artifacts/iceberg_ops.py` (PySpark time-travel reader by snapshot ID and binpack compaction rewrite).
- [x] 3.3 Author `tracks/03-modern-data-layers/02-lakehouse-iceberg-delta-lake/index.md` adhering strictly to the four-part pedagogical contract (S3 concurrent write collision crucible, metadata tree diagrams, OCC sequence flow, and Iceberg vs Delta Lake matrices).
- [x] 3.4 Validate Module 02 against the contract via `python3 shared/scripts/validate-module.py --path tracks/03-modern-data-layers/02-lakehouse-iceberg-delta-lake` and verify exit code 0.

## 4. Module 03: State Persistence & Memory Hierarchies for AI Agents

- [x] 4.1 Scaffold `tracks/03-modern-data-layers/03-agent-state-persistence-memory/` with `diagrams/` and `artifacts/` subdirectories.
- [x] 4.2 Implement companion artifacts `artifacts/episodic_memory.sql` (PostgreSQL + pgvector schema with temporal decay retrieval stored procedure) and `artifacts/agent_memory_manager.py` (async Python 3.11 tiered memory manager with Redis distributed mutex locks).
- [x] 4.3 Author `tracks/03-modern-data-layers/03-agent-state-persistence-memory/index.md` adhering strictly to the four-part pedagogical contract (context window amnesia crucible, 4-tier memory pyramid, ASCII state diagrams, and storage tier trade-off matrices).
- [x] 4.4 Validate Module 03 against the contract via `python3 shared/scripts/validate-module.py --path tracks/03-modern-data-layers/03-agent-state-persistence-memory` and verify exit code 0.

## 5. Track-Level Verification

- [x] 5.1 Run full track validation script across all Track 03 modules and verify zero lint errors.

## Workflow follow-up

- Archive the change via `/opsx-archive` after implementation and verification are complete.
- Sync delta specs to main specs.
