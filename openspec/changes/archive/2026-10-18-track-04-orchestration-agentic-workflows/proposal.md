# Proposal: Track 04 Orchestration & Agent Workflows Curriculum

## Why

As software systems evolve from rigid, deterministic microservices to stochastic, LLM-driven autonomous systems, enterprise engineering teams lack rigorous architectural blueprints for managing non-deterministic workflows. Naive agent implementations suffer from runaway token spend, circular routing loops, brittle JSON parsing failures, and an absence of distributed task coordination. 

This change introduces Track 04's comprehensive curriculum structure across three core pillars:
1. **Data & Workflow Orchestration with Prefect 3.x:** Managing distributed, dynamic dataflows, token rate-limit retries, and content-hash caching for AI pipelines.
2. **Agentic Frameworks & Topologies with LangGraph:** Cyclic actor-model state machines, supervisor-worker topologies, typed state reducers, checkpoint persistence, and human-in-the-loop (HITL) gates.
3. **Production Guardrails & LLMOps Evals:** In-flight Pydantic v2 strict schema enforcement, self-correction repair loops, OpenTelemetry GenAI semantic tracing, and automated evaluation harnesses.

## What Changes

- **Update Track Syllabus**: Revise `tracks/04-agentic-workflows/README.md` to establish the formalized 4-module roadmap and prerequisite structure.
- **Module 02 (`02-data-workflow-orchestration-prefect`)**: Establish a complete Educative.io style module covering Prefect 3.x flows, dynamic task mapping (`.map()`), content-hash caching, and ephemeral Kubernetes work pools.
- **Module 03 (`03-agentic-topologies-state-machines`)**: Establish a complete Educative.io style module covering LangGraph cyclic graphs, supervisor-worker fan-out/fan-in, typed state reducers, and HITL interrupt gates.
- **Module 04 (`04-production-guardrails-evals`)**: Establish a complete Educative.io style module covering Pydantic v2 strict schema validation, self-correction repair loops, OpenTelemetry GenAI span tracing, and RAG Triad evaluation metrics.
- **Companion Artifacts & Schemas**: Provide runnable, production-ready Python implementations and Kubernetes manifests for all modules.

## Capabilities

### New Capabilities
- `agentic-workflows-curriculum`: Defines curriculum standards, syllabus structure, module contracts, and companion code benchmarks for Track 04 (Orchestration & Agent Workflows).

### Modified Capabilities
- `curriculum-taxonomy`: Updates Track 04 taxonomy requirements to include the full suite of orchestration, cyclic state graphs, and production guardrail modules.

## Impact

- **Curriculum Architecture**: Extends `tracks/04-agentic-workflows` with modules 02, 03, and 04.
- **Tooling & Dependencies**: Python 3.11+, `prefect>=3.0`, `langgraph>=0.2.0`, `pydantic>=2.7.0`, `opentelemetry-api>=1.24.0`.
- **Validation**: Ensures all newly introduced modules pass the automated module contract linter (`shared/scripts/validate-module.py`).
