# Track 03: Modern Data Layers & Storage Systems

## Overview

Welcome to **Track 03: Modern Data Layers & Storage Systems**. This track equips engineers with the deep distributed systems, storage engine mechanics, and persistent state primitives required to power modern real-time streaming, lakehouse architectures, and ultra-high-dimensional semantic retrieval systems for autonomous AI workflows.

Modern data-intensive applications demand high-throughput event ingestion, sub-millisecond approximate nearest neighbor (ANN) vector indexing, ACID-compliant lakehouse storage tables that scale to petabytes on raw object storage, and multi-tier memory hierarchies for autonomous agents.

---

## Pedagogical Philosophy

1. **Storage Engine Mechanics:** How storage layouts (Voronoi partitions, HNSW skip graphs, columnar Parquet, hierarchical Avro metadata trees, Redis memory buffers) govern I/O performance, SIMD vectorization, and cache locality.
2. **Control Plane vs. Data Plane Topologies:** Detailed Mermaid and ASCII architectures delineating metadata coordination, consensus arbiters, and high-throughput payload execution tiers.
3. **Real-World Schemas & Production Manifests:** Production SQL DDL, HNSW index configurations, Apache Iceberg table properties, and async Python multi-tier memory managers.
4. **Consistency & Retrieval Trade-offs:** Rigorous comparative decision matrices analyzing latency, recall accuracy, write amplification, and failure containment runbooks.

---

## Curriculum Roadmap

```
+--------------------------------------------------------------------------------------------------+
|                               DATA LAYERS CURRICULUM ROADMAP                                     |
+--------------------------------------------------------------------------------------------------+
|  01. Vector Databases & High-Dimensional ANN Search                                              |
|      (Metric Geometry, HNSW vs. IVF-PQ, Symmetric Scalar Quantization, Distributed Sharding)     |
|                                                                                                  |
|  02. Modern Lakehouse Architectures: Apache Iceberg & Delta Lake                                 |
|      (ACID on S3/GCS, Hierarchical Metadata Trees, Optimistic Concurrency, Merge-on-Read, Time Travel)|
|                                                                                                  |
|  03. State Persistence & Memory Hierarchies for AI Agents                                        |
|      (4-Tier Memory Pyramid, Redis Mutex Locks, PGVector Episodic Decay, Semantic Prompt Caching) |
+--------------------------------------------------------------------------------------------------+
```

---

## Active Curriculum Modules

| Module Slug | Status | Focus Areas | Key Artifacts |
| :--- | :--- | :--- | :--- |
| `01-vector-databases-ann-search` | **Active** | ANN indexing algorithms (HNSW, IVF-Flat, IVF-PQ), metric geometry (L2/Cosine/MIPS), scalar quantization (SQ8), distributed vector clustering | `artifacts/vector_quantizer.py`, `artifacts/hnsw_pgvector.sql` |
| `02-lakehouse-iceberg-delta-lake` | **Active** | ACID transactions on object storage, Iceberg metadata trees vs Delta logs, OCC conflict resolution, Merge-on-Read, time travel | `artifacts/iceberg_schema.sql`, `artifacts/iceberg_ops.py` |
| `03-agent-state-persistence-memory` | **Active** | 4-tier agent memory pyramid, Redis distributed mutex leases, PostgreSQL pgvector episodic decay scoring, semantic caching | `artifacts/episodic_memory.sql`, `artifacts/agent_memory_manager.py` |

---

## Technical Prerequisites & Tooling

- Knowledge of database indexing fundamentals (B-Trees, inverted indexes, hash tables, graph traversals).
- Understanding of distributed systems concepts (CAP theorem, consensus, optimistic concurrency control, write-ahead logging).
- Python 3.10+ proficiency with type hints and async/await syntax.
- SQL DDL knowledge (PostgreSQL, `pgvector`, Apache Iceberg Spark SQL extensions).
- Local tooling: Docker Compose, `psql`, Python data client libraries (`numpy`, `pydantic`, `psycopg2`, `redis`).
