# Spec Delta: curriculum-taxonomy

## Purpose

Defines the hierarchical track structure, directory layout, naming conventions, and co-located artifact organization across the engineering knowledge book.

## ADDED Requirements

### Requirement: Four Core Technical Tracks
The repository SHALL organize all engineering modules under four distinct top-level track directories: `tracks/01-cloud-native-infra`, `tracks/02-ai-models-inference`, `tracks/03-modern-data-layers`, and `tracks/04-agentic-workflows`.

#### Scenario: Valid track directory access
- **WHEN** an author or consumer inspects the `tracks/` directory
- **THEN** the four designated track directories exist with track-level `README.md` syllabus overviews.

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
The curriculum SHALL provide dedicated design pattern modules in Track 4 (`tracks/04-agentic-workflows/01-design-patterns-ai-cloud-native`) containing both classic microservices patterns and AI agentic architectures implemented in modern Python.

#### Scenario: Design patterns module structure validation
- **WHEN** `tracks/04-agentic-workflows/01-design-patterns-ai-cloud-native` is inspected
- **THEN** it contains runnable Python implementations of classic resilience patterns and agentic coordination loops alongside comparative trade-off tables.

