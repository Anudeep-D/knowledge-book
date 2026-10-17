# Track 02: AI Models, Serving & Inference Engineering

## Overview

Welcome to **Track 02: AI Models, Serving & Inference Engineering**. This track establishes the core systems engineering discipline required to select foundation models, project unstructured knowledge into dense metric vector spaces, preserve semantic context across token window boundaries, ingest heterogeneous multimodal data, and deploy high-throughput distributed inference engines at scale.

---

## Pedagogical Philosophy

1. **First-Principles Representation Geometry:** Understanding high-dimensional metric manifolds, cosine proximity, Matryoshka Representation Learning (MRL), and quantization economics.
2. **Control Plane vs. Data Plane Separation:** Clear visual delineation between dynamic model routing / AST parsing and low-latency tensor execution / vector indexing.
3. **Executable Systems Code:** Production-grade Python 3.12+ reference implementations with Pydantic validation, typed async pipelines, and declarative JSON configurations.
4. **Failure Mode Blast Radius Analysis:** Concrete incident post-mortems exploring runaway token spend, vector memory cliffs, context boundary rupture, and table flattening disasters.

---

## Curriculum Roadmap

```
+---------------------------------------------------------------------------------------+
|                 TRACK 02: FOUNDATION MODELS, EMBEDDINGS & INFERENCE                   |
+---------------------------------------------------------------------------------------+
|  TIER A: REPRESENTATION & INGESTION LAYER                                             |
|                                                                                       |
|  01. Model Taxonomy & Selection: Architectural Tiers and Dynamic Routing              |
|      (Fast-Inference 8B vs Reasoning o-Series vs VLM vs LoRA, Entropy Scoring)        |
|                                                                                       |
|  02. Embedding Models & Vector Space: Metric Geometry & Dimensionality Compaction     |
|      (Hypersphere Geometry, Matryoshka Slicing 1536d->512d, L2 Norm, SQ8 int8)        |
|                                                                                       |
|  03. Context Windows & Chunking: Token Dynamics & Semantic Boundary Preservation      |
|      (Small-to-Big Retrieval, Parent-Child Hierarchies, Breadcrumb Metadata Injection)|
|                                                                                       |
|  04. Multimodal Data Pipelines: Mixed-Input Ingestion & Visual Late Interaction       |
|      (2D Financial Tables, Text-First VLM Decomposition vs ColPali Multi-Vectors)    |
|                                                                                       |
|  TIER B: DISTRIBUTED SERVING & GPU ACCELERATION                                       |
|                                                                                       |
|  05. Distributed Inference Serving & GPU Memory Management                            |
|      (PagedAttention, KV Cache Paging, Continuous Batching, Tensor Parallelism)       |
+---------------------------------------------------------------------------------------+
```

---

## Module Registry

| Module Slug | Status | Focus Areas | Key Artifacts |
| :--- | :--- | :--- | :--- |
| **[`01-model-taxonomy-selection`](./01-model-taxonomy-selection/)** | **Complete** | Fast vs reasoning tiers, dynamic routing, fallback SLA | `router.py`, `model-router-policy.json` |
| **[`02-embeddings-vector-space`](./02-embeddings-vector-space/)** | **Complete** | 240GB memory cliff, MRL slicing, SQ8 quantization | `embedding_pipeline.py`, `vector-index-config.json` |
| **[`03-context-windows-chunking`](./03-context-windows-chunking/)** | **Complete** | Boundary rupture, Parent-Child retrieval, breadcrumbs | `contextual_chunker.py`, `chunking-rules.json` |
| **[`04-multimodal-data-pipelines`](./04-multimodal-data-pipelines/)** | **Complete** | Table flattening, ColPali late-interaction, VLM | `multimodal_pipeline.py`, `multimodal-pipeline.json` |
| `05-distributed-inference-serving` | *Planned* | PagedAttention, KV-cache, continuous batching | Triton/vLLM configs, RayCluster manifests |

---

## Prerequisites & Tooling

- Solid foundation in Python 3.10+ and asynchronous programming (`asyncio`).
- Understanding of transformer architectures (self-attention mechanism, query-key-value projections).
- Familiarity with PyTorch tensors, vector databases (HNSW), and tokenizer mechanics.
- Recommended lab setup: Modern Python virtual environment (`.venv`) and access to local or cloud acceleration for vector indexing and serving experiments.
