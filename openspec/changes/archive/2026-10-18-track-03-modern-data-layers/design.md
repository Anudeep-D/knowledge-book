# Design: Track 03 Modern Data Layers & Storage Systems

## Context

See `proposal.md` for overall motivation. Track 03 builds upon the infrastructure primitives of Track 01 and the vector/embedding representation principles of Track 02. The focus here is the underlying storage mechanics, indexing structures, and distributed transactional durability required for data-intensive AI and analytics systems.

All modules strictly adhere to the four-part pedagogical contract in `openspec/specs/module-contract/spec.md`:
1. Interactive Concept Breakdown (The Production Crucible, First-Principles Mental Models, Architectural Invariants)
2. Visual Architecture (System Topology, ASCII Control vs Data Plane diagrams, State/Packet Flows)
3. Real-World Code & Configuration (Production Manifests, Idiomatic typed Python 3.11+, Line-by-Line Annotations)
4. Edge Cases, Failure Modes & Trade-offs (Comparative Decision Matrix, 3 Failure Scenarios, Observability Runbook)

## Goals / Non-Goals

**Goals:**
- Deliver 3 comprehensive, production-grade curriculum modules in `tracks/03-modern-data-layers/`:
  - `01-vector-databases-ann-search`
  - `02-lakehouse-iceberg-delta-lake`
  - `03-agent-state-persistence-memory`
- Provide runnable, fully typed companion Python 3.11+ scripts, SQL DDL with pgvector, and PySpark Iceberg execution scripts.
- Include plain ASCII and Mermaid diagrams for every module showing control plane vs data plane and storage flow trees.
- Provide comprehensive comparative trade-off tables and Prometheus SLI observability runbooks.

**Non-Goals:**
- Implementing production proprietary database server engines from scratch (we focus on architectural mechanics, indexing algorithms, and storage engine interactions).
- Benchmarking across cloud vendors (we focus on reproducible algorithms and standard containerized/open-source stacks: pgvector, Redis, Apache Iceberg, MinIO/S3).

## Decisions

### Decision 1: Focus Chapter 1 on Algorithmic Foundations (HNSW/IVF) and pgvector/Qdrant Primitives
- **Choice:** Anchor vector indexing mechanics in the metric geometry of high-dimensional spaces, comparing Voronoi cells (IVF) with multi-layer skip graphs (HNSW), backed by a custom Python 8-bit symmetric scalar quantizer (SQ8) and production pgvector HNSW DDL.
- **Alternatives Considered:** 
  - *Black-box vendor comparison (Pinecone vs Weaviate):* Rejected because it obscures algorithmic mechanics (graph hops, quantization codebooks, memory layout).
  - *Flat exact search only:* Rejected because it doesn't teach scaling or memory cliff trade-offs.

### Decision 2: Focus Chapter 2 on Apache Iceberg as Primary Standard with Delta Lake Parity
- **Choice:** Use Apache Iceberg's hierarchical snapshot tree (`metadata.json` -> manifest list -> manifest file -> data files) as the canonical mental model for object store ACID transactions, contrasting it with Delta Lake's linear transaction log (`_delta_log/00000.json`). Provide production SQL DDL for Merge-on-Read (MoR) and PySpark time-travel scripts.
- **Alternatives Considered:**
  - *Delta Lake exclusive:* Rejected because Apache Iceberg has emerged as the multi-engine, multi-catalog enterprise standard (Spark, Trino, Flink, Snowflake).
  - *Raw Parquet without lakehouse layers:* Rejected because it lacks ACID, schema evolution, and atomic snapshot isolation.

### Decision 3: Standardize Chapter 3 on a 4-Tier Agent Memory Pyramid
- **Choice:** Formalize agent state into a 4-tier memory hierarchy:
  1. *Tier 1 (Working Context):* Ephemeral token window scratchpad.
  2. *Tier 2 (Session State):* Redis Cluster with TTL and distributed mutex locks (`SETNX`) for parallel sub-agents.
  3. *Tier 3 (Episodic Store):* PostgreSQL + `pgvector` with temporal decay scoring ($Score = \alpha \cdot \text{Sim} + \beta \cdot e^{-\lambda \Delta t} + \gamma \cdot \text{Imp}$).
  4. *Tier 4 (Ontology):* Entity-relationship graph memory.
- **Alternatives Considered:**
  - *In-memory context stuffing:* Rejected due to token exhaustion, cost, and "Lost in the Middle" attention degradation.
  - *Single database for all tiers:* Rejected because low-latency coordination (<2ms) requires memory stores (Redis), while semantic retrieval requires vector indices (pgvector).

## Risks / Trade-offs

- **[Risk] High computational cost of building dense HNSW graphs in-memory** $\to$ *Mitigation:* Teach asymmetric scalar quantization (SQ8) and MRL prefix slicing to compress in-memory footprint by 75% while preserving >97% recall.
- **[Risk] Concurrency conflicts during high-frequency streaming writes to Iceberg** $\to$ *Mitigation:* Document Optimistic Concurrency Control (OCC) retry loop strategies and Merge-on-Read (MoR) positional delete buffering.
- **[Risk] Race conditions and state corruption during parallel sub-agent execution** $\to$ *Mitigation:* Provide distributed locking mechanics via Redis and atomic session leases.

## Migration Plan

1. Update `tracks/03-modern-data-layers/README.md` syllabus roadmap.
2. Author Module 01 (`01-vector-databases-ann-search`) with companion code in `artifacts/`.
3. Author Module 02 (`02-lakehouse-iceberg-delta-lake`) with companion code in `artifacts/`.
4. Author Module 03 (`03-agent-state-persistence-memory`) with companion code in `artifacts/`.
5. Run module contract linter (`python3 shared/scripts/validate-module.py`) to guarantee 100% compliance.
