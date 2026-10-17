# Track 03: Modern Data Layers & Vector Stores

## Overview

Welcome to **Track 03: Modern Data Layers & Vector Stores**. This track equips engineers with the deep distributed systems and storage foundations required to power modern real-time streaming, lakehouse architectures, and ultra-high-dimensional semantic retrieval systems.

Modern applications demand high-throughput event logs, sub-millisecond approximate nearest neighbor (ANN) vector indexing, and ACID-compliant lakehouse storage tables that scale to petabytes without locking bottlenecks.

---

## Pedagogical Philosophy

1. **Storage Engine Mechanics:** How storage layouts (LSM trees, B-trees, columnar Parquet, inverted indices, graph vector graphs) govern I/O performance and cache locality.
2. **Data Plane vs. Storage Topologies:** Detailed Mermaid and ASCII architectures showing streaming ingestion pipelines, vector index partitioning, and compaction engines.
3. **Real-World Manifests & Data Scripts:** Production Helm charts, vector index creation pipelines (Milvus, Qdrant, pgvector), and streaming pipeline jobs (Kafka/Flink).
4. **Consistency & Retrieval Trade-offs:** Comparative decision matrices analyzing latency, recall accuracy, memory footprint, and write amplification.

---

## Curriculum Roadmap

```
+--------------------------------------------------------------------------+
|                       DATA LAYERS CURRICULUM ROADMAP                     |
+--------------------------------------------------------------------------+
|  01. Approximate Nearest Neighbor Vector Indexing: HNSW vs. IVF-PQ       |
|      (Graph Traversal, Quantization, Recall@K, Cache Locality)           |
|                                                                          |
|  02. Real-Time Streaming Systems & Watermark Semantics                   |
|      (Kafka Partitioning, Flink Event-Time Windows, Exactly-Once State)  |
|                                                                          |
|  03. Modern Lakehouse Architecture: Apache Iceberg & Delta Lake          |
|      (Metadata Snapshots, Hidden Partitioning, Parquet Columnar Layout)  |
|                                                                          |
|  04. Distributed Caching & Invalidation Patterns                         |
|      (Redis Cluster, Cache-Aside, Write-Through, Thundering Herd Defense) |
|                                                                          |
|  05. Vector Database Clustering & Sharding at Scale                      |
|      (Milvus Distributed Architecture, Qdrant Collection Segments)       |
+--------------------------------------------------------------------------+
```

---

## Active & Upcoming Modules

| Module Slug | Status | Focus Areas | Key Artifacts |
| :--- | :--- | :--- | :--- |
| `01-vector-indexing-hnsw-ivf` | *Planned* | ANN algorithms, vector recall vs latency trade-offs | Python benchmarking script, index configs |
| `02-stream-processing-watermarks` | *Planned* | Out-of-order event streams, Flink state checkpoints | Kafka manifest, Flink processing job |
| `03-lakehouse-iceberg-metadata` | *Planned* | ACID transactions, table evolution, snapshot expiry | Iceberg Spark catalog config, schema DDL |
| `04-distributed-caching-redis` | *Planned* | Consistent hashing, probabilistic cache invalidation | Redis Cluster manifest, Python client |
| `05-vector-clustering-milvus` | *Planned* | Coordinator vs DataNode vs QueryNode split | Milvus Helm values, collection schema |

---

## Prerequisites & Tooling

- Knowledge of database indexing fundamentals (B-Trees, inverted indexes, hash tables).
- Understanding of distributed systems concepts (CAP theorem, replication, consensus, partitioning).
- Python 3.10+ and SQL proficiency.
- Local tools: Docker Compose, `psql`, `kcat` (Kafka Cat), Python data client libraries (`pymilvus`, `qdrant-client`, `psycopg2`).
