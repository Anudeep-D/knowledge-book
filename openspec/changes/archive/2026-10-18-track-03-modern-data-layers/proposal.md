# Proposal

## Why

Modern enterprise AI platforms and distributed systems are crashing against state bottlenecks: in-memory vector indexes breach the physical RAM cliff at tens of millions of embeddings, raw object store data lakes suffer from concurrency races and corrupted training sets, and autonomous multi-agent systems suffer from context amnesia and token bankruptcy without tiered memory persistence.

To equip engineers with the distributed systems and storage architectures required to build reliable data-intensive applications, Track 03: Modern Data Layers & Storage Systems must provide mathematically grounded, production-tested modules covering Vector Databases & Approximate Nearest Neighbor (ANN) search, Modern Lakehouse architectures (Apache Iceberg & Delta Lake), and Multi-Tier Agent State Persistence.

## What Changes

- Create curriculum specification `data-storage-curriculum` detailing requirements for three core modules in `tracks/03-modern-data-layers`:
  - `01-vector-databases-ann-search`: Deep-dive into high-dimensional ANN algorithms (HNSW, IVF-Flat, IVF-PQ, DiskANN), metric geometry (L2, Cosine, MIPS), scalar quantization, and distributed vector database clustering (coordinator, query node, data node separation).
  - `02-lakehouse-iceberg-delta-lake`: Unified storage layer mechanics for structured tables and multimodal AI training artifacts, ACID transactions on object storage via Optimistic Concurrency Control (OCC), snapshot metadata trees vs commit chains, Merge-on-Read (MoR) vs Copy-on-Write (CoW), and deterministic ML dataset time-travel.
  - `03-agent-state-persistence-memory`: Four-tier memory hierarchy (in-memory scratchpad, Redis session buffer, PostgreSQL + pgvector episodic store with temporal decay scoring, and knowledge graph memory), sub-agent concurrency locks, and semantic prompt/tool caching.
- Update `curriculum-taxonomy` specification to formalize Track 03 module composition requirements.
- Update `tracks/03-modern-data-layers/README.md` to reflect the updated syllabus, prerequisite matrix, and learning roadmap.

## Capabilities

### New Capabilities
- `data-storage-curriculum`: Requirements, pedagogical contracts, companion artifacts, and technical benchmarks for Track 03 (Modern Data Layers & Storage Systems).

### Modified Capabilities
- `curriculum-taxonomy`: Add requirement defining Track 03 Modern Data Layers curriculum composition and module sequence.

## Impact

- Tracks directory: `tracks/03-modern-data-layers/` will receive the 3 comprehensive module packages with runnable Python, SQL DDL, and PySpark scripts alongside architecture diagrams.
- Tooling/Dependencies: Exercises require Python 3.10+, `numpy`, `pydantic`, `pgvector` / `psycopg2`, and Apache Iceberg PySpark configs.
