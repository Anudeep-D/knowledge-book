# Track 04: Agentic Workflows & Multi-Agent Architectures

## Overview

Welcome to **Track 04: Agentic Workflows & Multi-Agent Architectures**. This track bridges traditional distributed software design and stochastic, LLM-driven autonomous systems. It is dedicated to designing resilient, cost-bounded, and deterministic multi-agent architectures using production Python 3.11+.

As software shifts from rigid imperative pipelines to goal-oriented agentic workflows, software engineers need proven design patterns, control structures, distributed data orchestration, cyclic state graphs, and rigorous evaluation loops to tame non-deterministic outputs.

---

## Pedagogical Philosophy

1. **Deterministic Foundations for Stochastic Systems:** Why classic microservice patterns (Circuit Breaker, Strategy, Repository) remain essential when wrapped around LLMs, and where they break down.
2. **Visual Agent Topologies:** Mermaid sequence diagrams, state machines, and flowcharts modeling reasoning loops, supervisor-worker handoffs, and evaluator-optimizer iterations.
3. **Clean, Production Python:** Battle-tested asynchronous implementations utilizing modern Python tooling (`httpx`, `tenacity`, Pydantic v2, `asyncio`, typing protocols) without framework bloat.
4. **Deterministic vs. Stochastic Trade-off Matrices:** Rigorous tables contrasting traditional software design with agentic counterparts, token budget guardrails, and runaway loop mitigations.

---

## Curriculum Roadmap

```
+----------------------------------------------------------------------------------------------------+
|                         TRACK 04: ORCHESTRATION & AGENT WORKFLOWS ROADMAP                          |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  01. Design Patterns in the AI & Cloud-Native Era (Python)                                         |
|      (Classic Resilience vs Agentic Patterns: Circuit Breaker, Router,                             |
|       Supervisor-Worker, Evaluator-Optimizer, Pydantic v2 Contracts)                               |
|                                                                                                    |
|  02. Data & Workflow Orchestration with Prefect                                                    |
|      (Dynamic Task Mapping [.map()], Content-Hash Caching, Kubernetes Work Pools,                  |
|       Token Concurrency Governance, Exponential Jitter Retries)                                    |
|                                                                                                    |
|  03. Agentic Topologies & Cyclic State Machines with LangGraph                                     |
|      (Actor-Model State Graphs, Supervisor-Worker Fan-Out/Fan-In, State Reducers,                  |
|       PostgreSQL/Memory Checkpointing, Human-in-the-Loop Interruption Gates)                        |
|                                                                                                    |
|  04. Production Guardrails, Structured Outputs & LLMOps Evaluation Loops                           |
|      (Pydantic v2 Strict Mode, LLM Self-Correction Loops, Ingress/Egress Guardrails,                |
|       OpenTelemetry GenAI Semantic Spans, RAG Triad Automated Evaluation Harness)                   |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

---

## Active & Core Curriculum Modules

| Module Slug | Status | Focus Areas | Key Artifacts |
| :--- | :--- | :--- | :--- |
| [`01-design-patterns-ai-cloud-native`](./01-design-patterns-ai-cloud-native/index.md) | **Active / Reference** | Classic vs Agentic patterns, Circuit Breaker, Supervisor-Worker, Evaluator-Optimizer | `classic_resilience.py`, `agentic_patterns.py` |
| [`02-data-workflow-orchestration-prefect`](./02-data-workflow-orchestration-prefect/index.md) | **Active** | Dynamic task mapping (`.map()`), content-hash caching, K8s work pool pods, token limits | `prefect_rag_pipeline.py`, `prefect_job_template.yaml` |
| [`03-agentic-topologies-state-machines`](./03-agentic-topologies-state-machines/index.md) | **Active** | Cyclic state graphs, supervisor-worker routing, checkpoint persistence, HITL gates | `supervisor_langgraph.py`, `hitl_checkpoint_agent.py` |
| [`04-production-guardrails-evals`](./04-production-guardrails-evals/index.md) | **Active** | Pydantic v2 strict schemas, self-correction repair, OpenTelemetry GenAI spans, RAG Triad evals | `guarded_schema_repair.py`, `evals_otel_harness.py` |

---

## Prerequisites & Tooling

- Advanced Python 3.11+ (type hints, `pydantic` v2, `asyncio`, decorators, typing protocols).
- Orchestration & Graph Engines: `prefect>=3.0`, `langgraph>=0.2.0`, `langchain-core>=0.2.0`.
- Observability & Resilience: `opentelemetry-api>=1.24.0`, `tenacity>=8.2.0`, `httpx>=0.27.0`.
- Testing & Verification: `pytest>=8.0.0`, `pytest-asyncio>=0.23.0`.
