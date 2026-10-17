# Proposal: Track 02 AI Models & Embeddings Layer

## Why

Enterprise systems require robust guidelines for selecting foundation models, projecting unstructured text and documents into dense vector spaces, and chunking data without context loss. Track 02 currently lacks curriculum definitions for model selection tiers, Matryoshka embeddings, semantic boundary chunking, and multimodal ingestion pipelines. Adding these modules equips engineering teams to design cost-effective, high-precision generative AI platforms before integrating lower-level GPU serving runtimes.

## What Changes

- Define the curriculum roadmap and module structure for Track 02 (`tracks/02-ai-models-inference/`).
- Introduce 4 foundational curriculum modules in Educative.io format:
  1. `01-model-taxonomy-selection`: Fast vs. reasoning vs. VLM vs. specialized models, dynamic latency/cost routing.
  2. `02-embeddings-vector-space`: Mechanics of vector spaces, dimensionality trade-offs (1536d vs 512d vs 384d), Matryoshka Representation Learning (MRL), and Scalar Quantization (SQ8).
  3. `03-context-windows-chunking`: Token constraints, information entropy, recursive hierarchical chunking (Parent-Child small-to-big), and metadata enrichment.
  4. `04-multimodal-data-pipelines`: Processing mixed inputs (PDF tables, charts, scanned forms) using Text-First VLM extraction and ColPali visual late-interaction.
- Position the existing distributed serving topics (`05-distributed-inference-serving`) as the architectural bridge to GPU compute and memory execution.
- Provide production Python reference implementations and declarative JSON configurations for all 4 modules.

## Capabilities

### New Capabilities
- `ai-models-curriculum`: Defines curriculum requirements, pedagogical contracts, companion artifacts, and learning benchmarks for Track 02 (AI Models & Embeddings Layer).

### Modified Capabilities
- `curriculum-taxonomy`: Updates track definitions to codify Track 02's syllabus spanning model taxonomy, vector geometry, chunking architectures, multimodal pipelines, and distributed serving.

## Impact

- Track 02 directory layout (`tracks/02-ai-models-inference/`).
- Track 02 `README.md` syllabus roadmap and module registry.
- Companion artifacts and runnable Python scripts for routing, embedding slicing, chunking, and multimodal packaging.
- Validation suite coverage via `shared/scripts/validate-module.py`.
