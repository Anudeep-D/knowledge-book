# agentic-workflows-curriculum Specification

## Purpose

Defines the curriculum standards, syllabus requirements, and learning objectives for Track 04 covering data orchestration with Prefect, cyclic state graphs with LangGraph, and production guardrails with LLMOps evaluation loops.

## Requirements

### Requirement: Track 04 Syllabus Structure
The Track 04 syllabus SHALL provide four sequential modules covering classic versus agentic design patterns, distributed Prefect dataflows, LangGraph cyclic state machines, and production guardrails with evaluation loops.

#### Scenario: Track syllabus overview inspection
- **WHEN** `tracks/04-agentic-workflows/README.md` is inspected
- **THEN** it indexes modules 01 through 04 with title, status, difficulty level, prerequisites, and companion artifact references.

### Requirement: Prefect Dataflow Orchestration Module
The curriculum SHALL provide a dedicated data orchestration module in `tracks/04-agentic-workflows/02-data-workflow-orchestration-prefect` detailing dynamic task mapping, content-hash caching, and Kubernetes work pools for AI batch workloads.

#### Scenario: Prefect module structure verification
- **WHEN** `tracks/04-agentic-workflows/02-data-workflow-orchestration-prefect` is inspected
- **THEN** it contains an `index.md` satisfying the 4-part module contract and runnable Prefect 3.x Python pipelines in `artifacts/`.

### Requirement: LangGraph Cyclic State Topologies Module
The curriculum SHALL provide a dedicated agentic topologies module in `tracks/04-agentic-workflows/03-agentic-topologies-state-machines` detailing actor-model state graphs, supervisor-worker routing, and human-in-the-loop interruption gates.

#### Scenario: LangGraph module structure verification
- **WHEN** `tracks/04-agentic-workflows/03-agentic-topologies-state-machines` is inspected
- **THEN** it contains an `index.md` satisfying the 4-part module contract and runnable LangGraph state graphs with checkpoint persistence in `artifacts/`.

### Requirement: Production Guardrails and Evals Module
The curriculum SHALL provide a dedicated guardrails and observability module in `tracks/04-agentic-workflows/04-production-guardrails-evals` detailing Pydantic v2 strict schemas, self-correction repair loops, OpenTelemetry GenAI semantic tracing, and automated evaluation harnesses.

#### Scenario: Guardrails and evals module verification
- **WHEN** `tracks/04-agentic-workflows/04-production-guardrails-evals` is inspected
- **THEN** it contains an `index.md` satisfying the 4-part module contract and runnable guardrails, tracing spans, and evaluation assertions in `artifacts/`.
