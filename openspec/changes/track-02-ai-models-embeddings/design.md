# Design: Track 02 AI Models & Embeddings Layer

## Context

See `proposal.md` for background and motivation. Track 02 currently has a top-level placeholder `README.md` focusing strictly on GPU serving engines (PagedAttention, Speculative Decoding, Continuous Batching). This design defines the architecture for the prerequisite **Representation & Ingestion Layer** covering Model Taxonomy, High-Dimensional Vector Spaces, Chunking Mechanics, and Multimodal Pipelines.

## Goals / Non-Goals

**Goals:**
- Establish four foundational curriculum modules in `tracks/02-ai-models-inference/` satisfying the strict 4-section Educative.io pedagogical contract.
- Provide production-grade, executable Python 3.12+ reference code and declarative JSON configurations for each module in dedicated `artifacts/` subdirectories.
- Include terminal-safe plain ASCII architecture diagrams (Control Plane vs. Data Plane) in `diagrams/` subdirectories.
- Provide comprehensive comparative decision matrices, failure blast radius post-mortems, and SRE triage runbooks for all four modules.

**Non-Goals:**
- Implementing low-level CUDA kernels or C++ inference engine runtimes (deferred to Module 05 / serving modules).
- Training custom foundational models from scratch (focus is on enterprise evaluation, representation, and systems integration).
- Modifying Track 01, Track 03, or Track 04 modules.

## Decisions

### 1. Module Sequencing & Roadmap Integration
- **Decision:** Sequence the 4 new modules as `01` through `04`, followed by `05-distributed-inference-serving` as the bridge to GPU hardware acceleration.
- **Rationale:** Systems engineers need to understand model selection economics, embedding dimensions, context window boundaries, and multimodal extraction before managing GPU memory allocations and KV caches.
- **Alternatives Considered:** Creating a separate "Track 05" (rejected to preserve the 4-track core taxonomy defined in `curriculum-taxonomy`).

### 2. Pedagogical Contract Enforcement
- **Decision:** Every module `index.md` must implement the exact 4-part structure validated by `shared/scripts/validate-module.py`:
  1. Interactive Concept Breakdown (Production Crucible, First-Principles Mental Model, Invariants)
  2. Visual Architecture (End-to-End Topology, Control Plane vs. Data Plane Split, Step-by-Step Flow)
  3. Real-World Code & Configuration (Declarative Configs, Idiomatic Python 3.12+, Line-by-Line Annotations)
  4. Edge Cases, Failure Modes & Trade-offs (Decision Matrix, Blast Radius Analysis, Observability Runbook)
- **Rationale:** Ensures parity with Track 01 modules and guarantees automated linter compliance.

### 3. Vector Representation & Quantization Approach
- **Decision:** Standardize on Matryoshka Representation Learning (MRL) prefix slicing (1536d -> 512d) combined with symmetric 8-bit Scalar Quantization (SQ8).
- **Rationale:** Achieves ~78% RAM reduction and 3x faster HNSW search speed with <1% MRR@10 penalty, solving the primary vector memory scaling bottleneck without requiring complex product quantization codebooks.

### 4. Multimodal Strategy: Text-First vs. Visual Late Interaction
- **Decision:** Present both Text-First VLM decomposition (for standard text search stacks) and ColPali visual late-interaction (for complex tables, charts, and scanned forms) in a dual-lane architecture.
- **Rationale:** Modern enterprise architectures are actively transitioning from brittle OCR parsers to vision-transformer late-interaction models; presenting both equips engineers for legacy and modern architectures.

## Risks / Trade-offs

- **[Risk: Fast-moving AI ecosystem and model deprecations]** → Design modules around architectural primitives (MRL vector geometry, AST-aware chunking, late-interaction scoring) rather than ephemeral model weights.
- **[Risk: Linter failures on strict frontmatter or section naming]** → Ensure all `index.md` files strictly mirror the `templates/module-template.md` schema and pass `shared/scripts/validate-module.py`.
- **[Risk: Large token count in module documentation]** → Keep explanations concise, crisp, and high-signal, relying on structured tables and annotated code snippets.

## Migration Plan

1. Create module directories under `tracks/02-ai-models-inference/`:
   - `01-model-taxonomy-selection/`
   - `02-embeddings-vector-space/`
   - `03-context-windows-chunking/`
   - `04-multimodal-data-pipelines/`
2. Update `tracks/02-ai-models-inference/README.md` to reflect the updated 5-module roadmap.
3. Validate all modules using `python3 shared/scripts/validate-module.py --all`.
