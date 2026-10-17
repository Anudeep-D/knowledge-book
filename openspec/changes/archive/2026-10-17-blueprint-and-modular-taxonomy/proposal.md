# Proposal

## Why

To establish an enterprise-grade, extensible engineering knowledge book modeled after interactive platforms like Educative.io, we need a rigorous architectural blueprint and modular taxonomy. As the knowledge base expands across Cloud-Native Infrastructure, AI Models & Serving, Modern Data Layers, and Agentic Workflows, an ad-hoc or purely narrative format leads to fragmented quality, broken references, and inconsistent depth. Introducing a standardized track-and-module structure with a strictly enforced 4-part pedagogical contract guarantees that every current and future module delivers production-grade mental models, architectural visuals, battle-tested code/manifests, and failure-mode analysis.

## What Changes

- Establish the **Curriculum Taxonomy & Directory Structure** organizing content into four foundational engineering tracks:
  - `01-cloud-native-infra`
  - `02-ai-models-inference`
  - `03-modern-data-layers`
  - `04-agentic-workflows`
- Define the **Standard Module Contract & Schema**, requiring all future modules to implement:
  1. **Interactive Concept Breakdown** ("The Why Before The How")
  2. **Visual Architecture** (ASCII & Mermaid diagrams with control/data plane splits)
  3. **Production Code & Configuration** (Kubernetes manifests, KEDA ScaledObjects, OpenShift templates, Python/TypeScript)
  4. **Edge Cases, Failure Modes & Trade-offs** (Blast radius matrices, observability triage runbooks, comparative tables)
- Introduce a reusable **Canonical Module Template** (`templates/module-template.md`) and frontmatter specification.
- Establish an automated **Module Validation & Linting Tooling** (`shared/scripts/validate-module.py`) to enforce module structure and ensure zero regressions.
- Create an initial **Cloud-Native Pilot Module** (`tracks/01-cloud-native-infra/01-keda-autoscaling-patterns/`) demonstrating event-driven autoscaling and manifest co-location.
- Create a dedicated **Design Patterns Module** (`tracks/04-agentic-workflows/01-design-patterns-ai-cloud-native/`) implementing:
  1. *Classic Microservices Patterns in Modern Python* (Circuit Breaker with `httpx` & `tenacity`, Strategy with Pydantic v2 & `typing.Protocol`, Repository pattern).
  2. *AI & Agentic Design Patterns in Python* (Semantic Router, Supervisor-Worker hierarchy, Evaluator-Optimizer self-correction loop).
  3. *Visual Architecture* (Mermaid state machines for circuit breakers and multi-agent coordination loops).
  4. *Comparative Trade-off Analysis* (Deterministic software engineering vs stochastic LLM agentic patterns).

## Capabilities

### New Capabilities
- `curriculum-taxonomy`: Defines the track structure, folder layout, naming conventions, and co-located artifact hierarchy across all four engineering domains.
- `module-contract`: Defines the mandatory 4-part pedagogical structure, frontmatter metadata schema, diagramming standards, and automated structural validation for every module.

### Modified Capabilities
None (initial greenfield project).

## Impact

- **Filesystem Layout**: Creates top-level `tracks/`, `templates/`, and `shared/` directories.
- **Tooling & CI**: Adds automated Python-based structural validation for module linting.
- **Documentation & Authorship**: All future module authors and AI generation agents must adhere to the 4-part module specification.
