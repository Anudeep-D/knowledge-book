# Tasks

## 1. Base Directory Scaffolding & Track Overviews

- [x] 1.1 Create top-level directories (`tracks/`, `templates/`, `shared/scripts/`) and verify filesystem presence
- [x] 1.2 Scaffold track overview syllabi (`README.md`) for all four core tracks (`01-cloud-native-infra`, `02-ai-models-inference`, `03-modern-data-layers`, `04-agentic-workflows`) and verify syllabus roadmaps

## 2. Canonical Module Template & Automated Validation Tool

- [x] 2.1 Implement `templates/module-template.md` containing strict YAML frontmatter, instructional scaffolding, and headers for the 4 mandatory sections
- [x] 2.2 Implement `shared/scripts/validate-module.py` to validate module frontmatter, header hierarchy, and required subdirectories, verifying with unit validation runs

## 3. Reference Pilot Module: KEDA Autoscaling Patterns

- [x] 3.1 Scaffold `tracks/01-cloud-native-infra/01-keda-autoscaling-patterns/` directory structure (`index.md`, `diagrams/`, `artifacts/`)
- [x] 3.2 Author Section 1: "Interactive Concept Breakdown" (production failure scenario, mental model, and KEDA architectural invariants)
- [x] 3.3 Author Section 2: "Visual Architecture" (ASCII and Mermaid diagrams illustrating control plane vs. data plane split, metrics scraping, and reconciliation loops)
- [x] 3.4 Author Section 3: "Real-World Code & Configuration" (co-located production manifests including `ScaledObject`, `TriggerAuthentication`, and resilient Kubernetes deployment)
- [x] 3.5 Author Section 4: "Edge Cases, Failure Modes & Trade-offs" (comparative decision matrix and SRE operational runbook for metric lag and cooldown flapping)

## 4. Dedicated Module: Design Patterns in AI & Cloud-Native Era (Python)

- [x] 4.1 Scaffold `tracks/04-agentic-workflows/01-design-patterns-ai-cloud-native/` directory structure (`index.md`, `diagrams/`, `artifacts/`)
- [x] 4.2 Author Section 1: "Interactive Concept Breakdown" (shift from deterministic state machines to stochastic reasoning loops, failure boundaries of classic patterns)
- [x] 4.3 Author Section 2: "Visual Architecture" (Mermaid diagrams for Circuit Breaker, Semantic Router, Supervisor-Worker hierarchy, and Evaluator-Optimizer loop)
- [x] 4.4 Author Section 3: "Real-World Code & Configuration" (production Python snippets in `artifacts/`: Circuit Breaker with `tenacity`/`httpx`, Strategy/Repository with Pydantic v2, Semantic Router, Supervisor-Worker, Evaluator-Optimizer)
- [x] 4.5 Author Section 4: "Edge Cases, Failure Modes & Trade-offs" (comparative decision table: Traditional Deterministic Patterns vs LLM-Driven Agentic Patterns, infinite loops, and token budget runbooks)

## 5. End-to-End Verification & Validation

- [x] 5.1 Run `shared/scripts/validate-module.py` across all created track modules and verify exit code 0 with clean validation output
- [x] 5.2 Validate Python scripts and manifest syntax across all modules for syntax correctness
