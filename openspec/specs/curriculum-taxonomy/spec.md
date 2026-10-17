# curriculum-taxonomy Specification

## Purpose

Defines the hierarchical track structure, directory layout, naming conventions, and co-located artifact organization across the engineering knowledge book.

## Requirements

### Requirement: Four Core Technical Tracks
The repository SHALL organize all engineering modules under five distinct top-level track directories: `tracks/01-cloud-native-infra`, `tracks/02-ai-models-inference`, `tracks/03-modern-data-layers`, `tracks/04-agentic-workflows`, and `tracks/05-unstructured-data-governance`.

#### Scenario: Valid track directory access
- **WHEN** an author or consumer inspects the `tracks/` directory
- **THEN** the five designated track directories exist with track-level `README.md` syllabus overviews.

#### Scenario: Track 05 syllabus and linter recognition
- **WHEN** `shared/scripts/validate-module.py` or a curriculum consumer validates `tracks/05-unstructured-data-governance`
- **THEN** the track is recognized as a valid first-class curriculum domain.

### Requirement: Standardized Module Directory Structure
Every module SHALL be encapsulated in its own directory using a zero-padded sequential index and kebab-case slug (e.g., `01-keda-autoscaling-patterns`) containing an `index.md` and dedicated subdirectories for companion assets.

#### Scenario: Module folder layout verification
- **WHEN** a module is created within a track directory
- **THEN** it contains `index.md`, a `diagrams/` directory for diagram sources, and an `artifacts/` directory for runnable code and manifests.

### Requirement: Module Metadata Declaration
Each module SHALL declare machine-readable metadata containing title, track, difficulty level, prerequisites, estimated duration, and tags in frontmatter format at the top of `index.md`.

#### Scenario: Frontmatter parsing
- **WHEN** an automated parser inspects module `index.md`
- **THEN** valid YAML frontmatter is extracted containing required fields `title`, `track`, `difficulty`, `tags`, and `estimated_minutes`.

### Requirement: Foundational Design Patterns Coverage
The curriculum SHALL provide dedicated design pattern and orchestration modules in Track 4 (`tracks/04-agentic-workflows`) containing classic microservices patterns, distributed Prefect dataflows, LangGraph cyclic state machines, and production guardrail evaluation loops implemented in modern Python.

#### Scenario: Design patterns module structure validation
- **WHEN** `tracks/04-agentic-workflows/01-design-patterns-ai-cloud-native` is inspected
- **THEN** it contains runnable Python implementations of classic resilience patterns and agentic coordination loops alongside comparative trade-off tables.

#### Scenario: Track 04 module suite inspection
- **WHEN** `tracks/04-agentic-workflows` is inspected
- **THEN** modules covering design patterns, Prefect orchestration, LangGraph state topologies, and production guardrails exist with compliant companion artifacts.

### Requirement: Track 02 Models and Embeddings Layer Composition
The Track 02 syllabus SHALL organize foundational modules covering model taxonomy and selection, embedding vector representations, context chunking strategies, multimodal ingestion pipelines, and distributed inference serving.

#### Scenario: Syllabus coverage verification
- **WHEN** `tracks/02-ai-models-inference/README.md` is inspected
- **THEN** it indexes the 4 foundational representation modules followed by distributed inference serving modules with prerequisites and companion artifact references.

### Requirement: Track 03 Modern Data Layers and Storage Systems Composition
The Track 03 syllabus SHALL organize foundational modules covering vector database indexing, modern lakehouse storage engines, and agentic state persistence hierarchies.

#### Scenario: Track 03 syllabus coverage verification
- **WHEN** `tracks/03-modern-data-layers/README.md` is inspected
- **THEN** it indexes modules `01-vector-databases-ann-search`, `02-lakehouse-iceberg-delta-lake`, and `03-agent-state-persistence-memory` with explicit prerequisites and companion artifact references.


