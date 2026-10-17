# Design: Track 04 Orchestration & Agent Workflows Architecture

## Context

See `proposal.md` for motivation. Track 04 currently contains a single reference module (`01-design-patterns-ai-cloud-native`). This design specifies the technical architecture, directory layouts, companion code artifacts, and pedagogical structures for expanding Track 04 with three new modules:
- `02-data-workflow-orchestration-prefect`
- `03-agentic-topologies-state-machines`
- `04-production-guardrails-evals`

All modules must strictly adhere to the repository's `module-contract` specification: exactly four numbered sections ("1. Interactive Concept Breakdown", "2. Visual Architecture", "3. Real-World Code & Configuration", and "4. Edge Cases, Failure Modes & Trade-offs"), companion `artifacts/` and `diagrams/` folders, and 100% compliance with `shared/scripts/validate-module.py`.

## Goals / Non-Goals

**Goals:**
- Provide complete, in-depth architectural guides for modern distributed AI workflows, cyclic state machines, and production evaluation loops.
- Deliver runnable, production-quality Python 3.11+ companion code (with Pydantic v2 schemas, type annotations, and error handling) and enterprise Kubernetes manifests.
- Embed clear ASCII and Mermaid diagrams separating control plane from data plane execution and mapping state transitions.
- Establish comprehensive comparative trade-off matrices and failure-mode triage runbooks for each topic.

**Non-Goals:**
- Creating a proprietary agent framework; the curriculum focuses on industry standards (Prefect 3.x, LangGraph, Pydantic v2, OpenTelemetry).
- Deploying live cloud infrastructure or spinning up active cloud clusters during curriculum builds.

## Decisions

### 1. Prefect 3.x as the AI Workflow Engine
- **Decision**: Adopt Prefect 3.x for data pipeline orchestration over Apache Airflow and Celery.
- **Rationale**: AI workloads require dynamic task mapping (`.map()`) based on runtime chunk counts, content-hash caching (`cache_key_fn`) to avoid re-embedding identical text, and lightweight ephemeral execution on Kubernetes work pools rather than heavy static DAG schedulers.
- **Alternatives Considered**:
  - *Apache Airflow 2.x*: Strong for traditional scheduled ETL, but static DAG parsing and heavy worker architectures make dynamic sub-chunk fan-out cumbersome.
  - *Temporal / Cadence*: Excellent event-sourcing and replay capabilities, but introduces higher operational complexity for data-heavy batch RAG ingestion.

### 2. LangGraph for Multi-Agent Cyclic Topologies
- **Decision**: Standardize on LangGraph for stateful agentic workflows.
- **Rationale**: Classical ReAct loops and simple linear chains fail in production due to runaway recursion and unmanaged state. LangGraph provides formal cyclic state graphs, immutable state reducers (`operator.add`), checkpoint persistence (`MemorySaver` / `PostgresSaver`), and first-class human-in-the-loop interruption gates (`interrupt_before`).
- **Alternatives Considered**:
  - *CrewAI*: High-level role-playing abstraction, but less granular control over low-level state transitions, time-travel debugging, and explicit graph cycle prevention.
  - *Custom Python State Machine*: Maximum control, but requires reinventing checkpoint persistence, time-travel state updates, and visualization adapters.

### 3. Multi-Layer Guardrails, Constrained Decoding & OpenTelemetry
- **Decision**: Implement a defense-in-depth guardrails architecture combining Pydantic v2 strict models, self-correction repair loops, OpenTelemetry GenAI semantic tracing, and RAG Triad evaluation metrics.
- **Rationale**: Prompting alone cannot guarantee valid JSON or prevent SQL injection. In-flight schema enforcement paired with automated repair and OpenTelemetry GenAI spans provides deterministic boundary guarantees and end-to-end auditability.
- **Alternatives Considered**:
  - *Pure Vendor JSON Mode*: Convenient but locks the system to specific proprietary APIs; lacks field-level custom regex and boundary assertion logic.
  - *External Gateway Only (e.g. LiteLLM proxy)*: Useful for rate limiting, but unable to inspect and repair application-level state schemas.

### 4. Directory & Module Structural Invariants
- **Decision**: Co-locate code and diagrams inside each module directory (`tracks/04-agentic-workflows/<module-slug>/`):
  - `index.md`: Full module text meeting the 4-part pedagogical contract.
  - `diagrams/`: Source diagrams (ASCII / Mermaid / PNGs).
  - `artifacts/`: Runnable Python scripts and Kubernetes manifests.

## Risks / Trade-offs

- **[Risk: Fast-evolving agent framework APIs]** → *Mitigation*: Emphasize architectural mental models, state machines, and standard typing protocols; pin dependencies and isolate framework-specific bindings.
- **[Risk: Module contract linter violations]** → *Mitigation*: Run `shared/scripts/validate-module.py` continuously across each new module directory before committing.
- **[Risk: Code snippets becoming toy-like]** → *Mitigation*: Strictly enforce production-grade patterns (security contexts, resource requests/limits, exponential backoff with jitter, error handling).

## Migration Plan

1. Update `tracks/04-agentic-workflows/README.md` to reflect the expanded curriculum roadmap.
2. Scaffold module `02-data-workflow-orchestration-prefect` with `index.md`, `artifacts/prefect_rag_pipeline.py`, and `artifacts/prefect_job_template.yaml`.
3. Scaffold module `03-agentic-topologies-state-machines` with `index.md`, `artifacts/supervisor_langgraph.py`, and `artifacts/hitl_checkpoint_agent.py`.
4. Scaffold module `04-production-guardrails-evals` with `index.md`, `artifacts/guarded_schema_repair.py`, and `artifacts/evals_otel_harness.py`.
5. Run `python3 shared/scripts/validate-module.py --all` to verify repository-wide contract compliance.
