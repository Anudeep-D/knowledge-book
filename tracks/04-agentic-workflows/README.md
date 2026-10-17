# Track 04: Agentic Workflows & Multi-Agent Architectures

## Overview

Welcome to **Track 04: Agentic Workflows & Multi-Agent Architectures**. This track bridges traditional distributed software design and stochastic, LLM-driven autonomous systems. It is dedicated to designing resilient, cost-bounded, and deterministic multi-agent architectures using production Python.

As software shifts from rigid imperative pipelines to goal-oriented agentic workflows, software engineers need proven design patterns, control structures, observability primitives, and evaluation loops to tame non-deterministic outputs.

---

## Pedagogical Philosophy

1. **Deterministic Foundations for Stochastic Systems:** Why classic microservice patterns (Circuit Breaker, Strategy, Repository) remain essential when wrapped around LLMs, and where they break down.
2. **Visual Agent Topologies:** Mermaid sequence diagrams, state machines, and flowcharts modeling reasoning loops, supervisor-worker handoffs, and evaluator-optimizer iterations.
3. **Clean, Production Python:** Battle-tested asynchronous implementations utilizing modern Python tooling (`httpx`, `tenacity`, Pydantic v2, `asyncio`, typing protocols) without framework bloat.
4. **Deterministic vs. Stochastic Trade-off Matrices:** Rigorous tables contrasting traditional software design with agentic counterparts, token budget guardrails, and runaway loop mitigations.

---

## Curriculum Roadmap

```
+--------------------------------------------------------------------------+
|                     AGENTIC WORKFLOWS CURRICULUM ROADMAP                 |
+--------------------------------------------------------------------------+
|  01. Design Patterns in the AI & Cloud-Native Era (Python)              |
|      (Classic Resilience vs Agentic Patterns: Circuit Breaker, Router,  |
|       Supervisor-Worker, Evaluator-Optimizer, Pydantic v2 Contracts)    |
|                                                                          |
|  02. ReAct Reasoning Loops & Structured Tool Calling                     |
|      (Thought-Action-Observation, Tool Registries, Schema Validation)    |
|                                                                          |
|  03. Multi-Agent Topologies & Hierarchical Orchestration                 |
|      (Orchestrator-Workers, Blackboard Patterns, Consensus Voting)       |
|                                                                          |
|  04. Agent Memory Architectures: Short-Term, Epistemic & Long-Term       |
|      (Buffer Windows, Summary Compaction, Vector Memory Retrieval)       |
|                                                                          |
|  05. Sandboxed Code Execution & Tool Safety                              |
|      (gVisor Containers, WebAssembly Sandboxes, Ephemeral Runner Pods)   |
|                                                                          |
|  06. Agentic Evaluations & Synthetic Benchmarks                          |
|      (LLM-as-a-Judge, Ground-Truth Trajectory Alignment, Cost Limits)    |
+--------------------------------------------------------------------------+
```

---

## Active & Upcoming Modules

| Module Slug | Status | Focus Areas | Key Artifacts |
| :--- | :--- | :--- | :--- |
| `01-design-patterns-ai-cloud-native` | **Active / Reference** | Classic vs Agentic patterns, Circuit Breaker, Supervisor-Worker, Evaluator-Optimizer | Production Python implementations (`circuit_breaker.py`, `semantic_router.py`, `supervisor_worker.py`, `evaluator_optimizer.py`) |
| `02-react-loops-tool-calling` | *Planned* | Dynamic tool selection, JSON schema repair | Python ReAct loop, tool registry |
| `03-multi-agent-orchestration` | *Planned* | LangGraph / Native graph state handoffs | State graph engine, worker agents |
| `04-agent-memory-hierarchies` | *Planned* | Semantic cache, episodic vector recall | Sliding window buffer, vector memory |
| `05-sandboxed-agent-execution` | *Planned* | Docker/gVisor sandboxed Python runner | Sandboxed runner service, safety checks |
| `06-agentic-evals-judge` | *Planned* | Metric assertions, synthetic benchmark suites | Evaluation harness, rubric scorer |

---

## Prerequisites & Tooling

- Advanced Python 3.10+ (type hints, `pydantic` v2, `asyncio`, decorators).
- Familiarity with LLM APIs (OpenAI, Anthropic, or local vLLM/Ollama endpoints).
- Understanding of microservices concepts (circuit breaking, retry policies, distributed state).
- Recommended environment: Python 3.11 virtual environment with `httpx`, `tenacity`, `pydantic`, `pytest`.
