# Design: Master Blueprint & Modular Taxonomy

## Context

See `proposal.md` for motivation and background. This design establishes the concrete architecture, file tree, validation tooling, and template structures needed to build and scale an enterprise-grade engineering curriculum across four tracks: Cloud-Native Infrastructure, AI Models & Inference, Modern Data Layers, and Agentic Workflows.

## Goals / Non-Goals

**Goals:**
- Provide a clean, extensible filesystem layout allowing independent authoring across tracks.
- Enforce the 4-part pedagogical contract deterministically via automated linting.
- Co-locate narrative documentation, diagrams (Mermaid/ASCII), and production artifacts (K8s manifests, code).
- Implement a reusable, fully annotated canonical module template.
- Implement an automated Python-based structural linter (`validate-module.py`).
- Implement an end-to-end cloud-native pilot module (`tracks/01-cloud-native-infra/01-keda-autoscaling-patterns/`) demonstrating KEDA autoscaling and manifest co-location.
- Implement a dedicated design patterns module (`tracks/04-agentic-workflows/01-design-patterns-ai-cloud-native/`) contrasting classic resilience patterns with modern AI agentic patterns in Python.

**Non-Goals:**
- Deploying a frontend static site generator (e.g., Docusaurus, Astro) in this initial phase; content will be pure GitHub Flavored Markdown with standard Mermaid rendering, compatible with future SSG ingestion.
- Creating all curriculum modules at once; this design establishes the framework and pilot modules.

## Decisions

### 1. Hierarchical Track-and-Module Directory Layout
- **Decision:** Organize by four top-level tracks (`tracks/01-cloud-native-infra`, `tracks/02-ai-models-inference`, `tracks/03-modern-data-layers`, `tracks/04-agentic-workflows`). Within each track, modules use zero-padded two-digit numbering prefixes (e.g., `01-keda-autoscaling-patterns/`).
- **Rationale:** Mirrors high-end educational platforms (Educative, Coursera, O'Reilly) while maintaining natural sorting in file trees and IDEs.
- **Alternatives Considered:**
  - *Flat Alphanumeric Catalog (`modules/CNI-101-...`)*: Decouples tracks from folder paths, but makes browsing and syllabus progression much less intuitive for human readers.

### 2. Co-Located Module Artifacts vs Central Assets
- **Decision:** Co-locate companion files within each module folder:
  ```
  tracks/<track-id>/<module-slug>/
  |-- index.md
  |-- diagrams/
  `-- artifacts/
  ```
- **Rationale:** Keeps each module self-contained and modular. Moving, renaming, or exporting a module keeps all its manifests and diagrams intact without broken relative paths.
- **Alternatives Considered:**
  - *Global `assets/` or `examples/` directory*: Causes high coupling and risk of orphaned manifests as the curriculum scales.

### 3. Lightweight Python Validation Linter (`validate-module.py`)
- **Decision:** Build a standalone Python script utilizing standard library modules (`yaml` / `re` fallback, `argparse`, `pathlib`) located at `shared/scripts/validate-module.py`.
- **Rationale:** Zero external dependencies beyond standard Python, fast execution in local hooks or CI, and direct inspection of frontmatter keys and the 4 required markdown section headers.
- **Alternatives Considered:**
  - *Heavy Node.js/Markdown AST tool*: Adds npm dependency management and node version requirements to an otherwise documentation/manifest repo.

### 4. Diagramming Standards (Dual Mermaid & ASCII)
- **Decision:** Mandate Mermaid.js diagrams with clean ASCII fallback representation where appropriate, enforcing control plane vs. data plane boundary delineation.
- **Rationale:** Mermaid renders natively in GitHub, GitLab, and all modern markdown viewers, while ASCII diagrams provide immediate, deterministic CLI and terminal visualization.

### 5. Standard Module Template Structure
- **Decision:** Provide `templates/module-template.md` containing boilerplate YAML frontmatter and the 4 mandatory sections with annotated developer prompts.

### 6. Design Patterns in AI & Cloud-Native Era Module Architecture
- **Decision:** Establish `tracks/04-agentic-workflows/01-design-patterns-ai-cloud-native/` to bridge traditional software architecture and stochastic AI engineering through production Python (`httpx`, `tenacity`, Pydantic v2).
- **Chapter Breakdown:**
  1. *Interactive Concept Breakdown*: Evolution from deterministic state machines to stochastic reasoning loops; why classic Gang of Four and microservices patterns fail when LLMs hallucinate or stall.
  2. *Visual Architecture*: Mermaid diagrams illustrating:
     - Circuit Breaker state transitions (`Closed` -> `Open` -> `Half-Open`) with fallback handling.
     - Semantic Router topology (intent classification -> specialized model/prompt workers).
     - Supervisor-Worker hierarchical delegation and state handoff.
     - Evaluator-Optimizer feedback loop (Generator -> Evaluator Judge -> Correction).
  3. *Production Python Code*:
     - *Classic Microservices Patterns*: Circuit Breaker with `tenacity` & `httpx`, Strategy pattern using Pydantic v2 & `typing.Protocol`, async Repository pattern.
     - *AI & Agentic Patterns*: Semantic Router with typed confidence thresholds, Supervisor-Worker orchestrator with structured outputs, Evaluator-Optimizer self-correction loop.
  4. *Edge Cases & Trade-offs*:
     - Comparative decision matrix: Traditional Deterministic Patterns vs LLM-Driven Stochastic Patterns.
     - Production failure modes: Infinite self-correction loops, context window saturation, retry storm amplification, and token quota exhaustion.
- **Rationale:** Software engineers need an authoritative mental model mapping familiar enterprise patterns (resilience, interfaces, repositories) to emerging agentic constructs (routers, supervisors, judges) using idiomatic Python.

## Risks / Trade-offs

- **[Risk] Authors omitting edge cases or trade-offs in rush to complete topics** → **Mitigation:** The automated linter strictly requires Section 4 with table syntax, and PR reviews will check against the `module-contract` spec.
- **[Risk] Track numbering collisions if curriculum reorganizes** → **Mitigation:** Two-digit prefixes (`01-`, `02-`) allow clean ordering; sub-modules or updates can use decimals (`01.1-`) if re-indexing is avoided.
- **[Risk] Code snippets drifting out of sync with actual cloud-native tool versions** → **Mitigation:** Manifests and Python scripts in `artifacts/` are standalone, syntax-checked files that can be executed directly.
- **[Risk] Non-deterministic LLM agent patterns getting stuck in infinite loops** → **Mitigation:** Code examples must enforce hard iteration caps, token budgets, and deterministic circuit breakers.

## Migration Plan

1. Create core directories (`tracks/`, `templates/`, `shared/scripts/`).
2. Implement `templates/module-template.md` with complete pedagogical annotations.
3. Implement `shared/scripts/validate-module.py` and verify test cases.
4. Scaffold track `README.md` files for all four tracks with syllabi and module roadmap.
5. Implement the cloud-native pilot module `tracks/01-cloud-native-infra/01-keda-autoscaling-patterns/`.
6. Implement the design patterns module `tracks/04-agentic-workflows/01-design-patterns-ai-cloud-native/`.
7. Run `validate-module.py` against both modules to ensure 100% compliance.
